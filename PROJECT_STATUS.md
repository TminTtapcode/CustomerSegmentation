# PROJECT STATUS / PHASE GATES

**Last updated:** 2026-11-10T02:30:00+07:00.  
**Current phase:** **P8 — FINAL VERIFICATION, ACADEMIC DEFENSE & PROJECT SIGN-OFF: COMPLETED (PASS).**  
**Dataset present:** **YES — REES46 VERIFIED (Raw: 20.69M rows; Clean: 19.58M rows; Feature Table: 1.34M customers in `data/features/`).**  
**Model trained & evaluated:** **YES — Standard K-Means (K=4 on F1 Space) serialized in `outputs/models/kmeans_best_model.joblib`; Holdout evaluation validated on Feb 2020 events.**  
**Decision Engine implemented:** **YES — Explainable Evidence-Based Rule Engine (`src/decision_engine/rules.py`); 1,341,499 recommendations generated in `outputs/recommendations/`.**  
**Dashboard implemented:** **YES — Clean Minimalist Light Analytics Dashboard in `outputs/dashboard/index.html` with verified static snapshot `outputs/dashboard/ivre_dashboard_snapshot.json` (32.98 KB).**  
**IVRE Integration Spec:** **YES — `docs/IVRE_INTEGRATION_SPEC.md` published with React Component Contract and Iframe Embed Spec.**

---

## Phase 0 — Business Understanding (Ngày 1–2): HOÀN THÀNH (PASS)

_(Toàn bộ 8 nhiệm vụ Task 0.1 – 0.8, hợp đồng 16 KPI và 5 giả thuyết nghiên cứu đã được nghiệm thu và lưu trữ)._

---

## Phase 1 — Data Understanding & Exploratory Data Analysis (Ngày 3–4): HOÀN THÀNH (PASS)

### Checklist nhiệm vụ Phase 1

- [x] **Kiểm tra môi trường & công cụ:** Khảo sát phần cứng (16 CPUs, 15.24 GB RAM, 49.6 GB Disk Free). Cài đặt và khóa phiên bản trong `.venv`: `duckdb==2.0.0`, `pandas==3.1.1`, `numpy==2.5.4`, `pyarrow==26.0.1`, `psutil==7.2.2`, `scikit-learn==1.9.1`, `matplotlib==3.11.2` tại `requirements-lock.txt`.
- [x] **Kiểm tra & Đối soát tập dữ liệu REES46:** Xác nhận đầy đủ 5 tệp CSV trong `data/raw/` (`2019-Oct.csv` đến `2020-Feb.csv`) với tổng dung lượng 2,321.51 MB (~2.32 GB), 20,692,840 dòng dữ liệu thực tế spanning 152 ngày (01/10/2019 – 29/02/2020).
- [x] **Data Profiling toàn diện bằng DuckDB:**
  - Lược đồ 9 trường dữ liệu được chuẩn hóa; kiểm toán missing values từng cột qua từng tháng.
  - Tỷ lệ thiếu `user_id`: **0.00%** (100% người dùng định danh).
  - Tỷ lệ thiếu `user_session`: **0.022%** (4,598 dòng). **Đặc biệt: 0.00% sự kiện purchase bị thiếu session!**
  - Tỷ lệ thiếu `category_code`: **98.29%** (phế bỏ làm đặc trưng chính; thay bằng `category_id`).
  - Tỷ lệ thiếu `brand`: **42.32%** (gán nhãn 'unknown').
  - Thống kê phân vị giá: Median = 4.05, 99th percentile = 95.08, Max = 327.78; phát hiện 131 dòng giá âm và 104,157 dòng giá 0 cần làm sạch ở Phase 2.
- [x] **Phân tích Phễu Chuyển đổi Cấp Phiên (Session-level Funnel):**
  - Tổng số phiên quan sát hợp lệ: 3,614,959 sessions.
  - Tỷ lệ phiên thêm giỏ (`cart_session_rate`): **22.14%** (800,307 sessions).
  - Tỷ lệ phiên mua hàng (`purchase_session_rate`): **3.50%** (126,503 sessions).
  - Tỷ lệ bỏ giỏ hàng (`cart_abandonment_rate`): **87.13%** (697,337 sessions có cart nhưng không purchase).
- [x] **Xuất bản 8 Biểu đồ EDA Chuẩn mực (`outputs/figures/`):**
  1. `fig1_event_type_distribution.png`: Tỷ trọng 4 loại sự kiện (View 46.7%, Cart 27.9%, Remove 19.2%, Purchase 6.2%).
  2. `fig2_daily_monthly_volume.png`: Khối lượng sự kiện hàng ngày; đỉnh Black Friday tháng 11/2019 (>322k purchases).
  3. `fig3_unique_users_sessions_over_time.png`: Xu hướng DAU (25k–38k) và Daily Sessions (40k–60k).
  4. `fig4_user_activity_distribution.png`: Phân phối tương tác lệch đuôi dài (Median = 1 session, 2 events).
  5. `fig5_purchase_behavior_distribution.png`: Tần suất mua (79.9% mua 1 phiên, 20.1% repeat buyer) và chi tiêu (Median 33.17).
  6. `fig6_session_funnel.png`: Trực quan hóa phễu 4 bước và tỷ lệ rơi rụng giỏ hàng 87.13%.
  7. `fig7_missing_values_by_month.png`: Tính ổn định của tỷ lệ missing qua 5 tháng.
  8. `fig8_price_distribution.png`: Phân phối giá tuyến tính và log scale, phát hiện outliers.
- [x] **Kiểm toán Ranh giới Cắt Thời gian (Temporal Split & Anti-Leakage):**
  - Observation `[2019-10-01, 2020-02-01)`: 16,536,158 sự kiện (79.91%).
  - Holdout `[2020-02-01, 2020-03-01)`: 4,156,682 sự kiện (20.09%).
  - Số phiên vắt qua cutoff: 10,451 phiên; áp dụng quy tắc cắt cứng theo event timestamp để niêm phong tuyệt đối tập holdout.
- [x] **Đo kiểm Hiệu năng Thực tế (Benchmark Profiling):**
  - Wall-clock time: **78.39 giây**.
  - Throughput: **263,973.0 dòng/giây**.
  - Process RSS: Baseline = 123.71 MB $\to$ Peak = 1,618.41 MB (Delta: +1,494.7 MB), an toàn tuyệt đối dưới hạn mức 2 GB.
- [x] **Cập nhật Báo cáo Học thuật & Sổ tay Kỹ thuật:**
  - Hoàn thiện Chương 4 trong `reports/DATA_ANALYTICS_REPORT.md` với đầy đủ số liệu thực nghiệm, phân tích 8 biểu đồ và kế hoạch chi tiết cho Phase 2.
  - Bổ sung Phần II (P1.1 – P1.7) trong `reports/TECHNICAL_LEARNING_NOTES.md` theo cấu trúc 9 phần chuẩn kèm bộ 4 câu hỏi vấn đáp bảo vệ đồ án Q13–Q16.
- [x] **Kiểm thử Phần mềm & Xác thực Hợp đồng:**
  - `python -m unittest discover -s tests -v`: **18/18 PASS (0.003s)** kiểm thử cả logic Phase 0 và các giả định/cấu trúc Phase 1.
  - `python scripts/validate_phase0.py`: **PASS** (bảo toàn tính tương thích ngược, không hồi quy).
  - `python scripts/validate_phase1.py`: **PASS** (xác thực toàn bộ 20.69M dòng, 8 biểu đồ và hồ sơ JSON).

---

## Quyết định Nghiệm thu Cổng Phase 1 (Phase Gate Evaluation)

- **Quyết định:** **PASS**
- **Căn cứ & Bằng chứng:**
  1. Toàn bộ 20,692,840 dòng dữ liệu thực tế từ 5 tệp CSV của REES46 đã được phân tích 100%, không sử dụng dữ liệu giả tạo.
  2. Toàn bộ 8 biểu đồ trực quan hóa EDA đã được sinh ra và lưu tại `outputs/figures/`.
  3. Hồ sơ dữ liệu máy đọc `outputs/experiments/phase1_data_profile.json` đã được xuất bản và xác thực.
  4. Giả định cốt lõi về Purchase Session Proxy được xác nhận hoàn toàn: 100% sự kiện purchase có session, tỷ lệ 8.27 items/session chứng minh không thể lấy purchase event làm số đơn hàng.
  5. Phát hiện được các vấn đề chất lượng then chốt để xử lý trong Phase 2: Missing category_code (98.29%), 104k giá $\le 0$, 10.4k spanning sessions.
  6. 18/18 bài kiểm tra đơn vị và cả 2 kịch bản validation đều vượt qua tuyệt đối.

---

## Phase 2 — Data Preparation & Cleaning (Ngày 5–6): HOÀN THÀNH (PASS)

### Checklist nhiệm vụ Phase 2

- [x] **Kiểm toán & Đính chính Phát hiện Phase 1:**
  - Đính chính ngày đỉnh tháng 11: Ngày 22/11/2019 đạt 22,780 purchases (2,352 sessions, 270,074 events); Black Friday 29/11 đạt 17,992 purchases. Tổng tháng 11 là 322,417 purchases (đã sửa lỗi diễn đạt văn xuôi).
  - Đổi tên chỉ số 87.13% thành `Cart Session No-Purchase Rate` (697,337 phiên có giỏ hàng nhưng không mua trong cùng phiên), không quy chụp thành tỷ lệ bỏ giỏ của khách hàng.
  - Kiểm toán chi tiết 104,288 dòng `price <= 0`: 49,370 cart, 30,492 view, 24,299 remove, chỉ có 127 purchase. Quyết định: Giữ lại toàn bộ cho Engagement; chỉ loại khỏi Monetary đối với các giao dịch mua có giá $\le 0$.
  - Khảo sát va chạm UUID phiên: Phát hiện 331 mã phiên bị dùng chung bởi nhiều user; thiết kế khóa kết hợp `user_session_id = user_id || '_' || user_session` để giải quyết triệt để (0 collisions).
