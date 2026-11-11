# IVRE Owner Portal — Research Analytics Integration Specification & Data Contract

**Tài liệu kỹ thuật:** Đặc tả tích hợp Phân hệ Phân tích Khách hàng Nghiên cứu (Research Customer Analytics) vào IVRE Owner Portal.  
**Phiên bản hợp đồng:** `v1.0.0`  
**Ngày cập nhật:** 2026-11-10  
**Trạng thái phân hệ:** Standalone Research Demo (`outputs/dashboard/index.html`) $\to$ In-Portal React Route Spec (`/owner/research-analytics`).

---

## 1. Phân Định Ranh Giới: Standalone Dashboard vs. In-Portal Integration

| Tiêu chí | Standalone Research Dashboard (`outputs/dashboard/index.html`) | IVRE In-Portal Integration (`/owner/research-analytics`) |
| :--- | :--- | :--- |
| **Môi trường thực thi** | Trình duyệt độc lập, tải trực tiếp tệp HTML tĩnh hoặc chạy qua local HTTP server | Nằm trong React Router của IVRE Owner Portal, chia sẻ chung Navigation, Auth Context và Theme Provider |
| **Nguồn dữ liệu** | Đọc dữ liệu từ gói snapshot tĩnh `outputs/dashboard/ivre_dashboard_snapshot.json` (32.98 KB) | Tải qua REST API tĩnh `/api/v1/analytics/snapshot` hoặc đọc JSON bundle từ CDN/S3 bucket |
| **Quyền truy cập** | Read-Only Analytical Sandbox cho mục đích nghiên cứu & bảo vệ đồ án | Phân quyền Owner / Chief Marketing Officer (Role-Based Access Control) |
| **Bảo vệ ranh giới** | Không ghi dữ liệu vào database IVRE, không trigger SMS/Email thật | Không chỉnh sửa giỏ hàng, bảng `orders`, hay API thanh toán thực tế của shop thời trang IVRE |
| **Trạng thái nghiệm thu Phase 7** | **PASS** (Đã hoàn thành và xác thực trên Chrome DevTools) | **CONDITIONAL** (Do workspace hiện tại độc lập với codebase React `FashionStore`) |

---

## 2. Kiến Trúc Tích Hợp Đề Xuất (React / Vite / Next.js)

### 2.1. Tùy chọn 1: Thành phần React Thuần (Native React Component — Khuyến nghị)
Tạo route mới trong Owner Layout:
```tsx
// src/pages/owner/ResearchAnalyticsPage.tsx
import React, { useEffect, useState } from 'react';
import { OverviewCards } from '@/components/analytics/OverviewCards';
import { SegmentCards } from '@/components/analytics/SegmentCards';
import { FunnelAnalysis } from '@/components/analytics/FunnelAnalysis';
import { DecisionEngine } from '@/components/analytics/DecisionEngine';
import { HoldoutInsights } from '@/components/analytics/HoldoutInsights';
import snapshotData from '@/assets/data/ivre_dashboard_snapshot.json';

export const ResearchAnalyticsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'segments' | 'funnel' | 'decisions' | 'insights'>('overview');

  return (
    <div className="p-6 bg-slate-50 min-h-screen">
      {/* Research Governance Banner */}
      <div className="bg-amber-50 border border-amber-200 text-amber-800 px-4 py-2 rounded-md mb-6 text-xs flex justify-between">
        <span><strong>Research Demo:</strong> REES46 Historical Research Data (01/10/2019 – 29/02/2020) &bull; Read-only Analytical Sandbox</span>
        <span className="bg-amber-100 text-amber-900 px-2 py-0.5 rounded font-bold">100% PENDING_CONSENT</span>
      </div>

      {/* App Header & Badges */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Customer Intelligence &amp; Decision Support</h1>
        <p className="text-sm text-slate-500">Phân tích hành vi, phân cụm K-Means và gợi ý chiến thuật tiếp thị có thể giải thích.</p>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-200 gap-4 mb-6">
        {/* Tab Buttons */}
      </div>

      {/* Content Panes */}
      {activeTab === 'overview' && <OverviewCards data={snapshotData.customer_overview} />}
      {activeTab === 'segments' && <SegmentCards buyers={snapshotData.buyer_segments} nonBuyers={snapshotData.non_buyer_tiers} />}
      {activeTab === 'funnel' && <FunnelAnalysis funnel={snapshotData.session_funnel} events={snapshotData.clean_event_distribution} />}
      {activeTab === 'decisions' && <DecisionEngine tactics={snapshotData.candidate_tactics} archetypes={snapshotData.archetypes} />}
      {activeTab === 'insights' && <HoldoutInsights holdout={snapshotData.historical_holdout_evaluation} lineage={snapshotData.metadata} />}
    </div>
  );
};
```

