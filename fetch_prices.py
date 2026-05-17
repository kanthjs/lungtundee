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
    import pandas as pd
except ImportError:
    print("ERROR: yfinance หรือ pandas ยังไม่ได้ติดตั้ง — รัน: pip install yfinance pandas")
    sys.exit(1)

# หุ้น/ETF ในพอร์ต Kant ที่เทรดใน exchange จริง
# LAND = Gladstone Land Corp (NASDAQ), ไม่ใช่ LAND.BK
STOCK_TICKERS = ["SCB.BK", "LAND", "VOO", "JEPQ", "CTVA", "SIVR", "SCHD"]

# อัตราแลกเปลี่ยน: THB=X คือ USD/THB (1 USD = ? THB) ใน yfinance
FX_TICKER = "THB=X"

OUTPUT_FILE = Path(__file__).parent / "live_prices.json"


def fetch_one(ticker: str) -> dict:
    """ดึงราคาล่าสุดและคำนวณ Technical Indicators"""
    try:
        t = yf.Ticker(ticker)
        
        # ดึงประวัติย้อนหลัง 1 ปีเพื่อคำนวณ Indicators
        hist = t.history(period="1y")
        if hist.empty:
            return {"price": None, "prev_close": None, "change_pct": None, "error": "no data from yfinance"}
        
        last_row = hist.iloc[-1]
        prev_row = hist.iloc[-2] if len(hist) >= 2 else last_row
        
        price = float(last_row["Close"])
        prev_close = float(prev_row["Close"])
        
        # คำนวณ Moving Averages
        ma20 = hist["Close"].rolling(window=20).mean().iloc[-1]
        ma50 = hist["Close"].rolling(window=50).mean().iloc[-1]
        ma200 = hist["Close"].rolling(window=200).mean().iloc[-1]
        
        # คำนวณ RSI (14)
        delta = hist["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))

        change_pct = None
        if prev_close != 0:
            change_pct = round((price - prev_close) / prev_close * 100, 4)

        return {
            "price": round(float(price), 4),
            "prev_close": round(float(prev_close), 4),
            "change_pct": change_pct,
            "indicators": {
                "ma20": round(float(ma20), 4) if not pd.isna(ma20) else None,
                "ma50": round(float(ma50), 4) if not pd.isna(ma50) else None,
                "ma200": round(float(ma200), 4) if not pd.isna(ma200) else None,
                "rsi": round(float(rsi), 2) if not pd.isna(rsi) else None,
            }
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
