"""
Script: scripts/build_phase7_snapshot.py
Purpose: Export verified, aggregated, and anonymized analytics snapshots
         for the IVRE Owner Research Dashboard.
Strict Constraints:
  - Never dump 1.34M raw customer rows into browser JSON.
  - Export structured aggregated metrics, distributions, and anonymized samples.
  - Strict namespace separation: Observation vs. Historical Holdout vs. Marketing Decisions.
  - Mask all personal identifiers (anonymized demo IDs only).
  - Versioned contract and SHA-256 manifest.
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime, timezone
import duckdb

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def build_snapshots():
    t0 = time.perf_counter()
    print("=" * 75)
    print("PHASE 7: BUILDING VERIFIED ANALYTICS DASHBOARD SNAPSHOTS")
    print("=" * 75)

    output_dir = "outputs/dashboard"
    os.makedirs(output_dir, exist_ok=True)
    con = duckdb.connect()

    # 1. METADATA & DATA QUALITY
    print("\n[1/7] Building Metadata & Data Quality Overview...")
    metadata = {
        "schema_version": "v1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_dataset": "REES46 eCommerce Events (Cosmetics Category)",
        "source_period": "2019-10-01 to 2020-02-29 (152 days)",
        "observation_window": {
            "start": "2019-10-01T00:00:00Z",
            "cutoff": "2020-02-01T00:00:00Z",
            "duration_days": 123
        },
        "holdout_window": {
            "start": "2020-02-01T00:00:00Z",
            "end": "2020-03-01T00:00:00Z",
            "duration_days": 29,
            "evaluation_type": "Out-of-Time Historical Validation"
        },
        "disclaimer": "REES46 Cosmetics Research Demo — Historical Data 2019–2020. Read-only Research Analytics. Not live IVRE fashion customers.",
        "data_quality_summary": {
            "raw_events": 20692840,
            "deduplicated_events": 1109098,
            "clean_events": 19583742,
            "observation_events": 15667350,
            "holdout_events": 3916392,
            "compression_ratio": "4.92x (CSV 2,321 MB -> Parquet 471.7 MB)",
            "benchmark_speedup": "8.09x median query speedup",
            "user_id_missing_rate": 0.0,
            "user_session_missing_rate": 0.00022,
            "purchase_session_proxy_validity": "100.0% purchases have valid session"
        }
    }

    # 2. CUSTOMER OVERVIEW & FUNNEL
    print("[2/7] Extracting Customer Overview & Behavioral Funnel...")
    customer_overview = {
        "total_observed_customers": 1341499,
        "buyers_count": 92652,
        "buyers_percentage": 6.9066,
        "non_buyers_count": 1248847,
        "non_buyers_percentage": 93.0934,
        "total_observed_sessions": 3614959,
        "observed_purchase_sessions": 126503,
        "total_purchase_events": 965158,
        "total_monetary_observed": 5140880.08
    }

    behavioral_funnel = {
        "event_level": [
            {"step": "view", "count": 9660505, "pct": 46.68},
            {"step": "cart", "count": 5770086, "pct": 27.88},
            {"step": "remove_from_cart", "count": 3971488, "pct": 19.19},
            {"step": "purchase", "count": 1290761, "pct": 6.24}
        ],
        "session_level": [
            {"step": "total_sessions", "count": 3614959, "rate_from_prev": 100.0, "stage_desc": "All Valid User Sessions"},
            {"step": "cart_sessions", "count": 800307, "rate_from_prev": 22.1388, "stage_desc": "Sessions with >=1 Cart Addition"},
            {"step": "purchase_sessions", "count": 126503, "rate_from_prev": 15.8068, "stage_desc": "Sessions with >=1 Purchase"}
        ],
        "dropoff_metrics": {
            "cart_session_rate": 22.1388,
            "purchase_session_rate": 3.4994,
            "cart_session_no_purchase_rate": 87.1294,
            "no_purchase_sessions_count": 697337,
            "semantic_note": "Cart Session No-Purchase Rate is measured strictly within the same session. Does not assert permanent cross-device abandonment."
        }
    }

    # 3. BUYER SEGMENTS (K=4 CLUSTERS)
    print("[3/7] Aggregating Buyer Segment Profiles...")
    cluster_profiles_raw = con.execute("""
        SELECT 
            cluster,
            COUNT(*) as customer_count,
            ROUND(COUNT(*) * 100.0 / 92652, 2) as pct_of_buyers,
            ROUND(COUNT(*) * 100.0 / 1341499, 2) as pct_of_population,
            ROUND(MEDIAN(recency_days), 1) as median_recency_days,
            ROUND(AVG(recency_days), 1) as mean_recency_days,
            ROUND(MEDIAN(frequency), 1) as median_frequency,
            ROUND(AVG(frequency), 2) as mean_frequency,
            ROUND(MEDIAN(monetary), 2) as median_monetary,
            ROUND(AVG(monetary), 2) as mean_monetary,
            ROUND(MEDIAN(sessions_30d), 1) as median_sessions_30d,
            ROUND(AVG(sessions_30d), 2) as mean_sessions_30d,
            ROUND(MEDIAN(views_30d), 1) as median_views_30d,
            ROUND(AVG(views_30d), 2) as mean_views_30d,
            ROUND(MEDIAN(cart_sessions_30d), 1) as median_cart_sessions_30d,
            ROUND(AVG(cart_sessions_30d), 2) as mean_cart_sessions_30d,
            ROUND(MEDIAN(log_activity_ratio), 2) as median_log_activity_ratio,
            ROUND(AVG(log_activity_ratio), 2) as mean_log_activity_ratio
        FROM 'data/features/buyer_clusters.parquet'
        GROUP BY cluster
        ORDER BY cluster
    """).fetchall()

    cluster_labels = {
        0: {
            "cluster_id": 0,
            "name": "Khách Mua 1 Lần Ngủ Đông Giá Trị Thấp",
            "name_en": "Dormant Low-Value Single Buyers",
            "short_tag": "Dormant",
            "color": "#64748B",
            "strategic_role": "Cost-constrained reach / Passive nurture",
            "description": "Khách hàng mua duy nhất 1 lần từ lâu (Median R=82.3d, F=1 phiên, M=$20.24), không còn phiên truy cập gần đây (Median Sessions 30d=0)."
        },
        1: {
            "cluster_id": 1,
            "name": "Khách VIP Trung Thành Cốt Lõi",
            "name_en": "Core VIP Champions",
            "short_tag": "VIP Champion",
            "color": "#4F46E5",
            "strategic_role": "High-touch retention / Brand advocacy",
            "description": "Nhóm khách hàng giá trị tối cao đóng góp phần lớn lợi nhuận (Median R=12.7d, F=3 phiên, M=$117.69, Sessions 30d=9), tương tác đa kênh liên tục."
        },
        2: {
            "cluster_id": 2,
            "name": "Khách Chi Tiêu Khá Đang Hạ Nhiệt / Nguy Cơ Rời Bỏ",
            "name_en": "At-Risk Cooling-Down Spenders",
            "short_tag": "At-Risk",
            "color": "#E11D48",
            "strategic_role": "High-priority winback survey & retention",
            "description": "Khách hàng từng mua với giá trị khá (Median R=54.3d, F=1 phiên, M=$67.29) nhưng đã ngừng ghé thăm trong tháng gần nhất (Median Sessions 30d=0)."
        },
        3: {
            "cluster_id": 3,
            "name": "Khách Mua Gần Đây & Tương Tác Tích Cực / Triển Vọng Mua Lại",
            "name_en": "Recently Active Repeat Prospects",
            "short_tag": "Active Prospect",
            "color": "#0D9488",
            "strategic_role": "Basket completion / Cross-sell / Nurture second order",
            "description": "Khách hàng giao dịch rất gần (Median R=16.3d, F=1 phiên, M=$28.13) đang tích cực duyệt xem sản phẩm (Median Sessions 30d=3) với ý định mua lại cao."
        }
    }

    segments_data = []
    for r in cluster_profiles_raw:
        cid = r[0]
        meta = cluster_labels[cid]
        segments_data.append({
            **meta,
            "customer_count": r[1],
            "pct_of_buyers": r[2],
            "pct_of_population": r[3],
            "median_recency_days": r[4],
            "mean_recency_days": r[5],
            "median_frequency": r[6],
            "mean_frequency": r[7],
            "median_monetary": r[8],
            "mean_monetary": r[9],
            "median_sessions_30d": r[10],
            "mean_sessions_30d": r[11],
            "median_views_30d": r[12],
            "mean_views_30d": r[13],
            "median_cart_sessions_30d": r[14],
            "mean_cart_sessions_30d": r[15],
            "median_log_activity_ratio": r[16],
            "mean_log_activity_ratio": r[17]
        })

    # 4. NON-BUYER ENGAGEMENT TIERS
    print("[4/7] Aggregating Non-Buyer Engagement Tiers...")
    non_buyer_tiers_raw = con.execute("""
        SELECT 
            engagement_tier,
            COUNT(*) as customer_count,
            ROUND(COUNT(*) * 100.0 / 1248847, 2) as pct_of_non_buyers,
            ROUND(COUNT(*) * 100.0 / 1341499, 2) as pct_of_population,
            ROUND(MEDIAN(sessions_30d), 1) as median_sessions_30d,
            ROUND(MEDIAN(views_30d), 1) as median_views_30d,
            ROUND(MEDIAN(cart_sessions_30d), 1) as median_cart_sessions_30d,
            recommended_tactic,
            marketing_goal,
            primary_kpi
        FROM 'outputs/recommendations/non_buyer_recommendations.parquet'
        GROUP BY engagement_tier, recommended_tactic, marketing_goal, primary_kpi
        ORDER BY customer_count DESC
    """).fetchall()

    tier_descriptions = {
        "HIGH_INTENT": {
            "name": "Ý định mua sắm cao (Có giỏ hàng)",
            "name_en": "High-Intent Browse & Cart Prospects",
            "color": "#F59E0B",
            "description": "Người dùng chưa từng mua nhưng có sự kiện thêm giỏ trong 30 ngày và duyệt web tích cực. Cơ hội chuyển đổi đơn đầu cao nhất.",
            "cart_state_qualification": "Candidate Cart Follow-Up based on recent 30d cart interest signal, not verified persistent shopping cart state."
        },
        "EXPLORING": {
            "name": "Khám phá danh mục tích cực",
            "name_en": "Active Catalog Explorers",
            "color": "#3B82F6",
            "description": "Người dùng duyệt xem nhiều sản phẩm nhưng chưa bấm thêm vào giỏ. Đề xuất nội dung định hướng và mẫu thử dùng thử.",
            "cart_state_qualification": "Zero cart additions in 30d; high consideration volume."
        },
        "LOW_ENGAGEMENT": {
            "name": "Tương tác mức thấp",
            "name_en": "Low Engagement Casual Browsers",
            "color": "#8B5CF6",
            "description": "Khách ghé thăm 1-2 lần rồi dừng. Đề xuất tiếp cận qua bản tin định kỳ chi phí tối thiểu.",
            "cart_state_qualification": "Infrequent browsing sessions without cart."
        },
        "INACTIVE": {
            "name": "Không hoạt động / Thoát trang",
            "name_en": "Inactive / Single-Visit Bounces",
            "color": "#475569",
            "description": "Khách vãng lai xem lướt rồi thoát từ lâu (>60 ngày). Kích hoạt rào cản G5 không can thiệp tiếp thị để chống spam.",
            "cart_state_qualification": "Zero activity in recent window."
        }
    }

    non_buyer_tiers_data = []
    for r in non_buyer_tiers_raw:
        tier_code = r[0]
        meta = tier_descriptions.get(tier_code, {})
        non_buyer_tiers_data.append({
            "tier_code": tier_code,
            **meta,
            "customer_count": r[1],
            "pct_of_non_buyers": r[2],
            "pct_of_population": r[3],
            "median_sessions_30d": r[4],
            "median_views_30d": r[5],
            "median_cart_sessions_30d": r[6],
            "recommended_tactic": r[7],
            "marketing_goal": r[8],
            "primary_kpi": r[9]
        })

    # 5. HISTORICAL OUT-OF-TIME HOLDOUT VALIDATION (FEB 2020)
    print("[5/7] Formatting Historical Holdout Evaluation Metrics...")
    holdout_manifest_path = "outputs/experiments/phase5_holdout_evaluation.json"
    holdout_evaluation = {}
    if os.path.exists(holdout_manifest_path):
        with open(holdout_manifest_path, "r", encoding="utf-8") as f:
            holdout_evaluation = json.load(f)

    # 6. MARKETING RECOMMENDATIONS & DECISION INTELLIGENCE
    print("[6/7] Aggregating Prescriptive Marketing Recommendations...")
    tactic_summary_raw = con.execute("""
        SELECT 
            recommended_tactic,
            marketing_goal,
            COUNT(*) as total_count,
            ROUND(COUNT(*) * 100.0 / 1341499, 2) as pct_of_population,
            SUM(CASE WHEN cohort = 'BUYER' THEN 1 ELSE 0 END) as buyers_count,
            SUM(CASE WHEN cohort = 'NON_BUYER' THEN 1 ELSE 0 END) as non_buyers_count,
            FIRST(primary_kpi) as sample_primary_kpi
        FROM (
            SELECT recommended_tactic, marketing_goal, cohort, primary_kpi FROM 'outputs/recommendations/buyer_recommendations.parquet'
            UNION ALL
            SELECT recommended_tactic, marketing_goal, cohort, primary_kpi FROM 'outputs/recommendations/non_buyer_recommendations.parquet'
        )
        GROUP BY recommended_tactic, marketing_goal
        ORDER BY total_count DESC
    """).fetchall()

    tactic_metadata = {
        "TAC_NO_ACTION": {
            "name": "Không can thiệp (Bảo vệ ngân sách)",
            "name_en": "No Action (Budget Protection & Anti-Spam)",
            "channel": "None",
            "cost_level": "Zero ($0.00)",
            "desc": "Triệt tiêu gửi thông điệp rác vào tài khoản ngủ đông sâu hoặc khách vãng lai đã thoát."
        },
        "TAC_LOW_COST_NURTURE": {
            "name": "Bản tin nuôi dưỡng chi phí thấp",
            "name_en": "Low-Cost Automated Nurture",
            "channel": "Automated Email Newsletter",
            "cost_level": "Extremely Low (~$0.001 - $0.005)",
            "desc": "Bản tin tổng hợp xu hướng, cẩm nang làm đẹp đại trà tự động theo tuần/tháng."
        },
        "TAC_PRODUCT_EDU": {
            "name": "Giáo dục sản phẩm & Khám phá danh mục",
            "name_en": "Product Education & Category Discovery",
            "channel": "In-app / Web Banner / Email",
            "cost_level": "Low (~$0.005)",
            "desc": "Hướng dẫn chăm sóc da, thành phần nổi bật, top sản phẩm bán chạy cho khách đang tìm hiểu."
        },
        "TAC_CART_RECOVERY": {
            "name": "Candidate Cart Follow-Up",
            "name_en": "Candidate Cart Follow-Up",
            "channel": "Web Push / Direct Notification",
            "cost_level": "Low-Medium (~$0.01)",
            "desc": "Nhắc nhở và hỗ trợ tháo gỡ rào cản thanh toán cho khách hàng có tín hiệu thêm giỏ trong cửa sổ quan sát gần đây (lưu ý: chưa xác minh trạng thái giỏ còn mở)."
        },
        "TAC_WINBACK_SURVEY": {
            "name": "Khảo sát hồi quy & Ưu đãi giá trị cao",
            "name_en": "VIP/At-Risk Winback Survey & Offer",
            "channel": "Personalized Email / Dedicated Care",
            "cost_level": "Medium-High (~$0.05)",
            "desc": "Khảo sát lý do gián đoạn kèm mã kích hoạt riêng biệt dành cho khách hàng từng có đóng góp cao."
        },
        "TAC_LOYALTY_VIP": {
            "name": "Đặc quyền thành viên VIP nòng cốt",
            "name_en": "VIP Tier Loyalty & Early Access",
            "channel": "Concierge / Exclusive Loyalty Portal",
            "cost_level": "High (Dedicated Services)",
            "desc": "Tri ân quà tặng sinh nhật, quyền truy cập sớm sản phẩm mới và quản lý khách hàng riêng biệt."
        },
        "TAC_CROSS_SELL": {
            "name": "Gợi ý bán chéo danh mục bổ trợ",
            "name_en": "Personalized Cross-Sell",
            "channel": "On-site Recommendation / Post-order",
            "cost_level": "Low (~$0.005)",
            "desc": "Đề xuất bộ dưỡng đi kèm hoặc sản phẩm cùng bộ cho khách mới mua gần đây."
        },
        "TAC_POST_PURCHASE_CARE": {
            "name": "Chăm sóc trải nghiệm sau sự kiện mua",
            "name_en": "Post-Purchase Care & Review",
            "channel": "Automated Survey & Care Guide",
            "cost_level": "Low (~$0.005)",
            "desc": "Hướng dẫn sử dụng và khảo sát trải nghiệm sau sự kiện mua hàng được ghi nhận (lưu ý: dataset không có bằng chứng giao hàng thành công)."
        }
    }

    tactic_distribution = []
    for r in tactic_summary_raw:
        tac_code = r[0]
        meta = tactic_metadata.get(tac_code, {})
        tactic_distribution.append({
            "tactic_code": tac_code,
            **meta,
            "marketing_goal": r[1],
            "total_count": r[2],
            "pct_of_population": r[3],
            "buyers_count": r[4],
            "non_buyers_count": r[5],
            "primary_kpi": r[6]
        })

    # Diversity Matrix (Segment x Tactic)
    diversity_matrix_raw = con.execute("""
        SELECT 
            cluster_id,
            recommended_tactic,
            COUNT(*) as count
        FROM 'outputs/recommendations/buyer_recommendations.parquet'
        GROUP BY cluster_id, recommended_tactic
        ORDER BY cluster_id, count DESC
    """).fetchall()

    diversity_matrix = {}
    for r in diversity_matrix_raw:
        cid = str(r[0])
        if cid not in diversity_matrix:
            diversity_matrix[cid] = []
        diversity_matrix[cid].append({
            "tactic_code": r[1],
            "count": r[2],
            "pct_in_cluster": round(r[2] * 100.0 / con.execute(f"SELECT COUNT(*) FROM 'outputs/recommendations/buyer_recommendations.parquet' WHERE cluster_id = {r[0]}").fetchone()[0], 2)
        })

    # Hypothetical Cost Avoidance Scenario
    hypothetical_cost_avoidance = {
        "title": "Hypothetical Marketing Cost Avoidance Scenario",
        "rationale": "REES46 dataset does not track real-world marketing dispatch costs or execution schedules. This scenario evaluates theoretical cost efficiency under conservative simulation parameters.",
        "simulated_audience_suppressed": 892508,
        "suppressed_pct_of_population": 66.53,
        "parameters": {
            "simulated_frequency": "1 message per customer per week",
            "low_cost_unit_rate_usd": 0.005,
            "medium_cost_unit_rate_usd": 0.02
        },
        "projected_cost_avoidance_usd": {
            "weekly_low_estimate": 4462.54,
            "weekly_high_estimate": 17850.16,
            "monthly_low_estimate": 17850.16,
            "monthly_high_estimate": 71400.64
        },
        "governance_note": "Suppressing inactive profiles prevents brand spam reputation loss and preserves marketing ROI for engaged prospects."
    }

    # 7. ANONYMIZED CUSTOMER SAMPLES (NO RAW PII)
    print("[7/7] Generating Anonymized Customer Demonstration Samples...")
    # Representative samples across 8 archetypes
    archetype_samples = [
        {
            "demo_id": "DEMO_BUYER_01",
            "archetype_name": "Active VIP Champion",
            "cohort": "BUYER",
            "segment_name": "Cluster 1 · Core VIP Champions",
            "observation_behavior": {
                "recency_days": 5.0,
                "frequency": 12,
                "monetary_usd": 350.00,
                "sessions_30d": 9,
                "views_30d": 24,
                "cart_sessions_30d": 2,
                "log_activity_ratio": 1.25
            },
            "marketing_goal": "RETAIN_HIGH_VALUE",
            "recommended_tactic": "TAC_LOYALTY_VIP",
            "reason_codes": ["HIGH_HISTORICAL_SPEND", "REPEAT_PURCHASER", "ACTIVE_RECENT_ENGAGEMENT"],
            "explanation": "Khách hàng VIP nòng cốt chi tiêu cao ($350.00) duy trì giao dịch gần đây (5 ngày) và tương tác đa kênh liên tục. Đề xuất đặc quyền tri ân và truy cập sớm BST.",
            "guardrails_applied": ["G1_EXECUTION_CONSENT_CHECK", "G2_BUDGET_PROTECTION_VIP_WINBACK"],
            "eligibility_status": "PENDING_CONSENT",
            "evaluation_kpi": "vip_retention_rate_90d"
        },
        {
            "demo_id": "DEMO_BUYER_02",
            "archetype_name": "Cooling VIP (Silent)",
            "cohort": "BUYER",
            "segment_name": "Cluster 1 · Core VIP Champions",
            "observation_behavior": {
                "recency_days": 50.0,
                "frequency": 8,
                "monetary_usd": 280.00,
                "sessions_30d": 0,
                "views_30d": 0,
                "cart_sessions_30d": 0,
                "log_activity_ratio": -1.80
            },
            "marketing_goal": "REENGAGE_INACTIVE",
            "recommended_tactic": "TAC_WINBACK_SURVEY",
            "reason_codes": ["HIGH_HISTORICAL_SPEND", "PROLONGED_ABSENCE", "WINBACK_CANDIDATE"],
            "explanation": "Khách hàng VIP từng đóng góp lớn nhưng đã ngừng tương tác trong 50 ngày qua. Đề xuất gửi khảo sát lý do gián đoạn kèm ưu đãi kích hoạt.",
            "guardrails_applied": ["G1_EXECUTION_CONSENT_CHECK", "G2_BUDGET_PROTECTION_VIP_WINBACK"],
            "eligibility_status": "PENDING_CONSENT",
            "evaluation_kpi": "winback_reactivation_rate"
        },
        {
            "demo_id": "DEMO_BUYER_03",
            "archetype_name": "Active Repeat Prospect with Recent Cart",
            "cohort": "BUYER",
            "segment_name": "Cluster 3 · Recently Active Repeat Prospects",
            "observation_behavior": {
                "recency_days": 3.0,
                "frequency": 2,
                "monetary_usd": 45.00,
                "sessions_30d": 4,
                "views_30d": 11,
                "cart_sessions_30d": 2,
                "log_activity_ratio": 0.85
            },
            "marketing_goal": "SUPPORT_CART_COMPLETION",
            "recommended_tactic": "TAC_CART_RECOVERY",
            "reason_codes": ["ACTIVE_CART_ADDITIONS", "HIGH_PURCHASE_INTENT", "CHECKOUT_BARRIER_SUSPECTED"],
            "explanation": "Khách hàng mới mua gần đây vừa thêm sản phẩm vào giỏ nhưng chưa thanh toán. Áp dụng Guardrail G4 ưu tiên cứu giỏ hàng trong 48 giờ.",
            "guardrails_applied": ["G1_EXECUTION_CONSENT_CHECK", "G4_CART_INTENT_PRECEDENCE"],
            "eligibility_status": "PENDING_CONSENT",
            "evaluation_kpi": "cart_checkout_rate"
        },
        {
            "demo_id": "DEMO_BUYER_04",
            "archetype_name": "High-Value At-Risk Cooling Down",
            "cohort": "BUYER",
            "segment_name": "Cluster 2 · At-Risk Cooling-Down Spenders",
            "observation_behavior": {
                "recency_days": 65.0,
                "frequency": 3,
                "monetary_usd": 110.00,
                "sessions_30d": 0,
                "views_30d": 0,
                "cart_sessions_30d": 0,
                "log_activity_ratio": -1.50
            },
            "marketing_goal": "REENGAGE_INACTIVE",
            "recommended_tactic": "TAC_WINBACK_SURVEY",
            "reason_codes": ["SIGNIFICANT_HISTORICAL_SPEND", "COOLING_DOWN_ENGAGEMENT", "HIGH_RISK_ATTRITION"],
            "explanation": "Khách hàng chi tiêu khá ($110.00) có nguy cơ rời bỏ do ngưng tương tác hơn 2 tháng. Đề xuất chiến dịch winback chuyên sâu.",
            "guardrails_applied": ["G1_EXECUTION_CONSENT_CHECK", "G2_BUDGET_PROTECTION_VIP_WINBACK"],
            "eligibility_status": "PENDING_CONSENT",
            "evaluation_kpi": "winback_reactivation_rate"
        },
        {
            "demo_id": "DEMO_BUYER_05",
            "archetype_name": "Low-Value Dormant Single Buyer",
            "cohort": "BUYER",
            "segment_name": "Cluster 0 · Dormant Low-Value Single Buyers",
            "observation_behavior": {
                "recency_days": 45.0,
                "frequency": 1,
                "monetary_usd": 15.00,
                "sessions_30d": 0,
                "views_30d": 0,
                "cart_sessions_30d": 0,
                "log_activity_ratio": 0.00
            },
            "marketing_goal": "LOW_COST_NURTURE",
            "recommended_tactic": "TAC_LOW_COST_NURTURE",
            "reason_codes": ["LOW_OR_DORMANT_ACTIVITY", "COST_CONSTRAINED_REACH", "PASSIVE_ENGAGEMENT"],
            "explanation": "Khách mua 1 lần giá trị thấp đã ngưng hoạt động. Đề xuất duy trì hiện diện thụ động qua bản tin tự động chi phí thấp.",
            "guardrails_applied": ["G1_EXECUTION_CONSENT_CHECK"],
            "eligibility_status": "PENDING_CONSENT",
            "evaluation_kpi": "newsletter_open_rate"
        },
        {
            "demo_id": "DEMO_BUYER_06",
            "archetype_name": "Deep Dormant Budget Guarded",
            "cohort": "BUYER",
            "segment_name": "Cluster 0 · Dormant Low-Value Single Buyers",
            "observation_behavior": {
                "recency_days": 110.0,
                "frequency": 1,
                "monetary_usd": 8.50,
                "sessions_30d": 0,
                "views_30d": 0,
                "cart_sessions_30d": 0,
                "log_activity_ratio": 0.00
            },
            "marketing_goal": "NO_ACTION",
            "recommended_tactic": "TAC_NO_ACTION",
            "reason_codes": ["DEEP_DORMANCY", "LOW_HISTORICAL_VALUE", "GUARDRAIL_G3_BUDGET_PROTECTION"],
            "explanation": "Khách mua giá trị thấp ngủ đông sâu (>110 ngày). Kích hoạt Guardrail G3 cắt giảm hoàn toàn chi phí tiếp thị vô ích.",
            "guardrails_applied": ["G1_EXECUTION_CONSENT_CHECK", "G3_BUDGET_PROTECTION_DEEP_DORMANT"],
            "eligibility_status": "PENDING_CONSENT",
            "evaluation_kpi": "unsolicited_contact_prevention_rate"
        },
        {
            "demo_id": "DEMO_NON_BUYER_01",
            "archetype_name": "High-Intent Cart Prospect",
            "cohort": "NON_BUYER",
            "segment_name": "NonBuyer_HIGH_INTENT",
            "observation_behavior": {
                "recency_days": None,
                "frequency": 0,
                "monetary_usd": 0.00,
                "sessions_30d": 3,
                "views_30d": 15,
                "cart_sessions_30d": 1,
                "log_activity_ratio": 0.95
            },
            "marketing_goal": "SUPPORT_CART_COMPLETION",
            "recommended_tactic": "TAC_CART_RECOVERY",
            "reason_codes": ["NON_BUYER_HIGH_INTENT", "ACTIVE_CART_ADDITIONS", "FIRST_ORDER_OPPORTUNITY"],
            "explanation": "Người dùng chưa mua nhưng có ý định cao (có giỏ hàng gần đây và 3 phiên truy cập). Đề xuất hỗ trợ chuyển đổi đơn đầu tiên.",
            "guardrails_applied": ["G1_EXECUTION_CONSENT_CHECK", "G4_CART_INTENT_PRECEDENCE"],
            "eligibility_status": "PENDING_CONSENT",
            "evaluation_kpi": "first_time_buyer_conversion"
        },
        {
            "demo_id": "DEMO_NON_BUYER_02",
            "archetype_name": "Cold Bounce Inactive",
            "cohort": "NON_BUYER",
            "segment_name": "NonBuyer_INACTIVE",
            "observation_behavior": {
                "recency_days": None,
                "frequency": 0,
                "monetary_usd": 0.00,
                "sessions_30d": 0,
                "views_30d": 0,
                "cart_sessions_30d": 0,
                "log_activity_ratio": 0.00
            },
            "marketing_goal": "NO_ACTION",
            "recommended_tactic": "TAC_NO_ACTION",
            "reason_codes": ["NON_BUYER_INACTIVE", "PROLONGED_DORMANCY", "GUARDRAIL_G5_FATIGUE_PREVENTION"],
            "explanation": "Người dùng vãng lai vào xem 1 lượt từ tháng trước rồi thoát. Kích hoạt Guardrail G5 loại bỏ khỏi danh sách tiếp thị.",
            "guardrails_applied": ["G1_EXECUTION_CONSENT_CHECK", "G5_CONTACT_FATIGUE_PREVENTION"],
            "eligibility_status": "PENDING_CONSENT",
            "evaluation_kpi": "unsolicited_contact_prevention_rate"
        }
    ]

    # ASSEMBLE MASTER DASHBOARD SNAPSHOT
    master_snapshot = {
        "metadata": metadata,
        "customer_overview": customer_overview,
        "behavioral_funnel": behavioral_funnel,
        "buyer_segments": segments_data,
        "non_buyer_tiers": non_buyer_tiers_data,
        "historical_holdout_evaluation": holdout_evaluation,
        "tactic_distribution": tactic_distribution,
        "diversity_matrix": diversity_matrix,
        "hypothetical_cost_avoidance": hypothetical_cost_avoidance,
        "archetype_samples": archetype_samples,
        "model_and_system_insights": {
            "model_version": "v1.0.0-f1-std-k4",
            "model_hash_sha256": "ab98e132480914abb028c8009fd090030eef73ebf0faee2fa6dbd05e13dc9bfc",
            "selected_feature_space": "F1 (7 Dimensions: RFM + 30-day Engagement)",
            "selected_scaler": "StandardScaler after log1p on 5 skewed features",
            "clustering_algorithm": "Standard K-Means (k-means++ initialization)",
            "k_clusters": 4,
            "internal_validation": {
                "silhouette_score": 0.2828,
                "davies_bouldin_index": 1.4173,
                "mean_initialization_ari": 0.9876,
                "min_cluster_proportion": 9.45
            },
            "surrogate_explainer": {
                "algorithm": "DecisionTreeClassifier (max_depth=3)",
                "test_fidelity": 82.11,
                "discrepancy_rate": 17.89,
                "role_note": "Approximate visual explainer only. Decision engine uses true cluster_id."
            },
            "performance_benchmarks": {
                "profiling_runtime_s": 78.39,
                "etl_runtime_s": 212.18,
                "feature_engineering_s": 11.25,
                "clustering_screening_stability_s": 131.53,
                "winning_fit_time_s": 0.37,
                "holdout_evaluation_s": 25.85,
                "decision_engine_s": 4.52,
                "decision_engine_throughput": 296528.0,
                "parquet_query_speedup": "8.09x median fair benchmark"
            }
        }
    }

    # WRITE SNAPSHOT FILES
    print("\nWriting Snapshot Files to outputs/dashboard/...")
    master_path = os.path.join(output_dir, "ivre_dashboard_snapshot.json")
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master_snapshot, f, ensure_ascii=False, indent=2)
    master_size_kb = os.path.getsize(master_path) / 1024
    print(f"[PASS] Master snapshot exported: {master_path} ({master_size_kb:.2f} KB)")

    # Modular snapshots for efficient lazy loading if needed
    modular_files = {
        "summary_snapshot.json": {
            "metadata": metadata,
            "customer_overview": customer_overview,
            "behavioral_funnel": behavioral_funnel
        },
        "segments_snapshot.json": {
            "buyer_segments": segments_data,
            "non_buyer_tiers": non_buyer_tiers_data
        },
        "recommendations_snapshot.json": {
            "tactic_distribution": tactic_distribution,
            "diversity_matrix": diversity_matrix,
            "hypothetical_cost_avoidance": hypothetical_cost_avoidance,
            "archetype_samples": archetype_samples
        },
        "holdout_evaluation_snapshot.json": holdout_evaluation,
        "model_system_insights_snapshot.json": master_snapshot["model_and_system_insights"]
    }

    manifest_entries = {}
    for filename, data in modular_files.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        manifest_entries[filename] = {
            "size_kb": round(os.path.getsize(filepath) / 1024, 2),
            "sha256": get_sha256(filepath)
        }

    manifest_entries["ivre_dashboard_snapshot.json"] = {
        "size_kb": round(master_size_kb, 2),
        "sha256": get_sha256(master_path)
    }

    # Write Manifest
    manifest_path = os.path.join(output_dir, "snapshot_manifest.json")
    manifest_data = {
        "manifest_version": "v1.0.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(manifest_entries),
        "files": manifest_entries
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print(f"[PASS] Snapshot manifest exported: {manifest_path}")

    elapsed = time.perf_counter() - t0
    print(f"\n[DONE] Phase 7 Snapshot generation completed in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    build_snapshots()

