---
name: implement-and-verify-phase
description: Triển khai từng phase P1–P8 của Customer Analytics theo CRISP-DM với kiểm thử, benchmark time/RSS, kiểm soát data leakage, cập nhật báo cáo và phase gate.
---

# Repeatable phase execution & verification

1. Đọc `AGENTS.md`, `PROJECT_PLAN.md`, `PROJECT_STATUS.md`, cấu hình và hai báo cáo; xác nhận phase hiện hành.
2. Trích yêu cầu/inputs/outputs/tests/dependencies/acceptance của phase từ plan. Không triển khai phase mới trước gate hiện hành.
3. Viết test nhỏ và dữ liệu synthetic **chỉ cho unit test** trước; giữ nguồn kết quả demo tách khỏi nghiên cứu.
4. Implement bước tối thiểu, ưu tiên DuckDB/Parquet xử lý event lớn, scikit-learn trên customer features.
5. Đo time, sampled peak process RSS, số record/chỉ tiêu, CPU/thread count khi benchmark. Đo toàn pipeline, không chỉ `.fit()`.
6. Run tests, inspect output thật, xử lý lỗi; nếu thiếu dữ liệu/log thì đánh dấu BLOCKED, không phát minh kết quả.
7. Bảo vệ temporal split `[2019-10-01,2020-02-01)` và February holdout; không dùng future để tối ưu features/hyperparams mà vẫn tự nhận holdout độc lập.
8. Tối ưu bằng evidence: correct first, trade-off matrix + hard constraints, benchmark công bằng; giữ model dễ giải thích nếu không có lợi ích rõ khi đổi.
9. Cập nhật chương liên quan trong `reports/DATA_ANALYTICS_REPORT.md`; bổ sung lý thuyết, ví dụ tính tay, vì sao chọn, alternative/risks/questions trong `reports/TECHNICAL_LEARNING_NOTES.md`.
10. Cập nhật `PROJECT_STATUS.md` với kết quả kiểm thử, artifacts, trade-offs, blocker và gate. Báo user ngắn gọn đã làm gì/đã kiểm chứng gì/còn hạn chế gì.

## Điều kiện từ chối phase gate

- Không có dữ liệu đầu vào xác minh được; con số KPI không traceable; schema không đúng; leakage; không có kiểm chứng tính đúng; lỗi lặp lại không khắc phục; hoặc chưa cập nhật hai báo cáo.

## Khi đủ thời gian

- P4: benchmark K-Means vs MiniBatchKMeans (same feature/preproc/sample). P5: surrogate depth 3 để **xấp xỉ** nhãn K-Means, đánh giá fidelity trên test set. UMAP/SHAP/GMM là optional.
