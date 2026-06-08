#!/usr/bin/env python3
"""Add / refresh `token` blocks on each project in season JSON files.

Usage:
  python3 scripts/add_tokens.py              # all seasons
  python3 scripts/add_tokens.py season1      # one season

Token status values:
  live      - official token trading; coingecko_id drives live market-cap fetch
  pre_token - TGE planned/registered/points; supply known but not actively trading
  none      - project explicitly has no native token (may use stablecoins/product tokens)
  unknown   - no verified token data; imposters may exist

Audited 2026-06-08 against CoinGecko, CoinMarketCap, DexScreener, CoinCarp, project docs.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")

DEFAULT = {"status": "unknown"}

TOKENS_BY_SEASON = {
    "season1": {
        "APRO": {
            "status": "live",
            "symbol": "AT",
            "chain": "BNB Chain",
            "coingecko_id": "apro",
            "supply": {"total": 1000000000, "max": 1000000000, "circulating": 230000000},
            "note": "Listed on Binance Spot (Nov 2025). BNB + Ethereum contracts.",
            "cached": {"market_cap_usd": 28390000, "price_usd": 0.1235, "change_24h": 5.2, "as_of": "2026-06-08"},
            "trackers": [
                {"name": "CoinGecko", "url": "https://www.coingecko.com/en/coins/apro"},
                {"name": "Binance", "url": "https://www.binance.com/en/trade/AT_USDT"},
            ],
        },
        "Bitway": {
            "status": "live",
            "symbol": "BTW",
            "chain": "BNB Chain",
            "coingecko_id": "bitway",
            "contract": "0x444045B0EE1ee319A660a5E3d604CA0ffA35ACaA",
            "supply": {"total": 10000000000, "max": 10000000000, "circulating": 2200000000},
            "note": "Native BTW token live. Bitway Chain + Finance in public beta.",
            "cached": {"market_cap_usd": 131700480, "price_usd": None, "change_24h": None, "as_of": "2026-06-08"},
            "trackers": [
                {"name": "CoinGecko", "url": "https://www.coingecko.com/en/coins/bitway"},
                {"name": "CMC", "url": "https://coinmarketcap.com/currencies/bitway-btw/"},
            ],
        },
        "Byte AI": {
            "status": "live",
            "symbol": "BYTE",
            "chain": "Base",
            "coingecko_id": "byte-3",
            "contract": "0x2d90785e30a9df6cce329c0171cb8ba0f4a5c17b",
            "supply": {"total": 1000000000, "max": 1000000000, "circulating": 1000000000},
            "note": "BYTE by Virtuals on Base (tryabyte.xyz). Micro-cap, thin liquidity — verify contract.",
            "cached": {"market_cap_usd": 260119, "price_usd": 0.0002601, "change_24h": 3.8, "as_of": "2026-06-08"},
            "trackers": [
                {"name": "CoinGecko", "url": "https://www.coingecko.com/en/coins/byte-3"},
                {"name": "DexScreener", "url": "https://dexscreener.com/base/0x2d90785e30a9df6cce329c0171cb8ba0f4a5c17b"},
            ],
        },
        "OptimAI": {
            "status": "pre_token",
            "symbol": "OPI",
            "chain": "BNB Chain",
            "note": "OPI documented in GitHub/docs; contract TBD on opBNB. Node points accrue pre-TGE. CMC Labs cohort.",
            "trackers": [{"name": "GitHub", "url": "https://github.com/OptimaiNetwork/optimai-cookbooks"}],
        },
        "RecycleFarm": {
            "status": "pre_token",
            "symbol": "RCF",
            "note": "RCF in GitBook tokenomics; ESA/DePIN credits convert to RCF. Not yet on CG/CMC. Beware RecycliFi RCF imposter.",
            "trackers": [{"name": "GitBook", "url": "https://recyclefarm.gitbook.io/recyclefarm-en"}],
        },
        "Paimon Finance": {
            "status": "pre_token",
            "symbol": "PAIMON",
            "note": "RWA product tokens live (xSPCX, PPT); PAIMON/vePAIMON governance planned — not yet issued.",
            "trackers": [{"name": "GitBook", "url": "https://paimon-finance.gitbook.io/paimon.finance/"}],
        },
        "Modus": {
            "status": "pre_token",
            "note": "On-chain prime brokerage on Monad; no TGE announced. Beware unrelated Solana MODUS pumps.",
            "trackers": [],
        },
        "StableStock": {
            "status": "none",
            "note": "TraDeFi platform uses sStock wrapped equities + stablecoins (USDT/USDC). No native governance token.",
            "trackers": [{"name": "StableStock", "url": "https://stablestock.xyz/"}],
        },
        "Video Tutor": {
            "status": "none",
            "note": "$11M equity seed; no crypto token plans reported.",
            "trackers": [],
        },
        "Lumi": {"status": "none", "note": "Biotech lab AI (Reach Industries). No token. Beware LumiShare LUMI imposter."},
        "Freebeat.AI": {"status": "none", "note": "AI video SaaS. No token/TGE."},
        "ComplyGen": {"status": "none", "note": "Fintech compliance SaaS. No token."},
        "AMMO": {"status": "none", "note": "Super Intern uses in-app TU credits — not an on-chain tradable token."},
        "Hubble AI": {"status": "unknown", "note": "Agent transaction infra (hubble.xyz). No confirmed token roadmap."},
        "Robata": {"status": "unknown", "note": "Robotics data network. No token announced. Beware ROBA/ROBO imposters."},
    },
    "season2": {
        "Predict.fun": {
            "status": "none",
            "note": "No native token — platform runs on USDT/USDC. $1.7B+ volume; no confirmed TGE/airdrop structure.",
            "trackers": [{"name": "Predict.fun", "url": "https://predict.fun/"}],
        },
        "42.space": {
            "status": "pre_token",
            "note": "Event Outcome Tokens (OT) via bonding curves live; protocol governance token TBA.",
            "trackers": [{"name": "42.space", "url": "https://markets.42.space/"}],
        },
        "Bento.fun": {"status": "pre_token", "note": "BNB Chain social prediction layer; alpha/mainnet rollout. Beware Base BENTO meme imposter."},
        "Frontrun": {"status": "none", "note": "Trading wallet/extension (frontrun.pro). No native platform token announced."},
        "Hertzflow": {"status": "pre_token", "note": "Permissionless leverage markets live at hertzflow.xyz; no HERTZ token on CG yet."},
        "Saturn Labs": {
            "status": "pre_token",
            "note": "USDat/sUSDat yield products live; Gravity Points → up to 5% of future governance token (TGE contingent).",
            "trackers": [{"name": "Saturn Docs", "url": "https://saturncredit.gitbook.io/saturn-docs/"}],
        },
        "Sats Terminal": {"status": "pre_token", "note": "Bitcoin DeFi aggregator; $1.7M pre-seed. No native token. Beware Ordinals SATS imposters."},
        "Help.fun": {"status": "none", "note": "Nonprofit token launchpad — launches third-party charity tokens (e.g. $DEVELOPER), no native Help.fun token."},
        "MeleeMon": {"status": "pre_token", "note": "Stablecoin wagering mobile game. No game token listed yet."},
        "4D Labs": {"status": "pre_token", "note": "Tokenized 3D data-rights framework planned per YZi thesis; no token issued yet."},
        "AllScale": {"status": "none", "note": "Self-custodial stablecoin neobank; uses USDT/USDC only. Equity-funded, no ICO."},
        "Advent": {"status": "none", "note": "AI gene therapy biotech. No crypto token."},
        "AgriDynamics": {"status": "none", "note": "Fruit-harvesting robotics. No web3/token."},
        "FingerDance": {"status": "none", "note": "Sign-language AI infrastructure. No token."},
        "Manifolds": {"status": "none", "note": "AI 3D video SaaS ($150K ARR). No token."},
        "Neomera BioLab": {"status": "none", "note": "Non-opioid drug discovery biotech. No token."},
        "Trellis Robotics": {"status": "none", "note": "AI soft robotics for industrial inspection. No token."},
    },
    "season3": {
        "Nemesis": {
            "status": "live",
            "symbol": "NEMESIS",
            "chain": "Base",
            "coingecko_id": "nemesis-2",
            "note": "Live on Uniswap (Base). Beware imposter tickers (e.g. 'Nemesis AI Trader').",
            "cached": {"market_cap_usd": 566555, "price_usd": 0.000567, "change_24h": -5.7, "as_of": "2026-06-08"},
            "trackers": [{"name": "CoinGecko", "url": "https://www.coingecko.com/en/coins/nemesis-2"}],
        },
        "Flap": {
            "status": "pre_token",
            "symbol": "FLAP",
            "chain": "BNB Chain",
            "coingecko_id": "flap",
            "note": "CoinGecko preview page; platform live on BNB. Native FLAP TGE pending — user-launched flap.sh tokens are not FLAP.",
            "trackers": [{"name": "CoinGecko", "url": "https://www.coingecko.com/en/coins/flap"}],
        },
        "TermMax": {
            "status": "pre_token",
            "symbol": "TMX",
            "chain": "Ethereum",
            "coingecko_id": "termmax",
            "contract": "0x3c2F61f2E27C865981D2e7aAf6b2CDf823030039",
            "supply": {"total": 1000000000, "max": 1000000000, "circulating": 200000000},
            "note": "TMX registered (1B fixed supply, ~20% at TGE); TGE to be announced. Not yet trading.",
            "trackers": [
                {"name": "CoinGecko", "url": "https://www.coingecko.com/en/coins/termmax"},
                {"name": "Etherscan", "url": "https://etherscan.io/address/0x3c2F61f2E27C865981D2e7aAf6b2CDf823030039"},
            ],
        },
        "Taco AI": {
            "status": "pre_token",
            "symbol": "TACO",
            "note": "Planned $TACO airdrop targeted Q1 2026; not listed on CG/CMC as of Jun 2026. Stars/Coins are in-app points.",
            "trackers": [],
        },
        "Functor": {
            "status": "pre_token",
            "symbol": "FUNC",
            "note": "FUNC as node-mining/points via functor.sh; airdrop confirmed, not yet tradable on CG/CMC.",
            "trackers": [],
        },
        "Isaac": {
            "status": "pre_token",
            "symbol": "USD-i",
            "note": "Interest-free stablecoin pre-launch (usd-i.com). No verified contract yet — beware USDI/iUSD imposters.",
            "trackers": [],
        },
        "Renaiss": {
            "status": "pre_token",
            "chain": "BNB Chain",
            "note": "Open beta; value via collectible NFT twins + points/SBTs. No native fungible token TGE announced.",
            "trackers": [],
        },
        "Polysights": {
            "status": "pre_token",
            "note": "Polymarket analytics; no TGE announced. Solana POLYSIGHTS meme is an imposter.",
            "trackers": [],
        },
        "vibe.fun": {
            "status": "unknown",
            "note": "Cannot verify CoinCarp 'VIBE' (1B supply) as official @vibedotfun token — likely different project. Await official contract.",
            "trackers": [
                {"name": "CoinGecko search", "url": "https://www.coingecko.com/en/search?query=vibe.fun"},
            ],
        },
        "Bank of AI": {
            "status": "none",
            "note": "No official token (docs.bankofai.io). Beware BOAI/BAI BSC imposters with near-zero liquidity.",
            "trackers": [],
        },
        "Brief Tech": {"status": "none", "note": "LegalTech SaaS. No crypto token."},
        "Cournot": {"status": "none", "note": "AI reasoning oracle (docs.cournot.ai). No token/TGE."},
        "Dapital": {
            "status": "none",
            "note": "Social trading broker (dapital.xyz). Beware unverified BSC namesake token.",
            "trackers": [],
        },
        "GEMINT": {
            "status": "none",
            "note": "Collectible/IP market structure. Beware GemMint Solana meme imposter.",
            "trackers": [],
        },
        "LayerV": {"status": "none", "note": "On-chain options platform. No official X or token in cohort sources."},
        "LunarBase": {
            "status": "none",
            "chain": "Base",
            "note": "Prop AMM + launchpad (lunarbase.gg). Product live; no native governance token announced.",
            "trackers": [],
        },
        "L7": {"status": "none", "note": "Agentic capital platform (@TradeOnL7). No token/TGE announced."},
        "Möbius": {
            "status": "none",
            "chain": "BNB Chain",
            "note": "Prime brokerage (mob.exchange). Not Mantle MobiusExchange MBS or MBU imposters.",
            "trackers": [],
        },
        "Newsliquid": {"status": "none", "note": "AI news-to-trade layer. No official token."},
        "Openstocks": {
            "status": "none",
            "note": "RWA private-market platform; points program coming. No native token TGE confirmed.",
            "trackers": [],
        },
        "PokerFi": {
            "status": "none",
            "note": "S3 skill-game options (@pokerfi_gg). NOT pokerfi.com.br POKERFI on CMC — different project.",
            "trackers": [],
        },
        "0xBow.io": {
            "status": "none",
            "note": "Privacy Pools / ASP compliance infra. No native token. Beware Archerswap BOW imposter.",
            "trackers": [],
        },
        "MARGIN X": {"status": "none", "note": "BNB Chain prime brokerage. No official token. @marginx_io is unrelated."},
        "OrbSwap": {
            "status": "none",
            "chain": "Arbitrum",
            "note": "Stablecoin AMM (orbswap.org). LP tokens only; no governance token. Beware ORBS/ORBI imposters.",
            "trackers": [],
        },
        "SilentSwap": {
            "status": "none",
            "note": "Cross-chain privacy swap (V2 live). No official native token. Beware SILE Ethereum imposter.",
            "trackers": [],
        },
    },
}

SEASON_FILES = {
    "season1": "season1.json",
    "season2": "season2.json",
    "season3": "season3.json",
    "projects": "projects.json",
}


def apply_tokens(path, token_map):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for p in data["projects"]:
        p["token"] = token_map.get(p["name"], dict(DEFAULT))
    statuses = [p["token"]["status"] for p in data["projects"]]
    data["meta"]["token_summary"] = {
        "live": statuses.count("live"),
        "pre_token": statuses.count("pre_token"),
        "none": statuses.count("none"),
        "unknown": statuses.count("unknown"),
        "as_of": "2026-06-08",
    }
    data["meta"]["token_audit"] = "2026-06-08 — CoinGecko, CMC, DexScreener, CoinCarp, project docs"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Updated {path} — {data['meta']['token_summary']}")


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["season1", "season2", "season3"]
    for key in targets:
        if key not in SEASON_FILES:
            print(f"Unknown season: {key}", file=sys.stderr)
            continue
        path = os.path.join(DATA_DIR, SEASON_FILES[key])
        if not os.path.isfile(path):
            print(f"Skip missing {path}", file=sys.stderr)
            continue
        season_key = "season3" if key == "projects" else key
        apply_tokens(path, TOKENS_BY_SEASON.get(season_key, {}))
    if "season3" in targets or (not sys.argv[1:] and os.path.isfile(os.path.join(DATA_DIR, "projects.json"))):
        apply_tokens(os.path.join(DATA_DIR, "projects.json"), TOKENS_BY_SEASON["season3"])


if __name__ == "__main__":
    main()
