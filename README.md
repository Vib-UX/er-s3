# EASY Residency S3 — X Profile Research Dashboard

Validated reference for official X (Twitter) accounts of all **25** projects that graduated from [YZi Labs EASY Residency Season 3](https://www.yzilabs.com/blog/meet-the-easy-residency-season-3-cohort) (Demo Day, May 2026 — Computer History Museum, Mountain View, CA).

## Quick start

```bash
cd ~/Desktop/easy-residency-s3-x-research
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

Or open `index.html` directly after starting a local server (required for JSON fetch).

## Share on your local network (Wi‑Fi / LAN)

By default, `python3 -m http.server` only listens on `localhost`. To let phones or other computers on the **same network** open the dashboard:

```bash
./scripts/serve-network.sh
```

Or manually:

```bash
python3 -m http.server 8080 --bind 0.0.0.0
```

Then share this URL with anyone on your Wi‑Fi (replace with your Mac’s IP — find it with `ipconfig getifaddr en0`):

```
http://192.168.x.x:8080
```

**Requirements:** your Mac and their device must be on the same network. macOS may prompt to allow incoming connections for Python — click Allow.

## Share on the public internet

For sharing outside your home/office network, pick one of these:

| Method | Best for | Command / steps |
|--------|----------|-----------------|
| **Cloudflare Tunnel** | Free, stable link, no port forwarding | `cloudflared tunnel --url http://localhost:8080` |
| **ngrok** | Quick temporary demo | `ngrok http 8080` |
| **GitHub Pages** | Permanent public link | Push repo to GitHub → Settings → Pages → serve from `main` |
| **Netlify Drop** | One-off drag-and-drop deploy | Drag the project folder onto [app.netlify.com/drop](https://app.netlify.com/drop) |

Static hosting (GitHub Pages, Netlify, Vercel) works well because the project is just `index.html` + `data/projects.json` — no backend needed.

**GitHub Pages quick path:**

```bash
cd ~/Desktop/easy-residency-s3-x-research
git add -A && git commit -m "Add EASY S3 X research dashboard"
# Create repo on GitHub, then:
git remote add origin git@github.com:YOUR_USER/easy-residency-s3-x-research.git
git push -u origin master
# Enable Pages: repo Settings → Pages → Branch: master, folder: / (root)
```

Your site will be at `https://YOUR_USER.github.io/easy-residency-s3-x-research/`.

## Files

| File | Purpose |
|------|---------|
| [`data/projects.json`](data/projects.json) | Single source of truth — all 25 projects, handles, followers, join dates, sources |
| [`index.html`](index.html) | Interactive dashboard (sortable table, filters, summary cards) |
| [`scripts/validate_profiles.sh`](scripts/validate_profiles.sh) | Check that X profile URLs are reachable |

## Summary (live validation 2026-06-04)

| Metric | Value |
|--------|-------|
| Total projects | 25 |
| With official X published | 22 |
| No official X published | 3 (Brief Tech, LayerV, MARGIN X) |
| Dual X accounts | 1 (Bank of AI: @BAI_AGI + @bankofai_io) |

## Program funding (YZi Labs)

YZi Labs (formerly Binance Labs) offers up to **$500,000** in direct funding per startup through **EASY Residency** (formerly the MVB incubator program):

| Tranche | Amount | Terms |
|---------|--------|-------|
| SAFE | $150,000 | 5% equity (upfront / liquid tranche) |
| Uncapped SAFE | $350,000 | Uncapped SAFE |

**S3 cohort illustrations** (25 graduates, if all receive the full published package):

| Metric | Calculation | Total |
|--------|-------------|-------|
| Cohort upfront SAFE | $150K × 25 | **$3.75M** |
| Max cohort allocation | $500K × 25 | **$12.5M** |

These are illustrative maximums; actual capital deployed per team may differ.

## Validation methodology

### Handle confirmation

Handles were cross-checked against:

1. **[YZi Labs official cohort blog](https://www.yzilabs.com/blog/meet-the-easy-residency-season-3-cohort)** (May 14, 2026) — confirms all 25 project names and descriptions; does **not** list X handles.
2. **[Odaily S3 graduation article](https://www.odaily.news/en/post/5210753)** (May 13, 2026) — lists handles inline with “XHunt Rank” metrics.
3. **[jb51/Bee-style roundup](https://www.jb51.net/blockchain/1027183qcwt.html)** (May 14, 2026) — explicit “Official X account” per project.

All 22 published handles match across jb51 and your original table. Odaily uses the same handles with minor case differences (X handles are case-insensitive).

### Follower count confidence tiers

| Tier | Label in JSON | Meaning |
|------|---------------|---------|
| `verified_live` | Live | Scraped from public X profile page on 2026-06-04 |
| `verified_live_protected` | Protected | Account exists but is protected; public view may show 0 followers |
| `source_snapshot` | Snapshot | Third-party snapshot (not used for current dashboard after live pass) |
| `unknown` | Unknown | No reliable count available |

### Important: Odaily “XHunt Rank” ≠ followers

Odaily lists numbers like “XHunt Rank: 14,384” next to handles. **These are XHunt ranking metrics, not follower counts.** Example:

| Handle | Odaily XHunt Rank | Actual followers (2026-06-04) |
|--------|-------------------|-------------------------------|
| @BAI_AGI | 14,384 | **262.8K** |
| @FunctorNetwork | 195,698 | **69.1K** |
| @TacoTradeX | 165,910 | **38.6K** |
| @SilentSwap | 92,229 | **11.9K** |

The dashboard uses live follower counts only.

### “Joined” date

The **Joined** column is the X account creation date visible on the profile. It is **not** the company founding date or EASY Residency admission date.

## Known discrepancies and notes

### Bank of AI — dual accounts

| Handle | Role | Followers (2026-06-04) | Listed by |
|--------|------|------------------------|-----------|
| [@BAI_AGI](https://x.com/BAI_AGI) | Primary brand | 262.8K | Odaily |
| [@bankofai_io](https://x.com/bankofai_io) | Secondary / ecosystem | 4,516 | jb51, Bee, KuCoin |

Both accounts are active. Odaily cites @BAI_AGI; exchange-style listings cite @bankofai_io.

### No official X (3 projects)

- **Brief Tech** — LegalTech AI; no handle in any Season 3 listing.
- **LayerV** — On-chain options; no handle in any listing.
- **MARGIN X** — On-chain prime brokerage; no handle in any listing. Unrelated [@marginx_io](https://x.com/marginx_io) exists but is not listed as official for this cohort.

### Protected account

- **L7** ([@TradeOnL7](https://x.com/TradeOnL7)) — Protected account. Public view shows 0 followers; handle is confirmed from listings.

### Case normalization

- LunarBase: Odaily `@lunarbasex` → canonical [@LunarBaseX](https://x.com/LunarBaseX)
- PokerFi: Odaily `@Pokerfi_gg` → canonical [@pokerfi_gg](https://x.com/pokerfi_gg)

## Live follower snapshot (2026-06-04)

| Project | Handle | Followers | Joined |
|---------|--------|-----------|--------|
| Bank of AI | @BAI_AGI | 262.8K | — |
| Bank of AI | @bankofai_io | 4,516 | — |
| Cournot | @CournotProtocol | 3,477 | Jan 2026 |
| Dapital | @trydapital | 7,294 | Jun 2025 |
| Flap | @flapdotsh | 82.9K | Jan 2024 |
| GEMINT | @GEMINT | 2,042 | Feb 2026 |
| LunarBase | @LunarBaseX | 2,902 | Oct 2025 |
| L7 | @TradeOnL7 | 0 (protected) | Aug 2025 |
| Möbius | @MobiusExchange | 863 | Jan 2025 |
| Nemesis | @Nemesisdottrade | 49.4K | Dec 2024 |
| Newsliquid | @newsliquidX | 18.2K | Sep 2023 |
| Openstocks | @openstocks_hq | 279 | Mar 2026 |
| PokerFi | @pokerfi_gg | 388 | Oct 2025 |
| Polysights | @Polysights | 16.5K | Oct 2024 |
| Renaiss | @renaissxyz | 65.9K | Dec 2022 |
| TermMax | @TermMaxFi | 92.6K | Nov 2022 |
| 0xBow.io | @0xbowio | 9,482 | Oct 2023 |
| Functor | @FunctorNetwork | 69.1K | Aug 2024 |
| Isaac | @getusdi | 8,449 | Sep 2025 |
| OrbSwap | @0xorbSwap | 576 | Nov 2022 |
| SilentSwap | @SilentSwap | 11.9K | Dec 2023 |
| Taco AI | @TacoTradeX | 38.6K | Nov 2025 |
| vibe.fun | @vibedotfun | 2,938 | Sep 2023 |

## How to refresh data

1. Visit each profile at `https://x.com/{handle}` and note follower count + “Joined” date.
2. Update the matching entry in [`data/projects.json`](data/projects.json):
   - `followers.count`, `followers.display`, `followers.as_of`, `followers.confidence`
   - `joined.month`, `joined.year`, `joined.source`
3. Update `meta.last_updated` and `meta.live_validation_date`.
4. Reload the dashboard.

Optional URL check:

```bash
./scripts/validate_profiles.sh
```

## Sources

| Source | URL | Accessed |
|--------|-----|----------|
| YZi Labs Blog | https://www.yzilabs.com/blog/meet-the-easy-residency-season-3-cohort | 2026-06-04 |
| Odaily | https://www.odaily.news/en/post/5210753 | 2026-06-04 |
| jb51 | https://www.jb51.net/blockchain/1027183qcwt.html | 2026-06-04 |
| X profile pages | https://x.com/{handle} | 2026-06-04 (live validation) |

## Limitations

- Follower counts change continuously; all numbers are snapshots.
- X may rate-limit or require login for automated access; live validation was done via browser on public profile pages.
- Company founding dates are out of scope (would require Crunchbase/RootData per project).
- Odaily XHunt ranks are preserved in research notes only; they must not be interpreted as followers.

## License

Research compilation for personal reference. Project names and trademarks belong to their respective owners.
