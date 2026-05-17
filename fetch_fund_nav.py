import requests
import re
import csv
import json
from pathlib import Path

def get_nav(fund_name):
    """ดึงราคา NAV ล่าสุดจาก Finnomena"""
    try:
        url = f"https://www.finnomena.com/fund/{fund_name}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            return None
        
        # ค้นหา JSON block ใน __NUXT__
        # เราจะหา nav ที่อยู่ใกล้กับคำว่า fundCode:"TICKER" มากที่สุด
        # หรือหาตัวที่อยู่ใน block ข้อมูลหลัก
        
        # ลองหาแบบเจาะจง fundCode
        pattern = f'\"fundCode\":\"{fund_name}\".*?\"nav\":([0-9.]+)'
        match = re.search(pattern, r.text)
        if match:
            return float(match.group(1))
            
        # ลองหาแบบเจาะจงล่าสุด
        pattern = f'\"fundCode\":\"{fund_name}\".*?\"latest_nav\":([0-9.]+)'
        match = re.search(pattern, r.text)
        if match:
            return float(match.group(1))

        # ถ้าไม่เจอ ลองหา nav ตัวแรกที่เจอ (มักจะเป็นตัวหลัก)
        match = re.search(r'\"nav\":([0-9.]+)', r.text)
        if match:
            val = float(match.group(1))
            if 1 < val < 1000:
                return val
                
    except Exception as e:
        print(f"Error {fund_name}: {e}")
    return None

def update_csv(file_path):
    if not file_path.exists(): return
    rows = []
    updated = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            fund_name = row['Fund_Name']
            nav = get_nav(fund_name)
            if nav:
                # ตรวจสอบว่าไม่ใช่เลข benchmark ยอดฮิต (27.598, 9.9057)
                # ถ้าใช่ ให้ลองหาตัวอื่นใน text
                if round(nav, 4) in [27.598, 9.9057]:
                    all_navs = re.findall(r'\"nav\":([0-9.]+)', requests.get(f"https://www.finnomena.com/fund/{fund_name}", headers={"User-Agent": "Mozilla/5.0"}).text)
                    for n in all_navs:
                        n_val = float(n)
                        if round(n_val, 4) not in [27.598, 9.9057] and 1 < n_val < 500:
                            nav = n_val
                            break
                
                row['Current_NAV'] = round(nav, 4)
                print(f"  ✓ {fund_name:<15} : {nav:.4f}")
                updated += 1
            else:
                print(f"  ? {fund_name:<15} : Not Found")
            rows.append(row)
            
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Done {file_path}, updated {updated}\n")

if __name__ == "__main__":
    print("=== Lungtundee Fund NAV Fetcher ===")
    paths = [Path("sources/portfolio/kant/mutual_funds.csv"), Path("sources/portfolio/me-tang/mutual_funds.csv")]
    for p in paths:
        update_csv(p)
