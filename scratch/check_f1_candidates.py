import json

with open('outputs/experiments/phase4_model_selection.json') as f:
    d = json.load(f)

print("=== ROUND 1 SCREENING FOR F1 ===")
for r in d['round1_screening']:
    if r['feature_space'] == 'F1' and (r['k'] in [3, 4]):
        print(f"Scaler: {r['scaler']} | K: {r['k']} | WCSS: {r['inertia']:.1f} | Sil: {r['silhouette_10k']:.4f} | DBI: {r['davies_bouldin']:.4f} | Min/Max Clust: {r['min_cluster_pct']:.1f}% / {r['max_cluster_pct']:.1f}% | Fit: {r['fit_time_sec']:.2f}s")

print("\n=== STABILITY SUMMARY (5 SEEDS) ===")
for s in d['stability_summary']:
    if s['feature_space'] == 'F1' and s['k'] in [3, 4]:
        print(f"Scaler: {s['scaler']} | K: {s['k']} | Mean ARI: {s['mean_ari']:.4f} +/- {s['std_ari']:.4f} (Min: {s['min_ari']:.4f}, Max: {s['max_ari']:.4f}) | Mean Sil: {s['mean_sil']:.4f} | Mean DBI: {s['mean_dbi']:.4f}")

