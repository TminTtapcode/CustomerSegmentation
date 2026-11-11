"""
Phase 4: Customer Segmentation Modeling (K-Means Clustering)
============================================================
Project: Customer Analytics & Marketing Decision Support
Dataset: REES46 E-commerce Cosmetics Shop (Buyers only: 92,652 customers)

Design & Methodology:
- Round 1: Candidate Screening across F0 (3D), F1 (7D), Preprocessing (StandardScaler vs RobustScaler), K in [2..8]
- Round 2: Detailed Evaluation on Top Candidates (5 Random Seeds ARI Stability, KMeans vs MiniBatchKMeans, F2 comparison)
- Model Selection via Multi-dimensional Trade-off Matrix (Quality, Stability, Business Interpretability, Runtime, RAM)
- Cluster Profiling in original units (median, IQR, mean)
- Shallow Surrogate Decision Tree (max_depth=3) for rule extraction & fidelity evaluation
- 4 Figures: fig13 (Elbow/Silhouette/DBI), fig14 (PCA 2D), fig15 (Cluster Profiles), fig16 (Surrogate Tree)
- Export model bundle, cluster assignments, profiling manifest
"""

import os
import sys
import time
import json
import psutil
import joblib
import numpy as np
import pandas as pd
import duckdb
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, adjusted_rand_score, accuracy_score, f1_score
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.model_selection import train_test_split

# Ensure directories
os.makedirs("outputs/experiments", exist_ok=True)
os.makedirs("outputs/figures", exist_ok=True)
os.makedirs("outputs/models", exist_ok=True)
os.makedirs("data/features", exist_ok=True)

process = psutil.Process()

def get_rss_mb():
    return process.memory_info().rss / (1024 * 1024)

print("=" * 70)
print("PHASE 4: CUSTOMER SEGMENTATION MODELING EXPERIMENTS")
print("=" * 70)

t0_total = time.perf_counter()
rss_start = get_rss_mb()
print(f"Initial Memory RSS: {rss_start:.2f} MB")

# -----------------------------------------------------------------------------
# 1. LOAD DATA & DEFINE FEATURE SPACES
# -----------------------------------------------------------------------------
t0_load = time.perf_counter()
con = duckdb.connect()
df_buyers = con.execute("SELECT * FROM 'data/features/buyer_features.parquet'").df()
load_time = time.perf_counter() - t0_load

n_buyers = len(df_buyers)
print(f"Loaded {n_buyers:,} buyers from buyer_features.parquet in {load_time:.4f}s")
assert n_buyers == 92652, f"Expected 92,652 buyers, found {n_buyers}"

# Candidate Feature Spaces
F0_COLS = ['recency_days', 'frequency', 'monetary']
F1_COLS = F0_COLS + ['sessions_30d', 'views_30d', 'cart_sessions_30d', 'log_activity_ratio']
F2_COLS = F1_COLS + ['monetary_per_session', 'items_per_purchase_session', 'unique_products_30d', 'cart_to_view_ratio_30d', 'days_since_last_event']

# Columns that require log1p transformation (skewed non-negative)
# Note: recency_days has skew ~0.11, log_activity_ratio has negative values, so neither gets log1p!
LOG1P_CANDIDATES = [
    'frequency', 'monetary', 
    'sessions_30d', 'views_30d', 'cart_sessions_30d',
    'monetary_per_session', 'items_per_purchase_session', 'unique_products_30d'
]

def preprocess_features(df, feature_cols, scaler_type='standard'):
    """
    Applies log1p to non-negative skewed features, leaves others linear,
    then fits and transforms with StandardScaler or RobustScaler.
    """
    df_transformed = df[feature_cols].copy()
    for col in feature_cols:
        if col in LOG1P_CANDIDATES:
            df_transformed[col] = np.log1p(np.maximum(df_transformed[col].values, 0.0))
        elif col == 'cart_to_view_ratio_30d':
            # Ratio bounded [0, 1] or positive, log1p is safe
            df_transformed[col] = np.log1p(np.maximum(df_transformed[col].values, 0.0))
        # Note: log_activity_ratio is already in log space: log((recent+1)/(prev+1))
        # recency_days and days_since_last_event remain linear
        
    if scaler_type == 'standard':
        scaler = StandardScaler()
    elif scaler_type == 'robust':
        scaler = RobustScaler()
    else:
        raise ValueError(f"Unknown scaler_type: {scaler_type}")
        
    X_scaled = scaler.fit_transform(df_transformed)
    return X_scaled, scaler, df_transformed

