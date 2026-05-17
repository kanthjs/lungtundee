#!/usr/bin/env python3
"""
analyze_portfolio.py — คำนวณภาพรวมพอร์ตการลงทุน (Math Engine)
อ่านข้อมูลจาก CSV และราคาล่าสุด แล้วสรุปออกมาเป็น Markdown
เพื่อลดความผิดพลาดในการคำนวณของ AI
"""

import csv
import json
from pathlib import Path
from datetime import datetime

# Paths
PORTFOLIOS = {
    'Kant': {
        'mf': Path("sources/portfolio/kant/mutual_funds.csv"),
        'holdings': Path("sources/portfolio/kant/holdings.csv")
    },
    'Me-Tang': {
        'mf': Path("sources/portfolio/me-tang/mutual_funds.csv"),
        'holdings': Path("sources/portfolio/me-tang/holdings.csv")
    }
}
LIVE_PRICES = Path("live_prices.json")
SUMMARY_FILE = Path("sources/portfolio_summary.md")

def load_prices():
    """โหลดราคาล่าสุดจากไฟล์ JSON"""
    if not LIVE_PRICES.exists():
        print(f"[WARNING] ไม่พบไฟล์ {LIVE_PRICES} จะใช้ราคาจาก CSV แทน")
        return {}
    with open(LIVE_PRICES, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('prices', {})

def get_ticker_price(ticker, market, prices):
    """หาค่าราคาปัจจุบันของ ticker จากข้อมูลราคา real-time"""
    yf_ticker = ticker
    if market == 'SET':
        yf_ticker = f"{ticker}.BK"
    
    # ลองหาแบบ yf_ticker (เช่น SCB.BK)
    data = prices.get(yf_ticker)
    if data and data.get('price'):
        return data['price']
    
    # ลองหาแบบชื่อตรงๆ (เช่น VOO, LAND)
    data = prices.get(ticker)
    if data and data.get('price'):
        return data['price']
        
    return None

def analyze():
    prices = load_prices()
    # ดึงอัตราแลกเปลี่ยน ถ้าไม่มีใช้ 35.0 เป็นค่าเริ่มต้น
    usd_thb = prices.get('THB=X', {}).get('price', 35.0)
    
    report = [f"# Portfolio Analysis Summary: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]
    report.append(f"**USD/THB Rate (Reference):** {usd_thb:.4f}\n")

    for name, paths in PORTFOLIOS.items():
        report.append(f"## Portfolio: {name}")
        total_cost_thb = 0
        total_value_thb = 0
        items = []
        
        # 1. ประมวลผลหุ้น/ETF (Holdings)
        if paths['holdings'].exists():
            with open(paths['holdings'], 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        shares = float(row['Shares'] or 0)
                        avg_price = float(row['Avg_Price'] or 0)
                        currency = row['Currency']
                        market = row['Market']
                        ticker = row['Ticker']
                    except (ValueError, KeyError):
                        continue
                    
                    if shares == 0: continue
                    
                    curr_price = get_ticker_price(ticker, market, prices)
                    if curr_price is None: 
                        curr_price = avg_price # ถ้าไม่มีราคาล่าสุด ให้ใช้ราคาทุนไปก่อน
                    
                    cost_native = shares * avg_price
                    value_native = shares * curr_price
                    
                    if currency == 'USD':
                        cost_thb = cost_native * usd_thb
                        value_thb = value_native * usd_thb
                    else:
                        cost_thb = cost_native
                        value_thb = value_native
                    
                    pnl_thb = value_thb - cost_thb
                    pnl_pct = (pnl_thb / cost_thb * 100) if cost_thb != 0 else 0
                    
                    items.append({
                        'name': ticker,
                        'value': value_thb,
                        'cost': cost_thb,
                        'pnl_pct': pnl_pct,
                        'type': 'Stock/ETF'
                    })
                    total_cost_thb += cost_thb
                    total_value_thb += value_thb

        # 2. ประมวลผลกองทุนรวม (Mutual Funds)
        if paths['mf'].exists():
            with open(paths['mf'], 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        units = float(row['Units'] or 0)
                        avg_nav = float(row['Avg_NAV'] or 0)
                        curr_nav = float(row['Current_NAV'] or 0)
                    except (ValueError, KeyError):
                        continue
                        
                    if units == 0: continue
                    
                    cost_thb = units * avg_nav
                    value_thb = units * curr_nav
                    pnl_thb = value_thb - cost_thb
                    pnl_pct = (pnl_thb / cost_thb * 100) if cost_thb != 0 else 0
                    
                    items.append({
                        'name': row['Fund_Name'],
                        'value': value_thb,
                        'cost': cost_thb,
                        'pnl_pct': pnl_pct,
                        'type': 'Mutual Fund'
                    })
                    total_cost_thb += cost_thb
                    total_value_thb += value_thb

        # 3. สรุปผลลัพธ์และคำนวณสัดส่วน (%)
        if total_value_thb > 0:
            pnl_total = total_value_thb - total_cost_thb
            pnl_total_pct = (pnl_total / total_cost_thb * 100) if total_cost_thb != 0 else 0
            
            report.append(f"- **Total Value:** {total_value_thb:,.2f} THB")
            report.append(f"- **Total Cost:** {total_cost_thb:,.2f} THB")
            report.append(f"- **Total P&L:** {pnl_total:,.2f} THB ({pnl_total_pct:+.2f}%)")
            report.append("\n| Asset | Type | Weight | P&L % |")
            report.append("| :--- | :--- | :--- | :--- |")
            
            # เรียงลำดับตามมูลค่า (Weight) จากมากไปน้อย
            items.sort(key=lambda x: x['value'], reverse=True)
            for item in items:
                weight = (item['value'] / total_value_thb) * 100
                report.append(f"| {item['name']} | {item['type']} | {weight:.2f}% | {item['pnl_pct']:+.2f}% |")
        else:
            report.append("- Portfolio นี้ไม่มีข้อมูลสินทรัพย์หรือราคาปัจจุบัน")
        
        report.append("\n---\n")

    # บันทึกไฟล์สรุป
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print(f"✓ วิเคราะห์เสร็จสิ้น! บันทึกสรุปแล้วที่: {SUMMARY_FILE}")

if __name__ == "__main__":
    analyze()
