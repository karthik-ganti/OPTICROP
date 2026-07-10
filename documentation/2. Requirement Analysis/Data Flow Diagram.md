# Data Flow Diagram

> **Project:** OptiCrop — Smart Agricultural Production Optimization Engine
>
> **Phase 2 — Requirement Analysis**

| Team Member | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |

---

## Context (Level 0)

```
        ┌─────────┐        soil + climate inputs         ┌──────────────────┐
        │  User   │  ─────────────────────────────────▶  │                  │
        │(Farmer) │                                       │  OptiCrop System │
        │         │  ◀─────────────────────────────────  │                  │
        └─────────┘   crop recommendation + tips          └──────────────────┘
                                                                   │
                                                                   ▼
                                                          ┌──────────────────┐
                                                          │  SQLite Database │
                                                          └──────────────────┘
```

## Level 1 — Prediction Flow

```
 ┌──────┐   1. register/login    ┌─────────────────┐   store/verify   ┌──────────────┐
 │ User │ ─────────────────────▶ │ Auth (Flask-    │ ───────────────▶ │  users table │
 │      │                        │ Login/Werkzeug) │                  └──────────────┘
 │      │                        └─────────────────┘
 │      │
 │      │   2. submit 7 inputs    ┌─────────────────────────────────────────────┐
 │      │ ──────────────────────▶ │  /predict route (app.py)                    │
 │      │                         │  a. parse & validate 7 floats               │
 │      │                         │  b. scaler.transform(inputs)  ◀── scaler.pkl│
 │      │                         │  c. model.predict_proba()     ◀── model.pkl │
 │      │                         │  d. rank → best crop + top-3 + confidence   │
 │      │                         │  e. enrich via crop_data / Crop table       │
 │      │                         └───────────────┬─────────────────────────────┘
 │      │                                         │ 3. persist
 │      │                                         ▼
 │      │                         ┌──────────────────────────────────┐
 │      │                         │ soil_data + prediction tables    │
 │      │  4. recommendation      └──────────────────────────────────┘
 │      │ ◀───────────────────────  result page (session)
 │      │
 │      │   5. view history       ┌─────────────────┐   join soil_data
 │      │ ──────────────────────▶ │ /history route  │ ─── + prediction ──▶ table view
 └──────┘                         └─────────────────┘
```

## Data Stores

| Store | Contents |
|---|---|
| `users` | Account: name, email (unique), password hash, role |
| `soil_data` | The 7 input values per submission, linked to a user + timestamp |
| `prediction` | Recommended crop, confidence, links to soil_data, ml_model, crop |
| `crop` | Reference agronomic metadata for 22 crops (seeded at boot) |
| `ml_model` | Deployed model metadata (name, algorithm, accuracy) |
| `model.pkl` / `scaler.pkl` | Serialized trained model and feature scaler on disk |
| `dataset/Crop_recommendation.csv` | Training data (2,200 rows, 22 classes) |

## Processing Steps (offline training)

```
CSV ─▶ clean (median/mode) ─▶ split (80/20 stratified) ─▶ StandardScaler
    ─▶ train 4 models ─▶ pick best (accuracy) ─▶ pickle model.pkl + scaler.pkl + metrics.txt
```