- [x] **Xây dựng & Thực thi Pipeline ETL DuckDB (`scripts/phase2_etl.py`):**
  - Đọc trực tiếp từ 5 file CSV thô (2,321.51 MB, 20,692,840 dòng).
  - Khử trùng lặp chính xác bằng `ROW_NUMBER() OVER (...)`: Loại bỏ 1,109,098 bản ghi trùng lặp (5.360%, trong đó 991,821 là duplicate `remove_from_cart`).
  - Tập dữ liệu sạch: 19,583,742 bản ghi duy nhất bảo toàn 1,639,358 người dùng duy nhất (0 người dùng bị mất).
  - Thiết lập hệ thống cờ chất lượng (`quality_flag`, `is_valid_for_engagement`, `is_valid_for_monetary`).
  - Phân tách chuỗi thời gian nghiêm ngặt ở cấp độ sự kiện tại mốc $T_{\text{cutoff}} = \text{2020-02-01T00:00:00Z}$:
    - `data/cleaned/observation_events.parquet`: 15,667,350 dòng (376.70 MB).
    - `data/cleaned/holdout_events.parquet`: 3,916,392 dòng (95.02 MB).
    - `data/cleaned/clean_events.parquet`: 19,583,742 dòng (471.74 MB).
- [x] **Đo kiểm Hiệu năng Thực nghiệm (Empirical Benchmark CSV vs Parquet):**
  - Kích thước lưu trữ: Từ 2,321.51 MB (CSV thô) xuống 471.74 MB (Parquet ZSTD), **tỷ lệ nén đạt 4.92x (tiết kiệm 79.7% đĩa, đạt tiêu chuẩn < 500 MB)**.
  - Thời gian truy vấn tổng hợp: 5.150s (CSV) $\to$ 0.618s (Clean Parquet), **tốc độ tăng 8.33 lần (Speedup 8.33x)**.
  - Thời gian thực thi toàn trình ETL: 212.18s (~3.5 phút), thông lượng 97,525 dòng/giây.
  - Peak RSS qua `psutil`: 2,379.03 MB (kiểm soát ổn định dưới giới hạn an toàn máy trạm).
  - Xuất bản tệp hồ sơ thực nghiệm: `outputs/experiments/phase2_data_cleaning.json`.
- [x] **Cập nhật Báo cáo Học thuật & Sổ tay Kỹ thuật:**
  - Hoàn thiện Chương 5 trong `reports/DATA_ANALYTICS_REPORT.md` với đầy đủ ma trận đánh đổi, bảng đối soát số học, phân phối cờ chất lượng và đối soát dòng tiền (+2,642.88 đơn vị điều chỉnh).
  - Bổ sung Phần III (P2.1 – P2.6) trong `reports/TECHNICAL_LEARNING_NOTES.md` theo cấu trúc 9 phần chuẩn kèm bộ 5 câu hỏi vấn đáp bảo vệ đồ án Q17–Q21.
- [x] **Kiểm thử Phần mềm & Xác thực Tự động:**
  - Viết mới `tests/test_phase2_data_preparation.py` với 8 bài test chuyên sâu (đối soát số lượng, kiểm tra anti-leakage, tính duy nhất của composite session key, bảo toàn engagement, loại trừ monetary, kiểm tra nén Parquet và speedup).
  - `python -m unittest discover -s tests -v`: **26/26 PASS (1.18s)** (8 Phase 0, 10 Phase 1, 8 Phase 2).
  - `python scripts/validate_phase0.py`: **PASS**.
  - `python scripts/validate_phase1.py`: **PASS**.
  - `python scripts/validate_phase2.py`: **PASS**.

---

## Quyết định Nghiệm thu Cổng Phase 2 (Phase Gate Evaluation)

- **Quyết định:** **PASS**
- **Căn cứ & Bằng chứng:**
  1. Toàn bộ 20,692,840 dòng dữ liệu thô đã được đối soát số học minh bạch: Khử đúng 1,109,098 bản ghi trùng lặp (chủ yếu là lỗi kỹ thuật frontend ở sự kiện xóa giỏ); bảo toàn 100% 1,639,358 người dùng duy nhất.
  2. Đã giải quyết triệt để 331 trường hợp va chạm UUID phiên bằng khóa kết hợp `user_session_id`, đưa số lượng va chạm giữa các user về đúng bằng 0.
  3. Chính sách cờ dữ liệu đa mục đích bảo toàn 104,161 tương tác xem hàng/thêm giỏ quà tặng 0 đồng cho Engagement, đồng thời loại trừ đúng 88 giao dịch mua giá $\le 0$ khỏi Monetary, điều chỉnh đúng +2,642.88 đơn vị tiền tệ bị âm vô lý trong doanh thu quan sát.
  4. Quy tắc phân tách thời gian nghiêm ngặt tại $T_{\text{cutoff}} = \text{2020-02-01T00:00:00Z}$ triệt tiêu rò rỉ dữ liệu tương lai (Data Leakage); 10,451 phiên vắt qua ranh giới được cắt lát ở cấp độ sự kiện chính xác.
  5. Tiêu chí kỹ thuật Parquet đạt vượt kỳ vọng: Dung lượng nén ZSTD đạt 471.74 MB (< 500 MB, nén 4.92x); tốc độ truy vấn tổng hợp tăng gấp 8.33 lần (vượt ngưỡng kỳ vọng 5–10x).
  6. Toàn bộ 26/26 bài unit tests và cả 3 kịch bản xác thực độc lập đều vượt qua 100%.

---

## Phase 3 — Customer Feature Engineering & Behavioral Analytics (Ngày 7–9): HOÀN THÀNH (PASS)

### Checklist nhiệm vụ Phase 3

- [x] **Xây dựng Bảng Đặc trưng Khách hàng Cấp độ Grain Chuẩn tắc:**
  - Khởi tạo Customer Feature Table từ 15,667,350 dòng sự kiện `observation_events.parquet` tại mốc $T_{\text{cutoff}} = \text{2020-02-01T00:00:00Z}$.
  - Tổng số khách hàng quan sát duy nhất: **1,341,499 khách hàng** (100% bảo toàn).
  - Phân tách 2 nhóm rõ rệt: **92,652 Buyers (6.91%)** và **1,248,847 Non-Buyers (93.09%)**.
- [x] **Trích xuất Đặc trưng RFM cho Tập Khách hàng Đã mua (Buyers):**
  - `recency_days`: Đo chính xác từ lần mua hợp lệ cuối cùng đến cutoff (Median = 56.72 ngày, Mean = 56.24 ngày, Skew = 0.11).
  - `frequency`: Tần suất mua bằng proxy phiên `purchase_sessions` (Median = 1 phiên, Max = 103 phiên, Skew = 17.12; 79.94% mua 1 lần, 20.06% mua lặp lại).
  - `monetary`: Tổng chi tiêu hợp lệ (`price > 0`) (Median = 33.15, Mean = 55.49, Max = 3,162.90 đơn vị tiền tệ, Skew = 7.19).
  - Các đặc trưng phái sinh: `monetary_per_session` (AOV proxy), `items_per_purchase_session` (trung bình 7.81 món/phiên), `purchase_span_days`.
- [x] **Trích xuất Bộ Đặc trưng Tương tác Clickstream (Engagement 30 ngày):**
  - Thiết lập hai cửa sổ trượt 30 ngày không chồng lấn: Recent $[2020-01-02, 2020-02-01)$ và Previous $[2019-12-03, 2020-01-02)$.
  - Tính toán: `sessions_30d`, `views_30d`, `carts_30d`, `unique_products_30d`, `cart_sessions_30d`, `cart_to_view_ratio_30d`, `days_since_last_event`.
  - Đo lường xung lượng thay đổi hoạt động qua `log_activity_ratio` với kỹ thuật làm mượt Laplace (+1), phân phối hình chuông đối xứng chuẩn tắc (Mean = 0.04, Skew = 0.15).
- [x] **Kiến trúc Tách biệt Tập Khách hàng Chưa mua (Decoupled Non-Buyers):**
  - Bảo vệ tính toàn vẹn toán học: 100% trong số 1,248,847 Non-buyers có `recency_days = NULL`, tuyệt đối không gán giá trị nhân tạo 0, 999 hay $\infty$.
  - Xuất bản tệp riêng `non_buyer_features.parquet` bảo toàn toàn bộ hành vi duyệt xem để phân tầng nuôi dưỡng ở Phase 6.
- [x] **Xuất bản 3 Tệp Parquet Đặc trưng (`data/features/`):**
  - `customer_features.parquet`: 1,341,499 dòng (13.35 MB, nén ZSTD).
  - `buyer_features.parquet`: 92,652 dòng (2.16 MB, nén ZSTD) — _Đầu vào cho Phase 4_.
  - `non_buyer_features.parquet`: 1,248,847 dòng (9.58 MB, nén ZSTD) — _Đầu vào cho Phase 6_.
- [x] **Xuất bản 4 Biểu đồ EDA Đặc trưng (`outputs/figures/`):**
  - `fig9_rfm_distributions.png`: Phân phối RFM, độ lệch xiên cực đoan của Frequency và Monetary.
  - `fig10_engagement_distributions.png`: Phân phối tương tác 30 ngày và xung lượng hoạt động.
  - `fig11_rfm_correlation_matrix.png`: Ma trận tương quan các đặc trưng; xác nhận không có cặp nào vượt $r = 0.66$ (không có đa cộng tuyến nghiêm trọng).
  - `fig12_buyer_vs_non_buyer_engagement.png`: So sánh đối đầu giữa Buyers và Non-Buyers (Buyers có tương tác gấp 41 lần).
