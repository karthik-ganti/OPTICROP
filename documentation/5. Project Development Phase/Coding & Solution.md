# Coding & Solution

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

## 1. Training Pipeline (`train_model.py`)

A one-shot script that produces the deployed artifacts. Run with `python train_model.py`.

**Steps:**

1. **Load data** — read `dataset/Crop_recommendation.csv`; `canonicalize_columns()` maps header
   aliases to the canonical `N, P, K, temperature, humidity, ph, rainfall, label`.
2. **Clean** — fill missing numeric values with the median, categorical with the mode.
3. **Outlier analysis** — IQR report only; raw features are kept to avoid train/serve skew.
4. **Split** — `train_test_split(test_size=0.2, random_state=42, stratify=y)`.
5. **Scale** — `StandardScaler` fit on training features; K-Means elbow analysis (k=1..10) saved
   to `static/images/elbow_plot.png`.
6. **Train & compare** four models via `evaluate()`:
   - `KNeighborsClassifier(n_neighbors=5)`
   - `LogisticRegression(max_iter=1000, random_state=42)`
   - `DecisionTreeClassifier(random_state=42)`
   - `RandomForestClassifier(n_estimators=100, random_state=42)`
   Best model by accuracy chosen; comparison saved to `static/images/model_comparison.png`.
7. **Persist** — pickle best model → `models/model.pkl`, scaler → `models/scaler.pkl`, and write
   `models/metrics.txt` (`algorithm=Random Forest`, `accuracy=99.55`).

## 2. Inference (`/predict` in `app.py`)

```python
# 1. Parse & validate the 7 inputs (flash a friendly error on bad input)
try:
    values = [float(request.form[f]) for f in FEATURE_ORDER]
except (ValueError, KeyError):
    flash('Please enter valid numeric values for all fields.', 'danger')
    return redirect(url_for('predict_form'))

# 2. Scale with the SAME scaler used at training time
X = scaler.transform(np.array([values]))

# 3. Probabilities → recommended crop + confidence + top-3 alternatives
proba = model.predict_proba(X)[0]
ranked = sorted(zip(model.classes_, proba), key=lambda t: t[1], reverse=True)
recommended, confidence = ranked[0][0], round(ranked[0][1] * 100, 2)
top3 = ranked[:3]

# 4. Enrich, persist (SoilData + Prediction), stash in session, redirect to /result
```

> The exact code lives in `app.py`; the snippet above shows the essential flow.

## 3. Boot-time Setup (`app.py`)

```python
with app.app_context():
    db.create_all()      # create tables if missing
    seed_crops()         # populate the 22 crops (idempotent)
    seed_ml_model()      # insert model metadata from models/metrics.txt
    load_ml_assets()     # load model.pkl + scaler.pkl into module globals (if present)
```

## 4. Agronomic Enrichment (`crop_data.py`)

```python
def get_crop_info(crop_name):
    """Return the metadata dict for a crop label, or a sensible default."""
    return CROP_INFO.get((crop_name or '').strip().lower(), DEFAULT_INFO)
```

Each of the 22 crops has `crop_type`, `season`, `optimal_ph`, `water_requirement`, `emoji`, `tips`.

## 5. Data Models (`models_db.py`)

Five tables: `User`, `SoilData`, `Crop`, `MLModel`, `Prediction` — see the
[Solution Architecture](../3.%20Project%20Design%20Phase/Solution%20Architecture.md) ER diagram.

## Key Techniques

- Probability-based ranking (`predict_proba`) to expose confidence and alternatives.
- Identical `StandardScaler` at train and serve time (persisted alongside the model).
- Idempotent seeding so repeated boots don't duplicate reference rows.
- Env-var driven configuration for portability across local and cloud.
