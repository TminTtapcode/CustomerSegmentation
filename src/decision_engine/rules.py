"""
Prescriptive Marketing Rules Module
====================================
Defines the business logic, eligibility checks, conflict resolution,
and explainability formatting for both Buyers and Non-Buyers.
"""

import os
import json
import datetime

RULES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "configs", "marketing_rules.yaml")

def load_marketing_rules(rules_path=None):
    if rules_path is None:
        rules_path = RULES_PATH
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)

class MarketingDecisionRules:
    def __init__(self, rules_path=None):
        self.rules = load_marketing_rules(rules_path)
        self.ruleset_version = self.rules.get("ruleset_version", "v1.0.0")
        self.observation_cutoff = self.rules.get("observation_cutoff", "2020-02-01T00:00:00Z")
        self.model_version = self.rules.get("compatible_model_version", "v1.0.0-f1-std-k4")
        self.tactics = self.rules.get("candidate_tactics", {})
        self.goals = self.rules.get("marketing_goals", {})
        self.non_buyer_tiers = self.rules.get("non_buyer_tiering_rules", {})

    def evaluate_customer(self, customer_evidence: dict) -> dict:
        """
        Evaluates a single customer record against evidence-based rules.
        Dynamic, non-static routing: Customers within the same cluster
        receive different recommendations based on individual behavioral evidence.
        """
        user_id = customer_evidence.get("user_id")
        is_buyer = bool(customer_evidence.get("is_buyer", False))
        cluster_id = customer_evidence.get("cluster") # 0, 1, 2, 3 or None
        
        # Guardrail G2: Missing/corrupt data check
        if not user_id:
            return self._build_recommendation(
                user_id="UNKNOWN",
                cohort="UNKNOWN",
                segment_id="INVALID",
                goal_id="NO_ACTION",
                tactic_id="TAC_NO_ACTION",
                alt_tactics=[],
                reason="Dữ liệu định danh người dùng bị khuyết hoặc không hợp lệ. Kích hoạt guardrail G2 bảo vệ hệ thống.",
                reason_codes=["INSUFFICIENT_DATA", "GUARDRAIL_G2_TRIGGERED"],
                guardrails=["G2_DATA_QUALITY_FALLBACK"],
                evidence=customer_evidence
            )
            
        guardrails_applied = ["G1_EXECUTION_CONSENT_CHECK"]
        
        # ---------------------------------------------------------------------
        # CASE 1: BUYER COHORT
        # ---------------------------------------------------------------------
        if is_buyer:
            cohort = "BUYER"
            segment_id = f"Cluster_{cluster_id}" if cluster_id is not None else "Buyer_Unassigned"
            
            recency = float(customer_evidence.get("recency_days", 999.0))
            frequency = float(customer_evidence.get("frequency", 1.0))
            monetary = float(customer_evidence.get("monetary", 0.0))
            sessions_30d = float(customer_evidence.get("sessions_30d", 0.0))
            views_30d = float(customer_evidence.get("views_30d", 0.0))
            cart_sessions_30d = float(customer_evidence.get("cart_sessions_30d", 0.0))
            log_act = float(customer_evidence.get("log_activity_ratio", 0.0))
            
            # Guardrail G3: Budget protection for deep dormant low-value single buyers
            if recency > 90.0 and monetary < 20.0 and sessions_30d == 0.0:
                guardrails_applied.append("G3_BUDGET_PROTECTION_DEEP_DORMANT")
                return self._build_recommendation(
                    user_id=user_id,
                    cohort=cohort,
                    segment_id=segment_id,
                    goal_id="NO_ACTION",
                    tactic_id="TAC_NO_ACTION",
                    alt_tactics=["TAC_LOW_COST_NURTURE"],
                    reason=f"Khách hàng đã ngủ đông sâu (Recency: {recency:.1f} ngày > 90 ngày) với giá trị lịch sử thấp (Monetary: ${monetary:.2f} < $20) và không có phiên tương tác gần đây. Kích hoạt Guardrail G3 tiết kiệm ngân sách tiếp thị.",
                    reason_codes=["DEEP_DORMANCY", "LOW_HISTORICAL_VALUE", "GUARDRAIL_G3_BUDGET_PROTECTION"],
                    guardrails=guardrails_applied,
                    evidence=customer_evidence
                )
                
            # Active VIP privilege takes highest precedence if purchased recently (<= 30d) and active
            if cluster_id == 1 and sessions_30d >= 2.0 and recency <= 30.0:
                return self._build_recommendation(
                    user_id=user_id,
                    cohort=cohort,
                    segment_id=segment_id,
                    goal_id="RETAIN_HIGH_VALUE",
                    tactic_id="TAC_LOYALTY_VIP",
                    alt_tactics=["TAC_CART_RECOVERY" if cart_sessions_30d >= 1.0 else "TAC_CROSS_SELL"],
                    reason=f"Khách hàng VIP nòng cốt chi tiêu cao (Monetary: ${monetary:.2f}) duy trì giao dịch gần đây (Recency: {recency:.1f} ngày) và tương tác tích cực ({int(sessions_30d)} phiên). Đề xuất đặc quyền VIP tri ân và chăm sóc độc quyền.",
                    reason_codes=["HIGH_HISTORICAL_SPEND", "REPEAT_PURCHASER", "ACTIVE_RECENT_ENGAGEMENT"],
                    guardrails=guardrails_applied,
                    evidence=customer_evidence
                )

            # Guardrail G4: Cart intent precedence (applies across all buyer clusters)
            if cart_sessions_30d >= 1.0:
                guardrails_applied.append("G4_CART_INTENT_PRECEDENCE")
                return self._build_recommendation(
                    user_id=user_id,
                    cohort=cohort,
                    segment_id=segment_id,
                    goal_id="SUPPORT_CART_COMPLETION",
                    tactic_id="TAC_CART_RECOVERY",
                    alt_tactics=["TAC_CROSS_SELL" if frequency >= 2 else "TAC_PRODUCT_EDU"],
                    reason=f"Khách hàng đã phát sinh {int(cart_sessions_30d)} phiên thêm giỏ trong 30 ngày gần nhất mà chưa thanh toán. Tín hiệu giỏ hàng được ưu tiên xử lý (G4) để hỗ trợ hoàn tất đơn hàng.",
                    reason_codes=["ACTIVE_CART_ADDITIONS", "HIGH_PURCHASE_INTENT", "CHECKOUT_BARRIER_SUSPECTED"],
                    guardrails=guardrails_applied,
                    evidence=customer_evidence
                )
                
            # Evidence-driven Routing within Cluster 1 (Remaining VIP Champions)
            if cluster_id == 1:
                if recency <= 45.0:
                    # Recent VIP slackening: Post purchase care
                    return self._build_recommendation(
                        user_id=user_id,
                        cohort=cohort,
                        segment_id=segment_id,
                        goal_id="ENCOURAGE_REPEAT_PURCHASE",
                        tactic_id="TAC_POST_PURCHASE_CARE",
                        alt_tactics=["TAC_LOYALTY_VIP"],
                        reason=f"Khách hàng VIP mới mua gần đây (Recency: {recency:.1f} ngày) nhưng mức hoạt động đang chững lại ({int(sessions_30d)} phiên). Đề xuất chăm sóc sau mua và hướng dẫn sử dụng sản phẩm.",
                        reason_codes=["HIGH_HISTORICAL_SPEND", "POST_PURCHASE_WINDOW", "EXPERIENCE_CHECK_WINDOW"],
                        guardrails=guardrails_applied,
                        evidence=customer_evidence
                    )
                else:
                    # Silent VIP: Winback
                    return self._build_recommendation(
                        user_id=user_id,
                        cohort=cohort,
                        segment_id=segment_id,
                        goal_id="REENGAGE_INACTIVE",
                        tactic_id="TAC_WINBACK_SURVEY",
                        alt_tactics=["TAC_LOYALTY_VIP"],
                        reason=f"Khách hàng VIP chi tiêu lớn (${monetary:.2f}) nhưng đã ngừng tương tác hoàn toàn trong 30 ngày qua (Recency: {recency:.1f} ngày). Đề xuất khảo sát lý do rời bỏ và ưu đãi tái kích hoạt chọn lọc.",
                        reason_codes=["HIGH_HISTORICAL_SPEND", "PROLONGED_INACTIVITY", "CHURN_RISK_DETECTED"],
                        guardrails=guardrails_applied,
                        evidence=customer_evidence
                    )

            # Evidence-driven Routing within Cluster 2 (At-Risk Cooling Down Spenders)
            elif cluster_id == 2:
                if monetary >= 40.0:
                    # Substantial past spend, inactive: Winback
                    return self._build_recommendation(
                        user_id=user_id,
                        cohort=cohort,
                        segment_id=segment_id,
                        goal_id="REENGAGE_INACTIVE",
                        tactic_id="TAC_WINBACK_SURVEY",
                        alt_tactics=["TAC_LOW_COST_NURTURE"],
                        reason=f"Khách hàng từng chi tiêu khá (Monetary: ${monetary:.2f}) đang có dấu hiệu rời bỏ (Recency: {recency:.1f} ngày, 0 phiên gần đây, xung lượng {log_act:.2f}). Đề xuất chiến dịch tái kích hoạt và khảo sát trải nghiệm.",
                        reason_codes=["MODERATE_OR_HIGH_PAST_VALUE", "PROLONGED_INACTIVITY", "CHURN_RISK_DETECTED"],
                        guardrails=guardrails_applied,
                        evidence=customer_evidence
                    )
                else:
                    # Moderate spend, inactive: Low cost nurture
                    return self._build_recommendation(
                        user_id=user_id,
                        cohort=cohort,
                        segment_id=segment_id,
                        goal_id="LOW_COST_NURTURE",
                        tactic_id="TAC_LOW_COST_NURTURE",
                        alt_tactics=["TAC_NO_ACTION"],
                        reason=f"Khách hàng thuộc nhóm hạ nhiệt với mức chi tiêu vừa phải (${monetary:.2f}) và không có tương tác 30 ngày. Đề xuất nuôi dưỡng định kỳ chi phí thấp qua bản tin xu hướng.",
                        reason_codes=["MODERATE_PAST_VALUE", "LOW_OR_DORMANT_ACTIVITY", "COST_CONSTRAINED_REACH"],
                        guardrails=guardrails_applied,
                        evidence=customer_evidence
                    )

            # Evidence-driven Routing within Cluster 3 (Recently Active Repeat Prospects)
            elif cluster_id == 3:
                if recency <= 14.0 and sessions_30d <= 2.0:
                    # Very recent purchase: Post purchase care
                    return self._build_recommendation(
                        user_id=user_id,
                        cohort=cohort,
                        segment_id=segment_id,
                        goal_id="ENCOURAGE_REPEAT_PURCHASE",
                        tactic_id="TAC_POST_PURCHASE_CARE",
                        alt_tactics=["TAC_CROSS_SELL"],
                        reason=f"Khách hàng vừa mua hàng trong 2 tuần qua (Recency: {recency:.1f} ngày). Đề xuất kiểm tra sự hài lòng và cung cấp mẹo sử dụng để tạo tiền đề cho đơn mua lặp lại.",
                        reason_codes=["RECENT_TRANSACTION", "POST_PURCHASE_WINDOW", "EXPERIENCE_CHECK_WINDOW"],
                        guardrails=guardrails_applied,
                        evidence=customer_evidence
                    )
                elif views_30d >= 5.0:
                    # Active browsing without cart: Cross-sell
                    return self._build_recommendation(
                        user_id=user_id,
                        cohort=cohort,
                        segment_id=segment_id,
                        goal_id="ENCOURAGE_REPEAT_PURCHASE",
                        tactic_id="TAC_CROSS_SELL",
                        alt_tactics=["TAC_PRODUCT_EDU"],
                        reason=f"Khách hàng mới mua đang quay lại lướt xem tích cực ({int(views_30d)} lượt xem, xung lượng +{log_act:.2f}). Đề xuất các sản phẩm bổ trợ cá nhân hóa dựa trên danh mục đã xem.",
                        reason_codes=["RECENT_TRANSACTION", "ACTIVE_CATEGORY_BROWSING", "BASKET_EXPANSION_OPPORTUNITY"],
                        guardrails=guardrails_applied,
                        evidence=customer_evidence
                    )
                else:
                    # General recent active buyer: Product education
                    return self._build_recommendation(
                        user_id=user_id,
                        cohort=cohort,
                        segment_id=segment_id,
                        goal_id="INCREASE_PRODUCT_DISCOVERY",
                        tactic_id="TAC_PRODUCT_EDU",
                        alt_tactics=["TAC_LOW_COST_NURTURE"],
                        reason=f"Khách hàng mua gần đây (Recency: {recency:.1f} ngày) đang duy trì tương tác số nhẹ ({int(sessions_30d)} phiên). Đề xuất nội dung định hướng làm đẹp và bộ sản phẩm dùng thử.",
                        reason_codes=["RECENT_TRANSACTION", "ACTIVE_RECENT_ENGAGEMENT", "CONSIDERATION_STAGE"],
                        guardrails=guardrails_applied,
                        evidence=customer_evidence
                    )

            # Evidence-driven Routing within Cluster 0 (Dormant Low-Value Single Buyers)
            else:
                if sessions_30d >= 1.0 or views_30d >= 3.0:
                    # Re-awakening dormant buyer: Educate and encourage
                    return self._build_recommendation(
                        user_id=user_id,
                        cohort=cohort,
                        segment_id=segment_id,
                        goal_id="INCREASE_PRODUCT_DISCOVERY",
                        tactic_id="TAC_PRODUCT_EDU",
                        alt_tactics=["TAC_LOW_COST_NURTURE"],
                        reason=f"Khách hàng ngủ đông có tín hiệu quay lại tương tác ({int(sessions_30d)} phiên, {int(views_30d)} lượt xem trong 30 ngày). Đề xuất nội dung giáo dục sản phẩm để kích hoạt sự quan tâm.",
                        reason_codes=["REAWAKENING_DORMANT", "ACTIVE_RECENT_ENGAGEMENT", "CONSIDERATION_STAGE"],
                        guardrails=guardrails_applied,
                        evidence=customer_evidence
                    )
                else:
                    # Standard dormant: Low cost newsletter
                    return self._build_recommendation(
                        user_id=user_id,
                        cohort=cohort,
                        segment_id=segment_id,
                        goal_id="LOW_COST_NURTURE",
                        tactic_id="TAC_LOW_COST_NURTURE",
                        alt_tactics=["TAC_NO_ACTION"],
                        reason=f"Khách hàng mua 1 lần giá trị thấp (${monetary:.2f}) đã ngưng tương tác lâu ngày (Recency: {recency:.1f} ngày). Đề xuất duy trì hiện diện qua bản tin xu hướng chi phí tối thiểu.",
                        reason_codes=["LOW_OR_DORMANT_ACTIVITY", "COST_CONSTRAINED_REACH", "PASSIVE_ENGAGEMENT"],
                        guardrails=guardrails_applied,
                        evidence=customer_evidence
                    )

        # ---------------------------------------------------------------------
        # CASE 2: NON-BUYER COHORT (Engagement Tiering)
        # ---------------------------------------------------------------------
        else:
            cohort = "NON_BUYER"
            sessions_30d = float(customer_evidence.get("sessions_30d", 0.0))
            views_30d = float(customer_evidence.get("views_30d", 0.0))
            carts_30d = float(customer_evidence.get("carts_30d", 0.0))
            cart_sessions_30d = float(customer_evidence.get("cart_sessions_30d", 0.0))
            lifetime_sessions = float(customer_evidence.get("lifetime_sessions", 1.0))
            
            # Non-Buyer Tiering Logic
            if (cart_sessions_30d >= 1.0 or carts_30d >= 1.0) and (sessions_30d >= 2.0 or views_30d >= 5.0):
                tier = "HIGH_INTENT"
                guardrails_applied.append("G4_CART_INTENT_PRECEDENCE")
                return self._build_recommendation(
                    user_id=user_id,
                    cohort=cohort,
                    segment_id=f"NonBuyer_{tier}",
                    goal_id="SUPPORT_CART_COMPLETION",
                    tactic_id="TAC_CART_RECOVERY",
                    alt_tactics=["TAC_PRODUCT_EDU"],
                    reason=f"Người dùng chưa từng mua nhưng có ý định cao: {int(cart_sessions_30d)} phiên thêm giỏ và {int(sessions_30d)} phiên duyệt web trong 30 ngày. Đề xuất hỗ trợ tháo gỡ rào cản hoàn tất đơn hàng đầu tiên.",
                    reason_codes=["NON_BUYER_HIGH_INTENT", "ACTIVE_CART_ADDITIONS", "FIRST_ORDER_OPPORTUNITY"],
                    guardrails=guardrails_applied,
                    evidence=customer_evidence
                )
            elif sessions_30d >= 2.0 or views_30d >= 5.0:
                tier = "EXPLORING"
                return self._build_recommendation(
                    user_id=user_id,
                    cohort=cohort,
                    segment_id=f"NonBuyer_{tier}",
                    goal_id="INCREASE_PRODUCT_DISCOVERY",
                    tactic_id="TAC_PRODUCT_EDU",
                    alt_tactics=["TAC_LOW_COST_NURTURE"],
                    reason=f"Người dùng tích cực khám phá ({int(views_30d)} lượt xem sản phẩm, {int(sessions_30d)} phiên) nhưng chưa thêm giỏ hàng. Đề xuất nội dung hướng dẫn làm đẹp, đánh giá sản phẩm và bộ mẫu thử (Starter Kits).",
                    reason_codes=["NON_BUYER_EXPLORER", "ZERO_CART_FRICTION", "CONSIDERATION_STAGE"],
                    guardrails=guardrails_applied,
                    evidence=customer_evidence
                )
            elif sessions_30d >= 1.0:
                tier = "LOW_ENGAGEMENT"
                return self._build_recommendation(
                    user_id=user_id,
                    cohort=cohort,
                    segment_id=f"NonBuyer_{tier}",
                    goal_id="LOW_COST_NURTURE",
                    tactic_id="TAC_LOW_COST_NURTURE",
                    alt_tactics=["TAC_NO_ACTION"],
                    reason=f"Người dùng vãng lai có tương tác nhẹ ({int(sessions_30d)} phiên, {int(views_30d)} lượt xem) trong tháng qua. Đề xuất duy trì kết nối chi phí thấp qua bản tin phong cách và mẹo làm đẹp.",
                    reason_codes=["NON_BUYER_LOW_ENGAGEMENT", "PASSIVE_ENGAGEMENT", "COST_CONSTRAINED_REACH"],
                    guardrails=guardrails_applied,
                    evidence=customer_evidence
                )
            else:
                tier = "INACTIVE"
                guardrails_applied.append("G5_CONTACT_FATIGUE_PREVENTION")
                return self._build_recommendation(
                    user_id=user_id,
                    cohort=cohort,
                    segment_id=f"NonBuyer_{tier}",
                    goal_id="NO_ACTION",
                    tactic_id="TAC_NO_ACTION",
                    alt_tactics=["TAC_LOW_COST_NURTURE"],
                    reason=f"Người dùng chưa từng mua và hoàn toàn không có phiên truy cập nào trong 30 ngày qua (0 phiên, tổng lịch sử {int(lifetime_sessions)} phiên). Kích hoạt Guardrail G5 ngăn chặn gửi tin rác và tiết kiệm ngân sách.",
                    reason_codes=["NON_BUYER_INACTIVE", "PROLONGED_DORMANCY", "GUARDRAIL_G5_FATIGUE_PREVENTION"],
                    guardrails=guardrails_applied,
                    evidence=customer_evidence
                )

    def _build_recommendation(self, user_id, cohort, segment_id, goal_id, tactic_id, alt_tactics, reason, reason_codes, guardrails, evidence):
        goal_info = self.goals.get(goal_id, {})
        tactic_info = self.tactics.get(tactic_id, {})
        
        # Build clean sanitized evidence summary
        sanitized_evidence = {
            "recency_days": round(float(evidence.get("recency_days", 0.0)), 1) if evidence.get("recency_days") is not None else None,
            "frequency": int(evidence.get("frequency", 0)) if evidence.get("frequency") is not None else None,
            "monetary": round(float(evidence.get("monetary", 0.0)), 2) if evidence.get("monetary") is not None else None,
            "sessions_30d": int(evidence.get("sessions_30d", 0)),
            "views_30d": int(evidence.get("views_30d", 0)),
            "cart_sessions_30d": int(evidence.get("cart_sessions_30d", 0)),
            "log_activity_ratio": round(float(evidence.get("log_activity_ratio", 0.0)), 2) if evidence.get("log_activity_ratio") is not None else 0.0
        }
        
        return {
            "user_id": str(user_id),
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "observation_cutoff": self.observation_cutoff,
            "cohort": cohort,
            "segment_id": segment_id,
            "marketing_goal": goal_id,
            "marketing_goal_name_vi": goal_info.get("name_vi", goal_id),
            "recommended_tactic": tactic_id,
            "recommended_tactic_name_vi": tactic_info.get("name_vi", tactic_id),
            "alternative_tactics": alt_tactics,
            "evidence": sanitized_evidence,
            "human_readable_reason": reason,
            "reason_codes": reason_codes,
            "eligibility_status": "PENDING_CONSENT",
            "guardrails_applied": guardrails,
            "evaluation_kpis": {
                "primary_kpi": tactic_info.get("evaluation_kpi", goal_info.get("primary_kpi", "conversion_rate")),
                "secondary_kpi": goal_info.get("secondary_kpi", "average_order_value")
            },
            "limitations": tactic_info.get("risks_and_limitations", "Chưa kiểm chứng nhân quả A/B testing; đề xuất mang tính hướng dẫn nghiên cứu."),
            "ruleset_version": self.ruleset_version,
            "model_version": self.model_version
        }