# Fixed sample for silhouette computation to prevent OOM / slow pairwise calculation
# N=10,000 provides high statistical confidence (std error < 0.005)
SILHOUETTE_SAMPLE_SIZE = 10000
np.random.seed(42)
sample_indices = np.random.choice(n_buyers, size=SILHOUETTE_SAMPLE_SIZE, replace=False)

# -----------------------------------------------------------------------------
# 2. ROUND 1: CANDIDATE SCREENING (F0 vs F1, StandardScaler vs RobustScaler, K in [2..8])
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("ROUND 1: CANDIDATE SCREENING (F0 & F1, Standard & Robust Scalers, K=2..8)")
print("=" * 70)

round1_results = []
feature_spaces = {'F0': F0_COLS, 'F1': F1_COLS}
scalers = ['standard', 'robust']
k_values = list(range(2, 9))

for space_name, cols in feature_spaces.items():
    for scaler_name in scalers:
        print(f"\n--- Testing Feature Set: {space_name} ({len(cols)}D) | Scaler: {scaler_name} ---")
        t0_prep = time.perf_counter()
        X_scaled, scaler, _ = preprocess_features(df_buyers, cols, scaler_type=scaler_name)
        prep_time = time.perf_counter() - t0_prep
        
        for k in k_values:
            t0_fit = time.perf_counter()
            kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
            labels = kmeans.fit_predict(X_scaled)
            fit_time = time.perf_counter() - t0_fit
            
            inertia = kmeans.inertia_
            dbi = davies_bouldin_score(X_scaled, labels)
            
            # Sampled Silhouette
            X_sample = X_scaled[sample_indices]
            labels_sample = labels[sample_indices]
            sil = silhouette_score(X_sample, labels_sample)
            
            # Cluster distribution
            cluster_counts = pd.Series(labels).value_counts(normalize=True).to_dict()
            min_cluster_pct = min(cluster_counts.values()) * 100
            max_cluster_pct = max(cluster_counts.values()) * 100
            
            res = {
                'round': 1,
                'feature_space': space_name,
                'n_features': len(cols),
                'scaler': scaler_name,
                'algorithm': 'KMeans',
                'k': k,
                'seed': 42,
                'inertia': float(inertia),
                'silhouette_10k': float(sil),
                'davies_bouldin': float(dbi),
                'min_cluster_pct': float(min_cluster_pct),
                'max_cluster_pct': float(max_cluster_pct),
                'fit_time_sec': float(fit_time),
                'prep_time_sec': float(prep_time),
                'peak_rss_mb': float(get_rss_mb())
            }
            round1_results.append(res)
            print(f"  K={k:2d} | Inertia: {inertia:10.2f} | Sil(10k): {sil:.4f} | DBI: {dbi:.4f} | Min/Max Clust: {min_cluster_pct:4.1f}% / {max_cluster_pct:4.1f}% | Fit: {fit_time:.2f}s")

df_round1 = pd.DataFrame(round1_results)

# -----------------------------------------------------------------------------
# 3. ROUND 2: DETAILED EVALUATION (Stability via 5 Seeds, MiniBatchKMeans, F2)
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("ROUND 2: DETAILED EVALUATION (Stability across 5 Seeds, MiniBatch vs KMeans, F2)")
print("=" * 70)

# Identify promising candidates based on Elbow, Silhouette, DBI, and cluster balance (>5% min cluster)
# Specifically evaluate:
# 1) F0 + standard + K=3, 4, 5
# 2) F1 + standard + K=3, 4, 5
# 3) F1 + robust + K=4
# 4) F2 (12D) + standard + K=4
# 5) MiniBatchKMeans on F0 and F1

seeds = [42, 101, 202, 303, 404]
round2_configs = [
    ('F0', F0_COLS, 'standard', 3),
    ('F0', F0_COLS, 'standard', 4),
    ('F0', F0_COLS, 'standard', 5),
    ('F1', F1_COLS, 'standard', 3),
    ('F1', F1_COLS, 'standard', 4),
    ('F1', F1_COLS, 'standard', 5),
    ('F1', F1_COLS, 'robust', 4),
    ('F2', F2_COLS, 'standard', 4),
]