- [x] **Đề xuất 3 Không gian Đặc trưng cho Phase 4:**
  - $F0$ (Traditional RFM — 3D): `[recency_days, frequency, monetary]`.
  - $F1$ (RFM + Core Engagement — 7D, Đề xuất chính): $F0$ + `[sessions_30d, views_30d, cart_sessions_30d, log_activity_ratio]`.
  - $F2$ (Extended Behavioral — 12D): $F1$ + `[monetary_per_session, items_per_purchase_session, unique_products_30d, cart_to_view_ratio_30d, days_since_last_event]`.
- [x] **Đo kiểm Hiệu năng Thực tế (Performance Benchmark):**
  - Thời gian toàn trình: **11.25 giây** (Tổng hợp 5.14s, Xuất Parquet 1.34s, Thống kê & Figures 4.77s).
  - Thông lượng: **1,392,653 sự kiện/giây** (119,244 khách hàng/giây).
  - Peak RSS: **1,478.11 MB** (~1.44 GB), kiểm soát an toàn dưới hạn mức 2 GB.
  - Xuất bản hồ sơ máy đọc: `outputs/experiments/phase3_feature_profiling.json`.
- [x] **Kiểm thử Tự động & Xác thực Hợp đồng:**
  - `python -m unittest discover -s tests -v`: **40/40 PASS (1.77s)** bao gồm Phase 0, 1, 2 và 10 tests mới của Phase 3.
  - `python scripts/validate_phase0.py`: **PASS**.
  - `python scripts/validate_phase1.py`: **PASS**.
  - `python scripts/validate_phase2.py`: **PASS**.
  - `python scripts/validate_phase3.py`: **PASS**.

---

## Quyết định Nghiệm thu Cổng Phase 3 (Phase Gate Evaluation)

- **Quyết định:** **PASS**
- **Căn cứ & Bằng chứng:**
  1. Toàn bộ 1,341,499 khách hàng trong kỳ quan sát đã được xây dựng hồ sơ đặc trưng chuẩn tắc 100%, không mất hoặc thêm bất kỳ khách hàng nào.
  2. Phân tách rạch ròi 92,652 Buyers (có RFM hợp lệ, Frequency proxy phiên chuẩn xác) và 1,248,847 Non-Buyers (Recency nghiêm ngặt = NULL, bảo toàn toàn bộ tương tác 30 ngày).
  3. Xung lượng hoạt động `log_activity_ratio` được làm mượt Laplace đối xứng chuẩn tắc, triệt tiêu lỗi chia cho 0 và tạo phân phối hình chuông lý tưởng cho K-Means.
  4. Đã xuất bản đầy đủ 3 tệp Parquet nén ZSTD (tổng 25.09 MB) và 4 biểu đồ trực quan hóa đặc trưng đạt chất lượng xuất bản khoa học.
  5. Đã đề xuất 3 không gian đặc trưng thử nghiệm $F0, F1, F2$ và khuyến nghị phương pháp tiền xử lý (Log Transformation + RobustScaler/StandardScaler) cho Phase 4 để giải quyết độ lệch xiên cực đoan.
  6. Toàn bộ 40/40 tests và 4/4 scripts validation đều vượt qua 100%.

---

## Phase 4 — Customer Segmentation Modeling (Ngày 7–10): HOÀN THÀNH (PASS)

### Checklist nhiệm vụ Phase 4

- [x] **Tiền xử lý Dữ liệu Chuẩn tắc (Preprocessing Pipeline):**
  - Biến đổi `np.log1p` trên các biến lệch xiên dương (`frequency`, `monetary`, `sessions_30d`, `views_30d`, `cart_sessions_30d`).
  - Giữ nguyên thang đo tuyến tính cho `recency_days` và `days_since_last_event` (phân phối đều, skew ~0.11).
  - Giữ nguyên `log_activity_ratio` không áp dụng log1p trực tiếp vì chứa giá trị âm (đã ở không gian log, skew ~0.11).
  - Khảo sát và so sánh cả `StandardScaler` và `RobustScaler`.
- [x] **Vòng 1 — Sàng lọc Ứng viên (Candidate Screening across 28 models):**
  - Quét lưới trên $F0$ (3D) và $F1$ (7D) với $K \in [2, 8]$ trên seed cố định 42.
  - Đo lường Inertia (Elbow), Sampled Silhouette ($N=10,000$ seed 42), Davies-Bouldin Index (DBI), tỷ lệ cụm Min/Max và thời gian fit.
- [x] **Vòng 2 — Đánh giá Chi tiết & Kiểm tra Độ ổn định (Stability across 5 Seeds):**
  - Đo độ ổn định Pairwise Adjusted Rand Index (ARI) qua 5 random seeds (`[42, 101, 202, 303, 404]`) trên cùng 92,652 khách hàng.
  - $F1$ ($K=4$) đạt $\text{Mean ARI} = 0.9876 \pm 0.0077$ (cặp thấp nhất $0.9785$), chứng minh các cụm là cấu trúc toàn cục vững chắc.
  - Phát hiện $K=5$ trên $F1$ bị suy giảm độ ổn định nghiêm trọng ($\text{Mean ARI} = 0.8614$, min 0.6711).
- [x] **Đối đầu Thực nghiệm: Standard K-Means vs MiniBatchKMeans:**
  - Chứng minh K-Means chuẩn rất nhanh trên 92k dòng ($0.33$s so với $0.38$s của MiniBatch).
  - MiniBatchKMeans có WCSS cao hơn $+0.98\%$ và chỉ đạt độ tương đồng $ARI = 0.5561$, chứng minh hội tụ về nghiệm kém hơn. Quyết định: chọn 100% Standard K-Means.
- [x] **Thực nghiệm Không gian Mở rộng $F2$ (12D):**
  - Chứng minh "lời nguyền số chiều" (Curse of Dimensionality): Silhouette giảm sâu xuống $0.2272$, DBI tăng vọt lên $1.5798$, gây loãng khoảng cách Euclidean.
- [x] **Ma trận Đánh đổi Đa chiều & Lựa chọn Mô hình Quán quân:**
  - Tuyển chọn cấu hình: **Không gian $F1$ (7D) + StandardScaler + $K=4$** đạt tối ưu Pareto (chất lượng hình học cân bằng, ổn định seed tuyệt đối, không có cụm suy thoái $< 9.4\%$, runtime $0.37$s).
- [x] **Xây dựng Chân dung Phân cụm ở Đơn vị Đo Lường Gốc:**
  - Cluster 0: Khách Mua 1 Lần Ngủ Đông (42,145 khách — 45.49%, Recency 82d, Freq 1, Monetary 20.2, Sessions 30d = 0).
  - Cluster 1: Khách VIP Trung Thành Cốt Lõi (8,755 khách — 9.45%, Recency 12.7d, Freq 3, Monetary 117.7, Sessions 30d = 9).
  - Cluster 2: Khách Đã Nguội Lạnh Chi Tiêu Khá (18,608 khách — 20.08%, Recency 54.3d, Freq 1, Monetary 67.3, Sessions 30d = 0, Log Act Ratio = -0.69).
  - Cluster 3: Khách Mới Mua & Duyệt Web Tích Cực (23,144 khách — 24.98%, Recency 16.3d, Freq 1, Monetary 28.1, Sessions 30d = 3, Log Act Ratio = +1.10).
- [x] **Tính Khả giải (Explainability):**
  - Huấn luyện Cây Quyết định Nông (`max_depth = 3`) trên 80% train, kiểm tra trên 20% test ($N=18,531$). Đạt độ trung thành mô phỏng **Test Fidelity = 82.11%** (Macro-F1 = 0.7780); trích xuất bộ luật If-Then minh bạch.
  - Chiếu không gian 2D PCA giải thích **76.40%** phương sai (PC1 56.39%, PC2 20.00%).
- [x] **Xuất bản 4 Biểu đồ Khoa học Phase 4 (`outputs/figures/`):**
  - `fig13_elbow_silhouette.png`, `fig14_cluster_pca.png`, `fig15_cluster_profiles.png`, `fig16_surrogate_tree.png`.
- [x] **Xuất bản Artifacts Đầy đủ:**
  - Model Bundle: `outputs/models/kmeans_best_model.joblib` (42.3 KB).
  - Cluster Table: `data/features/buyer_clusters.parquet` (92,652 dòng, nén ZSTD).
  - Manifest & CSVs: `outputs/experiments/phase4_model_selection.json`, `phase4_round1_screening.csv`, `phase4_round2_stability.csv`.
- [x] **Kiểm thử Tự động Toàn diện:**
  - `tests/test_phase4_clustering.py`: 10 tests mới.
  - Toàn bộ suite: **50/50 unit tests PASS (2.53s)**.
  - Cả 5 scripts validation `validate_phase0.py` $\to$ `validate_phase4.py`: **100% PASS**.

---

## Quyết định Nghiệm thu Cổng Phase 4 (Phase Gate Evaluation)

- **Quyết định:** **PASS**
- **Căn cứ & Bằng chứng:**
  1. Mô hình phân cụm được huấn luyện nghiêm ngặt trên 92,652 Buyers hợp lệ từ `buyer_features.parquet`, tuyệt đối không chạm vào tập Holdout tháng 02/2020.
  2. Sàng lọc minh bạch 28 cấu hình Vòng 1 và 40 cấu hình Vòng 2; không áp đặt chủ quan số cụm hay không gian đặc trưng.
  3. Lựa chọn $K=4$ trên không gian $F1$ (7 chiều) dựa trên Ma trận Đánh đổi Đa chiều (Pareto Dominance), đạt độ ổn định seed $\text{Mean ARI} = 0.9876 \pm 0.0077$, không có cụm suy thoái ($9.45\% \to 45.49\%$).
  4. Đã đối đầu thực nghiệm và chứng minh Standard K-Means vượt trội hơn MiniBatchKMeans cả về thời gian ($0.33$s) lẫn chất lượng hội tụ ($\Delta \text{WCSS} = +1.0\%$, agreement ARI chỉ 0.55).
  5. Đạt tính khả giải cao với Cây Quyết định Nông độ sâu 3 (Test Fidelity = 82.11%) và hình chiếu PCA 2D giải thích 76.40% phương sai.
  6. Xuất bản đầy đủ bộ artifacts đóng gói (.joblib, .parquet, .json, .csv) và 4 biểu đồ khoa học 300 DPI.
  7. Toàn bộ 50/50 unit tests và 5/5 validation scripts đều vượt qua 100%.

