# Functional Features

> **Project:** OptiCrop — Smart Agricultural Production Optimization Engine
>
> **Phase 5 — Project Development Phase**

| Team Member | Role |
|---|---|
| Vaddimani Nikitha Sai | Team Lead |
| Ramavenkata Manideep Gokarakonda | Member |
| Kavya Kallapalli | Member |
| Samikeri Rama Pallavi | Member |
| S K R S Sai Prakash Nidadavolu | Member |

---

## Functional Features Implemented

| # | Feature | Description |
|---|---|---|
| F1 | Crop Recommendation | Predicts the best crop from N, P, K, temperature, humidity, pH, rainfall. |
| F2 | Confidence Score | Shows the recommended crop's probability as a percentage. |
| F3 | Top-3 Alternatives | Lists the next two best-matching crops as progress bars. |
| F4 | Agronomic Guidance | Displays crop type, season, optimal pH, water need, emoji and a practical tip. |
| F5 | User Registration | Create an account (name, email, password); role defaults to *Farmer*. |
| F6 | Login / Logout | Session auth via Flask-Login with `?next=` redirect support. |
| F7 | Prediction History | Per-user list of all past predictions with inputs and results. |
| F8 | Input Validation | Client-side (JS) + server-side numeric/range checks with clear error messages. |
| F9 | Informational Pages | Home and About pages showing the live model accuracy/algorithm. |
| F10 | Multi-Model Training | Compares 4 classifiers and deploys the best (Random Forest). |
| F11 | Graceful No-Model Mode | App boots without a trained model and prompts the user to train it. |
| F12 | Animated Stats UI | Home-page stat counters animate into view (IntersectionObserver). |

## Application Routes

| Route | Methods | Auth | Purpose |
|---|---|---|---|
| `/` (`home`) | GET | Public | Landing page; shows model accuracy/algorithm |
| `/about` | GET | Public | About page |
| `/register` | GET, POST | Public | Create account |
| `/login` | GET, POST | Public | Log in (`?next=` supported) |
| `/logout` | GET | `@login_required` | Log out |
| `/findyourcrop` (`predict_form`) | GET | `@login_required` | Prediction input form |
| `/predict` | POST | `@login_required` | Run inference, persist, redirect to result |
| `/result` | GET | `@login_required` | Show recommendation (from session) |
| `/history` | GET | `@login_required` | User's past predictions |

## Feature-to-Requirement Traceability

| Feature | Requirement (see Phase 2) |
|---|---|
| F1–F4 | FR-5, FR-6, FR-7 |
| F5, F6 | FR-1, FR-2 |
| F7 | FR-8, FR-9 |
| F8 | FR-4 |
| F9 | FR-10 |
| F10 | NFR-1 |
| F11 | NFR-6 |
