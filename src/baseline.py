from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

TARGET = "warning_next_6h"
GROUP = "patient"


def main():
    dataset = pd.read_csv("data/processed/sepsis_windows.csv")

    X = dataset.drop(columns=[TARGET, GROUP])
    y = dataset[TARGET]
    groups = dataset[GROUP]

    split = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(split.split(X, y, groups=groups))

    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    preprocessing = ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), X.columns.tolist())
    ])

    model = Pipeline([
        ("preprocessing", preprocessing),
        ("classifier", LogisticRegression(
            class_weight="balanced",
            max_iter=2000,
            random_state=42,
        )),
    ])

    model.fit(X_train, y_train)

    probability = model.predict_proba(X_test)[:, 1]
    prediction = model.predict(X_test)

    print("Train patients:", groups.iloc[train_idx].nunique())
    print("Test patients:", groups.iloc[test_idx].nunique())
    print("AUROC:", roc_auc_score(y_test, probability))
    print("AUPRC:", average_precision_score(y_test, probability))
    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, prediction))
    print("\nClassification report:")
    print(classification_report(y_test, prediction, digits=3))


if __name__ == "__main__":
    main()
