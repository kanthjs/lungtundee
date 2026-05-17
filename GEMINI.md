# Project: lungtundee (ลงทุนดี)

**Overview:**  
"ลงทุนดี" is a Personal AI Fund Manager system designed to manage stock and mutual fund portfolios. It employs a Multi-Agent architecture to synthesize fundamental analysis, technical timing, and portfolio monitoring into actionable investment decisions led by a Chief Investment Officer (CIO).

## Core Architecture & Agents
The system resides in `.claude/agents/` and follows a strict synthesis workflow. Each agent has a Thai persona and specific mandate:

- **Digital Twin — "มีตัง" (investor-self):** The starting point for all thinking. Represents the owner's inner monologue.
  - **Process:** Story-first (ถ้า story ไม่ติด ไม่แตะ), inner monologue, "ฉันจะ" (not "คุณควร").
  - **Orchestration:** Thinks first, then calls specialists (พี่หมอเงิน, พี่หมอดู, ฯลฯ) only when needed.
  - **Blind Spot Check:** Explicitly checks for holding losers too long or averaging down without a new thesis.

- **CIO (Chief Investment Officer) — "พี่ขุน" (cio):** The final decision-maker. 
  - **Process:** Synthesizes reports from specialists. Applies an investment style filter.
  - **Sizing Rule:** Never all-in. High conviction = Max 20% of cash. Medium = Max 10%.
  - **Verdict:** Provides a clear "บทสรุป" with specific Ticker, Amount, Entry Zone, and Stop Loss.

- **Fundamental Analyst — "พี่หมอเงิน" (fundamental-analyst):** Evaluates business quality and intrinsic value.
  - **Frameworks:** Business Quality (moat/powers), Financial Ratios (P/E, ROE, D/E), Red Flags, and Intrinsic Value ranges (DCF/PE-based).
  - **Goal:** Answer "What" a company is worth and "Why".

- **Technical Analyst — "พี่หมอดู" (technical-analyst):** Analyzes price action and indicators for timing.
  - **Focus:** Trends (Primary/Secondary), Key levels (Support/Resistance), RSI/MACD/MA, and Entry/Exit zones.
  - **Goal:** Answer "When" to enter or exit.

- **Portfolio Monitor — "ยาม" (portfolio-monitor):** Tracks holdings, P&L, and alerts.
  - **Focus:** Stop loss breaches, unusual moves, and NAV updates.

- **Market Researcher — "นักสืบตลาด":** Sector overview, idea generation, and competitive landscape.

## Investment Strategy (Investor Profile)
- **Style:** Value Investing (Fundamentals-first) + Technical Timing. 
- **Voice:** Professional, direct, and honest. Favors specific "Kill Conditions" over vague risks.
- **Time Horizon:** Medium (1–6 months). Focuses on catalysts rather than indefinite holding.
- **Universe:** SET (Thai), US (NYSE/NASDAQ), Global ETFs, Mutual Funds (SSF/RMF/General).
- **Risk Management:** 
  - Moderate tolerance (15–25% drawdown).
  - Position sizing: Max 20% of cash per decision (CIO Rule).
  - Kill Condition: Thesis change or >25% unexplained drawdown.

## Directory Structure
- `scripts/`: Automation scripts (located at root).
  - `fetch_prices.py`, `fetch_fund_nav.py`, `fetch_fundamentals.py`.
  - `analyze_portfolio.py`, `alert_monitor.py`.
- `briefs/`: Research reports and investment theses.
- `sources/`: Data and tracking files.
  - `portfolio/`: Data files for the portfolios (`kant/`, `me-tang/`).
  - `portfolio_summary.md`: **Source of Truth** for agents (auto-generated).
  - `live_prices.json`: Real-time data (auto-generated).
- `logs/`: Investment journals, portfolio reviews, and `alerts.md`.

## Operational Workflows

### 1. Stock & Fund Research (`/brief`)
When analyzing a new asset, generate a 6-section report:
1. **Data Prep:** Run `python fetch_fundamentals.py <TICKER>` to get latest ratios.
2. **Company Snapshot:** Plain Thai explanation of the business (2-3 sentences).
3. **Fundamentals Signal:** Directional trends (Revenue, Margin, Capital Allocation) using the fetched fundamentals.
4. **Latest Earnings:** Specific bullets from the most recent reports.
5. **Bull/Bear Case:** Specific to the company (avoid generic "macro" risks).
6. **Kill Conditions:** Explicit triggers for exiting (e.g., "Margin drops for 3 consecutive quarters").
7. **Questions to Ask:** Crucial questions a beginner should answer before buying.

**Rules:** No buy/sell recommendations in the brief. No "moat" (use specific powers). No hedging.

### 2. Consolidated Portfolio Analysis & Advice
Me-Tang (Digital Twin) initiates the process:
1. **Data Prep:** Run the **Automated Workflow** (see below) to generate `portfolio_summary.md`.
2. **Analysis:** Read `portfolio_summary.md` for accurate P&L and weights.
3. **Inner Monologue:** Scan for the most concerning position or opportunity.
4. **Specialist Call:** Invoke **พี่หมอเงิน** / **พี่หมอดู** for deep dives based on current data.
5. **CIO Verdict:** **พี่ขุน** provides the final "Path Forward" with sizing and levels.
6. **Record:** Log the strategy in `logs/YYYY-MM-DD-portfolio-review.md`.

### 3. Portfolio Monitoring
1. **ยาม (Portfolio Monitor)** reads CSV files and `live_prices.json`.
2. Flags alerts for each portfolio separately.

## Development Conventions
- **Language:** Supports Thai and English. **Thai is REQUIRED for verdicts (บทสรุป).**
- **Data Integrity:** ALWAYS prefer CSV files for numerical calculations.
- **Safety:** Never modify files outside the project root.
- **Me-Tang Mandate:** Always provide a solution, not just a status report. Think like the owner.

## Commands & Tools
- **Research:** `/brief` for automated research report generation.
- **Price Fetching:** `fetch_prices.py` — Fetches real-time prices + Technical Indicators (MA, RSI) to `live_prices.json`.
- **Fund NAV Fetching:** `fetch_fund_nav.py` — Updates Thai mutual fund NAVs in CSV files.
- **Fundamental Data:** `fetch_fundamentals.py` — Fetches financial ratios (P/E, ROE, etc.) for stock analysis.
- **Math Engine:** `analyze_portfolio.py` — Calculates P&L, Weights, and generates `portfolio_summary.md`.
- **Alert System:** `alert_monitor.py` — Checks Kill Conditions and logs alerts to `logs/alerts.md`.

## Automated Workflow (Recommended Run Sequence)
1. `python fetch_prices.py`
2. `python fetch_fund_nav.py`
3. `python analyze_portfolio.py`
4. `python alert_monitor.py`