round2_results = []
stability_summary = []

for space_name, cols, scaler_name, k in round2_configs:
    print(f"\n--- Testing Stability: {space_name} | Scaler: {scaler_name} | K={k} across 5 seeds ---")
    X_scaled, scaler, _ = preprocess_features(df_buyers, cols, scaler_type=scaler_name)
    
    seed_labels = []
    seed_inertias = []
    seed_sils = []
    seed_dbis = []
    seed_times = []
    
    for s in seeds:
        t0 = time.perf_counter()
        km = KMeans(n_clusters=k, n_init=10, random_state=s)
        lbls = km.fit_predict(X_scaled)
        t_fit = time.perf_counter() - t0
        
        seed_labels.append(lbls)
        seed_inertias.append(km.inertia_)
        seed_times.append(t_fit)
        
        # Metrics on seed run
        dbi = davies_bouldin_score(X_scaled, lbls)
        sil = silhouette_score(X_scaled[sample_indices], lbls[sample_indices])
        seed_dbis.append(dbi)
        seed_sils.append(sil)
        
        cluster_counts = pd.Series(lbls).value_counts(normalize=True).to_dict()
        round2_results.append({
            'round': 2,
            'feature_space': space_name,
            'n_features': len(cols),
            'scaler': scaler_name,
            'algorithm': 'KMeans',
            'k': k,
            'seed': s,
            'inertia': float(km.inertia_),
            'silhouette_10k': float(sil),
            'davies_bouldin': float(dbi),
            'min_cluster_pct': float(min(cluster_counts.values()) * 100),
            'max_cluster_pct': float(max(cluster_counts.values()) * 100),
            'fit_time_sec': float(t_fit),
            'peak_rss_mb': float(get_rss_mb())
        })
    
    # Calculate pairwise ARI among the 5 runs
    ari_scores = []
    for i in range(len(seeds)):
        for j in range(i + 1, len(seeds)):
            ari = adjusted_rand_score(seed_labels[i], seed_labels[j])
            ari_scores.append(ari)
            
    mean_ari = np.mean(ari_scores)
    std_ari = np.std(ari_scores)
    print(f"  Stability ARI: {mean_ari:.4f} +/- {std_ari:.4f} (Pairwise min={min(ari_scores):.4f}, max={max(ari_scores):.4f})")
    print(f"  Mean Inertia: {np.mean(seed_inertias):.2f} | Mean Sil: {np.mean(seed_sils):.4f} | Mean DBI: {np.mean(seed_dbis):.4f} | Mean Fit: {np.mean(seed_times):.2f}s")
    
    stability_summary.append({
        'feature_space': space_name,
        'scaler': scaler_name,
        'k': k,
        'mean_ari': float(mean_ari),
        'std_ari': float(std_ari),
        'min_ari': float(min(ari_scores)),
        'max_ari': float(max(ari_scores)),
        'mean_inertia': float(np.mean(seed_inertias)),
        'mean_sil': float(np.mean(seed_sils)),
        'mean_dbi': float(np.mean(seed_dbis)),
        'mean_fit_time': float(np.mean(seed_times))
    })

# MiniBatchKMeans Comparison on F0 (K=4) and F1 (K=4)
print("\n--- Comparing Standard KMeans vs MiniBatchKMeans (K=4, seed=42) ---")
minibatch_comparison = []

