# Project Planning

> **Project:** OptiCrop — Smart Agricultural Production Optimization Engine
>
> **Phase 4 — Project Planning Phase**

| Team Member | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |

---

## Milestones

| Milestone | Deliverable | Key Files |
|---|---|---|
| M1 — Data & EDA | Dataset understood, cleaned, analysed | `notebooks/opticrop_model.ipynb`, `dataset/Crop_recommendation.csv` |
| M2 — Model training | Best model selected & serialized | `train_model.py`, `models/*.pkl`, `models/metrics.txt` |
| M3 — Core web app | Flask app, prediction route | `app.py`, `templates/findyourcrop.html`, `result.html` |
| M4 — Auth & history | Accounts, login, saved predictions | `models_db.py`, `templates/login.html`, `history.html` |
| M5 — UI & guidance | Bootstrap UI, agronomic tips, validation | `crop_data.py`, `static/`, `templates/base.html` |
| M6 — Deployment | Free-tier cloud deploy | `Procfile`, `render.yaml`, `requirements.txt` |
| M7 — Documentation | 8-phase project documentation | `documentation/` |

## Sprint Plan

| Sprint | Focus | Milestones | Outcome |
|---|---|---|---|
| Sprint 1 | Data exploration + modelling | M1, M2 | Random Forest (99.55%) saved as `model.pkl` |
| Sprint 2 | Web app + inference | M3 | Working `/predict` → `/result` flow |
| Sprint 3 | Auth, history, UI, tips | M4, M5 | Accounts, per-user history, polished UI |
| Sprint 4 | Deployment + docs | M6, M7 | Live on Render + full documentation |

## Task Allocation

| Member | Primary Responsibilities |
|---|---|
| **Vaddimani Nikitha Sai** (Team Lead) | Planning, coordination, architecture decisions, review & integration, deployment oversight |
| Ramavenkata Manideep Gokarakonda | Data preprocessing, EDA notebook, model training & comparison (`train_model.py`) |
| Kavya Kallapalli | Flask routes & inference logic, session/result flow (`app.py`) |
| Samikeri Rama Pallavi | Database models & auth, prediction history (`models_db.py`, auth templates) |
| S K R S Sai Prakash Nidadavolu | Frontend (Bootstrap templates, CSS/JS validation), agronomic data (`crop_data.py`) |

> Allocation reflects primary ownership; members collaborated across areas and shared testing,
> documentation and demo preparation.

## Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Free-tier memory limit (512 MB) | App crashes / OOM | Single gunicorn worker + threads; small model artifact |
| Train/serve feature-order skew | Wrong predictions | Shared fixed `FEATURE_ORDER` / `FEATURE_COLS` |
| Missing trained model at deploy | Prediction fails | App boots gracefully and flashes a "train model" message |
| Overfitting on clean dataset | Misleading accuracy | Stratified 80/20 split, multi-model comparison |
