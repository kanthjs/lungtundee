#!/usr/bin/env python3
"""
alert_monitor.py — ตรวจสอบสถานะพอร์ตและแจ้งเตือนตาม Kill Conditions
รันหลังดึงราคาเสร็จเพื่อตรวจสอบว่ามีตัวไหนต้อง "หนี" หรือไม่
"""

import json
import csv
from pathlib import Path
from datetime import datetime

# Paths
LIVE_PRICES = Path("live_prices.json")
PORTFOLIO_PATHS = [
    Path("sources/portfolio/kant/holdings.csv"),
    Path("sources/portfolio/me-tang/holdings.csv")
]
ALERTS_LOG = Path("logs/alerts.md")

def check_drawdown():
    if not LIVE_PRICES.exists():
        print("[SKIP] ไม่พบ live_prices.json")
        return []
    
    with open(LIVE_PRICES, 'r', encoding='utf-8') as f:
        price_data = json.load(f)
        prices = price_data.get('prices', {})
        
    alerts = []
    
    for p_path in PORTFOLIO_PATHS:
        if not p_path.exists(): continue
        
        with open(p_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ticker = row['Ticker']
                avg_price = float(row['Avg_Price'] or 0)
                
                # หาค่าราคาปัจจุบัน (จัดการ .BK สำหรับหุ้นไทย)
                curr_price = None
                yf_ticker = f"{ticker}.BK" if row.get('Market') == 'SET' else ticker
                if yf_ticker in prices:
                    curr_price = prices[yf_ticker].get('price')
                elif ticker in prices:
                    curr_price = prices[ticker].get('price')
                    
                if curr_price and avg_price > 0:
                    drawdown = (curr_price - avg_price) / avg_price * 100
                    
                    # Kill Condition: Drawdown > 25% (ตาม GEMINI.md)
                    if drawdown <= -25.0:
                        alerts.append({
                            "portfolio": p_path.parent.name,
                            "ticker": ticker,
                            "drawdown": round(drawdown, 2),
                            "price": curr_price,
                            "avg": avg_price,
                            "severity": "CRITICAL"
                        })
                    # Warning: Drawdown > 15%
                    elif drawdown <= -15.0:
                        alerts.append({
                            "portfolio": p_path.parent.name,
                            "ticker": ticker,
                            "drawdown": round(drawdown, 2),
                            "price": curr_price,
                            "avg": avg_price,
                            "severity": "WARNING"
                        })
    return alerts

def main():
    print("=== Lungtundee Alert Monitor ===")
    alerts = check_drawdown()
    
    if not alerts:
        print("✓ ไม่พบความเสี่ยงที่ผิดปกติ")
        return

    # บันทึกหรือแสดงผลการแจ้งเตือน
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = [f"## Portfolio Alerts: {timestamp}\n"]
    
    for a in alerts:
        icon = "🚨" if a['severity'] == "CRITICAL" else "⚠️"
        msg = f"{icon} **{a['severity']}**: {a['ticker']} ({a['portfolio']}) ร่วงลง {a['drawdown']}% (ราคา: {a['price']}, ทุน: {a['avg']})"
        print(f"  {msg}")
        report.append(f"- {msg}")

    # เขียนลงไฟล์ log อัปเดตล่าสุด
    with open(ALERTS_LOG, 'a', encoding='utf-8') as f:
        f.write("\n".join(report) + "\n\n")
    
    print(f"\n✓ บันทึกการแจ้งเตือนแล้วที่: {ALERTS_LOG}")

if __name__ == "__main__":
    main()
