# Project Demo Planning

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

## Demo Objective

Show, end-to-end, how OptiCrop turns raw soil/climate numbers into a trustworthy crop
recommendation — from problem to model to live app.

## Pre-Demo Checklist

- [ ] `pip install -r requirements.txt` completed in a fresh venv.
- [ ] `python train_model.py` run — confirm `models/model.pkl`, `scaler.pkl`, `metrics.txt` exist.
- [ ] `python app.py` running at http://localhost:5000 (or live Render URL open).
- [ ] A demo account created (or ready to register live).
- [ ] Sample input values ready (see below).
- [ ] `static/images/model_comparison.png` and `elbow_plot.png` available to show.

## Demo Flow (≈ 6–8 minutes)

| Step | Action | What to Highlight |
|---|---|---|
| 1 | Open Home / About | Problem statement + live model accuracy (99.55%) |
| 2 | Register / Login | Account creation, secure password hashing |
| 3 | Find Your Crop | Enter 7 inputs with guided validation |
| 4 | Submit → Result | Recommended crop + confidence + top-3 + agronomic tips |
| 5 | Second prediction | Try different values to show the model responds |
| 6 | History | Show saved past predictions per user |
| 7 | Behind the scenes | Model comparison plot + training pipeline overview |

## Sample Demo Inputs

| N | P | K | Temperature | Humidity | pH | Rainfall | Expected |
|---|---|---|---|---|---|---|---|
| 90 | 42 | 43 | 20.8 | 82 | 6.5 | 202 | **rice** 🌾 |

## Roles During Demo

| Member | Demo Role |
|---|---|
| Vaddimani Nikitha Sai (Lead) | Introduction, problem statement, wrap-up & Q&A |
| Ramavenkata Manideep Gokarakonda | Dataset, model training & comparison walkthrough |
| Kavya Kallapalli | Live prediction flow (Find Your Crop → Result) |
| Samikeri Rama Pallavi | Auth & history demonstration |
| S K R S Sai Prakash Nidadavolu | UI/UX, agronomic guidance, validation |

## Fallback Plan

- If live model is missing, show the graceful "model not trained" message, then run
  `train_model.py` live or use a pre-recorded clip.
- If cloud is down, demo the local instance.
