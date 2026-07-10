# Customer Journey Map

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

## Persona

**Ravi — smallholder farmer** with a recent soil-test report, deciding this season's crop.

## Journey Stages

| Stage | User Goal | User Action | Touchpoint | Emotion | System Response |
|---|---|---|---|---|---|
| 1. Discover | Find help choosing a crop | Opens OptiCrop, reads Home/About | `/`, `/about` | 🙂 Curious | Explains the tool + shows model accuracy |
| 2. Sign up | Get a personal account | Registers with name/email/password | `/register` | 🙂 Willing | Creates account, logs in |
| 3. Input | Provide plot data | Enters N, P, K, temp, humidity, pH, rainfall | `/findyourcrop` | 🤔 Focused | Validates each field with hints |
| 4. Get result | Know what to plant | Submits form | `/predict` → `/result` | 😀 Relieved | Best crop + confidence + top-3 + tips |
| 5. Understand | Judge the advice | Reads crop type, season, pH, water need, tip | `/result` | 🙂 Confident | Plain-language agronomic guidance |
| 6. Revisit | Track past decisions | Opens history | `/history` | 🙂 Reassured | Lists all past predictions |
| 7. Act | Plant with confidence | Uses the recommendation in the field | offline | 😀 Empowered | — |

## Pain Points → Solutions

| Pain Point | OptiCrop Solution |
|---|---|
| "I don't know which crop fits my numbers." | Instant ML recommendation from the 7 inputs. |
| "One answer isn't enough to trust." | Confidence score + top-3 alternatives. |
| "The recommendation lacks context." | Agronomic tips: season, optimal pH, water need. |
| "I can't remember past results." | Saved, per-user prediction history. |
| "Tools are hard to use." | Simple guided form with min/max hints, responsive UI. |

## Moments of Truth

- **First recommendation (Stage 4):** the confidence score and matching alternatives determine
  whether the user trusts the tool.
- **Guidance clarity (Stage 5):** plain-language tips convert a raw label into an actionable decision.
