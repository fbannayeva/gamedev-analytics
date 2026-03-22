# Tableau Public Dashboard Guide
## Shadow Realm: MobileGame Player Analytics Dashboard

---

## Data Sources

- Connect `players.csv` as the main data source
- Connect `purchases.csv` as a second data source
- Both files linked on `player_id`

---

## Sheet 1 · Retention Rates

**Steps:**
1. Drag `D1 Retained`, `D7 Retained`, `D30 Retained` to Rows
2. Right-click each pill → Measure → Average
3. Format Y axis → Numbers → Percentage → Decimal 1
4. Drag `Ab Group` to Color in Marks card
5. In Marks card click Label → Show Mark Labels

**Result:** Vertical bar chart showing D1 ~38%, D7 ~15%, D30 ~5%

---

## Sheet 2 · Revenue & ARPU by Country

**Steps:**
1. Drag `Country` to Columns
2. Drag `Amount Usd` to Rows — keeps SUM
3. Format Y axis → Numbers → Currency → USD
4. Sort by descending revenue

**Add ARPU calculated field:**
- Analysis → Create Calculated Field
- Name: `ARPU`
- Formula: `SUM([Amount Usd]) / COUNT([Player Id])`
- Drag `ARPU` to Rows next to SUM(Amount Usd)

**Result:** Two bar charts side by side — Total Revenue and ARPU by country.
US leads on revenue. DE, FR, CN, RU lead on ARPU.

---

## Sheet 3 · A/B Test

**Steps:**
1. Drag `Ab Group` to Columns
2. Drag `Measure Names` to Columns next to Ab Group
3. Drag `Measure Values` to Rows
4. In Measure Values card keep only:
   - AVG(D1 Retained)
   - AVG(D7 Retained)
   - AVG(D30 Retained)
5. Move `Measure Names` to the left of `Ab Group` in Columns
6. Drag `Ab Group` to Color in Marks card
7. Format Y axis → Numbers → Percentage → Decimal 1
8. Worksheet → Show Title → rename to `A/B Test — Onboarding Flow`
9. Marks → Label → Show Mark Labels

**Result:** Three pairs of bars — Control vs Variant A for D1, D7, D30.
Variant A shows higher retention across all three metrics.

---

## Dashboard Assembly

1. Bottom panel click + → New Dashboard
2. Size → Fixed → Desktop Browser (1000 x 800)
3. Drag sheets onto canvas:
   - Retention → top left
   - Revenue → top right
   - A/B Test → bottom full width
4. Objects → Text → drag to top → add title:
   `Shadow Realm: MobileGame Player Analytics Dashboard`

---

## Publishing

1. File → Save to Tableau Public As
2. Name: `Shadow Realm MobileGame Analytics`
3. Save → browser opens with your live dashboard
4. Copy the URL and add it to README and LinkedIn

**Live Dashboard:** [View on Tableau Public](https://public.tableau.com/app/profile/fidan.bannayeva/viz/MobileGamePlayerAnalyticsDashboard/Dashboard1?publish=yes)

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
Feel free to use, modify, and distribute this work.

**Author:** 
Fidan Bannayeva — [LinkedIn](https://www.linkedin.com/in/fbannayeva)
