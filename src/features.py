from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

VITALS = ["HR", "O2Sat", "Temp", "SBP", "MAP", "Resp"]
STATIC_FEATURES = ["Age", "Gender", "Unit1", "Unit2", "HospAdmTime"]


def _last_valid(series: pd.Series) -> float:
    values = series.dropna()
    if values.empty:
        return float("nan")
    return float(values.iloc[-1])


def _slope(values: pd.Series, times: pd.Series) -> float:
    valid = values.notna() & times.notna()
    if valid.sum() < 2:
        return float("nan")

    x = times.loc[valid].astype(float).to_numpy()
    y = values.loc[valid].astype(float).to_numpy()

    if np.unique(x).size < 2:
        return float("nan")

    return float(np.polyfit(x, y, 1)[0])


def extract_window_features(
    observation: pd.DataFrame,
    patient_id: str,
    vital_columns: Iterable[str] = VITALS,
) -> dict:
    """Create interpretable features using only the observation window."""
    features = {
        "patient": patient_id,
        "window_end_iculos": float(observation["ICULOS"].iloc[-1]),
    }

    for column in STATIC_FEATURES:
        features[column] = _last_valid(observation[column])

    times = observation["ICULOS"]

    for column in vital_columns:
        values = observation[column]
        features[f"{column}_mean"] = float(values.mean())
        features[f"{column}_min"] = float(values.min())
        features[f"{column}_max"] = float(values.max())
        features[f"{column}_std"] = float(values.std())
        features[f"{column}_last"] = _last_valid(values)
        features[f"{column}_slope"] = _slope(values, times)
        features[f"{column}_missing_fraction"] = float(values.isna().mean())

    return features


def make_patient_windows(
    patient: pd.DataFrame,
    patient_id: str,
    observation_hours: int = 6,
    prediction_hours: int = 6,
    stride: int = 1,
) -> list[dict]:
    """
    Create causal sliding-window samples for one patient.

    Each sample uses the previous observation_hours rows and predicts whether
    SepsisLabel becomes positive during the following prediction_hours rows.
    Windows are dropped once SepsisLabel is already positive in the observed
    period.
    """
    if observation_hours < 1 or prediction_hours < 1 or stride < 1:
        raise ValueError("observation_hours, prediction_hours and stride must be >= 1")

    required = set(VITALS + STATIC_FEATURES + ["ICULOS", "SepsisLabel"])
    missing = required.difference(patient.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))

    samples = []
    final_end = len(patient) - prediction_hours

    for end_idx in range(observation_hours, final_end + 1, stride):
        observation = patient.iloc[end_idx - observation_hours:end_idx]
        future = patient.iloc[end_idx:end_idx + prediction_hours]

        if observation["SepsisLabel"].max() == 1:
            continue

        row = extract_window_features(observation, patient_id)
        row["warning_next_6h"] = int(future["SepsisLabel"].max())
        samples.append(row)

    return samples
