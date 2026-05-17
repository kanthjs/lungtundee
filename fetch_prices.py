#!/usr/bin/env python3
"""
fetch_prices.py — ดึงราคา real-time ของสินทรัพย์ในพอร์ต lungtundee
และบันทึกลงไฟล์ live_prices.json

การใช้งาน:
    pip install yfinance
    python fetch_prices.py
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance ยังไม่ได้ติดตั้ง — รัน: pip install yfinance")
    sys.exit(1)

# หุ้น/ETF ในพอร์ต Kant ที่เทรดใน exchange จริง
# LAND = Gladstone Land Corp (NASDAQ), ไม่ใช่ LAND.BK
STOCK_TICKERS = ["SCB.BK", "LAND", "VOO", "JEPQ", "CTVA", "SIVR", "SCHD"]

# อัตราแลกเปลี่ยน: THB=X คือ USD/THB (1 USD = ? THB) ใน yfinance
FX_TICKER = "THB=X"

OUTPUT_FILE = Path(__file__).parent / "live_prices.json"


def fetch_one(ticker: str) -> dict:
    """ดึงราคาล่าสุดของ ticker หนึ่งตัว ใช้ fast_info ก่อน fallback ไป history"""
    try:
        t = yf.Ticker(ticker)
        info = t.fast_info

        price = info.last_price
        prev_close = info.previous_close

        if price is None:
            hist = t.history(period="5d")
            if hist.empty:
                return {"price": None, "prev_close": None, "change_pct": None, "error": "no data from yfinance"}
            price = float(hist["Close"].iloc[-1])
            prev_close = float(hist["Close"].iloc[-2]) if len(hist) >= 2 else None

        change_pct = None
        if price is not None and prev_close is not None and prev_close != 0:
            change_pct = round((price - prev_close) / prev_close * 100, 4)

        return {
            "price": round(float(price), 4) if price is not None else None,
            "prev_close": round(float(prev_close), 4) if prev_close is not None else None,
            "change_pct": change_pct,
        }
    except Exception as e:
        return {"price": None, "prev_close": None, "change_pct": None, "error": str(e)}


def main() -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"\n[{datetime.now():%Y-%m-%d %H:%M:%S}] กำลังดึงราคา real-time...\n")

    prices: dict[str, dict] = {}

    all_tickers = STOCK_TICKERS + [FX_TICKER]
    for ticker in all_tickers:
        data = fetch_one(ticker)
        prices[ticker] = data

        if data.get("error"):
            label = f"ERROR: {data['error']}"
        elif ticker == FX_TICKER:
            label = f"{data['price']:.4f} THB/USD"
        else:
            sign = "+" if (data["change_pct"] or 0) >= 0 else ""
            label = f"{data['price']:.4f}  ({sign}{data['change_pct']:.2f}%)" if data["change_pct"] is not None else str(data["price"])
        print(f"  {ticker:<12} {label}")

    output = {
        "fetched_at": timestamp,
        "note": "ราคา real-time จาก yfinance — ใช้กับ Portfolio Monitor เท่านั้น",
        "prices": prices,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✓ บันทึกแล้วที่: {OUTPUT_FILE}")
    return output


if __name__ == "__main__":
    main()
