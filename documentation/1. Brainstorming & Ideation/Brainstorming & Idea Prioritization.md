# Brainstorming & Idea Prioritization

> **Project:** OptiCrop — Smart Agricultural Production Optimization Engine
>
> **Phase 1 — Brainstorming & Ideation**

| Team Member | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |

---

## Brainstormed Ideas

Each team member contributed ideas around the problem "help farmers pick the right crop from
soil and climate data".

| # | Idea | Contributor focus |
|---|---|---|
| 1 | ML model that recommends a crop from N, P, K, temperature, humidity, pH, rainfall | Core concept |
| 2 | Web app with a simple 7-field form for non-technical users | UX |
| 3 | Show a **confidence score** and **top-3 alternative** crops, not just one answer | Trust / usability |
| 4 | Enrich each recommendation with agronomic tips (season, optimal pH, water need) | Value add |
| 5 | User accounts so each farmer can save and review prediction **history** | Retention |
| 6 | Compare multiple ML algorithms and deploy the most accurate one | Model quality |
| 7 | Fertiliser dosage / yield-quantity prediction | Stretch idea |
| 8 | Real-time weather API auto-fill for climate fields | Stretch idea |
| 9 | Mobile app / regional-language support | Future idea |
| 10 | Deploy on a free cloud tier for public access | Delivery |

## Prioritization (Impact vs. Effort)

| Idea | Impact | Effort | Decision |
|---|---|---|---|
| 1 — Crop recommendation model | High | Medium | ✅ Core (must-have) |
| 2 — Simple web form | High | Low | ✅ Core |
| 3 — Confidence + top-3 | High | Low | ✅ Core |
| 4 — Agronomic tips | Medium | Low | ✅ Core |
| 5 — Accounts + history | Medium | Medium | ✅ Included |
| 6 — Multi-model comparison | High | Medium | ✅ Included |
| 10 — Free-tier deployment | Medium | Low | ✅ Included |
| 7 — Fertiliser/yield prediction | Medium | High | ⏳ Future |
| 8 — Weather API auto-fill | Medium | High | ⏳ Future |
| 9 — Mobile / multi-language | Medium | High | ⏳ Future |

## Prioritized Scope (MVP)

The team converged on OptiCrop's MVP:

1. Train and compare four classifiers (KNN, Logistic Regression, Decision Tree, Random Forest)
   on the Crop Recommendation dataset; deploy the best (Random Forest, 99.55%).
2. A Flask web app with a 7-field prediction form.
3. Recommendation output = best crop + confidence + top-3 alternatives + agronomic tips.
4. User registration/login and per-user prediction history.
5. Free-tier cloud deployment (Render).

Stretch ideas (fertiliser/yield prediction, weather auto-fill, mobile, multi-language) are
recorded in the [Scalability & Future Plan](../8.%20Project%20Demonstration/Scalability%20%26%20Future%20Plan.md).
