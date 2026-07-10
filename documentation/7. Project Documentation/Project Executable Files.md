# Project Executable Files

> **Project:** OptiCrop — Smart Agricultural Production Optimization Engine
>
> **Phase 7 — Project Documentation**

| Team Member | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |

---

## File Inventory

```
OptiCrop/
├── app.py                       # Flask app: routes, auth, inference, persistence, seeding
├── models_db.py                 # SQLAlchemy models (User, SoilData, Crop, MLModel, Prediction)
├── crop_data.py                 # 22-crop agronomic metadata + get_crop_info()
├── train_model.py               # Training pipeline: clean → split → scale → train → save
├── requirements.txt             # Python dependencies
├── Procfile                     # gunicorn start command (production)
├── render.yaml                  # Render.com Blueprint deploy config
├── README.md                    # Top-level project readme
├── dataset/
│   └── Crop_recommendation.csv  # 2,200 rows, 22 crop classes
├── models/                      # Generated ML artifacts (tracked)
│   ├── model.pkl                # Deployed Random Forest classifier
│   ├── scaler.pkl               # Fitted StandardScaler
│   └── metrics.txt              # algorithm + accuracy
├── notebooks/
│   └── opticrop_model.ipynb     # EDA + modelling notebook
├── static/
│   ├── css/main.css             # Custom oc-* styling
│   ├── js/main.js               # Client validation + animated stats
│   └── images/                  # elbow_plot.png, model_comparison.png
├── templates/                   # 8 Jinja2 pages (base, home, about, login, register,
│                                #   findyourcrop, result, history)
└── documentation/               # This 8-phase documentation
```

## Executable Entry Points

| Command | Purpose |
|---|---|
| `python train_model.py` | Train & compare models, write `models/model.pkl`, `scaler.pkl`, `metrics.txt`, plots |
| `python app.py` | Run the Flask dev server (reads `PORT`, default 5000) |
| `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120` | Production server (from `Procfile`) |

## How to Run Locally

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train_model.py        # generates models/model.pkl + scaler.pkl
python app.py                # open http://localhost:5000
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train_model.py
python app.py
```

> **Note:** the app boots even without a trained model, but predictions require running
> `train_model.py` first (it creates `models/model.pkl` and `models/scaler.pkl`).

## Deployment (Render)

- `render.yaml` defines a free-plan web service: `buildCommand: pip install -r requirements.txt`,
  gunicorn start command, `PYTHON_VERSION=3.12.4`, and an auto-generated `SECRET_KEY`.
- Single worker + 4 threads chosen deliberately to fit the 512 MB free tier.
