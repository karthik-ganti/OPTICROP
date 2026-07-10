# Proposed Solution

> **Project:** OptiCrop — Smart Agricultural Production Optimization Engine
>
> **Phase 3 — Project Design Phase**

| Team Member | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |

---

| # | Parameter | Description |
|---|---|---|
| 1 | **Problem Statement** | Farmers lack a fast, data-driven way to turn soil (N, P, K, pH) and climate (temperature, humidity, rainfall) readings into a confident crop choice. |
| 2 | **Idea / Solution** | OptiCrop — an ML web app that recommends the best crop from 7 inputs, with a confidence score, top-3 alternatives and agronomic tips. |
| 3 | **Novelty / Uniqueness** | Combines a high-accuracy multi-model comparison (99.55% Random Forest) with plain-language agronomic enrichment and per-user history — not just a bare label. |
| 4 | **Social Impact** | Helps optimise yield and reduce wasted water/fertiliser; democratises agronomic guidance for smallholders. |
| 5 | **Business Model** | Free, open, education/impact-oriented tool; deployable on a free cloud tier. Extensible to advisory-service or agri-input partnerships. |
| 6 | **Scalability** | Stateless prediction; SQLite → Postgres via `DATABASE_URL`; horizontally scalable web tier; model artifact is small and loaded once. |

## Solution Summary

A logged-in user enters seven measured values on the **Find Your Crop** page. The backend scales
the inputs with the same `StandardScaler` used at training time, runs the pickled Random Forest's
`predict_proba`, and returns the highest-probability crop as the recommendation together with the
next two as alternatives and a confidence percentage. The result is enriched with agronomic
metadata (type, season, optimal pH, water need, tip) from the seeded `Crop` table, saved to the
user's history, and displayed on a clean Bootstrap result page.

## Key Design Decisions

- **Random Forest deployed** after comparing KNN, Logistic Regression and Decision Tree — best
  accuracy on the held-out test set.
- **Fixed feature order contract** shared between training and serving to prevent train/serve skew.
- **Model + scaler loaded once at boot** into module globals for fast inference.
- **Graceful degradation:** the app boots and runs even before a model exists, prompting training.
- **Single-worker gunicorn** to fit the 512 MB free tier while keeping concurrency via threads.
