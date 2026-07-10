# Solution Architecture

> **Project:** OptiCrop — Smart Agricultural Production Optimization Engine
>
> **Phase 3 — Project Design Phase**

| Team Member | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |

---

## Architecture Diagram

```
 ┌───────────────────────────────────────────────────────────────────────────┐
 │                              CLIENT (Browser)                              │
 │   Bootstrap 5 UI · Jinja2 templates · static/js/main.js (validation)      │
 └───────────────┬───────────────────────────────────────────────────────────┘
                 │  HTTP (forms / pages)
                 ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │                        FLASK APPLICATION (app.py)                          │
 │                                                                           │
 │   Routing & Views        Auth (Flask-Login)        Inference             │
 │   / , /about             /login /register /logout  scaler.transform()    │
 │   /findyourcrop          @login_required           model.predict_proba() │
 │   /predict /result       user_loader               rank → top-3          │
 │   /history                                         crop_data enrichment  │
 └───────┬───────────────────────────┬───────────────────────┬──────────────┘
         │                           │                       │
         ▼                           ▼                       ▼
 ┌──────────────┐          ┌──────────────────┐    ┌───────────────────────┐
 │  ML Assets   │          │  ORM (SQLAlchemy)│    │  Reference data       │
 │ model.pkl    │          │  users           │    │  crop_data.py (22)    │
 │ scaler.pkl   │          │  soil_data       │    │  Crop table (seeded)  │
 │ metrics.txt  │          │  prediction      │    │                       │
 └──────┬───────┘          │  crop / ml_model │    └───────────────────────┘
        │                  └────────┬─────────┘
        │ trained offline           │
        ▼                           ▼
 ┌──────────────────┐      ┌──────────────────┐
 │ train_model.py   │      │  SQLite DB       │
 │ (4 models → best)│      │  opticrop.db     │
 │ dataset CSV      │      │  (DATABASE_URL)  │
 └──────────────────┘      └──────────────────┘
```

## Components

| Component | File(s) | Responsibility |
|---|---|---|
| Web app / routes | `app.py` | Views, auth, inference, persistence, boot-time seeding |
| Data models | `models_db.py` | `User`, `SoilData`, `Crop`, `MLModel`, `Prediction` |
| Agronomic reference | `crop_data.py` | 22-crop metadata + `get_crop_info()` |
| Training pipeline | `train_model.py` | Clean → split → scale → train 4 models → pickle best |
| ML artifacts | `models/model.pkl`, `models/scaler.pkl`, `models/metrics.txt` | Deployed model, scaler, metadata |
| Dataset | `dataset/Crop_recommendation.csv` | 2,200 rows, 22 crop classes |
| Views | `templates/*.html` | Jinja2 pages extending `base.html` |
| Static assets | `static/css`, `static/js`, `static/images` | Styling, client validation, plots |
| Deploy config | `Procfile`, `render.yaml` | gunicorn startup, Render Blueprint |

## Request Lifecycle (`/predict`)

1. `@login_required` ensures an authenticated user.
2. Parse 7 form fields to floats; on `ValueError`/`KeyError`, flash an error and return.
3. Build `np.array` in `FEATURE_ORDER`; `scaler.transform()`.
4. `model.predict_proba()` → sort descending → recommended crop + confidence + top-3.
5. Enrich with `Crop`/`crop_data` metadata (type, season, pH, water, tip, emoji).
6. Persist `SoilData` + `Prediction` rows; stash results in `session`.
7. Redirect to `/result`, which renders from session.

## Boot Sequence (`with app.app_context()`)

`db.create_all()` → `seed_crops()` (22 crops) → `seed_ml_model()` (reads `metrics.txt`) →
`load_ml_assets()` (loads `model.pkl` + `scaler.pkl` into globals if present).

## Data Model (ER)

```
User (1) ───< SoilData (1) ─── (1) Prediction >─── (1) MLModel
                                       │
                                       └── (0..1) Crop  [reference]
```

- **User → SoilData:** one user has many soil-data submissions.
- **SoilData → Prediction:** one-to-one; each submission yields one prediction.
- **Prediction → MLModel:** which model produced the result.
- **Prediction → Crop:** reference link to the recommended crop's metadata.
