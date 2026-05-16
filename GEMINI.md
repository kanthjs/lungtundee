# Project: lungtundee (ลงทุนดี)

**Overview:**  
"ลงทุนดี" is a Personal AI Fund Manager system designed to manage stock and mutual fund portfolios. It employs a Multi-Agent architecture to synthesize fundamental analysis, technical timing, and portfolio monitoring into actionable investment decisions led by a Chief Investment Officer (CIO).

## Core Architecture & Agents
The system resides in `.claude/agents/` and follows a strict synthesis workflow:
- **CIO (Chief Investment Officer):** The final decision-maker. Synthesizes reports from other agents to recommend cash deployment.
- **Fundamental Analyst:** Evaluates business quality and intrinsic value (What to buy).
- **Technical Analyst:** Analyzes price action and indicators for entry/exit timing (When to buy).
- **Portfolio Monitor:** Tracks current holdings, P&L, and alerts on status.

## Investment Strategy (Investor Profile)
- **Style:** Value Investing (Fundamentals-first) + Technical Timing.
- **Time Horizon:** Medium (1–6 months).
- **Universe:** SET (Thai), US (NYSE/NASDAQ), Global ETFs, Mutual Funds.
- **Risk Management:** 
  - Moderate tolerance (15–25% drawdown).
  - Position sizing: Never all-in; scale into positions (Max 20% of cash per decision).
  - Kill Condition: Thesis change or >25% unexplained drawdown.

## Directory Structure
- `briefs/`: Research reports and investment theses.
  - `SET/`, `US/`, `Commodity/`: Stock-specific briefs.
  - `Funds/`: Mutual fund policy and performance analysis.
- `sources/portfolio/`: Data files for the portfolios.
  - `kant/`: Personal Portfolio (คุณ Kant).
    - `holdings.csv`: Current stock positions.
    - `mutual_funds.csv`: Current mutual fund positions.
    - `portfolio-plan-kant.md`: Strategic roadmap based on real holdings.
  - `me-tang/`: AI Autonomous Portfolio (20,000 THB).
    - `holdings.csv`: Stock positions for the AI's fund.
    - `mutual_funds.csv`: Mutual fund positions for the AI's fund.
    - `transactions.csv`: Transaction history for the AI's fund.
    - `portfolio-plan-20k.md`: AI fund's roadmap and execution plan.
- `.claude/agents/`: Definitions and system prompts for each agent.
- `logs/`: Investment journal entries recording "Why" behind every trade and portfolio reviews.

## Operational Workflows

### 1. Stock & Fund Research (`/brief`)
When analyzing a new asset:
1. Invoke **Fundamental Analyst** (for stocks) or research Fund Policy (for funds).
2. Invoke **Technical Analyst** to find entry/exit zones.
3. Save the combined report into `briefs/<CATEGORY>/<TICKER_OR_NAME>.md`.

### 2. Consolidated Portfolio Analysis & Advice
When the user asks about their portfolio, Me-Tang **MUST**:
1. **Synthesize:** Combine data from both `kant/` and `me-tang/` (Stocks + Mutual Funds).
2. **Check Overlap:** Identify if any stock is already a major holding in a mutual fund.
3. **Advise:** Provide a clear **"Path Forward"** (Actionable Solution).
4. **Decide:** State a firm recommendation (**BUY / SELL / HOLD / REBALANCE**) with specific rationale.
5. **Execute:** Suggest the next immediate step and record it in `logs/YYYY-MM-DD-portfolio-review.md`.

### 3. Portfolio Monitoring
1. **Portfolio Monitor** reads CSV files from both `kant/` and `me-tang/`.
2. Flags alerts (Stop loss breach, unusual moves, NAV updates) for each portfolio separately.

## Development Conventions
- **Language:** Supports both Thai and English. **Thai is preferred for final verdicts.**
- **Data Integrity:** ALWAYS prefer CSV files for numerical calculations over Markdown text.
- **Safety:** Never modify files outside the project root. Ask for permission before large deletions.
- **Precision:** Avoid hedging in decisions. Use "BUY/WAIT/REDUCE/HOLD".
- **Me-Tang Mandate:** Always provide a solution, not just a status report.
- **Me-Tang Fund:** The `me-tang/` portfolio is the AI's benchmark for proving its capabilities.

## Commands & Tools (TODO)
- Currently using manual agent invocation and file editing.
- Future: Automated scripts for CSV updates and price fetching.
