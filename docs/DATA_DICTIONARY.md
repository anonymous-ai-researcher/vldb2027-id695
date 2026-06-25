# Data Dictionary

All result CSVs are in `data/`. Columns are self-describing; the most load-bearing files are annotated below.

| File | Rows | Cols | Role |
|---|---:|---:|---|
| `N_patch_summary.csv` | 35 | 5 |  |
| `ab_rag_acorn_honeybee_rows.csv` | 2 | 8 |  |
| `access_control_workload_sensitivity.csv` | 25920 | 17 |  |
| `appendix_G_real_stats.csv` | 48 | 24 | Statistical significance (bootstrap CIs, Holm correction, rank-biserial) |
| `attack.csv` | 3200 | 10 | Inference attacks: reconstruction F1/EM and distinguishing AUC |
| `audit.csv` | 12 | 8 |  |
| `audit_negative_tests.csv` | 108 | 9 |  |
| `baseline_unified_metrics.csv` | 10400 | 23 | Main results: per-method leakage/drift/recall/latency/memory/throughput (all patterns, fracs, datasets, seeds) |
| `bypass_ablation.csv` | 5600 | 19 | Ablation of the bypass overlay (no/pruned/unpruned, per-role/view/user) |
| `completion_source_map.csv` | 4 | 5 |  |
| `concurrency_crash_claim_aligned_by_scenario.csv` | 36 | 17 |  |
| `concurrency_crash_claim_aligned_file_manifest.csv` | 5 | 3 |  |
| `concurrency_crash_claim_aligned_summary.csv` | 4 | 16 |  |
| `concurrency_crash_claim_aligned_validation.csv` | 10 | 3 |  |
| `concurrency_crash_consistency.csv` | 720 | 26 | Concurrency & crash consistency: leakage/recall/recovery per crash point |
| `concurrency_crash_consistency_claim_aligned.csv` | 720 | 37 |  |
| `concurrency_crash_consistency_file_manifest.csv` | 3 | 3 |  |
| `concurrency_crash_consistency_recovery_path_summary.csv` | 36 | 12 |  |
| `concurrency_crash_consistency_validation.csv` | 11 | 3 |  |
| `concurrency_crash_correctness_by_scenario.csv` | 36 | 10 |  |
| `concurrency_crash_correctness_summary.csv` | 4 | 18 |  |
| `concurrency_crash_derived_correctness.csv` | 720 | 10 |  |
| `concurrency_crash_derived_file_manifest.csv` | 3 | 3 |  |
| `concurrency_crash_tab_ready.csv` | 4 | 10 |  |
| `csv_inventory.csv` | 49 | 5 |  |
| `dataset_size_reference.csv` | 4 | 4 |  |
| `diskann_vamana_validation.csv` | 420 | 17 | Generality to a second graph index (DiskANN/Vamana) |
| `exact_linear_scan_reference.csv` | 5600 | 11 |  |
| `exception_rate_sensitivity.csv` | 7200 | 16 | Sensitivity to the predicate exception rate |
| `fig_recall_b_source_mapping.csv` | 2 | 8 |  |
| `file_size_report.csv` | 39 | 7 |  |
| `graph_bypass_oracle_comparison.csv` | 2400 | 17 |  |
| `graph_construction_determinism.csv` | 1296 | 14 |  |
| `hub_bridge_adversarial_revocation.csv` | 1000 | 12 | Adversarial revocation targeting (hub/bridge/cluster/...) |
| `large_scale_stress.csv` | 180 | 23 |  |
| `latency_breakdown.csv` | 3360 | 15 |  |
| `leakage_instrumentation.csv` | 11520 | 31 | Per-stage operational leakage instrumentation |
| `leakage_recall.csv` | 11520 | 11 | Recall & drift sweep across revoked fraction and pattern |
| `memory.csv` | 288 | 22 |  |
| `memory_accounting.csv` | 1440 | 22 | Per-component memory accounting (base graph, overlay, reverse-adjacency, ...) |
| `micro_toy_graph_trace.csv` | 24 | 15 |  |
| `new_files_manifest.csv` | 14 | 5 |  |
| `oracle_stability.csv` | 2200 | 11 |  |
| `original_vs_N_patch_comparison.csv` | 35 | 6 |  |
| `per_query_trace_artifact.csv` | 1200 | 17 |  |
| `physical_global_erasure_split.csv` | 240 | 18 | Physical unrecoverability boolean checks |
| `rag_quality.csv` | 200 | 21 | End-to-end RAG quality (EM/F1) with access control |
| `rag_quality_acorn_honeybee_summary.csv` | 2 | 10 |  |
| `rag_quality_acorn_honeybee_supplement.csv` | 80 | 20 |  |
| `rag_quality_rerun.csv` | 200 | 21 |  |
| `recoverability.csv` | 40 | 7 |  |
| `reverse_adjacency_cost.csv` | 240 | 14 |  |
| `routing_trace.csv` | 11520 | 19 |  |
| `same_role_user_level_revocation.csv` | 7200 | 14 | User-level revocation within a shared role |
| `scalability.csv` | 180 | 23 | Scalability to large N (latency, throughput, memory, build time) |
| `statistical_reruns_summary.csv` | 48 | 14 |  |
| `stats_summary.csv` | 48 | 24 |  |
| `stats_summary_attribution_patch.csv` | 1 | 5 |  |
| `stats_summary_file_manifest.csv` | 3 | 4 |  |
| `stats_summary_fixed.csv` | 48 | 19 |  |
| `stats_summary_real.csv` | 48 | 23 |  |
| `stats_summary_validation.csv` | 10 | 3 |  |
| `tab_cost_single_source.csv` | 6 | 9 | Cost table single-source values (per-method batch_B operating point) |
| `throughput_window.csv` | 1800 | 11 | Revocation throughput and compliance window per batch size |
| `validation_checks.csv` | 6 | 3 |  |
| `view_isolation.csv` | 200 | 31 | View isolation: revoked vs unaffected user drift |
| `view_isolation_cross_validation.csv` | 40 | 6 |  |
| `view_isolation_summary.csv` | 5 | 19 |  |
| `view_scope_unaffected_user_drift.csv` | 7200 | 14 | Scope of disturbance to unaffected users |