---

## Phase 5 — Model Evaluation & Business Segment Profiling (Ngày 11–13): HOÀN THÀNH (PASS)

### Checklist nhiệm vụ Phase 5

- [x] **Kiểm toán & Đóng băng Mô hình (Model Freeze & Pre-Holdout Audit):**
  - Niêm phong mô hình quán quân với mã băm an toàn **SHA-256: `ab98e132480914abb028c8009fd090030eef73ebf0faee2fa6dbd05e13dc9bfc`** (phiên bản `v1.0.0-f1-std-k4`).
  - Đối soát chính xác 905 bản ghi mua trùng lặp: 793 bản ghi trong Observation + 112 bản ghi trong Holdout ($793 + 112 = 905$).
  - Giải trình toán học & nghiệp vụ cho việc chọn $K=4$ thay vì $K=3$ (tách nhóm C2 có doanh thu tương lai gấp $4.70\times$ C0).
  - Giải trình StandardScaler sau biến đổi $\log(1+x)$ bảo toàn tỷ lệ phương sai đồng hướng so với RobustScaler.
- [x] **Hậu kiểm Chuỗi Thời gian Ngoài Mẫu trên Tháng 02/2020 (Out-of-Time Holdout Validation):**
  - Quét và liên kết toàn bộ 3,916,392 sự kiện sạch trong `data/cleaned/holdout_events.parquet`.
  - Bảo toàn 100% 92,652 khách hàng Buyers mà không làm thất thoát bất kỳ dòng dữ liệu nào.
  - Đo lường 9 chỉ số hành vi tương lai cho từng phân cụm (Future Purchase Rate, Future Activity Rate, Future Spend per Customer, v.v.).
- [x] **Xác nhận Trật tự Đơn điệu Hoàn hảo (Strict Monotonic Ordering):**
  - Tỷ lệ Mua Hàng Tương lai: Non-Buyers ($0.42\%$) < Cluster 0 ($2.66\%$) < Cluster 2 ($7.32\%$) < Cluster 3 ($10.13\%$) < Cluster 1 ($35.02\%$).
  - Doanh thu Đóng góp Tương lai / Khách hàng: Non-Buyers ($\$0.20$) < Cluster 0 ($\$0.91$) < Cluster 2 ($\$4.28$) < Cluster 3 ($\$4.91$) < Cluster 1 ($\$25.85$).
- [x] **Kiểm định Thống kê & Khoảng Tin cậy Wilson Score 95%:**
  - Sai số biên $< \pm 1.0\%$, không có bất kỳ sự chồng lấn nào giữa các khoảng tin cậy của 4 cụm.
  - Kiểm định Chi bình phương về tính độc lập đạt $p < 10^{-100}$.
- [x] **Đối chuẩn Toàn diện với 1,248,847 Khách hàng Chưa Mua (Non-Buyers Benchmark):**
  - Tỷ lệ chuyển đổi tự nhiên của Non-Buyers đạt $0.4226\%$ (5,278 người mua), đóng góp $\$245,011.20$ doanh thu.
  - Tỷ số nâng chuyển đổi tương lai: C0 gấp $6.3\times$, C2 gấp $17.3\times$, C3 gấp $24.0\times$, C1 gấp $82.9\times$ so với Non-Buyers.
- [x] **Định danh Nghiệp vụ (Business Personas) & Từ điển Nhãn:**
  - C0: Khách Mua 1 Lần Ngủ Đông Giá Trị Thấp (Dormant Low-Value Single Buyers) — 45.49%
  - C1: Khách VIP Trung Thành Cốt Lõi (Core VIP Champions) — 9.45%
  - C2: Khách Chi Tiêu Khá Đang Hạ Nhiệt / Nguy Cơ Rời Bỏ (At-Risk Cooling-Down Spenders) — 20.08%
  - C3: Khách Mua Gần Đây & Duyệt Web Tích Cực / Triển Vọng Mua Lại (Recently Active Repeat Prospects) — 24.98%
  - Xuất bản `outputs/models/cluster_business_labels.json`.
- [x] **Xuất bản 4 Biểu đồ Khoa học Phân giải cao (300 DPI):**
  - `fig17_future_purchase_rate.png` (Tỷ lệ mua tương lai kèm Wilson 95% CI).
  - `fig18_future_spend_per_customer.png` (Doanh thu trung bình trên khách hàng và trên người mua).
  - `fig19_segment_transition_sankey.png` (Sơ đồ chuyển dịch trạng thái hành vi từ Observation sang Holdout).
  - `fig20_cluster_profiles_comprehensive.png` (Radar profile và Heatmap chân dung đa chiều kết hợp quá khứ & tương lai).
- [x] **Đo lường Hiệu năng Thực tế (Benchmark Profiling):**
  - Thời gian thực thi toàn trình Phase 5: **25.85 giây**.
  - Mức tiêu hao RAM tối đa (Peak Process RSS): **211.06 MB** (kiểm soát an toàn dưới ngưỡng 2 GB).
- [x] **Kiểm thử Phần mềm Tự động:**
  - Bổ sung 10 unit tests trong `tests/test_phase5_evaluation.py`.
  - Toàn bộ test suite đạt **60/60 PASS (2.54s)**.
  - Chuỗi 6 script kiểm chứng (`validate_phase0.py` đến `validate_phase5.py`) đều **PASS 100%**.

---

### Kết luận Cổng Nghiệm thu Phase 5 (Phase Gate 5)

- **Quyết định:** **PASS**
- **Căn cứ & Bằng chứng:**
  1. Hậu kiểm trên toàn bộ 3.92M sự kiện Holdout tháng 02/2020 chứng minh các phân cụm có khả năng phân hóa hành vi tương lai sắc bén và tuân thủ trật tự đơn điệu hoàn hảo cả về tỷ lệ mua ($2.66\% \to 35.02\%$) và chi tiêu bình quân ($\$0.91 \to \$25.85$).
  2. Bằng chứng thực nghiệm khẳng định việc chọn $K=4$ là hoàn toàn chính xác: Cluster 2 có chi tiêu tương lai gấp $4.70\times$ Cluster 0, bảo vệ doanh nghiệp khỏi việc đánh đồng khách hàng giá trị cao với khách mua vãng lai.
  3. Khoảng tin cậy Wilson Score 95% có sai số biên $< \pm 1.0\%$, không chồng lấn, kiểm định $\chi^2$ đạt $p < 10^{-100}$.
  4. Đã đối chuẩn đầy đủ với 1.25 triệu khách hàng chưa mua, xác lập nền tảng khoa học cho chiến lược phễu ở Phase 6.
  5. Đầy đủ bộ artifacts (.json, 4 figures 300 DPI), tài liệu báo cáo và sổ tay được cập nhật đồng bộ.
  6. Toàn bộ 60/60 unit tests và 6/6 kịch bản validation đều vượt qua 100%.

---

## Phase 6 — Prescriptive Marketing Decision Support Engine (Ngày 13–14): HOÀN THÀNH (PASS)

### Checklist nhiệm vụ Phase 6

- [x] **Xử lý Triệt để & Tiếp thu Khuyến nghị Audit Phase 5:**
  - Làm rõ tính độc lập của Holdout: Việc chọn $K=4$ hoàn toàn dựa trên dữ liệu Observation (điểm gập Elbow, độ ổn định khởi tạo ARI = 0.988, cân bằng kích thước). Holdout tháng 02/2020 được niêm phong nghiêm ngặt, chỉ đóng vai trò hậu kiểm ngoài mẫu về giá trị nghiệp vụ, không phải tiêu chí tối ưu chọn mô hình.
  - Hiệu chỉnh thuật ngữ tiếp thị: Bãi bỏ các khẳng định "cam kết ROI" hoặc "chắc chắn tăng doanh thu"; thay bằng các chỉ số quan sát khách quan: Tỷ lệ mua tương lai quan sát được, Doanh thu tương lai bình quân, Cơ hội kinh doanh tương đối, và Chiến thuật ứng viên cần A/B testing trước khi mở rộng ngân sách.
  - Định vị chuẩn mực của Surrogate Tree: Cây quyết định nông (độ sâu 3, fidelity 82.11%, tỷ lệ lệch 18%) chỉ đóng vai trò bộ giải thích xấp xỉ trực quan; Decision Engine vận hành trên nhãn phân cụm thực tế `cluster_id` từ K-Means kết hợp bằng chứng cá nhân hóa.
  - Thống nhất chỉ số tăng tốc Benchmark: Đạt **8.09x median fair benchmark** (cold speedup 6.57x) trên cùng 19.58M bản ghi sạch.
- [x] **Kiểm thử Khói Mô hình (Model Artifact Smoke Test) (`scripts/smoke_test_model_inference.py`):**
  - Xây dựng `SafeNumpyUnpickler` vượt qua rào cản Windows 11 Smart App Control chặn Cython DLLs (`_fast_dict.pyd`), giải nén an toàn toàn bộ trọng số từ `outputs/models/kmeans_best_model.joblib` (SHA-256 `ab98e13248...`).
  - Trích xuất ma trận tâm cụm (4, 7), scaler mean (7), scaler scale (7) và PCA components (2, 7).
  - Tái tạo vector hóa suy luận (Log1p transform $\to$ Standardize $\to$ Argmin Euclidean Distance).
  - Đối soát độc lập trên 1,000 khách hàng mẫu: **Khớp tuyệt đối 1,000 / 1,000 (100.00%) với `buyer_clusters.parquet`**.
