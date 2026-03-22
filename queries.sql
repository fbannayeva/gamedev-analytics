-- ============================================================
--  Shadow Realm: Idle RPG  —  Analytics SQL Queries
--  Author : <your name>
--  Stack  : SQLite-compatible (also runs on BigQuery / Snowflake
--           with minor dialect tweaks)
-- ============================================================


-- ────────────────────────────────────────────────────────────
-- 1. DAU / WAU / MAU  (daily cohort aggregation)
-- ────────────────────────────────────────────────────────────
WITH daily_active AS (
    SELECT
        DATE(session_start)          AS activity_date,
        COUNT(DISTINCT player_id)    AS dau
    FROM sessions
    GROUP BY 1
)
SELECT
    activity_date,
    dau,
    AVG(dau) OVER (
        ORDER BY activity_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    )                                AS dau_7d_ma,
    SUM(dau) OVER (
        ORDER BY activity_date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    )                                AS mau_rolling
FROM daily_active
ORDER BY 1;


-- ────────────────────────────────────────────────────────────
-- 2. Retention Cohorts  (D1 / D7 / D30 by install week)
-- ────────────────────────────────────────────────────────────
SELECT
    strftime('%Y-W%W', install_date)   AS install_week,
    COUNT(*)                           AS cohort_size,
    ROUND(AVG(d1_retained)  * 100, 1) AS d1_pct,
    ROUND(AVG(d7_retained)  * 100, 1) AS d7_pct,
    ROUND(AVG(d30_retained) * 100, 1) AS d30_pct
FROM players
GROUP BY 1
ORDER BY 1;


-- ────────────────────────────────────────────────────────────
-- 3. Revenue Breakdown by Country & Platform
-- ────────────────────────────────────────────────────────────
SELECT
    country,
    platform,
    COUNT(DISTINCT player_id)                        AS total_players,
    SUM(amount_usd)                                  AS total_revenue,
    ROUND(SUM(amount_usd) / COUNT(DISTINCT player_id), 2)
                                                     AS arpu,
    COUNT(DISTINCT player_id) FILTER (WHERE amount_usd > 0)
                                                     AS payers,
    ROUND(
        100.0 * COUNT(DISTINCT player_id) FILTER (WHERE amount_usd > 0)
        / COUNT(DISTINCT player_id), 2
    )                                                AS conversion_pct
FROM (
    SELECT pl.player_id, pl.country, pl.platform, pu.amount_usd
    FROM players pl
    LEFT JOIN purchases pu USING (player_id)
) t
GROUP BY 1, 2
ORDER BY total_revenue DESC;


-- ────────────────────────────────────────────────────────────
-- 4. A/B Test — Onboarding Flow Impact on D1 & D7 Retention
-- ────────────────────────────────────────────────────────────
SELECT
    ab_group,
    COUNT(*)                           AS n,
    ROUND(AVG(d1_retained) * 100, 2)  AS d1_retention_pct,
    ROUND(AVG(d7_retained) * 100, 2)  AS d7_retention_pct,
    ROUND(AVG(d30_retained)* 100, 2)  AS d30_retention_pct,
    ROUND(AVG(total_revenue), 3)       AS avg_revenue
FROM players
GROUP BY 1;


-- ────────────────────────────────────────────────────────────
-- 5. Payer Funnel  (conversion rates through engagement gates)
-- ────────────────────────────────────────────────────────────
WITH funnel AS (
    SELECT
        COUNT(*)                            AS installed,
        SUM(d1_retained)                    AS day1_active,
        SUM(d7_retained)                    AS day7_active,
        SUM(d30_retained)                   AS day30_active,
        SUM(is_payer)                       AS converted_to_payer
    FROM players
)
SELECT
    installed,
    day1_active,
    ROUND(100.0 * day1_active  / installed,   1) AS d1_cvr,
    day7_active,
    ROUND(100.0 * day7_active  / installed,   1) AS d7_cvr,
    day30_active,
    ROUND(100.0 * day30_active / installed,   1) AS d30_cvr,
    converted_to_payer,
    ROUND(100.0 * converted_to_payer / installed, 2) AS payer_cvr
FROM funnel;


-- ────────────────────────────────────────────────────────────
-- 6. Session Quality  (avg. duration & sessions/day by class)
-- ────────────────────────────────────────────────────────────
SELECT
    pl.player_class,
    COUNT(s.session_id)                         AS total_sessions,
    ROUND(AVG(s.duration_sec) / 60.0, 1)        AS avg_session_min,
    ROUND(COUNT(s.session_id) * 1.0
          / COUNT(DISTINCT pl.player_id), 2)    AS sessions_per_player
FROM sessions s
JOIN players pl USING (player_id)
GROUP BY 1
ORDER BY avg_session_min DESC;


-- ────────────────────────────────────────────────────────────
-- 7. Revenue Time-Series  (daily IAP revenue + 7-day MA)
-- ────────────────────────────────────────────────────────────
WITH daily_rev AS (
    SELECT
        DATE(purchase_date)      AS day,
        SUM(amount_usd)          AS revenue
    FROM purchases
    GROUP BY 1
)
SELECT
    day,
    ROUND(revenue, 2)            AS daily_revenue,
    ROUND(AVG(revenue) OVER (
        ORDER BY day
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 2)                        AS revenue_7d_ma
FROM daily_rev
ORDER BY 1;


-- ────────────────────────────────────────────────────────────
-- 8. Top Spenders  (leaderboard — useful for whale analysis)
-- ────────────────────────────────────────────────────────────
SELECT
    pl.player_id,
    pl.country,
    pl.platform,
    pl.player_class,
    pl.level_reached,
    ROUND(SUM(pu.amount_usd), 2)  AS lifetime_spend,
    COUNT(pu.purchase_id)         AS n_purchases,
    MIN(DATE(pu.purchase_date))   AS first_purchase_date
FROM purchases pu
JOIN players pl USING (player_id)
GROUP BY 1, 2, 3, 4, 5
ORDER BY lifetime_spend DESC
LIMIT 50;
