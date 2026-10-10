# Prototype baseline results

## Development run

The automated prototype pipeline was run on the first **1,000 patient files** from PhysioNet training set A.

After requiring complete 6-hour observation and 6-hour prediction windows:

- downloaded patient files: **1,000**
- patients contributing at least one sample: **970**
- sliding-window samples: **27,565**
- negative windows: **27,171**
- positive windows: **394**
- overall positive-window prevalence: **1.43%**

This is a strongly imbalanced prediction problem.

## Baseline model

Model:

- logistic regression
- median imputation
- feature standardization
- `class_weight="balanced"`
- patient-grouped 80/20 train/test split

Test set:

- train patients: **776**
- test patients: **194**
- test windows: **5,422**
- positive test windows: **78**

### Metrics

| Metric | Value |
|---|---:|
| AUROC | 0.747 |
| AUPRC | 0.0548 |
| Positive-class recall | 0.513 |
| Positive-class precision | 0.032 |
| Positive-class F1 | 0.061 |

Confusion matrix:

```
[[4142, 1202],
 [  38,   40]]
```

## Interpretation

The AUROC shows that the baseline contains some ranking signal, but it is not sufficient evidence of useful clinical performance.

The positive class is rare: only about 1.4% of windows are positive. For that reason, accuracy is particularly misleading. A model that predicted every window as negative would obtain very high accuracy while detecting no future warning events.

With the default threshold and balanced class weights, the logistic regression detects about half of the positive windows, but precision is only about 3.2%. In practical terms, it generates many false alarms.

The AUPRC of 0.0548 is above the approximate positive prevalence baseline (~0.014), but remains low in absolute terms.

## What this result is — and is not

This is a **development baseline**, not a clinical result.

Limitations include:

- only the first 1,000 patients from training set A were used;
- no external validation;
- only a small set of vital signs and demographics is included;
- no threshold tuning;
- no calibration analysis;
- no confidence intervals;
- repeated time windows come from each patient, although train/test splitting is correctly grouped by patient;
- the target is the future PhysioNet warning label, not direct clinical sepsis onset.

The purpose of this baseline is to establish a reproducible reference point for later models.
