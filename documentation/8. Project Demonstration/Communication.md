# Communication

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

## Communication Plan

### Internal (within the team)
- **Coordination:** led by the Team Lead (Vaddimani Nikitha Sai); tasks assigned per member's
  area of ownership (see [Project Planning](../4.%20Project%20Planning%20Phase/Project%20Planning.md)).
- **Version control:** Git — all code and documentation committed to the project repository.
- **Sync-ups:** regular stand-ups to review progress against sprints and unblock issues.

### Demonstration (to the audience / evaluators)

A clear narrative arc for the presentation:

| Segment | Message | Speaker |
|---|---|---|
| Problem | Farmers struggle to pick the right crop from soil/climate data | Team Lead |
| Solution | OptiCrop turns 7 inputs into a confident recommendation | Team Lead |
| Data & Model | 2,200-row dataset; Random Forest at 99.55% | Model owner |
| Live Demo | Prediction, confidence, alternatives, tips, history | App owner(s) |
| Impact & Future | Yield optimisation, reduced waste; roadmap | Team Lead |

## Elevator Pitch

> "OptiCrop is a smart agricultural engine that recommends the best crop for a farmer's land.
> Enter your soil's N, P, K and pH plus local temperature, humidity and rainfall, and our Random
> Forest model — 99.55% accurate — instantly returns the most suitable crop, a confidence score,
> alternative options, and practical growing tips. Accounts and history let farmers track and
> compare decisions over time."

## Key Talking Points

- **Trust:** we surface confidence + top-3 alternatives, not a single opaque label.
- **Actionability:** every result includes agronomic guidance (season, pH, water need, tips).
- **Engineering:** shared feature-order contract avoids train/serve skew; graceful no-model boot.
- **Accessibility:** clean responsive UI; deployed on a free cloud tier.

## Q&A Preparation

| Likely Question | Prepared Answer |
|---|---|
| How accurate is it? | 99.55% test accuracy (Random Forest), best of four compared models. |
| Why these 7 inputs? | They are the standard, measurable soil + climate drivers of crop suitability. |
| What if the model is wrong? | Confidence + alternatives let the user judge; guidance is indicative. |
| Can it scale? | Stateless inference; SQLite → Postgres via `DATABASE_URL`; horizontally scalable web tier. |
| Is it secure? | Passwords hashed (Werkzeug); protected routes; configurable secret key. |
