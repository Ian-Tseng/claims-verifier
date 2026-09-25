# Pilot results

## E6: custom development tasks

E6 was trained on 1,500 synthetic tasks and evaluated at the fixed update-100 checkpoint on 300 different, previously inspected development instances from familiar families. On the same 300 development tasks with matched prompts, decoding and scoring, **Original Qwen3-8B scored 69/300 (23.00%)**, compared with **E6's 268/300 (89.33%)**. Both completed runs passed saved-response identity and score-replay checks.

| Domain | E6 correct / tasks | E6 accuracy | Original |
|---|---:|---:|---|
| Math | 98 / 100 | 98.00% | 50 / 100 (50.00%) |
| Programming | 82 / 100 | 82.00% | 19 / 100 (19.00%) |
| Logic | 88 / 100 | 88.00% | 0 / 100 (0.00%) |
| **Overall** | **268 / 300** | **89.33%** | 69 / 300 (23.00%) |

![E6 development results](../figures/e6_results.png)

All 300 E6 outputs parsed as JSON; 267 met the strict reference-map contract. Answer correctness is scored separately from map validity. These are single-seed development results, not evidence of reliable transfer to unseen source material or a causal benefit from set representations. See the [dataset and protocol](../datasets/e6_custom_v1/README.md) and [saved aggregate](../datasets/e6_custom_v1/e6_update100_summary.json).

## Result interpretation

E6 answers **268/300 development tasks correctly (89.33%)**. It performs best on math (98/100), followed by logic (88/100) and programming (82/100). The domain differences identify where this custom-task evaluation succeeds and where errors remain.

**Answer accuracy and map validity are different outcomes.** All 300 outputs parse as JSON; 267 satisfy the strict reference-map contract. A valid map must match the supported task-bound structure. This count does not establish faithful interpretation of arbitrary paragraphs, and correct final answers do not necessarily contain valid maps.

**The comparison is within familiar task families.** Training uses 1,500 tasks; evaluation uses 300 different instances that were previously inspected during development. The matched Original control has completed and passed replay. This comparison measures the effect of the complete E6 fine-tuning procedure relative to the unadapted base under the shared output contract. It will not isolate a causal benefit of set maps from additional training or format learning; that requires matched training controls.

**Transfer remains unresolved.** Success here does not establish useful gains on unfamiliar source material, MATH-500, or fact verification. Source-to-map translation, execution, evidence selection and output-format failures remain competing explanations. We plan to measure those stages separately before choosing targeted changes; these diagnostics are not evidence that the transfer gap is already solved.

This is one training seed with automated checking and no expert review. Broader robustness and independent reproduction remain unestablished. The earlier E1 result is retained below as historical evidence rather than a substitute baseline.

The earlier E1 pilot below uses another evaluation cohort and protocol. Its percentages must not be used as E6's matched baseline.

## Historical E1 pilot

The completed procedural pilot compares final-answer accuracy on 1,500 paired test tasks, with 500 tasks each in mathematics, programming, and finite-set logic.

| Model | Correct / tasks | Accuracy |
|---|---:|---:|
| Original Qwen3-8B | 144 / 1,500 | 9.6% |
| Historical 300-task adapter | 154 / 1,500 | 10.3% |
| Answer-SFT, selected update 100 | 325 / 1,500 | 21.7% |
| Verified-map, selected update 60 | 470 / 1,500 | 31.3% |

The primary map-versus-answer-SFT difference is **+9.7 percentage points**, with a paired 95% bootstrap interval of **+7.3 to +12.1 points**. The exact two-sided McNemar test gives $p=9.12\times10^{-10}$, with 352 map-only correct tasks and 207 answer-SFT-only correct tasks. These estimates condition on the selected checkpoints, one training seed, and the sampled task families.

## Results differ by domain

| Domain | Answer-SFT | Verified-map | Difference |
|---|---:|---:|---:|
| Mathematics | 69 / 500 (13.8%) | 199 / 500 (39.8%) | +26.0 pp |
| Programming | 172 / 500 (34.4%) | 56 / 500 (11.2%) | -23.2 pp |
| Finite-set logic | 84 / 500 (16.8%) | 215 / 500 (43.0%) | +26.2 pp |

The best development accuracy is 33.0% (99/300), at map update 60. Development accuracy selects the checkpoint; 31.3% is its final test accuracy.

## Supervision and collection costs

| Quantity | Answer-SFT | Verified-map |
|---|---:|---:|
| Training tasks | 1,500 | 1,500 |
| Optimizer updates | 100 | 100 |
| Supervised target tokens | 22,200 | 136,624 |
| Candidate-generation attempts | 0 | 1,822 |
| Tasks using correction feedback | 0 | 322 |
| Training GPU time | 1,139 s | 1,096 s |
| Candidate-collection GPU time | 0 s | 20,929 s |

Timings cover the recorded training and candidate collection stages, excluding evaluation and model loading. The answer control also uses oracle-derived labels; zero collection attempts means it does not generate candidate maps.

## Historical E1 interpretation

The result supports the full map-training procedure under this pilot protocol. It does not isolate representation structure from longer targets, oracle-assisted corrections, or collection compute. Programming performance declines, so the overall average does not establish an improvement in every domain.

Strict answer extraction affects scores: the evaluator records 760 answer parse failures for the original model, 708 for the historical adapter, 22 for answer-SFT, and 606 for the map arm. These failures stay in the denominator. The original model's 9.6% score measures this prompt, output contract, and task distribution; it is not a general estimate of Qwen3-8B capability.

This is a single-seed procedural pilot. It does not establish biological plausibility, general natural-language understanding, fact-checking performance, or publication eligibility. Further ablations, seed replication, and external evaluation are necessary to assess those claims.

## Evidence files

- [Machine-readable results](pilot1500.json)
- [Compact benchmark table](pilot1500.csv)
- [Aggregate provenance](provenance.json)

The private experiment stores raw responses, completion records, and source identities. The public snapshot contains aggregate results only, so its hashes support version tracking without providing an independently executable reproduction.

Matched paired outcomes: both_correct=69, original_only=0, e6_only=199, both_wrong=32. See [comparison evidence](../datasets/e6_custom_v1/matched_comparison.json).
