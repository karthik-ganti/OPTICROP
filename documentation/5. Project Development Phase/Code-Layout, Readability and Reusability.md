# Code Layout, Readability and Reusability

> **Project:** OptiCrop — Smart Agricultural Production Optimization Engine
>
> **Phase 5 — Project Development Phase**

| Team Member | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |

---

## Module Responsibilities (Separation of Concerns)

| Module | Responsibility |
|---|---|
| `app.py` | Flask routes, auth wiring, inference, persistence, boot-time seeding/loading |
| `models_db.py` | SQLAlchemy models only — `User`, `SoilData`, `Crop`, `MLModel`, `Prediction` |
| `crop_data.py` | Agronomic reference data + `get_crop_info()` helper (single source of truth) |
| `train_model.py` | Self-contained training pipeline, importable/runnable independently of the web app |

Keeping data models, reference data, training and the web layer in separate files makes each unit
small, testable and independently editable.

## Readability Practices

- **Module docstrings:** every Python file opens with a docstring explaining its role.
- **Section comments:** `app.py` and `train_model.py` are divided into clearly labelled sections
  (config, models, seeding, routes / load–clean–split–scale–train–save).
- **Descriptive names:** `seed_crops`, `seed_ml_model`, `load_ml_assets`, `get_crop_info`,
  `canonicalize_columns`, `evaluate`.
- **Constants over magic values:** `FEATURE_ORDER` (app) / `FEATURE_COLS` (training) name the
  feature contract in one place.
- **Consistent styling:** the frontend uses namespaced `oc-*` CSS classes and a shared `base.html`
  layout so pages stay visually consistent.

## Reusability Practices

| Reused Element | Where Defined | Reused By |
|---|---|---|
| `get_crop_info(crop_name)` | `crop_data.py` | Crop-table seeding + result/history enrichment |
| `CROP_INFO` dict (22 crops) | `crop_data.py` | Seeding and inference-time metadata lookup |
| `FEATURE_ORDER` / `FEATURE_COLS` | `app.py` / `train_model.py` | Guarantees identical feature order at train & serve |
| `base.html` layout | `templates/` | Extended by all 8 page templates |
| Field validation rules | `static/js/main.js` + server parse | Same min/max ranges on client and server |
| Env-var config | `app.py` | Local dev, `Procfile`, `render.yaml` |

## Robustness

- `get_crop_info()` returns a safe default for unknown labels instead of raising.
- `/predict` guards float parsing with `try/except (ValueError, KeyError)` and flashes a friendly error.
- The app loads the model lazily/gracefully: if `model.pkl` is absent it still boots and prompts training.
- Passwords are never stored in plaintext; only Werkzeug hashes are persisted; emails are lowercased.
