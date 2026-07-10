# Scalability & Future Plan

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

## Current Scalability Design

| Aspect | Design | Benefit |
|---|---|---|
| Stateless inference | Prediction depends only on request + in-memory model | Easy horizontal scaling of web tier |
| Configurable DB | `DATABASE_URL` env var | Swap SQLite → Postgres without code changes |
| One-time model load | `model.pkl` + `scaler.pkl` loaded at boot | No per-request disk I/O |
| Free-tier friendly | gunicorn 1 worker + 4 threads | Fits 512 MB while serving concurrent users |
| Small artifacts | Compact pickled model | Fast startup and low memory |

## Scaling Path

1. **Database:** migrate SQLite → managed Postgres for concurrent writes and durability.
2. **Web tier:** increase gunicorn workers on a larger instance; run multiple app replicas behind
   a load balancer.
3. **Caching:** cache reference/crop metadata; optional CDN for static assets.
4. **Model serving:** move inference to a dedicated model service / batch endpoint if load grows.

## Future Enhancements

| Priority | Enhancement | Value |
|---|---|---|
| High | Fertiliser dosage & expected-yield prediction | Deeper decision support beyond crop choice |
| High | Live weather API auto-fill (temperature, humidity, rainfall) | Fewer manual inputs, fresher data |
| Medium | More crops & regional datasets | Broader geographic applicability |
| Medium | Regional-language support | Reach non-English-speaking farmers |
| Medium | Mobile app (PWA / native) | Field usability, offline access |
| Medium | Explainability (feature importance per prediction) | Show *why* a crop was recommended |
| Low | Admin dashboard & analytics | Track usage and model drift |
| Low | Periodic model retraining pipeline | Keep accuracy current as data grows |

## Sustainability

- **Reproducibility:** dataset + model artifacts + one-command training are version-controlled.
- **Maintainability:** clear module separation and shared feature contract ease future changes.
- **Extensibility:** new crops require only dataset + `crop_data.py` metadata additions and retraining.
