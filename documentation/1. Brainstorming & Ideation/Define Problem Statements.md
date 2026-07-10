# Define Problem Statements

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

## Background

Choosing what to grow is one of the highest-stakes decisions a farmer makes each season. In
practice the choice is often driven by habit, neighbours' choices, or market rumour rather than
by the actual soil chemistry and local climate of the plot. A poor match between crop and land
leads to low yield, wasted fertiliser and water, and financial loss.

Soil-test reports do exist (N, P, K, pH), and weather data (temperature, humidity, rainfall) is
available — but connecting those numbers to a concrete "grow *this* crop" recommendation requires
agronomic expertise that most smallholder farmers cannot easily access.

## Problem Statement

> Farmers and agricultural advisors lack a fast, data-driven way to translate a plot's soil
> nutrient levels (N, P, K, pH) and climate conditions (temperature, humidity, rainfall) into a
> confident, specific crop recommendation. As a result, crop selection is guess-driven, leading
> to sub-optimal yield, wasted inputs and avoidable losses.

## Problem Statement Cards

| # | I am… | I'm trying to… | But… | Because… | Which makes me feel… |
|---|---|---|---|---|---|
| PS-1 | A smallholder farmer | Decide which crop to plant this season | I don't know which crop truly fits my soil and weather | Interpreting a soil report against climate needs expertise | Anxious about wasting a whole season |
| PS-2 | An agri-extension officer | Advise many farmers quickly | Manual, case-by-case analysis is slow and inconsistent | I have no tool to standardise recommendations | Overloaded and unable to scale my help |
| PS-3 | A new / hobby farmer | Learn what grows well on my land | Agronomy knowledge is scattered and technical | There is no simple guided input-to-answer tool | Discouraged from starting |

## Who is affected

- **Primary:** smallholder and individual farmers deciding seasonal crops.
- **Secondary:** agricultural extension officers and advisors who guide many farmers.
- **Tertiary:** agri-tech students and educators learning applied ML for agriculture.

## Goal

Deliver a simple web tool where a user enters seven measurable values and instantly receives the
best-matched crop (with a confidence score and top alternatives), enriched with practical
agronomic guidance — turning raw soil/climate numbers into an actionable decision.
