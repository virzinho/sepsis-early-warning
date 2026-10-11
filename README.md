# Sepsis Early Warning

Early-warning experiment on the PhysioNet / Computing in Cardiology Challenge 2019 ICU dataset.

## Question

Can routinely collected ICU variables help identify a future sepsis warning event?

The current setup uses:
- 6 hours of observations
- a 6-hour prediction window
- patient-level train/test splitting
- simple time-window features from vital signs
- logistic regression as the first baseline

The target is the future **PhysioNet `SepsisLabel`**, not raw clinical sepsis onset. In the challenge data the label is already shifted 6 hours before the defined onset.

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

- `01_patient_exploration.ipynb` — first look at one patient, missing data, simple summaries and the first leakage check
- `02_build_patient_features.ipynb` — turn the same logic into reusable patient-level features

The production-style sliding-window version is in `src/`.

## Open in Jupyter on Windows

Python **3.13 or 3.12** is recommended. Python 3.15 can remain installed; the launcher simply does not use it.

1. Download and extract the repository.
2. Double-click `start_jupyter_windows.bat`.
3. The first run installs Jupyter and the dependencies.
4. Later runs reuse the same environment stored in Windows, even if you download a newer copy of the repo.

After the first setup, opening the project should only require starting Jupyter rather than reinstalling everything.

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
