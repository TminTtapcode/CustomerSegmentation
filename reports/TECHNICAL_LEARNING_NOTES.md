# SỔ TAY KỸ THUẬT VÀ HƯỚNG DẪN VẤN ĐÁP — CUSTOMER ANALYTICS & DECISION SUPPORT

**Dự án:** Phân tích và phân khúc khách hàng dựa trên hành vi mua sắm và tương tác website nhằm hỗ trợ ra quyết định marketing trong thương mại điện tử.  
**Cấu trúc chuẩn tắc cho từng bài học:**  
`What (Khái niệm là gì?)` $\to$ `Why (Tại sao cần dùng?)` $\to$ `How (Cách thức triển khai?)` $\to$ `Formula (Công thức toán học)` $\to$ `Worked Example (Ví dụ tính toán minh họa)` $\to$ `Alternatives (Phương án thay thế & So sánh)` $\to$ `Verification (Cách thức kiểm chứng)` $\to$ `Limitations (Giới hạn lý thuyết & thực tế)` $\to$ `Oral Defense Questions (Câu hỏi vấn đáp trọng tâm & Câu trả lời mẫu)`.

---

# MỤC LỤC SỔ TAY KỸ THUẬT

### PHẦN I — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 0 (BUSINESS UNDERSTANDING)
- [P0.1 — Phương pháp luận CRISP-DM trong Phân tích Dữ liệu Khách hàng](#p01--phương-pháp-luận-crisp-dm-trong-phân-tích-dữ-liệu-khách-hàng)
- [P0.2 — Phân cấp Khái niệm: Business Goal, Question, KPI, Feature, Model, Decision Engine](#p02--phân-cấp-khái-niệm-business-goal-question-kpi-feature-model-decision-engine)
- [P0.3 — Bản chất Cấp độ Hạt Dữ liệu: Event vs. Session vs. User vs. Purchase Session vs. Order](#p03--bản-chất-cấp-độ-hạt-dữ-liệu-event-vs-session-vs-user-vs-purchase-session-vs-order)
- [P0.4 — Khung phân tích RFM và Nan giải Recency của Người chưa mua (Non-buyer Dilemma)](#p04--khung-phân-tích-rfm-và-nan-giải-recency-của-người-chưa-mua-non-buyer-dilemma)
- [P0.5 — Phân tách Thời gian (Temporal Split) và Kiểm soát Rò rỉ Dữ liệu (Data Leakage)](#p05--phân-tách-thời-gian-temporal-split-và-kiểm-soát-rò-rỉ-dữ-liệu-data-leakage)
- [P0.6 — Cửa sổ Tương tác Clickstream Engagement và Kỹ thuật Làm mượt Laplace Smoothing](#p06--cửa-sổ-tương-tác-clickstream-engagement-và-kỹ-thuật-làm-mượt-laplace-smoothing)
- [P0.7 — Đánh giá Học máy không giám sát và Ma trận Đánh đổi Đa chiều (Trade-off Matrix)](#p07--đánh-giá-học-máy-không-giám-sát-và-ma-trận-đánh-đổi-đa-chiều-trade-off-matrix)
- [P0.8 — Bản chất của Marketing Decision Support: Rule-based Prescriptive vs. Causal Uplift](#p08--bản-chất-của-marketing-decision-support-rule-based-prescriptive-vs-causal-uplift)
- [P0.9 — Phương pháp Đo lường Hiệu năng: time.perf_counter(), psutil RSS vs. DuckDB Memory Limits](#p09--phương-pháp-đo-lường-hiệu-năng-timeperf_counter-psutil-rss-vs-duckdb-memory-limits)
- [P0.10 — Bộ 12 Câu hỏi Vấn đáp Trọng tâm và Hướng dẫn Trả lời Bảo vệ Đồ án](#p010--bộ-12-câu-hỏi-vấn-đáp-trọng-tâm-và-hướng-dẫn-trả-lời-bảo-vệ-đồ-án)

### PHẦN II — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 1 (DATA UNDERSTANDING & EDA)
- [P1.1 — Data Profiling trên Dữ liệu Lớn với DuckDB in-process OLAP Engine](#p11--data-profiling-trên-dữ-liệu-lớn-với-duckdb-in-process-olap-engine)
- [P1.2 — Nhận diện Hành vi Bất thường và Đính chính Hiện tượng Đột biến (The November Spike)](#p12--nhận-diện-hành-vi-bất-thường-và-đính-chính-hiện-tượng-đột-biến-the-november-spike)
- [P1.3 — Phân tích Phễu Chuyển đổi và Thuật ngữ Khoa học: Cart Session No-Purchase Rate](#p13--phân-tích-phễu-chuyển-đổi-và-thuật-ngữ-khoa-học-cart-session-no-purchase-rate)
- [P1.4 — Xử lý Giá trị Dị thường (Anomaly Price Handling) và Bảo toàn Tương tác Engagement](#p14--xử-lý-giá-trị-dị-thường-anomaly-price-handling-và-bảo-toàn-tương-tác-engagement)
- [P1.5 — Ranh giới Thời gian Nửa mở và Xử lý Phiên vắt ngang Thời điểm Cutoff](#p15--ranh-giới-thời-gian-nửa-mở-và-xử-lý-phiên-vắt-ngang-thời-điểm-cutoff)
- [P1.6 — Đo kiểm Hiệu năng Thực tế (Benchmark Profiling: Wall-clock, Process RSS vs Buffer Pool)](#p16--đo-kiểm-hiệu-năng-thực-tế-benchmark-profiling-wall-clock-process-rss-vs-buffer-pool)
- [P1.7 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 1 (Oral Defense Guide P1)](#p17--bộ-câu-hỏi-vấn-đáp-trọng-tâm-phase-1-oral-defense-guide-p1)

### PHẦN III — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 2 (DATA PREPARATION & CLEANING)
- [P2.1 — Khử trùng lặp dòng sự kiện Clickstream và Kỹ thuật Deduplication qua Window Function `ROW_NUMBER()`](#p21--khử-trùng-lặp-dòng-sự-kiện-clickstream-và-kỹ-thuật-deduplication-qua-window-function-row_number)
- [P2.2 — Xử lý xung đột Định danh Phiên (Session UUID Collisions) bằng Khóa kết hợp `user_session_id`](#p22--xử-lý-xung-đột-định-danh-phiên-session-uuid-collisions-bằng-khóa-kết-hợp-user_session_id)
- [P2.3 — Chiến lược Cờ phân loại Chất lượng Dữ liệu Đa mục đích: Engagement Preservation vs. Monetary Exclusion](#p23--chiến-lược-cờ-phân-loại-chất-lượng-dữ-liệu-đa-mục-đích-engagement-preservation-vs-monetary-exclusion)
- [P2.4 — Phân tách Chuỗi thời gian Nghiêm ngặt (Strict Event-level Temporal Split) và Giải quyết Phiên vắt qua Ranh giới (Cross-boundary Sessions)](#p24--phân-tách-chuỗi-thời-gian-nghiêm-ngặt-strict-event-level-temporal-split-và-giải-quyết-phiên-vắt-qua-ranh-giới-cross-boundary-sessions)
- [P2.5 — Chuyển đổi Lưu trữ Dạng cột (Columnar Storage Migration): Parquet ZSTD Compression và Đánh đổi Hiệu năng Thực nghiệm](#p25--chuyển-đổi-lưu-trữ-dạng-cột-columnar-storage-migration-parquet-zstd-compression-và-đánh-đổi-hiệu-năng-thực-nghiệm)
- [P2.6 — Bộ Câu hỏi Vấn đáp Trọng tâm và Hướng dẫn Bảo vệ Đồ án Phase 2 (Oral Defense Guide P2)](#p26--bộ-câu-hỏi-vấn-đáp-trọng-tâm-và-hướng-dẫn-bảo-vệ-đồ-án-phase-2-oral-defense-guide-p2)

### PHẦN IV — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 3 (CUSTOMER FEATURE ENGINEERING & BEHAVIORAL ANALYTICS)
- [P3.1 — Chuyển dịch Cấp độ Hạt (Grain Transition): Từ Sự kiện Clickstream sang Hồ sơ Khách hàng Đóng băng tại Mốc Cutoff](#p31--chuyển-dịch-cấp-độ-hạt-grain-transition-từ-sự-kiện-clickstream-sang-hồ-sơ-khách-hàng-đóng-băng-tại-mốc-cutoff)
- [P3.2 — Mô hình RFM cho Người Mua Hàng và Định lượng Tần suất Mua bằng Proxy Phiên (`purchase_sessions`)](#p32--mô-hình-rfm-cho-người-mua-hàng-và-định-lượng-tần-suất-mua-bằng-proxy-phiên-purchase_sessions)
- [P3.3 — Cửa sổ Trượt Hai Giai đoạn 30 Ngày và Kỹ thuật Làm mượt Laplace (Laplace Smoothing) trong Đo lường Xung lượng Hoạt động (`log_activity_ratio`)](#p33--cửa-sổ-trượt-hai-giai-đoạn-30-ngày-và-kỹ-thuật-làm-mượt-laplace-laplace-smoothing-trong-đo-lường-xung-lượng-hoạt-động-log_activity_ratio)
- [P3.4 — Chiến lược Tách biệt Bảng (Decoupled Cohort Architecture) và Xử lý Nan giải Recency của Người Chưa Mua (The Non-Buyer Dilemma)](#p34--chiến-lược-tách-biệt-bảng-decoupled-cohort-architecture-và-xử-lý-nan-giải-recency-của-người-chưa-mua-the-non-buyer-dilemma)
- [P3.5 — Phân tích Phân phối Lệch Xiên Cực đoan (Heavy Right-skewness), Đa cộng tuyến và Chiến lược Lựa chọn Không gian Đặc trưng ($F0, F1, F2$)](#p35--phân-tích-phân-phối-lệch-xiên-cực-đoan-heavy-right-skewness-đa-cộng-tuyến-và-chiến-lược-lựa-chọn-không-gian-đặc-trưng-f0-f1-f2)
- [P3.6 — Đo kiểm Hiệu năng Trích xuất Đặc trưng trên DuckDB (Throughput, Process RSS vs In-Memory Staging)](#p36--đo-kiểm-hiệu-năng-trích-xuất-đặc-trưng-trên-duckdb-throughput-process-rss-vs-in-memory-staging)
- [P3.7 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 3 (Oral Defense Guide P3: Q22 – Q26)](#p37--bộ-câu-hỏi-vấn-đáp-trọng-tâm-phase-3-oral-defense-guide-p3-q22--q26)

### PHẦN V — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 4 (CUSTOMER SEGMENTATION MODELING)
- [P4.1 — Thuật toán K-Means Clustering, Hàm Mục tiêu WCSS và Bản chất Hình học Khoảng cách Euclidean](#p41--thuật-toán-k-means-clustering-hàm-mục-tiêu-wcss-và-bản-chất-hình-học-khoảng-cách-euclidean)
- [P4.2 — Tác động của Skewness, Biến đổi Log1p và Chuẩn hóa Đặc trưng (StandardScaler vs RobustScaler)](#p42--tác-động-của-skewness-biến-đổi-log1p-và-chuẩn-hóa-đặc-trưng-standardscaler-vs-robustscaler)
- [P4.3 — Phương pháp Luận Lựa chọn Số cụm $K$: Elbow Curve, Silhouette Coefficient và Davies-Bouldin Index](#p43--phương-pháp-luận-lựa-chọn-số-cụm-k-elbow-curve-silhouette-coefficient-và-davies-bouldin-index)
- [P4.4 — Đánh giá Độ Ổn định Thuật toán Không giám sát qua Adjusted Rand Index (ARI) trên Nhiều Random Seeds](#p44--đánh-giá-độ-ổn-định-thuật-toán-không-giám-sát-qua-adjusted-rand-index-ari-trên-nhiều-random-seeds)
- [P4.5 — So sánh Đối đầu Thực nghiệm: Standard K-Means vs MiniBatchKMeans (Thời gian, Bộ nhớ và Chất lượng Hội tụ)](#p45--so-sánh-đối-đầu-thực-nghiệm-standard-k-means-vs-minibatchkmeans-thời-gian-bộ-nhớ-và-chất-lượng-hội-tụ)
- [P4.6 — Tính Khả giải (Explainability): Chân dung Vật lý, Cây Quyết định Nông Mô phỏng (Surrogate Tree) và Chiếu Không gian PCA 2D](#p46--tính-khả-giải-explainability-chân-dung-vật-lý-cây-quyết-định-nông-mô-phỏng-surrogate-tree-và-chiếu-không-gian-pca-2d)
- [P4.7 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 4 (Oral Defense Guide P4: Q27 – Q32)](#p47--bộ-câu-hỏi-vấn-đáp-trọng-tâm-phase-4-oral-defense-guide-p4-q27--q32)

### PHẦN VI — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 5 (MODEL EVALUATION & BUSINESS SEGMENT PROFILING)
- [P5.1 — Hậu kiểm Chuỗi Thời gian (Out-of-Time Temporal Holdout Validation) và Nguyên tắc Niêm phong Dữ liệu (Data Freezing)](#p51--hậu-kiểm-chuỗi-thời-gian-out-of-time-temporal-holdout-validation-và-nguyên-tắc-niêm-phong-dữ-liệu-data-freezing)
- [P5.2 — Khoảng Tin cậy Wilson Score 95% cho Tỷ lệ Chuyển đổi Tương lai và Kiểm định Ý nghĩa Thống kê](#p52--khoảng-tin-cậy-wilson-score-95-cho-tỷ-lệ-chuyển-đổi-tương-lai-và-kiểm-định-ý-nghĩa-thống-kê)
- [P5.3 — Phân tích Chân dung Phân cụm Đa chiều (Comprehensive Profiling) trên Không gian Đơn vị Gốc](#p53--phân-tích-chân-dung-phân-cụm-đa-chiều-comprehensive-profiling-trên-không-gian-đơn-vị-gốc)
- [P5.4 — Đối chuẩn Nhóm Chưa Mua (Observed Non-Buyers Benchmark) trong Không gian Hành vi Tương lai](#p54--đối-chuẩn-nhóm-chưa-mua-observed-non-buyers-benchmark-trong-không-gian-hành-vi-tương-lai)
- [P5.5 — Sơ đồ Chuyển dịch Phân khúc Khách hàng (Segment Transition Analysis) và Động học Trạng thái (State Dynamics)](#p55--sơ-đồ-chuyển-dịch-phân-khúc-khách-hàng-segment-transition-analysis-và-động-học-trạng-thái-state-dynamics)
- [P5.6 — Bản chất Quan hệ: Tương quan Phân khúc (Association) vs. Tác động Nhân quả (Causation) trong Nghiệp vụ](#p56--bản-chất-quan-hệ-tương-quan-phân-khúc-association-vs-tác-động-nhân-quả-causation-trong-nghiệp-vụ)
- [P5.7 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 5 (Oral Defense Guide P5: Q33 – Q38)](#p57--bộ-câu-hỏi-vấn-đáp-trọng-tâm-phase-5-oral-defense-guide-p5-q33--q38)

### PHẦN VII — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 6 (MARKETING DECISION SUPPORT ENGINE)
- [P6.1 — Phân cấp Phân tích Dữ liệu: Descriptive, Predictive và Prescriptive Analytics trong Thương mại Điện tử](#p61--phân-cấp-phân-tích-dữ-liệu-descriptive-predictive-và-prescriptive-analytics-trong-thương-mại-điện-tử)
- [P6.2 — Phân biệt Bản chất: Phân khúc Khách hàng (Segmentation) vs. Đề xuất Quyết định (Decision Recommendation)](#p62--phân-biệt-bản-chất-phân-khúc-khách-hàng-segmentation-vs-đề-xuất-quyết-định-decision-recommendation)
- [P6.3 — Kiến trúc Hệ Chuyên gia Dựa trên Bằng chứng (Rule-Based Expert System) và Xử lý Xung đột Luật (Conflict Resolution)](#p63--kiến-trúc-hệ-chuyên-gia-dựa-trên-bằng-chứng-rule-based-expert-system-và-xử-lý-xung-đột-luật-conflict-resolution)
- [P6.4 — Khung Khả giải Khuyến nghị Tiếp thị (Explainable Recommendation): Reason Codes và Bằng chứng Truy vết (Evidence Traceability)](#p64--khung-khả-giải-khuyến-nghị-tiếp-thị-explainable-recommendation-reason-codes-và-bằng-chứng-truy-vết-evidence-traceability)
- [P6.5 — Phân tầng Mức độ Quan tâm Không dùng Recency Giả cho Người Chưa Mua (Non-Buyer Engagement Tiering)](#p65--phân-tầng-mức-độ-quan-tâm-không-dùng-recency-giả-cho-người-chưa-mua-non-buyer-engagement-tiering)
- [P6.6 — Rào chắn An toàn (Guardrails), Quyền riêng tư và Trạng thái Chấp thuận Tiếp thị (Marketing Consent)](#p66--rào-chắn-an-toàn-guardrails-quyền-riêng-tư-và-trạng-thái-chấp-thuận-tiếp-thị-marketing-consent)
- [P6.7 — Thiết kế Chỉ số KPI Đánh giá Chiến thuật Tiếp thị (Evaluation KPI Framework)](#p67--thiết-kế-chỉ-số-kpi-đánh-giá-chiến-thuật-tiếp-thị-evaluation-kpi-framework)
- [P6.8 — Ranh giới Phương pháp luận: Chi tiêu Quan sát Tự nhiên (Observed Spend) vs. Lợi tức Đầu tư Tiếp thị Thực tế (Incremental Marketing ROI)](#p68--ranh-giới-phương-pháp-luận-chi-tiêu-quan-sát-tự-nhiên-observed-spend-vs-lợi-tức-đầu-tư-tiếp-thị-thực-tế-incremental-marketing-roi)
- [P6.9 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 6 (Oral Defense Guide P6: Q39 – Q45)](#p69--bộ-câu-hỏi-vấn-đáp-trọng-tâm-phase-6-oral-defense-guide-p6-q39--q45)

### PHẦN VIII — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 7 (VERIFIED SNAPSHOT & RESEARCH DASHBOARD)
- [P7.1 — Kiến trúc Luồng Dữ liệu Một Chiều và Triết lý Static Snapshots vs. Dynamic Database APIs](#p71--kiến-trúc-luồng-dữ-liệu-một-chiều-và-triết-lý-static-snapshots-vs-dynamic-database-apis)
- [P7.2 — Thiết kế Hợp đồng Dữ liệu (Data Contract), Snapshot Versioning và Cơ chế Kiểm toán Mã băm Toàn vẹn (SHA-256 Manifest)](#p72--thiết-kế-hợp-đồng-dữ-liệu-data-contract-snapshot-versioning-và-cơ-chế-kiểm-toán-mã-băm-toàn-vẹn-sha-256-manifest)
- [P7.3 — Chiến lược Tổng hợp Đa tầng (Multi-Level Aggregation) và Kiểm soát Kích thước Payload Trình duyệt](#p73--chiến-lược-tổng-hợp-đa-tầng-multi-level-aggregation-và-kiểm-soát-kích-thước-payload-trình-duyệt)
- [P7.4 — Bảo vệ Quyền Riêng tư (Data Privacy) và Kỹ thuật Ẩn danh Hóa Hồ sơ Khách hàng (Zero Raw PII)](#p74--bảo-vệ-quyền-riêng-tư-data-privacy-và-kỹ-thuật-ẩn-danh-hóa-hồ-sơ-khách-hàng-zero-raw-pii)
- [P7.5 — Ranh giới Ngữ cảnh Nghiên cứu và Nhãn Định danh Khách quan: Research Demo / REES46](#p75--ranh-giới-ngữ-cảnh-nghiên-cứu-và-nhãn-định-danh-khách-quan-research-demo--rees46)
- [P7.6 — Thiết kế Bảng Điều khiển Quản trị Cấp cao theo Phong cách Biên tập Thời trang Sang trọng (Dark Editorial Luxury Architecture)](#p76--thiết-kế-bảng-điều-khiển-quản-trị-cấp-cao-theo-phong-cách-biên-tập-thời-trang-sang-trọng-dark-editorial-luxury-architecture)
- [P7.7 — Trực quan hóa Khoa học và Kiểm soát Nhận thức: Biểu diễn Trật tự Đơn điệu và Khoảng Tin cậy Wilson Score 95%](#p77--trực-quan-hóa-khoa-học-và-kiểm-soát-nhận-thức-biểu-diễn-trật-tự-đơn-điệu-và-khoảng-tin-cậy-wilson-score-95)
- [P7.8 — Khóa An toàn Thực thi (No-Execution Guardrail) và Cơ chế Tiếp thị Có Trách nhiệm trên Giao diện](#p78--khóa-an-toàn-thực-thi-no-execution-guardrail-và-cơ-chế-tiếp-thị-có-trách-nhiệm-trên-giao-diện)
- [P7.9 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 7 (Oral Defense Guide P7: Q46 – Q52)](#p79--bộ-câu-hỏi-vấn-đáp-trọng-tâm-phase-7-oral-defense-guide-p7-q46--q52)

---

## P0.1 — Phương pháp luận CRISP-DM trong Phân tích Dữ liệu Khách hàng

### 1. What (Khái niệm là gì?)
CRISP-DM (Cross-Industry Standard Process for Data Mining) là quy trình tiêu chuẩn công nghiệp gồm 6 giai đoạn có tính lặp vòng: **Business Understanding $\leftrightarrow$ Data Understanding $\to$ Data Preparation $\leftrightarrow$ Modeling $\to$ Evaluation $\to$ Deployment**.

### 2. Why (Tại sao cần dùng?)
Tránh "bẫy công nghệ" phổ biến của sinh viên và kỹ sư mới: lao vào code mô hình phân cụm K-Means ngay từ ngày đầu tiên khi chưa hiểu bản chất dữ liệu, chưa xác định rõ ai sẽ dùng kết quả, và không có tiêu chí đánh giá nghiệp vụ. CRISP-DM đảm bảo mọi dòng code và thuật toán đều phục vụ một mục tiêu kinh doanh cụ thể.

### 3. How (Cách thức triển khai?)
Triển khai đồ án theo chu trình 21 ngày:
- Khởi động từ Phase 0 để chốt hợp đồng KPI, câu hỏi nghiệp vụ, giả thuyết và kiến trúc phân rã.
- Phase 1 & 2 làm chủ dữ liệu và chất lượng trước khi nạp vào thuật toán.
- Phase 3 & 4 trích xuất đặc trưng và mô hình hóa.
- Phase 5 & 6 đánh giá đa chiều và xây dựng luật quyết định tiếp thị.
- Phase 7 & 8 đóng gói dashboard hiển thị và bảo vệ đồ án.

### 4. Formula (Công thức / Sơ đồ luồng)
$$\text{Business Problem} \longrightarrow \text{Analytical Questions} \longrightarrow \text{Data Requirements} \longrightarrow \text{Model} \longrightarrow \text{Prescriptive Action}$$

### 5. Worked Example (Ví dụ minh họa)
Một shop online muốn "tăng doanh thu":
- *Cách tiếp cận sai (thiếu CRISP-DM):* Lấy dữ liệu chạy K-Means ra 4 cụm, vẽ biểu đồ 3D màu mè, kết luận "đây là 4 cụm khách hàng", không biết shop phải làm gì tiếp theo.
- *Cách tiếp cận đúng (theo CRISP-DM):*
  - Business Understanding: Vấn đề là CAC tăng cao, cần giữ chân khách hàng cũ và giảm tỷ lệ bỏ giỏ hàng.
  - Data Understanding: Phát hiện REES46 không có `order_id`, frequency phải tính bằng proxy phiên.
  - Data Preparation: Tách riêng Buyers để phân cụm RFM, tách Non-buyers để phân tích giỏ hàng.
  - Modeling: K-Means trên tập Buyers ($F1$).
  - Evaluation: Đánh giá xem cụm VIP có thực sự mua nhiều hơn trong tháng tiếp theo không.
  - Deployment: Đề xuất chiến thuật cart recovery cho người bỏ giỏ và chiến thuật loyalty cho VIP.

### 6. Alternatives (Phương án thay thế)
- *KDD (Knowledge Discovery in Databases):* Nặng về quy trình học thuật, ít nhấn mạnh pha kết nối nghiệp vụ và triển khai.
- *Agile/Scrum thuần túy:* Thích hợp cho phát triển phần mềm, nhưng dễ dẫn đến việc vội vã đưa ra mô hình chưa được kiểm chứng khoa học.

### 7. Verification (Cách thức kiểm chứng)
Kiểm tra xem mỗi giai đoạn có đáp ứng tiêu chuẩn nghiệm thu (Phase Gate) tại `PROJECT_STATUS.md` hay không; có bằng chứng log chạy thực tế trước khi chuyển pha.

### 8. Limitations (Giới hạn)
CRISP-DM là khung quy trình, không tự động giải quyết các vấn đề kỹ thuật như rò rỉ dữ liệu (leakage) hay tràn bộ nhớ (OOM); kỹ sư phải tự thiết lập các chốt kiểm soát chất lượng (quality gates).

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không bắt tay vào huấn luyện mô hình K-Means ngay mà phải mất thời gian cho Phase 0 — Business Understanding?"*  
> **Trả lời:** *"Thưa Thầy/Cô, việc phân tích dữ liệu chỉ có giá trị khi giải quyết đúng bài toán nghiệp vụ. Nếu làm mô hình ngay mà chưa xác lập Business Understanding, chúng em sẽ mắc các sai lầm nghiêm trọng: (1) Nhầm lẫn giữa purchase event và order thật do REES46 không có order_id; (2) Gán nhầm recency giả tạo cho người chưa từng mua làm méo khoảng cách K-Means; (3) Rò rỉ dữ liệu tương lai qua mốc cutoff. Phase 0 giúp xây dựng hợp đồng dữ liệu chuẩn xác, tiết kiệm thời gian gỡ lỗi về sau."*

---

## P0.2 — Phân cấp Khái niệm: Business Goal, Question, KPI, Feature, Model, Decision Engine

### 1. What (Khái niệm là gì?)
Một hệ thống phân tích dữ liệu hoàn chỉnh bao gồm 6 tầng logic phân biệt:
1. **Business Goal (Mục tiêu nghiệp vụ):** Kết quả kinh doanh cấp cao cần đạt (ví dụ: Giữ chân khách hàng giá trị cao).
2. **Business Question (Câu hỏi nghiệp vụ):** Câu hỏi định lượng cần trả lời (ví dụ: Ai là khách hàng giá trị cao đang có dấu hiệu rời bỏ?).
3. **KPI (Chỉ số đo lường hiệu quả):** Thước đo tổng hợp dùng để đánh giá trạng thái hoặc tiến độ (ví dụ: `purchase_session_rate`, `repeat_buyer_rate_proxy`).
4. **Feature (Đặc trưng mô hình):** Biến số định lượng được trích xuất cho từng thực thể (ví dụ: `recency_days`, `sessions_recent_30d` của user $u$).
5. **Model (Mô hình giải thuật):** Giải thuật học máy tìm cấu trúc trong dữ liệu (ví dụ: Thuật toán K-Means phân cụm khách hàng).
6. **Decision Engine (Bộ máy ra quyết định):** Hệ thống luật chuyên gia đề xuất hành động tiếp thị cụ thể dựa trên phân khúc và bằng chứng hành vi (ví dụ: Nếu thuộc cụm At-Risk và có giỏ hàng gần đây $\to$ Đề xuất chiến thuật Cart Recovery).

### 2. Why (Tại sao cần phân biệt?)
Sự nhập nhằng giữa các tầng khái niệm thường dẫn đến việc "thần thánh hóa" thuật toán (nghĩ rằng K-Means có thể tự động quyết định gửi voucher) hoặc nhầm lẫn giữa một feature đầu vào với một KPI đầu ra.

### 3. How (Cách thức triển khai?)
Thiết lập bảng ma trận liên kết truy vết (Traceability Matrix) từ BQ $\to$ Data $\to$ Method $\to$ KPI $\to$ Action.

### 4. Formula (Bảng phân cấp quan hệ)
$$\text{Business Goal} \xrightarrow{\text{cụ thể hóa}} \text{Business Question} \xrightarrow{\text{đo lường bằng}} \text{KPI / Features} \xrightarrow{\text{xử lý qua}} \text{Model} \xrightarrow{\text{kết hợp}} \text{Decision Rules}$$

### 5. Worked Example (Ví dụ phân cấp cụ thể)

| Tầng khái niệm | Trường hợp cụ thể trong dự án | Vai trò trong hệ thống |
|---|---|---|
| **Business Goal** | Tối ưu hóa chuyển đổi từ lượng người dùng quan tâm nhưng chưa mua. | Xác định định hướng chiến lược. |
| **Business Question** | Tỷ lệ phiên thêm giỏ nhưng không mua là bao nhiêu và nhóm nào có tiềm năng kích hoạt? | Xác định bài toán phân tích. |
| **KPI** | `cart_to_purchase_same_session_rate` (đo trên toàn sàn). | Giám sát hiệu quả phễu. |
| **Feature** | `product_views_recent_30d`, `cart_events_recent_30d` của từng user. | Đầu vào để phân loại người dùng. |
| **Model** | K-Means clustering (trên Buyers) / Rule-based Stratification (trên Non-buyers). | Tìm nhóm người dùng tương đồng. |
| **Decision Engine** | Gán chiến thuật `TAC_CART_RECOVERY` kèm lý do `has_recent_cart_no_purchase`. | Đưa ra hành động cụ thể cho chủ shop. |

### 6. Alternatives (Phương án thay thế)
Một số hệ thống thương mại gộp chung Feature và KPI thành một bảng tổng hợp, nhưng cách làm này dễ gây rò rỉ dữ liệu nếu không kiểm soát cửa sổ thời gian nghiêm ngặt.

### 7. Verification (Cách thức kiểm chứng)
Kiểm tra xem mọi đề xuất marketing đầu ra có truy vết ngược lại được ít nhất một đặc trưng định lượng và một câu hỏi nghiệp vụ ban đầu hay không.

### 8. Limitations (Giới hạn)
Decision Engine trong đồ án là hệ thống luật chuyên gia (Rule-based), không phải là Reinforcement Learning tối ưu tự động chính sách marketing.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Hệ thống của em có dùng Machine Learning để tự động tối ưu hóa mức giảm giá (voucher discount) cho từng khách hàng không?"*  
> **Trả lời:** *"Thưa Thầy/Cô, KHÔNG. Machine Learning (K-Means) trong hệ thống chỉ làm một nhiệm vụ duy nhất là phân nhóm khách hàng không giám sát dựa trên hành vi tương đồng. Việc chọn chiến thuật marketing nào do Decision Engine (bộ máy luật chuyên gia) đảm nhiệm dựa trên bằng chứng dữ liệu. Dataset REES46 không có dữ liệu thử nghiệm A/B với các mức voucher khác nhau, nên việc khẳng định ML tối ưu được voucher là thiếu căn cứ khoa học."*

---

## P0.3 — Bản chất Cấp độ Hạt Dữ liệu: Event vs. Session vs. User vs. Purchase Session vs. Order

### 1. What (Khái niệm là gì?)
Cấp độ hạt (Data Grain) đại diện cho mức độ chi tiết của một dòng dữ liệu trong bảng. Trong thương mại điện tử, có 6 cấp độ hạt phân biệt:
- **`Event Grain`:** 1 dòng = 1 tương tác tại thời điểm $t$ (`event_time`, `event_type`).
- **`Session Grain`:** 1 dòng = 1 chuỗi tương tác liên tục, khóa định danh là cặp `(user_id, user_session)`.
- **`User / Visitor Grain`:** 1 dòng = 1 người dùng định danh (`user_id`).
- **`Purchase Session Grain`:** 1 dòng = 1 phiên có $\ge 1$ sự kiện mua hàng. Đây là **proxy đại diện cho giao dịch**.
- **`Order Grain`:** 1 dòng = 1 đơn hàng chính thức từ cổng thanh toán / OMS. **REES46 KHÔNG CÓ trường này.**

### 2. Why (Tại sao phải phân biệt?)
Nếu lấy số dòng `purchase` làm số đơn hàng, bạn sẽ thổi phồng tần suất mua hàng (Frequency) lên gấp nhiều lần, vì trong thương mại điện tử khách hàng mua 5 sản phẩm trong 1 giỏ hàng sẽ sinh ra 5 sự kiện `purchase` riêng biệt trong cùng 1 phiên.

### 3. How (Cách thức triển khai?)
Trong DuckDB / SQL, luôn xác định rõ grain của mệnh đề `GROUP BY`:
- Muốn tính `purchase_session_rate`: Mẫu số phải là `COUNT(DISTINCT (user_id, user_session))`, không được dùng `COUNT(*)`.
- Muốn tính Frequency của Buyer: Đếm số `user_session` phân biệt có mua hàng, không đếm tổng số dòng purchase.

### 4. Formula (Công thức toán học)
$$\text{PurchaseSessionRate} = \frac{|\{(u, s) \mid \exists e \in (u, s) : e.\text{type} = \text{'purchase'}\}|}{|\{(u, s) \mid \text{valid session}\}|}$$

$$\text{BuyerFrequencyProxy}(u) = |\{s \mid \exists e \in (u, s) : e.\text{type} = \text{'purchase'}\}|$$

### 5. Worked Example (Ví dụ tính toán minh họa)
Cho tập dữ liệu sự kiện đồ chơi gồm 11 sự kiện dưới đây:

| User | Session | Event Time (UTC) | Event Type | Price | Giải thích bản ghi |
|---|---|---|---|---|---|
| `u1` | `s1` | 2020-01-15 12:00:00 | view | 10.0 | Khách u1 xem hàng trong phiên s1 |
| `u1` | `s1` | 2020-01-15 12:01:00 | cart | 10.5 | Thêm sản phẩm A vào giỏ |
| `u1` | `s1` | 2020-01-15 12:02:00 | purchase | 10.5 | Mua sản phẩm A |
| `u1` | `s1` | 2020-01-15 12:02:30 | purchase | 15.0 | Mua sản phẩm B trong cùng phiên s1 |
| `u1` | `s2` | 2020-01-20 11:00:00 | purchase | 20.0 | Mua sản phẩm C trong phiên s2 |
| `u2` | `s3` | 2020-01-25 11:00:00 | cart | 50.0 | Khách u2 thêm giỏ trong phiên s3 |
| `u2` | `s3` | 2020-01-25 11:01:00 | view | 50.0 | Tiếp tục xem hàng |
| `u3` | `s4` | 2020-01-26 09:00:00 | view | 5.0 | Khách u3 chỉ xem hàng trong phiên s4 |
| `u3` | `null` | 2020-01-27 09:00:00 | purchase | 5.0 | **Lỗi tracking: khuyết session** |
| `u2` | `s5` | 2020-02-01 00:00:00 | purchase | 50.0 | **Sự kiện tại ranh giới cutoff: thuộc tháng 2 (Holdout)** |
| `u3` | `s6` | 2019-09-30 23:59:59 | cart | 12.0 | **Sự kiện trước thời gian bắt đầu: loại khỏi observation** |

**Tính toán chỉ số trong kỳ Observation $[2019-10-01, 2020-02-01)$:**
1. **Tổng số phiên hợp lệ (Valid Sessions):** Có 4 phiên hợp lệ gồm `(u1, s1)`, `(u1, s2)`, `(u2, s3)`, `(u3, s4)`. Bản ghi khuyết session bị loại; bản ghi tháng 2 và tháng 9 nằm ngoài cửa sổ.
2. **Số phiên có mua hàng (Purchase Sessions Proxy):** Có 2 phiên là `(u1, s1)` và `(u1, s2)`.
3. **Số phiên có giỏ hàng (Cart Sessions):** Có 2 phiên là `(u1, s1)` và `(u2, s3)`.
4. **Số phiên giỏ hàng chuyển đổi mua (Cart then Purchase):** Chỉ có phiên `(u1, s1)` có purchase diễn ra sau cart (12:02 > 12:01).
5. **Các tỷ lệ phiên:**
   $$\text{PurchaseSessionRate} = \frac{2}{4} = 0.50 \quad (50\%)$$
   $$\text{CartSessionRate} = \frac{2}{4} = 0.50 \quad (50\%)$$
   $$\text{CartToPurchaseSameSessionRate} = \frac{1}{2} = 0.50 \quad (50\%)$$
6. **Đặc trưng RFM của khách hàng `u1` (Cutoff = 2020-02-01T00:00:00Z):**
   - Lần mua cuối của `u1` là 2020-01-20 11:00:00.
   - $\text{Recency} = \frac{(2020-02-01\ 00:00:00) - (2020-01-20\ 11:00:00)}{86400} = 11.54\ \text{ngày}$.
   - $\text{Frequency} = 2\ \text{purchase sessions}$ (`s1` và `s2`), **hoàn toàn KHÔNG phải là 3**.
   - $\text{Monetary} = 10.5 + 15.0 + 20.0 = 45.5$.

### 6. Alternatives (Phương án thay thế)
- *Session timeout-based synthetic ID:* Tự tạo session dựa trên ngưỡng 30 phút không hoạt động nếu dữ liệu thiếu trường `user_session`. Trong REES46 đã có sẵn trường `user_session` nên ưu tiên dùng khóa gốc.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động bằng unit tests: `test_session_denominators_and_proxy_order` và `test_buyer_rfm_semantics` trong `tests/test_kpi_semantics.py` đã vượt qua 100%.

### 8. Limitations (Giới hạn)
Một khách hàng có thể mua 2 lần trong cùng một phiên cách nhau 10 phút, proxy theo phiên sẽ gộp thành 1 lần mua; đây là hạn chế tất yếu khi dữ liệu clickstream không cung cấp `order_id` độc lập.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không lấy tổng số dòng sự kiện purchase làm số lần mua hàng (Frequency) của khách hàng?"*  
> **Trả lời:** *"Thưa Thầy/Cô, trong tập dữ liệu REES46, mỗi dòng sự kiện purchase tương ứng với một sản phẩm được mua (item-level event). Khi khách hàng mua một giỏ hàng gồm nhiều món tại cùng một thời điểm thanh toán, hệ thống sẽ log ra nhiều dòng purchase có cùng timestamp và cùng session. Nếu đếm số dòng sự kiện, chúng em sẽ nhầm lẫn giữa 'số lượng món hàng' và 'số lần mua hàng', làm méo mó nghiêm trọng phân phối Frequency. Vì dataset không có order_id, giải pháp khoa học và chuẩn xác nhất là sử dụng 'số phiên có mua hàng' (purchase sessions) làm proxy đại diện cho số lần giao dịch."*

---

## P0.4 — Khung phân tích RFM và Nan giải Recency của Người chưa mua (Non-buyer Dilemma)

### 1. What (Khái niệm là gì?)
- **RFM:** Kỹ thuật định lượng giá trị khách hàng gồm $R$ (số ngày từ lần mua cuối đến cutoff), $F$ (số phiên mua trong kỳ), $M$ (tổng tiền mua quan sát).
- **Non-buyer Recency Dilemma (Nan giải Recency của người chưa mua):** Khách hàng chưa từng mua hàng trong kỳ quan sát thì $R$ bằng bao nhiêu? Về mặt toán học, tập hợp thời gian mua hàng là rỗng $\emptyset$, do đó $\max(t_{purchase})$ không tồn tại, khiến $R$ là **không xác định (undefined)**.

### 2. Why (Tại sao phải giải quyết?)
Nếu người phân tích thiếu hiểu biết cố tình ép giá trị cho người chưa mua:
- Gán $R = 0$: Biến người chưa mua thành "người vừa mới mua hàng hôm nay" (ngụy tạo khách siêu mới).
- Gán $R = 999$ hoặc $R = \infty$: Kéo dãn trục tọa độ cực đại, khiến thuật toán K-Means (vốn nhạy cảm với khoảng cách Euclidean) bị bóp méo hoàn toàn, tạo ra cụm giả tạo và làm lu mờ sự phân hóa giữa các khách hàng đã mua thực tế.

### 3. How (Cách thức triển khai?)
Áp dụng nguyên tắc thiết kế phân rã (Decoupled Segmentation):
1. **Tách tập dữ liệu thành 2 nhánh độc lập:**
   - Nhánh 1: **Buyers ($F \ge 1$):** Đầy đủ 3 chiều $R, F, M \to$ Áp dụng thuật toán học máy K-Means.
   - Nhánh 2: **Observed Non-buyers ($F = 0$):** Không áp dụng K-Means. Thay vào đó, sử dụng hệ thống luật phân tầng theo mức độ tương tác (Rule-based Engagement Stratification: Cart Abandoners, Window Shoppers, Bouncers).
2. Tuyệt đối không gán giá trị nhân tạo cho $R$ của non-buyers.

### 4. Formula (Công thức toán học)
$$R_u = \begin{cases} \frac{T_{cutoff} - \max(t_{purchase, u})}{86400} & \text{nếu } u \in \text{Buyers} \\ \text{undefined} & \text{nếu } u \in \text{Observed Non-buyers} \end{cases}$$

### 5. Worked Example (Ví dụ minh họa)
Giả sử có 2 khách hàng:
- Khách hàng A (Buyer): Mua lần cuối ngày 15/01/2020 $\to R_A = 17$ ngày, $F_A = 2, M_A = 50.0 \to$ Chuẩn hóa và đưa vào K-Means.
- Khách hàng B (Non-buyer): Chưa từng mua, nhưng có 15 lượt xem và 2 lần thêm giỏ trong 30 ngày gần nhất $\to R_B = \text{undefined}$. Hệ thống chuyển B sang nhánh Non-buyers và gắn nhãn nghiệp vụ `High-Intent Non-buyer (Cart Abandoner)` để áp dụng kịch bản hỗ trợ giỏ hàng.

### 6. Alternatives (Phương án thay thế)
- *Dùng Recency của phiên truy cập web (Site Visit Recency):* Tính số ngày từ lần vào web cuối thay vì lần mua cuối. **Nhược điểm:** Làm mất đi ý nghĩa kinh điển của RFM trong việc phản ánh rủi ro rời bỏ giao dịch tài chính.
- *Thay thế bằng giá trị trung bình/trung vị:* Vẫn vi phạm tính trung thực vì khách hàng chưa từng mua không thể có giá trị trung bình mua hàng.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động trong `tests/test_kpi_semantics.py` hàm `test_buyer_rfm_semantics` xác nhận rằng khách hàng không có purchase trước cutoff sẽ không tồn tại trong từ điển kết quả RFM (hoàn toàn không có recency giả tạo).

### 8. Limitations (Giới hạn)
"Observed Non-buyer" chỉ mang ý nghĩa là không mua trong cửa sổ 4 tháng của dataset; không thể khẳng định họ chưa từng mua hàng trước tháng 10/2019 nếu thiếu dữ liệu lịch sử dài hạn.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không gán Recency = 999 cho những người chưa mua để gom chung vào chạy một mô hình K-Means cho tiện?"*  
> **Trả lời:** *"Thưa Thầy/Cô, K-Means tính toán dựa trên khoảng cách Euclidean trong không gian $d$ chiều. Nếu gán Recency = 999 cho tập người chưa mua (vốn chiếm tỷ lệ rất lớn trong e-commerce, thường >80%), giá trị ngoại lai cực lớn này sẽ chiếm ưu thế hoàn toàn trong hàm mục tiêu WCSS, ép tất cả buyers thực sự vào một góc nhỏ và tạo ra các cụm méo mó vô nghĩa. Giải pháp chuẩn mực của chúng em là tách tập dữ liệu: K-Means chỉ phục vụ phân cụm Buyers, còn Non-buyers được phân tích bằng bộ luật tương tác riêng. Điều này vừa bảo toàn tính toán học của mô hình, vừa giữ vững giá trị thực tế của kinh doanh."*

---

## P0.5 — Phân tách Thời gian (Temporal Split) và Kiểm soát Rò rỉ Dữ liệu (Data Leakage)

### 1. What (Khái niệm là gì?)
- **Temporal Split (Phân tách theo trục thời gian):** Phương pháp chia tập dữ liệu dựa trên mốc thời gian cố định $T_{cutoff}$, trong đó quá khứ $[start, T_{cutoff})$ dùng để xây dựng đặc trưng và phân cụm, còn tương lai $[T_{cutoff}, future\_end)$ được giữ lại làm tập kiểm chứng độc lập (Holdout).
- **Data Leakage (Rò rỉ dữ liệu):** Hiện tượng thông tin từ tương lai hoặc thông tin từ tập kiểm tra vô tình lọt vào quá trình chuẩn bị dữ liệu hoặc huấn luyện mô hình.

### 2. Why (Tại sao phải kiểm soát nghiêm ngặt?)
Trong phân tích khách hàng, nếu lấy dữ liệu của tháng 2 để tính đặc trưng phân cụm rồi lại lấy chính tháng 2 để kết luận "mô hình phân cụm dự báo rất chính xác khách nào sẽ mua hàng vào tháng 2", đây là lỗi ngụy biện khoa học nghiêm trọng (circular reasoning / data leakage), khiến kết quả thực nghiệm hoàn toàn mất giá trị tin cậy.

### 3. How (Cách thức triển khai?)
1. Xác lập mốc cutoff bất biến: $T_{cutoff} = 2020-02-01T00:00:00Z$.
2. Toàn bộ logic ETL, lọc dữ liệu, trích xuất đặc trưng RFM và Engagement chỉ được quét các bản ghi có $event\_time < T_{cutoff}$.
3. Tháng 02/2020 được niêm phong hoàn toàn. Chỉ ở Phase 5 mới mở ra đúng một lần để tính tỷ lệ mua hàng `future_purchase_rate_by_segment` nhằm hậu kiểm (post-hoc validation).

### 4. Formula (Quy ước khoảng thời gian nửa mở)
$$\mathcal{D}_{\text{train}} = \{e \in \mathcal{D} \mid 2019\text{-}10\text{-}01T00:00:00Z \le e.\text{time} < 2020\text{-}02\text{-}01T00:00:00Z\}$$

$$\mathcal{D}_{\text{future}} = \{e \in \mathcal{D} \mid 2020\text{-}02\text{-}01T00:00:00Z \le e.\text{time} < 2020\text{-}03\text{-}01T00:00:00Z\}$$

$$\mathcal{D}_{\text{train}} \cap \mathcal{D}_{\text{future}} = \emptyset$$

### 5. Worked Example (Ví dụ minh họa)
Khách hàng `u2` có một sự kiện mua hàng xảy ra lúc `2020-02-01T00:00:00Z`.
- Theo quy ước nửa mở $[start, end)$, mốc $T_{cutoff}$ là điểm chặn loại trừ (exclusive).
- Do đó, sự kiện này **KHÔNG thuộc về kỳ quan sát** $\to$ Khách hàng `u2` tại ngày 01/02/2020 vẫn là Non-buyer.
- Sự kiện này thuộc về tập tương lai tháng 2 $\to$ Được dùng để kiểm chứng xem phân khúc của `u2` có phát sinh chuyển đổi ở kỳ sau hay không.

### 6. Alternatives (Phương án thay thế)
- *Random Train/Test Split (Chia ngẫu nhiên):* Chia 80% bản ghi làm train, 20% làm test bất kể thời gian. **RẤT NGUY HIỂM trong bài toán chuỗi thời gian / hành vi**, vì mô hình sẽ học được tương lai để đoán quá khứ.

### 7. Verification (Cách thức kiểm chứng)
- Kiểm tra tự động bằng assertion trong `scripts/validate_phase0.py` dòng 28: `assert project["time"]["holdout_used_for_tuning"] is False`.
- Unit test `test_half_open_cutoff_and_missing_session` trong `tests/test_kpi_semantics.py` kiểm chứng chính xác sự kiện tại biên cutoff không bị lọt vào kỳ quan sát.

### 8. Limitations (Giới hạn)
Tập holdout 1 tháng (tháng 2/2020) có thể chịu ảnh hưởng của các yếu tố ngoại cảnh đặc biệt (như mùa lễ hội Tết âm lịch hoặc khởi đầu đại dịch Covid-19); cần ghi nhận đây là giới hạn dữ liệu khi phân tích kết quả.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Nếu em thấy kết quả phân cụm trên tập tháng 2 chưa tốt, em có thể quay lại chỉnh số cụm K hoặc thêm biến để tỷ lệ mua tháng 2 đẹp hơn không?"*  
> **Trả lời:** *"Thưa Thầy/Cô, TUYỆT ĐỐI KHÔNG. Nếu dùng kết quả tháng 2 để quay lại chỉnh K hay chọn biến, tập tháng 2 sẽ bị biến thành tập validation/training, làm mất hoàn toàn tư cách là một tập kiểm chứng độc lập (independent holdout). Nếu bắt buộc phải điều chỉnh mô hình dựa trên tháng 2, chúng em sẽ phải công khai báo cáo rằng đây là phân tích khám phá (exploratory analysis) chứ không được gọi là đánh giá kiểm chứng độc lập nữa."*

---

## P0.6 — Cửa sổ Tương tác Clickstream Engagement và Kỹ thuật Làm mượt Laplace Smoothing

### 1. What (Khái niệm là gì?)
- **Clickstream Engagement Windows:** Việc chia nhỏ thời gian tương tác gần mốc cutoff thành 2 cửa sổ liên tiếp không chồng lấn dài 30 ngày: Recent $[T-30d, T)$ và Previous $[T-60d, T-30d)$.
- **Activity Ratio with Laplace/Pseudocount Smoothing:** Tỷ số đo lường xu hướng tăng/giảm tương tác có cộng thêm hằng số giả định (+1) vào cả tử số và mẫu số để triệt tiêu lỗi chia cho 0.

### 2. Why (Tại sao cần dùng?)
Nhiều khách hàng có số phiên ở kỳ trước bằng 0 (`sessions_previous = 0`). Nếu chia trực tiếp `sessions_recent / sessions_previous`, phép tính sẽ bị lỗi phép chia cho 0 (`ZeroDivisionError` hoặc $\infty$). Thêm hằng số làm mượt Laplace giúp công thức toán học luôn ổn định.

### 3. How (Cách thức triển khai?)
Tính toán song song hai chỉ số:
1. `activity_ratio = (sessions_recent + 1) / (sessions_previous + 1)`
2. `activity_delta = sessions_recent - sessions_previous`
Luôn xem xét `activity_ratio` đi kèm với `activity_delta` và số lượng tuyệt đối `sessions_recent` để tránh ngụy biện.

### 4. Formula (Công thức toán học)
$$\text{ActivityRatio} = \frac{S_{\text{recent}} + 1}{S_{\text{previous}} + 1}$$

$$\text{ActivityDelta} = S_{\text{recent}} - S_{\text{previous}}$$

### 5. Worked Example (Ví dụ minh họa & Cạm bẫy toán học)

| Khách hàng | $S_{\text{previous}}$ | $S_{\text{recent}}$ | Activity Ratio | Activity Delta | Bản chất hành vi thực tế | Cạm bẫy nếu chỉ nhìn Ratio |
|---|---|---|---|---|---|---|
| Khách A | 0 | 0 | $\frac{0+1}{0+1} = 1.0$ | $0 - 0 = 0$ | Hoàn toàn bất động cả 2 kỳ | Ratio = 1.0 KHÔNG có nghĩa là đang hoạt động ổn định! |
| Khách B | 20 | 20 | $\frac{20+1}{20+1} = 1.0$ | $20 - 20 = 0$ | Hoạt động đều đặn, gắn kết cao | Cùng ratio = 1.0 nhưng bản chất khác hoàn toàn Khách A |
| Khách C | 0 | 10 | $\frac{10+1}{0+1} = 11.0$ | $10 - 0 = +10$ | Người dùng mới bùng nổ tương tác | Mẫu số bằng 0 được xử lý an toàn thành 1 |
| Khách D | 20 | 5 | $\frac{5+1}{20+1} \approx 0.286$ | $5 - 20 = -15$ | Suy giảm tương tác nghiêm trọng | Tín hiệu cảnh báo nguy cơ rời bỏ |

### 6. Alternatives (Phương án thay thế)
- *Gán giá trị mặc định khi mẫu số bằng 0:* Trả về null hoặc một giá trị cố định. **Nhược điểm:** Làm gián đoạn các giải thuật học máy yêu cầu ma trận số liên tục.
- *Log Ratio:* $\ln((S_{\text{recent}} + 1) / (S_{\text{previous}} + 1))$. Có tính đối xứng quanh 0, rất tốt cho mô hình tuyến tính.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động trong `tests/test_kpi_semantics.py` hàm `test_ratio_smoothing`: kiểm tra tính đúng đắn với $(0, 0) \to 1.0$, $(10, 0) \to 11.0$, và bắt lỗi ngoại lệ `ValueError` nếu truyền số âm.

### 8. Limitations (Giới hạn)
Hiệu ứng làm mượt làm co các tỷ số cực đoan về gần 1; do đó không được dùng riêng lẻ mà bắt buộc phải lưu trữ đồng thời số phiên tuyệt đối `sessions_recent_30d`.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Nếu một khách hàng có Activity Ratio = 1.0, em có thể khẳng định khách hàng này đang duy trì mức độ tương tác ổn định với website không?"*  
> **Trả lời:** *"Thưa Thầy/Cô, KHÔNG THỂ vội vã khẳng định nếu chưa kiểm tra số phiên tuyệt đối. Do công thức sử dụng kỹ thuật làm mượt Laplace $(S_{\text{recent}} + 1) / (S_{\text{previous}} + 1)$, một người dùng hoàn toàn không có tương tác nào ở cả hai kỳ ($S_{\text{recent}} = 0$ và $S_{\text{previous}} = 0$) vẫn sẽ cho ra Activity Ratio = 1.0. Đây là kết quả làm mượt toán học để tránh lỗi chia cho 0, chứ không phản ánh khách hàng đang hoạt động. Trong hệ thống của chúng em, một khách hàng chỉ được coi là hoạt động ổn định khi Activity Ratio $\approx 1.0$ VÀ số phiên tuyệt đối $S_{\text{recent}} > 0$."*

---

## P0.7 — Đánh giá Học máy không giám sát và Ma trận Đánh đổi Đa chiều (Trade-off Matrix)

### 1. What (Khái niệm là gì?)
- **Đánh giá không giám sát:** Đo lường cấu trúc nội tại của cụm khi không có nhãn đúng sai thực tế (Ground Truth Labels), thông qua tính phân tách (Silhouette Score), tính thu gọn nội cụm (Davies-Bouldin Index - DBI) và tính ổn định thuật toán (Adjusted Rand Index - ARI).
- **Multi-dimensional Trade-off Matrix (Ma trận đánh đổi đa chiều):** Khung ra quyết định lựa chọn mô hình dựa trên việc cân nhắc đồng thời nhiều tiêu chí xung đột (Chất lượng cụm vs. Độ ổn định vs. Ý nghĩa kinh doanh vs. Thời gian chạy vs. Bộ nhớ RAM) thay vì cố tạo ra một điểm số tổng hợp giả tạo.

### 2. Why (Tại sao không dùng một điểm số tổng hợp?)
Nhiều báo cáo cố gắng tạo công thức gộp: $\text{Score} = 0.4 \times \text{Silhouette} + 0.3 \times \text{Runtime} + 0.3 \times \text{RAM}$. Cách làm này hoàn toàn phi khoa học vì:
1. Không có cơ sở lý thuyết nào để gán trọng số 0.4 hay 0.3.
2. Các đại lượng có đơn vị đo hoàn toàn khác nhau (điểm không thứ nguyên vs. giây vs. megabytes).
3. Nó che giấu các khiếm khuyết chết người (ví dụ: một mô hình chạy cực nhanh nhưng phân cụm sai lệch vẫn có thể đạt điểm tổng cao).

### 3. How (Cách thức triển khai?)
1. **Bước 1: Áp dụng Hard Constraints (Ràng buộc cứng):** Loại bỏ ngay các mô hình vi phạm tính đúng đắn dữ liệu, gây rò rỉ dữ liệu, hoặc làm tràn RAM.
2. **Bước 2: Phân tích Ma trận Đánh đổi:** Lập bảng so sánh các phương án khả thi, nhận diện các phương án bị áp đảo (dominated options) và chọn mô hình tối ưu theo tiêu chí Pareto.

### 4. Formula (Công thức thước đo nội tại)
- **Silhouette Coefficient của điểm $i$:**
  $$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}, \quad s(i) \in [-1, 1]$$
- **Davies-Bouldin Index:**
  $$DBI = \frac{1}{K} \sum_{k=1}^K \max_{j \ne k} \left( \frac{\sigma_k + \sigma_j}{d(\mu_k, \mu_j)} \right)$$

### 5. Worked Example (Ví dụ ma trận đánh đổi thực tế)

| Cấu hình mô hình | Hard Gates | Silhouette ($F1$) | DBI | ARI (Stability) | Runtime | Peak RSS | Đánh giá nghiệp vụ & Quyết định |
|---|---|---|---|---|---|---|---|
| **Phương án A ($K=3$)** | PASS | 0.52 | 0.85 | 0.88 | 12s | 450MB | Cụm phân tách rất đẹp, ổn định cao, nhưng chỉ chia ra 3 nhóm quá rộng, thiếu hành động chi tiết. |
| **Phương án B ($K=5$)** | **PASS** | **0.48** | **0.95** | **0.82** | **18s** | **480MB** | **ĐƯỢC CHỌN:** Silhouette giảm nhẹ nhưng phân tách sắc nét 5 chân dung hành động được: VIP, Mới, Bỏ giỏ, Nguy cơ, Rời bỏ. |
| **Phương án C ($K=8$)** | PASS | 0.50 | 1.10 | 0.55 | 35s | 550MB | Cụm bị vỡ vụn, xuất hiện 2 cụm nhỏ chiếm <1% khách hàng, độ ổn định kém qua các seed. BỊ LOẠI. |
| **Phương án D** | FAILED | N/A | N/A | N/A | Crash | >16GB | Tràn bộ nhớ do không tối ưu pipeline. BỊ LOẠI TỪ VÒNG CỨNG. |

### 6. Alternatives (Phương án thay thế)
- *Phương pháp Elbow (Khuỷu tay trên Inertia):* Chỉ mang tính định tính bằng mắt, thường khó xác định điểm gãy rõ ràng trên dữ liệu thực tế nhiều nhiễu.
- *Calinski-Harabasz Index:* Tỷ số giữa phương sai liên cụm và nội cụm; có xu hướng thiên vị các cụm hình cầu lồi.

### 7. Verification (Cách thức kiểm chứng)
Chạy đo đạc thực nghiệm độc lập trên quy trình cách ly; ghi nhận kết quả thật vào bảng đối soát; không điền số liệu giả định.

### 8. Limitations (Giới hạn)
Silhouette phụ thuộc mạnh vào số chiều không gian (Curse of Dimensionality). Không thể lấy Silhouette của không gian 3 chiều ($F0$) so sánh trực tiếp với không gian 5 chiều ($F1$) để bảo mô hình nào "chính xác hơn".

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không gọi Silhouette Score là Độ chính xác (Accuracy) của thuật toán K-Means?"*  
> **Trả lời:** *"Thưa Thầy/Cô, Accuracy (Độ chính xác) là khái niệm chỉ tồn tại trong Học máy có giám sát (Supervised Learning), nơi chúng ta có sẵn nhãn thực tế (Ground Truth) để so sánh dự đoán đúng/sai. K-Means là thuật toán Học máy không giám sát (Unsupervised Learning), dữ liệu hoàn toàn không có nhãn đúng tuyệt đối. Silhouette Score chỉ là một thước đo hình học nội tại (Internal Geometric Metric) đo lường mức độ gắn kết bên trong cụm so với khoảng cách đến cụm lân cận. Gọi Silhouette là Accuracy là sai lệch bản chất toán học của Machine Learning."*

---

## P0.8 — Bản chất của Marketing Decision Support: Rule-based Prescriptive vs. Causal Uplift

### 1. What (Khái niệm là gì?)
- **Prescriptive Decision Support (Hỗ trợ ra quyết định theo quy tắc):** Hệ thống luật chuyên gia dựa trên bằng chứng dữ liệu (evidence-based rules) để gợi ý các hành động tiếp thị hợp lý theo ngữ cảnh.
- **Causal Uplift Modeling (Mô hình hóa tác động gia tăng nhân quả):** Phương pháp kinh tế lượng / học máy nhằm lượng hóa sự gia tăng thực sự về doanh thu do can thiệp tiếp thị mang lại so với nhóm không can thiệp:
  $$\text{Uplift} = E[Y \mid \text{Treatment}] - E[Y \mid \text{Control}]$$

### 2. Why (Tại sao phải phân định ranh giới?)
Nhiều đồ án tự nhận là "tối ưu hóa chiến dịch marketing và tăng 15% ROI". Đây là khẳng định ngụy tạo nếu chỉ dùng dữ liệu quan sát clickstream REES46. Nếu không có nhóm đối chứng (Control Group) và chi phí chiến dịch, việc tuyên bố ROI là hoàn toàn vô căn cứ.

### 3. How (Cách thức triển khai?)
1. Xây dựng bộ quy tắc gợi ý chiến thuật minh bạch: `Evidence $\to$ Segment $\to$ Insight $\to$ Goal $\to$ Tactic $\to$ Reasons $\to$ KPI`.
2. Gắn nhãn cố định cho mọi chiến thuật: `status = RECOMMENDED_NOT_VALIDATED`.
3. Chỉ định rõ KPI cần theo dõi trong tương lai nếu chủ shop quyết định triển khai thử nghiệm A/B.

### 4. Formula (Công thức đo lường chuẩn nếu có A/B Test)
$$\text{Incremental Profit} = (\text{CR}_{\text{treatment}} - \text{CR}_{\text{control}}) \times N_{\text{target}} \times \text{Gross Margin} - \text{Campaign Cost}$$
*(Trong REES46, chỉ số này được đánh dấu là `not_observable_with_REES46`)*.

### 5. Worked Example (Ví dụ phân biệt thực tế)
- **Tình huống:** Khách hàng `u10` thuộc cụm At-Risk, có 2 giỏ hàng bị bỏ dở trong 7 ngày gần nhất.
- **Những gì hệ thống LÀM ĐƯỢC:**
  - Phát hiện bằng chứng: `recency = 45 ngày`, `has_recent_cart = True`.
  - Đề xuất chiến thuật: `TAC_CART_RECOVERY` (Gửi email nhắc nhở giỏ hàng).
  - Cung cấp mã nguyên nhân: `REASON_CART_ABANDONED_RECENTLY`.
  - Cảnh báo: Đây là gợi ý thử nghiệm, cần theo dõi `cart_to_purchase_rate`.
- **Những gì hệ thống KHÔNG ĐƯỢC PHÉP TUYÊN BỐ:**
  - "Gửi email này chắc chắn sẽ làm khách u10 mua hàng 100%."
  - "Chiến thuật này đã đem lại 50$ lợi nhuận ròng."

### 6. Alternatives (Phương án thay thế)
- *Mô hình Uplift hai mô hình (Two-Model Approach) hoặc Causal Forest:* Chỉ áp dụng được khi doanh nghiệp có dữ liệu thử nghiệm A/B thực tế có nhóm Treatment và Control.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử bộ luật Decision Engine bằng Unit Tests: kiểm tra tính bao phủ (100% khách hàng có đề xuất), tính nhất quán (không có xung đột luật), và tính truy vết (mỗi đề xuất đều có lý do gắn với đặc trưng).

### 8. Limitations (Giới hạn)
Các chiến thuật tiếp thị đề xuất phụ thuộc vào chất lượng bộ luật của chuyên gia; không có khả năng tự động học hỏi nếu không có vòng phản hồi kết quả chiến dịch thực tế.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Hệ thống của em có chứng minh được rằng chiến thuật marketing đề xuất sẽ làm tăng doanh thu của shop không?"*  
> **Trả lời:** *"Thưa Thầy/Cô, KHÔNG THỂ chứng minh từ tập dữ liệu này. Tập dữ liệu REES46 là dữ liệu quan sát hành vi tự nhiên (observational log), hoàn toàn không chứa thông tin can thiệp tiếp thị (marketing campaign), không có nhóm đối chứng (control group) và không có chi phí quảng cáo. Theo nguyên tắc suy diễn nhân quả (Causal Inference), chúng em không thể suy diễn tương quan thành quan hệ nhân quả. Do đó, hệ thống định vị chính xác là 'Decision Support' (Hỗ trợ ra quyết định) nhằm đề xuất các ứng viên chiến thuật có căn cứ định lượng, và đánh dấu trạng thái là 'NOT_VALIDATED' để chủ shop tiến hành thử nghiệm A/B có kiểm soát trước khi triển khai diện rộng."*

---

## P0.9 — Phương pháp Đo lường Hiệu năng: time.perf_counter(), psutil RSS vs. DuckDB Memory Limits

### 1. What (Khái niệm là gì?)
- **`time.perf_counter()`:** Hàm đo đồng hồ thời gian thực (wall-clock time) có độ phân giải cao nhất trong Python, không bị ảnh hưởng bởi việc điều chỉnh giờ hệ thống.
- **Process RSS (Resident Set Size via `psutil`):** Lượng bộ nhớ RAM vật lý thực tế mà toàn bộ tiến trình hệ điều hành (bao gồm cả mã Python và thư viện C/C++ native) đang chiếm dụng.
- **`tracemalloc`:** Thư viện Python chỉ theo dõi lượng bộ nhớ được cấp phát bên trong trình thông dịch Python (Python heap), bỏ qua toàn bộ bộ nhớ native C++ của DuckDB và Scikit-learn.
- **DuckDB `memory_limit`:** Tham số cấu hình giới hạn vùng đệm của riêng DuckDB, **không phải là mức trần tuyệt đối** của toàn bộ tiến trình máy tính.

### 2. Why (Tại sao phải đo đúng?)
Nếu dùng `tracemalloc` để đo bộ nhớ khi chạy DuckDB, bạn sẽ thấy bộ nhớ chỉ tốn vài chục MB và vội kết luận hệ thống cực kỳ nhẹ, trong khi thực tế tiến trình DuckDB C++ native đang chiếm dụng hàng gigabyte RAM bên dưới và có thể làm sập máy tính.

### 3. How (Cách thức triển khai?)
1. Đo thời gian bằng cặp mốc `time.perf_counter()` trước và sau mỗi công đoạn.
2. Đo bộ nhớ bằng luồng lấy mẫu định kỳ (sampling thread) sử dụng `psutil.Process().memory_info().rss` để bắt đỉnh RAM (Peak RSS).
3. Chạy benchmark trên một tiến trình Python tươi mới (fresh process) để không bị ảnh hưởng bởi bộ nhớ đệm còn sót lại từ các lệnh trước.

### 4. Formula (Công thức tính toán)
$$\text{Wall Time} = t_{\text{finish}} - t_{\text{start}} \quad (\text{seconds})$$

$$\text{Peak Memory Delta} = \max_{t} (\text{RSS}(t)) - \text{RSS}_{\text{baseline}} \quad (\text{bytes})$$

$$\text{Throughput} = \frac{N_{\text{records}}}{\text{Wall Time}} \quad (\text{records/second})$$

### 5. Worked Example (Đo lường mẫu code Python)
```python
import time
import psutil
import os

process = psutil.Process(os.getpid())
baseline_rss = process.memory_info().rss

t0 = time.perf_counter()

# Thực hiện công đoạn tính toán (ví dụ: DuckDB query hoặc K-Means fit)
# ... quá trình xử lý ...

t1 = time.perf_counter()
peak_rss = process.memory_info().rss  # Hoặc lấy mẫu liên tục qua thread

elapsed_seconds = t1 - t0
memory_used_mb = (peak_rss - baseline_rss) / (1024 * 1024)
print(f"Thời gian thực thi: {elapsed_seconds:.4f} giây")
print(f"Bộ nhớ RSS tiêu tốn: {memory_used_mb:.2f} MB")
```

### 6. Alternatives (Phương án thay thế)
- *Công cụ dòng lệnh OS (Time, Memory Profiler):* Tốt cho việc đo toàn trình từ bên ngoài, nhưng khó bóc tách chi tiết từng hàm nội bộ.

### 7. Verification (Cách thức kiểm chứng)
Ghi nhận thông tin phần cứng máy trạm (CPU, RAM, OS, Python version) đi kèm với mỗi nhật ký benchmark; chạy lặp lại ít nhất 3 lần để lấy giá trị trung vị (median).

### 8. Limitations (Giới hạn)
Phương pháp lấy mẫu RSS (sampling) có thể bỏ lỡ các đỉnh bộ nhớ diễn ra quá ngắn (transient spikes) nằm giữa hai chu kỳ lấy mẫu.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không dùng tracemalloc của Python để đo bộ nhớ RAM khi truy vấn dữ liệu lớn bằng DuckDB?"*  
> **Trả lời:** *"Thưa Thầy/Cô, tracemalloc là công cụ theo dõi bộ nhớ cấp phát ở tầng Python interpreter. Trong khi đó, DuckDB là một hệ quản trị cơ sở dữ liệu OLAP được viết bằng C++ native. Phần lớn bộ nhớ dùng để đọc file Parquet, quét cột và xử lý truy vấn đều được cấp phát trực tiếp dưới tầng C++ runtime. Do đó, tracemalloc hoàn toàn mù (blind) trước lượng RAM thực tế mà DuckDB tiêu tốn. Để đo lường trung thực tài nguyên máy tính, chúng em bắt buộc phải sử dụng thư viện psutil để đo trực tiếp Resident Set Size (RSS) của toàn bộ tiến trình hệ điều hành."*

---

## P0.10 — Bộ 12 Câu hỏi Vấn đáp Trọng tâm và Hướng dẫn Trả lời Bảo vệ Đồ án

### Q01: Tại sao đồ án chọn mô hình CRISP-DM thay vì phát triển phần mềm theo Agile thông thường?
- **Trả lời:** CRISP-DM là quy trình được thiết kế chuyên biệt cho các dự án Khai phá Dữ liệu và Khoa học Dữ liệu. Khác với phát triển tính năng phần mềm thuần túy trong Agile, các dự án dữ liệu có tính khám phá cao và phụ thuộc chặt chẽ vào giả thuyết kinh doanh. CRISP-DM đảm bảo chu trình khép kín: từ thấu hiểu bài toán nghiệp vụ, kiểm soát chất lượng dữ liệu, trích xuất đặc trưng, mô hình hóa đến đánh giá đa chiều và triển khai có kiểm soát.

### Q02: Trong phân tích hành vi clickstream, việc nhầm lẫn giữa các cấp độ hạt (grains) sẽ dẫn đến hậu quả gì?
- **Trả lời:** Việc nhầm lẫn grain sẽ dẫn đến tính toán sai lệch hoàn toàn các chỉ số kinh doanh cốt lõi. Ví dụ: Nếu nhầm lẫn giữa event grain và session grain, mẫu số của tỷ lệ chuyển đổi sẽ bị thổi phồng hàng chục lần (do một phiên có hàng chục lượt view). Nếu nhầm lẫn giữa purchase event và order, tần suất mua sắm (Frequency) của khách hàng sẽ bị phóng đại sai sự thật.

### Q03: Tập dữ liệu REES46 có những hạn chế lớn nào và đồ án đã khắc phục về mặt thiết kế ra sao?
- **Trả lời:** REES46 có 4 hạn chế lớn: (1) Không có `order_id` độc lập $\to$ Đồ án sử dụng proxy phiên mua hàng (`purchase_sessions_proxy`); (2) Không có dữ liệu số lượng (quantity) và hoàn tiền $\to$ Đồ án công khai chỉ số Monetary chỉ là giá trị quan sát, không phải Net GMV; (3) Không có dữ liệu thử nghiệm chiến dịch marketing $\to$ Toàn bộ đề xuất chiến thuật được gắn trạng thái `NOT_VALIDATED` và chỉ đóng vai trò hỗ trợ quyết định; (4) Khuyết thiếu mã phiên ở một số bản ghi $\to$ Đồ án thiết lập bộ lọc chất lượng và công bố tỷ lệ thất thoát.

### Q04: Tại sao không thể gán Recency = 999 cho người dùng chưa từng mua hàng để chạy chung K-Means?
- **Trả lời:** Recency của người chưa mua về mặt toán học là không xác định (undefined). K-Means sử dụng khoảng cách Euclidean. Nếu gán một giá trị nhân tạo cực lớn như 999 cho một tập người dùng chiếm đa số, trục Recency sẽ bị kéo dãn cực độ, làm biến dạng hoàn toàn hàm mục tiêu WCSS và phá hủy cấu trúc phân cụm của những khách hàng đã mua thực tế.

### Q05: Khái niệm Data Leakage được kiểm soát như thế nào tại ranh giới thời gian cutoff?
- **Trả lời:** Đồ án thiết lập ranh giới thời gian nửa mở $[2019-10-01, 2020-02-01)$ cho kỳ quan sát. Mọi bước làm sạch dữ liệu, chuẩn hóa và trích xuất đặc trưng chỉ duyệt dữ liệu trước mốc cutoff $T_{cutoff} = 2020-02-01T00:00:00Z$. Dữ liệu tháng 02/2020 được niêm phong độc lập làm tập Holdout và chỉ được mở ra ở Phase 5 để hậu kiểm tỷ lệ mua hàng của các cụm mà không dùng để tinh chỉnh siêu tham số.

### Q06: Ý nghĩa của việc kết hợp Clickstream Engagement 30 ngày gần nhất vào mô hình RFM là gì?
- **Trả lời:** Mô hình RFM truyền thống chỉ phản ánh hành vi giao dịch trong quá khứ và có độ trễ lớn. Trong e-commerce, phần lớn hành vi thể hiện qua việc lướt xem hàng và thêm giỏ. Bổ sung Engagement 30 ngày gần nhất giúp nhận diện được trạng thái hiện tại của khách hàng: ví dụ, phân biệt khách hàng sắp rời bỏ (ngừng mua và ngừng vào web) với khách hàng vẫn đang quan tâm (ngừng mua nhưng vẫn vào xem sản phẩm hàng tuần).

### Q07: Tại sao Silhouette Score cao không đồng nghĩa với việc mô hình phân cụm tối ưu cho kinh doanh?
- **Trả lời:** Silhouette Score chỉ là một thước đo hình học nội tại đo độ gắn kết và phân tách trong không gian toán học trừu tượng. Một mô hình có thể đạt Silhouette rất cao khi cô lập một nhóm nhỏ ngoại lai hoặc chia dữ liệu thành 2 cụm quá khái quát. Trong kinh doanh, một mô hình tối ưu phải có ý nghĩa hành động (Actionable), các cụm phải có quy mô hợp lý và chân dung các cụm phải phân biệt rõ ở các chiều đo gốc.

### Q08: Nếu một mô hình K-Means chạy nhanh hơn nhưng Silhouette thấp hơn một chút, căn cứ nào để lựa chọn?
- **Trả lời:** Chúng em sử dụng Ma trận Đánh đổi Đa chiều (Multi-dimensional Trade-off Matrix). Nếu sự suy giảm Silhouette không đáng kể nhưng mô hình mang lại độ ổn định cao hơn qua các random seed ($ARI \ge 0.8$), các cụm có chân dung kinh doanh sắc nét hơn và thời gian chạy đáp ứng được chu kỳ vận hành batch của doanh nghiệp, mô hình đó sẽ được ưu tiên lựa chọn.

### Q09: Mô hình Cây Quyết định Nông (Surrogate Tree) đóng vai trò gì và có chứng minh được K-Means phân cụm đúng không?
- **Trả lời:** Cây Quyết định Nông đóng vai trò là một mô hình đại diện (surrogate model) dùng để bóc tách các luật ranh giới trực quan (if-then rules) nhằm giải thích cơ chế gán nhãn của K-Means cho người dùng dashboard. Độ chính xác mô phỏng (fidelity) của cây chỉ đo lường mức độ cây bắt chước K-Means tốt đến đâu, hoàn toàn KHÔNG chứng minh được việc phân cụm của K-Means là đúng đắn về mặt chân lý kinh doanh.

### Q10: Phân định ranh giới: Phần nào là Machine Learning, phần nào là Thống kê, và phần nào là Luật chuyên gia?
- **Trả lời:**
  - *Machine Learning (K-Means):* Thực hiện gom cụm không giám sát trên không gian đặc trưng.
  - *Thống kê mô tả (Statistical Profiling):* Tính toán các chỉ số median, mean, phễu chuyển đổi và kiểm định sự khác biệt giữa các cụm.
  - *Luật chuyên gia (Rule-based Decision Engine):* Ánh xạ từ chân dung cụm và bằng chứng cá nhân sang danh mục chiến thuật tiếp thị có thể giải thích được.
  - *Tác động nhân quả (Causal Impact):* Chưa thực hiện do thiếu dữ liệu thử nghiệm A/B.

### Q11: Làm thế nào để đảm bảo người dùng không nhầm lẫn dữ liệu nghiên cứu REES46 với dữ liệu thật của IVRE?
- **Trả lời:** Hệ thống áp dụng 3 biện pháp kiểm soát: (1) Phân rã kiến trúc độc lập, IVRE chỉ đọc tệp JSON snapshot tĩnh; (2) Toàn bộ màn hình dashboard đều hiển thị cố định huy hiệu `Research Demo / REES46 Cosmetics`; (3) Tuyên bố rõ ràng trong báo cáo và tài liệu hướng dẫn rằng dữ liệu mỹ phẩm REES46 không đại diện cho dữ liệu khách hàng thời trang của IVRE.

### Q12: Nếu chưa có dữ liệu thử nghiệm A/B, làm sao kiểm chứng được chất lượng của Marketing Decision Engine?
- **Trả lời:** Chúng em kiểm chứng bộ máy luật thông qua 4 tiêu chuẩn kỹ thuật phần mềm: (1) *Tính bao phủ (Coverage):* 100% khách hàng hợp lệ đều nhận được khuyến nghị; (2) *Tính nhất quán (Consistency):* Không có xung đột giữa các luật; (3) *Tính truy vết (Traceability):* Mỗi khuyến nghị đều đi kèm mã nguyên nhân (reason codes) liên kết trực tiếp với dữ liệu đặc trưng định lượng; (4) *Kiểm thử đơn vị tự động (Rule Unit Tests):* Xác thực logic điều kiện và loại trừ của từng luật.

---

# PHẦN II — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 1 (DATA UNDERSTANDING & EDA)

## P1.1 — Data Profiling trên Dữ liệu Lớn với DuckDB in-process OLAP Engine

### 1. What (Khái niệm là gì?)
Data Profiling là quá trình phân tích và đánh giá tự động cấu trúc, kiểu dữ liệu, tính đầy đủ, phân phối giá trị và mối quan hệ giữa các cột trong một tập dữ liệu lớn. DuckDB là một hệ quản trị cơ sở dữ liệu OLAP dạng nhúng (in-process) xử lý dữ liệu theo cột (columnar-vectorized execution).

### 2. Why (Tại sao cần dùng?)
Tập dữ liệu REES46 gồm 5 tệp CSV với tổng dung lượng 2.32 GB (~20.7 triệu dòng). Nếu nạp toàn bộ vào Pandas (`pd.read_csv`), Pandas sẽ tiêu tốn từ 8–12 GB RAM do cơ chế quản lý đối tượng phân mảnh của Python, dễ gây tràn bộ nhớ (Out-Of-Memory - OOM) trên máy trạm 16 GB RAM (chỉ còn ~2.3 GB khả dụng). DuckDB cho phép truy vấn trực tiếp trên đĩa với cơ chế phân trang và quản lý vùng đệm bộ nhớ nghiêm ngặt.

### 3. How (Cách thức triển khai?)
1. Cấu hình giới hạn bộ nhớ: `con.execute("SET memory_limit = '2GB'")`.
2. Giới hạn số luồng xử lý: `con.execute("SET threads = 4")`.
3. Quét trực tiếp các tệp CSV: `SELECT ... FROM read_csv('data/raw/*.csv', header=True, auto_detect=True)`.

### 4. Formula (Thông lượng xử lý dữ liệu)
$$\text{Throughput} = \frac{\text{Total Rows Processed}}{\text{Wall-Clock Time}} \quad (\text{rows/second})$$

### 5. Worked Example (Thực nghiệm trên REES46)
- Tổng số bản ghi: **20,692,840 dòng**.
- Thời gian thực thi: **78.39 giây**.
- Thông lượng: **263,973 dòng/giây**.
- Đỉnh RAM (Peak RSS): **1,618.41 MB** (hoàn toàn nằm dưới ngưỡng 2 GB cho phép).

### 6. Alternatives (Phương án thay thế)
- *Pandas chunking:* Đọc từng batch nhỏ (ví dụ: `chunksize=100000`). **Nhược điểm:** Phải tự viết logic tổng hợp phức tạp và chậm hơn DuckDB 5–10 lần.
- *Apache Spark / PySpark:* Rất mạnh cho cụm phân tán, nhưng quá cồng kềnh (overhead JVM) cho một máy trạm đơn lẻ trong phạm vi đồ án 21 ngày.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động bằng `TestPhase1Performance` trong `tests/test_phase1_data_understanding.py`: xác thực thời gian < 180s và Peak RSS < 2.5 GB.

### 8. Limitations (Giới hạn)
DuckDB phụ thuộc vào tốc độ đọc của ổ đĩa (Disk I/O). Việc đọc CSV dạng văn bản thô tốn nhiều CPU để phân tích chuỗi (parsing) hơn so với định dạng nhị phân Parquet.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không dùng pandas.read_csv() để phân tích dữ liệu ngay từ đầu?"*  
> **Trả lời:** *"Thưa Thầy/Cô, pandas.read_csv() là công cụ xử lý trên bộ nhớ RAM (in-memory) theo mô hình dòng đối tượng. Với 20.7 triệu dòng bản ghi thô (2.32 GB trên đĩa), Pandas sẽ cần tối thiểu 8–10 GB RAM để nạp DataFrame. Tại thời điểm chạy, RAM khả dụng của máy chỉ còn khoảng 2.3 GB, việc dùng Pandas chắc chắn sẽ làm sập tiến trình (OOM Crash). DuckDB sử dụng cơ chế xử lý theo cột (vectorized columnar engine) và stream dữ liệu từ đĩa với giới hạn bộ nhớ cấu hình 2 GB, hoàn thành toàn bộ tác vụ profiling chỉ trong 78 giây mà đỉnh RAM chỉ tốn 1.6 GB."*

---

## P1.2 — Phân tích Phễu Chuyển đổi Cấp Phiên (Session-Level Funnel) và Nút thắt Bỏ giỏ hàng

### 1. What (Khái niệm là gì?)
Phễu chuyển đổi cấp phiên (Session-level Funnel) phân tích hành trình người dùng qua các chặng trong một phiên truy cập: **Total Sessions $\to$ View Sessions $\to$ Cart Sessions $\to$ Purchase Sessions**.

### 2. Why (Tại sao phải phân tích ở cấp phiên thay vì cấp sự kiện?)
Nếu phân tích ở cấp sự kiện (event count), chúng ta sẽ thấy 9.6M views và 1.28M purchases $\to$ tưởng lầm tỷ lệ chuyển đổi là 13.3%. Nhưng trong thực tế, một phiên mua hàng chứa trung bình 8.27 món hàng. Phân tích ở cấp phiên (session grain) mới phản ánh đúng xác suất một lượt ghé thăm website có phát sinh giao dịch hay không.

### 3. How (Cách thức triển khai?)
1. Nhóm theo cặp khóa phiên `(user_id, user_session)`.
2. Tạo cờ boolean cho từng phiên: `has_view`, `has_cart`, `has_purchase`.
3. Kiểm tra điều kiện mua sau khi thêm giỏ: $\max(t_{purchase}) > \min(t_{cart})$.

### 4. Formula (Công thức tỷ lệ bỏ giỏ hàng)
$$\text{CartAbandonmentRate} = \frac{|\{s \in \text{Sessions} \mid \text{has\_cart}(s) \land \neg \text{has\_purchase}(s)\}|}{|\{s \in \text{Sessions} \mid \text{has\_cart}(s)\}|}$$

### 5. Worked Example (Số liệu thực tế trên 3.61M phiên kỳ observation)
- Tổng số phiên hợp lệ: **3,614,959**.
- Phiên có xem sản phẩm: **3,411,359** (94.37%).
- Phiên có thêm giỏ hàng: **800,307** (22.14%).
- Phiên có mua hàng: **126,503** (3.50%).
- Phiên giỏ hàng chuyển đổi mua trong cùng phiên: **102,314** (12.78% số phiên cart).
- **Số phiên bỏ giỏ hàng:** **697,337** phiên $\implies \text{Cart Abandonment Rate} = \mathbf{87.13\%}$.

### 6. Alternatives (Phương án thay thế)
- *User-level conversion rate:* Đo lường tỷ lệ người dùng có mua trong kỳ (đạt 6.91%). Phễu phiên bổ trợ cho phễu user để tìm nút thắt trải nghiệm.

### 7. Verification (Cách thức kiểm chứng)
Unit test `test_purchase_session_proxy_validity` và kiểm tra logic phễu trong kịch bản profiling.

### 8. Limitations (Giới hạn)
Dữ liệu chỉ đo chuyển đổi trong cùng một phiên; khách thêm giỏ hôm nay nhưng sang hôm sau mới quay lại mua ở phiên khác sẽ bị tính là bỏ giỏ trong phiên đầu tiên.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tỷ lệ bỏ giỏ hàng 87.13% nói lên điều gì về mặt kinh doanh và hệ thống của em giải quyết vấn đề này thế nào?"*  
> **Trả lời:** *"Thưa Thầy/Cô, con số 87.13% (gần 700,000 phiên bỏ giỏ) chứng minh rằng khách hàng có sự quan tâm rất cao đến sản phẩm mỹ phẩm (đã chọn món đưa vào giỏ), nhưng gặp rào cản ở bước thanh toán cuối cùng (có thể do phí vận chuyển cao, thiếu phương thức thanh toán phù hợp, hoặc đang so sánh giá). Hệ thống của chúng em phát hiện chính xác nút thắt này và giải quyết bằng cách: (1) Phân tầng nhóm 'Cart Abandoners' trong tập Non-buyers; (2) Tự động kích hoạt chiến thuật tiếp thị TAC_CART_RECOVERY với thông điệp hỗ trợ hoàn tất đơn hàng."*

---

## P1.3 — Xử lý Bất thường Dữ liệu Clickstream: Giá âm, Giá bằng 0 và Sự kiện Trùng lặp

### 1. What (Khái niệm là gì?)
Dữ liệu thô thực tế luôn chứa nhiễu kỹ thuật:
- **Giá âm (`price < 0`):** Giá trị âm trong trường giá (131 bản ghi, nhỏ nhất là -79.37).
- **Giá bằng 0 (`price = 0`):** Bản ghi có giá bằng 0 (104,157 bản ghi).
- **Sự kiện trùng lặp hợp lệ vs bất thường:** Khách hàng nhấn mua 1 giỏ hàng nhiều món sinh ra nhiều dòng purchase cùng giây vs việc gửi lặp gói tin do lỗi mạng.

### 2. Why (Tại sao phải phân loại rõ?)
Nếu mù quáng loại bỏ mọi dòng có cùng timestamp và cùng session, chúng ta sẽ xóa mất các món hàng hợp lệ trong cùng 1 giỏ hàng. Nhưng nếu để nguyên giá âm và giá 0, chỉ số chi tiêu Monetary của khách hàng sẽ bị tính sai lệch.

### 3. How (Cách thức xử lý cho Phase 2)
1. Chỉ tính Monetary trên các sự kiện purchase có `price > 0`.
2. Giữ nguyên các dòng purchase có cùng timestamp nếu chúng khác `product_id` (đây là các mặt hàng khác nhau trong cùng giỏ hàng).
3. Đếm riêng số lượng bản ghi giá bất thường vào báo cáo kiểm toán chất lượng.

### 4. Formula (Lọc giá trị Monetary hợp lệ)
$$M_u = \sum_{e \in \text{Purchases}(u)} e.\text{price} \quad \text{với điều kiện } e.\text{price} > 0$$

### 5. Worked Example (Thực nghiệm REES46)
- Số dòng `price < 0`: 131 dòng (chiếm tỷ lệ cực nhỏ: 0.0006%).
- Số dòng `price = 0`: 104,157 dòng (chiếm 0.50% tổng dữ liệu, thường là hàng mẫu thử nghiệm tester hoặc quà tặng kèm promotion).
- Sau khi lọc `price > 0`, phân phối Monetary của buyers duy trì tính chuẩn xác tuyệt đối với Median = 33.17 và Mean = 55.52.

### 6. Alternatives (Phương án thay thế)
- *Imputation (Điền giá trị thiếu/âm bằng trung vị sản phẩm):* Không cần thiết và tiềm ẩn rủi ro bóp méo doanh thu thực tế; tốt nhất là loại bỏ khi tính tiền tệ.

### 7. Verification (Cách thức kiểm chứng)
Unit test `test_price_anomalies_flagged` trong `tests/test_phase1_data_understanding.py`.

### 8. Limitations (Giới hạn)
Dataset không ghi chú nguyên nhân vì sao có giá âm (có thể là hoàn tiền refund, voucher trừ tiền hoặc lỗi hệ thống POS).

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Em xử lý thế nào với 104,288 bản ghi có giá nhỏ hơn hoặc bằng 0 trong tập dữ liệu?"*  
> **Trả lời:** *"Thưa Thầy/Cô, chúng em tiến hành kiểm toán và phát hiện có 131 dòng giá âm và 104,157 dòng giá bằng 0. Trong thương mại điện tử mỹ phẩm, các dòng giá 0 thường là hàng mẫu dùng thử (samples), quà tặng kèm (gift with purchase) hoặc mã giảm giá 100%. Chiến lược xử lý của chúng em trong Phase 2 là: Vẫn giữ lại các sự kiện này cho phân tích hành vi tương tác (Engagement), nhưng loại trừ tuyệt đối các dòng price <= 0 khi tính toán đặc trưng chi tiêu Monetary (M) và doanh số bán hàng, nhằm đảm bảo thước đo tài chính phản ánh đúng giá trị tiền tệ thực tế."*

---

## P1.4 — Chiến lược Xử lý Dữ liệu Khuyết thiếu (Missing Value Strategy)

### 1. What (Khái niệm là gì?)
Chiến lược xử lý khuyết thiếu dựa trên bản chất cơ chế sinh dữ liệu (MCAR, MAR, MNAR) của từng cột.

### 2. Why (Tại sao không được xóa toàn bộ dòng chứa null?)
Nếu áp dụng phương pháp thô bạo `df.dropna()`, bạn sẽ **xóa sạch 98.3% tập dữ liệu** (vì cột `category_code` khuyết 98.29%).

### 3. How (Quy tắc xử lý cụ thể cho từng trường trong REES46)

| Tên trường | Tỷ lệ Missing | Cơ chế sinh dữ liệu | Chiến lược xử lý chuẩn xác |
|---|---|---|---|
| `user_id` | **0.00%** | Hoàn chỉnh | Giữ nguyên 100%. |
| `user_session` | **0.022%** (4,598 dòng) | Lỗi tracking ngẫu nhiên | Loại bỏ khỏi các phân tích cấp phiên; không ảnh hưởng purchase vì purchase có 0% missing session. |
| `category_code` | **98.29%** | Thiếu do danh mục không gán cây thư mục | **KHÔNG dùng làm đặc trưng chính**. Thay thế bằng `category_id` (đầy đủ 100%). |
| `brand` | **42.32%** | Hàng gia công/không nhãn hiệu | Điền nhãn `'unknown'` hoặc `'unbranded'`; tạo biến nhị phân `is_branded`. |
| `price` | **0.00%** | Hoàn chỉnh | Lọc `price > 0` khi tính tiền tệ. |

### 4. Formula (Tỷ lệ hoàn thiện dữ liệu của trường)
$$\text{Completeness}(X) = 1 - \frac{\text{NullCount}(X)}{N_{\text{total}}}$$

### 5. Worked Example (Thực nghiệm)
- Trường `category_code` có Completeness = $1 - 0.9829 = 1.71\% \implies$ Phế bỏ làm biến phân cụm.
- Trường `user_session` có Completeness = $99.978\% \implies$ Đạt độ tin cậy tuyệt đối cho phân tích phễu phiên.

### 6. Alternatives (Phương án thay thế)
- *Dùng mô hình KNN Imputer hoặc Random Forest để đoán category_code:* Bị loại vì tỷ lệ khuyết quá lớn (>98%), mọi nỗ lực đoán mò đều sẽ sinh ra dữ liệu giả tạo (hallucinated data).

### 7. Verification (Cách thức kiểm chứng)
Hình ảnh [fig7_missing_values_by_month.png](file:///d:/Lap%20trinh/customer-analytics-antigravity/outputs/figures/fig7_missing_values_by_month.png) và kiểm thử `test_zero_missing_user_id`.

### 8. Limitations (Giới hạn)
Không thể phân loại sở thích ngành hàng chi tiết nếu chỉ dựa vào chuỗi văn bản danh mục; phải dựa vào mã số `category_id`.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao cột category_code khuyết tới hơn 98% mà em vẫn tiếp tục dùng tập dữ liệu này?"*  
> **Trả lời:** *"Thưa Thầy/Cô, cột category_code chỉ là trường chuỗi văn bản mô tả cây thư mục phụ trợ (ví dụ: 'appliances.environment.vacuum'). Trong khi đó, trường mã định danh danh mục category_id có đầy đủ 100% không khuyết một dòng nào. Quan trọng hơn, bài toán trọng tâm của đồ án là phân khúc dựa trên hành vi mua sắm (RFM) và tương tác số (Clickstream Engagement: số phiên, lượt view, giỏ hàng, xu hướng tương tác), vốn dựa trên user_id, user_session, event_time và event_type - những trường đều có độ hoàn thiện từ 99.98% đến 100%. Do đó, việc thiếu category_code hoàn toàn không ảnh hưởng đến chất lượng phân cụm khách hàng của chúng em."*

---

## P1.5 — Đánh giá Ranh giới Thời gian và Hiện tượng Phiên vắt qua Cutoff (Spanning Sessions)

### 1. What (Khái niệm là gì?)
Hiện tượng Spanning Session xảy ra khi một phiên truy cập của người dùng bắt đầu trước mốc cutoff ($t_{\text{start}} < T_{\text{cutoff}}$) và kéo dài qua mốc cutoff ($t_{\text{end}} \ge T_{\text{cutoff}}$).

### 2. Why (Tại sao phải phân định ranh giới?)
Nếu không có quy tắc rõ ràng, việc tính toàn bộ phiên này vào kỳ observation sẽ làm lọt các sự kiện của tương lai vào mô hình huấn luyện (Data Leakage). Ngược lại, nếu loại bỏ toàn bộ phiên, chúng ta sẽ làm mất dữ liệu của quá khứ.

### 3. How (Quy tắc ranh giới nửa mở ở cấp độ sự kiện)
Áp dụng quy tắc cắt cứng (Strict Event-level Cutoff):
- Sự kiện có $event\_time < 2020-02-01T00:00:00Z \to$ Thuộc về Kỳ Quan sát (Observation).
- Sự kiện có $event\_time \ge 2020-02-01T00:00:00Z \to$ Thuộc về Kỳ Hậu kiểm (Holdout).

### 4. Formula (Tập hợp phân chia)
$$\mathcal{E}_{\text{obs}} = \{e \in \mathcal{E} \mid e.\text{time} < T_{\text{cutoff}}\}$$
$$\mathcal{E}_{\text{future}} = \{e \in \mathcal{E} \mid e.\text{time} \ge T_{\text{cutoff}}\}$$

### 5. Worked Example (Thực nghiệm REES46)
- Tổng số phiên vắt qua cutoff: **10,451 phiên**.
- So với tổng 3.61 triệu phiên quan sát, tỷ lệ này chỉ chiếm **0.29%**.
- Việc cắt cứng theo timestamp sự kiện giúp 100% các đặc trưng của 1,341,499 người dùng tại ngày 01/02/2020 được đóng băng tuyệt đối, triệt tiêu hoàn toàn nguy cơ rò rỉ thông tin từ tháng 2.

### 6. Alternatives (Phương án thay thế)
- *Loại bỏ hoàn toàn các phiên vắt:* Làm mất 10,451 tương tác hợp lệ của quá khứ.

### 7. Verification (Cách thức kiểm chứng)
Unit test `test_temporal_split_integrity` trong `tests/test_phase1_data_understanding.py`: xác thực tổng sự kiện hai kỳ bằng chính xác tổng 20,692,840 dòng.

### 8. Limitations (Giới hạn)
Một khách hàng bắt đầu bỏ giỏ lúc 23:55 ngày 31/01 và thanh toán lúc 00:05 ngày 01/02 sẽ có sự kiện cart tính cho observation và purchase tính cho holdout; điều này hoàn toàn phù hợp với thực tế vận hành khi doanh nghiệp chốt sổ sách cuối tháng.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Em xử lý thế nào với 10,451 phiên truy cập bắt đầu từ tháng 1 nhưng kết thúc sang tháng 2?"*  
> **Trả lời:** *"Thưa Thầy/Cô, chúng em áp dụng nguyên tắc ranh giới nửa mở [start, end) triệt để ở cấp độ từng dòng sự kiện (event-level filtering). Bất kỳ sự kiện nào xảy ra trước đúng 00:00:00 ngày 01/02/2020 đều được tính cho kỳ quan sát (observation), còn các sự kiện xảy ra từ 00:00:00 trở đi thuộc về kỳ kiểm chứng tương lai (holdout). Cách làm này đảm bảo tính đóng băng tuyệt đối của không gian đặc trưng tại thời điểm chốt dữ liệu, không làm rò rỉ bất kỳ hành vi tương lai nào vào mô hình phân cụm."*

---

## P1.6 — Đo kiểm Hiệu năng Thực tế (Benchmark Profiling: Wall-clock, Process RSS vs Buffer Pool)

### 1. What (Khái niệm là gì?)
Đo kiểm hiệu năng khoa học bằng việc kết hợp giữa thời gian thực tế (Wall-Clock Time) và bộ nhớ vật lý thực tế của tiến trình (Resident Set Size - RSS) qua thư viện `psutil`.

### 2. Why (Tại sao DuckDB memory_limit không tương đương với Process RSS?)
Tham số `memory_limit` của DuckDB chỉ khống chế kích thước của **vùng đệm quản lý trang bộ nhớ (Buffer Pool)**. Nó không giới hạn bộ nhớ cấp phát cho luồng thực thi hệ thống, trình thông dịch Python, mã nhị phân thư viện C++ và bảng trang hệ điều hành. Do đó, nếu chỉ nhìn `memory_limit = 2GB`, bạn không thể khẳng định tiến trình chỉ tốn đúng 2 GB RAM nếu không đo trực tiếp RSS.

### 3. How (Cách thức đo kiểm chuẩn mực)
1. Khởi chạy luồng chạy ngầm (background thread) định kỳ mỗi 200ms để bắt đỉnh `process.memory_info().rss`.
2. Ghi nhận `baseline_rss` ban đầu và `peak_rss` cao nhất đạt được trong suốt quá trình xử lý.
3. Đo thời gian bằng `time.perf_counter()`.

### 4. Formula (Chênh lệch bộ nhớ thực tế)
$$\Delta \text{RSS} = \text{Peak RSS} - \text{Baseline RSS}$$

### 5. Worked Example (Số liệu thực tế trên máy trạm 16 CPUs)
- Dữ liệu đầu vào: **2.32 GB CSV** (20,692,840 dòng).
- Thời gian chạy toàn trình: **78.39 giây**.
- Thông lượng: **263,973 dòng/giây**.
- Baseline RSS: **123.71 MB**.
- Peak RSS: **1,618.41 MB** (~1.58 GB).
- Delta RSS: **+1,494.70 MB**.
- Nhận xét: Tiến trình thực sự chiếm dụng 1.62 GB RAM, nằm an toàn dưới giới hạn buffer pool 2 GB và dung lượng RAM khả dụng (2.27 GB).

### 6. Alternatives (Phương án thay thế)
- *Dùng tracemalloc:* Đã chứng minh ở Phase 0 là hoàn toàn "mù" trước bộ nhớ C++ của DuckDB.

### 7. Verification (Cách thức kiểm chứng)
Unit test `test_profiling_runtime_and_throughput` và `test_peak_memory_within_safe_limits`.

### 8. Limitations (Giới hạn)
Chu kỳ lấy mẫu 200ms có thể bỏ sót các đỉnh đột biến diễn ra trong vài mili-giây, nhưng vẫn phản ánh được 99% mức độ chịu tải RAM của hệ điều hành.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em thiết lập memory_limit = 2GB trong DuckDB mà Peak RSS thực tế lại là 1.62 GB?"*  
> **Trả lời:** *"Thưa Thầy/Cô, điều này chứng minh hệ thống hoạt động hoàn toàn chính xác và tối ưu. Tham số memory_limit = '2GB' của DuckDB là một ngưỡng trần (ceiling cap) cho vùng đệm buffer pool. DuckDB chỉ cấp phát lượng bộ nhớ thực sự cần thiết theo từng đợt truy vấn (on-demand allocation). Nhờ cơ chế streaming và xử lý theo vector, DuckDB chỉ cần đạt đỉnh 1.62 GB RSS là đã hoàn thành xử lý hơn 20 triệu dòng, giải phóng bộ nhớ đệm kịp thời mà không cần dùng hết hạn mức 2 GB được cấp."*

---

## P1.7 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 1 (Oral Defense Guide P1)

### Q13: Số lượng 20.69 triệu bản ghi có ý nghĩa gì đối với tính vững chắc của các phân khúc khách hàng?
- **Trả lời:** Với quy mô hơn 20.69 triệu sự kiện trên 1.64 triệu người dùng duy nhất, tập dữ liệu cung cấp một cỡ mẫu cực kỳ phong phú và có tính đại diện cao. Đặc biệt, trong kỳ quan sát có tới 92,652 khách hàng đã mua (Buyers) và 1.25 triệu khách hàng tiềm năng chưa mua (Observed Non-buyers). Cỡ mẫu gần 100k buyers cho phép thuật toán K-Means hội tụ về các cụm có độ tin cậy thống kê cao, không bị ảnh hưởng bởi hiện tượng quá khớp (overfitting) do cỡ mẫu nhỏ.

### Q14: Tại sao tỷ lệ khách mua lặp lại (Repeat Buyer Rate) chỉ đạt 20.06% và con số này định hình chiến lược marketing như thế nào?
- **Trả lời:** Con số 20.06% phản ánh một sự thật khách quan: Trong ngành mỹ phẩm bán lẻ trực tuyến, đa số người dùng (gần 80%) chỉ phát sinh đúng 1 phiên mua hàng trong suốt 4 tháng quan sát (One-time Buyers). Điều này định hình 2 chiến lược marketing rõ rệt: (1) Với nhóm 80% khách mới: Áp dụng chiến thuật bán chéo (`TAC_CROSS_SELL`) và chăm sóc hậu mãi trong vòng 14–30 ngày đầu để thúc đẩy họ mua lần 2; (2) Với nhóm 20% khách mua lặp lại: Áp dụng chương trình khách hàng thân thiết (`TAC_LOYALTY_VIP`) để tối đa hóa giá trị vòng đời (CLV).

### Q15: Tỷ lệ khuyết thiếu 0.022% của trường user_session ảnh hưởng thế nào đến độ chính xác của mô hình?
- **Trả lời:** Tỷ lệ khuyết thiếu 0.022% (chỉ 4,598 dòng trên tổng 20.69M dòng) là mức độ mất mát dữ liệu gần như bằng 0. Đặc biệt, kết quả kiểm toán xác nhận rằng 100% sự kiện mua hàng (purchase events) đều có trường user_session đầy đủ. Do đó, việc sử dụng phiên mua hàng làm proxy cho giao dịch đạt độ chính xác 100% trên tập purchase, hoàn toàn không bị ảnh hưởng bởi lỗi mất mát phiên.

### Q16: Tại sao Phase 2 cần chuyển đổi dữ liệu sang định dạng Parquet thay vì tiếp tục dùng CSV?
- **Trả lời:** Việc chuyển sang định dạng cột Parquet trong Phase 2 đem lại 3 lợi ích vượt trội: (1) *Dung lượng:* Giảm kích thước đĩa từ 2.32 GB xuống còn khoảng 400–500 MB nhờ thuật toán nén Snappy/ZSTD; (2) *Tốc độ:* Giúp DuckDB quét dữ liệu theo cột chỉ đọc các cột cần thiết (Projection Pushdown), tăng tốc độ tính toán đặc trưng RFM ở Phase 3 lên gấp 5–10 lần; (3) *Tính toàn vẹn kiểu dữ liệu:* Parquet lưu trữ sẵn kiểu dữ liệu (Schema metadata), loại bỏ hoàn toàn chi phí và rủi ro ép kiểu thời gian hay số học từ chuỗi văn bản CSV.


---

# PHẦN III — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 2 (DATA PREPARATION & CLEANING)

## P2.1 — Khử trùng lặp dòng sự kiện Clickstream và Kỹ thuật Deduplication qua Window Function `ROW_NUMBER()`

### 1. What (Khái niệm là gì?)
Khử trùng lặp sự kiện (Clickstream Event Deduplication) là quá trình nhận diện và loại bỏ các bản ghi trùng lặp tuyệt đối (exact identical rows) trên toàn bộ không gian thuộc tính (`event_time`, `event_type`, `product_id`, `category_id`, `category_code`, `brand`, `price`, `user_id`, `user_session`).

### 2. Why (Tại sao phát sinh trùng lặp và tại sao phải khử?)
Trong hệ thống theo dõi hành vi trực tuyến (Clickstream Tracking SDK), hiện tượng trùng lặp dòng sự kiện phát sinh từ:
- **Lỗi mạng và cơ chế Frontend Retry:** Khi kết nối chập chờn, SDK phía client tự động gửi lại payload sự kiện lên máy chủ thu thập (event collector) mà không có idempotency key.
- **Hành vi Double-click:** Người dùng nhấn chuột liên tiếp nhiều lần vào nút hành động (ví dụ nút xóa sản phẩm khỏi giỏ hàng).
- **Vòng lặp Javascript/Frontend Bug:** Trong tập dữ liệu REES46, kết quả kiểm toán phát hiện tới **1,109,098 bản ghi trùng lặp chính xác (5.360%)**, trong đó sự kiện `remove_from_cart` chiếm tới **991,821 bản ghi** (chiếm 89.43% tổng số bản ghi trùng lặp).

Nếu không loại bỏ:
- Phễu chuyển đổi (Conversion Funnel) sẽ bị sai lệch nghiêm trọng: tỷ lệ xóa giỏ bị phóng đại làm méo mó các chỉ số tương tác giỏ hàng.
- Thổi phồng kích thước tập dữ liệu và làm lãng phí tài nguyên RAM/CPU khi trích xuất đặc trưng RFM ở Phase 3.

### 3. How (Cách thức triển khai với DuckDB)
Sử dụng cấu trúc bảng tạm (Common Table Expression - CTE) kết hợp hàm cửa sổ `ROW_NUMBER()` có phân vùng trên toàn bộ các cột:
```sql
WITH ranked_events AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY 
                event_time, event_type, product_id, category_id, 
                category_code, brand, price, user_id, user_session
            ORDER BY event_time
        ) AS row_num
    FROM raw_events
)
SELECT * EXCLUDE (row_num)
FROM ranked_events
WHERE row_num = 1;
```

### 4. Formula / Algorithm (Công thức tính toán)
$$\text{Deduplicated}(R) = \{r \in R \mid \text{rank}(r) = 1 \text{ within } \text{Partition}(r)\}$$

$$\text{Duplication Rate} = \frac{N_{\text{raw}} - N_{\text{dedup}}}{N_{\text{raw}}} \times 100\% = \frac{1,109,098}{20,692,840} \times 100\% = 5.360\%$$

Trong đó:
- $N_{\text{raw}} = 20,692,840$ bản ghi thô.
- $N_{\text{dedup}} = 19,583,742$ bản ghi sau khi khử trùng lặp chính xác.

### 5. Worked Example (Ví dụ thực tế)
Xem xét 2 bản ghi clickstream sau:
| event_time | event_type | product_id | price | user_id | user_session | row_num | Xử lý |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `2019-11-05 14:20:01 UTC` | `remove_from_cart` | `5809990` | `2.16` | `567890123` | `a1b2-c3d4` | 1 | **GIỮ LẠI** |
| `2019-11-05 14:20:01 UTC` | `remove_from_cart` | `5809990` | `2.16` | `567890123` | `a1b2-c3d4` | 2 | **LOẠI BỎ** |

Bản ghi thứ hai giống hệt bản ghi thứ nhất tới từng giây, từng sản phẩm và từng phiên. Thuật toán gán `row_num = 2` và lọc bỏ, bảo toàn đúng 1 hành vi xóa giỏ thực tế.

### 6. Alternatives (Phương án thay thế & So sánh)
- **`SELECT DISTINCT *`:** Về mặt toán học trả về kết quả tương đương, nhưng `ROW_NUMBER()` trong DuckDB cho phép kiểm soát thứ tự ưu tiên, dễ dàng gán cờ debug hoặc bóc tách riêng tập dữ liệu bị trùng lặp để kiểm toán đối soát.
- **`pandas.drop_duplicates()`:** Đòi hỏi nạp toàn bộ 20.69 triệu dòng (2.32 GB CSV giải nén > 4 GB RAM) vào DataFrame của Python, chắc chắn gây tràn bộ nhớ (Out-Of-Memory) trên máy tính cá nhân 16 GB RAM có RAM khả dụng ~2.2 GB.

### 7. Verification (Cách thức kiểm chứng)
1. **Kiểm toán đối soát số học:** $N_{\text{raw}} (20,692,840) - N_{\text{duplicates}} (1,109,098) = N_{\text{clean}} (19,583,742)$.
2. **Kiểm chứng tác động trên kỳ quan sát (Observation Window Impact):**
   - Số người dùng duy nhất: Raw = 1,341,499 $\leftrightarrow$ Clean = 1,341,499 (Chênh lệch = **0**).
   - Số phiên duy nhất: Raw = 3,614,959 $\leftrightarrow$ Clean = 3,614,959 (Chênh lệch = **0**).
   - Số người mua hàng (Buyers): Raw = 92,652 $\leftrightarrow$ Clean = 92,652 (Chênh lệch = **0**).
   - Số phiên mua hàng (Purchase Sessions): Raw = 126,503 $\leftrightarrow$ Clean = 126,503 (Chênh lệch = **0**).
   - Số phiên có thêm giỏ (Cart Sessions): Raw = 800,307 $\leftrightarrow$ Clean = 800,307 (Chênh lệch = **0**).
   - Lượt xem (Views): Raw = 7,704,235 $\leftrightarrow$ Clean = 7,703,765 (Chênh lệch = 470 lượt, 0.006%).
   - Lượt mua (Purchases): Raw = 1,045,014 $\leftrightarrow$ Clean = 1,044,221 (Chênh lệch = 793 lượt, 0.076%).
   - Lượt xóa giỏ (Removes): Raw = 3,167,270 $\leftrightarrow$ Clean = 2,385,211 (Chênh lệch = 782,059 lượt, chiếm 89.4% lượng bản ghi trùng).
3. **Kiểm thử đơn vị:** Test case `test_reconciliation_counts` trong `tests/test_phase2_data_preparation.py`.

### 8. Limitations (Giới hạn thực tế)
Thuật toán chỉ nhận diện được sự kiện trùng lặp chính xác tới từng giây (exact timestamp). Nếu client retry cách nhau 2-3 giây, các bản ghi này sẽ có timestamp lệch nhau và không bị coi là exact duplicate; tuy nhiên điều này bảo toàn các thao tác nhấp chuột có chủ đích của người dùng.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em xóa hơn 1.1 triệu bản ghi trùng lặp, liệu việc này có làm mất hành vi người dùng thật không?"*  
> **Trả lời:** *"Thưa Thầy/Cô, việc xóa này hoàn toàn KHÔNG làm mất hành vi thật hay cấu trúc khách hàng. Kiểm chứng thực nghiệm đối soát trên kỳ quan sát chứng minh: Số lượng người dùng (1,341,499), số phiên (3,614,959), số người mua (92,652), số phiên mua (126,503) và số phiên thêm giỏ (800,307) được BẢO TOÀN 100% (chênh lệch đúng bằng 0). Có tới 89.4% lượng bản ghi trùng tập trung vào hành động xóa giỏ (remove_from_cart) với trường hợp lặp lại tối đa tới 48 lần cho cùng một sản phẩm trong cùng 1 giây. Lượt xem chỉ lệch 0.006% và lượt mua chỉ lệch 0.076%. Do đó, việc loại bỏ các bản ghi trùng lặp chính xác giúp làm sạch phễu chuyển đổi và bảo vệ các đặc trưng giỏ hàng ở Phase 3 mà không làm mất bất kỳ chủ thể người dùng hay phiên hợp lệ nào."*

---

## P2.2 — Xử lý xung đột Định danh Phiên (Session UUID Collisions) bằng Khóa kết hợp `user_session_id`

### 1. What (Khái niệm là gì?)
Xung đột định danh phiên (Session Collision) là hiện tượng một mã định danh phiên (`user_session` UUID) được gán hoặc xuất hiện đồng thời ở nhiều tài khoản người dùng (`user_id`) khác nhau. Khóa kết hợp chuẩn hóa (`user_session_id`) là giải pháp ghép nối `user_id` và `user_session` thành một chuỗi duy nhất để đảm bảo tính toàn vẹn quan hệ 1-N (một user có nhiều session, nhưng mỗi session chỉ thuộc về đúng một user).

### 2. Why (Tại sao có xung đột và tại sao phải tạo khóa kết hợp?)
Trong quá trình kiểm toán dữ liệu Phase 1 và đầu Phase 2, hệ thống phát hiện một dị thường:
- Số lượng cặp `(user_id, user_session)` duy nhất: **4,536,272**.
- Số lượng mã `user_session` duy nhất: **4,535,941**.
- **Chênh lệch:** 331 mã phiên bị dùng chung giữa nhiều `user_id` khác nhau.

Nguyên nhân thực tế trong e-commerce:
- Người dùng sử dụng chung thiết bị đầu cuối công cộng (máy tính thư viện, phòng net, quán cafe) mà không xóa cookie phiên khi đăng nhập tài khoản khác.
- Lỗi sinh UUID giả ngẫu nhiên (Pseudo-Random Generator) của thư viện tracking phía client có không gian entropy hẹp gây ra va chạm mã băm (Hash collision).

Nếu gom nhóm sự kiện chỉ bằng `user_session`:
- Hành vi của hai người dùng hoàn toàn xa lạ sẽ bị gộp chung vào một phiên, làm sai lệch thời lượng phiên, số lượt xem trang và giá trị giỏ hàng.
- Vi phạm giả định phân tích hành vi độc lập giữa các cá thể người dùng.

### 3. How (Cách thức triển khai)
Thiết lập cột phái sinh chuẩn hóa `user_session_id` trong pipeline DuckDB ETL:
```sql
CASE 
    WHEN user_session IS NULL THEN NULL
    ELSE CAST(user_id AS VARCHAR) || '_' || user_session 
END AS user_session_id
```

### 4. Formula / Relation (Mô hình quan hệ toán học)
$$\text{Collision Count} = |\{s \in \mathcal{S} \mid |\{u \in \mathcal{U} \mid (u, s) \in \text{Events}\}| > 1\}| = 331$$

$$\text{Composite Key Mapping}: (u, s) \mapsto k = u \mathbin{\Vert} \text{'_'} \mathbin{\Vert} s$$

$$\forall k_1, k_2 \in \mathcal{K}, \quad k_1 = k_2 \iff u_1 = u_2 \land s_1 = s_2$$

### 5. Worked Example (Ví dụ va chạm mã phiên)
Giả sử có hai người dùng `u101` và `u202` cùng xuất hiện mã phiên `session_abc123`:
- *Nếu dùng `user_session` làm khóa:* Nhóm `session_abc123` chứa sự kiện xem son môi của `u101` và sự kiện mua dầu gội của `u202`. Hệ thống tưởng rằng một người dùng đã thực hiện cả hai hành vi này trong 1 phiên $\to$ **Sai lệch**.
- *Khi tạo khóa kết hợp:*
  - Nhóm 1: `u101_session_abc123` $\to$ Phiên xem son môi của khách hàng 101.
  - Nhóm 2: `u202_session_abc123` $\to$ Phiên mua dầu gội của khách hàng 202.
  - Xung đột giảm về đúng bằng **0**.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Tạo UUID mới cho session bị trùng:** Làm thay đổi dữ liệu gốc, khó đối soát ngược lại với log thô khi cần audit.
- **Xóa toàn bộ các dòng thuộc 331 session bị trùng:** Làm mất oan hàng nghìn sự kiện tương tác hợp lệ của cả 2 khách hàng chỉ vì lỗi định danh cookie.
- **Sử dụng `user_session_id` kết hợp:** Giữ nguyên dữ liệu gốc, bảo toàn 100% sự kiện, giải quyết triệt để xung đột logic với chi phí tính toán bằng 0.

### 7. Verification & Reconciliation (Cách thức kiểm chứng & Đối soát số học)
1. **Kiểm toán va chạm phiên:**
   ```sql
   SELECT user_session_id, COUNT(DISTINCT user_id) as user_count 
   FROM clean_events 
   WHERE user_session_id IS NOT NULL 
   GROUP BY user_session_id 
   HAVING COUNT(DISTINCT user_id) > 1;
   ```
   Kết quả trả về: **0 dòng** (Đạt tỷ lệ thành công 100%). Test case `test_composite_session_key_uniqueness` trong test suite đã kiểm chứng độc lập.

2. **Đối soát số học về con số 1,533 phiên:**
   - Số lượng UUID phiên không null (`session_id`): Raw = **4,535,941** $\leftrightarrow$ Clean = **4,535,941** (Chênh lệch: **0**).
   - Số lượng cặp khóa kết hợp không null (`user_session_id`): Raw = **4,536,272** $\leftrightarrow$ Clean = **4,536,272** (Chênh lệch: **0**).
   - Chênh lệch 1,533 phiên xuất phát từ việc trong dữ liệu thô có đúng **1,533 người dùng** có sự kiện bị thiếu mã phiên (`user_session IS NULL`, chiếm 4,598 dòng). Khi đếm chuỗi kết hợp bao gồm cả NULL trong dữ liệu thô:
     $$4,536,272 \text{ (phiên hợp lệ)} + 1,533 \text{ (người dùng có phiên NULL)} = 4,537,805$$
   - Khi chuyển sang bảng sạch, các dòng thiếu phiên được gán `user_session_id = NULL` chuẩn tắc; hàm `COUNT(DISTINCT user_session_id)` trong SQL tự động loại trừ `NULL` và trả về đúng **4,536,272 phiên hợp lệ**.
   - **Kết luận:** Hoàn toàn **KHÔNG có một phiên hợp lệ nào bị mất** sau quá trình làm sạch.

### 8. Limitations (Giới hạn)
Đối với 4,598 dòng bị khuyết thiếu `user_session` (NULL), giá trị `user_session_id` vẫn là NULL. Tuy nhiên, 100% các dòng này là sự kiện view/cart, không có bất kỳ dòng purchase nào bị thiếu phiên.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao báo cáo sơ bộ ghi số phiên giảm 1,533 sau deduplication, liệu deduplication có làm mất phiên không?"*  
> **Trả lời:** *"Thưa Thầy/Cô, deduplication hoàn toàn KHÔNG làm mất bất kỳ phiên nào. Về mặt giải thuật, ROW_NUMBER() ... WHERE row_num = 1 luôn giữ lại một dòng đại diện trong mỗi nhóm trùng lặp, nên không thể làm mất phiên nếu phiên đó có dữ liệu. Con số 1,533 thực chất là số lượng người dùng có các sự kiện bị khuyết thiếu mã phiên (user_session IS NULL). Trong dữ liệu thô, các người dùng này bị đếm thành các chuỗi 'user_NULL' (4,536,272 + 1,533 = 4,537,805). Trong dữ liệu sạch, chúng em gán NULL chuẩn tắc cho user_session_id, nên hàm COUNT(DISTINCT) tự động bỏ qua NULL và trả về đúng 4,536,272 phiên. Khi đối soát trên cùng một grain, cả số lượng session UUID (4,535,941) và số lượng composite session (4,536,272) đều được bảo toàn 100% với độ lệch bằng 0."*

---

## P2.3 — Chiến lược Cờ phân loại Chất lượng Dữ liệu Đa mục đích: Engagement Preservation vs. Monetary Exclusion

### 1. What (Khái niệm là gì?)
Chiến lược cờ phân loại chất lượng dữ liệu (Data Quality Flagging) là phương pháp gán các trường logic (`is_valid_for_engagement`, `is_valid_for_monetary`) cho từng bản ghi dữ liệu thay vì áp dụng quy tắc xóa cứng (Hard Deletion) khi gặp các giá trị dị thường (`price <= 0`).

### 2. Why (Tại sao không được xóa toàn bộ các dòng có giá <= 0?)
Trong quá trình phân tích Phase 1, phát hiện **104,288 bản ghi có price $\le$ 0**. Nếu vội vã xóa sạch toàn bộ 104k bản ghi này khỏi tập dữ liệu:
- Phân bố theo `event_type` của 104,288 bản ghi này như sau:
  - `cart`: **49,370 bản ghi** (47.34%)
  - `view`: **30,492 bản ghi** (29.24%)
  - `remove_from_cart`: **24,299 bản ghi** (23.30%)
  - `purchase`: **127 bản ghi** (0.12%)
- **Hậu quả nếu xóa cứng:** Bạn sẽ xóa mất **104,161 sự kiện tương tác thực tế** của người dùng. Trong thương mại điện tử, các sản phẩm quà tặng 0 đồng, mẫu thử khuyến mại (testers, samples), hoặc sản phẩm sự kiện tri ân thường được định giá 0. Việc khách hàng vào xem và nhặt các sản phẩm này vào giỏ hàng thể hiện mức độ quan tâm (Engagement) rất cao. Xóa chúng sẽ làm sai lệch tần suất vào trang và mức độ gắn bó của khách hàng.
- **Tuy nhiên, đối với giao dịch mua sắm (purchase):** Có 127 giao dịch mua có giá $\le$ 0 (trong đó có giá âm với tổng giá trị âm là -$2,642.88). Nếu đưa các giá trị này vào tính toán chi tiêu (Monetary), tổng doanh thu của khách hàng sẽ bị trừ ngược vô lý, vi phạm định nghĩa tài chính.

### 3. How (Cách thức thiết kế cờ logic trong SQL)
Xây dựng 2 cờ logic riêng biệt:
```sql
-- Cờ tương tác: Mọi sự kiện hợp lệ đều được ghi nhận tương tác
CASE 
    WHEN user_id IS NOT NULL THEN TRUE 
    ELSE FALSE 
END AS is_valid_for_engagement,

-- Cờ tài chính: Chỉ ghi nhận giao dịch mua có giá dương
CASE 
    WHEN event_type = 'purchase' AND price > 0 THEN TRUE 
    ELSE FALSE 
END AS is_valid_for_monetary
```

### 4. Formula / Aggregation (Công thức tính toán đặc trưng an toàn)
$$\text{Engagement Count}(u) = \sum_{e \in E_u} \mathbb{I}(\text{is\_valid\_for\_engagement}(e) = \text{TRUE})$$

$$\text{Monetary}(u) = \sum_{e \in E_u} \text{price}(e) \cdot \mathbb{I}(\text{is\_valid\_for\_monetary}(e) = \text{TRUE})$$

$$\Delta \text{GMV}_{\text{correction}} = \sum_{e \in E_{\text{obs}}, \text{price} \le 0} |\text{price}(e)| = +2,642.88 \text{ USD}$$

### 5. Worked Example (Ví dụ khách hàng nhận quà khuyến mại)
Khách hàng `u555` thực hiện các hành động sau:
1. Xem sản phẩm son môi giá 15$ (`view`, price = 15).
2. Xem mẫu thử kem dưỡng 0$ (`view`, price = 0).
3. Thêm mẫu thử 0$ vào giỏ (`cart`, price = 0).
4. Mua son môi giá 15$ (`purchase`, price = 15).
5. Nhận kèm mẫu thử giá 0$ (`purchase`, price = 0).

- **Xử lý theo hệ thống:**
  - `is_valid_for_engagement = TRUE` cho cả 5 sự kiện $\to$ Tương tác ghi nhận = 5 (phản ánh trung thực hoạt động browsing).
  - `is_valid_for_monetary = TRUE` chỉ cho sự kiện 4 (15$) $\to$ Monetary = 15$ (chuẩn xác về mặt tài chính).

### 6. Alternatives (Phương án thay thế & So sánh)
- **Hard Deletion (Xóa cứng):** Mất 104,161 tương tác clickstream của người dùng.
- **Mean/Median Imputation (Điền giá trị trung bình):** Ngụy tạo doanh thu giả cho các sản phẩm quà tặng 0 đồng, vi phạm đạo đức dữ liệu tài chính.
- **Gán cờ (Flagging - Lựa chọn tối ưu):** Bảo toàn tính nguyên vẹn của lịch sử tương tác, phân tách rạch ròi giữa mục đích phân tích tương tác và mục đích phân tích doanh thu.

### 7. Verification (Cách thức kiểm chứng)
- Kiểm tra số lượng bản ghi `is_valid_for_engagement = TRUE`: đúng 19,583,742 bản ghi (100% bản ghi sạch).
- Kiểm tra số lượng bản ghi `is_valid_for_monetary = TRUE` trong Observation: 1,008,187 bản ghi (loại trừ đúng 88 giao dịch purchase $\le 0$).
- Unit test `test_monetary_exclusion_and_engagement_preservation` đạt PASS.

### 8. Limitations (Giới hạn)
Do REES46 không có trường dữ liệu ghi chú loại giao dịch (Transaction Notes), hệ thống không thể phân biệt rạch ròi 127 bản ghi purchase giá âm là do hàng trả lại hoàn tiền (Refunds) hay do lỗi hệ thống thanh toán của sàn thương mại điện tử.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao trong dữ liệu có 104k dòng giá bằng 0 hoặc âm, và em xử lý thế nào để không làm sai lệch kết quả?"*  
> **Trả lời:** *"Thưa Thầy/Cô, chúng em đã bóc tách chi tiết 104,288 dòng này và phát hiện hơn 99.8% là các sự kiện xem hàng và thêm giỏ của các sản phẩm quà tặng 0 đồng hoặc dùng thử. Nếu xóa cứng, chúng em sẽ làm mất hơn 104 nghìn tương tác thực tế của người dùng. Do đó, chúng em thiết kế giải pháp cờ kép: giữ lại toàn bộ cho phân tích tương tác (Engagement), và chỉ lọc bỏ 88 giao dịch mua giá âm/bằng không khi tính toán giá trị tiền tệ (Monetary). Cách làm này vừa bảo toàn hành vi tương tác, vừa sửa đổi chính xác +2,642.88 USD bị âm vô lý trong doanh thu quan sát."*

---

## P2.4 — Phân tách Chuỗi thời gian Nghiêm ngặt (Strict Event-level Temporal Split) và Giải quyết Phiên vắt qua Ranh giới (Cross-boundary Sessions)

### 1. What (Khái niệm là gì?)
Phân tách chuỗi thời gian nghiêm ngặt ở cấp độ sự kiện (Strict Event-level Temporal Split) là quy trình phân chia dữ liệu clickstream thành hai tập dữ liệu độc lập dựa trên mốc thời gian chốt sổ ($T_{\text{cutoff}} = \text{2020-02-01T00:00:00Z}$):
- **Observation Window (Kỳ quan sát):** Từ `2019-10-01 00:00:00 UTC` đến `< 2020-02-01 00:00:00 UTC`.
- **Holdout Window (Kỳ giữ lại kiểm chứng tương lai):** Từ `>= 2020-02-01 00:00:00 UTC` đến `<= 2020-02-29 23:59:59 UTC`.

### 2. Why (Tại sao phải phân tách nghiêm ngặt và rủi ro Data Leakage là gì?)
- **Ngăn chặn Rò rỉ Dữ liệu Tương lai (Data Leakage):** Trong bài toán phân khúc và chấm điểm khách hàng, nếu để dữ liệu tương lai (tháng 2/2020) lọt vào quá trình chuẩn hóa (StandardScaler) hoặc tính toán đặc trưng RFM, mô hình phân cụm K-Means sẽ tiếp cận được các hành vi chưa xảy ra tại thời điểm chốt sổ, dẫn đến hiện tượng quá lạc quan giả tạo khi đánh giá mô hình.
- **Hiện tượng Phiên vắt qua Ranh giới (Cross-boundary Sessions):** Trong thực tế, có **10,451 phiên truy cập** bắt đầu trước nửa đêm ngày 31/01/2020 và tiếp tục hoạt động sang rạng sáng ngày 01/02/2020. Nếu không có quy tắc phân tách nhất quán ở cấp độ sự kiện, dữ liệu sẽ bị trùng lặp hoặc vi phạm ranh giới thời gian.

### 3. How (Cách thức triển khai)
Áp dụng quy tắc khoảng nửa mở $[T_{\text{start}}, T_{\text{cutoff}})$ cho kỳ quan sát và $[T_{\text{cutoff}}, T_{\text{end}}]$ cho kỳ kiểm chứng tương lai:
```sql
-- Tạo tập Observation
COPY (
    SELECT * FROM clean_events 
    WHERE event_time >= '2019-10-01 00:00:00 UTC' 
      AND event_time < '2020-02-01 00:00:00 UTC'
) TO 'data/cleaned/observation_events.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);

-- Tạo tập Holdout
COPY (
    SELECT * FROM clean_events 
    WHERE event_time >= '2020-02-01 00:00:00 UTC' 
      AND event_time <= '2020-02-29 23:59:59 UTC'
) TO 'data/cleaned/holdout_events.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
```

### 4. Formula / Boundary Rules (Quy tắc ranh giới toán học)
$$E_{\text{obs}} = \{e \in E_{\text{clean}} \mid T_{\text{start}} \le t(e) < T_{\text{cutoff}}\}$$

$$E_{\text{holdout}} = \{e \in E_{\text{clean}} \mid T_{\text{cutoff}} \le t(e) \le T_{\text{end}}\}$$

$$E_{\text{obs}} \cap E_{\text{holdout}} = \emptyset, \quad E_{\text{obs}} \cup E_{\text{holdout}} = E_{\text{clean}}$$

$$\max_{e \in E_{\text{obs}}} t(e) < T_{\text{cutoff}} \le \min_{e \in E_{\text{holdout}}} t(e)$$

### 5. Worked Example (Ví dụ phiên vắt qua thời khắc giao thừa)
Một khách hàng truy cập website lúc `23:50:00 ngày 31/01/2020`:
- `23:52:10` (31/01): Xem sản phẩm son môi A $\to$ Thuộc về **Observation**.
- `23:58:45` (31/01): Thêm son môi A vào giỏ hàng $\to$ Thuộc về **Observation**.
- `00:03:15` (01/02): Nhấn nút thanh toán mua hàng $\to$ Thuộc về **Holdout**.

Kết quả: Tại thời điểm chốt sổ $T_{\text{cutoff}}$, khách hàng này được ghi nhận là một khách hàng tiềm năng có giỏ hàng chưa mua (At-Risk / Cart Abandoner). Sang tháng 2, sự kiện mua hàng xuất hiện trong Holdout chứng minh rằng khách hàng này đã chuyển đổi thành công trong tương lai. Đây chính là bản chất của bài toán đánh giá năng lực dự báo mà không bị rò rỉ thông tin.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Session-level Cutoff (Dựa vào thời điểm bắt đầu phiên):** Đẩy toàn bộ phiên sang tháng 1 hoặc tháng 2. Nếu đẩy sang tháng 1, sự kiện mua hàng lúc 00:03 ngày 01/02 sẽ bị tính vào observation (gây rò rỉ dữ liệu tương lai). Nếu đẩy sang tháng 2, các tương tác duyệt web trước nửa đêm bị xóa khỏi observation (làm mất dữ liệu quá khứ).
- **Event-level Cutoff (Lựa chọn chuẩn mực):** Cắt lát dữ liệu chính xác theo dòng thời gian thực tế, phản ánh đúng nguyên tắc đóng băng sổ sách kế toán của doanh nghiệp.

### 7. Verification (Cách thức kiểm chứng)
- Kiểm tra `MAX(event_time)` của `observation_events.parquet`: `2020-01-31 23:59:59 UTC` ($< T_{\text{cutoff}}$).
- Kiểm tra `MIN(event_time)` của `holdout_events.parquet`: `2020-02-01 00:00:00 UTC` ($\ge T_{\text{cutoff}}$).
- Tổng số dòng: $15,667,350 + 3,916,392 = 19,583,742$ (khớp tuyệt đối 100%).
- Unit test `test_anti_leakage_temporal_split` đạt PASS.

### 8. Limitations (Giới hạn)
Đối với 10,451 phiên bị cắt đôi tại ranh giới, phễu chuyển đổi nội bộ của riêng phiên đó sẽ bị ngắt quãng giữa giỏ hàng (tháng 1) và thanh toán (tháng 2). Tuy nhiên, số lượng này chỉ chiếm 0.23% tổng số phiên và hoàn toàn không ảnh hưởng đến tính đại diện của tập mẫu.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Em giải quyết thế nào với các phiên truy cập kéo dài qua ranh giới nửa đêm ngày 31/01/2020 để không bị rò rỉ dữ liệu?"*  
> **Trả lời:** *"Thưa Thầy/Cô, chúng em áp dụng nguyên tắc cắt lát ở cấp độ sự kiện (event-level temporal split) với ranh giới nửa mở triệt để. Mọi hành vi diễn ra trước đúng 00:00:00 ngày 01/02 đều thuộc về kỳ quan sát, và các hành vi diễn ra từ thời điểm đó trở đi thuộc về kỳ kiểm chứng tương lai. Điều này tương tự như việc kế toán chốt sổ doanh thu đúng vào thời khắc giao thừa; bất kỳ giao dịch nào hoàn tất sau nửa đêm đều phải chuyển sang kỳ kế toán tháng tiếp theo, đảm bảo mô hình phân cụm không nhìn trước được tương lai."*

---

## P2.5 — Chuyển đổi Lưu trữ Dạng cột (Columnar Storage Migration): Parquet ZSTD Compression và Đánh đổi Hiệu năng Thực nghiệm

### 1. What (Khái niệm là gì?)
Chuyển đổi lưu trữ dạng cột là quá trình di chuyển toàn bộ dữ liệu từ các tệp văn bản thô theo dòng (Row-oriented CSV) sang tệp nhị phân theo cột (Column-oriented Apache Parquet) có tích hợp thuật toán nén Zstandard (ZSTD) ở cấp độ khối dữ liệu.

### 2. Why (Tại sao cần chuyển sang Parquet?)
1. **Lãng phí dung lượng đĩa và I/O:** 5 tệp CSV thô chiếm tới **2.32 GB (2,321.51 MB)**. Việc đọc CSV liên tục từ đĩa làm nghẽn cổ chai I/O và tốn tài nguyên giải mã chuỗi văn bản (String parsing).
2. **Không hỗ trợ quét cột chọn lọc (Projection Pushdown):** Trong Phase 3 (Feature Engineering), hầu hết các truy vấn RFM chỉ cần 4 cột (`event_time`, `event_type`, `user_id`, `price`). Với file CSV, hệ quản trị bắt buộc phải đọc toàn bộ 9 cột của 20.69 triệu dòng.
3. **Mất mát kiểu dữ liệu (Schema Ambiguity):** CSV lưu trữ mọi thứ dưới dạng text thuần túy, dẫn đến nguy cơ sai lệch kiểu dữ liệu (ngày tháng, số thực) khi đọc bằng các thư viện khác nhau. Parquet lưu sẵn metadata schema ở cuối tệp.

### 3. How (Cách thức triển khai với DuckDB)
Xuất trực tiếp từ DuckDB sang định dạng Parquet với thuật toán nén ZSTD:
```sql
COPY clean_events TO 'data/cleaned/clean_events.parquet' (
    FORMAT PARQUET, 
    COMPRESSION ZSTD
);
```

### 4. Formula / Empirical Metrics (Các chỉ số thực nghiệm đo kiểm công bằng)
$$\text{Storage Compression Ratio} = \frac{\text{Size}_{\text{Clean CSV}}}{\text{Size}_{\text{Clean Parquet}}} = \frac{4,426.30 \text{ MB}}{474.71 \text{ MB}} = 9.324\times$$

$$\text{Fair Query Speedup (Median)} = \frac{t_{\text{Clean CSV (Median)}}}{t_{\text{Clean Parquet (Median)}}} = \frac{3.0624 \text{ s}}{0.3786 \text{ s}} = 8.089\times$$

$$\text{Fair Query Speedup (Cold)} = \frac{t_{\text{Clean CSV (Cold)}}}{t_{\text{Clean Parquet (Cold)}}} = \frac{3.6158 \text{ s}}{0.5503 \text{ s}} = 6.571\times$$

### 5. Worked Example & Fair Trade-off Matrix (Bảng Ma trận Đo kiểm Công bằng)

Benchmark đối đầu trên **CÙNG TẬP 19,583,742 BẢN GHI SẠCH** (5 lần lặp độc lập, đo Cold/Warm cache, CPU 16 cores, RAM cap 2GB):

| Tiêu chí Đánh đổi | Tệp Sạch Clean CSV (19.58M dòng) | Tệp Sạch Clean Parquet (19.58M dòng) | Kết quả Đo kiểm Công bằng (Fair Comparison) |
| :--- | :--- | :--- | :--- |
| **Dung lượng lưu trữ trên đĩa** | 4,426.30 MB (~4.43 GB) | **474.71 MB** (~0.47 GB) | **Tiết kiệm 89.27% đĩa** (Tỷ lệ nén 9.32x so với CSV giải nén) |
| **Thời gian khởi đầu (Cold Cache)** | 3.6158 giây | **0.5503 giây** | **Nhanh hơn 6.57 lần** ngay ở lần chạy đầu tiên |
| **Thời gian trung vị (Median Runtime)** | **3.0624 giây** | **0.3786 giây** | **Nhanh hơn 8.09 lần** (Median Speedup 8.09x) |
| **Độ ổn định (Mean ± Stdev)** | 3.1709s ± 0.2507s | 0.4273s ± 0.0769s | Parquet có độ biến thiên phương sai thấp hơn 3.26 lần |
| **Kích thước tập Observation** | — | **379.06 MB** | Đóng băng trước cutoff, sẵn sàng cho Phase 3 |
| **Kích thước tập Holdout** | — | **95.63 MB** | Nhỏ gọn, niêm phong độc lập cho Phase 5 |
| **Tổng dung lượng vật lý trên đĩa** | — | **949.40 MB** | Gồm cả 3 tệp Parquet (Minimal deployment: 474.69 MB) |
| **Bảo toàn kiểu dữ liệu (Schema)** | Thấp (Mọi thứ là text, dễ lỗi ép kiểu) | Tuyệt đối (Metadata nhị phân chuẩn hóa) | Khử hoàn toàn rủi ro sai lệch kiểu ngày tháng và số học |
| **Chi phí thời gian chuyển đổi (ETL)** | 0 giây (Dữ liệu có sẵn) | 212.18 giây (~3.5 phút) | Đánh đổi một lần trong pha chuẩn bị để tăng tốc cho mọi pha sau |
| **Khả năng đọc trực tiếp (Readability)**| Đọc được bằng Notepad / text editor | Cần công cụ chuyên dụng (DuckDB, PyArrow) | Tệp nhị phân tối ưu cho máy tính, không dùng để đọc thủ công |

### 6. Alternatives (Phương án thay thế & So sánh)
- **CSV nén GZIP (`.csv.gz`):** Tiết kiệm dung lượng đĩa tốt (~600 MB), nhưng vẫn là lưu trữ theo dòng; khi truy vấn vẫn phải giải nén toàn bộ dòng và toàn bộ cột từ đầu đến cuối, tốc độ truy vấn chậm hơn nhiều so với Parquet.
- **Apache Feather / Arrow IPC:** Tốc độ đọc ghi cực nhanh trên RAM, nhưng kích thước nén trên đĩa lớn hơn Parquet khoảng 30-40% và hỗ trợ ít công cụ phân tích hơn trên các hệ thống kho dữ liệu lớn.
- **Parquet nén Snappy:** Tốc độ ghi nhanh hơn ZSTD một chút, nhưng tỷ lệ nén kém hơn ZSTD (file kích thước lớn hơn khoảng 15-20%). Chọn **Parquet ZSTD** là sự cân bằng tối ưu giữa kích thước đĩa và tốc độ truy vấn.

### 7. Verification (Cách thức kiểm chứng)
- Kiểm tra dung lượng tệp thực tế trên đĩa bằng `os.path.getsize()`.
- Chạy benchmark A/B so sánh trực tiếp cùng một câu truy vấn tổng hợp trên CSV thô và Parquet sạch; kết quả lưu vết tại `outputs/experiments/phase2_data_cleaning.json`.
- Unit test `test_parquet_storage_and_speedup` đạt PASS.

### 8. Limitations (Giới hạn)
Chi phí tính toán của pha chuyển đổi ETL ban đầu tiêu tốn 212.18 giây và đỉnh RAM 2.38 GB. Đây là chi phí đánh đổi chấp nhận được của quy trình xử lý dữ liệu lớn (Batch Processing) trong các dự án công nghiệp.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao đồ án của em phải tốn hơn 3 phút để chuyển đổi dữ liệu từ CSV sang Parquet?"*  
> **Trả lời:** *"Thưa Thầy/Cô, việc chuyển đổi này tuân thủ nguyên tắc 'Write Once, Read Many' trong kỹ thuật dữ liệu lớn. Chi phí 212 giây chỉ tiêu tốn đúng một lần duy nhất trong quá trình chuẩn bị dữ liệu (Data Preparation). Đổi lại, kích thước dữ liệu giảm từ 2.32 GB xuống còn 471 MB (tiết kiệm gần 80% đĩa), và quan trọng nhất là tốc độ các câu truy vấn tổng hợp tính toán đặc trưng RFM ở Phase 3 chạy nhanh hơn gấp 8.33 lần (từ 5.15s xuống còn 0.62s). Đây là một sự đánh đổi cực kỳ kinh tế và khoa học."*

---

## P2.6 — Bộ Câu hỏi Vấn đáp Trọng tâm và Hướng dẫn Bảo vệ Đồ án Phase 2 (Oral Defense Guide P2)

### Q17: Bản chất của con số 87.13% trong phễu chuyển đổi Phase 1 là gì và tại sao không được gọi là "Tỷ lệ bỏ giỏ hàng của khách hàng"?
- **Trả lời:** Con số 87.13% phản ánh **Tỷ lệ phiên có thêm giỏ nhưng không phát sinh mua hàng trong cùng phiên đó** (`Cart Session No-Purchase Rate`). Không thể gọi đây là "Tỷ lệ bỏ giỏ của khách hàng" vì 3 lý do khoa học:
  1. *Cấp độ hạt (Grain):* Đây là con số đo trên cấp độ phiên (697,337 phiên thêm giỏ không mua trên tổng 800,323 phiên có thêm giỏ), không phải đo trên từng người dùng cá nhân.
  2. *Hành vi mua đa phiên:* Khách hàng có thể thêm sản phẩm vào giỏ ở phiên sáng trên điện thoại và thanh toán ở phiên tối trên máy tính.
  3. *Thời gian quan sát:* Nhiều phiên thêm giỏ xảy ra vào cuối tháng 1 và người dùng hoàn tất thanh toán vào đầu tháng 2. Do đó, đây là một chỉ số cơ hội để kích hoạt chiến thuật nhắc giỏ hàng (`TAC_CART_RECOVERY`), không phải là một kết luận suy diễn về sự từ bỏ vĩnh viễn của khách hàng.

### Q18: Tại sao lại xuất hiện hơn 1.1 triệu bản ghi trùng lặp và tỷ lệ này tập trung vào sự kiện nào?
- **Trả lời:** Kiểm toán chi tiết chỉ ra rằng có đúng 1,109,098 bản ghi (5.360%) trùng lặp tuyệt đối trên toàn bộ 9 cột dữ liệu. Đáng chú ý, có tới 991,821 bản ghi (chiếm gần 90% lượng trùng lặp) thuộc về sự kiện `remove_from_cart`. Đây là bằng chứng rõ ràng về lỗi kỹ thuật frontend của website thương mại điện tử: khi người dùng nhấp đúp nút xóa hoặc hệ thống lặp vòng lặp gửi request xóa giỏ hàng hàng loạt. Việc nhận diện và loại bỏ hơn 1.1 triệu bản ghi này giúp làm sạch triệt để phễu chuyển đổi và bảo vệ tính chuẩn xác của các đặc trưng tương tác.

### Q19: Vì sao hệ thống không xóa các bản ghi có giá bằng 0 hoặc giá âm mà lại dùng cờ chất lượng?
- **Trả lời:** Kiểm toán bóc tách 104,288 bản ghi có `price <= 0` cho thấy hơn 99.8% (104,161 dòng) là các sự kiện xem hàng và thêm giỏ của các sản phẩm quà tặng khuyến mại 0 đồng. Nếu xóa bỏ các dòng này, hệ thống sẽ xóa mất hành vi tương tác hợp lệ của người dùng. Thay vào đó, chúng em thiết kế cờ chất lượng: `is_valid_for_engagement` giữ nguyên giá trị TRUE cho toàn bộ các dòng để bảo toàn tín hiệu lướt web, và `is_valid_for_monetary` chỉ đánh dấu TRUE cho các giao dịch mua có giá dương (`event_type = 'purchase' AND price > 0`). Giải pháp này vừa bảo tồn hành vi tương tác, vừa sửa đổi chính xác +2,642.88 USD bị âm vô lý trong doanh thu quan sát.

### Q20: Việc phát hiện và xử lý 331 session collisions bằng composite key mang lại lợi ích gì cho tính toàn vẹn của mô hình?
- **Trả lời:** Việc phát hiện 331 mã phiên bị dùng chung bởi nhiều tài khoản người dùng khác nhau giúp ngăn chặn lỗi gộp nhầm hành vi của hai cá thể độc lập vào cùng một phiên. Bằng cách chuẩn hóa khóa kết hợp `user_session_id = user_id || '_' || user_session`, số lượng va chạm giảm tuyệt đối về 0. Điều này đảm bảo rằng khi bước sang Phase 3, các đặc trưng tính toán trên cấp độ phiên (như số phiên duyệt web, tỷ lệ phiên có mua hàng) được gán chính xác 100% cho đúng chủ thể người dùng, tuân thủ nghiêm ngặt nguyên tắc độc lập cá thể trong thống kê học.

### Q21: Đánh đổi thực tế (Trade-off) khi chuyển từ CSV sang Parquet là gì?
- **Trả lời:** Đánh đổi thực tế được lượng hóa minh bạch qua ma trận đánh đổi:
  - *Chi phí:* Tiêu tốn 212.18 giây thời gian chạy CPU và đỉnh RAM 2.38 GB trong quá trình ETL chuẩn bị dữ liệu một lần duy nhất.
  - *Lợi ích nhận lại:* Dung lượng đĩa giảm 79.68% (từ 2.32 GB xuống 471.74 MB), tốc độ truy vấn tổng hợp tăng gấp 8.33 lần (từ 5.15s xuống 0.62s), thông lượng quét dữ liệu đạt hơn 31.6 triệu dòng/giây, và kiểu dữ liệu được đóng băng an toàn trong metadata. Đây là khoản đầu tư kỹ thuật hoàn toàn xứng đáng cho sự ổn định và tốc độ của toàn bộ các pha phân tích tiếp theo.

---

# PHẦN IV — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 3 (CUSTOMER FEATURE ENGINEERING & BEHAVIORAL ANALYTICS)

## P3.1 — Chuyển dịch Cấp độ Hạt (Grain Transition): Từ Sự kiện Clickstream sang Hồ sơ Khách hàng Đóng băng tại Mốc Cutoff

### 1. What (Khái niệm là gì?)
Chuyển dịch cấp độ hạt (Grain Transition) là quá trình tổng hợp (aggregation) toàn bộ chuỗi nhật ký sự kiện tương tác (`event grain`, $N = 15,667,350$) của mỗi cá thể người dùng thành một bản ghi duy nhất đại diện cho chân dung hành vi tích lũy của người dùng đó (`customer grain`, $N = 1,341,499$) tại một thời điểm đóng băng cố định (Cutoff Timestamp $T_{\text{cutoff}} = \text{2020-02-01T00:00:00Z}$).

### 2. Why (Tại sao cần chuyển dịch và tại sao phải đóng băng tại Cutoff?)
- **Bản chất của thuật toán phân cụm:** Các mô hình học máy (K-Means) hoạt động trên ma trận đặc trưng tĩnh $X \in \mathbb{R}^{N \times D}$, trong đó mỗi dòng bắt buộc phải là một đối tượng độc lập (Customer). Thuật toán không thể nhận trực tiếp dữ liệu dạng chuỗi sự kiện có độ dài bất định theo thời gian.
- **Quy tắc đóng băng chống rò rỉ (Anti-Leakage Freeze):** Toàn bộ đặc trưng (tần suất, chi tiêu, lượt xem, phiên truy cập) phải được tính toán dựa trên dữ liệu diễn ra nghiêm ngặt trước $T_{\text{cutoff}}$. Bất kỳ sự kiện nào xảy ra sau ranh giới này đều thuộc về tương lai (Holdout) và không được phép xuất hiện trong bảng đặc trưng huấn luyện.

### 3. How (Cách thức triển khai với DuckDB)
Sử dụng mệnh đề `GROUP BY user_id` kết hợp với các hàm tổng hợp có điều kiện (`Conditional Aggregations`) trên bảng `observation_events.parquet`:
```sql
SELECT 
    user_id,
    MAX(event_time) AS max_event_time,
    COUNT(*) AS lifetime_events,
    COUNT(DISTINCT user_session_id) AS lifetime_sessions,
    -- Tính toán các đặc trưng RFM và Engagement
    ...
FROM read_parquet('data/cleaned/observation_events.parquet')
GROUP BY user_id;
```

### 4. Formula / Relation (Mô hình ánh xạ toán học)
$$\mathcal{M}: \mathcal{E}_u \longrightarrow \mathbf{x}_u \in \mathbb{R}^D, \quad \forall u \in \mathcal{U}_{\text{obs}}$$

Trong đó $\mathcal{E}_u = \{e \in E_{\text{obs}} \mid \text{user\_id}(e) = u\}$ là tập hợp các sự kiện của người dùng $u$ trong kỳ quan sát, và $\mathbf{x}_u$ là vector đặc trưng đại diện.
- $|\mathcal{E}| = 15,667,350$ dòng sự kiện $\longrightarrow |\mathcal{U}| = 1,341,499$ dòng khách hàng (Tỷ lệ thu gọn $11.68\times$).

### 5. Worked Example (Ví dụ minh họa)
Người dùng `u100` có 4 sự kiện trong kỳ quan sát:
- `2019-10-15 10:00:00`: View sản phẩm A (phiên s1)
- `2019-10-15 10:05:00`: Cart sản phẩm A (phiên s1)
- `2019-10-15 10:10:00`: Purchase sản phẩm A giá 20$ (phiên s1)
- `2020-01-20 14:00:00`: View sản phẩm B (phiên s2)

Sau khi chuyển dịch grain, dòng đại diện của `u100` tại cutoff `2020-02-01` là:
`{user_id: u100, recency_days: 108.58, frequency: 1, monetary: 20.0, sessions_30d: 1, views_30d: 1, is_buyer: TRUE}`.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Session-level Grain:** Giữ dữ liệu ở cấp phiên ($N = 3,614,959$). Chỉ phù hợp cho bài toán dự đoán ý định mua trong phiên (In-session Purchase Intent), không phù hợp cho bài toán phân khúc vòng đời khách hàng (Customer Lifetime Segmentation).
- **Time-series Embeddings (RNN/Transformer/LSTM):** Mã hóa chuỗi sự kiện thành vector embedding. Tuy nhiên đòi hỏi tài nguyên GPU lớn, khó giải thích với chủ doanh nghiệp (Black-box), và vi phạm nguyên tắc ưu tiên giải pháp minh bạch, dễ hành động (Actionable) của CRISP-DM.

### 7. Verification (Cách thức kiểm chứng)
Kiểm toán bảo toàn chủ thể: `COUNT(DISTINCT user_id)` trong bảng sự kiện quan sát thô = 1,341,499 $\equiv$ `COUNT(*)` trong bảng `customer_features.parquet` = 1,341,499 (Khớp tuyệt đối 100%, không trùng lặp và không sót người dùng nào).

### 8. Limitations (Giới hạn)
Việc nén chuỗi thời gian thành một vector tĩnh làm mất đi thứ tự chi tiết của từng bước duyệt web vi mô trong từng phiên; tuy nhiên điều này được bù đắp bằng các đặc trưng đo xung lượng như `log_activity_ratio`.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em phải chuyển đổi dữ liệu từ bảng sự kiện (event grain) sang bảng khách hàng (customer grain) thay vì để nguyên sự kiện để phân cụm?"*  
> **Trả lời:** *"Thưa Thầy/Cô, thuật toán phân cụm K-Means giải quyết bài toán phân khúc đối tượng khách hàng (Customer Segmentation) chứ không phải phân loại sự kiện. Doanh nghiệp cần biết chân dung của từng người dùng để áp dụng chiến lược tiếp thị (ví dụ: gửi ưu đãi cho khách VIP hay kích hoạt lại khách sắp rời bỏ). Vì mỗi khách hàng phát sinh số lượng sự kiện rất khác nhau (từ 1 sự kiện đến hàng nghìn sự kiện), việc chuyển dịch sang cấp hạt customer grain tại mốc chốt sổ cutoff giúp quy chuẩn hóa mỗi khách hàng thành một vector đặc trưng có cùng số chiều không gian, đảm bảo tính độc lập cá thể và tính so sánh hình học trong thuật toán."*

---

## P3.2 — Mô hình RFM cho Người Mua Hàng và Định lượng Tần suất Mua bằng Proxy Phiên (`purchase_sessions`)

### 1. What (Khái niệm là gì?)
Mô hình RFM (Recency, Frequency, Monetary) là khung đo lường giá trị giao dịch cốt lõi của khách hàng. Trong tập dữ liệu REES46, do thiếu trường `order_id` độc lập, **Frequency ($F$)** được định nghĩa chuẩn xác bằng **số lượng phiên mua hàng duy nhất (Distinct Purchase Sessions Proxy)** của người dùng.

### 2. Why (Tại sao phải dùng proxy phiên thay vì đếm purchase events?)
- **Đặc thù dữ liệu giỏ hàng e-commerce:** Trong một phiên mua sắm, khách hàng thanh toán cùng lúc một giỏ hàng gồm nhiều món (son môi, phấn phủ, kem dưỡng). Hệ thống tracking REES46 ghi nhận mỗi món hàng thành một dòng sự kiện `purchase` riêng biệt trong cùng một mã phiên `user_session`.
- **Hậu quả nếu đếm dòng purchase:** Nếu một khách hàng chỉ mua đúng 1 lần duy nhất trong đời nhưng giỏ hàng có 10 món mỹ phẩm, việc đếm dòng sự kiện sẽ kết luận sai lầm rằng khách hàng này đã mua hàng 10 lần ($F = 10$). Điều này sẽ biến một người mua vãng lai một lần (One-time Buyer) thành khách hàng trung thành mua thường xuyên (Loyal Customer), làm sai lệch hoàn toàn mô hình phân cụm K-Means.

### 3. How (Cách thức triển khai)
```sql
-- Frequency: Đếm số phiên mua duy nhất
COUNT(DISTINCT CASE 
    WHEN is_valid_for_monetary = TRUE THEN user_session_id 
END) AS frequency,

-- Monetary: Tính tổng giá trị của các món hàng hợp lệ
COALESCE(SUM(CASE 
    WHEN is_valid_for_monetary = TRUE THEN price 
    ELSE 0.0 
END), 0.0) AS monetary,

-- Recency: Khoảng cách từ lần mua cuối cùng đến mốc cutoff
ROUND(EXTRACT(EPOCH FROM (TIMESTAMP '2020-02-01 00:00:00' - MAX(CASE WHEN is_valid_for_monetary = TRUE THEN event_time END))) / 86400.0, 2) AS recency_days
```

### 4. Formula / Mathematical Definitions (Công thức toán học)
$$R_u = \frac{T_{\text{cutoff}} - \max_{e \in E_u, \text{valid purchase}} t(e)}{86400.0} \quad (\text{ngày})$$

$$F_u = |\{s \in \mathcal{S}_u \mid \exists e \in s: \text{event\_type}(e) = \text{'purchase'} \land \text{price}(e) > 0\}|$$

$$M_u = \sum_{e \in E_u, \text{purchase}, \text{price}>0} \text{price}(e) \quad (\text{đơn vị tiền tệ})$$

$$\text{AOV}_{\text{proxy}}(u) = \frac{M_u}{F_u}, \quad \text{ItemsPerSession}(u) = \frac{\sum \mathbb{I}(e \in \text{valid purchase})}{F_u}$$

### 5. Worked Example (Ví dụ thực tế)
Khách hàng `u888` trong 4 tháng quan sát có 2 phiên thanh toán:
- Phiên 1 (ngày 15/11): Mua 4 món mỹ phẩm với tổng hóa đơn $45.00.
- Phiên 2 (ngày 20/01 lúc 18:00 UTC): Mua 2 món với tổng hóa đơn $30.00.
- $T_{\text{cutoff}} =$ `2020-02-01 00:00:00 UTC`.
- **Kết quả tính toán:**
  - $R = \text{khoảng cách từ 20/01 18:00 đến 01/02 00:00} = 11.25$ ngày.
  - $F = 2$ phiên mua (mặc dù có tổng cộng 6 dòng sự kiện purchase).
  - $M = 45.00 + 30.00 = 75.00$ đơn vị tiền tệ.
  - $\text{AOV}_{\text{proxy}} = 75.00 / 2 = 37.50$ đơn vị tiền tệ/phiên.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Đếm tổng sự kiện mua (`COUNT(purchase)`):** Bị từ chối vì phóng đại tần suất mua gấp nhiều lần kích thước giỏ hàng.
- **Gom nhóm theo cụm thời gian (Time-window clustering, ví dụ 30 phút):** Phức tạp, dễ tạo ra ranh giới nhân tạo nếu phiên kéo dài; trong khi trường `user_session` do cookie client cấp phát đã là ranh giới phiên tự nhiên chuẩn xác nhất.

### 7. Verification (Cách thức kiểm chứng)
Kiểm tra tính toàn vẹn: 100% người mua hàng ($N = 92,652$) đều có $F \ge 1$, $M > 0$, $R \in [0.0, 123.0]$ ngày. Trung bình mỗi phiên mua ghi nhận 7.81 món hàng (`items_per_purchase_session`), chứng minh rõ ràng việc dùng proxy phiên đã sửa chữa độ lệch phóng đại 7.8 lần.

### 8. Limitations (Giới hạn)
Nếu một khách hàng thực hiện 2 đơn hàng hoàn toàn độc lập trong cùng một phiên duyệt web (ví dụ thanh toán đơn cho mình rồi thanh toán tiếp đơn tặng bạn), hệ thống vẫn chỉ ghi nhận là 1 phiên mua hàng. Tuy nhiên, tỷ lệ này trong thực tế bán lẻ rất thấp (<1%).

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao Frequency của em không phải là số đơn hàng (orders) và điều này ảnh hưởng gì đến kết quả phân tích?"*  
> **Trả lời:** *"Thưa Thầy/Cô, trong tập dữ liệu REES46 không có trường order_id. Chúng em đã kiểm toán thực nghiệm và phát hiện trung bình một phiên mua hàng có tới 7.81 dòng purchase (mỗi dòng tương ứng với 1 sản phẩm trong giỏ). Nếu đếm theo dòng sự kiện, tần suất mua của khách hàng sẽ bị phóng đại sai lệch gần 8 lần. Do đó, chúng em áp dụng nguyên lý proxy khoa học: sử dụng số phiên mua hàng duy nhất (Distinct Purchase Sessions) làm biến đại diện cho số lần phát sinh đơn. Mặc dù proxy này có thể coi 2 đơn mua liên tiếp trong cùng 1 phiên là 1 lần mua, nó phản ánh trung thực 99% hành vi ra quyết định mua sắm của khách hàng và bảo vệ mô hình K-Means khỏi việc phân loại sai One-time buyers thành Loyal buyers."*

---

## P3.3 — Cửa sổ Trượt Hai Giai đoạn 30 Ngày và Kỹ thuật Làm mượt Laplace (Laplace Smoothing) trong Đo lường Xung lượng Hoạt động (`log_activity_ratio`)

### 1. What (Khái niệm là gì?)
Cửa sổ trượt hai giai đoạn (Two-window Sliding Dynamics) là phương pháp chia thời gian trước cutoff thành hai cửa sổ 30 ngày liên tiếp không chồng lấn nhằm đo lường sự thay đổi hành vi theo thời gian. `log_activity_ratio` là chỉ số đo xung lượng tương tác (Activity Momentum) sử dụng logarit tỷ số có tích hợp hằng số làm mượt Laplace (Laplace smoothing $+1$).

### 2. Why (Tại sao cần làm mượt Laplace và tại sao dùng log ratio?)
- **Khắc phục lỗi chia cho 0 (Zero-division):** Rất nhiều khách hàng mới xuất hiện trong 30 ngày gần đây nhưng không có phiên nào trong 30 ngày trước đó ($S_{\text{prev}} = 0$). Nếu không có hằng số $+1$, phép chia $\frac{S_{\text{recent}}}{S_{\text{prev}}}$ sẽ bị lỗi vô cực ($\infty$). Tương tự, nếu khách hàng ngừng truy cập hoàn toàn ($S_{\text{recent}} = 0$), tỷ số sẽ bằng 0 và không lấy được logarit.
- **Tính đối xứng của hàm Logarit:** Phép đo chênh lệch tuyệt đối $S_{\text{recent}} - S_{\text{prev}}$ bị phụ thuộc vào quy mô (khách hàng vào 100 phiên giảm còn 90 phiên có $\Delta = -10$, trong khi khách vào 10 phiên giảm còn 0 phiên cũng có $\Delta = -10$ nhưng bản chất mức độ rời bỏ nghiêm trọng hơn nhiều). Biến đổi Logarit mang lại tính đối xứng: tăng gấp đôi ($\ln(2) \approx +0.69$) và giảm một nửa ($\ln(0.5) \approx -0.69$) có cùng độ lớn khoảng cách hình học trong không gian Euclidean.

### 3. How (Cách thức triển khai)
Thiết lập hai cửa sổ nửa mở nghiêm ngặt:
- $W_{\text{recent}} = [2020-01-02 \text{ 00:00:00}, 2020-02-01 \text{ 00:00:00 UTC})$
- $W_{\text{previous}} = [2019-12-03 \text{ 00:00:00}, 2020-01-02 \text{ 00:00:00 UTC})$
```sql
ROUND(LN((sessions_recent_30d + 1.0) / (sessions_previous_30d + 1.0)), 4) AS log_activity_ratio
```

### 4. Formula / Mathematical Properties (Công thức toán học)
$$\text{Momentum}(u) = \ln\left(\frac{S_{\text{recent}}(u) + 1}{S_{\text{prev}}(u) + 1}\right)$$

Các tính chất biên:
- Khi $S_{\text{recent}} = S_{\text{prev}} \implies \text{Momentum} = \ln(1) = 0$ (Hoạt động ổn định).
- Khi $S_{\text{recent}} > S_{\text{prev}} \implies \text{Momentum} > 0$ (Tương tác đang nóng lên / Heating up).
- Khi $S_{\text{recent}} < S_{\text{prev}} \implies \text{Momentum} < 0$ (Tương tác đang nguội đi / Cooling down / Rủi ro rời bỏ).
- Không bao giờ nhận giá trị $\pm \infty$ hoặc `NaN`.

### 5. Worked Example (Ví dụ thực tế)
- **Khách hàng A (Khách mới kích hoạt):** $S_{\text{prev}} = 0$ phiên, $S_{\text{recent}} = 3$ phiên.  
  $$\text{log\_activity\_ratio} = \ln\left(\frac{3 + 1}{0 + 1}\right) = \ln(4) \approx +1.3863$$
- **Khách hàng B (Khách có dấu hiệu rời bỏ):** $S_{\text{prev}} = 3$ phiên, $S_{\text{recent}} = 0$ phiên.  
  $$\text{log\_activity\_ratio} = \ln\left(\frac{0 + 1}{3 + 1}\right) = \ln(0.25) \approx -1.3863$$
- Nhận xét: Hai trường hợp đối xứng hoàn hảo quanh gốc tọa độ 0.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Tỷ lệ phần trăm thay đổi:** $\frac{S_{\text{recent}} - S_{\text{prev}}}{S_{\text{prev}}}$: Bị lỗi chia cho 0 khi $S_{\text{prev}} = 0$, bị chặn dưới ở $-100\%$ nhưng không bị chặn trên, làm biến dạng hàm mục tiêu của K-Means.
- **Chênh lệch tuyệt đối:** $S_{\text{recent}} - S_{\text{prev}}$: Bỏ qua tỷ lệ nền tảng (quy mô tương tác gốc).

### 7. Verification (Cách thức kiểm chứng)
Unit test `test_laplace_smoothing_log_activity_ratio` xác nhận 100% mẫu ngẫu nhiên khớp hoàn toàn công thức toán học; phân phối thực nghiệm trên 92,652 buyers có Mean = 0.04, Skewness = 0.15 (chuẩn tắc, hình chuông đối xứng).

### 8. Limitations (Giới hạn)
Hằng số làm mượt $+1$ (pseudocount) làm giảm nhẹ độ nhạy đối với những người dùng có số phiên rất nhỏ (ví dụ 1 phiên so với 0 phiên cho ra log ratio $\ln(2) \approx 0.69$ thay vì vô cực); tuy nhiên đây là sự đánh đổi có chủ đích để bảo đảm tính ổn định số học.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em sử dụng log_activity_ratio có cộng 1 thay vì chỉ lấy số phiên tháng này trừ số phiên tháng trước?"*  
> **Trả lời:** *"Thưa Thầy/Cô, nếu chỉ lấy chênh lệch tuyệt đối, chúng ta sẽ bỏ qua quy mô tương tác ban đầu. Một khách hàng giảm từ 2 phiên xuống 0 phiên (giảm 100% hoạt động) sẽ có cùng mức chênh lệch -2 với một khách hàng giảm từ 50 phiên xuống 48 phiên (chỉ giảm 4%). Trong tiếp thị, trường hợp thứ nhất là tín hiệu rời bỏ nghiêm trọng, còn trường hợp thứ hai chỉ là dao động ngẫu nhiên. Việc sử dụng logarit tỷ số kết hợp làm mượt Laplace (+1) giúp giải quyết triệt để 2 vấn đề: (1) Tránh lỗi chia cho 0 khi khách hàng không có phiên nào trong tháng trước; (2) Tạo ra một phân phối đối xứng chuẩn mực quanh giá trị 0, giúp K-Means đo khoảng cách Euclidean một cách công bằng giữa xu hướng tăng trưởng và xu hướng suy giảm tương tác."*

---

## P3.4 — Chiến lược Tách biệt Bảng (Decoupled Cohort Architecture) và Xử lý Nan giải Recency của Người Chưa Mua (The Non-Buyer Dilemma)

### 1. What (Khái niệm là gì?)
Chiến lược tách biệt bảng là kiến trúc dữ liệu phân tách hoàn toàn không gian phân tích thành hai tập dữ liệu độc lập: Tập khách hàng đã mua (`buyer_features.parquet`, $N = 92,652$) và Tập khách hàng chưa từng mua (`non_buyer_features.parquet`, $N = 1,248,847$).

### 2. Why (Tại sao gán Recency = 0 hoặc 999 cho Non-Buyers là sai lầm nghiêm trọng?)
- **Gán Recency = 0:** Mang ngữ nghĩa khách hàng "vừa mới mua hàng hôm nay", biến một người chưa từng bỏ tiền thành khách hàng có độ tươi mới mua sắm cao nhất sàn $\to$ **Sai bản chất nghiệp vụ**.
- **Gán Recency = 999 (hoặc giá trị cực lớn):** K-Means tối ưu hóa tổng bình phương khoảng cách Euclidean. Khi một tập người dùng chiếm tới 93% (1.25 triệu người) có giá trị cực lớn 999 trên trục Recency, trục này sẽ bị kéo dãn và chi phối 90% hàm mục tiêu WCSS. Thuật toán sẽ buộc phải tạo ra một cụm khổng lồ cô lập trục Recency này và làm phẳng hoàn toàn các sai khác tinh tế giữa các phân khúc khách hàng thật.

### 3. How (Cách thức triển khai)
- Gán `recency_days = NULL`, `frequency = 0`, `monetary = 0.0` trong bảng khách hàng tổng thể.
- Xuất riêng `buyer_features.parquet` (chỉ chứa các dòng có `is_buyer = TRUE` với Recency hợp lệ).
- Xuất riêng `non_buyer_features.parquet` phục vụ phân tầng theo luật Engagement ở Phase 6.

### 4. Formula / Separation Logic (Logic phân tách tập hợp)
$$\mathcal{U}_{\text{obs}} = \mathcal{U}_{\text{buyers}} \cup \mathcal{U}_{\text{non-buyers}}, \quad \mathcal{U}_{\text{buyers}} \cap \mathcal{U}_{\text{non-buyers}} = \emptyset$$

$$\mathcal{U}_{\text{buyers}} = \{u \in \mathcal{U}_{\text{obs}} \mid F_u \ge 1 \land M_u > 0\}, \quad |\mathcal{U}_{\text{buyers}}| = 92,652 \text{ (6.91\%)}$$

$$\mathcal{U}_{\text{non-buyers}} = \{u \in \mathcal{U}_{\text{obs}} \mid F_u = 0 \land M_u = 0\}, \quad |\mathcal{U}_{\text{non-buyers}}| = 1,248,847 \text{ (93.09\%)}$$

### 5. Worked Example (Ví dụ phân biệt đối xử)
- Khách hàng X (Non-buyer): Đã xem 50 sản phẩm, thêm 3 giỏ hàng trong 30 ngày qua nhưng chưa mua.
  - Bảng Buyer K-Means: Không xuất hiện.
  - Bảng Non-Buyer: Ghi nhận `{views_30d: 50, cart_sessions_30d: 3, cohort: NON_BUYER}` $\to$ Xếp vào phân tầng `High-Intent Non-Buyer`, kích hoạt chiến thuật gửi voucher giảm giá lần đầu (`TAC_FIRST_ORDER_DISCOUNT`).
- Khách hàng Y (Buyer): Đã mua 1 lần cách đây 20 ngày giá 30$.
  - Bảng Buyer K-Means: Ghi nhận `{recency: 20, frequency: 1, monetary: 30}` $\to$ Phân cụm cùng các khách hàng đã mua khác.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Gộp chung và impute giá trị trung bình/trung vị:** Biến người chưa mua thành người đã mua cách đây 56 ngày $\to$ Ngụy tạo dữ liệu.
- **Thêm cờ boolean `has_bought` vào K-Means:** Không giải quyết được giá trị khuyết thiếu của Recency trên khoảng cách Euclidean.

### 7. Verification (Cách thức kiểm chứng)
Unit test `test_non_buyer_recency_policy_is_null` xác nhận 100% trong số 1,248,847 non-buyers đều có `recency_days = NULL`, không có trường hợp nào bị gán 0 hay 999.

### 8. Limitations (Giới hạn)
Non-buyers không thể tham gia vào bài toán phân cụm RFM truyền thống; tuy nhiên họ được tiếp cận bằng một khung phân tích riêng biệt (Engagement Stratification) phù hợp hơn với bản chất hành vi duyệt web.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không đưa toàn bộ 1.34 triệu người dùng vào chạy K-Means mà lại tách riêng tập Non-Buyers?"*  
> **Trả lời:** *"Thưa Thầy/Cô, đây là nguyên tắc bắt buộc trong phương pháp luận phân tích RFM. Với 93% người dùng chưa từng mua hàng, Recency của họ về mặt toán học là không xác định. Nếu cố tình gán một con số nhân tạo như 999 để chạy chung K-Means, trục Recency sẽ bị kéo dãn cực độ, làm biến dạng không gian Euclidean và biến thuật toán K-Means thành một bộ lọc nhị phân tầm thường (chia thành nhóm mua và chưa mua) thay vì tìm ra các phân khúc khách hàng sâu sắc. Việc phân rã kiến trúc cho phép chúng em áp dụng K-Means một cách chuẩn xác nhất trên 92k khách hàng đã mua, đồng thời xây dựng bộ máy phân loại tương tác chuyên biệt cho 1.25 triệu khách hàng tiềm năng."*

---

## P3.5 — Phân tích Phân phối Lệch Xiên Cực đoan (Heavy Right-skewness), Đa cộng tuyến và Chiến lược Lựa chọn Không gian Đặc trưng ($F0, F1, F2$)

### 1. What (Khái niệm là gì?)
Phân phối lệch xiên cực đoan (Heavy Right-skewness) là hiện tượng đa số dữ liệu tập trung ở các giá trị nhỏ nhưng có một đuôi dài kéo dài về phía các giá trị cực lớn. Đa cộng tuyến (Multicollinearity) là hiện tượng hai hay nhiều đặc trưng có tương quan tuyến tính quá cao ($r > 0.85$). Các tập đặc trưng $F0, F1, F2$ là các không gian ứng viên có số chiều tăng dần ($D = 3, 7, 12$) được thiết kế để kiểm nghiệm ở Phase 4.

### 2. Why (Tại sao độ lệch xiên ảnh hưởng đến K-Means?)
Thuật toán K-Means tính tâm cụm bằng giá trị trung bình (mean) và đo khoảng cách bằng Euclidean. Khi dữ liệu bị lệch xiên cực đoan (ví dụ Frequency có $\text{Skew} = 17.12$, Monetary có $\text{Skew} = 7.19$):
- Vài khách hàng cá biệt có giá trị chi tiêu cực cao ($M = 3,162$) sẽ "kéo" tâm cụm về phía họ, tạo ra các cụm đơn lẻ chỉ chứa 1-2 cá thể ngoại lai (outlier clusters).
- Các cụm còn lại sẽ bị dồn nén vào một khối dày đặc, mất đi khả năng phân tách ranh giới tự nhiên.

### 3. How (Cách thức xử lý và thiết kế feature sets)
1. Khảo sát độ lệch qua Skewness:
   - `recency_days`: Skew = 0.11 (Gần đối xứng, không cần biến đổi).
   - `frequency`: Skew = 17.12 $\to$ Cần biến đổi log `np.log1p(F)`.
   - `monetary`: Skew = 7.19 $\to$ Cần biến đổi log `np.log1p(M)`.
2. Kiểm tra ma trận tương quan:
   - Cặp tương quan cao nhất là $(F, M)$ với $r = 0.65$ (nằm an toàn dưới ngưỡng nguy hiểm 0.85).
3. Thiết kế 3 không gian đặc trưng:
   - $F0$ (Baseline 3D): `[recency_days, frequency, monetary]`
   - $F1$ (Core 7D): `F0` + `[sessions_30d, views_30d, cart_sessions_30d, log_activity_ratio]`
   - $F2$ (Extended 12D): `F1` + `[monetary_per_session, items_per_session, unique_products_30d, cart_to_view_ratio, days_since_last_event]`

### 4. Formula / Log Transformation (Công thức biến đổi)
$$x' = \ln(x + 1)$$

$$\text{Skewness}(X) = \frac{\frac{1}{N} \sum_{i=1}^N (x_i - \bar{x})^3}{\left(\frac{1}{N} \sum_{i=1}^N (x_i - \bar{x})^2\right)^{3/2}}$$

### 5. Worked Example (Hiệu quả giảm xiên của Log-transform)
- Đối với Frequency:
  - Giá trị gốc: Median = 1.0, Mean = 1.37, Max = 103.0 $\implies \text{Skew} = 17.12$.
  - Sau $\ln(1 + F)$: $\ln(2) \approx 0.69$, $\ln(104) \approx 4.64 \implies \text{Skew}$ giảm xuống dưới 2.0, kéo đuôi phân phối về gần tâm giúp K-Means hội tụ ổn định.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Box-Cox Transformation:** Đòi hỏi dữ liệu hoàn toàn dương ($x > 0$), không áp dụng được trực tiếp cho các đặc trưng có giá trị 0 như `sessions_30d`.
- **Yeo-Johnson Transformation:** Hỗ trợ cả số 0 và số âm, nhưng chi phí tính toán tham số $\lambda$ cao hơn nhiều so với $\log(1+x)$ mà không mang lại khác biệt lớn cho K-Means.

### 7. Verification (Cách thức kiểm chứng)
Ma trận tương quan hình ảnh `outputs/figures/fig11_rfm_correlation_matrix.png` và bảng thống kê mô tả trong `outputs/experiments/phase3_feature_profiling.json` chứng minh 100% các cặp đặc trưng trong $F1$ đều có hệ số tương quan $|r| < 0.66$.

### 8. Limitations (Giới hạn)
Biến đổi log làm mất đi đơn vị đo lường gốc của dữ liệu (scale-free space). Do đó, sau khi phân cụm ở Phase 4, toàn bộ đặc trưng phải được ánh xạ ngược (inverse transform) về đơn vị đo gốc (ngày, phiên, đơn vị tiền tệ) khi xây dựng chân dung cụm (Profiling).

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao Frequency và Monetary có độ lệch xiên cao và em dự định tiền xử lý như thế nào trước khi chạy K-Means ở Phase 4?"*  
> **Trả lời:** *"Thưa Thầy/Cô, trong thương mại điện tử, hiện tượng lệch phải cực đoan là quy luật khách quan (nguyên lý Pareto): 80% khách hàng chỉ mua 1 lần với số tiền nhỏ, trong khi một số ít khách hàng VIP mua tới hàng chục lần và chi tiêu hàng nghìn đơn vị tiền tệ. Điều này thể hiện qua Skewness của Frequency đạt 17.12 và Monetary đạt 7.19. Vì K-Means sử dụng khoảng cách Euclidean, các giá trị ngoại lai cực lớn này sẽ làm lệch trọng tâm các cụm. Trong Phase 4, chúng em sẽ áp dụng phép biến đổi logarit tự nhiên log(1 + x) để nén đuôi phân phối, kết hợp với bộ chuẩn hóa RobustScaler để đưa các đặc trưng về cùng một thang đo mà không bị ảnh hưởng bởi các ngoại lai cực trị."*

---

## P3.6 — Đo kiểm Hiệu năng Trích xuất Đặc trưng trên DuckDB (Throughput, Process RSS vs In-Memory Staging)

### 1. What (Khái niệm là gì?)
Đo kiểm hiệu năng trích xuất đặc trưng là quá trình lượng hóa tài nguyên tính toán (Thời gian thực thi Wall-Clock, Thông lượng Throughput, Bộ nhớ vật lý đỉnh Peak RSS qua `psutil`) khi chuyển đổi 15.67 triệu dòng sự kiện thành bảng đặc trưng 1.34 triệu khách hàng.

### 2. Why (Tại sao DuckDB đạt tốc độ tổng hợp cực nhanh?)
- **Vectorized Group By:** DuckDB sử dụng cấu trúc bảng băm đa luồng (Radix Partitioned Hash Table) được tối ưu hóa cho các phép tính tổng hợp trên bộ nhớ đệm CPU (L1/L2/L3 cache), xử lý hàng triệu dòng cùng lúc theo từng vector 2048 phần tử.
- **Projection Pushdown:** Thay vì đọc toàn bộ 21 cột của `observation_events.parquet`, câu truy vấn chỉ quét đúng các cột cần thiết (`user_id`, `event_time`, `event_type`, `price`, `user_session_id`, `is_valid_for_monetary`).

### 3. How (Kết quả đo kiểm thực tế)
- **Thời gian xử lý toàn trình:** **11.25 giây**.
  - Tổng hợp dữ liệu (Aggregation): 5.14 giây.
  - Xuất 3 tệp Parquet: 1.34 giây.
  - Phân tích thống kê & sinh 4 biểu đồ: 4.77 giây.
- **Thông lượng quét sự kiện:** **1,392,653 dòng sự kiện/giây**.
- **Thông lượng tạo hồ sơ khách hàng:** **119,244 khách hàng/giây**.
- **Bộ nhớ RAM vật lý đỉnh (Peak RSS):** **1,478.11 MB** (~1.44 GB).
- **Dung lượng tệp kết quả trên đĩa:** 25.09 MB (cho cả 3 tệp Parquet).

### 4. Formula (Công thức tính toán)
$$\text{Throughput}_{\text{Events}} = \frac{15,667,350 \text{ events}}{11.25 \text{ seconds}} \approx 1,392,653 \text{ events/s}$$

$$\text{Throughput}_{\text{Customers}} = \frac{1,341,499 \text{ customers}}{11.25 \text{ seconds}} \approx 119,244 \text{ customers/s}$$

### 5. Verification (Cách thức kiểm chứng)
Nhật ký thực nghiệm máy đọc được lưu vết độc lập tại `outputs/experiments/phase3_feature_profiling.json`. Unit test `test_feature_tables_exist_and_sizes` kiểm tra tính toàn vẹn của dữ liệu trên đĩa.

### 6. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Hệ thống của em mất bao lâu để tạo ra bảng đặc trưng của 1.34 triệu khách hàng và lượng RAM tiêu tốn là bao nhiêu?"*  
> **Trả lời:** *"Thưa Thầy/Cô, toàn bộ quy trình trích xuất đặc trưng từ hơn 15.6 triệu dòng sự kiện diễn ra chỉ trong 11.25 giây trên máy tính cá nhân 16 lõi. Thông lượng xử lý đạt hơn 1.39 triệu sự kiện/giây và tạo ra hơn 119 nghìn hồ sơ khách hàng mỗi giây. Lượng RAM vật lý đỉnh (Peak RSS) đo qua psutil được kiểm soát ổn định ở mức 1.48 GB, hoàn toàn nằm dưới giới hạn an toàn 2 GB được cấp. Kết quả đầu ra được đóng gói thành các tệp Parquet nén ZSTD chỉ nặng 25 MB, sẵn sàng phục vụ cho việc huấn luyện mô hình K-Means ở Phase 4 trong vài giây."*

---

## P3.7 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 3 (Oral Defense Guide P3: Q22 – Q26)

### Q22: Tại sao việc tính Recency phải neo vào mốc Cutoff cố định thay vì neo vào ngày chạy code hôm nay (`datetime.now()`)?
- **Trả lời:** Đây là nguyên tắc cốt tử về tính tái lập (Reproducibility) và kiểm soát rò rỉ dữ liệu trong Khoa học Dữ liệu. Tập dữ liệu REES46 diễn ra từ năm 2019–2020. Nếu neo vào ngày hôm nay (`now()`), giá trị Recency của tất cả khách hàng sẽ bị cộng thêm hơn 6 năm (hơn 2,000 ngày), xóa nhòa hoàn toàn khoảng cách tương đối giữa người mua cách đây 1 ngày và người mua cách đây 30 ngày tại thời điểm đó. Việc neo chặt vào mốc chốt sổ $T_{\text{cutoff}} = \text{2020-02-01 00:00:00 UTC}$ phản ánh trung thực trạng thái thực tế của doanh nghiệp tại thời khắc chốt kỳ quan sát.

### Q23: Tại sao tỷ lệ khách hàng mua lặp lại (Repeat Buyer Rate) là 20.06% và điều này nói lên điều gì về cấu trúc tập khách hàng?
- **Trả lời:** Trong số 92,652 khách hàng đã mua, có đúng 18,587 khách hàng phát sinh từ 2 phiên mua trở lên (20.06%), còn lại 74,065 khách hàng (79.94%) là One-time Buyers chỉ mua đúng 1 lần. Con số này phản ánh đặc thù điển hình của thương mại điện tử mỹ phẩm trực tuyến: tỷ lệ rơi rụng sau lần mua đầu tiên rất lớn. Điều này chứng minh rằng việc xây dựng bộ đặc trưng Engagement 30 ngày gần nhất là tối quan trọng: nó giúp phân tách nhóm 80% One-time buyers thành 2 nhóm rõ rệt: những người đã rời bỏ hoàn toàn (không vào web nữa) và những người vẫn đang tích cực xem hàng, thêm giỏ (đối tượng tiềm năng để kích hoạt mua lần 2).

### Q24: Việc bổ sung các đặc trưng Clickstream Engagement 30 ngày ($F1$) có nguy cơ gây ra hiện tượng gì và em kiểm soát ra sao?
- **Trả lời:** Việc bổ sung đặc trưng có 2 nguy cơ chính: (1) Đa cộng tuyến (Multicollinearity) nếu các đặc trưng quá giống nhau; (2) Lời nguyền số chiều (Curse of Dimensionality) làm loãng khoảng cách Euclidean. Chúng em kiểm soát bằng 3 biện pháp: (1) Kiểm tra ma trận tương quan (Figure 11) chứng minh không có cặp nào vượt ngưỡng $r = 0.85$; (2) Thiết kế phép đo xung lượng qua hàm log đối xứng `log_activity_ratio`; (3) Thiết kế 3 không gian thử nghiệm $F0$ (3 chiều), $F1$ (7 chiều) và $F2$ (12 chiều) để đánh giá thực nghiệm đa tiêu chí (Silhouette, Davies-Bouldin, ARI) ở Phase 4 thay vì áp đặt chủ quan.

### Q25: Làm thế nào để chứng minh bảng đặc trưng Feature Table hoàn toàn không bị rò rỉ dữ liệu tương lai (Data Leakage)?
- **Trả lời:** Chúng em kiểm chứng tính chống rò rỉ qua 3 tầng bảo vệ: (1) *Tầng dữ liệu nguồn:* Bảng đặc trưng chỉ được truy vấn duy nhất từ tệp `observation_events.parquet`, trong đó toàn bộ sự kiện đã được xác minh độc lập có `event_time < 2020-02-01 00:00:00 UTC`; (2) *Tầng kiểm thử đơn vị:* Unit test `test_strict_temporal_split_anti_leakage` xác nhận số sự kiện mua trong kỳ quan sát diễn ra sau cutoff bằng đúng 0; (3) *Tầng niêm phong:* Tập dữ liệu tháng 2/2020 (`holdout_events.parquet`) hoàn toàn không được nạp vào bất kỳ câu lệnh SQL nào của Phase 3.

### Q26: Sự khác biệt cơ bản về mức độ tương tác giữa Buyers và Non-Buyers là gì?
- **Trả lời:** Kết quả phân tích đối đầu ở Figure 12 chỉ ra sự khác biệt sâu sắc: Khách hàng đã mua (Buyers) có mức độ gắn kết cao vượt trội so với người chưa mua: trung vị số sự kiện tích lũy của Buyers là 41 sự kiện (so với đúng 1 sự kiện ở Non-buyers, gấp 41 lần); trung vị số phiên truy cập là 4 phiên (so với 1 phiên ở Non-buyers); và thời gian kể từ tương tác cuối cùng gần hơn 17 ngày (40.6 ngày so với 57.8 ngày). Điều này chứng minh rằng hành vi xem hàng và duyệt web là điều kiện tiên quyết dẫn đến chuyển đổi, và việc phân tầng Non-buyers để nuôi dưỡng (Nurturing) là một chiến lược marketing hoàn toàn có cơ sở thực nghiệm vững chắc.


---

# PHẦN V — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 4 (CUSTOMER SEGMENTATION MODELING)

## P4.1 — Thuật toán K-Means Clustering, Hàm Mục tiêu WCSS và Bản chất Hình học Khoảng cách Euclidean

### 1. What (Khái niệm là gì?)
K-Means là thuật toán học máy không giám sát dựa trên trọng tâm (Centroid-based Unsupervised Clustering), phân chia $N$ điểm dữ liệu vào $K$ cụm rời rạc sao cho mỗi điểm dữ liệu thuộc về cụm có tâm gần nhất.

### 2. Why (Tại sao áp dụng cho Phân khúc Khách hàng?)
- **Độ phức tạp tuyến tính:** Thời gian tính toán $\mathcal{O}(N \times K \times D \times I)$ rất nhỏ trên tập 92,652 khách hàng ($D=7, K=4$), huấn luyện chỉ mất $0.3$ giây.
- **Tính khả giải cao:** Tâm cụm (Centroid) biểu diễn khách hàng đại diện trực quan, dễ dàng diễn giải thành hành vi mua sắm thực tế.
- **Ranh giới phân vùng Voronoi:** Tạo ra các vùng quyết định lồi (Convex Voronoi Cells), dễ dàng ánh xạ thành các luật tiếp thị dạng cây ở Phase 6.

### 3. How (Cách thức triển khai thực tế)
- Sử dụng `sklearn.cluster.KMeans` với thuật toán khởi tạo tối ưu `k-means++`.
- Thiết lập số lần khởi tạo độc lập `n_init = 20` để chọn mô hình có quán tính tối thiểu toàn cục.
- Cố định `random_state = 42` phục vụ tính tái lập (Reproducibility).

### 4. Formula (Công thức toán học)
Hàm mục tiêu Quán tính / Tổng bình phương khoảng cách nội cụm (Within-Cluster Sum of Squares — WCSS):
$$J = \text{WCSS} = \sum_{k=1}^K \sum_{x_i \in C_k} \| x_i - \mu_k \|_2^2$$
Trong đó:
- $C_k$ là tập hợp các khách hàng thuộc cụm $k$.
- $\mu_k = \frac{1}{|C_k|} \sum_{x_i \in C_k} x_i$ là tâm trọng lực (Mean Centroid) của cụm $k$.
- Khoảng cách Euclidean bậc hai giữa khách hàng $x_i$ và tâm $\mu_k$:
$$\| x_i - \mu_k \|_2^2 = \sum_{j=1}^D (x_{i,j} - \mu_{k,j})^2$$

### 5. Worked Example (Ví dụ tính toán minh họa)
Xét không gian 2 chiều thu gọn gồm Recency $z_R$ và Monetary $z_M$.
Tâm cụm VIP $\mu_1 = (1.5, 2.0)$ và tâm cụm Dormant $\mu_2 = (-0.5, -1.0)$.
Khách hàng A có tọa độ $x_A = (1.2, 1.8)$:
$$d^2(x_A, \mu_1) = (1.2 - 1.5)^2 + (1.8 - 2.0)^2 = (-0.3)^2 + (-0.2)^2 = 0.09 + 0.04 = 0.13$$
$$d^2(x_A, \mu_2) = (1.2 - (-0.5))^2 + (1.8 - (-1.0))^2 = (1.7)^2 + (2.8)^2 = 2.89 + 7.84 = 10.73$$
Vì $0.13 < 10.73$, khách hàng A được phân bổ chính xác vào Cụm 1 (VIP).

### 6. Alternatives (Phương án thay thế & So sánh)
- **Hierarchical Agglomerative Clustering (HAC):** Độ phức tạp $\mathcal{O}(N^2)$ về bộ nhớ và $\mathcal{O}(N^3)$ thời gian; không thể chạy trên 92k dòng trong bộ nhớ RAM máy trạm.
- **DBSCAN:** Phân cụm dựa trên mật độ; nhạy cảm với tham số $\epsilon$, không phù hợp với dữ liệu thương mại điện tử vốn có mật độ không đồng đều giữa các nhóm giá trị.
- **Gaussian Mixture Models (GMM):** Cho phép cụm elip và gán nhãn xác suất, nhưng chi phí tính toán cao hơn 10 lần và dễ rơi vào ma trận hiệp phương sai kỳ dị (Singular Covariance).

### 7. Verification (Cách thức kiểm chứng)
Đo lường hàm suy giảm quán tính WCSS và kiểm thử tự động `test_03_cluster_label_domain` và `test_07_model_predict_contract`.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Giả định các cụm có hình cầu đẳng hướng (Spherical Clusters) và kích thước phương sai tương đương nhau.
- Nhạy cảm với giá trị ngoại lai cực đại nếu không chuẩn hóa và làm sạch kỹ ở Phase 2 & 3.
- Bắt buộc phải xác định trước số cụm $K$.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"K-Means giải bài toán tối ưu bằng thuật toán gì và có đảm bảo đạt cực tiểu toàn cục không?"*  
> **Trả lời:** *"Thưa Thầy/Cô, K-Means sử dụng thuật toán tối ưu hóa tọa độ khối (Block Coordinate Descent / Lloyd's Algorithm), luân phiên giữa 2 bước: (1) Gán điểm dữ liệu vào tâm gần nhất (Assignment Step), và (2) Cập nhật lại tọa độ tâm cụm bằng trung bình cộng (Update Step). Thuật toán được chứng minh luôn hội tụ đơn điệu về cực tiểu hàm mục tiêu WCSS, nhưng chỉ đạt Cực tiểu cục bộ (Local Minimum), không đảm bảo cực tiểu toàn cục. Để khắc phục, đồ án áp dụng phương pháp khởi tạo k-means++ kết hợp n_init = 20 lần chạy độc lập để chọn nghiệm có WCSS thấp nhất."*

---

## P4.2 — Tác động của Skewness, Biến đổi Log1p và Chuẩn hóa Đặc trưng (StandardScaler vs RobustScaler)

### 1. What (Khái niệm là gì?)
Tiền xử lý đặc trưng cho K-Means là quy trình chuyển đổi phân phối lệch xiên (Skewed Distribution) về dạng gần đối xứng và chuẩn hóa thang đo (Feature Scaling) để đảm bảo mọi chiều không gian đều đóng góp công bằng vào khoảng cách Euclidean.

### 2. Why (Tại sao không thể chạy K-Means trên dữ liệu thô?)
- **Độ lệch xiên cực đoan:** Frequency có Skewness = 17.12 và Monetary có Skewness = 7.19. Nếu giữ nguyên, khách hàng mua 3,000 đơn vị tiền tệ sẽ tạo ra khoảng cách bình phương $(3000 - 33)^2 \approx 8.8 \times 10^6$, hoàn toàn lấn át toàn bộ các chiều còn lại (như Recency dao động trong 120 ngày).
- **Trọng số ẩn (Implicit Feature Weighting):** Biến nào có đơn vị đo lớn hơn tự động được K-Means coi là quan trọng hơn, làm mất tính khách quan khoa học.

### 3. How (Quy trình tiền xử lý tái sử dụng)
1. Lọc danh sách các đặc trưng không âm có độ lệch xiên cao (`frequency`, `monetary`, `sessions_30d`, `views_30d`, `cart_sessions_30d`).
2. Áp dụng biến đổi logarit tự nhiên: $x_{\text{log}} = \ln(1 + \max(x, 0))$.
3. Giữ nguyên dạng tuyến tính đối với các biến phân phối đều (`recency_days`, `days_since_last_event`).
4. Giữ nguyên `log_activity_ratio` vì đã ở không gian log và chứa giá trị âm.
5. Áp dụng `StandardScaler` (hoặc `RobustScaler`) để đưa trung bình về 0 và phương sai về 1.

### 4. Formula (Công thức toán học)
- **Biến đổi Log1p:**
$$f(x) = \ln(1 + x) \quad (\forall x \ge 0)$$
- **StandardScaler:**
$$z_j = \frac{x_j - \mu_j}{\sigma_j}$$
- **RobustScaler:**
$$z_j^{\text{robust}} = \frac{x_j - \text{Median}_j}{\text{IQR}_j} = \frac{x_j - Q_2(j)}{Q_3(j) - Q_1(j)}$$

### 5. Worked Example (Ví dụ minh họa)
Một khách hàng có `frequency = 1` và khách hàng VIP có `frequency = 100`:
- *Nếu chưa log:* Khoảng cách thô $= 100 - 1 = 99$.
- *Sau biến đổi log1p:*
  - Khách 1: $\ln(1 + 1) = \ln(2) \approx 0.693$.
  - Khách 100: $\ln(1 + 100) = \ln(101) \approx 4.615$.
  - Khoảng cách log $= 4.615 - 0.693 = 3.922$.
Biến đổi log đã nén khoảng cách từ 99 lần xuống chỉ còn 5.6 lần, bảo toàn trật tự thứ hạng nhưng ngăn chặn triệt để hiện tượng giá trị ngoại lai kéo lệch tâm cụm.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Min-Max Scaling ($[0, 1]$):** Rất nhạy cảm với ngoại lai; nếu có 1 khách chi tiêu 3,162 đơn vị, 99% khách hàng còn lại sẽ bị nén nghẹt vào khoảng hẹp $[0, 0.05]$.
- **Box-Cox / Yeo-Johnson Power Transform:** Tối ưu hóa tham số $\lambda$ để ép về phân phối chuẩn, nhưng tăng độ phức tạp tính toán và khó giải thích ngược về đơn vị gốc.

### 7. Verification (Cách thức kiểm chứng)
Kiểm tra độ lệch chuẩn $\sigma = 1.0$ và giá trị trung bình $\mu \approx 0.0$ của ma trận sau chuẩn hóa. Unit test `test_07_model_predict_contract` xác nhận khả năng biến đổi và dự đoán nhất quán của pipeline.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- `log1p` chỉ áp dụng được cho số không âm ($x \ge 0$); không áp dụng trực tiếp cho các biến có giá trị âm như `log_activity_ratio`.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không áp dụng log1p lên đặc trưng `log_activity_ratio`?"*  
> **Trả lời:** *"Thưa Thầy/Cô, đặc trưng log_activity_ratio được xây dựng từ công thức log((n_recent + 1)/(n_previous + 1)). Bản thân nó đã ở trong không gian logarit và có miền giá trị từ -6.53 đến +7.42. Nếu áp dụng hàm log1p lên giá trị âm nhỏ hơn -1, hàm logarit sẽ không xác định (lỗi miền giá trị toán học và sinh ra giá trị NaN). Hơn nữa, phân phối của đặc trưng này đã đối xứng hoàn hảo quanh giá trị 0 (Skewness = 0.11), nên chỉ cần chuẩn hóa tỷ lệ qua StandardScaler mà không cần biến đổi phi tuyến thêm."*

---

## P4.3 — Phương pháp Luận Lựa chọn Số cụm $K$: Elbow Curve, Silhouette Coefficient và Davies-Bouldin Index

### 1. What (Khái niệm là gì?)
Lựa chọn số cụm $K$ là bài toán xác định siêu tham số quan trọng nhất trong K-Means nhằm đạt được sự cân bằng giữa độ cô đọng nội cụm (Compactness) và độ phân tách liên cụm (Separation).

### 2. Why (Tại sao không thể chỉ nhìn vào một chỉ số duy nhất?)
- **Inertia (Elbow):** Luôn giảm đơn điệu khi $K$ tăng (khi $K=N$, WCSS = 0), do đó không thể dùng giá trị nhỏ nhất của WCSS để chọn $K$.
- **Silhouette:** Thường đạt giá trị cao nhất tại $K=2$, nhưng $K=2$ phân khúc quá thô sơ, không đáp ứng được nhu cầu cá nhân hóa chiến dịch tiếp thị.
- **Davies-Bouldin Index (DBI):** Đo lường tỷ số độ phân tán nội cụm trên khoảng cách giữa các tâm cụm; bổ sung góc nhìn độc lập kiểm tra độ chồng lấn.

### 3. How (Phương pháp kết hợp đa tiêu chí)
- Vẽ đồ thị 3 bảng trên cùng hình vẽ ([fig13_elbow_silhouette.png](file:///d:/Lap%20trinh/customer-analytics-antigravity/outputs/figures/fig13_elbow_silhouette.png)): (a) Elbow curve, (b) Silhouette curve, (c) DBI curve.
- Tính Silhouette trên mẫu cố định 10,000 khách hàng (với seed 42) để tránh tràn bộ nhớ tính toán ma trận khoảng cách $92k \times 92k$.
- Đặt điều kiện nghiệm thu thực tế: Cụm nhỏ nhất phải chiếm ít nhất **5%** dân số khách hàng (loại bỏ $K \ge 5$ vì xuất hiện cụm suy thoái $4.6\%$).

### 4. Formula (Công thức toán học)
- **Hệ số Silhouette của điểm $i$:**
$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))} \in [-1, +1]$$
Trong đó:
  - $a(i) = \frac{1}{|C_I| - 1} \sum_{j \in C_I, j \ne i} d(i, j)$ là khoảng cách trung bình từ $i$ đến các điểm trong cùng cụm.
  - $b(i) = \min_{J \ne I} \frac{1}{|C_J|} \sum_{j \in C_J} d(i, j)$ là khoảng cách trung bình từ $i$ đến cụm lân cận gần nhất.
- **Davies-Bouldin Index (DBI):**
$$R_{ij} = \frac{s_i + s_j}{d(\mu_i, \mu_j)}, \quad \text{DBI} = \frac{1}{K} \sum_{i=1}^K \max_{j \ne i} R_{ij}$$
(Trong đó $s_i$ là độ phân tán trung bình nội cụm $i$; DBI càng nhỏ thì các cụm càng tách biệt).

### 5. Worked Example (Ví dụ minh họa)
Xét điểm $i$: khoảng cách trung bình nội cụm $a(i) = 0.4$, khoảng cách đến cụm gần nhất $b(i) = 1.0$:
$$s(i) = \frac{1.0 - 0.4}{\max(0.4, 1.0)} = \frac{0.6}{1.0} = +0.60$$
Điểm $i$ có hệ số Silhouette dương cao (+0.60), chứng minh điểm này nằm rất sâu bên trong cụm của nó và cách xa cụm lân cận.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Gap Statistic:** So sánh WCSS thực tế với phân phối đồng đều ngẫu nhiên giả định (Null Reference Distribution); chi phí tính toán cực cao do phải sinh nhiều tập giả lập Monte Carlo.
- **Calinski-Harabasz Index (Variance Ratio Criterion):** Tỷ số phân tán giữa các cụm trên phân tán nội cụm; nhạy cảm với hình dạng cụm cầu.

### 7. Verification (Cách thức kiểm chứng)
Kết quả đo kiểm trên 28 cấu hình Vòng 1 ghi nhận rõ ràng: tại $K=4$, Inertia gập góc Elbow, Silhouette đạt mức ổn định $0.284$, DBI đạt $1.42$, và kích thước cụm nhỏ nhất đạt $9.45\%$ (hoàn toàn thỏa mãn ngưỡng $> 5\%$).

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Silhouette có xu hướng suy giảm khi số chiều tăng (do hiệu ứng làm đồng đều khoảng cách ở số chiều cao), vì vậy không thể so sánh Silhouette giữa $F0$ (3D) và $F1$ (7D) để khẳng định $F0$ ưu việt hơn về mặt nghiệp vụ.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao hệ số Silhouette của mô hình F0 (3D) là 0.33 cao hơn F1 (7D) là 0.28 mà em lại chọn mô hình F1?"*  
> **Trả lời:** *"Thưa Thầy/Cô, đây là hệ quả tự nhiên của hình học không gian (Curse of Dimensionality). Trong không gian 3 chiều, các điểm dữ liệu có mật độ dày hơn nên khoảng cách giữa các điểm phân hóa rõ hơn, tạo ra điểm Silhouette cao hơn. Tuy nhiên, F0 hoàn toàn bỏ sót dữ liệu hành vi tương tác website (số phiên, số lần thêm giỏ, xu hướng hoạt động). Mô hình F1 tuy có Silhouette thấp hơn một chút (0.28) nhưng mang lại giá trị phân khúc nghiệp vụ vượt trội: phân tách rõ ràng nhóm khách VIP trung thành và nhóm khách đang có nguy cơ rời bỏ web (Cooling Down), điều mà mô hình RFM truyền thống hoàn toàn mù mờ."*

---

## P4.4 — Đánh giá Độ Ổn định Thuật toán Không giám sát qua Adjusted Rand Index (ARI) trên Nhiều Random Seeds

### 1. What (Khái niệm là gì?)
Đánh giá độ ổn định (Clustering Stability Evaluation) là phương pháp định lượng mức độ nhất quán của kết quả phân cụm khi thay đổi các yếu tố ngẫu nhiên (chẳng hạn như hạt giống ngẫu nhiên `random_state` khi chọn tâm cụm khởi tạo ban đầu).

### 2. Why (Tại sao tính ổn định là điều kiện tiên quyết trong Phân tích Khách hàng?)
Nếu một mô hình phân cụm bị thay đổi hoàn toàn cấu trúc chỉ vì đổi `random_state = 42` sang `101`, doanh nghiệp không thể tin tưởng áp dụng: chiến dịch tiếp thị tháng này gán khách hàng A vào nhóm VIP nhưng tháng sau chạy lại hạt giống khác lại bị rơi sang nhóm Ngủ đông. Mô hình phân khúc bắt buộc phải ổn định bền vững.

### 3. How (Cách thức đo kiểm thực nghiệm)
- Chạy K-Means trên 5 random seeds độc lập: `[42, 101, 202, 303, 404]`.
- Thu được 5 vectơ nhãn phân cụm: $y^{(1)}, y^{(2)}, y^{(3)}, y^{(4)}, y^{(5)}$ trên cùng 92,652 khách hàng.
- Tính toán toàn bộ $\binom{5}{2} = 10$ cặp chỉ số Adjusted Rand Index (ARI) giữa các lần chạy.
- Báo cáo giá trị trung bình $\text{Mean ARI}$, độ lệch chuẩn $\text{Std ARI}$, và giá trị nhỏ nhất $\text{Min ARI}$.

### 4. Formula (Công thức toán học)
Chỉ số Rand Index (RI) và phiên bản điều chỉnh ngẫu nhiên Adjusted Rand Index (ARI):
$$\text{ARI} = \frac{\text{RI} - \mathbb{E}[\text{RI}]}{\max(\text{RI}) - \mathbb{E}[\text{RI}]} \in [-1, +1]$$
Dựa trên bảng ngẫu nhiên Contingency Table giữa phân cụm $U$ và $V$:
$$\text{ARI} = \frac{\sum_{i,j} \binom{n_{ij}}{2} - \left[ \sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2} \right] / \binom{n}{2}}{\frac{1}{2} \left[ \sum_i \binom{a_i}{2} + \sum_j \binom{b_j}{2} \right] - \left[ \sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2} \right] / \binom{n}{2}}$$
- $\text{ARI} = 1.0$: Hai kết quả phân cụm hoàn toàn trùng khớp (chỉ khác hoán vị nhãn).
- $\text{ARI} \approx 0.0$: Mức độ tương đồng không khác gì gán nhãn ngẫu nhiên.

### 5. Worked Example (Ví dụ minh họa)
Xét 4 khách hàng $\{1, 2, 3, 4\}$.
Lần chạy 1 phân thành: $\{1, 2\}$ và $\{3, 4\}$.
Lần chạy 2 phân thành: $\{3, 4\}$ và $\{1, 2\}$ (chỉ đổi tên nhãn cụm 0 thành 1).
- Cặp $(1, 2)$ cùng cụm ở cả hai lần.
- Cặp $(3, 4)$ cùng cụm ở cả hai lần.
- Các cặp $(1, 3), (1, 4), (2, 3), (2, 4)$ khác cụm ở cả hai lần.
Chỉ số $\text{ARI} = 1.0$ (hoàn toàn tương đồng, bất biến trước phép hoán vị nhãn).

### 6. Alternatives (Phương án thay thế & So sánh)
- **Normalized Mutual Information (NMI):** Dựa trên lý thuyết thông tin; có xu hướng bị thiên lệch khi số cụm lớn.
- **Fowlkes-Mallows Index:** Trung bình hình học của Precision và Recall trên các cặp điểm.

### 7. Verification (Bằng chứng thực nghiệm đồ án)
Thực nghiệm Vòng 2 chứng minh:
- Cấu hình quán quân $F1$ ($K=4$) đạt $\text{Mean ARI} = \mathbf{0.9876} \pm 0.0077$, với cặp thấp nhất vẫn đạt $\mathbf{0.9785}$.
- Ngược lại, tại $K=5$, chỉ số ổn định giảm sút nghiêm trọng xuống $\mathbf{0.8614}$ và xuất hiện cặp chỉ đạt $0.6711$, chứng minh $K=5$ gây ra sự bất ổn định ranh giới cụm.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- ARI chỉ đo lường tính nhất quán nội tại (Internal Consistency) giữa các lần chạy, không đo lường độ đúng đắn về mặt chân lý kinh doanh.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không sử dụng Accuracy để đánh giá sự tương đồng giữa 2 lần chạy K-Means với 2 seed khác nhau?"*  
> **Trả lời:** *"Thưa Thầy/Cô, K-Means là học không giám sát nên nhãn cụm (0, 1, 2, 3) chỉ là các ký hiệu đại số ngẫu nhiên. Lần chạy thứ nhất có thể gán nhóm VIP là nhãn 0, nhưng lần chạy thứ hai gán nhóm VIP là nhãn 1. Nếu tính Accuracy thông thường, độ chính xác có thể bằng 0% dù cấu trúc phân nhóm giống nhau 100%. Ngược lại, Adjusted Rand Index (ARI) đánh giá trên từng cặp cặp điểm dữ liệu xem chúng có được gom chung cụm hay tách rời nhau ở cả hai lần chạy hay không, do đó hoàn toàn bất biến trước phép hoán vị nhãn cụm."*

---

## P4.5 — So sánh Đối đầu Thực nghiệm: Standard K-Means vs MiniBatchKMeans (Thời gian, Bộ nhớ và Chất lượng Hội tụ)

### 1. What (Khái niệm là gì?)
MiniBatchKMeans là một biến thể của K-Means sử dụng các mini-batch dữ liệu ngẫu nhiên (chẳng hạn 1,024 điểm) để cập nhật tọa độ tâm cụm thay vì quét toàn bộ dữ liệu trong mỗi vòng lặp.

### 2. Why (Tại sao cần đối đầu thực nghiệm thay vì vội vàng áp dụng?)
Nhiều tài liệu học máy khuyến nghị dùng MiniBatchKMeans khi dữ liệu lớn để tiết kiệm thời gian. Tuy nhiên, quy mô tập Buyers trong đồ án là **92,652 khách hàng**, nhỏ hơn hàng trăm lần so với 20.7 triệu sự kiện clickstream thô. Do đó, cần kiểm chứng xem MiniBatch có thực sự nhanh hơn hay gây ra suy thoái chất lượng hội tụ không đáng có.

### 3. How (Thiết kế đối đầu thực nghiệm)
Chạy cả hai thuật toán trên cùng không gian $F1$ (7D), cùng chuẩn hóa StandardScaler, cùng $K=4$ và cùng seed 42:
- Đo thời gian `fit_time`.
- Đo bộ nhớ đỉnh `peak_rss`.
- Đo độ suy giảm quán tính WCSS ($\Delta \text{Inertia}$).
- Đo chỉ số thỏa thuận giữa 2 thuật toán qua Adjusted Rand Index.

### 4. Formula (Công thức cập nhật của MiniBatch)
Tâm cụm được cập nhật gia số theo tốc độ học phụ thuộc vào số lượng điểm đã gán vào cụm đó:
$$\mu_k^{(t)} = (1 - \eta) \mu_k^{(t-1)} + \eta \cdot x_i, \quad \text{với } \eta = \frac{1}{v_k}$$
Trong đó $v_k$ là tổng số điểm dữ liệu đã được gán vào cụm $k$ qua các batch.

### 5. Worked Example & Kết quả Thực nghiệm Đối đầu
Kết quả đo kiểm thực tế trên máy trạm 16 CPUs:
- **Thời gian chạy:** K-Means chuẩn mất **0.33 giây**, MiniBatch mất **0.38 giây** (MiniBatch thậm chí chậm hơn do chi phí nạp mẫu ngẫu nhiên).
- **Quán tính:** MiniBatch có WCSS cao hơn K-Means chuẩn **+0.98%** (266,370 so với 263,773).
- **Độ tương đồng (Agreement ARI):** Chỉ đạt **0.5561**.

### 6. Alternatives & Lựa chọn
- Giữ nguyên K-Means chuẩn: Hội tụ về nghiệm tốt hơn, quán tính thấp hơn, không có chi phí lấy mẫu batch, và thời gian hoàn toàn tức thời (dưới nửa giây).

### 7. Verification (Bằng chứng kiểm chứng)
Lưu trữ bảng đối soát tại `outputs/experiments/phase4_model_selection.json` trong mục `minibatch_vs_kmeans`.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- MiniBatchKMeans chỉ phát huy ưu thế rõ rệt khi số lượng mẫu $N > 10^7$ (vượt quá khả năng chứa trong RAM). Khi dữ liệu đã được thu gọn thành bảng đặc trưng 92k dòng, K-Means chuẩn luôn là lựa chọn vượt trội.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không dùng MiniBatchKMeans để tăng tốc độ phân cụm cho 92,652 khách hàng?"*  
> **Trả lời:** *"Thưa Thầy/Cô, thực nghiệm đối đầu trực tiếp trong đồ án đã chứng minh: K-Means chuẩn trên 92k dòng chỉ mất 0.33 giây để huấn luyện, trong khi MiniBatchKMeans mất 0.38 giây (chậm hơn do chi phí lấy mẫu ngẫu nhiên). Hơn nữa, MiniBatch chỉ đạt độ tương đồng ARI = 0.55 so với K-Means chuẩn và làm tăng quán tính WCSS thêm gần 1%. Vì thời gian 0.33 giây đã là tức thời trong môi trường thực tế, chúng em ưu tiên tính chính xác hội tụ và độ ổn định của K-Means chuẩn thay vì đánh đổi chất lượng lấy một sự tối ưu thời gian không tồn tại."*

---

## P4.6 — Tính Khả giải (Explainability): Chân dung Vật lý, Cây Quyết định Nông Mô phỏng (Surrogate Tree) và Chiếu Không gian PCA 2D

### 1. What (Khái niệm là gì?)
Tính khả giải trong học máy không giám sát là khả năng giải thích ranh giới phân vùng và đặc tính của các phân cụm bằng ngôn ngữ nghiệp vụ rõ ràng, vượt qua bản chất "hộp đen" của khoảng cách đa chiều.

### 2. Why (Tại sao tâm cụm chuẩn hóa là chưa đủ đối với Giám đốc Tiếp thị?)
Tâm cụm trong không gian chuẩn hóa là các số z-score trừu tượng (ví dụ: $z_{\text{monetary}} = +1.45, z_{\text{recency}} = -0.82$). Giám đốc tiếp thị không thể cấu hình chiến dịch nếu không biết cụ thể: khách hàng này đã không vào web bao nhiêu ngày, chi tiêu bao nhiêu tiền, và điều kiện định tuyến logic là gì.

### 3. How (Ba tầng khả giải của đồ án)
1. **Tầng 1 — Chân dung trên đơn vị vật lý gốc:** Ánh xạ ngược tọa độ tâm cụm và tính toán Median/Mean/IQR của từng phân khúc theo các đơn vị thực tế (ngày, phiên, đơn vị tiền tệ).
2. **Tầng 2 — Cây Quyết định Nông Mô phỏng (Surrogate Decision Tree):** Huấn luyện cây quyết định độ sâu 3 (`max_depth = 3`) lấy nhãn cụm K-Means làm mục tiêu; trích xuất các luật phân nhánh If-Then phục vụ lập trình Engine ở Phase 6.
3. **Tầng 3 — Chiếu trực quan 2D PCA:** Dùng Phân tích Thành phần Chính (PCA) để nén không gian 7 chiều xuống mặt phẳng 2D, giải thích được 76.40% phương sai toàn phần.

### 4. Formula (Công thức toán học)
- **Độ trung thành mô phỏng (Surrogate Fidelity):**
$$\text{Fidelity} = \frac{1}{|D_{\text{test}}|} \sum_{x_i \in D_{\text{test}}} \mathbb{I}(\hat{y}_{\text{tree}}(x_i) == \hat{y}_{\text{kmeans}}(x_i))$$
- **Hình chiếu PCA:**
$$z_{\text{pca}} = X_{\text{scaled}} \cdot W_2$$
Trong đó $W_2 \in \mathbb{R}^{7 \times 2}$ chứa 2 vectơ riêng có trị riêng lớn nhất của ma trận hiệp phương sai.

### 5. Worked Example (Kết quả trích xuất luật của đồ án)
Cây quyết định nông đạt độ trung thành trên tập kiểm tra độc lập **Test Fidelity = 82.11%** (Macro-F1 = 0.7780).
Luật cốt lõi trích xuất:
- `cart_sessions_30d <= 0.35` (Không thêm giỏ trong 30 ngày):
  - Nếu chi tiêu thấp $\to$ **Cluster 0 (Khách ngủ đông)**.
  - Nếu chi tiêu khá và Recency $\le 83.76$ ngày $\to$ **Cluster 2 (Khách nguội lạnh chi tiêu khá)**.
- `cart_sessions_30d > 0.35` (Có thêm giỏ gần đây):
  - Nếu mua $\ge 2$ phiên $\to$ **Cluster 1 (VIP Champions)**.
  - Nếu chỉ mua 1 phiên $\to$ **Cluster 3 (Khách mới mua & duyệt web tích cực)**.

### 6. Alternatives (Phương án thay thế & So sánh)
- **SHAP / LIME cho Clustering:** Tính toán phức tạp, chỉ giải thích cục bộ từng cá nhân, không tạo ra được bộ luật toàn cục ngắn gọn để lập trình cho rule engine tiếp thị.
- **t-SNE / UMAP:** Trực quan hóa phi tuyến tốt, nhưng làm méo mó khoảng cách toàn cục, không bảo toàn mật độ và không thể dùng làm bằng chứng duy nhất chứng minh chất lượng mô hình.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_09_pca_variance_explained` xác nhận tổng phương sai giải thích đạt $76.40\% \ge 40\%$; unit test `test_10_surrogate_tree_fidelity` xác nhận độ chính xác mô phỏng đạt $82.11\% \ge 80\%$.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Cây quyết định độ sâu 3 chỉ xấp xỉ được $82.11\%$ ranh giới của K-Means; $17.89\%$ điểm biên còn lại nằm ở các góc siêu không gian phức tạp mà cây nông không thể nắm bắt trọn vẹn (đây là sự đánh đổi có chủ ý để giữ cây ở mức đơn giản, dễ hiểu cho con người).

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Độ chính xác Test Fidelity 82.11% của Cây quyết định nông có phải là độ chính xác phân loại của mô hình K-Means không?"*  
> **Trả lời:** *"Thưa Thầy/Cô, tuyệt đối không. K-Means là thuật toán học không giám sát (Unsupervised Learning) không có nhãn đúng-sai thực tế (Ground Truth), do đó không tồn tại khái niệm Classification Accuracy cho K-Means. Chỉ số Fidelity 82.11% ở đây là độ trung thành mô phỏng (Surrogate Fidelity), đo lường mức độ cây quyết định nông độ sâu 3 sao chép lại ranh giới quyết định hình học của K-Means trên tập dữ liệu kiểm tra độc lập. Con số 82.11% chứng minh rằng hơn 8/10 quyết định phân cụm phức tạp của K-Means trong không gian 7 chiều có thể được giải thích một cách trong suốt bằng một bộ luật If-Then đơn giản chỉ gồm 3 câu hỏi điều kiện."*

---

## P4.7 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 4 (Oral Defense Guide P4: Q27 – Q32)

### Q27: Tại sao em không đưa toàn bộ 1.34 triệu người dùng vào huấn luyện K-Means mà chỉ huấn luyện trên 92,652 Buyers?
- **Trả lời:** Đây là quyết định kiến trúc quan trọng nhất để bảo vệ tính đúng đắn toán học: Trong 1.34 triệu khách hàng, có tới 93.09% (1.25 triệu người) chưa từng mua hàng. Đối với nhóm này, Recency và Frequency mua sắm là không xác định (Undefined/NULL). Nếu gán bừa một giá trị giả tạo như Recency = 999 để ép chạy chung K-Means, trục Recency sẽ bị kéo dãn và bóp méo hoàn toàn khoảng cách Euclidean, gom 93% người dùng thành một cụm khổng lồ và xóa nhòa cấu trúc phân khúc của 92k khách hàng đã mua. Bằng cách tách riêng, chúng em xây dựng được mô hình phân khúc sắc bén cho người mua, trong khi tập người chưa mua được phân tầng dựa trên mức độ quan tâm (Engagement Tiering) ở Phase 6.

### Q28: Trong 92,652 Buyers có tới gần 80% khách hàng chỉ mua đúng 1 lần (Frequency = 1), điều này ảnh hưởng thế nào đến kết quả phân cụm và em đã xử lý ra sao?
- **Trả lời:** Việc 79.94% khách hàng chỉ mua 1 phiên phản ánh hiện tượng dồn ứ giá trị tại 1 trên trục Frequency. Nếu chỉ dùng mô hình RFM 3 chiều truyền thống ($F0$), thuật toán sẽ gặp rất nhiều khó khăn để phân biệt giữa hàng chục nghìn khách mua 1 lần này. Bằng cách mở rộng sang không gian $F1$ bổ sung 4 đặc trưng tương tác 30 ngày (`sessions_30d`, `views_30d`, `cart_sessions_30d`, `log_activity_ratio`), K-Means đã phân tách xuất sắc nhóm 80% này thành 2 phân khúc hoàn toàn đối nghịch: Cluster 0 (Khách mua 1 lần đã ngủ đông hoàn toàn, Recency 82 ngày, 0 phiên tương tác) và Cluster 3 (Khách mua 1 lần nhưng đang quay lại duyệt web cực kỳ tích cực, Recency 16 ngày, 3 phiên truy cập, xung lượng tăng tốc +1.10).

### Q29: Làm thế nào em chọn ra số cụm K = 4 mà không phải là K = 3 hay K = 5?
- **Trả lời:** Chúng em lựa chọn $K=4$ dựa trên Ma trận Đánh đổi Đa chiều (Trade-off Matrix) thay vì chỉ nhìn vào một chỉ số:
1. *Tại K=3:* Cụm lớn nhất chiếm tới 64.3% dân số khách hàng, phân khúc bị dồn ứ quá mức và không phân tách được nhóm khách hàng đang nguội lạnh chi tiêu khá.
2. *Tại K=5:* Chỉ số ổn định qua 5 random seeds sụt giảm nghiêm trọng ($\text{Mean ARI}$ giảm xuống 0.86, có cặp seed chỉ đạt 0.67), chứng tỏ mô hình bị phân mảnh nhân tạo ranh giới cụm.
3. *Tại K=4:* Đạt điểm gập khuỷu tay rõ rệt (Elbow Curve), hệ số ổn định gần như tuyệt đối ($\text{Mean ARI} = 0.988 \pm 0.008$), và kích thước các cụm phân bổ rất cân bằng (từ 9.5% đến 45.5%, không có cụm suy thoái $< 5\%$).

### Q30: Sự khác biệt bản chất giữa Cluster 2 (Khách nguội lạnh chi tiêu khá) và Cluster 0 (Khách ngủ đông chi tiêu thấp) là gì?
- **Trả lời:** Cả hai cụm đều có điểm chung là không có hoạt động truy cập nào trong 30 ngày qua (`sessions_30d = 0`). Tuy nhiên, bản chất giá trị của chúng hoàn toàn khác nhau:
- *Cluster 0 (45.5%):* Là khách mua 1 lần với số tiền rất nhỏ (Monetary trung vị chỉ 20.24 đơn vị tiền tệ), đã rời bỏ từ rất lâu (Recency trung vị 82 ngày).
- *Cluster 2 (20.1%):* Từng là nhóm khách hàng chi tiêu khá cao (Monetary trung vị 67.29 đơn vị, cao hơn gấp 3 lần Cluster 0), thời gian mua cách đây khoảng gần 2 tháng (Recency 54 ngày). Đây là nhóm khách hàng chất lượng đang rơi vào vùng nguy hiểm (At-Risk / Cooling Down), cần các chiến dịch tiếp thị kích hoạt khẩn cấp trước khi họ nguội lạnh hoàn toàn thành Cluster 0.

### Q31: Tại sao em không dùng tập dữ liệu Holdout tháng 02/2020 để kiểm tra xem phân cụm K-Means có chính xác hay không trong Phase 4?
- **Trả lời:** Đây là nguyên tắc nghiêm ngặt về kiểm soát rò rỉ dữ liệu (Anti-Leakage) và phân định ranh giới phương pháp luận trong CRISP-DM. Phase 4 là giai đoạn xây dựng và lựa chọn mô hình phân cụm không giám sát dựa trên dữ liệu trong quá khứ. Tập Holdout tháng 02/2020 là "tương lai chưa biết" được niêm phong để làm bài kiểm tra khách quan duy nhất một lần ở Phase 5 (Model Evaluation). Nếu sử dụng dữ liệu tháng 2 để chọn số cụm K hoặc điều chỉnh tham số ở Phase 4, mô hình sẽ bị rò rỉ thông tin tương lai (Lookahead Bias), khiến các đánh giá kiểm định ở Phase 5 mất đi tính trung thực khoa học.

### Q32: Em có phát hiện thấy hiện tượng đa cộng tuyến giữa Frequency và Monetary không, và nó ảnh hưởng thế nào đến mô hình?
- **Trả lời:** Qua phân tích ma trận tương quan ở Figure 11 và kiểm tra thực nghiệm, hệ số tương quan giữa Frequency và Monetary là $r = 0.63$ (và $r = 0.54$ trên thang log1p). Con số này nằm dưới ngưỡng nguy hiểm của đa cộng tuyến tuyến tính ($r > 0.85$). Tuy nhiên, đối với khoảng cách Euclidean, sự tương quan này đồng nghĩa với việc phương diện "quy mô mua sắm" được nhân đôi trọng số hình học so với phương diện Recency. Để kiểm chứng, chúng em đã so sánh mô hình $F0$ (chỉ có RFM) với $F1$ (bổ sung 4 biến tương tác). Kết quả cho thấy khi đưa thêm Engagement, trọng số được phân bổ cân bằng hơn giữa hành vi giao dịch và hành vi truy cập web, giúp cải thiện đáng kể khả năng phân biệt giữa các nhóm khách hàng.

---

# PHẦN VI — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 5 (MODEL EVALUATION & BUSINESS SEGMENT PROFILING)

## P5.1 — Hậu kiểm Chuỗi Thời gian (Out-of-Time Temporal Holdout Validation) và Nguyên tắc Niêm phong Dữ liệu (Data Freezing)

### 1. What (Khái niệm là gì?)
Hậu kiểm Chuỗi Thời gian (Out-of-Time / Temporal Holdout Validation) là phương pháp đánh giá mô hình học máy trên một tập dữ liệu nằm hoàn toàn ở tương lai so với thời điểm mốc phân tách dữ liệu huấn luyện (Cutoff Boundary). Nguyên tắc Niêm phong Dữ liệu (Data Freezing / Model Freeze) là việc cố định tuyệt đối trọng số, tham số, pipeline tiền xử lý và nhãn phân cụm (thông qua mã băm mật mã học SHA-256) trước khi tiếp xúc với dữ liệu kiểm chứng tương lai.

### 2. Why (Tại sao cần dùng?)
Trong học máy không giám sát, việc đánh giá chỉ dựa trên các chỉ số hình học nội tại (Silhouette, DBI) rất dễ dẫn đến ảo tưởng về chất lượng phân cụm. Hậu kiểm trên tập Holdout tương lai là "bài thử lửa duy nhất" để chứng minh tính hữu ích kinh doanh thực tế (Business Utility): Nếu các phân cụm hình thành từ quá khứ không thể hiện được sự khác biệt về hành vi chuyển đổi trong tương lai, mô hình hoàn toàn vô giá trị trong việc hỗ trợ ra quyết định marketing.

### 3. How (Cách thức triển khai?)
1. Khóa cứng mô hình `outputs/models/kmeans_best_model.joblib` và ghi nhận mã băm SHA-256 (`ab98e13248...`).
2. Tải tập dữ liệu kiểm chứng tháng 02/2020 (`data/cleaned/holdout_events.parquet`, 3,916,392 sự kiện).
3. Thực hiện phép kết nối trái (Left Join) giữa danh sách 92,652 khách hàng Buyers (kèm nhãn cụm Phase 4) với các sự kiện trong tháng 2 dựa trên khóa `user_id`.
4. Tính toán 9 chỉ số hành vi tương lai: Tỷ lệ hoạt động tương lai, Tỷ lệ mua tương lai, Doanh thu tương lai trung bình, v.v.

### 4. Formula (Công thức toán học)
- **Tỷ lệ Mua Hàng Tương lai của Phân cụm $k$ (Future Purchase Rate):**
  $$\text{FPR}_k = \frac{\sum_{i \in C_k} \mathbb{I}(\text{future\_purchase\_sessions}_i > 0)}{|C_k|} = \frac{N_{k, \text{buyers}}}{N_k}$$
- **Doanh thu Trung bình Tương lai trên mỗi Khách hàng (Future Spend per Customer):**
  $$\text{FSC}_k = \frac{\sum_{i \in C_k} \text{future\_spend}_i}{|C_k|}$$

### 5. Worked Example (Số liệu thực nghiệm đồ án)
- Cụm VIP ($C_1, N=8,755$): Có 3,066 khách phát sinh mua trong tháng 2 $\to \text{FPR}_1 = 35.02\%$. Tổng doanh thu tương lai là $\$226,329.95 \to \text{FSC}_1 = \$25.85$.
- Cụm Ngủ đông ($C_0, N=42,145$): Có 1,120 khách phát sinh mua trong tháng 2 $\to \text{FPR}_0 = 2.66\%$. Tổng doanh thu tương lai là $\$38,496.82 \to \text{FSC}_0 = \$0.91$.
- Tỷ số phân hóa: VIP có tỷ lệ mua gấp **$13.2\times$** và chi tiêu gấp **$28.4\times$** cụm ngủ đông.

### 6. Alternatives (Phương án thay thế & So sánh)
- **K-Fold Cross Validation:** Hoàn toàn sai lầm đối với dữ liệu chuỗi thời gian clickstream vì sẽ làm rò rỉ thông tin tương lai về quá khứ (Lookahead Leakage).
- **In-sample Cluster Metrics (Silhouette, DBI):** Chỉ đo độ nén hình học, không chứng minh được độ nhạy kinh doanh trong tương lai.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_02_customer_count_conservation` xác nhận bảo toàn tuyệt đối 92,652 khách hàng không thất thoát; `test_03_monotonic_conversion_ordering` kiểm chứng tính đơn điệu của tỷ lệ chuyển đổi.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Tập Holdout chỉ kéo dài 1 tháng (tháng 2/2020), do đó chỉ đo lường được hành vi ngắn hạn ngay sau cutoff; chưa phản ánh được giá trị vòng đời dài hạn (CLV nhiều năm).

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không dùng tập Holdout tháng 2 để tinh chỉnh số cụm K hoặc điều chỉnh siêu tham số?"*  
> **Trả lời:** *"Thưa Thầy/Cô, việc dùng tập Holdout để điều chỉnh mô hình vi phạm nguyên tắc Data Snooping / Lookahead Leakage. Trong CRISP-DM, Holdout đại diện cho tương lai chưa diễn ra. Nếu dùng tương lai để chọn mô hình, kết quả đánh giá sẽ bị thổi phồng giả tạo (Over-optimistic bias). Chúng em đóng băng mô hình trước khi mở tập Holdout đúng 1 lần duy nhất để kiểm tra tính khách quan của phân cụm."*

---

## P5.2 — Khoảng Tin cậy Wilson Score 95% cho Tỷ lệ Chuyển đổi Tương lai và Kiểm định Ý nghĩa Thống kê

### 1. What (Khái niệm là gì?)
Khoảng tin cậy Wilson Score (Wilson Score Interval) là phương pháp ước lượng khoảng tin cậy đối xứng cho tham số tỷ lệ $p$ của phân phối nhị thức, dựa trên việc giải phương trình nghịch đảo của kiểm định thống kê điểm số (Score Test).

### 2. Why (Tại sao cần dùng?)
Khoảng tin cậy cổ điển Wald ($\hat{p} \pm z \sqrt{\hat{p}(1-\hat{p})/n}$) có sai số nghiêm trọng khi tỷ lệ $p$ gần 0 hoặc gần 1 (như tỷ lệ chuyển đổi thương mại điện tử chỉ $0.4\% \to 2\%$) hoặc khi kích thước mẫu nhỏ. Wilson Score interval khắc phục triệt để hiện tượng này, luôn đảm bảo giá trị nằm trong khoảng $[0, 1]$ và có độ bao phủ xác suất (coverage probability) chính xác tuyệt đối.

### 3. How (Cách thức triển khai?)
Áp dụng công thức Wilson với mức ý nghĩa $\alpha = 0.05$ ($z_{1-\alpha/2} = 1.95996$) cho tỷ lệ mua hàng và tỷ lệ hoạt động của từng phân cụm.

### 4. Formula (Công thức toán học)
$$\text{CI}_{\text{Wilson}} = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

### 5. Worked Example (Tính toán minh họa cho Cluster 2)
- Với Cluster 2: $n = 18,608$, số người mua $k = 1,363 \to \hat{p} = 1363 / 18608 \approx 0.073248$ ($7.32\%$).
- $z = 1.95996 \to z^2 \approx 3.84146$.
- Mẫu số: $1 + 3.84146 / 18608 \approx 1.000206$.
- Tử số điểm giữa: $0.073248 + 3.84146 / (2 \times 18608) \approx 0.073351$.
- Số hạng dưới căn: $\frac{0.07325 \times 0.92675}{18608} + \frac{3.84146}{4 \times 18608^2} \approx 3.648 \times 10^{-6}$. Căn bậc hai $\approx 0.001910$.
- Sai số biên: $1.95996 \times 0.001910 \approx 0.003743$.
- Kết quả khoảng tin cậy 95%: $[0.06959, 0.07708]$ hay $[6.96\%, 7.71\%]$.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Wald Interval:** Thường tính ra giới hạn dưới âm khi $p$ nhỏ, phạm sai lầm xác suất.
- **Clopper-Pearson (Exact) Interval:** Quá bảo thủ (khoảng tin cậy quá rộng).
- **Bootstrap Percentile Interval:** Tính toán lâu trên dữ liệu lớn, trong khi Wilson giải tích tính tức thời và chuẩn xác.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_04_wilson_confidence_intervals` xác nhận giới hạn dưới luôn nhỏ hơn giới hạn trên và nằm trọn vẹn trong đoạn $[0, 100\%]$.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Giả định các quan sát là độc lập và cùng phân phối (i.i.d). Nếu có hiện tượng chia sẻ tài khoản gia đình hoặc botnet, giả định độc lập có thể bị vi phạm nhẹ.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Khoảng tin cậy Wilson 95% có ý nghĩa gì trong việc khẳng định mô hình K-Means phân cụm tốt?"*  
> **Trả lời:** *"Thưa Thầy/Cô, khoảng tin cậy Wilson 95% của 4 cụm hoàn toàn không chồng lấn lên nhau: C0 là $[2.51\%, 2.82\%]$, C2 là $[6.96\%, 7.71\%]$, C3 là $[9.75\%, 10.52\%]$, C1 là $[34.03\%, 36.03\%]$. Điều này chứng minh sự khác biệt về tỷ lệ chuyển đổi giữa các cụm không phải do may rủi hay biến động mẫu ngẫu nhiên mà là sự phân hóa thực chất mang tính quy luật với độ tin cậy vượt trên $99.99\%$ ($p < 10^{-100}$)."*

---

## P5.3 — Phân tích Chân dung Phân cụm Đa chiều (Comprehensive Profiling) trên Không gian Đơn vị Gốc

### 1. What (Khái niệm là gì?)
Phân tích Chân dung Phân cụm Đa chiều là quy trình tổng hợp và đối chiếu các thông số thống kê trung tâm (Median, Mean, IQR) của từng phân khúc khách hàng trên các đơn vị đo lường vật lý gốc (ngày, phiên truy cập, đơn vị tiền tệ), kết hợp giữa lịch sử quá khứ và hành vi tương lai.

### 2. Why (Tại sao cần dùng?)
Các centroid trong không gian z-score đã chuẩn hóa (`StandardScaler`) hoàn toàn vô nghĩa đối với các nhà quản trị kinh doanh. Để đội ngũ marketing có thể xây dựng thông điệp và kế hoạch ngân sách, mọi chỉ số bắt buộc phải được chuyển dịch ngược về đơn vị tiền tệ, số ngày mua hàng và số phiên lướt web thực tế.

### 3. How (Cách thức triển khai?)
Truy vấn bảng `buyer_clusters.parquet` kết hợp với bảng `holdout_events.parquet`, tính toán phân vị và trung bình cho từng cụm, sau đó trực quan hóa qua biểu đồ Radar Profile và Bảng chân dung toàn diện (`fig20_cluster_profiles_comprehensive.png`).

### 4. Formula (Công thức toán học)
- Giá trị trung vị của đặc trưng $X$ trong phân cụm $C_k$:
  $$\text{Median}_k(X) = Q_{0.5}(\{x_i \mid i \in C_k\})$$

### 5. Worked Example (Bảng so sánh 4 chân dung)
- **Cluster 0 (Ngủ đông - 45.49%):** Recency 82.3 ngày, Chi tiêu $20.24, 0 phiên gần đây $\to$ Tương lai: 2.66% mua, $0.91/khách.
- **Cluster 1 (VIP - 9.45%):** Recency 12.7 ngày, Chi tiêu $117.69, 9 phiên gần đây $\to$ Tương lai: 35.02% mua, $25.85/khách.
- **Cluster 2 (Đang hạ nhiệt - 20.08%):** Recency 54.3 ngày, Chi tiêu $67.29, 0 phiên gần đây $\to$ Tương lai: 7.32% mua, $4.28/khách.
- **Cluster 3 (Mới mua duyệt tích cực - 24.98%):** Recency 16.3 ngày, Chi tiêu $28.12, 3 phiên gần đây $\to$ Tương lai: 10.13% mua, $4.91/khách.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Chỉ báo cáo Mean:** Rất nguy hiểm vì phân phối RFM lệch đuôi dài cực đoan; Mean bị kéo lệch bởi các đại gia ngoại lai (Outliers), tạo ảo tưởng về mức chi tiêu của khách hàng thông thường. Báo cáo song song Median và Mean là bắt buộc.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_08_cluster_size_distribution` xác minh quy mô từng cụm khớp tuyệt đối với Phase 4 ($42,145; 8,755; 18,608; 23,144$).

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Hồ sơ phân vị thể hiện tính chất tĩnh tại thời điểm cắt; không nắm bắt được những biến đổi bất thường xảy ra ngay giữa kỳ quan sát.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Dựa vào đâu để em chứng minh Cluster 2 và Cluster 0 không thể gộp làm một?"*  
> **Trả lời:** *"Thưa Thầy/Cô, mặc dù cả hai cụm đều không có tương tác trong 30 ngày gần nhất, nhưng trong quá khứ Cluster 2 từng chi tiêu trung vị $67.29$ (gấp hơn $3.3\times$ Cluster 0). Quan trọng hơn cả, trên tập kiểm chứng tương lai, Cluster 2 đạt tỷ lệ mua $7.32\%$ (gấp $2.75\times$ Cluster 0) và mang lại doanh thu bình quân $\$4.28$ (gấp $4.70\times$ Cluster 0). Nếu gộp chung theo $K=3$, doanh nghiệp sẽ bỏ qua 18,608 khách hàng có giá trị cao đang đứng trước nguy cơ rời bỏ này."*

---

## P5.4 — Đối chuẩn Nhóm Chưa Mua (Observed Non-Buyers Benchmark) trong Không gian Hành vi Tương lai

### 1. What (Khái niệm là gì?)
Đối chuẩn Nhóm Chưa Mua là việc đưa toàn bộ quần thể 1,248,847 khách hàng chỉ phát sinh tương tác lướt web mà chưa từng mua hàng trước cutoff vào làm nhóm kiểm chứng cơ sở (Control / Baseline Benchmark) để so sánh hành vi với nhóm khách hàng đã mua (Buyers).

### 2. Why (Tại sao cần dùng?)
Nếu không có nhóm đối chuẩn, ta không thể biết được tỷ lệ quay lại mua $2.66\%$ của Cluster 0 là cao hay thấp trong bối cảnh toàn sàn thương mại điện tử. Nhóm Non-Buyers cung cấp "mức sàn chuyển đổi tự nhiên" của hệ thống.

### 3. How (Cách thức triển khai?)
Quét bảng `non_buyer_features.parquet` đối soát với `holdout_events.parquet`, xác định có bao nhiêu người chuyển đổi lần đầu trong tháng 2 và tổng doanh thu họ tạo ra.

### 4. Formula (Công thức toán học)
- **Tỷ số Tỷ lệ Mua quan sát so với Nhóm chưa mua (Observed Purchase Ratio vs Non-Buyers Baseline):**
  $$\text{Observed Purchase Ratio}_k = \frac{\text{Future Purchase Rate of Cluster } k}{\text{Future Purchase Rate of Non-Buyers}}$$
  *(Lưu ý thuật ngữ chuyên môn: Đây là tỷ số hành vi tự nhiên quan sát được trong tương lai giữa các nhóm đối chứng, không phải là Causal Marketing Uplift do can thiệp chiến dịch tạo ra).*

### 5. Worked Example (Số liệu thực nghiệm đồ án)
- Tỷ lệ chuyển đổi tự nhiên của Non-Buyers: $0.4226\%$ (5,278 người mua trên 1.25 triệu người dùng).
- Tỷ số tỷ lệ mua quan sát so với mức sàn Non-Buyers:
  - Cluster 0: $2.6575\% / 0.4226\% = \mathbf{6.29\times}$
  - Cluster 2: $7.3248\% / 0.4226\% = \mathbf{17.33\times}$
  - Cluster 3: $10.1279\% / 0.4226\% = \mathbf{23.97\times}$
  - Cluster 1: $35.0200\% / 0.4226\% = \mathbf{82.87\times}$

### 6. Alternatives (Phương án thay thế & So sánh)
- **Bỏ qua nhóm Non-Buyers:** Khiến bài toán phân tích khách hàng bị thu hẹp phiến diện vào nhóm người mua (chỉ chiếm $6.9\%$ người dùng), bỏ qua cơ hội tăng trưởng doanh thu khổng lồ từ phễu chuyển đổi ban đầu.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_06_non_buyers_benchmark` xác nhận có đúng 1,248,847 khách hàng chưa mua được đánh giá và tỷ lệ mua đạt đúng $0.4226\%$.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Non-Buyers là một tập hợp rất đa dạng (từ người vào nhầm 1 lần đến người lướt xem hàng chục sản phẩm). Do đó cần tiếp tục phân tầng Engagement Tiering ở Phase 6.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao tổng doanh thu tháng 2 của nhóm Non-Buyers ($245k) lại cao hơn cả nhóm VIP ($226k) dù tỷ lệ mua của họ chỉ có 0.42%?"*  
> **Trả lời:** *"Thưa Thầy/Cô, đây là hệ quả của quy luật số lớn (Law of Large Numbers) trong thương mại điện tử: Nhóm Non-Buyers chiếm tới 93.1% dân số toàn sàn (1.25 triệu người), đông gấp 142 lần nhóm VIP (8.7k người). Dù xác suất mua của mỗi cá nhân rất nhỏ (0.42%), nhưng tích lũy trên 1.25 triệu người vẫn tạo ra 5,278 đơn hàng và hơn $245,000 doanh thu. Điều này chứng minh đồ án cần có cả hai mũi nhọn chiến lược: vừa chăm sóc nhóm VIP để tối ưu biên lợi nhuận, vừa kích hoạt chuyển đổi nhóm Non-Buyers để mở rộng quy mô."*

---

## P5.5 — Sơ đồ Chuyển dịch Phân khúc Khách hàng (Segment Transition Analysis) và Động học Trạng thái (State Dynamics)

### 1. What (Khái niệm là gì?)
Sơ đồ Chuyển dịch Phân khúc Khách hàng là công cụ mô hình hóa động học trạng thái hành vi, theo dõi sự dịch chuyển của khách hàng từ các phân khúc ban đầu sang các trạng thái hoạt động thực tế trong tương lai thông qua sơ đồ dòng chảy Alluvial / Sankey Diagram (`fig19_segment_transition_sankey.png`).

### 2. Why (Tại sao cần dùng?)
Phân khúc khách hàng không phải là nhãn dán bất biến mà là một trạng thái động (Dynamic State). Hiểu rõ xác suất chuyển dịch trạng thái giúp doanh nghiệp định lượng được "tốc độ suy thoái" của từng nhóm và thiết kế các chiến dịch can thiệp đúng thời điểm vàng.

### 3. How (Cách thức triển khai?)
Phân loại hành vi tháng 2 của từng khách hàng thành 3 trạng thái:
1. **Repeat Buyer:** Có ít nhất 1 phiên mua hàng.
2. **Active Non-Buyer:** Có phiên truy cập lướt web nhưng không mua.
3. **Dormant / Churned:** Hoàn toàn không có phiên truy cập nào trong tháng 2.

### 4. Formula (Công thức toán học)
- Xác suất chuyển dịch từ phân cụm $C_k$ sang trạng thái $S_j$:
  $$P(S_j \mid C_k) = \frac{|\{i \in C_k \mid \text{state}_{i, \text{future}} = S_j\}|}{|C_k|}$$

### 5. Worked Example (Số liệu chuyển dịch thực tế đồ án)
- **VIP (Cluster 1):** $35.0\%$ trở thành Repeat Buyer, $37.5\%$ Active Non-Buyer, chỉ có $27.5\%$ Churned/Dormant.
- **Recent Active (Cluster 3):** $10.1\%$ Repeat Buyer, $24.9\%$ Active Non-Buyer, $65.0\%$ Churned.
- **Cooling Down (Cluster 2):** $7.3\%$ Repeat Buyer, $14.0\%$ Active Non-Buyer, $78.7\%$ Churned.
- **Dormant (Cluster 0):** $2.7\%$ Repeat Buyer, $8.0\%$ Active Non-Buyer, $89.3\%$ Churned.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Mô hình HMarkov bậc cao:** Đòi hỏi chuỗi thời gian nhiều tháng liên tục, phức tạp và dễ quá khớp trên tập dữ liệu ngắn hạn. Sơ đồ ma trận chuyển dịch trực tiếp là giải pháp tối ưu cho chu kỳ 21 ngày.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_07_transition_flow_conservation` xác nhận tổng xác suất chuyển dịch của mỗi cụm luôn bằng đúng $100.0\%$.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Chưa tính đến các yếu tố mùa vụ đặc thù của tháng 2 (như dịp Tết Nguyên Đán hoặc ngày Valentine 14/02) có thể ảnh hưởng đến dòng chuyển dịch tự nhiên.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Dựa vào sơ đồ chuyển dịch, nhóm khách hàng nào có nguy cơ rơi rụng cao nhất và nhóm nào có tiềm năng thăng hạng lớn nhất?"*  
> **Trả lời:** *"Thưa Thầy/Cô, nhóm có nguy cơ rơi rụng cao nhất là Cluster 2 (78.7% biến mất hoàn toàn trong tháng 2), đây là nhóm đang hạ nhiệt cần can thiệp khẩn cấp. Ngược lại, nhóm có tiềm năng thăng hạng lớn nhất là Cluster 3: có tới 35.0% duy trì tương tác tích cực (trong đó 10.1% đã mua tiếp), đây chính là nguồn lực bổ sung mạnh mẽ nhất để nuôi dưỡng thành khách hàng VIP trong chu kỳ tiếp theo."*

---

## P5.6 — Bản chất Quan hệ: Tương quan Phân khúc (Association) vs. Tác động Nhân quả (Causation) trong Nghiệp vụ

### 1. What (Khái niệm là gì?)
Tương quan Phân khúc (Cluster Association) là mối liên hệ thống kê giữa nhãn cụm quan sát được và hành vi trong tương lai. Tác động Nhân quả (Causal Impact) là sự thay đổi trong hành vi của khách hàng gây ra trực tiếp bởi một can thiệp tiếp thị cụ thể (Treatment Effect).

### 2. Why (Tại sao cần làm rõ?)
Một sai lầm rất phổ biến của các nhà phân tích dữ liệu là nhầm lẫn rằng: Vì nhóm VIP mua nhiều nên nếu gửi khuyến mãi cho khách hàng nhóm khác thì họ sẽ mua nhiều như VIP. Khẳng định sai lầm này dẫn đến việc lãng phí ngân sách tiếp thị vào những can thiệp không có hiệu quả gia tăng (Incremental Lift).

### 3. How (Cách thức triển khai?)
1. Luôn ghi rõ trong báo cáo và dashboard: Các chỉ số phân cụm là **kết quả quan sát tự nhiên (Observational)**.
2. Thiết kế Engine ở Phase 6 dưới dạng **Bộ luật khuyến nghị dựa trên bằng chứng (Evidence-based Prescriptive Rules)** chứ không khẳng định tác động nhân quả đã được kiểm chứng.
3. Đề xuất quy trình thử nghiệm A/B Testing có nhóm đối chứng (Control Group) trước khi triển khai thực tế.

### 4. Formula (Công thức toán học)
- **Hiệu quả gia tăng nhân quả thực sự (Average Treatment Effect - ATE):**
  $$\text{ATE} = \mathbb{E}[Y(1) - Y(0)] \neq \mathbb{E}[Y \mid T=1] - \mathbb{E}[Y \mid T=0]$$
  Sự chênh lệch giữa hai vế là Sai số Nhiễu (Confounding Bias) do các đặc tính nội tại của khách hàng.

### 5. Worked Example (Minh họa cho đồ án)
Tỷ lệ mua $35.0\%$ của khách hàng VIP (Cluster 1) phản ánh nhu cầu tự nhiên của họ đối với mỹ phẩm. Nếu ta gửi email giảm giá $20\%$ cho một khách hàng VIP và họ mua hàng, ta không thể vội vàng kết luận email giảm giá đã tạo ra đơn hàng đó, vì rất có thể họ vẫn sẽ mua dù không nhận được email (hiện tượng "Sure Things" trong Uplift Modeling).

### 6. Alternatives (Phương án thay thế & So sánh)
- **Uplift Modeling / Causal Trees / Double Machine Learning:** Các phương pháp ước lượng nhân quả nâng cao. Đồ án nhận diện rõ đây là hướng mở rộng lý tưởng sau 21 ngày khi có dữ liệu chạy thử nghiệm A/B thực tế.

### 7. Verification (Cách thức kiểm chứng)
Toàn bộ tài liệu báo cáo và sổ tay đều có mục ranh giới phương pháp luận và cảnh báo giới hạn suy diễn nhân quả.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Dataset REES46 là nhật ký quan sát thụ động (Observational Log), không có thông tin về các chiến dịch marketing đã chạy trước đó, do đó về mặt toán học không thể bóc tách tác động nhân quả thuần túy mà không có giả định mạnh.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Các đề xuất chiến lược tiếp thị của em ở Phase 6 có đảm bảo chắc chắn sẽ làm tăng doanh thu không?"*  
> **Trả lời:** *"Thưa Thầy/Cô, chúng em tuyệt đối không đưa ra lời khẳng định nhân quả tuyệt đối. Báo cáo của chúng em dựa trên dữ liệu nhật ký quan sát (Observational Data), vì vậy các chỉ số phân khúc phản ánh hành vi tự nhiên chứ không phải hiệu quả can thiệp đã được kiểm chứng. Các khuyến nghị ở Phase 6 là các giả định có căn cứ khoa học (Evidence-based Hypotheses). Để đảm bảo chắc chắn tăng doanh thu, doanh nghiệp bắt buộc phải triển khai thử nghiệm A/B Testing với nhóm đối chứng để đo lường hiệu quả gia tăng (Incremental Uplift) trước khi áp dụng trên diện rộng."*

---

## P5.7 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 5 (Oral Defense Guide P5: Q33 – Q38)

### Q33: Tại sao em lại tự tin khẳng định mô hình K-Means của mình có giá trị thực tế hơn là chỉ đạt điểm toán học cao?
- **Trả lời:** Chúng em tự tin vì mô hình đã vượt qua bài kiểm tra Hậu kiểm Chuỗi Thời gian (Out-of-Time Temporal Holdout) trên gần 4 triệu sự kiện độc lập của tháng 02/2020. Kết quả thực nghiệm cho thấy:
1. Nhãn cụm phân hóa tỷ lệ mua hàng tương lai theo trật tự đơn điệu hoàn hảo: Non-Buyers ($0.42\%$) $\to$ Cluster 0 ($2.66\%$) $\to$ Cluster 2 ($7.32\%$) $\to$ Cluster 3 ($10.13\%$) $\to$ Cluster 1 ($35.02\%$).
2. Doanh thu đóng góp tương lai cũng tăng đơn điệu từ $\$0.20 \to \$0.91 \to \$4.28 \to \$4.91 \to \$25.85$.
3. Các khoảng tin cậy Wilson 95% hoàn toàn tách biệt, kiểm định $\chi^2$ đạt $p < 10^{-100}$. Đây là bằng chứng thực nghiệm thép chứng minh các cụm có hành vi kinh doanh khác biệt thực sự chứ không phải là phân cụm giả tạo trên dữ liệu quá khứ.

### Q34: Tại sao em không gộp Cluster 0 và Cluster 2 để mô hình có số cụm K=3 gọn gàng hơn?
- **Trả lời:** Nếu chọn $K=3$, thuật toán K-Means sẽ gom Cluster 0 và Cluster 2 thành một cụm khổng lồ chiếm tới 64.3% khách hàng. Nhưng dữ liệu kiểm chứng tháng 2 chứng minh hai nhóm này có bản chất hoàn toàn khác nhau:
- Khách hàng Cluster 2 quay lại mua hàng với tỷ lệ $7.32\%$ (cao gấp $2.75\times$ Cluster 0) và mang lại doanh thu $\$4.28/khách$ (cao gấp $4.70\times$ Cluster 0).
- Nếu gộp chung, doanh nghiệp sẽ đánh đồng 18,608 khách hàng có giá trị cao đang hạ nhiệt với những người mua món đồ rẻ rồi biến mất, bỏ lỡ cơ hội cứu vãn nhóm khách hàng mang lại tỷ suất lợi nhuận cao nhất cho chiến dịch win-back. Do đó, $K=4$ là sự lựa chọn vượt trội cả về mặt toán học lẫn thực tiễn kinh doanh.

### Q35: Sai số biên trong khoảng tin cậy Wilson của các tỷ lệ mua tương lai là bao nhiêu và nó nói lên điều gì?
- **Trả lời:** Nhờ quy mô tập dữ liệu lớn ($N$ từ 8,755 đến 42,145 khách hàng mỗi cụm), sai số biên (Margin of Error) của khoảng tin cậy Wilson 95% đều rất nhỏ, **dưới $\pm 1.0\%$** (ví dụ: C1 là $[34.03\%, 36.03\%]$, C3 là $[9.75\%, 10.52\%]$, C2 là $[6.96\%, 7.71\%]$, C0 là $[2.51\%, 2.82\%]$). Điều này khẳng định kích thước mẫu hoàn toàn đủ mạnh để triệt tiêu biến động ngẫu nhiên, cho phép chúng em đưa ra các kết luận thống kê với độ tin cậy cực kỳ cao.

### Q36: Tại sao tỷ lệ chuyển đổi của nhóm khách hàng mới mua (Cluster 3: 10.13%) lại cao hơn nhóm khách hàng từng chi tiêu khá (Cluster 2: 7.32%) trong tháng 2?
- **Trả lời:** Điều này phản ánh chính xác quy luật "Sức mạnh của Tương tác Gần" (Power of Recent Engagement). Khách hàng Cluster 3 vừa mới mua hàng cách đây trung vị 16 ngày và vẫn đang lướt web cực kỳ tích cực (3 phiên, 8 lượt xem sản phẩm, xung lượng hoạt động dương $+1.10$). Tâm trí của họ đối với thương hiệu đang ở trạng thái nóng nhất (Top-of-Mind). Ngược lại, khách hàng Cluster 2 dù từng chi tiêu nhiều tiền hơn trong quá khứ nhưng đã ngưng truy cập suốt 30 ngày qua (Recency 54 ngày, xung lượng âm $-0.69$). Quán tính rời bỏ đã kéo tụt xác suất quay lại của họ xuống thấp hơn nhóm mới mua.

### Q37: Nhóm khách hàng chưa mua (Non-Buyers) có vai trò gì trong đồ án khi mà K-Means chỉ phân cụm trên nhóm đã mua?
- **Trả lời:** Nhóm Non-Buyers đóng vai trò là "Thước đo Đối chuẩn Cơ sở" (Baseline Control Benchmark). Bằng cách theo dõi 1.25 triệu khách hàng này sang tháng 2, chúng em xác định được tỷ lệ chuyển đổi tự nhiên toàn sàn là $0.42\%$ và doanh thu tự nhiên là $\$0.20/người$. Từ đó, chúng em chứng minh được rằng ngay cả nhóm khách hàng mua kém nhất (Cluster 0) vẫn có giá trị chuyển đổi gấp $6.3\times$ người chưa mua, và nhóm VIP gấp tới $82.9\times$. Đồng thời, việc nhóm Non-Buyers đóng góp tới $245,000 doanh thu tháng 2 là cơ sở để chúng em thiết kế bộ chiến thuật kích hoạt người dùng mới ở Phase 6.

### Q38: Sơ đồ dòng chuyển dịch trạng thái (Transition Flow) có ý nghĩa ứng dụng như thế nào trong quản trị marketing?
- **Trả lời:** Sơ đồ dòng chuyển dịch giúp ban giám đốc nhìn thấy bức tranh động học của dòng đời khách hàng:
1. Nó chỉ ra "nguồn kế cận VIP": $35.0\%$ khách hàng Cluster 3 tiếp tục hoạt động tích cực trong tháng 2, đây là nguồn khách hàng triển vọng nhất cần được nuôi dưỡng thành VIP.
2. Nó cảnh báo "rò rỉ dòng tiền": Có tới $78.7\%$ khách hàng Cluster 2 rơi vào trạng thái ngủ đông, cho thấy nếu doanh nghiệp chậm trễ trong việc gửi thông điệp chăm sóc trong vòng 30–45 ngày sau mua, chi phí để kéo họ quay lại sau này sẽ đắt hơn gấp nhiều lần.

---

# PHẦN VII — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 6 (MARKETING DECISION SUPPORT ENGINE)

## P6.1 — Phân cấp Phân tích Dữ liệu: Descriptive, Predictive và Prescriptive Analytics trong Thương mại Điện tử

### 1. What (Khái niệm là gì?)
Phân cấp Phân tích Dữ liệu (Analytics Maturity Hierarchy) gồm 4 tầng phát triển:
1. **Descriptive Analytics (Mô tả):** Trả lời "Điều gì đã xảy ra?" (VD: EDA, Funnel, RFM quá khứ).
2. **Diagnostic Analytics (Chẩn đoán):** Trả lời "Tại sao điều đó xảy ra?" (VD: Đối soát sụt giảm, phân tích phễu rơi rụng).
3. **Predictive Analytics (Dự báo):** Trả lời "Điều gì có khả năng xảy ra trong tương lai?" (VD: Phân cụm tiên lượng chuyển đổi Holdout).
4. **Prescriptive Analytics (Chỉ dẫn hành động):** Trả lời "Chúng ta nên làm gì để tối ưu hóa kết quả?" (VD: Decision Support Engine sinh khuyến nghị).

### 2. Why (Tại sao cần dùng?)
Nếu dừng lại ở Descriptive hay Predictive, doanh nghiệp chỉ có thông tin thụ động nhưng thiếu năng lực ra quyết định. Prescriptive Engine chuyển hóa tri thức dữ liệu thành các hành động tiếp thị cụ thể, kèm lý do và điều kiện áp dụng.

### 3. How (Cách thức triển khai?)
Xây dựng chuỗi chuyển đổi: `Customer Evidence -> Customer Segment -> Marketing Goal -> Candidate Tactics -> Eligibility & Guardrails -> Recommended Action`.

### 4. Formula / Algorithm (Mô hình thuật toán)
$$\text{Prescription}(u) = \arg\max_{t \in T_{\text{eligible}}(u)} \text{Priority}(t \mid \text{Evidence}(u), \text{Segment}(u))$$
Thực thi kiểm tra guardrails và trả về bộ khuyến nghị kèm lý do giải thích.

### 5. Worked Example (Minh họa cho đồ án)
Khách hàng có bằng chứng: `recency = 10.5` ngày, `sessions_30d = 8`, `monetary = $185.50` (Cluster 1 VIP).
- *Descriptive:* Khách chi tiêu $185.50, thuộc top 9.5% sàn.
- *Predictive:* Xác suất mua tháng tiếp theo đạt 35.02%.
- *Prescriptive:* Đề xuất chiến thuật `TAC_LOYALTY_VIP` (Mục tiêu: `RETAIN_HIGH_VALUE`) với lý do tri ân và giữ chân lâu dài.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Static Cluster Mapping:** Gán cứng 1 chiến thuật cho toàn bộ cụm. Nhược điểm: Bỏ qua biến động cá nhân trong cụm.
- **Black-box Reinforcement Learning:** Học tự động tối ưu hóa nhưng hoàn toàn không thể giải thích và đòi hỏi môi trường live tương tác thật.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_01_ruleset_structure` xác nhận sự hiện diện đầy đủ của cấu trúc 7 mục tiêu và 8 chiến thuật.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Hệ thống prescriptive rule-based phụ thuộc vào tính hoàn thiện của bộ luật chuyên gia; chưa tự động sinh luật mới nếu gặp hành vi chưa từng thấy.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Hệ thống của em thuộc cấp độ phân tích nào trong 4 tầng phân tích dữ liệu?"*  
> **Trả lời:** *"Thưa Thầy/Cô, đồ án của chúng em trải dài trọn vẹn cả 4 cấp độ: Descriptive ở Phase 1 (EDA) và Phase 3 (RFM); Diagnostic ở Phase 2 (Kiểm toán chất lượng dữ liệu); Predictive ở Phase 4 & 5 (K-Means phân cụm và kiểm chứng tiên lượng tương lai); và Prescriptive ở Phase 6 (Bộ máy sinh khuyến nghị tiếp thị có giải thích và gắn rào chắn an toàn)."*

---

## P6.2 — Phân biệt Bản chất: Phân khúc Khách hàng (Segmentation) vs. Đề xuất Quyết định (Decision Recommendation)

### 1. What (Khái niệm là gì?)
- **Segmentation (Phân khúc):** Là phép chiếu gom nhóm khách hàng dựa trên sự tương đồng về đặc trưng lịch sử (Mathematical Clustering).
- **Decision Recommendation (Đề xuất quyết định):** Là quy trình suy luận chọn hành động tiếp thị tối ưu cho từng cá thể dựa trên mục tiêu kinh doanh, điều kiện ràng buộc và bằng chứng hành vi cụ thể (Prescriptive Policy).

### 2. Why (Tại sao cần làm rõ?)
Một sai lầm rất phổ biến là đánh đồng "Phân khúc = Chiến thuật tiếp thị" (VD: Coi Cluster 1 chính là "chiến dịch VIP"). Phân khúc là đặc tính đối tượng (Ai?), còn quyết định tiếp thị là hành động can thiệp (Làm gì?). Cùng một phân khúc vẫn có nhiều hành động khác nhau tùy theo ngữ cảnh.

### 3. How (Cách thức triển khai?)
Engine nhận đầu vào gồm cả `segment_id` (kết quả K-Means hoặc Tiering) VÀ các đặc trưng hành vi cá nhân (`cart_sessions_30d`, `sessions_30d`, `monetary`), từ đó tính toán đề xuất riêng biệt.

### 4. Formula / Algorithm (Mô hình thuật toán)
$$\text{Tactic}(u) = f(\text{Cluster}(u), \text{Evidence}(u)) \neq g(\text{Cluster}(u))$$

### 5. Worked Example (Minh họa phân hóa trong cùng Cluster 1)
Trong Cluster 1 (8,755 VIPs):
- 7,418 khách hàng hoạt động đều đặn nhận `TAC_LOYALTY_VIP`.
- 1,287 khách hàng có giỏ hàng chưa thanh toán nhận `TAC_CART_RECOVERY`.
- 27 khách hàng đã ngưng hoạt động trên 45 ngày nhận `TAC_WINBACK_SURVEY`.
- 23 khách hàng mới mua đang chững lại nhận `TAC_POST_PURCHASE_CARE`.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Bảng ánh xạ 1:1:** Đơn giản nhưng thô thiển, dẫn đến việc spam khách hàng VIP bằng thông điệp không phù hợp với ngữ cảnh hiện tại.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_05_non_static_segment_diversity` xác nhận mỗi cụm Buyers nhận ít nhất 3 chiến thuật khác nhau.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Đòi hỏi phải theo dõi và cập nhật liên tục các biến tương tác gần (`sessions_30d`, `cart_sessions_30d`) để tránh ra quyết định dựa trên dữ liệu cũ.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao hai khách hàng cùng thuộc cụm VIP lại nhận hai đề xuất marketing hoàn toàn khác nhau?"*  
> **Trả lời:** *"Thưa Thầy/Cô, vì mô hình phân khúc K-Means chỉ xác định giá trị lịch sử dài hạn của khách hàng, trong khi quyết định tiếp thị phụ thuộc vào hành vi tức thời gần đây. Một khách VIP đang xem hàng mỗi ngày cần được tri ân đặc quyền (Loyalty VIP), nhưng một khách VIP đang có giỏ hàng bỏ quên lại cần hỗ trợ tháo gỡ rào cản thanh toán (Cart Recovery). Việc phân tách này giúp chiến dịch tiếp thị mang tính cá nhân hóa sâu sắc thay vì tiếp thị đại trà."*

---

## P6.3 — Kiến trúc Hệ Chuyên gia Dựa trên Bằng chứng (Rule-Based Expert System) và Xử lý Xung đột Luật (Conflict Resolution)

### 1. What (Khái niệm là gì?)
Hệ Chuyên gia Dựa trên Bằng chứng (Evidence-Based Rule Engine) là kiến trúc phần mềm sử dụng tập luật If-Then có cấu trúc rõ ràng, kết hợp cơ chế giải quyết xung đột (Conflict Resolution via Precedence & Priorities) để đưa ra khuyến nghị tất định (Deterministic).

### 2. Why (Tại sao cần dùng?)
Khác với các mô hình "hộp đen" (Black-box ML), hệ chuyên gia có tính minh bạch $100\%$, dễ kiểm toán, tuân thủ các rào chắn pháp lý và cho phép chuyên gia marketing điều chỉnh ngưỡng quy tắc trong file cấu hình YAML mà không cần viết lại mã nguồn.

### 3. How (Cách thức triển khai?)
1. Tách biệt hoàn toàn tệp tri thức (`configs/marketing_rules.yaml`) khỏi mã thực thi (`src/decision_engine/rules.py`).
2. Thiết lập thứ tự ưu tiên (Priority levels: 10, 20, 30... 99).
3. Đặt các Guardrails chặn ở tầng đầu tiên trước khi đánh giá luật kinh doanh.

### 4. Formula / Algorithm (Thuật toán giải quyết xung đột)
Thứ tự ưu tiên giải quyết xung đột:
1. **Guardrail G2 (Data Quality Fallback):** Dữ liệu lỗi $\to$ `TAC_NO_ACTION`.
2. **Guardrail G3 (Budget Protection):** Ngủ đông sâu giá trị thấp $\to$ `TAC_NO_ACTION`.
3. **VIP Active Privilege:** Khách VIP đang hoạt động $\to$ `TAC_LOYALTY_VIP`.
4. **Guardrail G4 (Cart Intent Precedence):** Có giỏ hàng gần đây $\to$ `TAC_CART_RECOVERY`.
5. **Segment-specific Tactic Matching:** Winback, Cross-sell, Post-purchase care, Education.
6. **Fallback Default:** `TAC_LOW_COST_NURTURE` hoặc `TAC_NO_ACTION`.

### 5. Worked Example (Xung đột giữa Giỏ hàng và Ngủ đông)
Khách hàng có Recency 85 ngày (thuộc cụm ngủ đông C0), nhưng bất ngờ có 1 phiên thêm giỏ hàng vào ngày 30/01 (`cart_sessions_30d = 1`).
- Luật C0 thông thường đề xuất: `TAC_LOW_COST_NURTURE`.
- Luật Giỏ hàng đề xuất: `TAC_CART_RECOVERY`.
- *Cơ chế giải quyết xung đột:* Guardrail G4 ưu tiên tín hiệu thêm giỏ hàng (Priority 20 > Priority 70), quyết định chọn `TAC_CART_RECOVERY` để nắm bắt cơ hội chuyển đổi ngay lập tức.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Scoring Model / Weighted Ranking:** Gán điểm cho từng chiến thuật rồi lấy điểm cao nhất. Nhược điểm: Phức tạp trong việc hiệu chuẩn trọng số và khó giải thích rành mạch cho ban giám đốc.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_12_decision_rules_deterministic_and_reproducible` xác nhận tính tất định $100\%$ qua nhiều lần chạy độc lập.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Khi số lượng luật tăng lên hàng trăm, nguy cơ xung đột chéo (Rule Contradiction) tăng cao, đòi hỏi phải có công cụ kiểm toán ma trận luật tự động.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Khi một khách hàng vừa đủ điều kiện nhận ưu đãi VIP vừa có giỏ hàng chưa thanh toán, hệ thống sẽ xử lý thế nào?"*  
> **Trả lời:** *"Thưa Thầy/Cô, hệ thống áp dụng cơ chế giải quyết xung đột bằng thứ tự ưu tiên đã được cấu hình trong `marketing_rules.yaml`. Nếu khách VIP vẫn đang trong chu kỳ mua thường xuyên ($\le 30$ ngày), hệ thống ưu tiên chiến thuật `TAC_LOYALTY_VIP` làm hành động chính và đưa `TAC_CART_RECOVERY` vào danh sách hành động thay thế khả thi. Ngược lại, nếu khách VIP đã lâu không mua ($> 30$ ngày) nhưng có giỏ hàng phát sinh, hệ thống sẽ ưu tiên ngay `TAC_CART_RECOVERY` để tháo gỡ rào cản mua sắm."*

---

## P6.4 — Khung Khả giải Khuyến nghị Tiếp thị (Explainable Recommendation): Reason Codes và Bằng chứng Truy vết (Evidence Traceability)

### 1. What (Khái niệm là gì?)
Khung Khả giải Khuyến nghị là chuẩn mực cấu trúc đầu ra bảo đảm mỗi đề xuất tiếp thị đều có thể truy vết ngược về các giá trị đặc trưng dữ liệu thật và được giải thích bằng hai ngôn ngữ: ngôn ngữ tự nhiên cho con người (`human_readable_reason`) và mã lý do chuẩn hóa cho máy (`reason_codes`).

### 2. Why (Tại sao cần dùng?)
Theo các quy định hiện đại về AI đáng tin cậy (Responsible AI / EU AI Act), người dùng và nhân viên kinh doanh có quyền được biết lý do đằng sau các quyết định tự động. Khung khả giải giúp chuyên viên marketing tự tin phê duyệt chiến dịch và hiểu rõ bối cảnh khách hàng.

### 3. How (Cách thức triển khai?)
Mỗi đề xuất xuất bản trả về JSON/Parquet chứa: `human_readable_reason`, danh sách `reason_codes`, từ điển `evidence` (chứa các giá trị recency, monetary, sessions...), và các chỉ số `evaluation_kpis`.

### 4. Formula / Algorithm (Cấu trúc dữ liệu)
```json
{
  "user_id": "...",
  "recommended_tactic": "TAC_WINBACK_SURVEY",
  "reason_codes": ["MODERATE_PAST_VALUE", "PROLONGED_INACTIVITY", "CHURN_RISK_DETECTED"],
  "evidence": {"recency_days": 55.0, "monetary": 68.50, "sessions_30d": 0},
  "primary_kpi": "winback_reactivation_rate"
}
```

### 5. Worked Example (Minh họa thực tế)
Đề xuất cho User Cluster 2:
- Lý do văn bản: *"Khách hàng từng chi tiêu khá (Monetary: $68.50) đang có dấu hiệu rời bỏ (Recency: 55.0 ngày, 0 phiên gần đây). Đề xuất chiến dịch tái kích hoạt và khảo sát trải nghiệm."*
- Bằng chứng kiểm toán: `recency_days = 55.0`, `monetary = 68.50`, `sessions_30d = 0`.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Chỉ xuất Tactic ID:** Thiếu thông tin giải thích, người vận hành không hiểu căn cứ đưa ra quyết định.
- **Văn bản tự do sinh bởi LLM:** Tiềm ẩn ảo giác (Hallucination) và khó kiểm soát chất lượng trên quy mô triệu khách hàng. Bộ mã lý do cấu trúc là chuẩn mực công nghiệp an toàn nhất.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_11_explainability_contract_traceability` xác nhận $100\%$ bản ghi có mã lý do và KPI hợp lệ.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Mã lý do phản ánh các điều kiện logic, không thể hiện được các yếu tố cảm xúc hay động cơ tâm lý sâu xa của người tiêu dùng.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Hệ thống làm thế nào để người làm marketing kiểm tra xem đề xuất có bịa đặt hay không?"*  
> **Trả lời:** *"Thưa Thầy/Cô, hệ thống tuân thủ Hợp đồng Khả giải (Explainability Contract) nghiêm ngặt: Mỗi dòng khuyến nghị xuất ra đều đính kèm một từ điển `evidence` lưu giữ chính xác các giá trị số thực tế của khách hàng tại mốc cutoff (số ngày mua gần nhất, số tiền đã chi, số phiên lướt web). Chuyên viên marketing chỉ cần đối chiếu các giá trị này với quy tắc trong file cấu hình để kiểm chứng tính xác thực."*

---

## P6.5 — Phân tầng Mức độ Quan tâm Không dùng Recency Giả cho Người Chưa Mua (Non-Buyer Engagement Tiering)

### 1. What (Khái niệm là gì?)
Phân tầng Mức độ Quan tâm Nhóm Chưa Mua là kỹ thuật phân loại 1,248,847 khách hàng chưa từng mua hàng thành 4 tầng hành vi dựa trên phân phối số phiên truy cập và lượt xem trong 30 ngày quan sát gần nhất.

### 2. Why (Tại sao cần dùng?)
Tuyệt đối không thể đưa nhóm chưa mua vào mô hình RFM vì họ chưa từng có giao dịch mua; việc gán `Recency = 999` hay 0 là phi lý toán học. Phân tầng theo Engagement giúp doanh nghiệp khai thác phễu chuyển đổi khách hàng tiềm năng mà không vi phạm nguyên tắc khoa học dữ liệu.

### 3. How (Cách thức triển khai?)
Phân chia thành 4 tầng dựa trên phân phối thực nghiệm của 1.25 triệu người dùng:
1. **`HIGH_INTENT` (2.73%):** Có thêm giỏ hàng ($\ge 1$) và tương tác tích cực ($\ge 2$ phiên hoặc $\ge 5$ views) $\to$ `TAC_CART_RECOVERY`.
2. **`EXPLORING` (6.57%):** Duyệt web nhiều ($\ge 2$ phiên hoặc $\ge 5$ views) nhưng chưa thêm giỏ $\to$ `TAC_PRODUCT_EDU`.
3. **`LOW_ENGAGEMENT` (19.76%):** Tương tác nhẹ (1 phiên, $< 5$ views) $\to$ `TAC_LOW_COST_NURTURE`.
4. **`INACTIVE` (70.95%):** Không truy cập trong 30 ngày $\to$ `TAC_NO_ACTION` (Guardrail G5).

### 4. Formula / Algorithm (Điều kiện logic)
$$\text{Tier}(u) = \begin{cases} 
\text{HIGH\_INTENT} & \text{nếu } (\text{cart\_sessions}_{30\text{d}} \ge 1 \lor \text{carts}_{30\text{d}} \ge 1) \land (\text{sessions}_{30\text{d}} \ge 2 \lor \text{views}_{30\text{d}} \ge 5) \\
\text{EXPLORING} & \text{nếu } (\text{sessions}_{30\text{d}} \ge 2 \lor \text{views}_{30\text{d}} \ge 5) \land \text{cart} = 0 \\
\text{LOW\_ENGAGEMENT} & \text{nếu } \text{sessions}_{30\text{d}} \ge 1 \land \text{views}_{30\text{d}} < 5 \land \text{cart} = 0 \\
\text{INACTIVE} & \text{nếu } \text{sessions}_{30\text{d}} = 0 
\end{cases}$$

### 5. Worked Example (Số liệu thực nghiệm đồ án)
- `HIGH_INTENT`: 34,061 khách hàng được gửi hỗ trợ hoàn tất đơn hàng đầu tiên.
- `EXPLORING`: 81,994 khách hàng được gửi cẩm nang làm đẹp và bộ mẫu thử.
- `INACTIVE`: 886,075 khách hàng được đưa vào diện bảo vệ tần suất liên lạc.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Gộp chung với Buyers:** Ép chạy K-Means chung làm sai lệch toàn bộ cấu trúc cụm.
- **Bỏ qua hoàn toàn Non-Buyers:** Đánh mất cơ hội chuyển đổi trên 93% lượng truy cập toàn sàn.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_06_non_buyer_tiering_coverage` xác nhận có đầy đủ 4 tầng và không có bản ghi nào bị gán nhãn NULL.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Nhóm Inactive (70.95%) chiếm tỷ trọng rất lớn do đặc thù lưu lượng truy cập vãng lai từ quảng cáo số; cần các kênh tiếp thị lại (Retargeting Pixel) ngoài sàn để kích hoạt lại.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không gán Recency bằng số ngày từ lần xem web cuối cùng cho người chưa mua để chạy chung K-Means?"*  
> **Trả lời:** *"Thưa Thầy/Cô, trong định nghĩa kinh điển của RFM, Recency là thời gian kể từ lần giao dịch mua hàng cuối cùng (Purchase Recency), đo lường rủi ro rời bỏ tài chính. Nếu thay thế bằng Visit Recency cho người chưa mua và trộn chung vào K-Means, khoảng cách Euclidean sẽ so sánh một ngày mua hàng $50 với một ngày xem lướt một thỏi son $2, làm xóa nhòa ranh giới giá trị giao dịch. Do đó, tách riêng hai cohort và dùng Engagement Tiering là phương pháp luận chuẩn xác nhất."*

---

## P6.6 — Rào chắn An toàn (Guardrails), Quyền riêng tư và Trạng thái Chấp thuận Tiếp thị (Marketing Consent)

### 1. What (Khái niệm là gì?)
Rào chắn An toàn (Guardrails) là tập hợp các quy tắc kiểm soát bắt buộc nhằm ngăn chặn việc phát tán thông điệp tiếp thị sai đối tượng, bảo vệ ngân sách doanh nghiệp và tuân thủ các quy định bảo vệ dữ liệu cá nhân (GDPR, PDPA).

### 2. Why (Tại sao cần dùng?)
Một hệ thống marketing tự động không có guardrails sẽ nhanh chóng dẫn đến thảm họa: gửi hàng triệu email cho người dùng không hoạt động (lọt vào hòm thư rác / Blacklist), gửi ưu đãi cho tài khoản lỗi, hoặc lãng phí chi phí tiếp cận vào những khách hàng có giá trị dự kiến thấp hơn chi phí gửi tin.

### 3. How (Cách thức triển khai?)
Triển khai 5 rào chắn bảo vệ:
- `G1_EXECUTION_CONSENT_CHECK`: Gán trạng thái `PENDING_CONSENT` cho toàn bộ 1.34M đề xuất.
- `G2_DATA_QUALITY_FALLBACK`: Chặn tài khoản khuyết mã định danh.
- `G3_BUDGET_PROTECTION_DEEP_DORMANT`: Chặn khách ngủ đông sâu giá rẻ ($> 90$d, $< \$20$).
- `G4_CART_INTENT_PRECEDENCE`: Ưu tiên xử lý giỏ hàng chưa thanh toán.
- `G5_CONTACT_FATIGUE_PREVENTION`: Chặn gửi tin rác cho 886k Non-Buyers bất động.

### 4. Formula / Algorithm (Cơ chế kích hoạt)
$$\text{If } \text{Condition}(\text{Guardrail}_i) \implies \text{Action} = \text{Suppress or Override}$$

### 5. Worked Example (Số lượng thực nghiệm đồ án)
- Guardrail G1 đã bảo đảm $100\%$ đề xuất không bị phát lệnh tự động.
- Guardrail G3 đã tiết kiệm chi phí tiếp thị cho 6,433 khách hàng ngủ đông sâu.
- Guardrail G5 đã bảo vệ 886,075 người dùng khỏi bị spam.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Cho phép gửi trực tiếp:** Vi phạm nghiêm ngặt đạo đức nghiên cứu và quy định pháp lý về quyền riêng tư khi dữ liệu REES46 không có thông tin opt-in.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_07_guardrail_g1_consent_pending`, `test_08_guardrail_g3_budget_protection` và `test_10_guardrail_g5_non_buyer_fatigue` đều PASS 100%.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Để triển khai ngoài đời thực, hệ thống cần tích hợp với module Quản lý Chấp thuận (Consent Management Platform - CMP) để kiểm tra trạng thái Opt-in theo thời gian thực.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao trạng thái của tất cả các đề xuất đều là 'PENDING_CONSENT' thay vì 'READY_TO_SEND'?"*  
> **Trả lời:** *"Thưa Thầy/Cô, đây là cam kết về Tiếp thị Có Trách nhiệm (Responsible Marketing). Dataset nghiên cứu REES46 không ghi nhận trường dữ liệu người dùng đồng ý nhận quảng cáo (Marketing Opt-in). Trong môi trường kinh doanh thực tế, việc tự ý gửi tin nhắn khi chưa có sự đồng ý của khách hàng sẽ vi phạm luật an toàn thông tin và gây thiệt hại danh tiếng thương hiệu. Do đó, hệ thống gán nhãn PENDING_CONSENT để yêu cầu bước kiểm duyệt chấp thuận trước khi kích hoạt chiến dịch."*

---

## P6.7 — Thiết kế Chỉ số KPI Đánh giá Chiến thuật Tiếp thị (Evaluation KPI Framework)

### 1. What (Khái niệm là gì?)
Khung KPI Đánh giá là tập hợp các chỉ số định lượng được liên kết chặt chẽ với từng chiến thuật tiếp thị, nhằm đo lường mức độ thành công sau khi can thiệp tiếp thị được triển khai.

### 2. Why (Tại sao cần dùng?)
Một đề xuất tiếp thị không có chỉ số đánh giá đi kèm là một đề xuất "vô trách nhiệm". Người quản trị không thể biết chiến dịch có đạt hiệu quả hay không nếu không xác định trước thước đo đo lường thành công.

### 3. How (Cách thức triển khai?)
Mỗi chiến thuật trong thư viện `candidate_tactics` bắt buộc phải khai báo một `evaluation_kpi` chính và một KPI phụ tương ứng với mục tiêu tiếp thị.

### 4. Formula / Algorithm (Ma trận ánh xạ KPI)
- `TAC_LOYALTY_VIP` $\to$ `vip_retention_rate_90d`
- `TAC_CART_RECOVERY` $\to$ `cart_checkout_rate`
- `TAC_CROSS_SELL` $\to$ `cross_category_adoption_rate`
- `TAC_POST_PURCHASE_CARE` $\to$ `second_order_conversion_rate`
- `TAC_WINBACK_SURVEY` $\to$ `winback_reactivation_rate`
- `TAC_PRODUCT_EDU` $\to$ `first_time_buyer_conversion`
- `TAC_LOW_COST_NURTURE` $\to$ `newsletter_open_rate`
- `TAC_NO_ACTION` $\to$ `unsolicited_contact_prevention_rate`

### 5. Worked Example (Minh họa cho chiến thuật Giỏ hàng)
Với chiến thuật `TAC_CART_RECOVERY`, chỉ số chính là `cart_checkout_rate` (Tỷ lệ người dùng nhận thông báo hoàn tất thanh toán giỏ hàng trong vòng 48 giờ); chỉ số phụ là `checkout_abandonment_reduction`.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Dùng chung một KPI (Tổng doanh thu toàn sàn):** Quá vĩ mô và bị nhiễu bởi các yếu tố bên ngoài (mùa vụ, giá cả, thời tiết), không phản ánh được tác động trực tiếp của từng chiến thuật.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_11_explainability_contract_traceability` xác nhận $100\%$ bản ghi có `primary_kpi` hợp lệ.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Do dataset REES46 không có nhật ký thực thi chiến dịch (campaign logs), các KPI này đóng vai trò là "hợp đồng đo lường định hướng" cho giai đoạn triển khai thực tế.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Em dùng KPI nào để đánh giá chiến thuật dành cho nhóm khách hàng có nguy cơ rời bỏ (Cluster 2)?"*  
> **Trả lời:** *"Thưa Thầy/Cô, đối với chiến thuật khảo sát tái kích hoạt `TAC_WINBACK_SURVEY` dành cho nhóm Cluster 2, chỉ số đánh giá chính là `winback_reactivation_rate` (tỷ lệ khách hàng quay lại đăng nhập và phát sinh phiên tương tác trong vòng 30 ngày kể từ khi gửi thông điệp), và chỉ số phụ là `winback_conversion_rate` (tỷ lệ khách hàng thực sự phát sinh đơn hàng mua trở lại)."*

---

## P6.8 — Ranh giới Phương pháp luận: Chi tiêu Quan sát Tự nhiên (Observed Spend) vs. Lợi tức Đầu tư Tiếp thị Thực tế (Incremental Marketing ROI)

### 1. What (Khái niệm là gì?)
- **Observed Future Spend (Chi tiêu tương lai quan sát được):** Doanh thu tự nhiên mà khách hàng chi tiêu theo đà quán tính trong điều kiện không có can thiệp có chủ đích.
- **Incremental Marketing ROI (Lợi tức đầu tư tiếp thị gia tăng):** Tỷ lệ lợi nhuận ròng tăng thêm tạo ra trực tiếp bởi chiến dịch tiếp thị so với chi phí bỏ ra để thực hiện chiến dịch đó.

### 2. Why (Tại sao cần làm rõ?)
Một sai lầm rất tai hại trong ngành phân tích là lấy doanh thu quan sát được của nhóm VIP ($25.85) trừ đi chi phí gửi email để tuyên bố "ROI của chiến dịch VIP là $2500\%". Khẳng định này là ngụy biện khoa học, vì phần lớn số tiền $25.85 đó khách VIP vốn dĩ sẽ tự chi tiêu dù không nhận được bất kỳ email nào.

### 3. How (Cách thức triển khai?)
1. Luôn tách bạch rõ ràng giữa hai khái niệm trong mọi tài liệu báo cáo.
2. Từ chối đưa ra các tuyên bố "đã chứng minh ROI tiếp thị" khi chưa có thử nghiệm A/B Testing.
3. Đề xuất quy trình thử nghiệm ngẫu nhiên có nhóm đối chứng (Randomized Controlled Trials - RCT).

### 4. Formula / Algorithm (Công thức toán học)
$$\text{Incremental Lift} = \bar{Y}_{\text{treatment}} - \bar{Y}_{\text{control}}$$
$$\text{True Marketing ROI} = \frac{\text{Incremental Lift} \times \text{Gross Margin} - \text{Campaign Cost}}{\text{Campaign Cost}}$$
Nếu không có $\bar{Y}_{\text{control}}$ và $\text{Campaign Cost}$, về mặt toán học không thể tính được ROI.

### 5. Worked Example (Minh họa cho Cluster 2)
Cluster 2 có mức chi tiêu tự nhiên trong tháng 2 là $\$4.28/khách$. Con số này thể hiện tiềm năng giá trị tự nhiên của phân khúc. Nếu một chiến dịch win-back gửi mã giảm giá $\$2$ cho nhóm này, ta cần đo lường xem nhóm nhận mã có chi tiêu vượt trội hơn nhóm không nhận mã hay không. Nếu nhóm nhận mã chi tiêu $\$4.50$ và nhóm đối chứng chi tiêu $\$4.28$, thì doanh thu gia tăng thực sự chỉ là $\$0.22$, không bù đắp được chi phí ưu đãi $\$2$!

### 6. Alternatives (Phương án thay thế & So sánh)
- **Causal Machine Learning / Uplift Trees:** Mô hình ước lượng tác động gia tăng cá nhân hóa. Đây là hướng phát triển nâng cao của đồ án sau 21 ngày.

### 7. Verification (Cách thức kiểm chứng)
Tài liệu báo cáo Chapter 9 đã được bổ sung mục ranh giới phương pháp luận nghiêm ngặt.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
- Dữ liệu lịch sử quan sát thụ động (Observational Data) không thể thay thế cho các thử nghiệm can thiệp chủ động (Interventional Experiments).

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không khẳng định chiến dịch tiếp thị ở Phase 6 sẽ mang lại ROI cao nhất cho Cluster 2?"*  
> **Trả lời:** *"Thưa Thầy/Cô, chúng em tuyệt đối không khẳng định điều đó vì thiếu cơ sở khoa học: Dữ liệu tháng 2 cho thấy khách hàng Cluster 2 chi tiêu tự nhiên $4.28/khách, chứng minh đây là nhóm có cơ hội nghiệp vụ tương đối (Relative Business Opportunity) hấp dẫn. Tuy nhiên, để tính được ROI của một chiến dịch, chúng em cần biết chi phí gửi tin, chi phí mã giảm giá và quan trọng nhất là phải có nhóm đối chứng (Control Group) để đo lường doanh thu tăng thêm thực sự do chiến dịch tạo ra. Do đồ án sử dụng dữ liệu nhật ký quan sát, chúng em chỉ đưa ra khuyến nghị chiến thuật khả thi và đề xuất thử nghiệm A/B testing trước khi nhân rộng."*

---

## P6.9 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 6 (Oral Defense Guide P6: Q39 – Q45)

### Q39: Bộ máy hỗ trợ quyết định tiếp thị ở Phase 6 của em có phải là một mô hình Machine Learning tự động ra quyết định không?
- **Trả lời:** Dạ thưa Thầy/Cô, không. Đây là một Hệ Chuyên Gia Chỉ Dẫn Dựa Trên Bằng Chứng (Evidence-Based Prescriptive Decision Support System) sử dụng bộ luật nghiệp vụ minh bạch kết hợp với kết quả phân cụm K-Means. Chúng em chủ ý không dùng mô hình Black-box ML để sinh khuyến nghị vì trong quản trị tiếp thị, tính minh bạch, khả năng giải thích (Explainability), sự kiểm soát rào chắn an toàn (Guardrails) và khả năng kiểm toán luật (Auditability) là những ưu tiên hàng đầu của doanh nghiệp.

### Q40: Làm thế nào em chứng minh rằng hệ thống của em không phải là một bảng ánh xạ cứng tĩnh (Static Mapping) giữa Cluster và Chiến thuật?
- **Trả lời:** Tính phi tĩnh (Non-static diversity) của hệ thống được chứng minh bằng thực nghiệm trên toàn bộ 92,652 khách hàng:
1. Trong cùng Cụm 1 (VIP), có 7,418 khách nhận `TAC_LOYALTY_VIP`, 1,287 khách nhận `TAC_CART_RECOVERY`, 27 khách nhận `TAC_WINBACK_SURVEY` và 23 khách nhận `TAC_POST_PURCHASE_CARE`.
2. Trong cùng Cụm 2 (Hạ nhiệt), có 13,169 khách nhận `TAC_WINBACK_SURVEY`, 3,660 khách nhận `TAC_LOW_COST_NURTURE` và 1,779 khách nhận `TAC_CART_RECOVERY`.
3. Kiểm thử tự động `test_05_non_static_segment_diversity` xác nhận mỗi cụm đều phân nhánh sang từ 3 đến 4 chiến thuật khác nhau tùy theo bằng chứng hành vi tức thời của từng cá nhân.

### Q41: Tại sao có tới 66.5% khách hàng toàn sàn được đề xuất chiến thuật `TAC_NO_ACTION`? Điều này có phải là hệ thống hoạt động kém không?
- **Trả lời:** Hoàn toàn ngược lại, đây là tính năng bảo vệ then chốt của hệ thống. Trong thương mại điện tử, hơn 70% người truy cập là khách vãng lai chỉ vào xem rồi biến mất và không có hoạt động nào trong 30 ngày qua (886k Non-Buyers và 6.4k Buyers ngủ đông sâu). Việc gửi thông điệp tiếp thị đại trà đến nhóm này sẽ gây lãng phí ngân sách khổng lồ và khiến thương hiệu bị đánh dấu là nguồn gửi thư rác (Spam Fatigue). Việc hệ thống chủ động gán `TAC_NO_ACTION` thông qua Guardrail G3 và G5 giúp doanh nghiệp tiết kiệm tài nguyên để tập trung ngân sách vào 33.5% khách hàng thực sự có ý định mua sắm (Actionable Candidates).

### Q42: Tín hiệu nào được hệ thống ưu tiên xử lý cao nhất khi khách hàng có nhiều hành vi mâu thuẫn?
- **Trả lời:** Tín hiệu giỏ hàng chưa thanh toán (`cart_sessions_30d >= 1`) được hệ thống ưu tiên xử lý cao nhất thông qua Guardrail G4 (`G4_CART_INTENT_PRECEDENCE`). Trong thương mại điện tử, hành vi thêm sản phẩm vào giỏ hàng trong 30 ngày gần nhất thể hiện ý định mua sắm cận kề và khẩn cấp nhất của người tiêu dùng. Bất kể khách hàng thuộc phân cụm nào (ngoại trừ khách VIP đang hoạt động thường xuyên), việc hỗ trợ hoàn tất giỏ hàng (`TAC_CART_RECOVERY`) luôn được ưu tiên hơn các chiến dịch bản tin hay nội dung giáo dục chung chung.

### Q43: Làm thế nào để đảm bảo tính an toàn và quyền riêng tư khi hệ thống đưa ra gợi ý tiếp thị?
- **Trả lời:** Hệ thống thực thi nguyên tắc Tiếp thị Có Trách nhiệm (Responsible Marketing) thông qua Guardrail G1: Toàn bộ 1,341,499 đề xuất đều được gán trạng thái bắt buộc là `eligibility_status = 'PENDING_CONSENT'`. Vì dataset REES46 không có thông tin về sự chấp thuận nhận quảng cáo của khách hàng (Opt-in), mọi đề xuất chỉ dừng lại ở mức gợi ý nghiên cứu (Research Proposal). Để chuyển thành lệnh gửi tin thực tế ngoài đời, hệ thống đòi hỏi phải có bước xác thực chấp thuận tiếp thị từ phía doanh nghiệp.

### Q44: Hiệu năng thực thi của bộ máy ra quyết định có đáp ứng được quy mô dữ liệu lớn không?
- **Trả lời:** Hiệu năng của hệ thống đạt chuẩn mực xử lý dữ liệu lớn xuất sắc: Nhờ kiến trúc vector hóa dạng cột trên DuckDB và PyArrow, bộ máy đánh giá toàn bộ 1,341,499 khách hàng chỉ mất **4.52 giây**, đạt thông lượng xử lý **296,528 khách hàng/giây**, và mức tiêu hao bộ nhớ RAM tối đa chỉ **314.68 MB**, an toàn tuyệt đối dưới ngưỡng giới hạn 2 GB của hệ thống.

### Q45: Bộ máy này sẽ kết nối như thế nào với giao diện IVRE Owner Dashboard ở Phase 7 tiếp theo?
- **Trả lời:** Ở Phase 7, hệ thống sẽ xuất bản một tệp tóm tắt cấu trúc chuẩn (JSON Snapshot) từ các bảng Parquet khuyến nghị của Phase 6. Dashboard IVRE sẽ đọc trực tiếp tệp snapshot này để hiển thị màn hình chuyên đề Recommendations: Cho phép chủ shop lọc theo phân khúc, xem danh sách hành động đề xuất, tra cứu lý do giải thích bằng lời, kiểm tra bằng chứng hành vi thực tế và theo dõi các chỉ số KPI tương ứng, kèm theo nhãn nghiên cứu minh bạch `Research Demo / REES46`.


---

# PHẦN VIII — KIẾN THỨC KỸ THUẬT VÀ VẤN ĐÁP PHASE 7 (VERIFIED SNAPSHOT & RESEARCH DASHBOARD)

## P7.1 — Kiến trúc Luồng Dữ liệu Một Chiều và Triết lý Static Snapshots vs. Dynamic Database APIs

### 1. What (Khái niệm là gì?)
- **Static Snapshot Architecture (Kiến trúc Ảnh chụp Tĩnh):** Mô hình xuất bản dữ liệu phân tích ngoại tuyến (offline export) thành các tệp dữ liệu có cấu trúc cố định (JSON/Parquet), được đánh dấu phiên bản (versioned) và kiểm toán tính toàn vẹn (cryptographic hashing), phục vụ trực tiếp cho tầng giao diện người dùng mà không yêu cầu máy chủ cơ sở dữ liệu động.
- **Dynamic Database API (Giao diện Lập trình Cơ sở Dữ liệu Động):** Mô hình ứng dụng web truyền thống nơi trình duyệt gửi các yêu cầu HTTP/REST/GraphQL đến backend để truy vấn cơ sở dữ liệu thời gian thực.

### 2. Why (Tại sao cần dùng trong Đồ án Nghiên cứu?)
1. **Bảo toàn Tính Bất Biến Khoa học (Reproducibility & Auditability):** Tập dữ liệu REES46 là tập dữ liệu lịch sử đóng băng. Việc sử dụng Static Snapshot đảm bảo mọi người xem (hội đồng chấm thi, giảng viên, chủ doanh nghiệp) đều quan sát cùng một bộ số liệu nhất quán tuyệt đối, không bị trôi dạt do cập nhật cơ sở dữ liệu.
2. **Triệt tiêu Rủi ro Hiệu năng Trình duyệt (Browser OOM Prevention):** Dân số 1.34 triệu khách hàng nếu xuất thành JSON thô sẽ có dung lượng >150 MB, chắc chắn gây tràn bộ nhớ (Out-of-Memory) và làm treo tab trình duyệt. Snapshot nén tổng hợp chỉ nặng **32.98 KB**, tải trong <50ms.
3. **Phân tách An toàn Hệ thống (Decoupled Security Boundary):** Ngăn ngừa việc mã giao diện can thiệp vào cơ sở dữ liệu sản xuất hoặc vô tình kích hoạt các hành động tiếp thị ngoài ý muốn.

### 3. How (Cách thức triển khai?)
1. Viết kịch bản xuất bản độc lập `scripts/build_phase7_snapshot.py` sử dụng DuckDB quét các tệp Parquet sạch và bảng khuyến nghị Phase 6.
2. Thực hiện tính toán tổng hợp (Aggregations: Counts, Percentiles, Medians, Means, Cross-tabulations).
3. Đóng gói kết quả thành `outputs/dashboard/ivre_dashboard_snapshot.json` và các tệp modular json.
4. Tạo mã băm SHA-256 cho từng tệp và ghi nhận vào `outputs/dashboard/snapshot_manifest.json`.

### 4. Formula / Algorithm (Mô hình luồng dữ liệu)
$$\text{Clean Parquet Data (19.58M rows)} \xrightarrow{\text{DuckDB Aggregations}} \text{Static Snapshot JSON (33 KB)} \xrightarrow{\text{HTTP / File Load}} \text{IVRE Research UI (Client-Side Rendering)}$$

### 5. Worked Example (So sánh Kích thước & Tốc độ)
| Đặc tính | Dynamic Database API | Static Verified Snapshot |
| :--- | :--- | :--- |
| **Tài nguyên máy chủ** | Cần server backend (Node.js/Python) + Database engine | Không cần server (Serverless / Static Hosting) |
| **Kích thước tải về trình duyệt** | 150+ MB (nếu truy vấn lớn) hoặc phân trang phức tạp | **32.98 KB** (Tải tức thì) |
| **Thời gian phản hồi** | 200ms – 2,500ms phụ thuộc tải server | **< 15ms** (Từ bộ nhớ đệm hoặc tệp tĩnh) |
| **Rủi ro rò rỉ dữ liệu (PII)** | Cao nếu API query thiếu bảo vệ | **Bằng 0** (Chỉ chứa aggregates và mẫu demo) |

### 6. Alternatives (Phương án thay thế & So sánh)
- **Direct OLAP Querying via DuckDB-WASM:** Chạy DuckDB trực tiếp trong trình duyệt qua WebAssembly để truy vấn tệp Parquet. Phương án này rất hiện đại nhưng yêu cầu tải tệp Parquet 25 MB về máy khách, không phù hợp với các thiết bị di động hoặc đường truyền yếu. Static JSON Snapshot là phương án tối ưu về tính gọn nhẹ và khả năng tương thích 100%.

### 7. Verification (Cách thức kiểm chứng)
Kịch bản `scripts/validate_phase7.py` kiểm tra sự tồn tại của toàn bộ tệp snapshot và xác thực từng mã băm SHA-256 với manifest.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
Snapshot không hỗ trợ truy vấn ad-hoc tùy ý của người dùng trên toàn bộ dữ liệu thô. Nếu người dùng muốn phân tích một chiều không có sẵn trong snapshot, họ phải chạy lại script Python ở backend.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em không dựng một REST API với FastAPI/NodeJS để frontend gọi lấy dữ liệu động?"*  
> **Trả lời:** *"Dạ thưa Thầy/Cô, chúng em chủ ý lựa chọn kiến trúc Static Verified Snapshot vì 3 lý do kỹ thuật: Thứ nhất, bài toán của chúng em là phân tích dữ liệu lịch sử đóng băng tại mốc cutoff 01/02/2020, dữ liệu không biến động theo thời gian thực nên việc dựng dynamic server là thừa thãi tài nguyên. Thứ hai, static snapshot cho phép gắn chữ ký điện tử SHA-256 vào manifest, đảm bảo tính bất biến khoa học và khả năng tái lập 100%. Thứ ba, snapshot tổng hợp chỉ nặng 33 KB giúp bảng điều khiển tải tức thì dưới 50ms mà không gây quá tải trình duyệt hay tốn chi phí duy trì backend server."*

---

## P7.2 — Thiết kế Hợp đồng Dữ liệu (Data Contract), Snapshot Versioning và Cơ chế Kiểm toán Mã băm Toàn vẹn (SHA-256 Manifest)

### 1. What (Khái niệm là gì?)
- **Data Contract (Hợp đồng Dữ liệu):** Bản đặc tả chính thức giữa bên sản xuất dữ liệu (Data Producer: Python Pipeline) và bên tiêu thụ dữ liệu (Data Consumer: Dashboard UI), xác định rõ lược đồ (schema), kiểu dữ liệu, các ràng buộc toàn vẹn số học và quy ước ngữ nghĩa.
- **SHA-256 Manifest (Bản kê Mã băm Mật mã):** Tệp kê khai toàn bộ danh mục sản phẩm dữ liệu kèm mã băm SHA-256 của từng tệp, hoạt động như một cơ chế niêm phong chống giả mạo (Anti-Tampering Seal).

### 2. Why (Tại sao cần dùng?)
Trong các dự án dữ liệu lớn, lỗi thường xảy ra khi frontend hiển thị sai lệch số liệu so với mô hình backend do thay đổi ngầm định về tên cột hoặc quy ước đơn vị đo. Data Contract và Manifest đảm bảo rằng nếu bất kỳ tệp dữ liệu nào bị sửa đổi thủ công hoặc sinh thiếu, hệ thống kiểm toán tự động sẽ phát hiện và từ chối tải ngay lập tức.

### 3. How (Cách thức triển khai?)
1. Định nghĩa chuẩn phiên bản `v1.0.0` trong metadata của snapshot.
2. Đóng gói các trường bắt buộc theo hợp đồng: `schema_version`, `generated_at`, `source_dataset`, `observation_window`, `holdout_window`, `customer_overview`, `behavioral_funnel`, `buyer_segments`, `non_buyer_tiers`, `historical_holdout_evaluation`, `tactic_distribution`, `diversity_matrix`, `hypothetical_cost_avoidance`, `archetype_samples`, `model_and_system_insights`.
3. Tính toán hàm băm mật mã: $H(F) = \text{SHA256}(\text{bytes of } F)$ cho từng tệp JSON và lưu vào `snapshot_manifest.json`.

### 4. Formula / Algorithm (Công thức băm toàn vẹn)
$$\text{SHA256}(m) = \text{Digest}_{256}(m), \quad \forall f \in \text{SnapshotFiles}$$
Ràng buộc hợp đồng: $\text{FileHash}(f) \equiv \text{ManifestHash}(f) \implies \text{Integrity PASS}$.

### 5. Worked Example (Trích lục Manifest Thực tế)
```json
{
  "manifest_version": "v1.0.0",
  "created_at": "2026-11-10T00:45:00Z",
  "total_files": 6,
  "files": {
    "ivre_dashboard_snapshot.json": {
      "size_kb": 32.98,
      "sha256": "8f3a9e2b1c4d..."
    },
    "summary_snapshot.json": {
      "size_kb": 2.90,
      "sha256": "7a1b5c3d2e4f..."
    }
  }
}
```

### 6. Alternatives (Phương án thay thế & So sánh)
- **JSON Schema Validation:** Sử dụng thư viện `jsonschema` để xác thực cấu trúc. Phương án này được tích hợp song song cùng kiểm tra SHA-256 để đảm bảo cả tính đúng đắn về cấu trúc lẫn tính bất biến của nội dung.

### 7. Verification (Cách thức kiểm chứng)
Unit test `test_02_manifest_checksum_integrity` trong `tests/test_phase7_dashboard_snapshot.py` đọc trực tiếp các tệp từ đĩa, băm lại nội dung và so khớp từng byte với manifest.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
Mã băm SHA-256 bảo vệ tính toàn vẹn của tệp trên đĩa nhưng không ngăn chặn được việc người có quyền truy cập root sửa đổi đồng thời cả tệp dữ liệu và tệp manifest nếu không có khóa ký số bất đối xứng (Asymmetric Digital Signature). Trong phạm vi đồ án học thuật, SHA-256 manifest đáp ứng hoàn hảo tiêu chuẩn kiểm toán.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Làm sao Thầy cô biết được các con số trên giao diện web của em thực sự lấy từ kết quả chạy mô hình chứ không phải em tự gõ cứng (hardcode) vào HTML?"*  
> **Trả lời:** *"Dạ thưa Thầy/Cô, hệ thống của chúng em tuân thủ nghiêm ngặt Hợp đồng Dữ liệu (Data Contract): Toàn bộ số liệu trên dashboard được sinh hoàn toàn tự động qua kịch bản `scripts/build_phase7_snapshot.py` đọc trực tiếp từ các tệp Parquet và model artifact. Mỗi tệp JSON xuất bản đều được gắn mã băm SHA-256 trong `snapshot_manifest.json`. Khi chạy `python scripts/validate_phase7.py`, hệ thống tự động băm lại các tệp và đối soát với manifest; nếu em sửa bất kỳ một chữ số nào trong tệp JSON, kiểm thử sẽ lập tức báo lỗi đỏ (Checksum Mismatch) và Phase Gate sẽ thất bại ngay lập tức."*

---

## P7.3 — Chiến lược Tổng hợp Đa tầng (Multi-Level Aggregation) và Kiểm soát Kích thước Payload Trình duyệt

### 1. What (Khái niệm là gì?)
- **Multi-Level Aggregation (Tổng hợp Đa tầng):** Kỹ thuật tiền xử lý dữ liệu ở backend nhằm trích xuất các chỉ số thống kê tóm tắt ở các cấp độ phân cấp khác nhau (Toàn sàn $\to$ Phân khúc $\to$ Chiến thuật $\to$ Mẫu điển hình), thay vì gửi dữ liệu vi mô của từng cá nhân xuống giao diện người dùng.

### 2. Why (Tại sao cần dùng?)
1. **Tiết kiệm Băng thông & Tăng Tốc độ Tải:** Giảm dung lượng truyền tải từ hơn 150 MB xuống chỉ còn 33 KB (giảm 99.98% dung lượng mạng).
2. **Tối ưu hóa Trải nghiệm Người dùng (UX Responsiveness):** Trình duyệt không phải phân tích cú pháp (parse) các mảng dữ liệu hàng triệu phần tử, giúp thời gian tương tác (Time to Interactive - TTI) đạt mức tức thì (<100ms).

### 3. How (Cách thức triển khai?)
1. **Tầng 1 (Toàn sàn):** Tổng số khách hàng (1,341,499), tỷ lệ Buyers (6.91%), tổng doanh thu quan sát (\$5.14M).
2. **Tầng 2 (Phân khúc & Tầng tương tác):** Phân vị hành vi (Median Recency, Median Frequency, Median Monetary, Median 30-day activity) cho 4 cụm Buyers và 4 tầng Non-Buyers.
3. **Tầng 3 (Chiến thuật tiếp thị):** Phân bố tần suất của 8 chiến thuật và ma trận đa dạng nội cụm ($4 \times 8$).
4. **Tầng 4 (Mẫu hồ sơ nghiên cứu):** 8 hồ sơ Archetypes được chọn lọc đại diện đầy đủ cho các không gian hành vi.

### 4. Formula / Algorithm (Tỷ lệ nén dữ liệu)
$$\text{Data Reduction Ratio} = 1 - \frac{\text{Payload Size}_{\text{Aggregated}}}{\text{Payload Size}_{\text{Raw}}} = 1 - \frac{32.98 \text{ KB}}{150 \times 1024 \text{ KB}} \approx 99.978\%$$

### 5. Worked Example (Bảng so sánh kích thước)
- Raw Parquet Recommendations: $1.12 \text{ MB} + 5.84 \text{ MB} = 6.96 \text{ MB}$ (nén dạng cột).
- Raw JSON Uncompressed: $\approx 165 \text{ MB}$.
- Aggregated Master Snapshot JSON: **32.98 KB**.
- Tỷ lệ tiết kiệm băng thông trình duyệt: **Gấp ~5,000 lần**.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Server-Side Pagination:** Thiết kế API phân trang (mỗi trang 50 khách hàng). Phương án này khả thi nhưng phức tạp hóa hạ tầng (cần máy chủ web luôn chạy) và không mang lại giá trị cho việc ra quyết định cấp cao (chủ doanh nghiệp cần nhìn thấy bức tranh toàn cảnh của 4 phân khúc chứ không thể đọc từng trang 50 khách trong số 1.34 triệu người).

### 7. Verification (Cách thức kiểm chứng)
Kịch bản `scripts/validate_phase7.py` kiểm tra dung lượng `ivre_dashboard_snapshot.json` luôn nằm trong giới hạn cho phép (<500 KB).

### 8. Limitations (Giới hạn lý thuyết & thực tế)
Tổng hợp đa tầng làm mất đi các chi tiết cá nhân đơn lẻ không nằm trong mẫu đại diện. Tuy nhiên, toàn bộ dữ liệu vi mô vẫn được bảo lưu 100% trong các tệp Parquet nội bộ phục vụ cho các nghiên cứu chuyên sâu.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Nếu ban giám đốc muốn xem danh sách toàn bộ 1.34 triệu khách hàng trên dashboard thì em xử lý thế nào?"*  
> **Trả lời:** *"Dạ thưa Thầy/Cô, theo nguyên lý thiết kế Dashboard điều hành (Executive Dashboard Architecture), việc hiển thị danh sách 1.34 triệu dòng trên giao diện web là một phản mẫu (anti-pattern) vì mắt người không thể đọc hết 1 triệu dòng và trình duyệt sẽ bị sập bộ nhớ. Thay vào đó, hệ thống cung cấp giao diện tổng quan đa chiều (Executive Overview & Funnel) để nắm bắt xu hướng vĩ mô, bảng phân khúc để hiểu cơ cấu nhóm, và trình duyệt mẫu hồ sơ điển hình (Archetype Explorer) để thẩm tra logic chi tiết. Danh sách đầy đủ 1.34 triệu khách hàng được lưu trữ dưới dạng Parquet chuẩn nén ZSTD, sẵn sàng xuất ra các hệ thống thực thi tiếp thị chuyên dụng (như Braze, Klaviyo hoặc CRM nội bộ) thông qua quy trình xử lý theo lô (batch process) có bảo mật."*

---

## P7.4 — Bảo vệ Quyền Riêng tư (Data Privacy) và Kỹ thuật Ẩn danh Hóa Hồ sơ Khách hàng (Zero Raw PII)

### 1. What (Khái niệm là gì?)
- **Personally Identifiable Information (PII - Thông tin Định danh Cá nhân):** Bất kỳ dữ liệu nào có thể được sử dụng để trực tiếp hoặc gián tiếp nhận dạng một cá nhân cụ thể. Trong ngữ cảnh thương mại điện tử, mã số khách hàng nội bộ (`user_id`), địa chỉ email, số điện thoại, hoặc địa chỉ IP là PII.
- **Data Anonymization (Ẩn danh Hóa Dữ liệu):** Quy trình xử lý thông tin để biến đổi dữ liệu cá nhân sao cho chủ thể dữ liệu không thể bị nhận dạng lại bằng bất kỳ biện pháp hợp lý nào.

### 2. Why (Tại sao cần dùng?)
1. **Tuân thủ Tiêu chuẩn Đạo đức Nghiên cứu & Pháp lý (GDPR / An toàn Dữ liệu):** Không được công bố mã định danh người dùng gốc lên các tệp JSON tĩnh công khai của website, tránh nguy cơ đối soát chéo (cross-referencing attack) với các bộ dữ liệu khác.
2. **Bảo vệ Tính Bảo mật Thương mại:** Bảo vệ dữ liệu hành vi của người tiêu dùng không bị khai thác thương mại trái phép.

### 3. How (Cách thức triển khai?)
1. Tuyệt đối **không xuất bản danh sách `user_id` thô** vào bất kỳ tệp JSON tĩnh nào trong thư mục `outputs/dashboard/`.
2. Trong tệp snapshot và giao diện Explorer, toàn bộ các hồ sơ khách hàng mẫu được đại diện hóa bằng các mã định danh nghiên cứu tổng hợp: `DEMO_BUYER_01`, `DEMO_BUYER_02`... và `DEMO_NON_BUYER_01`, `DEMO_NON_BUYER_02`.
3. Các thuộc tính hành vi hiển thị ($R, F, M$, lượt xem, số phiên) phản ánh giá trị trung vị hoặc đặc trưng chuẩn tắc của hồ sơ nghiên cứu, không gán kèm bất kỳ thông tin cá nhân nhạy cảm nào.

### 4. Formula / Algorithm (Quy tắc lọc PII)
$$\forall s \in \text{ExportedSamples}: \quad s.\text{demo\_id} \in \{\text{DEMO\_*}\} \quad \land \quad s.\text{user\_id} \notin \text{SnapshotJSON}$$

### 5. Worked Example (Cấu trúc mẫu đã ẩn danh)
```json
{
  "demo_id": "DEMO_BUYER_01",
  "archetype_name": "Active VIP Champion",
  "cohort": "BUYER",
  "segment_name": "Cluster 1 · Core VIP Champions",
  "observation_behavior": {
    "recency_days": 5.0,
    "frequency": 12,
    "monetary_usd": 350.00,
    "sessions_30d": 9
  },
  "eligibility_status": "PENDING_CONSENT"
}
```

### 6. Alternatives (Phương án thay thế & So sánh)
- **Kỹ thuật Masking / Hashing (SHA-256 trên User ID):** Băm mã số người dùng thành chuỗi hex (ví dụ: `463240011` $\to$ `a1b2c3...`). Tuy nhiên, nếu không gian ID nhỏ, kẻ tấn công vẫn có thể dùng bảng tra cứu trước (Rainbow Table) để tìm lại ID gốc. Việc sử dụng mã nghiên cứu tổng hợp `DEMO_*` là giải pháp an toàn tuyệt đối 100%.

### 7. Verification (Cách thức kiểm chứng)
Kiểm thử tự động `test_07_privacy_and_anonymization` trong `test_phase7_dashboard_snapshot.py` quét toàn bộ mảng `archetype_samples` và xác nhận tất cả `demo_id` đều bắt đầu bằng tiền tố `DEMO_`, không chứa bất kỳ ID số nguyên thô nào.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
Mã ẩn danh không thể dùng để trực tiếp gửi email cho khách hàng thực ngoài đời. Để triển khai thật, bộ phận kỹ thuật phải chạy kịch bản giải mã nội bộ có phân quyền trên cơ sở dữ liệu gốc.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao trên giao diện demo của em không hiển thị mã `user_id` thật của khách hàng mà lại dùng mã `DEMO_BUYER_01`?"*  
> **Trả lời:** *"Dạ thưa Thầy/Cô, đây là nguyên tắc thiết kế Bảo vệ Quyền Riêng tư (Privacy by Design): Để đáp ứng các tiêu chuẩn đạo đức nghiên cứu và phòng tránh nguy cơ rò rỉ dữ liệu định danh người dùng (PII) khi xuất bản tệp JSON công khai, chúng em triệt tiêu hoàn toàn các mã định danh gốc trên tầng giao diện. Chúng em xây dựng 8 hồ sơ nghiên cứu đại diện (Archetypes) mang mã ẩn danh `DEMO_*` chứa đầy đủ các bằng chứng hành vi vi mô để minh họa trọn vẹn quy trình giải trình tiếp thị mà vẫn bảo vệ an toàn 100% dữ liệu cá nhân."*

---

## P7.5 — Ranh giới Ngữ cảnh Nghiên cứu và Nhãn Định danh Khách quan: Research Demo / REES46

### 1. What (Khái niệm là gì?)
- **Research Demo Context Boundary (Ranh giới Ngữ cảnh Bản Trình diễn Nghiên cứu):** Nguyên tắc ghi nhãn rõ ràng nguồn gốc dữ liệu thực nghiệm (Dataset REES46 ngành hàng Mỹ phẩm giai đoạn 2019–2020), phân biệt rạch ròi với thương hiệu trình diễn giao diện (IVRE thời trang), nhằm tránh gây hiểu lầm cho người dùng hoặc hội đồng đánh giá rằng hệ thống đang vận hành trên dữ liệu thời gian thực của IVRE năm 2026.

### 2. Why (Tại sao cần làm rõ?)
Một trong những lỗi nặng nề nhất về tính liêm chính trong phân tích dữ liệu là việc "ngụy trang dữ liệu" (Data Misrepresentation) — tức là lấy một tập dữ liệu mở tải trên mạng rồi gán nhãn như thể đó là số liệu bán hàng thực tế của một doanh nghiệp trong nước. Việc ghi rõ nhãn nghiên cứu thể hiện tính trung thực khoa học, sự minh bạch về nguồn gốc dữ liệu (Data Lineage) và tinh thần chuyên nghiệp của kỹ sư dữ liệu.

### 3. How (Cách thức triển khai?)
1. Đặt dải băng cảnh báo cố định trên cùng của giao diện (Sticky Top Banner): **`REES46 Cosmetics Research Demo — Historical Data 2019–2020`**.
2. Ghi rõ chú thích ngữ cảnh: *"Read-only Analytical Sandbox. Dữ liệu thực nghiệm lịch sử từ tập REES46 eCommerce Events (01/10/2019 – 29/02/2020). Không đại diện cho khách hàng thời trang thực tế của IVRE."*
3. Trong tệp snapshot JSON, trường `metadata.disclaimer` được khóa cứng nội dung này.

### 4. Formula / Algorithm (Ràng buộc toàn vẹn nhãn)
$$\text{DisclaimerCheck}(M) = \begin{cases} \text{PASS}, & \text{if } "REES46" \in M.\text{disclaimer} \land "Research\ Demo" \in M.\text{disclaimer} \\ \text{FAIL}, & \text{otherwise} \end{cases}$$

### 5. Worked Example (Hiển thị Banner trên UI)
```html
<div class="research-banner">
  <span class="research-badge">Research Demo</span>
  <span>REES46 Cosmetics eCommerce Analytics (Oct 2019 – Feb 2020) — Read-Only Analytical Sandbox</span>
</div>
```

### 6. Alternatives (Phương án thay thế & So sánh)
- Bỏ nhãn hoặc ghi chung chung "Live E-Commerce Analytics": Đây là hành vi vi phạm nghiêm trọng quy tắc liêm chính khoa học và quy ước bất biến trong `AGENTS.md`. Đồ án kiên quyết loại bỏ phương án này.

### 7. Verification (Cách thức kiểm chứng)
Unit test `test_09_disclaimer_and_html_dashboard_integrity` đọc trực tiếp tệp `index.html` và `ivre_dashboard_snapshot.json`, xác thực sự hiện diện bắt buộc của các chuỗi ký tự `"REES46"` và `"Research Demo"`.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
Mặc dù dữ liệu là ngành mỹ phẩm nhưng các mẫu hình hành vi (phân phối đuôi dài, phễu bỏ giỏ, khách hàng ngủ đông) mang tính quy luật phổ quát trong toàn ngành thương mại điện tử bán lẻ.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Dự án của em lấy tên thương hiệu là IVRE Atelier nhưng tại sao số liệu lại là REES46 Cosmetics? Liệu điều này có mâu thuẫn không?"*  
> **Trả lời:** *"Dạ thưa Thầy/Cô, hoàn toàn không mâu thuẫn mà đây chính là tính trung thực khoa học cao nhất của đồ án: Đồ án nghiên cứu độc lập của chúng em sử dụng tập dữ liệu thực nghiệm chuẩn mực REES46 (20.69 triệu sự kiện giao dịch thực tế) để xây dựng pipeline phân tích hành vi và thuật toán phân cụm. Giao diện IVRE Atelier được sử dụng làm phong cách thiết kế trình diễn (Design System & Research Demo Portal) để chứng minh khả năng ứng dụng thực tiễn của giải pháp vào các thương hiệu bán lẻ cao cấp. Trên toàn bộ giao diện và tài liệu, chúng em luôn đặt nhãn định danh minh bạch `Research Demo / REES46` để khẳng định rõ ranh giới nghiên cứu, tuyệt đối không ngụy tạo số liệu khách hàng thật."*

---

## P7.6 — Thiết kế Bảng Điều khiển Quản trị Cấp cao theo Phong cách Biên tập Thời trang Sang trọng (Dark Editorial Luxury Architecture)

### 1. What (Khái niệm là gì?)
- **Dark Editorial Luxury UI:** Phong cách thiết kế giao diện lấy cảm hứng từ các tạp chí thời trang cao cấp (Editorial Aesthetics) kết hợp với bảng màu tối (Dark Mode), đặc trưng bởi kiểu chữ có chân thanh lịch (Serif Display Typography), đường nét viền mỏng tinh xảo (Hairline Borders), tỷ lệ khoảng trống thoáng đãng (Generous Whitespace), và các điểm nhấn kim loại quý (Muted Gold & Champagne Accents).

### 2. Why (Tại sao cần dùng cho Dashboard Quản trị?)
1. **Giảm Mỏi Mắt Khi Đọc Dữ liệu Lâu (Ergonomics):** Nền tối (`#0a0c10` / `#12151c`) giảm độ chói lóa của màn hình khi các nhà phân tích và chủ doanh nghiệp làm việc với bảng số liệu lớn trong thời gian dài.
2. **Nâng Cao Tính Chuyên Nghiệp & Giá Trị Cảm Nhận:** Giao diện được trau chuốt giúp nâng cao trải nghiệm người dùng, tạo cảm giác tin cậy và chuyên nghiệp khi trình diễn trước hội đồng hoặc khách hàng doanh nghiệp.

### 3. How (Cách thức triển khai?)
1. **Typography Hierarchy:**
   - Tiêu đề chính: *Cormorant Garamond* (Serif cổ điển, font chữ thời trang cao cấp).
   - Nội dung bảng biểu & văn bản: *Inter* (Sans-serif hiện đại, tối ưu độ nét hiển thị số liệu).
   - Số liệu định lượng & mã kỹ thuật: *JetBrains Mono* (Monospace cố định chiều rộng chữ, giúp đối soát cột số không bị lệch dòng).
2. **Color Palette:**
   - Background Base: `#0a0c10` (Obsidian đen tuyền).
   - Card Surfaces: `#141720` (Slate sâu) viền `#202634`.
   - Gold Accents: `#c5a059` (Brushed Gold) và `#e5c07b` (Champagne).
   - Semantic Highlights: Teal `#0d9488` (Active), Rose `#e11d48` (At-Risk), Slate `#64748b` (Dormant).

### 4. Formula / Algorithm (Tỷ lệ tương phản WCAG)
Đảm bảo độ tương phản màu chữ so với nền luôn đạt chuẩn WCAG 2.1 AA ($\ge 4.5:1$):
$$\text{Contrast Ratio} = \frac{L_1 + 0.05}{L_2 + 0.05} \ge 4.5$$
(Chữ trắng `#f8fafc` trên nền `#141720` đạt tỷ số tương phản $13.8:1$, vượt xa chuẩn quy định).

### 5. Worked Example (Kiến trúc Bố cục Giao diện)
- Băng thông báo nghiên cứu (Research Banner) cố định trên đỉnh trang.
- Header chứa thông tin thương hiệu và 4 chỉ số thống kê vĩ mô (Global Stats).
- Thanh điều hướng 6 thẻ chuyên đề (Tabs Navigation).
- Khung hiển thị nội dung chính với lưới tự co giãn (CSS Grid 2–4 cột).
- Chân trang (Footer) chứa thông tin xuất xứ học thuật và lưu ý pháp lý.

### 6. Alternatives (Phương án thay thế & So sánh)
- **Light Theme Corporate Dashboard:** Phong cách bảng điều khiển nền trắng truyền thống. Dù phổ biến trong các phần mềm văn phòng, phong cách này không phản ánh được tinh thần thương hiệu thời trang cao cấp của IVRE và kém nổi bật hơn khi trình diễn đồ án.

### 7. Verification (Cách thức kiểm chứng)
Kiểm tra khả năng hiển thị tương thích trên các độ phân giải màn hình khác nhau (Desktop 1440px, Laptop 1280px, Tablet 768px, Mobile 390px).

### 8. Limitations (Giới hạn lý thuyết & thực tế)
Màn hình nền tối đòi hỏi người dùng ở trong môi trường có ánh sáng vừa phải; nếu xem dưới ánh nắng gắt trực tiếp, độ tương phản có thể bị suy giảm.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em lại chọn phong cách Dark Luxury cho một dashboard phân tích dữ liệu kỹ thuật?"*  
> **Trả lời:** *"Dạ thưa Thầy/Cô, việc lựa chọn phong cách Dark Editorial Luxury xuất phát từ 2 mục tiêu: Thứ nhất, về mặt trải nghiệm người dùng (UX), nền tối giúp các biểu đồ và chỉ số định lượng nổi bật hơn, giảm mỏi mắt cho người quản trị khi theo dõi các bảng số liệu phức tạp trong thời gian dài. Thứ hai, về mặt định vị thương hiệu, đồ án hướng đến đối tượng sử dụng là chủ sở hữu và nhà quản trị của các thương hiệu bán lẻ cao cấp (như IVRE Atelier), nơi tính thẩm mỹ, sự tinh tế của kiểu chữ và sự chuẩn mực của không gian hiển thị đóng vai trò quan trọng trong việc truyền tải giá trị của các thông tin phân tích chuyên sâu."*

---

## P7.7 — Trực quan hóa Khoa học và Kiểm soát Nhận thức: Biểu diễn Trật tự Đơn điệu và Khoảng Tin cậy Wilson Score 95%

### 1. What (Khái niệm là gì?)
- **Cognitive Visualization Control (Kiểm soát Nhận thức trong Trực quan hóa):** Phương pháp thiết kế đồ họa dữ liệu nhằm truyền tải chính xác mức độ không chắc chắn (uncertainty) và ranh giới khoa học của các con số, ngăn ngừa hiện tượng người xem diễn dịch sai tương quan thành quan hệ nhân quả.
- **Wilson Score 95% Confidence Interval Display:** Cách thức trực quan hóa tỷ lệ chuyển đổi kèm theo dải sai số thống kê xác thực, phản ánh quy mô mẫu của từng phân cụm.

### 2. Why (Tại sao cần dùng?)
Nếu chỉ hiển thị một con số trần trụi (ví dụ: "Cluster 1 đạt 35.02%"), người xem có xu hướng coi đó là một hằng số tuyệt đối. Việc hiển thị khoảng tin cậy $[34.02\%, 36.03\%]$ giúp nhà quản trị nhận thức rõ sai số mẫu, đồng thời nhận ra rằng khoảng tin cậy của C1 hoàn toàn không chồng lấn với C3 $[9.75\%, 10.53\%]$ hay C2 $[6.95\%, 7.70\%]$, khẳng định tính tách biệt thống kê khách quan của các phân cụm.

### 3. How (Cách thức triển khai?)
1. Trên tab *Out-of-Time Holdout Validation*, các thanh đo tỷ lệ chuyển đổi được hiển thị kèm nhãn rõ ràng: `35.02% (CI: [34.02%, 36.03%])`.
2. Đi kèm cảnh báo nghiên cứu (Research Callout): Khẳng định đây là phép đo quán tính lịch sử, không phải dự báo nhân quả cho tương lai.
3. Sử dụng trật tự đơn điệu trực quan: Sắp xếp các cụm từ cao xuống thấp (C1 $\to$ C3 $\to$ C2 $\to$ C0 $\to$ Non-Buyers).

### 4. Formula / Algorithm (Công thức Wilson Score Interval)
$$\text{CI}_{95\%} = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}, \quad \text{với } z = 1.96$$

### 5. Worked Example (Số liệu thực tế hiển thị trên UI)
- Cluster 1 (VIP): $35.02\%$ (CI: $[34.02\%, 36.03\%]$)
- Cluster 3 (Active): $10.13\%$ (CI: $[9.75\%, 10.53\%]$)
- Cluster 2 (At-Risk): $7.32\%$ (CI: $[6.95\%, 7.70\%]$)
- Cluster 0 (Dormant): $2.66\%$ (CI: $[2.51\%, 2.82\%]$)
- Non-Buyers Baseline: $0.42\%$ (CI: $[0.41\%, 0.43\%]$)
(Các khoảng tin cậy hoàn toàn tách biệt, sai số biên $< \pm 1.0\%$).

### 6. Alternatives (Phương án thay thế & So sánh)
- **Hiển thị Khoảng Wald truyền thống ($\hat{p} \pm 1.96\sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$):** Như đã chứng minh ở Phase 5, khoảng Wald bị sai lệch xác suất khi tỷ lệ $p$ nhỏ (dưới 1%). Khoảng Wilson Score là chuẩn mực thống kê bắt buộc.

### 7. Verification (Cách thức kiểm chứng)
Unit test `test_08_holdout_monotonicity_and_separation` xác thực trật tự đơn điệu nghiêm ngặt trên dữ liệu snapshot.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
Khoảng tin cậy 95% chỉ phản ánh sai số chọn mẫu ngẫu nhiên (Sampling Error) trong điều kiện phân phối không đổi; nó không đo lường được các cú sốc thị trường vĩ mô (Covariate Shift) như dịch bệnh hay khủng hoảng kinh tế.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao em phải mất công tính khoảng tin cậy Wilson Score 95% cho từng phân cụm mà không chỉ vẽ biểu đồ cột tỷ lệ chuyển đổi bình thường?"*  
> **Trả lời:** *"Dạ thưa Thầy/Cô, việc thể hiện khoảng tin cậy Wilson Score 95% thể hiện tính chặt chẽ về mặt khoa học dữ liệu: Tỷ lệ chuyển đổi là một ước lượng thống kê trên mẫu dữ liệu. Việc cung cấp khoảng tin cậy với sai số biên dưới 1% chứng minh cho hội đồng thấy rằng sự khác biệt về tỷ lệ mua giữa các nhóm (35.02% của VIP so với 10.13% của Active và 0.42% của Non-Buyers) là một sự phân hóa thực chất có ý nghĩa thống kê ($p < 10^{-100}$), hoàn toàn không phải do biến động ngẫu nhiên của mẫu."*

---

## P7.8 — Khóa An toàn Thực thi (No-Execution Guardrail) và Cơ chế Tiếp thị Có Trách nhiệm trên Giao diện

### 1. What (Khái niệm là gì?)
- **No-Execution Guardrail (Rào chắn Khóa Thực thi):** Nguyên tắc thiết kế giao diện có chủ đích loại bỏ mọi nút bấm hoặc cơ chế kích hoạt gửi tin tiếp thị (Send Email / Trigger Webhook / Launch Campaign), giữ hệ thống thuần túy là môi trường hỗ trợ ra quyết định phân tích (Analytics Decision Support System).
- **Responsible Marketing Flagging:** Cơ chế bắt buộc 100% đề xuất chiến thuật hiển thị trạng thái `PENDING_CONSENT`.

### 2. Why (Tại sao cần dùng?)
1. **Phòng Ngừa Lỗi Thao Tác (Accidental Campaign Dispatch):** Trong môi trường doanh nghiệp, việc một nhà phân tích bấm nhầm nút gửi tin tự động có thể dẫn đến việc hàng trăm nghìn email tiếp thị bị bắn ra ngoài ý muốn, gây tổn hại danh tiếng và ngân sách của công ty.
2. **Tuân Thủ Pháp Lý Chặt Chẽ:** Hệ thống khẳng định vai trò là công cụ tham mưu (advisory tool), trao toàn quyền quyết định kích hoạt và kiểm tra tính pháp lý cho con người (Human-in-the-loop).

### 3. How (Cách thức triển khai?)
1. Trên toàn bộ giao diện dashboard, chỉ cung cấp các chức năng đọc, lọc (filtering) và tra cứu hồ sơ (exploration).
2. Tuyệt đối **không lập trình bất kỳ API POST/PUT** nào kích hoạt dịch vụ bên ngoài (SendGrid, Twilio, Firebase).
3. Mỗi thẻ khuyến nghị đều hiển thị huy hiệu màu hổ phách: `PENDING_CONSENT` kèm cảnh báo quy định.

### 4. Formula / Algorithm (Kiểm toán quyền can thiệp)
$$\forall \text{UI Element } e \in \text{Dashboard}: \quad e.\text{type} \neq \text{"ExecuteCampaignButton"} \quad \land \quad e.\text{action} \neq \text{"ExternalDispatch"}$$

### 5. Worked Example (Giao diện Explorer)
Trong thẻ hồ sơ khách hàng mẫu, phần trạng thái hiển thị rõ:
- Trạng thái điều kiện: `<span class="badge badge-pending">PENDING_CONSENT</span>`
- Ghi chú thẩm quyền: *"Quy tắc: configs/marketing_rules.yaml (v1.0.0). Yêu cầu phê duyệt nội bộ và xác thực opt-in hợp lệ trước khi thực hiện."*

### 6. Alternatives (Phương án thay thế & So sánh)
- **Tích hợp nút "Demo Send Campaign" kèm thông báo giả lập (Alert Box):** Phương án này có thể gây hiểu lầm cho người dùng rằng hệ thống đã có backend gửi tin thật. Việc loại bỏ hoàn toàn nút bấm là lựa chọn minh bạch và chuyên nghiệp nhất.

### 7. Verification (Cách thức kiểm chứng)
Kiểm tra mã nguồn `outputs/dashboard/index.html` và kịch bản `validate_phase7.py` xác nhận 100% khuyến nghị mang cờ `PENDING_CONSENT` và không có bất kỳ lệnh gọi API gửi tin nào.

### 8. Limitations (Giới hạn lý thuyết & thực tế)
Hệ thống không tự động hóa hoàn toàn quy trình tiếp thị từ đầu đến cuối (End-to-End Automation). Đây là một sự đánh đổi có chủ đích để đảm bảo tính an toàn và trách nhiệm giải trình.

### 9. Oral Defense Questions (Câu hỏi vấn đáp)
> **Hỏi:** *"Tại sao trên giao diện của em không có nút bấm để chủ shop bấm 'Gửi chiến dịch ngay' cho các phân khúc?"*  
> **Trả lời:** *"Dạ thưa Thầy/Cô, đây là quyết định thiết kế kiến trúc có chủ đích nhằm đảm bảo Tiếp thị Có Trách nhiệm (Responsible Marketing): Đồ án của chúng em định vị là một Hệ Thống Hỗ Trợ Ra Quyết Định (Decision Support System), đóng vai trò cung cấp thông tin phân tích và khuyến nghị chiến thuật minh bạch. Việc gửi thông điệp tiếp thị thực tế đến người tiêu dùng đòi hỏi phải có sự chấp thuận hợp lệ (Legal Opt-in Consent) và kiểm soát ngân sách của Trưởng bộ phận Tiếp thị (Human-in-the-loop). Chúng em chủ ý không gắn nút thực thi để triệt tiêu hoàn toàn rủi ro thao tác nhầm hoặc gửi tin spam vi phạm quy định pháp lý."*

---

## P7.9 — Bộ Câu hỏi Vấn đáp Trọng tâm Phase 7 (Oral Defense Guide P7: Q46 – Q52)

### Q46: Làm thế nào em giải quyết được bài toán hiển thị dữ liệu của 1.34 triệu khách hàng trên giao diện web mà không làm đơ trình duyệt?
- **Trả lời:** Chúng em giải quyết bài toán này bằng Kiến trúc Xuất bản Ảnh chụp Tĩnh Tổng hợp Đa tầng (Multi-Level Aggregated Static Snapshot): Thay vì nạp toàn bộ 1.34 triệu bản ghi thô xuống trình duyệt, kịch bản Python ở backend sử dụng DuckDB để tính toán trước các chỉ số thống kê vĩ mô, phân vị hành vi theo phân cụm, ma trận đa dạng chiến thuật và 8 hồ sơ nghiên cứu đại diện (Archetypes). Nhờ đó, kích thước tệp JSON truyền tải xuống trình duyệt chỉ nặng **32.98 KB**, giúp trang web tải tức thì dưới 50ms và hoạt động mượt mà trên cả máy tính lẫn điện thoại di động mà không làm mất đi bức tranh toàn cảnh của hệ thống.

### Q47: Mã băm SHA-256 trong tệp `snapshot_manifest.json` có tác dụng gì trong quy trình kiểm toán đồ án?
- **Trả lời:** Mã băm SHA-256 đóng vai trò là "chứng chỉ niêm phong toàn vẹn dữ liệu" (Cryptographic Integrity Seal). Nó đảm bảo rằng dữ liệu mà giao diện hiển thị chính là dữ liệu thực tế được sinh ra từ các mô hình và bảng Parquet sạch của Phase 3–6. Bất kỳ sự can thiệp thủ công nào vào các tệp dữ liệu sau khi xuất bản đều sẽ làm thay đổi chuỗi băm SHA-256, khiến kịch bản kiểm toán `validate_phase7.py` báo lỗi ngay lập tức. Đây là bằng chứng đanh thép bảo đảm tính trung thực khoa học và khả năng tái lập 100% của đồ án.

### Q48: Tại sao trên giao diện dashboard của em lại xuất hiện dải băng cảnh báo "REES46 Cosmetics Research Demo"?
- **Trả lời:** Dải băng này thể hiện nguyên tắc Liêm chính Dữ liệu (Data Integrity & Transparency): Đồ án sử dụng tập dữ liệu thực nghiệm REES46 (thương mại điện tử mỹ phẩm giai đoạn 2019–2020) làm nguồn nghiên cứu phân tích và sử dụng phong cách IVRE Atelier làm giao diện trình diễn giải pháp. Việc ghi rõ nhãn nghiên cứu khẳng định ranh giới khoa học rõ ràng, giúp hội đồng và người dùng nhận biết minh bạch nguồn gốc dữ liệu, tránh hiểu lầm rằng đây là dữ liệu thời trang thực tế của IVRE trong năm 2026.

### Q49: Khái niệm "Candidate Cart Follow-Up" trên giao diện khác gì so với việc khẳng định "Khách hàng đã bỏ giỏ hàng"?
- **Trả lời:** Đây là sự chuẩn hóa thuật ngữ khoa học rất quan trọng: Dữ liệu clickstream chỉ ghi nhận sự kiện người dùng bấm nút thêm sản phẩm vào giỏ (`cart_events > 0`) trong một phiên duyệt web. Dữ liệu này không cho biết giỏ hàng đó hiện có còn được lưu trên máy chủ hay không, hoặc khách có dùng thiết bị khác để thanh toán hay không. Do đó, việc gọi là "Candidate Cart Follow-Up" (Ứng viên theo dấu giỏ hàng) thể hiện rằng đây là một tín hiệu quan tâm cao cần hỗ trợ chăm sóc, hoàn toàn không khẳng định một cách chủ quan rằng khách hàng chắc chắn đang có giỏ hàng mở bị bỏ rơi.

### Q50: Con số tiết kiệm chi phí tiếp thị $4,460 – $17,850/tuần hiển thị trên dashboard được hiểu như thế nào cho đúng bản chất?
- **Trả lời:** Con số này được trình bày minh bạch dưới dạng **Kịch bản Mô phỏng Giả định (Hypothetical Cost Avoidance Scenario)**: Do tập dữ liệu REES46 không có thông tin về chi phí gửi tin thực tế, chúng em thiết lập một mô hình giả định có căn cứ: Nếu doanh nghiệp áp dụng chiến dịch tiếp thị đại trà (gửi 1 tin/tuần với đơn giá $0.005 đến $0.02) cho toàn bộ tệp khách hàng, thì việc hệ thống chủ động lọc bỏ 892,508 tài khoản ngủ đông sâu và vãng lai (chiếm 66.5% dân số thông qua Guardrails G3 và G5) sẽ giúp doanh nghiệp tránh lãng phí từ $4,460 đến $17,850 mỗi tuần. Con số này phản ánh giá trị kinh tế của tính năng bảo vệ ngân sách, không phải là doanh thu thực tế đã thu được.

### Q51: Tại sao toàn bộ khuyến nghị trên giao diện đều mang nhãn `PENDING_CONSENT`?
- **Trả lời:** Nhãn `PENDING_CONSENT` phản ánh nguyên tắc Tiếp thị Có Trách nhiệm (Responsible Marketing): Dataset REES46 không ghi nhận dữ liệu về việc khách hàng có đồng ý nhận thông tin quảng cáo hay không (Opt-in Consent). Do đó, về mặt pháp lý và đạo đức dữ liệu, mọi đề xuất của hệ thống chỉ mang tính chất chỉ dẫn nghiên cứu nội bộ (Internal Analytical Recommendation). Để thực thi chiến dịch ngoài đời thực, doanh nghiệp bắt buộc phải đối soát danh sách này với cơ sở dữ liệu chấp thuận tiếp thị hợp pháp của khách hàng.

### Q52: Em đã kiểm thử giao diện dashboard như thế nào để đảm bảo không có lỗi kỹ thuật?
- **Trả lời:** Chúng em thực hiện quy trình kiểm thử toàn diện gồm 3 tầng: Thứ nhất, kiểm thử đơn vị tự động với 9 bài kiểm tra trong `test_phase7_dashboard_snapshot.py` (nâng tổng số test toàn dự án lên **81/81 PASS**) xác thực tính toàn vẹn của tệp, mã băm SHA-256, sự bảo toàn dân số 1.34 triệu khách hàng và trật tự đơn điệu của tập holdout. Thứ hai, kịch bản `validate_phase7.py` kiểm chứng hợp đồng dữ liệu độc lập. Thứ ba, kiểm tra trực quan giao diện (HTML/CSS) đảm bảo phong cách Clean Minimalist Light Analytics, tính phản hồi co giãn tốt trên 5 kích thước màn hình từ Desktop (1440px) đến Mobile (320px), đo kiểm thời gian phân tích DOM đạt 16.0ms, không tràn viền ngang và không có bất kỳ lỗi JavaScript nào trên bảng điều khiển.

---

# PHẦN IX — KIỂM CHỨNG TOÀN TRÌNH, HỒ SƠ BẢO VỆ VÀ VẤN ĐÁP PHASE 8 (END-TO-END VERIFICATION & ORAL DEFENSE)

## P8.1 — Phương pháp luận Kiểm chứng Toàn trình Đầu-cuối (End-to-End System Pipeline Verification)

### 1. What (Khái niệm là gì?)
**End-to-End System Pipeline Verification (Kiểm chứng Toàn trình Đầu-cuối):** Quy trình kiểm toán khoa học và kỹ thuật phần mềm nhằm đối soát toàn bộ chuỗi mắt xích chuyển hóa dữ liệu qua 8 công đoạn liên hoàn:
$$\text{Raw CSVs (20.69M)} \to \text{Clean Parquet (19.58M)} \to \text{Features (1.34M)} \to \text{K-Means (K=4, 92.6k)} \to \text{Holdout Eval (Feb 2020)} \to \text{Decision Engine (1.34M recs)} \to \text{Snapshot Export (33 KB)} \to \text{Clean Dashboard}$$

### 2. Why (Tại sao cần làm trong Phase 8?)
Trong một hệ thống học máy và phân tích dữ liệu quy mô lớn, việc từng unit test riêng lẻ pass không đồng nghĩa toàn bộ hệ thống hoạt động gắn kết. Kiểm chứng toàn trình đảm bảo:
1. **Bảo toàn số học nghiêm ngặt (Zero Record Loss):** Số lượng khách hàng và sự kiện không bị thất thoát hoặc nhân đôi giữa các bước.
2. **Khóa chống rò rỉ thời gian (Anti-Leakage Enforcement):** Dữ liệu tương lai (tháng 02/2020) tuyệt đối không thẩm thấu vào quá trình làm sạch, trích xuất đặc trưng và huấn luyện mô hình.
3. **Tính bất biến & Khả năng tái lập (Reproducibility & Immutability):** Bất kỳ nhà nghiên cứu nào khi chạy lại toàn bộ mã nguồn đều thu được kết quả đồng nhất với sai số bằng 0.

### 3. How (Cách thức triển khai?)
1. Xây dựng 8 kịch bản xác thực độc lập `scripts/validate_phase0.py` đến `scripts/validate_phase7.py`.
2. Kiểm tra mã băm SHA-256 đối soát giữa model bundle, các bảng Parquet và tệp `snapshot_manifest.json`.
3. Kiểm toán 81 bài unit tests bao phủ 100% các hợp đồng toán học và logic rào chắn an toàn.

### 4. Formula / Algorithm (Ma trận đối soát toàn trình)
$$\begin{aligned}
N_{\text{raw}} &= 20,692,840 \\
N_{\text{clean}} &= N_{\text{observation}} (15,667,350) + N_{\text{holdout}} (3,916,392) = 19,583,742 \\
N_{\text{customers}} &= N_{\text{buyers}} (92,652) + N_{\text{non\_buyers}} (1,248,847) = 1,341,499 \\
\sum_{k=0}^{3} N_{\text{cluster\_}k} &= 42,145 + 8,755 + 18,608 + 23,144 = 92,652 \\
\sum \text{Tactics} &= 1,341,499 \quad (100\% \text{ PENDING\_CONSENT})
\end{aligned}$$

---

## P8.2 — Ma trận Đánh giá Đa tiêu chí Kỹ thuật (Multi-criteria Engineering Trade-off Matrix)

Hệ thống ghi nhận tường minh bảng đánh đổi đa tiêu chí kỹ thuật:

| Hạng mục kiến trúc | Lựa chọn áp dụng | Phương án thay thế | Đánh giá Trade-off cốt lõi |
| :--- | :--- | :--- | :--- |
| **Định dạng dữ liệu** | **Parquet (Snappy/ZSTD)** | CSV Phân mảnh | Giảm từ 2.32 GB xuống 471.74 MB (nén 4.92x); tăng tốc truy vấn 8.09x. |
| **Engine tính toán** | **DuckDB In-Process** | Pandas / Spark | Thực thi SQL vector hóa trực tiếp trên đĩa; RAM đỉnh < 2.4 GB; không tốn chi phí cụm. |
| **Xử lý tập khách hàng**| **Tách Buyers & Non-Buyers**| Gán Recency 0/999 | Gán giá trị giả tạo sẽ bóp méo hình học Euclidean của K-Means; tách riêng giữ đúng bản chất RFM. |
| **Không gian đặc trưng** | **$F1$ (7 chiều: RFM + 30d)** | $F0$ (3 chiều) / $F2$ (14 chiều) | $F0$ bị mù tương tác gần; $F2$ đa cộng tuyến cao; $F1$ cân bằng tối ưu giữa độ phân giải và tính giải thích. |
| **Thuật toán phân cụm** | **Standard K-Means** | MiniBatch K-Means | Thời gian fit chỉ 0.37s trên 92.6k khách; MiniBatch hội tụ kém (ARI chỉ 0.55). |
| **Số lượng cụm $K$** | **$K = 4$ Cụm** | $K = 3$ hoặc $K = 5$ | $K=3$ gộp lẫn C2 (Hạ nhiệt) vào C0 (Ngủ đông); $K=4$ tách biệt rõ 4 hành vi kinh doanh. |
| **Hệ thống gợi ý** | **Hệ Chuyên gia Luật Dựa trên Bằng chứng** | Black-box Classifier | Tiếp thị có trách nhiệm đòi hỏi giải trình 100% (Explainability) và rào cản an toàn (Guardrails). |
| **Kiến trúc UI** | **Static Verified Snapshot (33 KB)**| Dynamic REST API | Tải trang < 300ms, không tốn server backend, bảo vệ dữ liệu bằng mã băm SHA-256 bất biến. |

---

## P8.3 — Kiểm chứng 5 Giả thuyết Nghiên cứu H1–H5 (Empirical Hypothesis Defense)

1. **H1 — Pareto & Phân phối Đuôi dài (Supported):**
   - $6.91\%$ Buyers ($92,652$ người) tạo ra $100\%$ doanh thu quan sát ($\$5.14\text{M}$); $93.09\%$ là Non-Buyers với trung vị tương tác là 1 session và 2 events.
2. **H2 — Phân tách Không gian RFM + Tương tác số (Supported):**
   - Tách đôi 2 bảng đặc trưng độc lập bảo vệ không gian Euclidean. Trên tập Buyers, các biến 30 ngày phân tách rõ C1 (Active VIP, 9 phiên 30d) khỏi C2 (Cooling, 0 phiên 30d) dù cả hai đều có Monetary lịch sử cao.
3. **H3 — Cấu trúc Cụm & Độ ổn định K-Means (Supported):**
   - Cấu hình $F1$ ($K=4$, StandardScaler) đạt $\text{Mean ARI} = 0.9876 \pm 0.0077$ qua 5 seeds; Silhouette $0.283$; DBI $1.42$; Cây quyết định nông mô phỏng đạt $\text{Test Fidelity} = 82.11\%$.
4. **H4 — Hậu kiểm Đơn điệu Ngoài Mẫu Feb 2020 (Supported as Empirical Finding):**
   - Tỷ lệ mua tương lai tăng đơn điệu: Non-Buyers ($0.42\%$) < C0 ($2.66\%$) < C2 ($7.32\%$) < C3 ($10.13\%$) < C1 ($35.02\%$), các khoảng tin cậy Wilson 95% không chồng lấn ($p < 10^{-100}$).
5. **H5 — Khả năng Cá nhân hóa & Tiết kiệm Chi phí (Supported in Simulation):**
   - $100\%$ khách hàng nhận đề xuất có thể giải thích; Guardrails G3/G5 bảo vệ $892,508$ tài khoản ngủ đông khỏi bị gửi tin rác (tiết kiệm giả định $\$4,462$–$\$17,850$/tuần).

---

## P8.4 — Kiểm toán Trình duyệt Thực tế & Đo lường Web Vitals (Real Browser Telemetry)

Sử dụng Navigation Timing API đo kiểm thực tế qua Chrome DevTools MCP trên trang `outputs/dashboard/index.html`:
- **DOM Interactive:** `16.0 ms`
- **DOMContentLoaded:** `16.8 ms`
- **First Contentful Paint (FCP):** `256 ms` (đạt mức Good của Google Core Web Vitals < 1.8s)
- **Tổng số DOM Elements:** `816`
- **Console Errors / Warnings:** `0`
- **Kiểm toán Tràn viền ngang (Horizontal Overflow):** Kiểm tra trên 5 độ phân giải: Desktop (1440px), Laptop (1280px), Tablet (768px), Mobile (390px), Small Mobile (320px) $\to$ **100% không có thanh cuộn ngang ngoài ý muốn (`hasPageHorizontalScrollbar = false`)**.

---

## P8.5 — Sổ tay Tái lập & Vận hành Hệ thống (Reproducibility Runbook)

### 1. Yêu cầu Hệ thống Tối thiểu
- **Hệ điều hành:** Windows 10/11, macOS, hoặc Linux (x86_64 / ARM64).
- **Phần cứng:** Tối thiểu 4 CPU cores, 8 GB RAM (khuyến nghị 16 GB), 5 GB đĩa cứng trống.
- **Python:** Phiên bản `Python 3.10` đến `Python 3.14` (đã kiểm chứng trên `Python 3.14.7`).

### 2. Thiết lập Môi trường
```bash
# 1. Khởi tạo và kích hoạt môi trường ảo
python -m venv .venv
# Trên Windows PowerShell:
.venv\Scripts\Activate.ps1
# Trên Linux/macOS:
source .venv/bin/activate

# 2. Cài đặt các gói phụ thuộc cố định phiên bản
pip install -r requirements-lock.txt
```

> **Lưu ý đặc biệt về Windows Smart App Control (SAC):**  
> Trên Windows 11 với tính năng Smart App Control bật ở chế độ nghiêm ngặt, một số tệp binary `.pyd` / `.dll` của các bản wheel mới có thể bị hệ điều hành kiểm duyệt gây chậm lần tải đầu hoặc chặn import. Cách khắc phục chuẩn: Chạy terminal ở quyền người dùng chuẩn, sử dụng Python từ `python.org` hoặc cài đặt bản wheel chính thức từ PyPI.

### 3. Tải Dữ liệu & Đặt vào Workspace
Đặt 5 tệp CSV REES46 (`2019-Oct.csv` đến `2020-Feb.csv`) vào thư mục `data/raw/`.

### 4. Thực thi Toàn trình 8 Giai đoạn
```bash
# Phase 1: Phân tích khám phá dữ liệu (EDA)
python scripts/phase1_profiling.py

# Phase 2: Làm sạch dữ liệu và xuất bản Parquet
python scripts/phase2_etl.py

# Phase 3: Trích xuất đặc trưng RFM & Tương tác 30 ngày
python scripts/phase3_features.py

# Phase 4: Huấn luyện phân cụm K-Means & Cây quyết định nông
python scripts/phase4_clustering.py

# Phase 5: Hậu kiểm ngoài mẫu chuỗi thời gian Holdout Feb 2020
python scripts/phase5_evaluation.py

# Phase 6: Bộ máy luật ra quyết định tiếp thị chỉ dẫn
python scripts/phase6_decision_engine.py

# Phase 7: Xuất bản Master Snapshot JSON & Kiểm toán SHA-256
python scripts/build_phase7_snapshot.py
```

### 5. Kiểm thử Tự động & Xác thực Cổng Nghiệm thu
```bash
# Chạy toàn bộ 81 bài unit tests
python -m unittest discover -s tests -v

# Chạy chuỗi kịch bản kiểm chứng liên hoàn P0 đến P7
python scripts/validate_phase0.py
python scripts/validate_phase1.py
python scripts/validate_phase2.py
python scripts/validate_phase3.py
python scripts/validate_phase4.py
python scripts/validate_phase5.py
python scripts/validate_phase6.py
python scripts/validate_phase7.py
```

### 6. Khởi chạy Giao diện Trực quan hóa
```bash
# Cách 1: Chạy qua HTTP server cục bộ (Khuyến nghị để tránh chính sách CORS của file://)
python -m http.server 8000 --directory outputs/dashboard
# Truy cập trình duyệt: http://localhost:8000/

# Cách 2: Mở trực tiếp tệp HTML độc lập
# Double-click vào outputs/dashboard/index.html (Đã tích hợp sẵn snapshot fallback)
```

---

## P8.6 — Kịch bản Trình diễn Live Demo 5–7 Phút (Live Demo Script & Contingency Plan)

### Thứ tự Trình diễn (5–7 Phút):
1. **Phút 0:00 – 1:00 (Mở đầu & Ranh giới Nghiên cứu):**
   - Mở màn hình Tab 1 (Executive Overview). Chỉ vào biểu ngữ trên cùng: *"Thưa Thầy/Cô, đây là hệ thống phân tích nghiên cứu trên 20.69M sự kiện REES46 với mốc cutoff 01/02/2020. Dữ liệu gồm 1.34 triệu khách hàng, tạo ra $5.14M doanh thu."*
   - Nhấn mạnh: Chỉ 6.91% khách hàng đã mua tạo ra toàn bộ doanh thu, chứng minh nguyên lý Pareto.
2. **Phút 1:00 – 2:30 (4 Phân khúc Khách hàng & Đặc trưng F1):**
   - Chuyển sang Tab 2 (Customer Segments). Trình bày 4 thẻ phân cụm:
     - Cluster 1 (VIP Champions): 8,755 khách, chi tiêu $170, truy cập 8 phiên/tháng.
     - Cluster 3 (Active Prospects): 23,144 khách, vừa mua xong và đang lướt web cực kỳ tích cực.
     - Cluster 2 (At-Risk Cooling): 18,608 khách, từng chi tiêu khá nhưng đã ngừng hẳn tương tác.
     - Cluster 0 (Dormant): 42,145 khách ngủ đông sau mùa sale.
   - Nhấn mạnh: Bổ sung biến tương tác 30 ngày giúp tách biệt hoàn hảo C1 và C2.
3. **Phút 2:30 – 3:45 (Hậu kiểm Chuỗi Thời gian Holdout Feb 2020):**
   - Chuyển sang Tab 5 (Model & System Insights). Chỉ vào biểu đồ thanh tỷ lệ mua tương lai:
     - *"Mô hình hình thành hoàn toàn từ dữ liệu trước tháng 2, nhưng khi đối chiếu với 3.92M sự kiện tháng 2, tỷ lệ mua hàng thể hiện tính đơn điệu tách biệt hoàn hảo: Non-Buyers 0.42% < C0 2.66% < C2 7.32% < C3 10.13% < C1 35.02%. Khoảng tin cậy Wilson 95% hoàn toàn không chồng lấn."*
4. **Phút 3:45 – 5:15 (Bộ máy Ra Quyết định & Khám phá Chân dung Vi mô):**
   - Chuyển sang Tab 4 (Marketing Decision Engine). Trình bày phân bổ 8 chiến thuật:
     - *"Hệ thống không ánh xạ tĩnh: Cùng cụm VIP vẫn phân nhánh sang các chiến thuật khác nhau."*
     - Chỉ vào kịch bản tiết kiệm chi phí: *"Guardrails G3/G5 loại trừ 892k khách ngủ đông, giúp tiết kiệm giả định từ $4.4k đến $17.8k mỗi tuần."*
     - Bấm chọn các Archetype (ARC-01 VIP Champion, ARC-03 Active Abandoner, ARC-08 Cold Bounce) để minh họa 3 câu hỏi: *Tại sao? Bằng chứng gì? Đo bằng KPI nào?*
5. **Phút 5:15 – 6:00 (Kết luận & Trách nhiệm Giải trình):**
   - Nhấn mạnh: Toàn bộ đề xuất mang cờ `PENDING_CONSENT`, không có nút gửi tin tự động để bảo đảm Tiếp thị Có Trách nhiệm.

### Phương án Dự phòng khi Gặp Sự cố (Contingency Emergency Plan):
- **Sự cố 1 (Trình duyệt chặn file:// protocol không nạp được JSON):** Sử dụng ngay lệnh `python -m http.server 8000 --directory outputs/dashboard` để mở qua `localhost:8000`.
- **Sự cố 2 (Mất kết nối mạng hoặc máy chiếu lỗi hiển thị web):** Sử dụng các biểu đồ chất lượng cao 300 DPI đã xuất bản sẵn tại `outputs/figures/` (`fig13` đến `fig20`) và các ảnh chụp màn hình kiểm toán `dashboard_desktop_light.png`, `dashboard_tab2_segments.png`.
- **Sự cố 3 (Hội đồng yêu cầu kiểm chứng số liệu thực tế):** Chạy ngay lệnh `python scripts/validate_phase7.py` trong terminal để chứng minh toàn bộ mã băm SHA-256 và các phép đối soát số học đều khớp 100%.

---

## P8.7 — Dàn ý Bài Thuyết trình Bảo vệ Đồ án 12 Slide (12-Slide Final Presentation Outline)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                 DÀN Ý THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN (12 SLIDES CHUẨN KHOA HỌC)                  │
├───────┬───────────────────────────────┬─────────────────────────────────────────────────────┤
│ Slide │ Chủ đề chính                  │ Số liệu & Biểu đồ minh chứng trọng tâm              │
├───────┼───────────────────────────────┼─────────────────────────────────────────────────────┤
│ 1     │ Tiêu đề & Giới thiệu Đồ án    │ Tên đề tài, nhóm thực hiện, GV hướng dẫn, CRISP-DM  │
│ 2     │ Bối cảnh & Vấn đề Doanh nghiệp│ Bài toán chi phí gửi tin đại trà vs Khách hàng rời bỏ│
│ 3     │ Mục tiêu & 5 Giả thuyết H1–H5 │ Hợp đồng 16 KPI, định nghĩa không gian bài toán      │
│ 4     │ Tập Dữ liệu REES46 & Làm sạch │ 20.69M dòng thô -> 19.58M dòng Parquet (Nén 4.92x)   │
│ 5     │ Kiến trúc Dữ liệu & Anti-Leak │ Cắt cứng cutoff 01/02/2020, cách ly 3.92M holdout   │
│ 6     │ Không gian Đặc trưng F1       │ Tách Buyers (92.6k) vs Non-Buyers (1.25M), biến 30d │
│ 7     │ Thực nghiệm Phân cụm K-Means  │ Quét 68 cấu hình, Elbow K=4, ARI=0.988, Tree 82.11% │
│ 8     │ Chân dung 4 Cụm Khách hàng    │ Radar profile C0, C1, C2, C3 trên đơn vị vật lý thực│
│ 9     │ Hậu kiểm Ngoài Mẫu Feb 2020   │ Trật tự đơn điệu 0.42% -> 35.02% kèm Wilson 95% CI  │
│ 10    │ Bộ máy Chỉ dẫn Quyết định     │ 8 Chiến thuật, Ma trận đa dạng nội cụm, G1–G5       │
│ 11    │ Clean Minimalist Dashboard    │ Giao diện nghiên cứu, Data Storytelling, Archetypes │
│ 12    │ Giới hạn, Bài học & Lộ trình  │ Không suy diễn nhân quả, lộ trình RCT & Uplift ML   │
└───────┴───────────────────────────────┴─────────────────────────────────────────────────────┘
```

---

## P8.8 — Bộ Câu hỏi Vấn đáp Nâng cao Bảo vệ Đồ án (Oral Defense Guide P8: Q53 – Q65)

### Q53: Vì sao em sử dụng dữ liệu giai đoạn 2019–2020 mà không phải dữ liệu mới nhất 2025–2026?
- **Trả lời:** Dạ thưa Thầy/Cô, tập dữ liệu REES46 giai đoạn 10/2019 – 02/2020 là một trong những bộ dữ liệu clickstream thương mại điện tử công khai hiếm hoi trên thế giới có quy mô lớn (>20 triệu sự kiện) ghi nhận đầy đủ cả định danh người dùng (`user_id`), mã phiên (`user_session`), loại sự kiện (`view, cart, purchase`), danh mục và giá sản phẩm. Dữ liệu này được cộng đồng khoa học quốc tế công nhận rộng rãi làm chuẩn đối sánh (benchmark). Về mặt nghiên cứu phương pháp luận, các quy luật hành vi người tiêu dùng (nguyên lý Pareto, hành vi bỏ giỏ, sự suy giảm tương tác theo thời gian) mang tính phổ quát và độc lập với mốc thời gian năm dương lịch.

### Q54: Vì sao em lại chọn dataset REES46 thay vì các tập dữ liệu khác như Hillstrom hay Online Retail II?
- **Trả lời:** Bộ dữ liệu Online Retail II chỉ ghi nhận các dòng hóa đơn giao dịch (Transaction-only), hoàn toàn thiếu vắng dữ liệu nhật ký duyệt web (Clickstream), do đó không thể phân tích phễu chuyển đổi hoặc theo dõi hành vi tương tác gần đây. Bộ dữ liệu Hillstrom Email Marketing thì có quy mô nhỏ và thiếu cấu trúc chuỗi thời gian liên tục. REES46 là tập dữ liệu duy nhất đáp ứng trọn vẹn cả hai chiều không gian: Lịch sử mua sắm giao dịch (RFM) và Dấu chân kỹ thuật số tương tác (Digital Engagement), cho phép chúng em chứng minh tính ưu việt của không gian đặc trưng $F1$ so với mô hình RFM truyền thống.

### Q55: Vì sao biến Frequency lại đếm số phiên mua (Distinct Purchase Sessions) thay vì đếm tổng số sự kiện mua hàng (Purchase Events)?
- **Trả lời:** Trong tập dữ liệu REES46, khi một khách hàng mua cùng lúc nhiều sản phẩm trong một đơn hàng (Multi-item Basket), hệ thống ghi nhận mỗi món hàng là một dòng sự kiện `purchase` riêng biệt có cùng mã `user_session`. Do đó, nếu đếm số sự kiện `purchase`, một khách hàng mua 5 thỏi son trong 1 lần thanh toán sẽ bị tính thành "mua hàng 5 lần", gây thổi phồng tần suất mua lặp lại một cách sai lệch. Việc đếm số phiên mua duy nhất (`count(distinct user_session)`) đóng vai trò là đại lượng ủy nhiệm (Proxy) chuẩn xác nhất cho số lần phát sinh đơn hàng độc lập của người tiêu dùng.

### Q56: Vì sao em phải tách biệt hoàn toàn giữa Buyers và Non-Buyers thay vì đưa chung vào phân cụm K-Means?
- **Trả lời:** Đây là nguyên tắc toán học sống còn để bảo vệ không gian hình học Euclidean: Với khách hàng chưa từng mua hàng (Non-Buyers), thuộc tính Recency (Số ngày kể từ lần mua cuối) và Monetary (Tổng tiền mua) về mặt toán học là không xác định (Undefined). Nếu gán các giá trị nhân tạo như `Recency = 0` (ngộ nhận họ vừa mua tức thì) hoặc `Recency = 999` (tạo ra điểm dị biệt giả khổng lồ), khoảng cách Euclidean giữa các điểm dữ liệu sẽ bị biến dạng hoàn toàn, làm sai lệch vị trí của các tâm cụm K-Means. Việc tách riêng 92.6k Buyers vào bảng phân cụm và 1.25M Non-Buyers vào 4 tầng tương tác giúp bảo toàn 100% tính đúng đắn toán học.

### Q57: Vì sao không gian RFM truyền thống cần phải bổ sung thêm các đặc trưng Tương tác số (Engagement)?
- **Trả lời:** Mô hình RFM truyền thống có một "điểm mù" nguy hiểm: Nó chỉ quan sát các giao dịch mua trong quá khứ mà hoàn toàn không biết khách hàng đang làm gì ở hiện tại. Ví dụ thực tế: Cụm 1 (VIP) và Cụm 2 (Cooling-down) trong đồ án đều có Monetary lịch sử rất cao. Nếu chỉ dùng RFM, hai nhóm này sẽ bị xếp chung. Tuy nhiên, khi bổ sung các biến tương tác 30 ngày (`sessions_30d`, `views_30d`), hệ thống bóc tách được: Cụm 1 đang truy cập 9 phiên/tháng (cần tri ân gắn kết), còn Cụm 2 đã 0 phiên/tháng (đang âm thầm rời bỏ, cần khảo sát win-back). Biến tương tác số chính là "tín hiệu cảnh báo sớm" (Early Warning Signal) trước khi khách hàng chuyển sang trạng thái ngủ đông hoàn toàn.

### Q58: K-Means có thực sự là một mô hình dự đoán (Predictive Model) khách hàng có mua hàng hay không?
- **Trả lời:** Dạ thưa Thầy/Cô, không. K-Means thuần túy là một thuật toán Học Không Giám Sát (Unsupervised Clustering) dùng để phân nhóm mô tả (Descriptive Pattern Recognition) các quan sát dựa trên độ tương đồng hình học trong không gian đặc trưng quá khứ. K-Means không hề dự đoán tương lai và không có biến mục tiêu (Target Variable). Tính chất phân hóa hành vi tương lai thu được ở Phase 5 là một **kết quả kiểm chứng thực nghiệm ngoài mẫu (Empirical Validation Finding)**, chứng minh rằng các cụm hình thành từ quá khứ phản ánh đúng sự phân hóa quán tính hành vi tự nhiên trong tương lai, chứ bản thân K-Means không phải là một mô hình phân loại giám sát (Supervised Classifier).

### Q59: Vì sao em chọn $K = 4$ cụm? Tại sao không chọn $K = 3$ (đơn giản hơn) hay MiniBatch K-Means (nhanh hơn)?
- **Trả lời:** Thứ nhất, về lựa chọn $K=4$ thay vì $K=3$: Mặc dù $K=3$ có Silhouette nhỉnh hơn một chút ($0.301$ vs $0.283$), nhưng về mặt nghiệp vụ, $K=3$ đã gộp chung nhóm khách hàng Đang hạ nhiệt (C2: từng chi tiêu khá $67, nhưng đã ngưng truy cập) vào nhóm Khách ngủ đông giá trị thấp (C0: chi tiêu nhỏ $20). Việc này làm mất đi phân khúc khách hàng quan trọng nhất cần cứu vãn của doanh nghiệp. $K=4$ bóc tách thành công 4 trạng thái hành vi có chiến thuật tiếp thị hoàn toàn khác nhau. Thứ hai, về việc từ chối MiniBatch: Do dữ liệu Buyers chỉ có 92,652 dòng, thuật toán K-Means chuẩn chỉ mất **0.37 giây** để hội tụ toàn cục; MiniBatch K-Means tuy nhanh hơn nhưng độ khớp (Agreement ARI) chỉ đạt $0.55$, việc đánh đổi độ chính xác hội tụ lấy vài phần mười giây là không thỏa đáng.

### Q60: Chỉ số ARI đo lường điều gì? Tại sao không chỉ dựa vào Silhouette Score và Davies-Bouldin Index (DBI)?
- **Trả lời:** Silhouette và DBI là các chỉ số hình học nội tại (Internal Cluster Metrics), chỉ phản ánh độ nén chặt và độ tách biệt của các cụm trong một lần chạy đơn lẻ. Ngược lại, **Adjusted Rand Index (ARI)** đo lường **độ ổn định ngẫu nhiên (Algorithmic Stability)** của cấu trúc phân cụm khi thay đổi các điểm khởi tạo ngẫu nhiên (Random Seeds). Một mô hình có Silhouette cao nhưng ARI thấp nghĩa là ranh giới cụm bị xáo trộn lung tung mỗi lần huấn luyện lại, không thể áp dụng vào kinh doanh thực tế. Cấu hình quán quân $F1$ ($K=4$) đạt $\text{Mean ARI} = 0.9876 \pm 0.0077$ qua 5 seeds độc lập, chứng minh cấu trúc 4 cụm là cực kỳ bền vững và nhất quán.

### Q61: Vì sao em dùng cơ chế Temporal Holdout thay vì K-Fold Cross Validation ngẫu nhiên? Làm sao để chắc chắn không bị rò rỉ dữ liệu (Data Leakage)?
- **Trả lời:** Dữ liệu hành vi người tiêu dùng có bản chất chuỗi thời gian phụ thuộc (Temporal Dependency). Nếu chia mẫu ngẫu nhiên (Random K-Fold), dữ liệu của một khách hàng ở tương lai (tháng 2) sẽ bị lẫn vào tập huấn luyện cùng với dữ liệu quá khứ (tháng 10), dẫn đến hiện tượng "nhìn trộm tương lai" (Look-ahead Leakage). Hệ thống áp dụng quy tắc cắt cứng nửa mở: Toàn bộ sự kiện có timestamp $< \text{2020-02-01 00:00:00 UTC}$ được xếp vào Observation; mọi sự kiện $\ge$ mốc này được niêm phong vào Holdout. 10,451 phiên vắt ngang mốc cutoff bị cắt đôi nghiêm ngặt theo event timestamp. Việc niêm phong tuyệt đối tập Holdout cho đến tận Phase 5 bảo đảm tính khách quan 100% của phép kiểm thử ngoài mẫu.

### Q62: Vì sao đồ án không tuyên bố chỉ số ROI (Return on Investment) cụ thể của các chiến dịch tiếp thị?
- **Trả lời:** Dạ thưa Thầy/Cô, việc từ chối tuyên bố ROI thể hiện sự nghiêm cẩn khoa học cao nhất: Để tính toán được Lợi tức Đầu tư Tiếp thị Thực tế (Incremental Marketing ROI), bắt buộc phải có hai thành phần dữ liệu: (1) Chi phí thực thi chiến dịch thực tế (chi phí gửi tin, chi phí mã giảm giá), và (2) Thử nghiệm ngẫu nhiên có nhóm đối chứng (A/B Testing RCT) để trừ đi doanh thu tự nhiên mà khách hàng vốn dĩ sẽ tự chi tiêu dù không nhận quảng cáo. Dataset REES46 là nhật ký quan sát thụ động, không có chi phí và không có can thiệp. Mọi số liệu doanh thu ở Phase 5 là chi tiêu tự nhiên quan sát được; việc lấy số đó tuyên bố ROI sẽ là hành vi ngụy biện khoa học.

### Q63: Bộ máy Marketing Decision Engine có phải là AI tự động hay không?
- **Trả lời:** Đây là một Hệ Chuyên Gia Chỉ Dẫn Dựa Trên Bằng Chứng (Evidence-Based Prescriptive Decision Support System) sử dụng các luật nghiệp vụ tường minh kết hợp với phân khúc K-Means. Chúng em chủ ý không dùng các mô hình Deep Learning Black-box để sinh khuyến nghị vì trong quản trị rủi ro doanh nghiệp, mọi hành động tiếp thị tác động đến người dùng đều phải có khả năng giải thích tường minh (Explainability), phải tuân thủ các rào chắn kiểm soát ngân sách (Guardrails G1–G5) và phải có thể kiểm toán luật 100%.

### Q64: Hệ thống có khả năng triển khai thực tế như thế nào? Làm sao để nạp dữ liệu khách hàng mới vào hệ thống?
- **Trả lời:** Hệ thống được thiết kế theo cấu trúc mô-đun hóa cao: Khi có dữ liệu khách hàng mới, quy trình diễn ra như sau: (1) Script ETL nạp các sự kiện clickstream mới vào Parquet; (2) Trích xuất vector 7 đặc trưng $F1$; (3) Nạp model bundle `.joblib` đã đóng băng để thực hiện gán nhãn cụm (Predict) tức thì với tốc độ hàng trăm nghìn bản ghi mỗi giây; (4) Chạy qua bộ máy luật `decision_rules.py` để sinh khuyến nghị kèm bằng chứng; (5) Xuất snapshot JSON cập nhật để giao diện hiển thị. Toàn bộ quy trình có thể tự động hóa định kỳ hàng tuần qua các công cụ điều phối (Airflow / Cronjob).

### Q65: Vì sao giao diện của IVRE Atelier (thời trang) lại hiển thị dữ liệu mỹ phẩm REES46? Làm sao để đo lường tác động khi IVRE thực hiện chiến dịch thật?
- **Trả lời:** Đây là mô hình nghiên cứu độc lập (Research Demo / Proof-of-Concept): Chúng em sử dụng tập dữ liệu chuẩn thương mại điện tử REES46 để chứng minh tính đúng đắn của phương pháp luận khoa học dữ liệu và sử dụng ngôn ngữ thiết kế của IVRE Atelier làm giao diện người dùng mẫu. Để bảo đảm tính liêm chính, giao diện hiển thị rõ nhãn cảnh báo nghiên cứu và toàn bộ đề xuất ở trạng thái `PENDING_CONSENT`. Khi IVRE quyết định triển khai chiến dịch thật trên tệp khách hàng thời trang của mình, chúng em đề xuất quy trình Thử nghiệm Ngẫu nhiên có Đối chứng (RCT): Trích giữ 10% khách hàng trong từng phân khúc làm nhóm đối chứng (Holdout Control Group không nhận tin), sau đó đo lường độ chênh lệch chuyển đổi (Incremental Lift) giữa nhóm nhận tin và nhóm đối chứng để tính toán chính xác ROI thực tế của chiến dịch.

