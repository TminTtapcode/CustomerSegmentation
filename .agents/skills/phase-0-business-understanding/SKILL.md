---
name: phase-0-business-understanding
description: Thiết lập và rà soát Phase 0 CRISP-DM của đồ án Customer Analytics; định nghĩa business questions, KPI, assumptions, scope, data grain, hypotheses và phase gate trước khi làm EDA.
---

# Phase 0 — Business Understanding

## Khi dùng

Khi user yêu cầu bắt đầu, tiếp tục, kiểm tra hoặc hoàn tất Phase 0, KPI Dictionary, phân tích nghiệp vụ và phạm vi đồ án.

## Quy trình

1. Đọc `AGENTS.md`, `PROJECT_PLAN.md`, `PROJECT_STATUS.md`, `configs/project.yaml`, `configs/kpi_dictionary.yaml` và phần P0 trong hai báo cáo.
2. Giữ nguyên phạm vi 1 dataset REES46, pipeline độc lập, IVRE chỉ để hiển thị. Không lấy dữ liệu/metrics chưa xác minh làm thực nghiệm.
3. Lập traceability: **Business objective → Business question → KPI & grain → Data columns → Analytics method → Marketing decision → How validated**.
4. Đối chiếu tất cả KPI về mẫu số, thời gian, proxy order, session validity, cohort, buyers/non-buyers; tách KPI mô tả có thể đo và KPI chiến dịch chỉ đo được trong tương lai.
5. Kiểm tra dữ liệu thiếu: event có nhiều purchase lines/session; không order_id, campaign, cost, marketing consent. Lập risk/assumption register, không đề xuất tính ROI đã quan sát.
6. Dự thảo giả thuyết H1–H5 và tiêu chí kiểm chứng; H5 phải giới hạn ở recommendation relevance, không claim causal marketing lift.
7. Chạy `python -m unittest discover -s tests -v` và `python scripts/validate_phase0.py`. Nếu lệnh không chạy, ghi lỗi và sửa nguyên nhân trước khi báo pass.
8. Cập nhật **chương P0 của `reports/DATA_ANALYTICS_REPORT.md`**, ghi What/Why/How và bài tập tính tay + câu hỏi trong `reports/TECHNICAL_LEARNING_NOTES.md`.
9. Cập nhật `PROJECT_STATUS.md` với checklist thực tế, bằng chứng, unresolved items, decision log và đề xuất P1. Chỉ chốt PASS khi tất cả Phase 0 gates đạt.

## Tiêu chí Phase Gate P0

- [ ] Đề tài và 3 business objectives được chốt.
- [ ] Bảng mapping mục tiêu → câu hỏi → KPI → phương pháp → đầu ra giải quyết được.
- [ ] KPI dictionary không mơ hồ về grain, cutoff, denominator và proxy.
- [ ] Buyer/nonbuyer được định nghĩa nhất quán.
- [ ] H1–H5 có phương pháp kiểm định khả thi hoặc giới hạn rõ.
- [ ] Scope, ethical/privacy, data licensing, benchmark và hard constraints có trong tài liệu.
- [ ] Unit tests, validation script chạy thành công và báo cáo đã cập nhật.
- [ ] Blockers chuyển sang P1 được công khai, không ghi PASS giả.

## Không làm

- Không chạy K-Means, tạo fake EDA hoặc huấn luyện model khi chưa có REES46.
- Không phát triển IVRE hoặc lập trình hệ thống marketing gửi thật.
- Không thêm report Markdown mới khi hai báo cáo chính đã đủ.
