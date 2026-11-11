"""Executable *toy-data* Phase 0 KPI contract; NOT an REES46 production ETL.

All KPI ratios are fractions in [0,1], not percentages.
Session identity = (user_id, user_session), timestamps parsed as UTC.
Half-open observation window; no inferred order_id or campaign effectiveness.
"""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timezone
from typing import Iterable, Mapping

VALID_EVENTS = frozenset({"view", "cart", "remove_from_cart", "purchase"})


def utc(dt: str) -> datetime:
    """Parse ISO 8601 UTC string, accepting Z; require offset to prevent time drift."""
    value = datetime.fromisoformat(dt.replace("Z", "+00:00"))
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Event timestamp must be timezone-aware")
    return value.astimezone(timezone.utc)


def _between(row: Mapping, start: datetime, end: datetime) -> bool:
    return start <= utc(str(row["event_time"])) < end


def _key(row: Mapping):
    user, session = row.get("user_id"), row.get("user_session")
    if user is None or str(user).strip() == "" or session is None or str(session).strip() == "":
        return None
    return (str(user), str(session))


def session_metrics(rows: Iterable[Mapping], start: str, end: str) -> dict:
    """Calculate three session KPI ratios; strict event-time ordering for cart->purchase."""
    begin, finish = utc(start), utc(end)
    if finish <= begin:
        raise ValueError("Window end must be > start")
    events = defaultdict(list)
    for row in rows:
        if row.get("event_type") not in VALID_EVENTS:
            continue
        if not _between(row, begin, finish):
            continue
        key = _key(row)
        if key is not None:
            events[key].append((utc(str(row["event_time"])), row["event_type"]))
    total = len(events)
    purchasing = 0
    carting = 0
    after_cart = 0
    for group in events.values():
        purchases = [t for t, event in group if event == "purchase"]
        carts = [t for t, event in group if event == "cart"]
        if purchases:
            purchasing += 1
        if carts:
            carting += 1
            if purchases and max(purchases) > min(carts):
                after_cart += 1
    return {
        "valid_sessions": total,
        "purchase_sessions_proxy": purchasing,
        "cart_sessions": carting,
        "cart_then_purchase_sessions": after_cart,
        "purchase_session_rate": purchasing / total if total else None,
        "cart_session_rate": carting / total if total else None,
        "cart_to_purchase_same_session_rate": after_cart / carting if carting else None,
    }


def repeat_buyer_rate_proxy(rows: Iterable[Mapping], start: str, end: str) -> float | None:
    """Buyer denominator contains ONLY buyers with >=1 valid purchase session."""
    begin, finish = utc(start), utc(end)
    user_sessions = defaultdict(set)
    for row in rows:
        if row.get("event_type") == "purchase" and _between(row, begin, finish):
            key = _key(row)
            if key is not None:
                user_sessions[key[0]].add(key[1])
    if not user_sessions:
        return None
    return sum(len(sessions) >= 2 for sessions in user_sessions.values()) / len(user_sessions)


def activity_ratio(sessions_recent: int, sessions_previous: int) -> float:
    if min(sessions_recent, sessions_previous) < 0:
        raise ValueError("session counts must be non-negative")
    return (sessions_recent + 1) / (sessions_previous + 1)


def activity_delta(sessions_recent: int, sessions_previous: int) -> int:
    if min(sessions_recent, sessions_previous) < 0:
        raise ValueError("session counts must be non-negative")
    return sessions_recent - sessions_previous


def buyer_rfm_metrics(rows: Iterable[Mapping], cutoff: str, start: str) -> dict[str, dict]:
    """Calculate RFM metrics per buyer strictly within [start, cutoff).
    
    Non-buyers are excluded completely (they do not receive recency=0 or 999).
    Frequency is distinct valid purchase sessions proxy.
    Monetary is sum of validated purchase event prices.
    """
    begin, finish = utc(start), utc(cutoff)
    if finish <= begin:
        raise ValueError("Cutoff must be strictly after start")
    
    buyer_purchases = defaultdict(list)
    buyer_sessions = defaultdict(set)
    buyer_monetary = defaultdict(float)
    
    for row in rows:
        if row.get("event_type") != "purchase":
            continue
        if not _between(row, begin, finish):
            continue
        
        user = row.get("user_id")
        if user is None or str(user).strip() == "":
            continue
        u_str = str(user)
        
        t = utc(str(row["event_time"]))
        buyer_purchases[u_str].append(t)
        
        # Session proxy
        session = row.get("user_session")
        if session is not None and str(session).strip() != "":
            buyer_sessions[u_str].add(str(session))
            
        # Price summation
        price = row.get("price", 0.0)
        try:
            val = float(price) if price is not None else 0.0
            if val > 0:
                buyer_monetary[u_str] += val
        except (ValueError, TypeError):
            pass
            
    result = {}
    for u_str, timestamps in buyer_purchases.items():
        max_t = max(timestamps)
        recency_days = (finish - max_t).total_seconds() / 86400.0
        result[u_str] = {
            "recency_days": recency_days,
            "purchase_sessions_proxy": len(buyer_sessions[u_str]),
            "monetary_observed": round(buyer_monetary[u_str], 2),
        }
    return result