- [x] **Định nghĩa Bộ Luật Tiếp thị Minh bạch (`configs/marketing_rules.yaml`):**
  - Chuẩn hóa 7 Mục tiêu Tiếp thị cấp chiến lược (`RETAIN_HIGH_VALUE`, `ENCOURAGE_REPEAT_PURCHASE`, `REENGAGE_INACTIVE`, `SUPPORT_CART_COMPLETION`, `INCREASE_PRODUCT_DISCOVERY`, `LOW_COST_NURTURE`, `NO_ACTION`).
  - Chuẩn hóa 8 Chiến thuật Tiếp thị Ứng viên (`TAC_LOYALTY_VIP`, `TAC_CROSS_SELL`, `TAC_POST_PURCHASE_CARE`, `TAC_CART_RECOVERY`, `TAC_WINBACK_SURVEY`, `TAC_PRODUCT_EDU`, `TAC_LOW_COST_NURTURE`, `TAC_NO_ACTION`).
  - Thiết lập 4 Phân tầng Tương tác Khách hàng Chưa Mua (Non-Buyer Engagement Tiers): `HIGH_INTENT`, `EXPLORING`, `LOW_ENGAGEMENT`, `INACTIVE` dựa trên phân phối percentile quan sát thực tế (không gán recency giả vô nghĩa).
  - Thiết lập 5 Hàng rào Bảo vệ Ngân sách & Tránh Spam (Guardrails G1–G5).
  - Tích hợp bộ quy tắc lý giải (Reason Codes) và KPI đo lường định lượng tương ứng cho từng hành động.
- [x] **Xây dựng Mô-đun Quyết định Hỗ trợ Ra Quyết định (`src/decision_engine/rules.py`):**
  - Lớp `MarketingDecisionRules` cài đặt phương thức `evaluate_customer()` đánh giá chi tiết từng cá nhân.
  - Triệt tiêu ánh xạ tĩnh (Anti-Fixed Mapping): Trong cùng một phân cụm, người dùng được định tuyến đến các chiến thuật khác nhau tùy theo hành vi giỏ hàng gần đây, độ trôi dạt tương tác và ngưỡng chi tiêu.
  - Trả lời đầy đủ 3 câu hỏi cốt lõi cho mọi khuyến nghị: **Tại sao chọn chiến thuật này? Dựa trên bằng chứng dữ liệu nào? Đo lường hiệu quả bằng KPI gì?**
- [x] **Kiểm chứng Toàn diện trên 8 Hồ sơ Điển hình (8 Archetypes Verification):**
  - ARC-01 (Active VIP Champion) $\to$ `TAC_LOYALTY_VIP` (Mục tiêu: RETAIN_HIGH_VALUE).
  - ARC-02 (Cooling VIP) $\to$ `TAC_WINBACK_SURVEY` (Mục tiêu: REENGAGE_INACTIVE).
  - ARC-03 (Active Cart Abandoner) $\to$ `TAC_CART_RECOVERY` (Mục tiêu: SUPPORT_CART_COMPLETION).
  - ARC-04 (High-Value Cooling) $\to$ `TAC_WINBACK_SURVEY` (Mục tiêu: REENGAGE_INACTIVE).
  - ARC-05 (Low-Value Single Inactive) $\to$ `TAC_LOW_COST_NURTURE` (Mục tiêu: LOW_COST_NURTURE).
  - ARC-06 (Single Zero-Activity Budget Guard) $\to$ `TAC_NO_ACTION` (Kích hoạt Guardrail G3).
  - ARC-07 (High-Intent Non-Buyer) $\to$ `TAC_CART_RECOVERY` (Mục tiêu: SUPPORT_CART_COMPLETION).
  - ARC-08 (Cold Non-Buyer Bounce) $\to$ `TAC_NO_ACTION` (Kích hoạt Guardrail G5).
- [x] **Thực thi Toàn diện trên Toàn bộ 1,341,499 Khách hàng (`scripts/phase6_decision_support.py`):**
  - Xử lý 92,652 Buyers trong **0.83 giây**; xuất bản `outputs/recommendations/buyer_recommendations.parquet` (1.12 MB).
  - Xử lý 1,248,847 Non-Buyers trong **3.36 giây**; xuất bản `outputs/recommendations/non_buyer_recommendations.parquet` (5.84 MB).
  - Tổng thời gian thực thi: **4.52 giây**; Thông lượng: **296,528.0 khách hàng/giây**; Peak Process RSS: **314.68 MB** (kiểm soát an toàn tuyệt đối).
  - Xuất bản hồ sơ tổng kết nghiệm thu: `outputs/experiments/phase6_decision_support_summary.json`.
- [x] **Phân tích Cơ cấu Khuyến nghị & Hiệu ứng Bảo vệ Doanh nghiệp:**
  - Tính đa dạng trong phân cụm:
    - Cluster 1 (VIP, N=8,755): 84.73% `TAC_LOYALTY_VIP`, 14.70% `TAC_CART_RECOVERY`, 0.31% `TAC_WINBACK_SURVEY`, 0.26% `TAC_POST_PURCHASE_CARE`.
    - Cluster 2 (At-Risk, N=18,608): 70.77% `TAC_WINBACK_SURVEY`, 19.67% `TAC_LOW_COST_NURTURE`, 9.56% `TAC_CART_RECOVERY`.
    - Cluster 3 (Active, N=23,144): 96.01% `TAC_CART_RECOVERY`, 2.91% `TAC_CROSS_SELL`, 0.84% `TAC_PRODUCT_EDU`, 0.24% `TAC_POST_PURCHASE_CARE`.
    - Cluster 0 (Dormant, N=42,145): 75.29% `TAC_LOW_COST_NURTURE`, 15.26% `TAC_NO_ACTION` (Guardrail G3), 7.06% `TAC_PRODUCT_EDU`, 2.38% `TAC_CART_RECOVERY`.
  - Phân tầng Khách chưa mua (Non-Buyers, N=1,248,847):
    - `HIGH_INTENT`: 34,061 (2.73%) $\to$ `TAC_CART_RECOVERY`.
    - `EXPLORING`: 81,994 (6.57%) $\to$ `TAC_PRODUCT_EDU`.
    - `LOW_ENGAGEMENT`: 246,717 (19.76%) $\to$ `TAC_LOW_COST_NURTURE`.
    - `INACTIVE`: 886,075 (70.95%) $\to$ `TAC_NO_ACTION` (Guardrail G5).
  - Cơ chế Tiếp thị Có trách nhiệm (Responsible Marketing): **100% (1,341,499) khuyến nghị mang trạng thái `PENDING_CONSENT`**.
  - Bảo vệ ngân sách: 66.53% dân số (892,508 tài khoản) được xếp vào `NO_ACTION`, ngăn chặn lãng phí hàng chục nghìn USD chi phí tiếp thị spam vào các tài khoản không có tín hiệu phản hồi.
- [x] **Cập nhật Báo cáo Học thuật & Sổ tay Kỹ thuật:**
  - Hoàn thiện Chương 9 trong `reports/DATA_ANALYTICS_REPORT.md` với đầy đủ cấu trúc 7 mục tiêu, 8 chiến thuật, ma trận đa dạng nội cụm, bảng giải trình 8 archetypes, và 5 rào chắn bảo vệ ngân sách.
  - Bổ sung Phần VII (P6.1 – P6.9) trong `reports/TECHNICAL_LEARNING_NOTES.md` theo cấu trúc 9 phần chuẩn kèm bộ 7 câu hỏi vấn đáp bảo vệ đồ án Q39–Q45.
- [x] **Kiểm thử Phần mềm Tự động:**
  - Bổ sung 12 unit tests trong `tests/test_phase6_decision_engine.py` kiểm thử toàn diện quy tắc định tuyến, tính đa dạng nội cụm, các rào cản G1-G5, tính bất biến dữ liệu.
  - Toàn bộ test suite đạt **72/72 PASS (6.63s)**.
  - Chuỗi 7 kịch bản kiểm chứng (`validate_phase0.py` đến `validate_phase6.py`) đều **PASS 100%**.

---

### Kết luận Cổng Nghiệm thu Phase 6 (Phase Gate 6)

- **Quyết định:** **PASS**
- **Căn cứ & Bằng chứng:**
  1. Đã tiếp thu và giải quyết triệt để 100% các khuyến nghị từ cổng kiểm toán Phase 5 (tính độc lập Holdout, tính khiêm tốn của luận điểm ROI, vai trò của Surrogate Tree, benchmark 8.09x).
  2. Khắc phục triệt để rào cản Windows 11 Smart App Control qua `SafeNumpyUnpickler`; smoke test xác thực 100% sự tương thích giữa model artifact và parquet clusters.
  3. Xây dựng thành công Rule Engine minh bạch, loại bỏ hoàn toàn ánh xạ tĩnh cứng nhắc; chứng minh tính phân hóa rõ rệt trong cùng một phân cụm (ví dụ Cluster 1 phân bổ thành 4 chiến thuật khác nhau).
  4. Phân tầng thành công 1.25 triệu Non-Buyers thành 4 tiers hành vi khách quan mà không gán Recency giả.
  5. Bảo vệ ngân sách vượt trội: Lọc 66.53% tài khoản sang `NO_ACTION` và đặt 100% khuyến nghị ở trạng thái `PENDING_CONSENT`.
  6. Xử lý toàn bộ 1,341,499 khách hàng chỉ trong 4.52 giây (296.5k khách hàng/giây), tiêu thụ 314.68 MB RAM.
  7. Toàn bộ 72/72 unit tests và chuỗi 7 kịch bản validation đều vượt qua 100%.

