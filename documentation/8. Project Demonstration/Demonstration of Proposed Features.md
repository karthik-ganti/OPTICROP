# Demonstration of Proposed Features

> **Project:** OptiCrop — Smart Agricultural Production Optimization Engine
>
> **Phase 8 — Project Demonstration**

| Team Member | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |

---

## Features Demonstrated

| # | Feature | How it is Shown | Status |
|---|---|---|---|
| 1 | Crop recommendation | Enter 7 inputs on *Find Your Crop* → best crop on *Result* | ✅ Implemented |
| 2 | Confidence score | Confidence badge on the result page | ✅ Implemented |
| 3 | Top-3 alternatives | Progress bars for the next two crops | ✅ Implemented |
| 4 | Agronomic guidance | Crop type, season, optimal pH, water need, tip | ✅ Implemented |
| 5 | User registration | Create a new account live | ✅ Implemented |
| 6 | Login / logout | Authenticated session, protected routes | ✅ Implemented |
| 7 | Prediction history | *History* page lists past predictions | ✅ Implemented |
| 8 | Input validation | Enter invalid data → friendly error | ✅ Implemented |
| 9 | Model accuracy display | Home/About show 99.55% Random Forest | ✅ Implemented |
| 10 | Multi-model training | Show `model_comparison.png` | ✅ Implemented |
| 11 | Graceful no-model mode | Predict before training → "train model" message | ✅ Implemented |

## Walkthrough Scenarios

### Scenario A — Happy Path
1. Log in as a demo farmer.
2. Enter N=90, P=42, K=43, temp=20.8, humidity=82, pH=6.5, rainfall=202.
3. **Result:** *rice* 🌾 with confidence, top-3 alternatives, and agronomic tips.
4. Open **History** — the prediction is saved.

### Scenario B — Validation
1. Leave a field blank or enter text.
2. Client-side validation blocks submission; server-side guard flashes an error.

### Scenario C — Alternatives Matter
1. Enter values near a class boundary.
2. Show how confidence drops and the top-3 alternatives become closer — reinforcing why
   confidence + alternatives are shown instead of a single label.

## Evidence Artifacts

- `static/images/model_comparison.png` — accuracy of the four models.
- `static/images/elbow_plot.png` — K-Means elbow analysis.
- `models/metrics.txt` — deployed algorithm and accuracy.
- Live app screens: Home, Find Your Crop, Result, History.
