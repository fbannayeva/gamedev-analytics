"""
Data generator for GameDev Analytics Portfolio Project.
Simulates a mobile RPG game with ~50k players over 90 days.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

# ── Config ──────────────────────────────────────────────────────────────────
N_PLAYERS      = 50_000
N_DAYS         = 90
START_DATE     = datetime(2024, 1, 1)
GAME_NAME      = "Shadow Realm: Idle RPG"

COUNTRIES      = ["US","DE","JP","BR","KR","FR","GB","RU","CN","CA"]
COUNTRY_WEIGHTS= [0.25,0.08,0.12,0.09,0.07,0.06,0.07,0.05,0.08,0.13]
PLATFORMS      = ["iOS","Android"]
CHANNELS       = ["organic","paid_social","influencer","google_uac","crosspromo"]
CHANNEL_W      = [0.30, 0.25, 0.15, 0.20, 0.10]
PLAYER_CLASSES = ["Warrior","Mage","Rogue","Paladin","Hunter"]
AB_GROUPS      = ["control","variant_a"]   # A/B test: new onboarding flow

# ── Players table ────────────────────────────────────────────────────────────
def make_players(n):
    install_days = np.random.exponential(scale=20, size=n).astype(int)
    install_days = np.clip(install_days, 0, N_DAYS - 1)
    install_dates = [START_DATE + timedelta(days=int(d)) for d in install_days]

    platform = np.random.choice(PLATFORMS, n, p=[0.45, 0.55])

    # iOS players pay slightly more
    ltv_base = np.where(platform == "iOS",
                        np.random.lognormal(2.5, 1.8, n),
                        np.random.lognormal(2.1, 1.9, n))

    country = np.random.choice(COUNTRIES, n, p=COUNTRY_WEIGHTS)

    ab_group = np.where(np.random.rand(n) < 0.5, "control", "variant_a")

    # variant_a has better D1 retention (+8%)
    d1_base = np.where(ab_group == "variant_a", 0.42, 0.34)
    d1_retained = np.random.rand(n) < d1_base

    d7_base = np.where(d1_retained,
                       np.where(ab_group == "variant_a", 0.18, 0.15),
                       0.04)
    d7_retained = np.random.rand(n) < d7_base

    d30_base = np.where(d7_retained,
                        np.where(ab_group == "variant_a", 0.08, 0.07),
                        0.01)
    d30_retained = np.random.rand(n) < d30_base

    players = pd.DataFrame({
        "player_id":    [f"p_{i:06d}" for i in range(n)],
        "install_date": install_dates,
        "platform":     platform,
        "country":      country,
        "channel":      np.random.choice(CHANNELS, n, p=CHANNEL_W),
        "player_class": np.random.choice(PLAYER_CLASSES, n),
        "ab_group":     ab_group,
        "d1_retained":  d1_retained.astype(int),
        "d7_retained":  d7_retained.astype(int),
        "d30_retained": d30_retained.astype(int),
        "total_revenue":np.round(ltv_base * d30_retained * np.random.uniform(0.5, 2.0, n), 2),
        "is_payer":     (ltv_base * d30_retained > 5).astype(int),
        "level_reached":np.random.negative_binomial(3, 0.15, n) + 1,
    })
    return players

# ── Sessions table ───────────────────────────────────────────────────────────
def make_sessions(players):
    records = []
    for _, p in players.iterrows():
        install_day = (p["install_date"] - START_DATE).days
        # active days depends on retention flags
        if p["d30_retained"]:
            active_days = random.randint(25, N_DAYS - install_day)
        elif p["d7_retained"]:
            active_days = random.randint(5, 20)
        elif p["d1_retained"]:
            active_days = random.randint(1, 6)
        else:
            active_days = 1

        active_days = min(active_days, N_DAYS - install_day)
        for day_offset in range(active_days):
            n_sessions = max(1, int(np.random.poisson(2.5)))
            for _ in range(n_sessions):
                session_start = p["install_date"] + timedelta(
                    days=day_offset,
                    hours=random.randint(7, 23),
                    minutes=random.randint(0, 59)
                )
                duration = max(30, int(np.random.lognormal(5.5, 0.8)))
                records.append({
                    "session_id":   f"s_{len(records):08d}",
                    "player_id":    p["player_id"],
                    "session_start":session_start,
                    "duration_sec": duration,
                    "platform":     p["platform"],
                    "country":      p["country"],
                })
        if len(records) > 400_000:   # cap for performance
            break
    return pd.DataFrame(records)

# ── Purchases table ──────────────────────────────────────────────────────────
def make_purchases(players):
    payers = players[players["is_payer"] == 1].copy()
    records = []
    ITEMS = {
        "Starter Pack":    4.99,
        "Gem Bundle S":    0.99,
        "Gem Bundle M":    4.99,
        "Gem Bundle L":   14.99,
        "Battle Pass":     9.99,
        "Cosmetic Skin":   2.99,
        "Energy Refill":   1.99,
        "VIP Pass":       29.99,
    }
    item_names = list(ITEMS.keys())
    item_prices = list(ITEMS.values())

    for _, p in payers.iterrows():
        n_purchases = max(1, int(np.random.lognormal(0.8, 0.9)))
        install_day = (p["install_date"] - START_DATE).days
        for _ in range(n_purchases):
            item = random.choice(item_names)
            days_after = random.randint(0, min(30, N_DAYS - install_day - 1))
            records.append({
                "purchase_id":   f"pu_{len(records):07d}",
                "player_id":     p["player_id"],
                "purchase_date": p["install_date"] + timedelta(days=days_after),
                "item_name":     item,
                "amount_usd":    ITEMS[item],
                "platform":      p["platform"],
                "country":       p["country"],
            })
    return pd.DataFrame(records)

# ── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__))
    print("Generating players...")
    players = make_players(N_PLAYERS)
    players.to_csv(f"{out}/players.csv", index=False)
    print(f"  → {len(players):,} players saved")

    print("Generating sessions (this takes ~30s)...")
    sessions = make_sessions(players.head(8_000))   # subset for speed
    sessions.to_csv(f"{out}/sessions.csv", index=False)
    print(f"  → {len(sessions):,} sessions saved")

    print("Generating purchases...")
    purchases = make_purchases(players)
    purchases.to_csv(f"{out}/purchases.csv", index=False)
    print(f"  → {len(purchases):,} purchases saved")

    print("Done ✓")