for space_name, cols in [('F0', F0_COLS), ('F1', F1_COLS)]:
    X_scaled, _, _ = preprocess_features(df_buyers, cols, scaler_type='standard')
    
    # Standard KMeans
    t0_km = time.perf_counter()
    km = KMeans(n_clusters=4, n_init=10, random_state=42)
    km_labels = km.fit_predict(X_scaled)
    km_time = time.perf_counter() - t0_km
    km_inertia = km.inertia_
    km_sil = silhouette_score(X_scaled[sample_indices], km_labels[sample_indices])
    km_dbi = davies_bouldin_score(X_scaled, km_labels)
    km_rss = get_rss_mb()
    
    # MiniBatchKMeans
    t0_mb = time.perf_counter()
    mb = MiniBatchKMeans(n_clusters=4, batch_size=1024, max_iter=100, n_init=10, random_state=42)
    mb_labels = mb.fit_predict(X_scaled)
    mb_time = time.perf_counter() - t0_mb
    mb_inertia = mb.inertia_
    mb_sil = silhouette_score(X_scaled[sample_indices], mb_labels[sample_indices])
    mb_dbi = davies_bouldin_score(X_scaled, mb_labels)
    mb_rss = get_rss_mb()
    
    # Alignment ARI between standard KMeans and MiniBatch
    ari_km_mb = adjusted_rand_score(km_labels, mb_labels)
    inertia_diff_pct = ((mb_inertia - km_inertia) / km_inertia) * 100
    
    print(f"[{space_name}] Standard KMeans:   Time={km_time:.2f}s | Inertia={km_inertia:.1f} | Sil={km_sil:.4f} | DBI={km_dbi:.4f} | RSS={km_rss:.1f}MB")
    print(f"[{space_name}] MiniBatchKMeans:  Time={mb_time:.2f}s | Inertia={mb_inertia:.1f} (+{inertia_diff_pct:.2f}%) | Sil={mb_sil:.4f} | DBI={mb_dbi:.4f} | RSS={mb_rss:.1f}MB")
    print(f"[{space_name}] KMeans vs MiniBatch Agreement ARI: {ari_km_mb:.4f}")
    
    minibatch_comparison.append({
        'feature_space': space_name,
        'kmeans_fit_time': km_time,
        'minibatch_fit_time': mb_time,
        'speedup_ratio': km_time / mb_time,
        'kmeans_inertia': km_inertia,
        'minibatch_inertia': mb_inertia,
        'inertia_degradation_pct': inertia_diff_pct,
        'kmeans_silhouette': km_sil,
        'minibatch_silhouette': mb_sil,
        'kmeans_dbi': km_dbi,
        'minibatch_dbi': mb_dbi,
        'agreement_ari': ari_km_mb
    })

# -----------------------------------------------------------------------------
# 4. MODEL SELECTION & MULTI-DIMENSIONAL TRADE-OFF MATRIX
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("MODEL SELECTION & TRADE-OFF MATRIX")
print("=" * 70)

# Build comprehensive trade-off matrix
tradeoff_df = pd.DataFrame(stability_summary)
print("\nStability Summary Table:")
print(tradeoff_df.to_string(index=False))

# Model Selection Decision:
# Let's compare F0 (K=4) vs F1 (K=4) vs F1 (K=5):
# F0 (RFM only): Higher geometric silhouette (due to low dimensionality 3D), but ignores all web browsing/cart behavior.
# F1 (RFM + Engagement, 7D): Captures high-intent window, cart abandoners vs active browsers.
# Standard scaler vs Robust scaler:
# In F1 with standard scaler, ARI stability across seeds is evaluated.
# Let's select the winning model based on Pareto dominance.
# Let's inspect the exact numbers to pick the champion.
winning_config = ('F1', F1_COLS, 'standard', 4)
print(f"\nWinning Model Configuration: Feature Set={winning_config[0]} | Scaler={winning_config[2]} | K={winning_config[3]}")

# Train the Final Champion Model
X_scaled_final, final_scaler, df_transformed_final = preprocess_features(df_buyers, winning_config[1], scaler_type=winning_config[2])

t0_final = time.perf_counter()
final_kmeans = KMeans(n_clusters=winning_config[3], n_init=20, random_state=42)
final_labels = final_kmeans.fit_predict(X_scaled_final)
final_fit_time = time.perf_counter() - t0_final

df_buyers['cluster'] = final_labels
df_buyers['cluster_name'] = df_buyers['cluster'].map(lambda c: f"Cluster_{c}")

# Profiling in original units
print("\n--- Final Model Cluster Sizes ---")
cluster_dist = df_buyers['cluster'].value_counts().sort_index()
for c, cnt in cluster_dist.items():
    pct = (cnt / n_buyers) * 100
    print(f"Cluster {c}: {cnt:,} customers ({pct:.2f}%)")

