# Prompt khởi động trong Antigravity IDE

> Giải nén ZIP rồi mở folder project là workspace root. Bắt đầu hội thoại agent mới và dán nguyên đoạn dưới.

```text
Hãy làm việc như một Data Analyst + ML Engineer + Data Engineering mentor cho đồ án môn Phân tích dữ liệu của tôi.

Đọc lần lượt AGENTS.md, PROJECT_PLAN.md, PROJECT_STATUS.md, configs/project.yaml,
configs/kpi_dictionary.yaml, hai file báo cáo trong reports/, và skill
.agents/skills/phase-0-business-understanding/SKILL.md.

Chỉ triển khai Phase 0 (Business Understanding) trước. Hãy:
1. Kiểm tra tính nhất quán của mục tiêu, phạm vi, KPI, grain và assumptions;
2. Xem xét, hoàn thiện các mục Phase 0 đã được khởi tạo (không viết lại từ đầu một cách mù quáng);
3. Chạy `python -m unittest discover -s tests -v` và `python scripts/validate_phase0.py`;
4. Chỉ rõ điều gì là định nghĩa thiết kế và điều gì đã được kiểm chứng bằng dữ liệu;
5. Cập nhật reports/DATA_ANALYTICS_REPORT.md, reports/TECHNICAL_LEARNING_NOTES.md và PROJECT_STATUS.md;
6. Báo cáo phase gate: PASS / CONDITIONAL / BLOCKED, có bằng chứng, blockers, bước P1 tiếp theo.

Không tải hoặc bịa dataset; không thay đổi IVRE; không chạy sang phase 1 khi chưa chốt phase 0. Mỗi quyết định phân tích phải giải thích What / Why / How / Alternatives / Tests / Limits để tôi học và vấn đáp.
```

Nếu IDE hỗ trợ gọi skill theo tên, có thể yêu cầu: **"Sử dụng skill `phase-0-business-understanding` và hoàn thiện Phase 0 của workspace này"**.

## Bạn sẽ thấy gì sau Phase 0?

- Chương Business Understanding với mục tiêu business → câu hỏi analytics → KPI → hành động marketing.
- KPI Dictionary định nghĩa kỹ biến event / session / user / purchase session; cutoff, denominator và proxy.
- Các giả thuyết H1–H5 và tiêu chí kiểm chứng.
- Scope/boundaries + hard correctness requirements + hiệu suất/giới hạn.
- Tests của hợp đồng KPI chạy được trên bộ dữ liệu *đồ chơi có đánh dấu illustrative*, không phải dữ liệu thật.
- Project status và danh sách câu hỏi cần kiểm chứng khi bắt đầu P1.
