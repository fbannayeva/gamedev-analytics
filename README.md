# Shadow Realm: Player Analytics
### Case · Mobile GameDev Data Analyst (Middle)

---

## Overview

End-to-end analytics project for a fictional mobile idle RPG. The goal is to surface actionable insights across **retention**, **monetisation**, and **A/B testing** using a synthetic but realistic dataset of 50,000 players over 90 days.

This project demonstrates the full analyst workflow:
```
Data Generation → SQL Queries → Python EDA → Statistical Testing → Business Recommendations
```

---

## Dataset

| Table | Rows | Description |
|-------|------|-------------|
| `players.csv` | 50,000 | One row per player: install date, platform, country, UA channel, player class, A/B group, retention flags (D1/D7/D30), total revenue, payer flag |
| `sessions.csv` | ~71,000 | Individual gameplay sessions with start time and duration |
| `purchases.csv` | ~1,400 | In-app purchases with item name and USD amount |

**Time range**: 2024-01-01 → 2024-03-31  
**Platforms**: iOS, Android  
**Countries**: US, DE, JP, BR, KR, FR, GB, RU, CN, CA

---

## Project Structure
```
gamedev-analytics/
├── data/
│   ├── generate_data.py      # Reproducible synthetic data generator
│   ├── players.csv
│   ├── sessions.csv
│   └── purchases.csv
├── notebooks/
│   └── shadow_realm_analysis.ipynb   # Main EDA notebook
├── sql/
│   └── queries.sql           # 8 production-ready SQL queries
├── dashboard/
│   └── tableau_guide.md      # Tableau Public dashboard spec
├── assets/                   # Auto-generated charts
│   ├── retention.png
│   ├── revenue.png
│   ├── ab_test.png
│   ├── funnel.png
│   └── sessions.png
└── README.md
```

---

## Analysis Modules

### 1 · Retention Funnel
- D1 / D7 / D30 retention rates vs industry benchmarks
- Weekly cohort heatmap to identify seasonal or product-driven changes

![Retention](/retention.png)

### 2 · Revenue & ARPU
- Total revenue and ARPU broken down by country and platform
- US leads on total revenue; DE, FR, CN, RU lead on ARPU per player
- iOS vs Android monetisation comparison

![Revenue](/revenue.png)

### 3 · A/B Test — New Onboarding Flow
- Two-proportion z-test (one-sided, α = 0.05)
- Tests whether `variant_a` significantly improves D1, D7, D30 retention
- Includes relative uplift and statistical significance flag

![A/B Test](/ab_test.png)

### 4 · Payer Conversion Funnel
- Install → D1 Active → D7 Active → D30 Active → Payer
- Absolute counts and conversion rates at each stage

![Funnel](/funnel.png)

### 5 · Session Engagement by Player Class
- Average session duration and sessions-per-player by character class
- Session duration is nearly identical across classes (5.55–5.63 min)
- Paladin and Warrior lead on sessions per player (9.16 and 9.26)

![Sessions](/sessions.png)

---

## Key Findings

| # | Finding | Recommendation |
|---|---------|----------------|
| 1 | **D1 retention ~38%** — below the RPG benchmark of 40-45% | Simplify tutorial; add a Day 1 login reward |
| 2 | **DE, FR, CN, RU** have the highest ARPU (USD 0.34-0.36) but are underleveraged | Shift a portion of UA budget from CA toward DE and FR |
| 3 | **GB** has the lowest ARPU (USD 0.18) despite a solid player base | Investigate whether the monetisation offer fits this market |
| 4 | **Variant A** lifts D1 +8pp and D7 +2pp (both p < 0.05) | Roll out to 100%; monitor D30 for 30 more days |
| 5 | **Payer CVR ~1%** — below F2P RPG benchmark of 2-5% | Add a soft-paywall starter pack offer on Day 3 |
| 6 | **Session duration identical** across all classes (5.55-5.63 min) | No class-based session targeting needed |
| 7 | **Paladin and Warrior** have the highest sessions per player (9.16 and 9.26) | Feature Paladin and Warrior in store banners and push campaigns |

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Data generation, EDA, visualisation |
| pandas / numpy | Data manipulation |
| matplotlib | Charts |
| scipy.stats | A/B test (two-proportion z-test) |
| SQL (SQLite dialect) | Aggregations, cohort analysis, funnel |
| Tableau Public | Interactive dashboard |

---

## How to Run
```bash
# 1. Clone the repo
git clone https://github.com/<your-handle>/gamedev-analytics.git
cd gamedev-analytics

# 2. Install dependencies
pip install pandas numpy matplotlib scipy jupyter

# 3. (Optional) Regenerate data
python data/generate_data.py

# 4. Open the notebook
jupyter notebook notebooks/shadow_realm_analysis.ipynb
```

---

## SQL Queries Included

1. DAU / WAU / MAU with rolling averages  
2. Retention cohorts by install week  
3. Revenue & ARPU by country and platform  
4. A/B test summary  
5. Payer conversion funnel  
6. Session quality by player class  
7. Daily revenue time-series with 7-day MA  
8. Top spender leaderboard (whale analysis)  

---

## Tableau Dashboard

See [`dashboard/tableau_guide.md`](https://github.com/fbannayeva/gamedev-analytics/blob/main/tableau_guide.md) for full instructions on building a 4-sheet interactive Tableau Public dashboard from this data.

**Live Dashboard:**
[View on Tableau Public](https://public.tableau.com/app/profile/fidan.bannayeva/viz/MobileGamePlayerAnalyticsDashboard/Dashboard1?publish=yes)
---

## Author

**Fidan Bannayeva** 
[LinkedIn](https://linkedin.com/in/fbannayeva) 