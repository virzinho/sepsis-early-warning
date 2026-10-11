# Sepsis Early Warning

Early-warning experiment on the PhysioNet / Computing in Cardiology Challenge 2019 ICU dataset.

## Question

Can routinely collected ICU variables help identify a future sepsis warning event?

Current setup:
- 6 hours of observations
- 6-hour prediction window
- patient-level train/test splitting
- simple time-window features
- logistic regression baseline

The target is the future PhysioNet `SepsisLabel`, not raw clinical sepsis onset.

## Current baseline

Development run on the first 1,000 patients from training set A:

| Metric | Result |
|---|---:|
| Eligible patients | 970 |
| Windows | 27,565 |
| Positive windows | 394 |
| AUROC | 0.747 |
| AUPRC | 0.0548 |
| Recall, positive class | 0.513 |
| Precision, positive class | 0.032 |

The main issue so far is false alarms. The positive class represents only about 1.4% of windows, so accuracy is not a useful headline metric.

More detail: [results/prototype_baseline.md](results/prototype_baseline.md)

## Notebooks

- `01_patient_exploration.ipynb`
- `02_build_patient_features.ipynb`

## Open in Jupyter on Windows

If Jupyter is already installed:

1. download and extract the repository
2. double-click `start_jupyter_windows.bat`
3. it simply opens the first notebook using your existing Jupyter installation

The launcher does **not** install Python, Jupyter or project dependencies.

If the launcher cannot find Jupyter, open Jupyter normally and browse to the extracted project folder.

## Files

```
notebooks/   exploratory work
src/         feature building and baseline model
scripts/     development data downloader
results/     current baseline results
docs/        modelling notes
```

## Dataset

PhysioNet / Computing in Cardiology Challenge 2019  
https://physionet.org/content/challenge-2019/1.0.0/

This is a research/portfolio project, not a clinical tool.
