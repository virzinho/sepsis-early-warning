# Sepsis Early Warning

A learning-oriented biomedical AI project exploring early warning of sepsis from routinely collected ICU data.

## Author

Fabio Virzì  
MSc student in **AI for Biomedicine and Healthcare (AIBH)**, University of Turin.

## Project goal

The long-term goal is to investigate whether routinely collected ICU variables can be used to identify patients at risk of sepsis before clinical onset.

The project is intentionally being developed step by step, starting from:
- understanding the raw patient-level data;
- exploring missing values;
- visualizing vital signs over time;
- comparing septic and non-septic patients;
- learning how to separate information available at prediction time from future information;
- engineering simple, interpretable features before moving to machine learning.

## Dataset

This project uses the public **PhysioNet / Computing in Cardiology Challenge 2019** sepsis dataset:

https://physionet.org/content/challenge-2019/1.0.0/

Each patient is stored as a separate `.psv` file containing hourly clinical variables such as:
- heart rate (`HR`);
- oxygen saturation (`O2Sat`);
- temperature (`Temp`);
- systolic blood pressure (`SBP`);
- mean arterial pressure (`MAP`);
- respiratory rate (`Resp`);
- laboratory values;
- demographic variables;
- `SepsisLabel`.

In the original challenge, the positive sepsis label is shifted earlier to support early prediction. Because of this, the exact prediction horizon and target definition must be handled carefully.

## Current status

### Phase 1 — completed / in progress
- [x] Load and inspect one patient
- [x] Inspect clinically relevant variables
- [x] Quantify missing data
- [x] Plot heart rate over ICU stay
- [x] Visualize the first positive sepsis warning label
- [x] Summarize multiple patients
- [x] Compare simple descriptive statistics between patients with and without a sepsis label
- [x] Introduce the concept of data leakage
- [x] Split an observation window from future data
- [x] Begin simple feature engineering on the first six observations
- [x] Handle missing HR values when computing a simple change feature
- [x] Build a reusable patient-processing function
- [x] Scale the same feature extraction logic to the first 100 patients

### Next steps
- [ ] Define a rigorous prediction horizon
- [ ] Investigate missing-data strategies
- [ ] Expand the feature set
- [ ] Create train/test splits at patient level
- [ ] Build an interpretable baseline model
- [ ] Evaluate sensitivity, specificity, AUROC and AUPRC
- [ ] Compare baseline models with more advanced approaches

## Repository structure

```
sepsis-early-warning/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── README.md
└── notebooks/
    ├── 01_patient_exploration.ipynb
    └── 02_build_patient_features.ipynb
```

## Important methodological note

This repository is a learning and research project. It is **not a clinical decision-support system** and must not be used for patient care.

A central focus of the project is avoiding **data leakage**: a prediction model must only use information that would genuinely have been available at the moment the prediction is made.
