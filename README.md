# Customer Intelligence & Marketing Decision Support System
## Phân Tích & Phân Khúc Khách Hàng Bằng Dữ Liệu Lớn Clickstream Trong Thương Mại Điện Tử (REES46)

[![Unit Tests](https://img.shields.io/badge/Unit%20Tests-81%2F81%20PASS-success)](file:///d:/Lap%20trinh/customer-analytics-antigravity/tests)
[![Phase Gates](https://img.shields.io/badge/CRISP--DM%20Gates-8%2F8%20PASS-blue)](file:///d:/Lap%20trinh/customer-analytics-antigravity/PROJECT_STATUS.md)
[![Dataset](https://img.shields.io/badge/Dataset-REES46%20Cosmetics-orange)](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop)
[![Engine](https://img.shields.io/badge/Engine-DuckDB%20%2B%20Parquet-green)](https://duckdb.org/)
[![UI](https://img.shields.io/badge/Dashboard-Clean%20Minimalist%20Analytics-purple)](file:///d:/Lap%20trinh/customer-analytics-antigravity/outputs/dashboard/index.html)

Đồ án môn học: **Phân tích Dữ liệu / Khoa học Dữ liệu Ứng dụng (Applied Data Science / Customer Analytics)**  
Quy trình thực hiện: Chuẩn mực **CRISP-DM (Cross-Industry Standard Process for Data Mining)** xuyên suốt 8 Phase (P0 – P8).

---

## 1. Tổng Quan Dự Án & Bộ Dữ Liệu Nghiên Cứu

Hệ thống giải quyết bài toán cốt lõi trong tiếp thị số TMĐT: **Làm thế nào để phân khúc khách hàng chính xác, phát hiện nguy cơ rời bỏ, nhận diện khách hàng VIP và đưa ra các đề xuất marketing có trách nhiệm nhằm bảo vệ ngân sách, tránh gửi khuyến mãi đại trà?**

- **Tập dữ liệu chính thức:** [REES46 eCommerce Events in Cosmetics Shop](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop) (10/2019 – 02/2020).
- **Quy mô phân tích:** **20.692.840** sự kiện thô $\rightarrow$ **19.583.742** sự kiện sạch sau khử trùng lặp.
- **Dân số khách hàng:** **1.341.499** khách hàng duy nhất (gồm **92.652** Buyers và **1.248.847** Non-Buyers).
- **Ranh giới thời gian (Temporal Split) chống rò rỉ dữ liệu (Anti-Leakage):**
  - *Observation Window* (01/10/2019 – 01/02/2020): Dùng để trích xuất đặc trưng và huấn luyện K-Means.
  - *Holdout Window* (01/02/2020 – 01/03/2020): **3.916.392** sự kiện được niêm phong để hậu kiểm hành vi mua sắm tương lai.

---

## 2. Phân Công Trách Nhiệm Nhóm 2 Người (Team Collaboration Model)

| Trụ cột chuyên môn | Thành viên A (Data Analyst & Research Lead) | Thành viên B (ML Engineer & System Lead) |
| :--- | :--- | :--- |
| **Phạm vi chính** | Dữ liệu, cơ sở nghiên cứu, EDA, Feature Engineering, kiểm chứng hành vi Holdout. | Phân cụm K-Means, độ ổn định mô hình, cây đại diện (Surrogate), Decision Engine và Dashboard. |
| **Tệp phụ trách chính**| `configs/kpi_dictionary.yaml`<br>`scripts/phase2_etl.py`<br>`scripts/phase3_feature_engineering.py`<br>`scripts/phase5_evaluation.py`<br>`reports/DATA_ANALYTICS_REPORT.md` (Chương 1–6, 8) | `scripts/phase4_clustering.py`<br>`src/decision_engine/rules.py`<br>`scripts/phase6_decision_support.py`<br>`outputs/dashboard/index.html`<br>`reports/DATA_ANALYTICS_REPORT.md` (Chương 7, 9–12) |
| **Nguyên tắc nghiệm thu**| Không tự nghiệm thu phần mình; thành viên còn lại phải chạy lại code, kiểm tra tính đúng đắn và đặt câu hỏi phản biện chéo trước khi đóng cổng. |

---

## 3. Cấu Trúc Thư Mục Hệ Thống (Architecture & File Map)

```text
customer-analytics-antigravity/
├── configs/
│   ├── project.yaml                 # Cấu hình cutoff, đường dẫn, engine và random seeds
│   └── kpi_dictionary.yaml          # Định nghĩa ngữ nghĩa toán học 16 chỉ số KPI
├── data/
│   ├── raw/                         # 5 CSVs REES46 (2.32 GB - không đẩy lên Git)
│   ├── cleaned/                     # Parquet sự kiện sạch (471 MB - sinh ra từ phase2_etl.py)
│   └── features/                    # Bảng đặc trưng RFM & Engagement 1.34M khách (tracked)
├── docs/
│   └── IVRE_INTEGRATION_SPEC.md     # Đặc tả tích hợp React Component & Iframe Sandbox
├── outputs/
│   ├── dashboard/
│   │   ├── index.html               # Clean Minimalist Light Analytics Dashboard (Standalone)
│   │   ├── ivre_dashboard_snapshot.json # Master data snapshot tĩnh
│   │   └── snapshot_manifest.json   # Checksum băm SHA-256 đối soát toàn vẹn
│   ├── experiments/                 # Hồ sơ đo kiểm tốc độ, profiling, độ ổn định ARI
│   ├── figures/                     # 20 biểu đồ nghiên cứu và ảnh chụp màn hình responsive
│   ├── models/                      # Model K-Means (kmeans_best_model.joblib) & Surrogate Tree
│   └── recommendations/             # 1.34M khuyến nghị tiếp thị (Parquet)
├── reports/
│   ├── DATA_ANALYTICS_REPORT.md     # Báo cáo học thuật chính 12 chương (Data Report)
│   └── TECHNICAL_LEARNING_NOTES.md  # Sổ tay công thức 9 phần kèm 65 câu hỏi vấn đáp
├── scripts/                         # 8 Scripts thực thi tương ứng từng Phase (phase1 -> phase7)
├── src/
│   ├── contracts/                   # Hợp đồng KPI và logic kiểm chứng
│   └── decision_engine/             # Bộ máy sinh quyết định marketing & 5 Guardrails
├── tests/                           # 81 Unit Tests tự động kiểm thử toàn trình
├── AGENTS.md                        # Quy tắc bất biến và cam kết liêm chính khoa học
├── PROJECT_PLAN.md                  # Kế hoạch chi tiết và tiêu chí nghiệm thu
├── PROJECT_STATUS.md                # Bằng chứng thực nghiệm, nhật ký lệnh và trạng thái Phase Gates
├── requirements.txt                 # Danh sách thư viện Python
└── requirements-lock.txt            # Khóa phiên bản chuẩn (DuckDB 2.0.0, Scikit-learn 1.9.1, ...)
```

---

## 4. Hướng Dẫn Cài Đặt & Chạy Thử Nghiệm

### 4.1. Thiết lập môi trường Python
```powershell
# Tạo và kích hoạt môi trường ảo
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Cài đặt thư viện theo phiên bản đã khóa
pip install -r requirements-lock.txt
```

### 4.2. Chạy Kiểm Thử Đơn Vị & Nghiệm Thu (Ngay sau khi clone)
Toàn bộ bảng đặc trưng (`data/features/`), mô hình (`outputs/models/`) và snapshot (`outputs/dashboard/`) đã được theo dõi trong kho lưu trữ, do đó bạn có thể chạy kiểm thử ngay lập tức:

```powershell
# Chạy toàn bộ 81 bài Unit Tests (thời gian ~1.9s)
python -m unittest discover -s tests -v

# Chạy xác thực 8 cổng Phase Gates từ P0 đến P7
python scripts/validate_phase0.py
python scripts/validate_phase1.py
python scripts/validate_phase2.py
python scripts/validate_phase3.py
python scripts/validate_phase4.py
python scripts/validate_phase5.py
python scripts/validate_phase6.py
python scripts/validate_phase7.py
```

### 4.3. Tái lập Toàn bộ Pipeline từ Dữ liệu Thô (Tùy chọn)
Nếu muốn chạy lại từ file CSV thô REES46 ban đầu:
1. Tải 5 tệp CSV từ [Kaggle](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop) và đặt vào `data/raw/` (`2019-Oct.csv` đến `2020-Feb.csv`).
2. Chạy chuỗi pipeline tuần tự:
```powershell
python scripts/phase1_profiling.py          # Khám phá & profile dữ liệu (78s)
python scripts/phase2_etl.py                # Làm sạch & chuyển Parquet (212s)
python scripts/phase3_feature_engineering.py # Xây dựng bảng đặc trưng (11s)
python scripts/phase4_clustering.py          # Huấn luyện K-Means K=4 (131s)
python scripts/phase5_evaluation.py          # Hậu kiểm ngoài mẫu Feb 2020 (26s)
python scripts/phase6_decision_support.py    # Sinh 1.34M khuyến nghị (4.5s)
python scripts/build_phase7_snapshot.py      # Đóng gói master snapshot JSON (0.2s)
```

### 4.4. Mở Giao diện Bảng Điều Khiển (Research Dashboard)
Mở trực tiếp tệp [`outputs/dashboard/index.html`](outputs/dashboard/index.html) bằng trình duyệt web:
- Giao diện độc lập (Standalone HTML/CSS/JS thuần, không cần server).
- Đạt chuẩn Clean Minimalist Analytics, tải trang siêu tốc ($FCP = 256\text{ ms}$).
- Tương thích 100% không cuộn ngang trên cả Desktop 1440px, Tablet 768px, Mobile 390px và 320px (touch targets $\ge 44\text{px}$).

---

## 5. Kết Quả Nghiên Cứu Cốt Lõi (Core Findings)

### 5.1. Bốn Phân Khúc Người Mua (Buyers - 92.652 khách hàng)
| Phân khúc | Tên gọi | Tỷ trọng | Recency (Median) | Frequency (Median) | Monetary (Median) | Tương tác 30d (Median) | Tỷ lệ mua Holdout T2 (Wilson 95% CI) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **C0** | Khách Mua 1 Lần Ngủ Đông | 45,49% | 82,3 ngày | 1 phiên | \$20,24 | 0 phiên (0 views) | **2,66%** [2,51% – 2,81%] |
| **C1** | Khách VIP Trung Thành Cốt Lõi | 9,45% | 12,7 ngày | 3 phiên | \$117,69 | 9 phiên (29 views) | **35,02%** [34,02% – 36,03%] |
| **C2** | Khách Chi Tiêu Khá Đang Rời Bỏ | 20,08% | 54,3 ngày | 1 phiên | \$67,29 | 0 phiên (0 views) | **7,32%** [6,96% – 7,71%] |
| **C3** | Khách Mua Gần & Đang Duyệt Xem | 24,98% | 16,3 ngày | 1 phiên | \$28,12 | 3 phiên (8 views) | **10,13%** [9,75% – 10,52%] |

### 5.2. Bốn Tầng Tương Tác Người Chưa Mua (Non-Buyers - 1.248.847 khách hàng)
- **`INACTIVE`** ($886.075$ khách - $70,95\%$): Không có phiên truy cập nào trong 30 ngày $\rightarrow$ Gán chiến thuật `TAC_NO_ACTION` nhằm bảo toàn ngân sách.
- **`LOW_ENGAGEMENT`** ($246.717$ khách - $19,76\%$): Có $\ge 1$ phiên nhưng $< 5$ lượt xem $\rightarrow$ Gán `TAC_LOW_COST_NURTURE` (kênh 0đ push app/banner).
- **`EXPLORING`** ($81.994$ khách - $6,57\%$): Duyệt xem tích cực $\ge 2$ phiên hoặc $\ge 5$ views $\rightarrow$ Gán `TAC_PRODUCT_EDU` (cẩm nang làm đẹp).
- **`HIGH_INTENT`** ($34.061$ khách - $2,73\%$): Có hành vi thêm giỏ hàng gần đây $\rightarrow$ Gán `TAC_CART_RECOVERY` (hỗ trợ chuyển đổi đơn đầu tiên).

---

## 6. Cam Kết Liêm Chính Khoa Học (Academic Integrity)

1. **Proxy Phiên Mua Hàng:** REES46 không có mã `order_id`; chỉ số Frequency được định nghĩa chặt chẽ là *số phiên mua hàng duy nhất (distinct purchase sessions proxy)*, không đánh đồng mỗi purchase event là một đơn hàng.
2. **Không Rò Rỉ Dữ Liệu (Zero Data Leakage):** Mọi đặc trưng phân cụm và quy tắc tiếp thị đều được tính toán nghiêm ngặt trước mốc cắt $T_{\text{cutoff}} = \text{01/02/2020}$. Dữ liệu tháng 2/2020 chỉ dùng một lần duy nhất để hậu kiểm ngoài mẫu.
3. **Phân Định Rõ Thuật Ngữ:**
   - Tỷ lệ quay lại mua trong tháng 2 phản ánh **quán tính hành vi tự nhiên (Natural Behavioral Momentum)**, được gọi chuẩn xác là *Tỷ số Tỷ lệ Mua Quan sát được (Observed Purchase Ratio)*, tuyệt đối không suy diễn thành *Causal Marketing Uplift* khi không có thử nghiệm đối chứng A/B.
   - Kịch bản tiết kiệm chi phí được ghi rõ là **Mô phỏng Giả định (Hypothetical Cost Avoidance Simulation)**, không phải lợi nhuận thực tế.
4. **Bảo Vệ Quyền Riêng Tư (Privacy Guardrails):** $100\%$ trong số $1.341.499$ khuyến nghị đều được gán cờ `PENDING_CONSENT`, hệ thống không có API tự động kích hoạt gửi chiến dịch ngoài đời thực khi chưa có sự đồng ý hợp pháp của khách hàng.

---

## 7. Tài Liệu Nghiên Cứu Chi Tiết
- [Báo cáo Học thuật Toàn diện 12 Chương](reports/DATA_ANALYTICS_REPORT.md)
- [Sổ tay Kỹ thuật 9 Phần & 65 Câu Hỏi Vấn Đáp Bảo Vệ](reports/TECHNICAL_LEARNING_NOTES.md)
- [Bằng chứng Nghiệm thu Phase Gates & Nhật ký Lệnh](PROJECT_STATUS.md)
- [Đặc tả Tích hợp IVRE Owner Portal](docs/IVRE_INTEGRATION_SPEC.md)

---
*Customer Intelligence & Marketing Decision Support Project — Ready for Academic Defense.*
