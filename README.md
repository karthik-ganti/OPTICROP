# 🌱 OptiCrop — Smart Agricultural Production Optimization Engine

OptiCrop is a machine-learning web application that recommends the most
suitable crop for a plot of land from its soil and climate parameters —
**Nitrogen (N), Phosphorus (P), Potassium (K), temperature, humidity, pH,
and rainfall**. It pairs a scikit-learn classifier with a Flask web app,
user accounts, and a searchable prediction history.

## Features

- **Smart crop recommendation** from 7 soil/climate inputs (22 possible crops).
- **Model comparison** — KNN, Logistic Regression, Decision Tree and Random
  Forest are trained and compared; the best is deployed. A K-Means elbow
  analysis is included for exploratory clustering.
- **Accounts & history** — register/login (Flask-Login); every prediction is
  saved and viewable per user.
- **Agronomic guidance** — each recommendation is enriched with the crop's
  season, optimal pH, water need and a practical tip.

## Tech stack

Flask · Flask-SQLAlchemy · Flask-Login · scikit-learn · pandas · NumPy ·
matplotlib/seaborn · Bootstrap 5 · SQLite.

## Project structure

```
OptiCrop/
├── app.py                 # Flask app: routes, auth, inference, persistence
├── models_db.py           # SQLAlchemy models (User, SoilData, Crop, MLModel, Prediction)
├── crop_data.py           # 22-crop agronomic reference metadata
├── train_model.py         # training pipeline -> models/model.pkl + scaler.pkl
├── requirements.txt
├── dataset/
│   └── Crop_recommendation.csv
├── models/                # model.pkl, scaler.pkl, metrics.txt (generated)
├── notebooks/
│   └── opticrop_model.ipynb
├── static/  (css, js, images)
└── templates/  (home, about, findyourcrop, result, history, login, register)
```

## Setup & run

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model (reads dataset/Crop_recommendation.csv)
python train_model.py

# 4. Run the app
python app.py
```

Then open **http://localhost:5000**. Register an account, go to
**FindYourCrop**, enter soil/climate values, and get a recommendation.

> The app boots even before the model is trained — the prediction pages simply
> show a "model not trained yet" message until `models/model.pkl` exists.

## Example input (recommends *rice*)

`N=90, P=42, K=43, temperature=20.8, humidity=82, pH=6.5, rainfall=202`

## Data model ↔ ER diagram

Five tables carry the data flow: **User → SoilData → Prediction ← MLModel**,
with a **Crop** reference table (22 crops) linked from Prediction. The ER
diagram's **Dataset** and **Report** entities are represented by the CSV +
`MLModel.model_file` and by the result/history views, respectively.

## Dataset

`Crop_recommendation.csv` (Kaggle — *Smart Agricultural Production Optimizing
Engine*): 2,200 rows, columns `N, P, K, temperature, humidity, ph, rainfall,
label`, with 22 crop classes.
