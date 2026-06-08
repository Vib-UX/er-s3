#!/usr/bin/env python3
"""Generate data/season1.json and data/season2.json from researched cohort lists.

Sources:
  S1 — PANews/Biteye S1 review (2025-12), Odaily S1 highlights, YZi Labs blog
  S2 — YZi Labs official cohort blog (2025-12-09), Odaily BBW recap

X handles for S1 are from published cohort reviews. S2 handles are from
official project profiles where found; others marked needs_live_check.
Token blocks are merged by scripts/add_tokens.py after generation.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

FUNDING = {
    "program": "YZi Labs EASY Residency (formerly MVB incubator program; YZi Labs formerly Binance Labs)",
    "max_per_startup_usd": 500000,
    "structure": [
        {"label": "SAFE", "amount_usd": 150000, "terms": "5% equity", "note": "Upfront / liquid tranche"},
        {"label": "Uncapped SAFE", "amount_usd": 350000, "terms": "Uncapped SAFE", "note": "Additional allocation"},
    ],
    "disclaimer": "Illustrative cohort totals if all graduates receive the full published package ($150K + $350K). Actual deployed capital per team may vary.",
}

YZI_BLOG = {"name": "YZi Labs Blog", "url": "https://www.yzilabs.com/blog/meet-the-easy-residency-season-2-cohort"}
S1_PANEWS = {"name": "PANews / Biteye S1 review", "url": "https://www.panewslab.com/en/articles/49450c5a-13ec-4c9d-b7da-197e318c2e0c"}


def handle(h, role="primary", confidence="source_snapshot"):
    return {
        "handle": h,
        "role": role,
        "profile_url": f"https://x.com/{h}",
        "validation_status": "confirmed",
        "sources": ["cohort_listing"],
        "followers": {"count": None, "display": None, "as_of": None, "confidence": confidence},
        "joined": {"month": None, "year": None, "source": None},
    }


def project(name, track, description, x_handle=None, validation_status="confirmed",
              notes="", sources=None, token=None):
    p = {
        "name": name,
        "track": track,
        "description": description,
        "validation_status": validation_status,
        "x_handles": [handle(x_handle)] if x_handle else [],
        "notes": notes,
        "official_sources": sources or [],
    }
    if token:
        p["token"] = token
    return p


S1_PROJECTS = [
    project("APRO", "AI Infrastructure", "AI-native oracle for verifiable multi-source data across DeFi, RWA, and AI.",
              "APRO_Oracle", notes="Token $AT listed on Binance Spot (Nov 2025). $3M seed from Polychain, Franklin Templeton, ABCDE.",
              sources=[S1_PANEWS, {"name": "Binance AT listing", "url": "https://www.binance.com/en/support/announcement/detail/b0c65316e2bc4878838852b16291d07b"}]),
    project("Hubble AI", "AI Infrastructure", "Intelligent agent transaction infrastructure — data, identity, and payments for agentic finance.",
              "MeetHubble", notes="ETHGlobal Buenos Aires 2025 Top 10 Finalist."),
    project("OptimAI", "AI Infrastructure", "Web3 data layer and agent AI for personalized digital twins.",
              "OptimaiNetwork", notes="~800K nodes reported across 179 countries."),
    project("Robata", "AI Infrastructure", "Decentralized data network for embodied intelligence and robotics training data.",
              "robataai", notes="1.6M+ data samples collected in early stage."),
    project("StableStock", "RWA", "Crypto-friendly neobroker bringing public stock liquidity on-chain via stablecoins.",
              "StableStock", notes="Weekly spot volume exceeded $3M; strategic round in progress."),
    project("Paimon Finance", "RWA", "Marketplace for tokenized pre-IPO assets (SpaceX, Stripe, ByteDance).",
              "Paimon_Finance", notes="$2M TVL and $1.5M volume in first month (no marketing)."),
    project("RecycleFarm", "DePIN", "DePIN-based digital MRV for carbon credit transparency.",
              "ReFarm_DePIN", notes="Active at Binance Blockchain Week and industry demo days."),
    project("Bitway", "Bitcoin / DeFi", "Decentralized on-chain capital market — Bitcoin application chain, native BTC lending, asset management.",
              "BitwayOfficial", notes="Bitway Chain and Finance in public beta; Bitway Earn coming soon."),
    project("Modus", "DeFi", "On-chain prime brokerage on Monad — lending, delta-neutral vault, sealed-bid liquidations.",
              "Modus_Finance", notes="Team from PancakeSwap, LayerZero, Protocol Labs backgrounds."),
    project("AMMO", "AI Applications", "AI-native assistants for online communities (Superintern Discord agent, Mode Marketplace).",
              "Ammo_AI"),
    project("Lumi", "Biotech / AI", "Visual AI co-pilot for lab automation; partners include AstraZeneca and Pfizer.",
              "lumi_systems", notes="Reach Industries product; founder Silas Adekunle (Reach Robotics)."),
    project("Freebeat.AI", "AI Applications", "Music-to-video generation platform; expanding to general-purpose video agent.",
              "freebeat_ai", notes="Expanded to 100+ countries."),
    project("Video Tutor", "AI Applications", "AI text-to-video personalized tutoring platform.",
              "VideoTutor_io", notes="$11M seed; 40K+ users in 5 months; MiniMax partnership."),
    project("Byte AI", "AI Applications", "Web-based food delivery agent accepting crypto payments.",
              "Byte__AI", notes="$BYTE token issued (Virtuals); verify contract before trading."),
    project("ComplyGen", "Fintech", "AI automation for fintech compliance — KYC/KYB and marketing content review.",
              "ComplyGen", validation_status="needs_live_check",
              notes="Limited public updates since Demo Day; account activity low."),
]

S2_PROJECTS = [
    project("42.space", "Prediction Markets", "Asset issuance protocol — trade real-world events like liquid tokens via bonding curves.",
              "42space", notes="Event Rush live on Binance Wallet; partnership with BNB Chain."),
    project("4D Labs", "AI / Spatial", "Spatial intelligence large models — 3D data collection, generation, and tokenized data rights.",
              validation_status="needs_live_check", notes="X handle not confirmed in cohort sources."),
    project("AllScale", "Fintech / Web3", "Self-custodial stablecoin neobank for cross-border business operations.",
              "AllScaleFinance", validation_status="needs_live_check", notes="Handle inferred from brand — verify on x.com."),
    project("Advent", "Biotech", "AI-driven precision gene therapeutics and AAV capsid discovery platform.",
              validation_status="no_official_x", notes="Biotech project; no official X published in YZi Labs cohort listing."),
    project("AgriDynamics", "Robotics / Biotech", "Fruit harvesting robot addressing farm labor crisis.",
              validation_status="no_official_x"),
    project("Bento.fun", "Prediction Markets", "Social layer for prediction markets — micro-duels in Telegram, Twitter, WhatsApp on BNB Chain.",
              "bento_fun", validation_status="needs_live_check", notes="BNB Chain native prediction-market primitive."),
    project("FingerDance", "AI", "Sign language translation AI infrastructure for the deaf community (SL-LLM).",
              validation_status="needs_live_check"),
    project("Frontrun", "Trading", "Pro trader wallet for fast discovery, due diligence, and execution (Solana-first, multi-chain roadmap).",
              "FrontrunPro", validation_status="needs_live_check", notes="Backed by Alliance DAO and YZi Labs; frontrun.pro."),
    project("Help.fun", "Web3", "Crypto launchpad for nonprofit and equity-backed startup tokens with anti-bot mechanics.",
              "helpdotfun", validation_status="needs_live_check"),
    project("Hertzflow", "Trading", "Permissionless leverage market for any oracle-supported asset (crypto, FX, commodities, stocks).",
              "HertzFlow_xyz", validation_status="needs_live_check", notes="hertzflow.xyz"),
    project("Manifolds", "AI / Video", "AI-powered 3D spatially controllable video generation platform.",
              validation_status="needs_live_check", notes="$150K ARR, 60 paid enterprise clients reported at Demo Day."),
    project("MeleeMon", "Gaming", "Competitive mobile monster-battle game with stablecoin wagering.",
              validation_status="needs_live_check", notes="YC '19 founders; prior Gamebytes 5M+ users."),
    project("Neomera BioLab", "Biotech", "Non-opioid drug discovery for chronic pain and major chronic diseases.",
              validation_status="no_official_x"),
    project("Sats Terminal", "Bitcoin / DeFi", "Native Bitcoin liquidity protocol — swaps, credit, and yield on BTC/EVM.",
              "SatsTerminal", validation_status="needs_live_check", notes="$1.7M pre-seed (Coinbase Ventures, Draper)."),
    project("Saturn Labs", "Bitcoin / DeFi", "10%+ yield stablecoin backed by Bitcoin credit (MicroStrategy STRC).",
              "SaturnLabsHQ", validation_status="needs_live_check"),
    project("Predict.fun", "Prediction Markets", "BNB Chain prediction market with yield-bearing collateral and DeFi-boosted liquidity.",
              "predictdotfun", notes="Founded by ex-PancakeSwap/LooksRare builder; $1.7B+ volume reported; no native token yet.",
              sources=[YZI_BLOG, {"name": "Predict.fun", "url": "https://predict.fun/"}]),
    project("Trellis Robotics", "Robotics", "AI soft robotics platform for confined-space industrial inspection.",
              validation_status="no_official_x", notes="Stanford vine-robot team; pilots with Dow, LBNL."),
]


def build_season(season_num, cohort_label, demo_day, projects, graduates, last_updated):
    cohort = {
        "graduates": graduates,
        "upfront_safe_per_startup_usd": 150000,
        "upfront_safe_cohort_total_usd": 150000 * graduates,
        "max_per_startup_usd": 500000,
        "max_cohort_allocation_usd": 500000 * graduates,
    }
    funding = {**FUNDING, "cohort": cohort}
    for p in projects:
        if not p.get("official_sources"):
            p["official_sources"] = [YZI_BLOG if season_num == 2 else S1_PANEWS]
    return {
        "meta": {
            "season": season_num,
            "cohort": cohort_label,
            "program": "YZi Labs EASY Residency",
            "demo_day": demo_day,
            "total_projects": len(projects),
            "last_updated": last_updated,
            "live_validation_date": None if season_num != 3 else "2026-06-04",
            "funding": funding,
        },
        "projects": projects,
    }


def main():
    s1 = build_season(
        1, "EASY Residency Season 1",
        "August 2025 — New York Stock Exchange, New York, NY",
        S1_PROJECTS, len(S1_PROJECTS), "2026-06-07",
    )
    s2 = build_season(
        2, "EASY Residency Season 2",
        "December 2025 — Binance Blockchain Week Demo Day",
        S2_PROJECTS, len(S2_PROJECTS), "2026-06-07",
    )
    for name, data in [("season1.json", s1), ("season2.json", s2)]:
        path = os.path.join(DATA, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Wrote {path} ({len(data['projects'])} projects)")


if __name__ == "__main__":
    main()
