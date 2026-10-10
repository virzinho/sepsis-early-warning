# Modelling design

## Current prediction task

For each eligible time window:

- **Observation window:** previous 6 hourly rows.
- **Prediction window:** following 6 hourly rows.
- **Target:** `warning_next_6h = 1` if `SepsisLabel` becomes positive at least once in the prediction window.
- Windows are excluded if the warning label is already positive during the observation window.

This is deliberately named a **warning-label prediction**, not direct prediction of clinical sepsis onset. In the PhysioNet 2019 training data, `SepsisLabel` is already shifted 6 hours before the defined sepsis onset.

## Why sliding windows?

Using only the first six hours of every admission is arbitrary and wastes most of each patient's time series. Sliding windows create examples throughout the ICU stay while preserving temporal order.

## Leakage control

Multiple rows can come from the same patient. Therefore random row-level train/test splitting would leak patient-specific information across splits. The baseline uses `GroupShuffleSplit` with patient ID as the grouping variable.

Missing values are imputed **inside the sklearn pipeline after the split**, so test-set information is not used to choose training medians.

## Baseline

The first model is logistic regression with:

- median imputation;
- standardization;
- balanced class weights.

This is intentionally simple and interpretable. More complex models should only be compared after the baseline is stable.
