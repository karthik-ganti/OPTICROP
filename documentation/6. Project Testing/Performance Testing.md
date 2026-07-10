# Performance Testing

> **Project:** OptiCrop — Smart Agricultural Production Optimization Engine
>
> **Phase 6 — Project Testing**

| Team Member | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |

---

## Model Performance

Four classifiers were trained on an 80/20 stratified split and compared by test accuracy. The
best model (Random Forest) is deployed.

| Model | Test Accuracy |
|---|---|
| **Random Forest** ✅ (deployed) | **99.55%** |
| Decision Tree | high (≈ 98%) |
| K-Nearest Neighbours | high (≈ 97%) |
| Logistic Regression | good (≈ 95%) |

> Exact values are produced by `train_model.py` and visualised in
> `static/images/model_comparison.png`. The deployed figures are recorded in
> `models/metrics.txt` (`algorithm=Random Forest`, `accuracy=99.55`) and surfaced on the Home/About pages.

- **Dataset:** 2,200 rows, 22 balanced crop classes.
- **Evaluation:** accuracy on the held-out 20% test set; K-Means elbow analysis (k=1..10) used only
  for exploratory clustering (`static/images/elbow_plot.png`).

## Functional Test Cases

| # | Test | Input | Expected | Result |
|---|---|---|---|---|
| T1 | Valid prediction | N=90, P=42, K=43, temp=20.8, humidity=82, pH=6.5, rainfall=202 | Recommends **rice** with confidence + top-3 | ✅ Pass |
| T2 | Non-numeric input | letters in a field | Friendly "enter valid numeric values" flash | ✅ Pass |
| T3 | Missing field | one field left blank | Validation blocks submit (client + server) | ✅ Pass |
| T4 | Unauthenticated access | open `/findyourcrop` while logged out | Redirect to login | ✅ Pass |
| T5 | Register duplicate email | existing email | Rejected as already registered | ✅ Pass |
| T6 | Login wrong password | valid email, wrong password | Login denied with message | ✅ Pass |
| T7 | History persistence | run prediction, open `/history` | Prediction appears in the list | ✅ Pass |
| T8 | No-model boot | start app before training | App boots; predict flashes "model not trained" | ✅ Pass |
| T9 | Unknown crop metadata | label not in `CROP_INFO` | Safe default metadata returned (no crash) | ✅ Pass |

## Performance / Load Notes

| Aspect | Observation |
|---|---|
| Inference latency | Single prediction is near-instant (small model, in-memory). |
| Model load | `model.pkl` + `scaler.pkl` loaded once at boot, not per request. |
| Concurrency | gunicorn `--workers 1 --threads 4` handles concurrent requests within free-tier RAM. |
| Memory footprint | Single worker keeps one copy of sklearn + model, staying under Render's 512 MB free tier. |
| Timeout | gunicorn `--timeout 120` guards against slow cold requests. |

## Security Checks

- Passwords stored only as Werkzeug hashes (verified — no plaintext in DB).
- Emails normalised to lowercase to prevent duplicate accounts.
- Protected routes enforce `@login_required`.
- `SECRET_KEY` overridable via env var (auto-generated on Render).