### 2.2. Tùy chọn 2: Nhúng Sandboxed Iframe (Zero-Maintenance Iframe)
Nếu nhóm kỹ thuật IVRE muốn nhúng ngay mà không cần viết lại toàn bộ CSS/JS:
```tsx
export const AnalyticsIframeContainer: React.FC = () => {
  return (
    <div className="w-full h-screen overflow-hidden">
      <iframe
        src="/static/analytics/index.html"
        title="IVRE Research Analytics Dashboard"
        className="w-full h-full border-none"
        sandbox="allow-scripts allow-same-origin"
      />
    </div>
  );
};
```

---

## 3. Data Contract: Lược Đồ Snapshot JSON (`ivre_dashboard_snapshot.json`)

Mọi thông tin hiển thị trên giao diện đều được trích xuất từ tệp JSON duy nhất hoặc 5 tệp thành phần tương ứng:

```typescript
export interface DashboardSnapshot {
  metadata: {
    project_name: string;             // "Customer Analytics & Marketing Decision Support"
    dataset: string;                  // "REES46 eCommerce Events 2019-2020"
    observation_cutoff: string;       // "2020-02-01T00:00:00Z"
    model_version: string;            // "v1.0.0-f1-std-k4"
    ruleset_version: string;          // "v1.0.0"
    sha256_checksum: string;          // Mã băm kiểm toán
    disclaimer: string;               // Thông báo giới hạn nghiên cứu
  };

  customer_overview: {
    total_customers_observed: number; // 1,341,499
    buyers_count: number;             // 92,652 (6.91%)
    non_buyers_count: number;         // 1,248,847 (93.09%)
    total_observed_revenue: number;   // 5,140,880.08
    median_spend_per_buyer: number;   // 33.17
    total_purchase_sessions: number;  // 126,503
    data_quality_valid_pct: number;   // 100.0
  };

  buyer_segments: Array<{
    cluster_id: number;               // 0, 1, 2, 3
    name_en: string;
    name_vi: string;
    description: string;
    n_customers: number;
    pct_of_buyers: number;
    median_recency_days: number;
    median_frequency: number;
    median_monetary: number;
    median_sessions_30d: number;
    color_hex: string;
  }>;

  non_buyer_tiers: Array<{
    tier_id: string;                  // HIGH_INTENT, EXPLORING, LOW_ENGAGEMENT, INACTIVE
    name_en: string;
    name_vi: string;
    n_customers: number;
    pct_of_non_buyers: number;
    condition_summary: string;
  }>;

  session_funnel: {
    total_sessions_observed: number;  // 2,873,439
    cart_sessions: number;            // 983,165 (34.21%)
    purchase_sessions: number;        // 126,503 (4.40%)
    cart_session_no_purchase_rate_pct: number; // 87.13%
  };

  candidate_tactics: Array<{
    tactic_id: string;                // TAC_LOYALTY_VIP, TAC_CART_RECOVERY, etc.
    name_en: string;
    name_vi: string;
    allocated_customers: number;
    pct_of_population: number;
    target_goal: string;
    evaluation_kpi: string;
    consent_status: "PENDING_CONSENT";
  }>;

  archetypes: Array<{
    id: string;                       // ARC-01 to ARC-08
    title: string;
    cohort: "BUYER" | "NON_BUYER";
    segment: string;
    goal: string;
    tactic: string;
    behavior: Record<string, string>;
    guardrails: string[];
    reason: string;
    evidence: string;
    kpi: string;
    status: "PENDING_CONSENT";
  }>;

  historical_holdout_evaluation: {
    holdout_event_count: number;      // 3,916,392
    holdout_window: string;           // "2020-02-01 to 2020-02-29"
    holdout_evaluation_metrics: Array<{
      cluster_id: number;
      cluster_name: string;
      future_purchase_rate_pct: number;
      wilson_95_ci_lower_pct: number;
      wilson_95_ci_upper_pct: number;
      future_spend_per_customer: number;
    }>;
    non_buyers_benchmark: {
      future_purchase_rate_pct: number;
      future_spend_per_customer: number;
    };
  };
}
```

---

## 4. Quy Chuẩn An Toàn & Bảo Mật Tiếp Thị (Safety & Governance)

1. **Không thực thi tự động (Zero Automated Dispatch):** Toàn bộ đề xuất tiếp thị từ Decision Engine phải giữ nguyên cờ `PENDING_CONSENT`. Tuyệt đối không bổ sung các nút bấm "Gửi email hàng loạt", "Kích hoạt khuyến mãi", hoặc "Export số điện thoại" vào giao diện.
2. **Loại bỏ PII (Zero Raw PII Exposure):** Không đưa `user_id` thật, email, IP, hoặc mã thiết bị vào các bảng dữ liệu của snapshot. Mọi hiển thị khách hàng chỉ dùng mã Archetype ẩn danh (`ARC-01` $\to$ `ARC-08`).
3. **Phân định rõ nghiên cứu (Clear Research Demarcation):** Mọi view đều phải hiển thị biểu ngữ `REES46 Historical Research Demo (2019–2020)`. Không gây hiểu lầm cho ban lãnh đạo IVRE rằng đây là số liệu của khách mua thời trang trực tiếp.