---

## Phase 7 — Export Snapshot & IVRE Owner Research Dashboard (Ngày 15–17): HOÀN THÀNH (PASS)

### Checklist nhiệm vụ Phase 7

- [x] **Xử lý Dứt điểm Khuyến nghị Kiểm toán Phase 6:**
  - Đối soát độc lập suy luận K-Means trên toàn bộ 92,652 Buyers: Kịch bản `scratch/verify_all_92k_buyers.py` xác thực vector hóa không gian $F1$ (7 đặc trưng, $\log(1+x)$ trên 5 biến, 2 biến tuyến tính) đạt tỷ lệ khớp **92,652 / 92,652 (100.0000%)** với `buyer_clusters.parquet`. Đính chính đoạn nhầm lẫn trong văn bản báo cáo.
  - Chuẩn hóa khái niệm giỏ hàng: Chuyển đổi nhãn `TAC_CART_RECOVERY` trên 34,061 Non-Buyers thành `Candidate Cart Follow-Up` dựa trên tín hiệu quan tâm giỏ hàng trong 30 ngày, phân định rõ không khẳng định sự tồn tại của giỏ hàng mở trên database giao dịch.
  - Tách bạch kịch bản chi phí giả định: Trình bày số tiền tiết kiệm \$4,460 – \$17,850/tuần dưới dạng `Hypothetical Marketing Cost Avoidance Scenario` với giả định rõ ràng (1 tin/tuần, đơn giá \$0.005–\$0.02) trên 892,508 tài khoản bị chặn (G3 & G5).
  - Kiểm toán cấu trúc Parquet: Xác nhận đầy đủ 100% các trường phục vụ giải trình (`reason_codes`, `evidence`, `primary_kpi`, `guardrails_applied`, `eligibility_status`, `ruleset_version`, `model_version`).
- [x] **Xây dựng Kịch bản Xuất bản Snapshot Dữ liệu (`scripts/build_phase7_snapshot.py`):**
  - Tích hợp DuckDB tổng hợp đa tầng: Tạo `outputs/dashboard/ivre_dashboard_snapshot.json` (32.98 KB trong 0.18s), giảm 99.98% dung lượng so với dữ liệu thô.
  - Xuất bản các tệp modular json (`summary_snapshot.json`, `segments_snapshot.json`, `recommendations_snapshot.json`, `holdout_evaluation_snapshot.json`, `model_system_insights_snapshot.json`).
  - Xuất bản `outputs/dashboard/snapshot_manifest.json` ghi nhận kích thước và mã băm SHA-256 niêm phong cho từng tệp.
- [x] **Thiết kế & Triển khai Giao diện Bảng Điều khiển Nghiên cứu (`outputs/dashboard/index.html`):**
  - Áp dụng triệt để phong cách **Dark Editorial Luxury (IVRE Atelier)**: Nền obsidian sâu (`#0a0c10`), viền hairline (`#202634`), điểm nhấn vàng ánh kim (`#c5a059`), kiểu chữ kết hợp *Cormorant Garamond* (Serif), *Inter* (Sans-serif) và *JetBrains Mono*.
  - Băng định vị nghiên cứu cố định: **`REES46 Cosmetics Research Demo — Historical Data 2019–2020`** (Read-Only Analytical Sandbox).
  - 6 Phân hệ chuyên đề tương tác: Executive Overview & Funnel, Customer Segmentation, Out-of-Time Holdout, Prescriptive Engine, Customer Recommendation Explorer, Model & System Insights.
- [x] **Bảo vệ Quyền Riêng tư & Tiếp thị Có Trách nhiệm:**
  - Zero Raw PII: Triệt tiêu hoàn toàn mã định danh người dùng thô; 8 hồ sơ nghiên cứu đại diện mang mã ẩn danh (`DEMO_BUYER_01`, `DEMO_NON_BUYER_01`...).
  - 100% khuyến nghị mang trạng thái `PENDING_CONSENT`.
  - Khóa an toàn thực thi (No-Execution Guardrail): Loại bỏ hoàn toàn nút bấm gửi chiến dịch hoặc API trigger bên ngoài.
- [x] **Kiểm thử Tự động & Xác thực Hợp đồng:**
  - Bổ sung 9 bài kiểm tra đơn vị trong `tests/test_phase7_dashboard_snapshot.py`, nâng tổng số test suite lên **81/81 PASS (1.99s)**.
  - Kịch bản `scripts/validate_phase7.py` kiểm chứng độc lập mã băm SHA-256, sự bảo toàn dân số 1,341,499 khách hàng, trật tự đơn điệu holdout và đạt **PASS 100%**.
  - Toàn bộ chuỗi 8 kịch bản validation liên hoàn từ Phase 0 đến Phase 7 (`validate_phase0.py` đến `validate_phase7.py`) đều **PASS 100%**.
- [x] **Cập nhật Báo cáo Học thuật & Sổ tay Kỹ thuật:**
  - Hoàn thiện Chương 10 trong `reports/DATA_ANALYTICS_REPORT.md`: "Dashboard Integration & Research Visualization".
  - Hoàn thiện Phần VIII (P7.1 – P7.9) trong `reports/TECHNICAL_LEARNING_NOTES.md` theo cấu trúc 9 phần chuẩn kèm bộ 7 câu hỏi vấn đáp bảo vệ đồ án Q46–Q52.

---

### Kết luận Cổng Nghiệm thu Phase 7 (Phase Gate 7)

- **Quyết định:** **PASS**
- **Căn cứ & Bằng chứng:**
  1. Đã giải quyết triệt để 100% các khuyến nghị kiểm toán Phase 6; chứng minh tính nhất quán của mô hình trên 100% 92,652 buyers.
  2. Xuất bản thành công bộ Static Snapshot gọn nhẹ (32.98 KB), có mã băm SHA-256 bảo vệ tính toàn vẹn trong `snapshot_manifest.json`.
  3. Bảo toàn tuyệt đối số học trên toàn bộ 1,341,499 khách hàng (92,652 buyers + 1,248,847 non-buyers), 4 clusters và 4 non-buyer tiers.
  4. Trực quan hóa chuẩn mực trật tự đơn điệu ngoài mẫu ($0.42\% \to 35.02\%$) kèm khoảng tin cậy Wilson Score 95% có sai số biên $< \pm 1.0\%$.
  5. Đảm bảo an toàn quyền riêng tư: 0 ID khách hàng thô trên giao diện web; 100% khuyến nghị gắn cờ `PENDING_CONSENT` và không có nút kích hoạt gửi tin.
  6. Giao diện Dark Editorial Luxury hoạt động mượt mà, tải trang tức thì (<50ms).
  7. Toàn bộ 81/81 unit tests và chuỗi 8 kịch bản validation liên hoàn đều vượt qua 100%.

---

## Nhật ký Quyết định Thiết kế (Decision Log)

