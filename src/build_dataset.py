from __future__ import annotations

from pathlib import Path
import pandas as pd

from features import make_patient_windows


def build_dataset(
    data_dirs,
    observation_hours: int = 6,
    prediction_hours: int = 6,
    stride: int = 1,
) -> pd.DataFrame:
    rows = []

    for data_dir in data_dirs:
        for path in sorted(Path(data_dir).glob("*.psv")):
            patient = pd.read_csv(path, sep="|")
            rows.extend(
                make_patient_windows(
                    patient=patient,
                    patient_id=path.stem,
                    observation_hours=observation_hours,
                    prediction_hours=prediction_hours,
                    stride=stride,
                )
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    dataset = build_dataset(
        ["data/raw/training_setA", "data/raw/training_setB"],
        observation_hours=6,
        prediction_hours=6,
        stride=1,
    )

    out = Path("data/processed")
    out.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(out / "sepsis_windows.csv", index=False)

    print("Rows:", len(dataset))
    print("Patients:", dataset["patient"].nunique())
    print(dataset["warning_next_6h"].value_counts(dropna=False))
