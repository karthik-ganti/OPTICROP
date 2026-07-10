# OptiCrop — Project Documentation

> **Smart Agricultural Production Optimization Engine**
>
> **Phase 7 — Project Documentation** (comprehensive reference)

| Team Member | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |

---

## 1. Overview

OptiCrop is a machine-learning web application that recommends the most suitable crop for a plot
of land from seven soil and climate inputs — **Nitrogen (N), Phosphorus (P), Potassium (K),
temperature, humidity, pH and rainfall** — choosing among **22 crops**. It is backed by a Random
Forest classifier (**99.55% test accuracy**) and provides user accounts, per-user prediction
history, and practical agronomic guidance for each recommendation.

🔗 **Live Application:** https://opticrop-6zg1.onrender.com

## 2. Objectives

- Turn measurable soil/climate readings into a specific, confident crop recommendation.
- Show a confidence score and top-3 alternatives so users can compare, not just accept.
- Enrich each result with agronomic context (season, optimal pH, water need, tips).
- Provide accounts and history so users can track decisions over time.
- Deploy on a free cloud tier for public access.

## 3. Features

| Feature | Description |
|---|---|
| Crop recommendation | Best-fit crop from 7 inputs via `predict_proba` |
| Confidence + top-3 | Probability of the top crop plus two alternatives |
| Agronomic guidance | Crop type, season, optimal pH, water need, emoji, tip |
| Accounts | Register / login / logout (Flask-Login) |
| History | Per-user list of past predictions |
| Multi-model training | KNN, Logistic Regression, Decision Tree, Random Forest compared |
| Graceful no-model mode | App boots and prompts training if no model exists |

## 4. Technology Stack

Python 3.12 · Flask · Flask-Login · Flask-SQLAlchemy · Werkzeug · scikit-learn · pandas · numpy ·
matplotlib · seaborn · Bootstrap 5 · SQLite · gunicorn · Render. Full detail in the
[Technology Stack](../2.%20Requirement%20Analysis/Technology%20Stack.md) document.

## 5. Architecture

Client (Bootstrap/Jinja2) → Flask (`app.py`: routing, auth, inference) → ML assets
(`model.pkl`, `scaler.pkl`) + ORM (SQLAlchemy) → SQLite. The model and scaler are trained offline
by `train_model.py` and loaded once at boot. See the full diagram and ER model in
[Solution Architecture](../3.%20Project%20Design%20Phase/Solution%20Architecture.md).

## 6. Dataset

- **Source:** public *Crop Recommendation* dataset — `dataset/Crop_recommendation.csv`.
- **Size:** 2,200 rows, 22 balanced crop classes.
- **Columns:** `N, P, K, temperature, humidity, ph, rainfall, label`.
- **Feature order (fixed):** `['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']`.

## 7. Machine-Learning Model

- **Pipeline:** load → clean (median/mode) → 80/20 stratified split → `StandardScaler` →
  train 4 models → pick best by accuracy → pickle.
- **Deployed:** Random Forest (`n_estimators=100`), **99.55%** accuracy.
- **Artifacts:** `models/model.pkl`, `models/scaler.pkl`, `models/metrics.txt`.
- **Reproducibility:** `python train_model.py` regenerates artifacts and comparison plots.

## 8. Application Routes

| Route | Methods | Auth | Purpose |
|---|---|---|---|
| `/` | GET | Public | Home; shows model accuracy |
| `/about` | GET | Public | About |
| `/register` | GET, POST | Public | Create account |
| `/login` | GET, POST | Public | Log in |
| `/logout` | GET | Required | Log out |
| `/findyourcrop` | GET | Required | Input form |
| `/predict` | POST | Required | Inference + persist |
| `/result` | GET | Required | Show recommendation |
| `/history` | GET | Required | Past predictions |

## 9. Data Model

Five tables — `User`, `SoilData`, `Crop`, `MLModel`, `Prediction`:

- **User** → many **SoilData** (a user's submissions).
- **SoilData** → one **Prediction** (the result of that submission).
- **Prediction** → **MLModel** (which model) and **Crop** (recommended crop metadata).

## 10. Setup & Run

```bash
pip install -r requirements.txt
python train_model.py      # creates models/model.pkl + scaler.pkl
python app.py              # http://localhost:5000
```

Detailed steps (Windows + macOS/Linux) are in
[Project Executable Files](./Project%20Executable%20Files.md).

## 11. Deployment

- **Procfile:** `web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`
- **render.yaml:** free-plan web service, `PYTHON_VERSION=3.12.4`, auto-generated `SECRET_KEY`.
- Single worker keeps memory under Render's 512 MB free tier.

## 12. Configuration

| Variable | Default | Purpose |
|---|---|---|
| `SECRET_KEY` | fallback constant | Session signing (set in production) |
| `DATABASE_URL` | `sqlite:///opticrop.db` | DB connection |
| `PORT` | `5000` | Bind port |

## 13. Testing

Model comparison, functional test cases and performance/security checks are documented in
[Performance Testing](../6.%20Project%20Testing/Performance%20Testing.md). Example: inputs
N=90, P=42, K=43, temp=20.8, humidity=82, pH=6.5, rainfall=202 → recommends **rice**.

## 14. Future Enhancements

Fertiliser/yield prediction, live weather API auto-fill, Postgres, more crops, mobile and
multi-language support — see
[Scalability & Future Plan](../8.%20Project%20Demonstration/Scalability%20%26%20Future%20Plan.md).

## 15. Team

| Name | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |
