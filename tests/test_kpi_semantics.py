"""Synthetic Phase 0 contract tests — NOT research/EDA observations."""
import unittest
from src.contracts.kpi_semantics import (
    session_metrics,
    repeat_buyer_rate_proxy,
    activity_ratio,
    activity_delta,
    buyer_rfm_metrics,
    utc,
)

START = "2019-10-01T00:00:00Z"
END = "2020-02-01T00:00:00Z"


def event(user, session, kind, time, price=0.0):
    return {
        "user_id": user,
        "user_session": session,
        "event_type": kind,
        "event_time": time,
        "price": price,
    }


class KPIContractTest(unittest.TestCase):
    def setUp(self):
        self.rows = [
            event("u1", "s1", "view", "2020-01-15T12:00:00Z"),
            event("u1", "s1", "cart", "2020-01-15T12:01:00Z"),
            event("u1", "s1", "purchase", "2020-01-15T12:02:00Z", price=10.5),
            event("u1", "s1", "purchase", "2020-01-15T12:02:30Z", price=15.0), # 2 purchase events same session => proxy frequency 1, sum price 25.5
            event("u1", "s2", "purchase", "2020-01-20T11:00:00Z", price=20.0), # session 2, price 20
            event("u2", "s3", "cart", "2020-01-25T11:00:00Z"),
            event("u2", "s3", "view", "2020-01-25T11:01:00Z"),
            event("u3", "s4", "view", "2020-01-26T09:00:00Z"),
            event("u3", None, "purchase", "2020-01-27T09:00:00Z", price=5.0), # missing session excluded from session KPI
            event("u2", "s5", "purchase", "2020-02-01T00:00:00Z", price=50.0), # future boundary excluded from observation
            event("u3", "s6", "cart", "2019-09-30T23:59:59Z"), # too early
        ]

    def test_session_denominators_and_proxy_order(self):
        x = session_metrics(self.rows, START, END)
        self.assertEqual(x["valid_sessions"], 4)
        self.assertEqual(x["purchase_sessions_proxy"], 2)
        self.assertEqual(x["cart_sessions"], 2)
        self.assertEqual(x["cart_then_purchase_sessions"], 1)
        self.assertEqual(x["purchase_session_rate"], .5)
        self.assertEqual(x["cart_session_rate"], .5)
        self.assertEqual(x["cart_to_purchase_same_session_rate"], .5)

    def test_frequency_distinct_sessions(self):
        # Only u1 has valid purchase sessions: s1 and s2 => repeat buyer proxy rate = 1
        self.assertEqual(repeat_buyer_rate_proxy(self.rows, START, END), 1.0)

    def test_half_open_cutoff_and_missing_session(self):
        x = session_metrics(self.rows, START, END)
        self.assertNotEqual(x["valid_sessions"], 5)
        self.assertEqual(x["purchase_sessions_proxy"], 2)

    def test_cart_purchase_strict_temporal_order(self):
        rows = [event("u", "s", "purchase", "2020-01-01T08:00:00Z"), event("u", "s", "cart", "2020-01-01T09:00:00Z")]
        x = session_metrics(rows, START, END)
        self.assertEqual(x["cart_to_purchase_same_session_rate"], 0.0)

    def test_ratio_zero_policy(self):
        x = session_metrics([], START, END)
        self.assertIsNone(x["purchase_session_rate"])
        self.assertIsNone(x["cart_to_purchase_same_session_rate"])
        self.assertIsNone(repeat_buyer_rate_proxy([], START, END))

    def test_ratio_smoothing(self):
        self.assertEqual(activity_ratio(0, 0), 1.0)
        self.assertAlmostEqual(activity_ratio(10, 0), 11.0)
        self.assertAlmostEqual(activity_ratio(5, 20), 6/21)
        with self.assertRaises(ValueError):
            activity_ratio(-1, 2)
        self.assertEqual(activity_delta(10, 5), 5)
        self.assertEqual(activity_delta(5, 20), -15)
        self.assertEqual(activity_delta(0, 0), 0)
        with self.assertRaises(ValueError):
            activity_delta(-1, 0)

    def test_buyer_rfm_semantics(self):
        rfm = buyer_rfm_metrics(self.rows, cutoff=END, start=START)
        # u1 is buyer with 2 purchase sessions (s1, s2), last purchase at 2020-01-20T11:00:00Z
        self.assertIn("u1", rfm)
        # u2 has only cart/view before cutoff; purchase at 2020-02-01T00:00:00Z is in holdout => u2 is non-buyer in observation
        self.assertNotIn("u2", rfm)
        # u1 recency: from 2020-01-20T11:00:00Z to 2020-02-01T00:00:00Z is 11 days + 13 hours = 11.5416666... days
        self.assertAlmostEqual(rfm["u1"]["recency_days"], 11.541666666, places=4)
        # u1 frequency: 2 distinct purchase sessions, NOT 3 purchase events
        self.assertEqual(rfm["u1"]["purchase_sessions_proxy"], 2)
        # u1 monetary: 10.5 + 15.0 + 20.0 = 45.5
        self.assertEqual(rfm["u1"]["monetary_observed"], 45.5)

    def test_utc_required(self):
        with self.assertRaises(ValueError):
            utc("2020-01-01T00:00:00")

if __name__ == "__main__":
    unittest.main()