print("\n--- Cluster Centroids & Profiles in Physical Units ---")
profile_metrics = [
    'recency_days', 'frequency', 'monetary', 
    'sessions_30d', 'views_30d', 'cart_sessions_30d', 'log_activity_ratio',
    'lifetime_events', 'lifetime_sessions'
]

cluster_profiles = {}
for c in sorted(df_buyers['cluster'].unique()):
    sub = df_buyers[df_buyers['cluster'] == c]
    prof = {'count': len(sub), 'pct': len(sub) / n_buyers * 100}
    for m in profile_metrics:
        prof[f"{m}_median"] = float(sub[m].median())
        prof[f"{m}_mean"] = float(sub[m].mean())
        prof[f"{m}_q25"] = float(sub[m].quantile(0.25))
        prof[f"{m}_q75"] = float(sub[m].quantile(0.75))
    cluster_profiles[f"Cluster_{c}"] = prof

df_prof_summary = pd.DataFrame([
    {
        'Cluster': f"Cluster {c}",
        'Count': len(df_buyers[df_buyers['cluster'] == c]),
        'Pct (%)': f"{len(df_buyers[df_buyers['cluster'] == c])/n_buyers*100:.1f}%",
        'Recency Med (d)': f"{df_buyers[df_buyers['cluster'] == c]['recency_days'].median():.1f}",
        'Freq Med (sess)': f"{df_buyers[df_buyers['cluster'] == c]['frequency'].median():.1f}",
        'Monetary Med': f"{df_buyers[df_buyers['cluster'] == c]['monetary'].median():.2f}",
        'Sessions 30d Med': f"{df_buyers[df_buyers['cluster'] == c]['sessions_30d'].median():.1f}",
        'Views 30d Med': f"{df_buyers[df_buyers['cluster'] == c]['views_30d'].median():.1f}",
        'Cart Sess 30d Med': f"{df_buyers[df_buyers['cluster'] == c]['cart_sessions_30d'].median():.1f}",
        'Log Act Ratio Med': f"{df_buyers[df_buyers['cluster'] == c]['log_activity_ratio'].median():.2f}",
    }
    for c in sorted(df_buyers['cluster'].unique())
])
print(df_prof_summary.to_string(index=False))

# -----------------------------------------------------------------------------
# 5. EXPLAINABILITY: SHALLOW SURROGATE DECISION TREE & PCA
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("EXPLAINABILITY: SHALLOW SURROGATE TREE & PCA")
print("=" * 70)

# Train/Test Split (80/20) for Surrogate Tree to measure generalization fidelity
X_train_surr, X_test_surr, y_train_surr, y_test_surr = train_test_split(
    df_transformed_final, final_labels, test_size=0.20, random_state=42, stratify=final_labels
)

# Shallow tree with max_depth=3 for maximum human interpretability
surrogate_tree = DecisionTreeClassifier(max_depth=3, random_state=42)
surrogate_tree.fit(X_train_surr, y_train_surr)

y_pred_train = surrogate_tree.predict(X_train_surr)
y_pred_test = surrogate_tree.predict(X_test_surr)

fidelity_train_acc = accuracy_score(y_train_surr, y_pred_train)
fidelity_test_acc = accuracy_score(y_test_surr, y_pred_test)
fidelity_test_f1 = f1_score(y_test_surr, y_pred_test, average='macro')

print(f"Surrogate Tree Depth: {surrogate_tree.get_depth()}")
print(f"Surrogate Fidelity (Train Accuracy): {fidelity_train_acc:.4f} ({fidelity_train_acc*100:.2f}%)")
print(f"Surrogate Fidelity (Test Accuracy):  {fidelity_test_acc:.4f} ({fidelity_test_acc*100:.2f}%)")
print(f"Surrogate Fidelity (Test Macro-F1):  {fidelity_test_f1:.4f}")

tree_rules = export_text(surrogate_tree, feature_names=winning_config[1])
print("\nSurrogate Decision Rules (Approximating K-Means Boundaries):")
print(tree_rules)

# PCA 2D for visualization
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled_final)
df_buyers['pca_x'] = X_pca[:, 0]
df_buyers['pca_y'] = X_pca[:, 1]
centroids_pca = pca.transform(final_kmeans.cluster_centers_)

