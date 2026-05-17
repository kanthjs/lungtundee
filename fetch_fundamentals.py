#!/usr/bin/env python3
"""
fetch_fundamentals.py — ดึงข้อมูลปัจจัยพื้นฐาน (Financial Ratios)
เพื่อใช้ประกอบการทำ Stock Brief
"""

import json
import sys
try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance ยังไม่ได้ติดตั้ง")
    sys.exit(1)

def fetch_fundamentals(ticker: str) -> dict:
    """ดึงข้อมูลพื้นฐานที่สำคัญจาก Yahoo Finance"""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        
        # กรองเอาเฉพาะข้อมูลที่จำเป็นต่อการวิเคราะห์
        data = {
            "ticker": ticker,
            "name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "pb_ratio": info.get("priceToBook"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "profit_margins": info.get("profitMargins"),
            "revenue_growth": info.get("revenueGrowth"),
            "dividend_yield": info.get("dividendYield"),
            "payout_ratio": info.get("dividendPayoutRatio"),
            "beta": info.get("beta")
        }
        
        # ปรับหน่วยให้อ่านง่ายขึ้น (%)
        for key in ["roe", "roa", "profit_margins", "revenue_growth", "dividend_yield"]:
            if data[key] is not None:
                data[key] = round(data[key] * 100, 2)
                
        return data
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_fundamentals.py <TICKER>")
        sys.exit(1)
    
    ticker = sys.argv[1]
    # ปรับ Ticker สำหรับหุ้นไทยถ้ายังไม่มี .BK
    if ticker.isalpha() and len(ticker) <= 5 and not ticker.endswith(".BK"):
        # ไม่กล้าแก้ auto กลัวพังกับหุ้น US
        pass
        
    result = fetch_fundamentals(ticker)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