| Ngày       | Quyết định thiết kế                                                                              | Cơ sở lý luận / Căn cứ                                                                                                                        | Hạng mục kiểm chứng còn lại                                                         |
| ---------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 2026-11-06 | Sử dụng DuckDB với `memory_limit = '2GB'` và `threads = 4` để profiling 20.7M dòng CSV.          | Bộ nhớ RAM khả dụng máy trạm chỉ còn ~2.3 GB; Pandas sẽ gây OOM; DuckDB stream trực tiếp từ đĩa.                                              | Đã chứng minh: Peak RSS đạt 1.62 GB, an toàn tuyệt đối.                             |
| 2026-11-06 | Bỏ qua trường `category_code` làm đặc trưng chính; ưu tiên dùng `category_id`.                   | `category_code` khuyết tới 98.29%, trong khi `category_id` hoàn thiện 100%.                                                                   | Đã áp dụng ở Phase 3.                                                               |
| 2026-11-06 | Áp dụng quy tắc cắt cứng (Strict Event-level Cutoff) cho 10,451 spanning sessions.               | Bảo toàn tính đóng băng dữ liệu huấn luyện, triệt tiêu rò rỉ thông tin từ tháng 2 vào observation.                                            | Đã chứng minh: Không rò rỉ dữ liệu qua cutoff.                                      |
| 2026-11-06 | Loại bỏ các dòng có `price <= 0` khi tính toán Monetary ở Phase 2.                               | Phát hiện 131 dòng giá âm và 104,157 dòng giá 0; giữ lại cho Engagement nhưng loại khỏi Monetary.                                             | Đã chứng minh: Cờ `is_valid_for_monetary` loại đúng 88 giao dịch mua $\le 0$.       |
| 2026-11-06 | Chuyển đổi toàn bộ CSV sang Clean Parquet trong Phase 2.                                         | Giảm dung lượng đĩa từ 2.3 GB xuống <500 MB và tăng tốc độ trích xuất đặc trưng RFM ở Phase 3 gấp 5–10 lần.                                   | Đã chứng minh ở Phase 3: Quét 15.67M dòng chỉ mất 5.14 giây.                        |
| 2026-11-06 | Thiết lập Composite Key `user_session_id = user_id \| '_' \| user_session`.                      | Khắc phục 331 trường hợp UUID phiên trùng giữa các user khác nhau do dùng chung máy/cookie va chạm.                                         | Đã chứng minh: 0 xung đột trên 4,536,272 phiên.                                     |
| 2026-11-07 | Tách riêng hai tệp `buyer_features.parquet` và `non_buyer_features.parquet`.                     | Ngăn chặn việc gán giá trị nhân tạo Recency = 999 làm biến dạng không gian Euclidean của K-Means.                                             | Đã chứng minh ở Phase 3: 92,652 buyers và 1,248,847 non-buyers tách biệt hoàn toàn. |
| 2026-11-07 | Áp dụng Laplace smoothing (+1) cho `log_activity_ratio`.                                         | Triệt tiêu lỗi chia cho 0 khi khách hàng không có phiên trong tháng trước; tạo phân phối đối xứng quanh 0.                                    | Đã chứng minh ở Phase 3: Skewness đạt 0.15, Mean = 0.04.                            |
| 2026-11-07 | Lựa chọn cấu hình Quán quân: Không gian $F1$ (7D) + StandardScaler + Standard K-Means với $K=4$. | Cân bằng đa chiều: ARI stability = 0.988, không có cụm suy thoái ($> 9.4\%$), giải thích được cả hành vi mua lẫn tương tác số, runtime 0.37s. | Hậu kiểm trên tập Holdout tháng 02/2020 ở Phase 5.                                  |
| 2026-11-07 | Loại bỏ MiniBatchKMeans; giữ nguyên Standard K-Means.                                            | Dữ liệu 92k dòng chỉ mất 0.33s với KMeans chuẩn; MiniBatch không tiết kiệm thời gian mà làm tăng WCSS +1% và agreement ARI chỉ 0.55.          | Đã kiểm chứng thực nghiệm.                                                          |
| 2026-11-07 | Dùng Cây Quyết định Nông (`max_depth = 3`) làm Surrogate Model.                                  | Cung cấp bộ luật If-Then trực quan với Test Fidelity đạt 82.11% phục vụ cấu hình rule engine ở Phase 6.                                       | Triển khai ở Phase 6.                                                               |
| 2026-11-09 | Đóng băng mô hình với mã băm SHA-256 trước khi hậu kiểm Holdout tháng 02/2020.                   | Triệt tiêu nguy cơ điều chỉnh mô hình bằng dữ liệu tương lai (Lookahead Bias), bảo đảm tính khách quan tuyệt đối.                              | Đã chứng minh: Model hash `ab98e13248...` bất biến.                                 |
| 2026-11-09 | Sử dụng Khoảng Tin cậy Wilson Score 95% thay vì khoảng Wald cổ điển.                             | Tỷ lệ chuyển đổi nhỏ ($0.4\% \to 2\%$) khiến khoảng Wald bị sai lệch xác suất hoặc tính ra cận dưới âm; Wilson chính xác tuyệt đối.            | Đã chứng minh: Cận dưới và trên luôn hợp lệ, sai số $< \pm 1.0\%$.                  |
| 2026-11-09 | Đưa toàn bộ 1.25 triệu Non-Buyers vào làm đối chuẩn cơ sở (Benchmark Baseline).                  | Cung cấp mức sàn chuyển đổi tự nhiên toàn sàn ($0.42\%$), định lượng tỷ số nâng chuyển đổi cho từng cụm.                                       | Đã chứng minh: Phân tích đầy đủ ở Phase 5.                                          |
| 2026-11-09 | Xây dựng SafeNumpyUnpickler để smoke test model artifact.                                        | Windows 11 Smart App Control chặn Cython DLLs (`_fast_dict.pyd`); unpickler an toàn bóc tách weights nguyên thủy mà không nạp Cython module.   | Đã chứng minh: Tái tạo vector hóa khớp 1,000/1,000 khách hàng mẫu.                 |
| 2026-11-09 | Khử tĩnh hóa luật tiếp thị (Anti-Fixed Mapping).                                                 | Tránh áp đặt 1 cụm $\to$ 1 hành động duy nhất; định tuyến động theo bằng chứng cá nhân hóa (giỏ hàng gần đây, trôi dạt tương tác, mức chi tiêu). | Đã chứng minh: Cả 4 cụm đều có độ phân tán từ 3–4 chiến thuật khác nhau.            |
| 2026-11-09 | Phân tầng Non-Buyers thành 4 Engagement Tiers dựa trên phân phối percentile thực tế.            | Không gán Recency giả; phân hóa chính xác người có ý định mua cao (High Intent có cart) và người không hoạt động (Inactive).                     | Đã chứng minh: 34k High Intent nhận Cart Recovery; 886k Inactive chuyển NO_ACTION. |
| 2026-11-09 | Thiết lập cơ chế Tiếp thị Có Trách nhiệm (Responsible Marketing & Pending Consent).              | 100% khuyến nghị mang trạng thái `PENDING_CONSENT`, bắt buộc qua phê duyệt người quản lý chiến dịch trước khi kích hoạt.                         | Đã chứng minh: 1,341,499 khuyến nghị đều có trạng thái hợp lệ.                      |
| 2026-11-09 | Áp dụng Guardrail G3 và G5 để bảo vệ ngân sách tối đa.                                           | Đưa 66.53% khách hàng (892k users) vào `TAC_NO_ACTION` nhằm triệt tiêu lãng phí tiếp thị vào tài khoản không có tín hiệu phản hồi.             | Đã chứng minh: Tiết kiệm chi phí tiếp thị spam trên toàn hệ thống.                  |
| 2026-11-10 | Áp dụng kiến trúc Static Verified Snapshot thay vì Dynamic Database API.                         | Dữ liệu lịch sử là đóng băng; static snapshot (32.98 KB) loại trừ nguy cơ OOM trình duyệt và cho phép gắn mã băm SHA-256 niêm phong dữ liệu.     | Đã chứng minh: Snapshot tải trong <50ms; bảo đảm tính bất biến.                      |
| 2026-11-10 | Triệt tiêu hoàn toàn mã định danh cá nhân thô (Zero Raw PII Policy) trên Dashboard.              | Không xuất ID số nguyên thô ra file JSON web; dùng 8 hồ sơ nghiên cứu ẩn danh (`DEMO_BUYER_01`...) để minh họa logic giải trình.                | Đã chứng minh: `test_07_privacy_and_anonymization` PASS 100%.                       |
| 2026-11-10 | Chuẩn hóa khái niệm Candidate Cart Follow-Up cho 34k Non-Buyers.                                 | Dữ liệu clickstream chỉ phản ánh tín hiệu quan tâm giỏ hàng trong 30d, không khẳng định sự tồn tại của giỏ hàng mở trên database giao dịch.     | Đã chứng minh: Rõ ràng trên giao diện và tài liệu.                                  |
| 2026-11-10 | Thiết lập rào cản Khóa Thực thi (No-Execution Guardrail) trên giao diện quản trị.                | Dashboard đóng vai trò hỗ trợ ra quyết định (Decision Support); loại bỏ hoàn toàn nút gửi chiến dịch thật để phòng tránh rủi ro gửi nhầm spam.    | Đã chứng minh: Không có endpoint hay nút gửi tin tự động.                           |

---

## Nhật ký Thực thi Lệnh Thực tế (Run Log)

