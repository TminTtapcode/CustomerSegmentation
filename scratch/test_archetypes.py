import sys, os
sys.path.insert(0, os.path.abspath("."))
from src.decision_engine.rules import MarketingDecisionRules

rules = MarketingDecisionRules()

archetypes = [
    {
        "name": "1. Active Core VIP",
        "evidence": {
            "user_id": "VIP_001", "is_buyer": True, "cluster": 1,
            "recency_days": 10.5, "frequency": 4, "monetary": 185.50,
            "sessions_30d": 8, "views_30d": 32, "cart_sessions_30d": 0, "log_activity_ratio": 1.2
        }
    },
    {
        "name": "2. Slackening VIP",
        "evidence": {
            "user_id": "VIP_002", "is_buyer": True, "cluster": 1,
            "recency_days": 25.0, "frequency": 3, "monetary": 120.00,
            "sessions_30d": 1, "views_30d": 3, "cart_sessions_30d": 0, "log_activity_ratio": -0.5
        }
    },
    {
        "name": "3. Recent Single Buyer Browsing",
        "evidence": {
            "user_id": "BUYER_003", "is_buyer": True, "cluster": 3,
            "recency_days": 15.0, "frequency": 1, "monetary": 28.00,
            "sessions_30d": 4, "views_30d": 12, "cart_sessions_30d": 0, "log_activity_ratio": 1.1
        }
    },
    {
        "name": "4. At-Risk Moderate Spender Cooling Down",
        "evidence": {
            "user_id": "BUYER_004", "is_buyer": True, "cluster": 2,
            "recency_days": 55.0, "frequency": 1, "monetary": 68.50,
            "sessions_30d": 0, "views_30d": 0, "cart_sessions_30d": 0, "log_activity_ratio": -0.8
        }
    },
    {
        "name": "5. Non-Buyer High-Intent",
        "evidence": {
            "user_id": "NB_005", "is_buyer": False, "cluster": None,
            "recency_days": None, "frequency": None, "monetary": None,
            "sessions_30d": 3, "views_30d": 8, "cart_sessions_30d": 2, "carts_30d": 3, "log_activity_ratio": 0.5
        }
    },
    {
        "name": "6. Non-Buyer Explorer",
        "evidence": {
            "user_id": "NB_006", "is_buyer": False, "cluster": None,
            "recency_days": None, "frequency": None, "monetary": None,
            "sessions_30d": 3, "views_30d": 14, "cart_sessions_30d": 0, "carts_30d": 0, "log_activity_ratio": 0.4
        }
    },
    {
        "name": "7. Deep Dormant Bouncer (Guardrail G3 Triggered)",
        "evidence": {
            "user_id": "BUYER_007", "is_buyer": True, "cluster": 0,
            "recency_days": 95.0, "frequency": 1, "monetary": 12.50,
            "sessions_30d": 0, "views_30d": 0, "cart_sessions_30d": 0, "log_activity_ratio": 0.0
        }
    },
    {
        "name": "8. VIP with Active Cart (Guardrail G4 Precedence)",
        "evidence": {
            "user_id": "VIP_008", "is_buyer": True, "cluster": 1,
            "recency_days": 12.0, "frequency": 5, "monetary": 240.00,
            "sessions_30d": 6, "views_30d": 20, "cart_sessions_30d": 2, "log_activity_ratio": 0.8
        }
    }
]

for arch in archetypes:
    rec = rules.evaluate_customer(arch["evidence"])
    print(f"\n=== {arch['name']} ===")
    print(f"Cohort: {rec['cohort']} | Segment: {rec['segment_id']}")
    print(f"Goal: {rec['marketing_goal']} ({rec['marketing_goal_name_vi']})")
    print(f"Tactic: {rec['recommended_tactic']} ({rec['recommended_tactic_name_vi']})")
    print(f"Alternatives: {rec['alternative_tactics']}")
    print(f"Reason: {rec['human_readable_reason']}")
    print(f"Reason Codes: {rec['reason_codes']}")
    print(f"Guardrails: {rec['guardrails_applied']}")
    print(f"KPIs: {rec['evaluation_kpis']}")
