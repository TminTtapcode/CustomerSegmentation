# AGENTS.md — Quy tắc bất biến cho Antigravity / coding agents

**Ngôn ngữ trao đổi và hai báo cáo:** tiếng Việt, thuật ngữ chuyên môn Anh kèm định nghĩa. **Workspace:** `customer-analytics-antigravity` (project nghiên cứu độc lập). **Phase hiện tại:** tra `PROJECT_STATUS.md`, không tự suy diễn.

## Đọc trước khi sửa code

1. `PROJECT_PLAN.md` — phạm vi, kiến trúc, tiêu chí nghiệm thu, lịch 21 ngày.
2. `PROJECT_STATUS.md` — trạng thái thực và bước tiếp theo.
3. `configs/project.yaml` và `configs/kpi_dictionary.yaml` — nguồn chân lý cho mốc thời gian và metric.
4. `reports/DATA_ANALYTICS_REPORT.md` và `reports/TECHNICAL_LEARNING_NOTES.md` — tài liệu phải cập nhật cùng code.
5. Skill tương ứng trong `.agents/skills/` trước khi bắt đầu phase.

## Ràng buộc KHÔNG được vi phạm

- Triển khai theo CRISP-DM, mỗi thay đổi: **mục tiêu → lý do → thiết kế → mã nguồn → chạy kiểm thử → đọc kết quả → cập nhật báo cáo → đánh giá phase gate**.
- Không tự tuyên bố PASS khi chưa chạy lệnh/không có log. Không điền chỉ số thực nghiệm giả, không tô vẽ thành tích, không tạo dữ liệu giả để thay thế số liệu nghiên cứu.
- Chỉ có **một dataset chính REES46**. Source ngoài là tài liệu tham khảo, không tự thêm Hillstrom/Uplift vào phạm vi. Không trộn định danh REES46 với IVRE.
- REES46 là sự kiện mỹ phẩm giai đoạn 2019–2020, IVRE thời trang chỉ dùng để **trực quan hóa** kết quả. Luôn ghi rõ `Research Demo / REES46` trong dashboard.
- `purchase` có thể có nhiều dòng trong một session: `frequency` = **count distinct purchase sessions** (proxy); `monetary` = sum purchase-event price được kiểm tra; không phải net GMV và không suy diễn order_id.
- Chỉ buyers có RFM mua hợp lệ; non-buyers tách riêng phân tích Engagement. Không ép recency vô nghĩa bằng 0/999/∞.
- Mọi feature phải tính từ dữ liệu **trước cutoff**. Future February chỉ được sử dụng một lần để đánh giá hậu kiểm nếu giữ tư cách holdout; nếu dùng February để chỉnh mô hình, phải đổi cách báo cáo đánh giá.
- K-Means là segmentation, không tạo chiến thuật marketing. Strategy engine là rule-/evidence-based; đề xuất không có hiệu quả chiến dịch đã xác minh.
- Không gọi Silhouette/DBI/ARI là classification accuracy; không gọi surrogate fidelity là độ đúng nghiệp vụ của K-Means.
- Không suy kết luận nhân quả từ tương quan, conversion funnel, session-level no-purchase hay profile; ghi nhận giả thuyết và giới hạn.
- Không tối ưu chỉ một số: áp dụng hard correctness constraints + **trade-off matrix** giữa quality, business utility, explainability, runtime, sampled RSS; không áp trọng số giả tạo.
- Performance: benchmark cố định phần cứng/config/threads, seed, cùng input; đo time.perf_counter, sampled process RSS với psutil, nêu rõ hạn chế lấy mẫu. DuckDB memory_limit là thông số engine, không phải chặn cứng RSS.
- Không tạo quá hai báo cáo văn xuôi lớn: `reports/DATA_ANALYTICS_REPORT.md` và `reports/TECHNICAL_LEARNING_NOTES.md`. Benchmark/metrics lưu máy bằng CSV/JSON dưới outputs/experiments, không tạo báo cáo Markdown riêng trừ khi thật sự cần.
- Không chỉnh repo IVRE/FashionStore, không tạo API và không gửi marketing thật nếu chưa có yêu cầu rõ ràng.

## Cách làm việc và giao tiếp

- Lập checklist task nhỏ theo từng Phase và xác định dependencies; tiến độ tại `PROJECT_STATUS.md`.
- Khi thực thi: đọc file thực tế và chạy tests trước khi khẳng định. Nếu thiếu dataset, dừng ở Data Understanding skeleton, nêu thiếu đầu vào thay vì bịa EDA.
- Mọi kỹ thuật phải giải thích theo mẫu **What / Why / How / Formula / Example / Alternatives / Verification / Limits / Oral Defense** trong sổ tay.
- Mỗi phase cập nhật đúng chương báo cáo chính; dẫn nguồn và ghi `Observed`, `Assumption`, `Design choice`, `Illustrative`, `Pending validation` rõ ràng.
- Trước khi chuyển phase: tests pass, output thực, log thực, acceptance checklist và tài liệu cập nhật. Không tự động lấn sang phase tiếp theo khi user chỉ yêu cầu phase hiện tại.
- Ưu tiên Python thuần để kiểm chứng hợp đồng; dùng DuckDB + Parquet cho dataset lớn, pandas sau khi thu hẹp bảng. Mỗi phép tính phải minh bạch về grain (`event`, `session`, `user`, `purchase session`).
- Không thêm mô hình nâng cao/visual decorative khi core chưa PASS. Nếu phát hiện vấn đề nặng, đề xuất phương án sửa có tác động đến thời gian/tài nguyên, không âm thầm thay đổi scope.