| Thời gian (UTC+7)   | Lệnh thực thi                                     | Kết quả thực tế        | Ý nghĩa & Bằng chứng kiểm chứng                                                                                                                  |
| ------------------- | ------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2026-11-06 11:38:33 | `pip install scikit-learn matplotlib`             | **SUCCESS**            | Bổ sung scikit-learn 1.9.1, matplotlib 3.11.2, scipy 1.18.1 vào `.venv`.                                                                         |
| 2026-11-06 11:43:17 | `python scripts/phase1_profiling.py`              | **SUCCESS (78.39s)**   | Xử lý 20,692,840 dòng, xuất bản 8 biểu đồ và lưu hồ sơ `phase1_data_profile.json`.                                                               |
| 2026-11-06 11:49:15 | `python scripts/audit_phase1_findings.py`         | **SUCCESS**            | Kiểm toán đính chính: Ngày đỉnh 22/11, 104k giá $\le 0$, 331 session collisions.                                                                 |
| 2026-11-06 11:55:20 | `python scripts/phase2_etl.py`                    | **SUCCESS (212.18s)**  | Khử 1.1M trùng lặp, xuất 3 tệp Parquet, Benchmark Speedup 8.33x.                                                                                 |
| 2026-11-07 00:19:05 | `python scripts/verify_session_reconciliation.py` | **SUCCESS**            | Đối soát số phiên: 0 phiên mất, giải trình số 1,533 là user có phiên NULL.                                                                       |
| 2026-11-07 00:20:18 | `python scripts/audit_deduplication_impact.py`    | **SUCCESS**            | Đối soát tác động dedup: 0 user, 0 session, 0 buyer, 0 cart session bị mất.                                                                      |
| 2026-11-07 00:21:50 | `python scripts/fair_benchmark.py`                | **SUCCESS**            | Fair benchmark trên cùng 19.58M dòng: Median Speedup 8.09x, Cold 6.57x.                                                                          |
| 2026-11-07 00:22:12 | `python scripts/audit_monetary_3step.py`          | **SUCCESS**            | Đối soát Monetary 3 bước: 5.141M $\to$ 5.138M $\to$ 5.141M (net -448.76).                                                                        |
| 2026-11-07 00:23:15 | `python scripts/update_parquet_schema.py`         | **SUCCESS**            | Bổ sung 4 cờ độc lập vào 3 tệp Parquet sạch trong 18.99s.                                                                                        |
| 2026-11-07 00:30:03 | `python scripts/phase3_feature_engineering.py`    | **SUCCESS (11.25s)**   | Trích xuất 1.34M khách hàng, xuất 3 tệp Parquet đặc trưng (25 MB) và 4 biểu đồ fig9-fig12. Peak RSS: 1,478 MB.                                   |
| 2026-11-07 00:30:36 | `python scripts/validate_phase3.py`               | **PASS**               | Xác thực 1.34M khách hàng, RFM & Engagement contracts, 4 figures.                                                                                |
| 2026-11-07 00:30:57 | `python -m unittest discover -s tests -v`         | **40/40 PASS (1.77s)** | Kiểm thử toàn diện cả 8 tests P0, 10 tests P1, 12 tests P2 và 10 tests P3.                                                                       |
| 2026-11-07 00:54:54 | `python scratch/check_cases.py`                   | **SUCCESS**            | Xác nhận 3 trường hợp Monetary (92,652 hợp lệ, 0 invalid-only, 1.25M non-buyers), tỷ số tương tác 41x median.                                    |
| 2026-11-07 00:58:55 | `python scripts/phase4_clustering.py`             | **SUCCESS (131.53s)**  | Quét 28 screening + 40 stability models, huấn luyện model quán quân K=4, xuất 4 figures, PCA, Surrogate Tree, model bundle. Peak RSS: 349.18 MB. |
| 2026-11-07 00:59:10 | `python scripts/validate_phase4.py`               | **PASS**               | Xác thực model bundle, 92k cluster parquet, 4 figures, surrogate fidelity 82.11%, anti-leakage.                                                  |
| 2026-11-07 00:59:21 | `python -m unittest discover -s tests -v`         | **50/50 PASS (2.53s)** | Toàn bộ 50 unit tests kiểm thử P0, P1, P2, P3 và 10 tests mới của P4.                                                                            |
| 2026-11-07 00:59:33 | `python scripts/validate_phase[0-4].py`           | **5/5 PASS**           | Xác thực toàn bộ chuỗi kiểm chứng cả 5 phase từ P0 đến P4.                                                                                       |
| 2026-11-09 23:10:45 | `python scripts/phase5_evaluation.py`             | **SUCCESS (25.85s)**   | Hậu kiểm trên 3.92M Holdout events, 9 future metrics, Wilson CIs, xuất 4 figures fig17-fig20, JSON manifest. Peak RSS: 211.06 MB.                |
| 2026-11-09 23:13:50 | `python scripts/validate_phase4.py`               | **PASS**               | Xác thực Phase 4 ổn định không phụ thuộc pandas.                                                                                                 |
| 2026-11-09 23:13:54 | `python scripts/validate_phase5.py`               | **PASS**               | Xác thực toàn vẹn Phase 5: bảo toàn khách hàng, trật tự đơn điệu chuyển đổi & chi tiêu, 4 figures.                                               |
| 2026-11-09 23:14:00 | `python -m unittest discover -s tests -v`         | **60/60 PASS (2.54s)** | Toàn bộ 60 unit tests kiểm thử P0, P1, P2, P3, P4 và 10 tests mới của P5.                                                                        |
| 2026-11-09 23:14:12 | `python scripts/validate_phase[0-5].py`           | **6/6 PASS**           | Xác thực toàn bộ chuỗi kiểm chứng cả 6 phase từ P0 đến P5.                                                                                       |
| 2026-11-09 23:35:10 | `python scripts/smoke_test_model_inference.py`    | **SUCCESS (0.28s)**    | SafeNumpyUnpickler bypass Cython DLLs; khớp 1,000 / 1,000 (100.00%) dự đoán với cluster parquet.                                                 |
| 2026-11-09 23:42:25 | `python scripts/phase6_decision_support.py`       | **SUCCESS (4.52s)**    | Xử lý 1,341,499 khách hàng, thông lượng 296.5k/s, xuất 2 parquet recommendations, summary JSON. Peak RSS: 314.68 MB.                            |
| 2026-11-09 23:45:12 | `python scripts/validate_phase6.py`               | **PASS**               | Xác thực toàn vẹn Phase 6: đầy đủ cột, không null, hợp lệ goals/tactics/tiers/guardrails, 100% PENDING_CONSENT.                                 |
| 2026-11-09 23:46:05 | `python -m unittest discover -s tests -v`         | **72/72 PASS (6.63s)** | Toàn bộ 72 unit tests kiểm thử toàn diện cả 7 phase từ P0 đến P6.                                                                                |
| 2026-11-09 23:46:30 | `python scripts/validate_phase[0-6].py`           | **7/7 PASS**           | Xác thực toàn bộ chuỗi kiểm chứng cả 7 phase từ P0 đến P6 không có hồi quy nào.                                                                 |
| 2026-11-10 00:43:00 | `python scratch/verify_all_92k_buyers.py`         | **SUCCESS (0.22s)**    | Vectorized NumPy inference khớp tuyệt đối 92,652 / 92,652 (100.00%) với `buyer_clusters.parquet`.                                                |
| 2026-11-10 00:45:03 | `python scripts/build_phase7_snapshot.py`         | **SUCCESS (0.18s)**    | Xuất bản master snapshot `ivre_dashboard_snapshot.json` (32.98 KB), 5 modular snapshots và `snapshot_manifest.json` (SHA-256).                   |
| 2026-11-10 00:45:52 | `python scripts/validate_phase7.py`               | **PASS (0.05s)**       | Xác thực toàn vẹn Phase 7: checksums khớp 100%, bảo toàn dân số, đơn điệu holdout, zero PII, 100% PENDING_CONSENT.                              |
| 2026-11-10 00:48:10 | `python -m unittest discover -s tests -v`         | **81/81 PASS (1.99s)** | Toàn bộ 81 unit tests kiểm thử toàn diện cả 8 phase từ P0 đến P7.                                                                                |
| 2026-11-10 00:48:18 | `python scripts/validate_phase[0-7].py`           | **8/8 PASS**           | Xác thực toàn bộ chuỗi kiểm chứng cả 8 phase từ P0 đến P7 không có hồi quy nào.                                                                 |

---

| 2026-11-10 02:20:30 | Chrome DevTools MCP & Nav Timing API              | **SUCCESS**            | DOMContentLoaded: 16.8ms, DOM Interactive: 16.0ms, FCP: 256ms. Zero console error, zero horizontal overflow.     |
| 2026-11-10 02:26:00 | Ban hành `docs/IVRE_INTEGRATION_SPEC.md`          | **SUCCESS**            | Đặc tả hợp đồng tích hợp React Component, Iframe Sandbox và REST endpoints cho IVRE Owner Portal.                 |
| 2026-11-10 02:30:00 | `python -m unittest discover -s tests -v`         | **81/81 PASS (2.07s)** | Toàn bộ 81 bài tests PASS 100%, bảo đảm không hồi quy.                                                            |
| 2026-11-10 02:30:15 | `python scripts/validate_phase[0-7].py`           | **8/8 PASS**           | 100% kịch bản kiểm chứng đạt chuẩn.                                                                               |
| 2026-11-10 16:10:00 | Chrome DevTools Device Emulation Viewport Audit   | **OVERALL PASS**       | Đo lường thực tế Chromium engine: 320px & 390px đạt chuẩn 0px overflow trên cả 5 tabs; giải quyết triệt để lỗi 486px OS window limitation. |
| 2026-11-10 16:12:00 | Snapshot & Dashboard Reconciliation (Views/Sess)  | **VERIFIED & PASS**    | Tách bạch hoàn toàn Sessions 30d (Med: C1=9.0, C3=3.0) vs Views 30d (Med: C1=29.0, C3=8.0); bổ sung bảng đối soát vào Tab 2; cập nhật marketing wording. |
| 2026-11-10 16:12:30 | Full Regression (`unittest` + `validate_phase*`)  | **81/81 & 8/8 PASS**   | 100% tests & validation scripts PASS, checksum manifest đồng bộ.                                                   |

---

## Tổng kết Trạng thái Toàn bộ 8 Phase (CRISP-DM Completion Status)

- **P0 — Business Understanding:** **HOÀN THÀNH (PASS)** — Hợp đồng 16 KPI, 5 giả thuyết nghiên cứu H1–H5.
- **P1 — Data Understanding & EDA:** **HOÀN THÀNH (PASS)** — Profile 20.69M dòng, 8 biểu đồ EDA chuẩn mực.
- **P2 — Data Preparation & Cleaning:** **HOÀN THÀNH (PASS)** — Làm sạch 19.58M sự kiện, Parquet nén 4.92x, tăng tốc 8.09x.
- **P3 — Customer Features Engineering:** **HOÀN THÀNH (PASS)** — 1.34M khách, tách Buyers & Non-Buyers, tạo biến F0, F1, F2.
- **P4 — Customer Segmentation Modeling:** **HOÀN THÀNH (PASS)** — K-Means K=4 trên F1 (ARI=0.988), Cây Surrogate 82.11%.
- **P5 — Model Evaluation & Profiling:** **HOÀN THÀNH (PASS)** — Hậu kiểm ngoài mẫu Feb 2020 trên 3.92M events, trật tự đơn điệu.
- **P6 — Prescriptive Marketing Decision Engine:** **HOÀN THÀNH (PASS)** — 1.34M khuyến nghị (296k/s), 100% PENDING_CONSENT, bảo vệ 892k khách.
- **P7 — Export Snapshot & Clean Analytics Dashboard:** **HOÀN THÀNH (PASS)** — Hoàn thành Standalone Clean Minimalist Dashboard; ban hành `docs/IVRE_INTEGRATION_SPEC.md`; đạt chuẩn responsive thực tế tại 320px & 390px (0px overflow).
- **P8 — Final Verification, Defense Guide & Project Sign-off:** **HOÀN THÀNH (PASS)** — Kiểm chứng toàn trình 100%, hoàn thiện 12 chương báo cáo học thuật, sổ tay kỹ thuật 9 phần với 65 câu hỏi vấn đáp, kịch bản live demo 5–7 phút và dàn ý thuyết trình 12 slide.

---

## Kết luận Nghiệm thu Toàn dự án (Final Project Verdict)

> **TRẠNG THÁI CUỐI CÙNG: PASS (DỰ ÁN ĐÃ NGHIỆM THU TOÀN PHẦN VÀ SẴN SÀNG BẢO VỆ CHÍNH THỨC).**  
> Hệ thống tuân thủ 100% các cam kết khoa học, liêm chính dữ liệu, an toàn quyền riêng tư và khả năng tái lập độc lập.
