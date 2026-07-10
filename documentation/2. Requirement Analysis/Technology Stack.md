# Technology Stack

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

## Overview

OptiCrop is a Python web application: a Flask backend serves Jinja2/Bootstrap pages and runs
inference with a pre-trained scikit-learn model persisted to disk with pickle.

## Stack Table

| Layer | Technology | Version (min) | Role |
|---|---|---|---|
| Language | Python | 3.12.4 (deploy target) | Backend + ML |
| Web framework | Flask | ≥ 2.3.0 | Routing, request handling, templating |
| Auth | Flask-Login | ≥ 0.6.0 | Session-based login, `@login_required` |
| ORM / DB | Flask-SQLAlchemy | ≥ 3.0.0 | Models & persistence |
| Security | Werkzeug | ≥ 2.3.0 | Password hashing (`generate/check_password_hash`) |
| ML | scikit-learn | ≥ 1.3.0 | Classifiers, `StandardScaler`, `KMeans` |
| Data | pandas | ≥ 2.0.0 | Load / clean the dataset |
| Numerics | numpy | ≥ 1.24.0 | Feature arrays for inference |
| Persistence | pickle / joblib | ≥ 1.3.0 | Save & load `model.pkl`, `scaler.pkl` |
| Visualization | matplotlib, seaborn | ≥ 3.7.0 / ≥ 0.12.0 | EDA, elbow & model-comparison plots |
| Notebook | jupyter, notebook | ≥ 1.0.0 / ≥ 7.0.0 | Exploratory analysis |
| Frontend | Bootstrap 5.3.0, Bootstrap Icons 1.11.0 | via CDN | Responsive UI |
| Database engine | SQLite (default) | — | Local/persistent store (`DATABASE_URL` configurable) |
| WSGI server | gunicorn | ≥ 21.2.0 | Production server |
| Hosting | Render (Blueprint) | — | Free-tier cloud deployment |

## Machine-Learning Models

Four classifiers are trained and compared in `train_model.py`; the best by accuracy is deployed.

| Model | Configuration | Purpose |
|---|---|---|
| K-Nearest Neighbours | `n_neighbors=5` | Baseline distance classifier |
| Logistic Regression | `max_iter=1000` | Linear baseline |
| Decision Tree | default, `random_state=42` | Interpretable tree |
| **Random Forest** ✅ | `n_estimators=100` | **Deployed** — 99.55% accuracy |
| K-Means (clustering) | `k=1..10`, elbow analysis | Exploratory grouping only |

## Feature Contract

The seven features are always used in this exact order at training and inference:

```
['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
```

Defined as `FEATURE_ORDER` in `app.py` and `FEATURE_COLS` in `train_model.py`.

## Configuration (Environment Variables)

| Variable | Default | Purpose |
|---|---|---|
| `SECRET_KEY` | `opticrop_secret_key_2024` (fallback) | Flask session signing; auto-generated on Render |
| `DATABASE_URL` | `sqlite:///opticrop.db` | Database connection string |
| `PORT` | `5000` | Port the server binds to |
