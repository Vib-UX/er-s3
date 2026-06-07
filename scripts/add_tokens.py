#!/usr/bin/env python3
"""Add / refresh a `token` block on each project in data/projects.json.

Idempotent: re-running overwrites the `token` field for known projects and
leaves a default {"status": "unknown"} for projects with no verified data.

Token status values:
  live      - token trades on a market; coingecko_id drives a live market-cap fetch
  pre_token - token announced/registered/issued but not actively trading (no market cap yet)
  none      - project has stated it has no token
  unknown   - no official token confirmed (often only imposter/namesake tokens exist)

An optional `supply` block ({total, max, circulating}) is shown by the UI even
when there is no market cap (e.g. a token is issued on-chain but not yet trading).

`as_of` cached values are point-in-time fallbacks shown only if the live fetch
fails. Verified 2026-06-07 from CoinGecko / project docs.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "projects.json")

# name -> token block. Only verified projects are listed; everything else
# defaults to {"status": "unknown"}.
TOKENS = {
    "Nemesis": {
        "status": "live",
        "symbol": "NEMESIS",
        "chain": "Base",
        "coingecko_id": "nemesis-2",
        "note": "Live on Uniswap (Base). Beware imposter tickers (e.g. 'Nemesis AI Trader').",
        "cached": {"market_cap_usd": 566555, "price_usd": 0.000567, "change_24h": -5.7, "as_of": "2026-06-07"},
        "trackers": [
            {"name": "CoinGecko", "url": "https://www.coingecko.com/en/coins/nemesis-2"}
        ],
    },
    "Flap": {
        "status": "pre_token",
        "symbol": "FLAP",
        "chain": "BNB Chain",
        "coingecko_id": "flap",
        "note": "Token page live on CoinGecko; not yet trading (launch TBA).",
        "trackers": [
            {"name": "CoinGecko", "url": "https://www.coingecko.com/en/coins/flap"}
        ],
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
            {"name": "Etherscan", "url": "https://etherscan.io/address/0x3c2F61f2E27C865981D2e7aAf6b2CDf823030039"}
        ],
    },
    "vibe.fun": {
        "status": "pre_token",
        "symbol": "VIBE",
        "chain": "Solana",
        "supply": {"total": 1000000000, "max": 1000000000},
        "note": "VIBE listed (Solana, 1B supply) but no live market cap / trading yet. Verify the contract — several unrelated 'VIBE' tokens exist.",
        "trackers": [
            {"name": "CoinCarp", "url": "https://www.coincarp.com/currencies/vibe-fun/price/"}
        ],
    },
    "Isaac": {
        "status": "pre_token",
        "symbol": "USD-i",
        "note": "Interest-free stablecoin (USD-i); no verified public token contract found yet — beware unrelated 'USDI' tokens.",
        "trackers": [],
    },
    "Bank of AI": {
        "status": "unknown",
        "note": "Multiple namesake/imposter BAI/BOAI tokens exist (some with near-zero liquidity); no clearly official token confirmed.",
    },
    "Dapital": {
        "status": "unknown",
        "note": "An unverified BSC namesake token exists; no official Dapital token confirmed.",
    },
    "GEMINT": {
        "status": "unknown",
        "note": "Namesake meme/sports tokens exist; no official GEMINT token confirmed.",
    },
    "SilentSwap": {
        "status": "unknown",
        "note": "A 'SILE' namesake token exists; official SilentSwap token not verified.",
    },
    "Renaiss": {
        "status": "pre_token",
        "symbol": None,
        "chain": "BNB Chain",
        "note": "No native token yet; in open beta. Value currently flows via collectible NFTs.",
        "trackers": [],
    },
    "Functor": {
        "status": "pre_token",
        "symbol": "FUNC",
        "note": "FUNC currently exists as in-app mining/points, not a listed tradable token.",
        "trackers": [],
    },
    "Taco AI": {
        "status": "pre_token",
        "note": "Pre-token; no TGE announced.",
        "trackers": [],
    },
    "Polysights": {
        "status": "pre_token",
        "note": "Pre-token; no TGE announced. An unaffiliated 'POLYSIGHTS' meme token on Solana is an imposter.",
        "trackers": [],
    },
}

DEFAULT = {"status": "unknown"}


def main():
    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    for p in data["projects"]:
        p["token"] = TOKENS.get(p["name"], dict(DEFAULT))

    # summary on meta
    statuses = [p["token"]["status"] for p in data["projects"]]
    data["meta"]["token_summary"] = {
        "live": statuses.count("live"),
        "pre_token": statuses.count("pre_token"),
        "unknown": statuses.count("unknown"),
        "none": statuses.count("none"),
        "as_of": "2026-06-07",
    }

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("Updated", DATA)
    print("Token summary:", data["meta"]["token_summary"])


if __name__ == "__main__":
    main()
