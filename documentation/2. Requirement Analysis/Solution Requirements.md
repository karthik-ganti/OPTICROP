# Solution Requirements

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

## Functional Requirements

| ID | Requirement | Description |
|---|---|---|
| FR-1 | User Registration | Create an account with name, email (unique) and password; role defaults to *Farmer*. |
| FR-2 | User Login / Logout | Authenticate with email + password; session managed via Flask-Login. |
| FR-3 | Soil & Climate Input | Enter 7 values — N, P, K, temperature, humidity, pH, rainfall — via a guided form. |
| FR-4 | Input Validation | Reject non-numeric / out-of-range values on both client and server sides. |
| FR-5 | Crop Prediction | Predict the best-fit crop from the 7 inputs using the trained model. |
| FR-6 | Confidence & Alternatives | Show the recommended crop's confidence score and the top-3 alternative crops. |
| FR-7 | Agronomic Guidance | Show crop type, season, optimal pH, water need and a practical tip for the result. |
| FR-8 | Persist Predictions | Save each prediction (inputs + result) linked to the logged-in user. |
| FR-9 | Prediction History | List a user's past predictions with inputs, result and confidence. |
| FR-10 | Informational Pages | Home and About pages describing the app and current model accuracy. |

## Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-1 | Accuracy | Deployed model achieves high test accuracy (Random Forest, 99.55%). |
| NFR-2 | Security | Passwords stored only as Werkzeug hashes; emails normalised to lowercase; `SECRET_KEY` configurable. |
| NFR-3 | Usability | Clean, responsive Bootstrap 5 UI usable on mobile browsers; clear input hints. |
| NFR-4 | Performance | Single prediction returns near-instantly; model + scaler loaded once at boot. |
| NFR-5 | Resource footprint | Runs within a 512 MB free tier (gunicorn: 1 worker, 4 threads). |
| NFR-6 | Reliability | App boots even before a model is trained, flashing a clear "model not trained" message. |
| NFR-7 | Portability | Configurable via env vars (`SECRET_KEY`, `DATABASE_URL`, `PORT`); deployable to Render. |
| NFR-8 | Reproducibility | Dataset and trained model artifacts tracked in git; one-command training script. |

## Constraints & Assumptions

- **Inputs:** the model expects exactly the 7 features in a fixed order
  (`N, P, K, temperature, humidity, ph, rainfall`); the same order is used at train and serve time.
- **Output space:** 22 crop classes only (see the dataset's `label` column).
- **Data source:** the public *Crop Recommendation* dataset (2,200 balanced rows, 22 classes).
- **Guidance is indicative:** agronomic tips are general reference, not exact field prescriptions.
- **Prerequisite:** `python train_model.py` must be run before predictions are available.
