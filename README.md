# Sepsis Early Warning

A biomedical AI portfolio project exploring early warning of sepsis from routinely collected ICU data.

## Author

Fabio Virzì  
MSc student in **AI for Biomedicine and Healthcare (AIBH)**, University of Turin.

## Open the project in Jupyter

### Windows — easiest method

You do **not** need to configure Jupyter manually.

1. On GitHub click **Code → Download ZIP**.
2. Extract the ZIP to a normal folder.
3. Double-click **`start_jupyter_windows.bat`**.
4. On the first launch the script creates a local Python environment and installs the project dependencies.
5. JupyterLab opens automatically in your browser.
6. Open the `notebooks` folder and start with:
   - `01_patient_exploration.ipynb`
   - then `02_build_patient_features.ipynb`

You need **Python 3.13 or Python 3.12** installed on Windows. Python 3.15 is currently too new for some Jupyter dependencies used by this project. The launcher automatically looks for Python 3.13 first and Python 3.12 second.

If you previously ran the launcher with Python 3.15, that failed environment can be ignored: the updated launcher now creates a separate clean environment called `.venv-jupyter`.

### If Jupyter is already installed

Clone or download this repository, open a terminal inside the project directory and run:

```bash
pip install -r requirements.txt
jupyter lab
```

The notebooks are standard `.ipynb` files and can also be opened directly with Jupyter Notebook or JupyterLab.

## Project goal

The project investigates whether routinely collected ICU variables can identify patients approaching a future PhysioNet sepsis warning event.

The emphasis is not only on model performance, but on building a **causal, reproducible and leakage-aware pipeline**:

- understand raw patient-level longitudinal data;
- quantify missingness;
- engineer interpretable time-window features;
- preserve temporal order;
- split train/test data by patient;
- establish a transparent baseline before trying more complex models.

## Dataset

This project uses the public **PhysioNet / Computing in Cardiology Challenge 2019** dataset:

https://physionet.org/content/challenge-2019/1.0.0/

The training data contain hourly clinical measurements such as heart rate, oxygen saturation, temperature, blood pressure, respiratory rate, laboratory values, demographics and `SepsisLabel`.

In the original challenge, `SepsisLabel` is shifted **6 hours before the defined sepsis onset**. Therefore this repository explicitly refers to the modelling target as a **future warning label**, rather than treating it as direct clinical onset.

## Prediction design

The current prototype uses sliding windows:

- **6-hour observation window**
- **6-hour future prediction window**
- target = whether `SepsisLabel` becomes positive in the following 6 hours
- windows are excluded after the warning label has already become positive

Multiple samples may come from one patient. Train/test splitting is therefore performed **by patient ID**, not by individual row, to prevent patient-level leakage.

See [docs/modelling_design.md](docs/modelling_design.md) for details.

## Prototype baseline

The automated development pipeline was tested on the first **1,000 patients** from training set A.

It produced:

- **970** eligible patients
- **27,565** sliding-window samples
- **394** positive windows (~1.43%)
- logistic-regression AUROC: **0.747**
- AUPRC: **0.0548**
- positive-class recall: **0.513**
- positive-class precision: **0.032**

The low precision is important: the model currently generates many false alarms. Accuracy is not emphasized because the target is extremely imbalanced.

Full interpretation: [results/prototype_baseline.md](results/prototype_baseline.md)

## Current status

- [x] Single-patient exploration
- [x] Missing-data exploration
- [x] Time-series visualization
- [x] Data-leakage analysis
- [x] Reusable feature extraction
- [x] Missing-safe trend features
- [x] Fixed observation and prediction horizons
- [x] Sliding-window dataset generation
- [x] Patient-grouped train/test split
- [x] Median imputation inside the modelling pipeline
- [x] Interpretable logistic-regression baseline
- [x] Automated GitHub Actions development run
- [ ] Threshold analysis
- [ ] Calibration analysis
- [ ] Confidence intervals / repeated validation
- [ ] Add selected laboratory variables
- [ ] Compare tree-based models
- [ ] Test on the full training cohort

## Repository structure

```
sepsis-early-warning/
├── .github/
│   └── workflows/
│       └── prototype-baseline.yml
├── data/
│   └── README.md
├── docs/
│   └── modelling_design.md
├── notebooks/
│   ├── 01_patient_exploration.ipynb
│   └── 02_build_patient_features.ipynb
├── results/
│   └── prototype_baseline.md
├── scripts/
│   └── download_sample.py
├── src/
│   ├── baseline.py
│   ├── build_dataset.py
│   └── features.py
├── .gitignore
├── README.md
├── requirements.txt
└── start_jupyter_windows.bat
```

## Important methodological note

This is a learning and research portfolio project. It is **not a clinical decision-support system** and must not be used for patient care.
