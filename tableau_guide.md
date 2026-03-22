# Tableau Public Dashboard Guide
## Shadow Realm: Analytics Dashboard

This document describes how to build the 4-sheet interactive Tableau Public dashboard from the project CSVs.

---

## Data Sources

Connect all three CSVs as separate data sources. Create relationships:
- `players.csv` ← join on `player_id` → `sessions.csv`
- `players.csv` ← join on `player_id` → `purchases.csv`

---

## Sheet 1 · KPI Overview (Text Table + Scorecards)

**Calculated Fields to create:**

```
// D1 Retention Rate
SUM([D1 Retained]) / COUNT([Player Id])

// D7 Retention Rate
SUM([D7 Retained]) / COUNT([Player Id])

// D30 Retention Rate
SUM([D30 Retained]) / COUNT([Player Id])

// ARPU
SUM([Amount Usd]) / COUNTD([Player Id])

// Payer Conversion Rate
SUM([Is Payer]) / COUNT([Player Id])
```

**Layout**: 5 BANs (big-ass numbers) in a horizontal row:
- Total Players | D1 Ret % | D7 Ret % | ARPU | Payer CVR %

**Filters**: Platform, Country, AB Group (all as dashboard-level filters)

---

## Sheet 2 · Retention Cohort Heatmap

**Rows**: `DATETRUNC('week', [Install Date])` → formatted as `"Wk" + WEEK()`  
**Columns**: `D1 Retained`, `D7 Retained`, `D30 Retained` (separate calculated fields as %)  
**Mark type**: Square  
**Color**: `AVG([D1 Retained])` — use diverging Red-Yellow-Green  
**Label**: Show percentage on each cell  

This creates a classic cohort retention grid.

---

## Sheet 3 · Revenue Map

**Mark type**: Map  
**Rows/Cols**: Use built-in Latitude / Longitude (generated from Country)  
**Size**: `SUM([Amount Usd])`  
**Color**: `SUM([Amount Usd]) / COUNTD([Player Id])` (ARPU)  
**Tooltip**: Country, Total Revenue, ARPU, # Payers  

---

## Sheet 4 · A/B Test Bar Chart

**Rows**: `AB Group`  
**Columns**: 3 separate sheets side-by-side:
  1. D1 Retention %
  2. D7 Retention %
  3. D30 Retention %

Use dual-axis with a reference line at the control group value.

**Add annotation**: "★ Statistically significant (p < 0.05)" on the Variant A bars for D1 and D7.

---

## Dashboard Assembly

1. Create a new Dashboard (1400 × 900 px, fixed)
2. Add a title text box: "Shadow Realm: Idle RPG — Player Analytics Dashboard"
3. Top row: Sheet 1 (KPIs, full width)
4. Middle row: Sheet 3 (map, left 50%) + Sheet 2 (cohort heatmap, right 50%)
5. Bottom row: Sheet 4 (A/B test, full width)
6. Add Platform + Country + AB Group as filter controls (top right)
7. Apply filters to all sheets using "Apply to Worksheets → All Using This Data Source"

---

## Publishing to Tableau Public

1. File → Save to Tableau Public
2. Sign in / create free account
3. Name: `Shadow Realm Idle RPG Analytics`
4. Copy the public URL and add it to your README and LinkedIn