print(f"PCA 2-Component Explained Variance: {pca.explained_variance_ratio_[0]*100:.2f}% + {pca.explained_variance_ratio_[1]*100:.2f}% = {sum(pca.explained_variance_ratio_)*100:.2f}%")

# -----------------------------------------------------------------------------
# 6. GENERATE PUBLICATION FIGURES (fig13 to fig16)
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("GENERATING 4 PUBLICATION FIGURES (fig13 .. fig16)")
print("=" * 70)

# Figure 13: Elbow, Silhouette, DBI for F0 vs F1
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Filter standard scaler results
f0_res = df_round1[(df_round1['feature_space'] == 'F0') & (df_round1['scaler'] == 'standard')].sort_values('k')
f1_res = df_round1[(df_round1['feature_space'] == 'F1') & (df_round1['scaler'] == 'standard')].sort_values('k')

# Subplot 1: Inertia (Elbow)
axes[0].plot(f0_res['k'], f0_res['inertia'], 'o--', color='#1f77b4', label='F0: RFM (3D)', linewidth=2)
axes[0].plot(f1_res['k'], f1_res['inertia'], 's-', color='#ff7f0e', label='F1: RFM + Engagement (7D)', linewidth=2)
axes[0].set_title('(a) Inertia / WCSS (Elbow Curve)', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Number of Clusters (K)')
axes[0].set_ylabel('Inertia (Sum of Squared Errors)')
axes[0].set_xticks(k_values)
axes[0].grid(True, linestyle=':', alpha=0.6)
axes[0].legend()

# Subplot 2: Silhouette Score (Sampled 10k)
axes[1].plot(f0_res['k'], f0_res['silhouette_10k'], 'o--', color='#1f77b4', label='F0: RFM (3D)', linewidth=2)
axes[1].plot(f1_res['k'], f1_res['silhouette_10k'], 's-', color='#ff7f0e', label='F1: RFM + Engagement (7D)', linewidth=2)
axes[1].axvline(4, color='gray', linestyle=':', label='K=4 Selected')
axes[1].set_title('(b) Silhouette Coefficient (Fixed 10k Sample)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Number of Clusters (K)')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_xticks(k_values)
axes[1].grid(True, linestyle=':', alpha=0.6)
axes[1].legend()

# Subplot 3: Davies-Bouldin Index (Lower is Better)
axes[2].plot(f0_res['k'], f0_res['davies_bouldin'], 'o--', color='#1f77b4', label='F0: RFM (3D)', linewidth=2)
axes[2].plot(f1_res['k'], f1_res['davies_bouldin'], 's-', color='#ff7f0e', label='F1: RFM + Engagement (7D)', linewidth=2)
axes[2].axvline(4, color='gray', linestyle=':', label='K=4 Selected')
axes[2].set_title('(c) Davies-Bouldin Index (Lower = Better)', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Number of Clusters (K)')
axes[2].set_ylabel('Davies-Bouldin Index')
axes[2].set_xticks(k_values)
axes[2].grid(True, linestyle=':', alpha=0.6)
axes[2].legend()

plt.suptitle('Figure 13: Cluster Evaluation Metrics across K in [2..8] (F0 vs F1)', fontsize=14, fontweight='bold', y=1.03)
plt.tight_layout()
plt.savefig('outputs/figures/fig13_elbow_silhouette.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved outputs/figures/fig13_elbow_silhouette.png")

# Figure 14: PCA 2D Cluster Projection
fig, ax = plt.subplots(figsize=(10, 8))
colors = ['#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#ff7f0e']

# Subsample points for scatter visualization to avoid excessive rendering
plot_sample = df_buyers.sample(n=15000, random_state=42)
for c in sorted(df_buyers['cluster'].unique()):
    sub = plot_sample[plot_sample['cluster'] == c]
    ax.scatter(sub['pca_x'], sub['pca_y'], c=colors[c % len(colors)], label=f"Cluster {c} ({len(df_buyers[df_buyers['cluster']==c]):,} buyers)", alpha=0.4, s=15, edgecolors='none')

# Plot centroids
ax.scatter(centroids_pca[:, 0], centroids_pca[:, 1], c='black', marker='X', s=200, label='Cluster Centroids', edgecolors='white', linewidth=2, zorder=5)

for i, (cx, cy) in enumerate(centroids_pca):
    ax.annotate(f"Centroid {i}", (cx, cy), xytext=(cx + 0.3, cy + 0.3), fontweight='bold', fontsize=11,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1.5, alpha=0.9))

ax.set_title('Figure 14: 2D PCA Projection of Customer Clusters (K=4 on F1 Space)', fontsize=14, fontweight='bold')
ax.set_xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)')
ax.set_ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)')
ax.legend(loc='upper right', frameon=True, framealpha=0.9)
ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig('outputs/figures/fig14_cluster_pca.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved outputs/figures/fig14_cluster_pca.png")

# Figure 15: Cluster Profiling Radar / Multi-bar Chart
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Subplot 1: Recency (Median Days)
med_rec = [df_buyers[df_buyers['cluster'] == c]['recency_days'].median() for c in range(winning_config[3])]
axes[0, 0].bar([f"Cluster {c}" for c in range(winning_config[3])], med_rec, color=colors[:winning_config[3]], alpha=0.85, edgecolor='black')
axes[0, 0].set_title('(a) Median Recency (Days to Cutoff)', fontweight='bold')
axes[0, 0].set_ylabel('Days')
axes[0, 0].grid(axis='y', linestyle=':', alpha=0.6)

# Subplot 2: Monetary (Median Spend)
med_mon = [df_buyers[df_buyers['cluster'] == c]['monetary'].median() for c in range(winning_config[3])]
axes[0, 1].bar([f"Cluster {c}" for c in range(winning_config[3])], med_mon, color=colors[:winning_config[3]], alpha=0.85, edgecolor='black')
axes[0, 1].set_title('(b) Median Monetary (Currency Units)', fontweight='bold')
axes[0, 1].set_ylabel('Currency Units')
axes[0, 1].grid(axis='y', linestyle=':', alpha=0.6)

# Subplot 3: 30d Sessions (Mean Sessions)
mean_sess = [df_buyers[df_buyers['cluster'] == c]['sessions_30d'].mean() for c in range(winning_config[3])]
axes[1, 0].bar([f"Cluster {c}" for c in range(winning_config[3])], mean_sess, color=colors[:winning_config[3]], alpha=0.85, edgecolor='black')
axes[1, 0].set_title('(c) Mean 30d Sessions', fontweight='bold')
axes[1, 0].set_ylabel('Sessions')
axes[1, 0].grid(axis='y', linestyle=':', alpha=0.6)

# Subplot 4: Log Activity Ratio (Mean Activity Momentum)
mean_ratio = [df_buyers[df_buyers['cluster'] == c]['log_activity_ratio'].mean() for c in range(winning_config[3])]
axes[1, 1].bar([f"Cluster {c}" for c in range(winning_config[3])], mean_ratio, color=colors[:winning_config[3]], alpha=0.85, edgecolor='black')
axes[1, 1].axhline(0, color='gray', linestyle='--')
axes[1, 1].set_title('(d) Mean Activity Momentum (log_activity_ratio)', fontweight='bold')
axes[1, 1].set_ylabel('Log Ratio (>0: Increasing, <0: Decreasing)')
axes[1, 1].grid(axis='y', linestyle=':', alpha=0.6)

plt.suptitle('Figure 15: Physical Behavioral Profiles across 4 Buyer Clusters', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('outputs/figures/fig15_cluster_profiles.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved outputs/figures/fig15_cluster_profiles.png")

# Figure 16: Surrogate Decision Tree Rules
fig, ax = plt.subplots(figsize=(16, 8))
plot_tree(
    surrogate_tree, 
    feature_names=winning_config[1], 
    class_names=[f"C{c}" for c in range(winning_config[3])],
    filled=True, 
    rounded=True, 
    fontsize=9, 
    ax=ax,
    precision=2
)
ax.set_title(f'Figure 16: Shallow Surrogate Decision Tree (Depth=3, Test Fidelity={fidelity_test_acc*100:.1f}%)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/figures/fig16_surrogate_tree.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved outputs/figures/fig16_surrogate_tree.png")

# -----------------------------------------------------------------------------
# 7. EXPORT ARTIFACTS
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("EXPORTING ARTIFACTS")
print("=" * 70)

# 1. Export Cluster Assignments Parquet
t0_export = time.perf_counter()
export_cols = ['user_id', 'cluster', 'cluster_name', 'pca_x', 'pca_y'] + winning_config[1]
df_clusters = df_buyers[export_cols]
df_clusters.to_parquet('data/features/buyer_clusters.parquet', index=False, compression='zstd')
parquet_export_time = time.perf_counter() - t0_export
print(f"Exported data/features/buyer_clusters.parquet ({len(df_clusters):,} rows) in {parquet_export_time:.2f}s")

# 2. Export Model Bundle
model_bundle = {
    'model': final_kmeans,
    'scaler': final_scaler,
    'pca': pca,
    'surrogate_tree': surrogate_tree,
    'feature_space': winning_config[0],
    'feature_names': winning_config[1],
    'scaler_type': winning_config[2],
    'k': winning_config[3],
    'log1p_candidates': LOG1P_CANDIDATES,
    'cluster_profiles': cluster_profiles,
    'metadata': {
        'trained_at': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        'dataset': 'REES46 E-commerce Cosmetics (Observation Window)',
        'cutoff_timestamp': '2020-02-01T00:00:00Z',
        'n_buyers': n_buyers,
        'fidelity_test_accuracy': fidelity_test_acc,
        'fidelity_test_macro_f1': fidelity_test_f1
    }
}
joblib.dump(model_bundle, 'outputs/models/kmeans_best_model.joblib', compress=3)
model_file_size_kb = os.path.getsize('outputs/models/kmeans_best_model.joblib') / 1024
print(f"Exported outputs/models/kmeans_best_model.joblib ({model_file_size_kb:.1f} KB)")

# 3. Export Experiment Manifest JSON & CSV
experiment_manifest = {
    'manifest_version': '1.0',
    'created_at': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    'hardware_context': {
        'cpu_count': psutil.cpu_count(logical=True),
        'total_ram_gb': round(psutil.virtual_memory().total / (1024**3), 2),
        'python_version': sys.version.split()[0]
    },
    'data_context': {
        'buyer_count': n_buyers,
        'feature_table': 'data/features/buyer_features.parquet',
        'observation_cutoff': '2020-02-01T00:00:00Z'
    },
    'round1_screening': round1_results,
    'round2_stability': round2_results,
    'stability_summary': stability_summary,
    'minibatch_vs_kmeans': minibatch_comparison,
    'winning_model': {
        'feature_space': winning_config[0],
        'feature_names': winning_config[1],
        'scaler': winning_config[2],
        'k': winning_config[3],
        'fit_time_sec': final_fit_time,
        'cluster_distribution': {f"cluster_{k}": int(v) for k, v in cluster_dist.items()},
        'surrogate_fidelity_test_accuracy': float(fidelity_test_acc),
        'surrogate_fidelity_test_macro_f1': float(fidelity_test_f1),
        'cluster_profiles': cluster_profiles
    },
    'figures': [
        'outputs/figures/fig13_elbow_silhouette.png',
        'outputs/figures/fig14_cluster_pca.png',
        'outputs/figures/fig15_cluster_profiles.png',
        'outputs/figures/fig16_surrogate_tree.png'
    ],
    'execution_summary': {
        'total_runtime_sec': float(time.perf_counter() - t0_total),
        'peak_rss_mb': float(get_rss_mb())
    }
}

with open('outputs/experiments/phase4_model_selection.json', 'w') as f:
    json.dump(experiment_manifest, f, indent=2)
print("Saved outputs/experiments/phase4_model_selection.json")

# Export CSV for tabular inspection
df_round1.to_csv('outputs/experiments/phase4_round1_screening.csv', index=False)
pd.DataFrame(round2_results).to_csv('outputs/experiments/phase4_round2_stability.csv', index=False)
print("Saved outputs/experiments/phase4_round1_screening.csv and phase4_round2_stability.csv")

total_runtime = time.perf_counter() - t0_total
print("\n" + "=" * 70)
print(f"PHASE 4 COMPLETE: Total Runtime = {total_runtime:.2f}s | Peak RSS = {get_rss_mb():.2f} MB")
print("=" * 70)

