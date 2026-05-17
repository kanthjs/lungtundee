# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
fetch_nav.py -- ดึง NAV กองทุนรวมไทยจาก SEC Open API
อัปเดต mutual_funds.csv (Kant) โดยอัตโนมัติ

Setup (ทำครั้งแรกครั้งเดียว):
  1. ลงทะเบียนที่ https://api-portal.sec.or.th
  2. Subscribe: "Fund Factsheet API" + "Fund Daily Info API"
  3. สร้างไฟล์ .env ใน project root:
       FACTSHEET_KEY=your_key_here
       DAILYINFO_KEY=your_key_here
  4. pip install requests python-dotenv

Usage:
  python fetch_nav.py                # ดึง NAV วันนี้
  python fetch_nav.py --refresh-map  # rebuild fund mapping (ถ้าเพิ่มกองใหม่)
"""

import csv
import json
import sys
import io
import time
import os
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("ERROR: requests ยังไม่ติดตั้ง -- รัน: pip install requests")
    sys.exit(1)

# ── Load .env (optional) ──────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Config ────────────────────────────────────────────────────────────────────
ROOT        = Path(__file__).parent
KANT_DIR    = ROOT / "sources/portfolio/kant"
FUNDS_CSV   = KANT_DIR / "mutual_funds.csv"
MAP_CACHE   = ROOT / "sources/portfolio/nav_fund_map.json"

FACTSHEET_KEY = os.getenv("FACTSHEET_KEY", "")
DAILYINFO_KEY = os.getenv("DAILYINFO_KEY", "")

BASE_FACTSHEET = "https://api.sec.or.th/FundFactsheet"
BASE_DAILYINFO = "https://api.sec.or.th/FundDailyInfo"

# Manual mapping: CSV fund name → SEC proj_abbr_name
# ใช้เมื่อ abbreviation ใน CSV ไม่ตรงกับ SEC (เช่น มี class suffix -E/-D/-N)
MANUAL_SEC_NAME = {
    "UCHINA":          "UCHINA-M",
    "UEMIF-N":         "UEMIF",
    "KKP NDQ100-UH-E": "KKP NDQ100-UH FUND",
    "KKP US500-UH-E":  "KKP US500-UH FUND",
    "KT-INDIA-D":      "KT-INDIA",
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def factsheet_headers():
    return {"Ocp-Apim-Subscription-Key": FACTSHEET_KEY}

def dailyinfo_headers():
    return {"Ocp-Apim-Subscription-Key": DAILYINFO_KEY}


def get_all_amcs() -> list:
    r = requests.get(f"{BASE_FACTSHEET}/fund/amc", headers=factsheet_headers(), timeout=30)
    r.raise_for_status()
    return r.json()


def get_funds_for_amc(unique_id: str) -> list:
    r = requests.get(f"{BASE_FACTSHEET}/fund/amc/{unique_id}",
                     headers=factsheet_headers(), timeout=30)
    if r.status_code == 200:
        return r.json()
    return []


def build_fund_map(target_csv_names: set) -> dict:
    """
    Build {csv_fund_name: proj_id} mapping by scanning SEC API.
    Uses MANUAL_SEC_NAME to translate CSV names → SEC abbreviations when needed.
    Returns mapping keyed by original CSV fund name.
    """
    # Resolve SEC abbreviations (some CSV names differ from SEC proj_abbr_name)
    sec_to_csv = {}  # SEC abbr → CSV name
    sec_targets = set()
    for csv_name in target_csv_names:
        sec_name = MANUAL_SEC_NAME.get(csv_name, csv_name)
        sec_to_csv[sec_name] = csv_name
        sec_targets.add(sec_name)

    print(f"Building fund map (scanning SEC API for {len(sec_targets)} funds)...")
    raw_map = {}  # SEC abbr → proj_id
    amcs = get_all_amcs()
    print(f"  Found {len(amcs)} AMCs -- scanning...")

    for amc in amcs:
        uid = amc.get("unique_id")
        if not uid:
            continue
        funds = get_funds_for_amc(uid)
        for f in funds:
            abbr = (f.get("proj_abbr_name") or "").strip()
            if abbr in sec_targets and abbr not in raw_map:
                raw_map[abbr] = f["proj_id"]
                csv_name = sec_to_csv[abbr]
                print(f"  Found: {csv_name:<24} ({abbr}) proj_id={f['proj_id']}")
        time.sleep(0.05)
        if len(raw_map) >= len(sec_targets):
            print("  All targets found -- stopping scan early")
            break

    # Convert back to CSV-name keyed mapping
    mapping = {sec_to_csv[sec]: pid for sec, pid in raw_map.items()}

    not_found = target_csv_names - set(mapping.keys())
    if not_found:
        print(f"  Warning: not found in SEC API: {not_found}")

    return mapping


def _class_suffix(csv_name: str) -> str | None:
    """Extract share-class suffix from CSV name.
    e.g. 'KKP NDQ100-UH-E' → 'E', 'KT-INDIA-D' → 'D', 'UEMIF-N' → 'N'
    Returns None if no single-letter suffix found.
    """
    parts = csv_name.split("-")
    if len(parts) >= 2 and len(parts[-1]) == 1 and parts[-1].isalpha():
        return parts[-1].upper()
    return None


def fetch_nav_for_date(proj_id: str, nav_date: str, class_suffix: str | None = None) -> float | None:
    """
    Fetch NAV for a single proj_id on nav_date (YYYY-MM-DD).
    Handles both list and dict responses.
    If class_suffix given, filters by class_abbr_name; otherwise returns first entry.
    Returns None if 204 (no data) or error.
    """
    url = f"{BASE_DAILYINFO}/{proj_id}/dailynav/{nav_date}"
    r = requests.get(url, headers=dailyinfo_headers(), timeout=15)
    if r.status_code != 200:
        return None
    data = r.json()
    # Normalise to list
    items = data if isinstance(data, list) else [data]
    if not items:
        return None
    # Filter by class suffix if provided
    if class_suffix:
        matched = [i for i in items if i.get("class_abbr_name", "").upper() == class_suffix]
        if matched:
            items = matched
    item = items[0]
    val  = item.get("last_val") or item.get("nav") or item.get("value")
    try:
        return float(val) if val else None
    except (TypeError, ValueError):
        return None


def latest_nav(proj_id: str, start: datetime, lookback: int = 7,
               class_suffix: str | None = None) -> tuple:
    """
    Try start date and up to lookback days back to find most recent NAV.
    Returns (nav_value, date_str) or (None, "").
    """
    for delta in range(lookback):
        d = (start - timedelta(days=delta)).strftime("%Y-%m-%d")
        val = fetch_nav_for_date(proj_id, d, class_suffix)
        if val:
            return val, d
        time.sleep(0.05)
    return None, ""


# ── CSV helpers ───────────────────────────────────────────────────────────────
def read_fund_names() -> list:
    names = []
    if not FUNDS_CSV.exists():
        return names
    with open(FUNDS_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            n = r.get("Fund_Name", "").strip()
            if n:
                names.append(n)
    return names


def read_full_csv() -> tuple:
    """Returns (fieldnames, rows_as_dicts, old_nav_col_name)."""
    with open(FUNDS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows   = [dict(r) for r in reader]

    # Detect old NAV column (any col starting with NAV that isn't Avg_NAV)
    old_nav_col = None
    for col in fields:
        c = col.strip()
        if c.startswith("NAV") and c != "Avg_NAV":
            old_nav_col = col
            break

    return fields, rows, old_nav_col


def thai_date_suffix(dt: datetime) -> str:
    """Convert datetime to DDMMYY (Buddhist Era year last 2 digits) e.g. 170569"""
    be_year = str(dt.year + 543)[-2:]
    return f"{dt.strftime('%d%m')}{be_year}"


def update_csv(nav_map: dict, today: datetime, old_rows: list, old_nav_col: str | None):
    """Rewrite mutual_funds.csv with updated NAV column."""
    nav_col   = f"NAV(at{thai_date_suffix(today)})"
    new_fields = ["Fund_Name", "Units", "Avg_NAV", nav_col]

    with open(FUNDS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=new_fields)
        writer.writeheader()
        for r in old_rows:
            name = r.get("Fund_Name", "").strip()
            if not name:
                continue
            new_nav = nav_map.get(name)
            if new_nav is None and old_nav_col:
                # fallback: keep existing NAV from previous column
                try:
                    existing = float(r.get(old_nav_col, "") or 0)
                    new_nav  = existing if existing else None
                except ValueError:
                    new_nav = None
            writer.writerow({
                "Fund_Name": name,
                "Units":     r.get("Units", ""),
                "Avg_NAV":   r.get("Avg_NAV", ""),
                nav_col:     f"{new_nav:.4f}" if new_nav else "",
            })

    print(f"\nUpdated: {FUNDS_CSV}")
    print(f"  NAV column: {nav_col}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if not FACTSHEET_KEY or not DAILYINFO_KEY:
        print("=" * 60)
        print("ERROR: ยังไม่ได้ตั้งค่า API Keys")
        print()
        print("ขั้นตอน:")
        print("  1. ไปที่ https://api-portal.sec.or.th")
        print("     (หรือ https://secopendata.sec.or.th สำหรับ portal ใหม่)")
        print("  2. Register / Login")
        print("  3. Subscribe: Fund Factsheet API + Fund Daily Info API")
        print("  4. สร้างไฟล์ .env ใน F:\\Github\\lungtundee\\")
        print("     เพิ่ม 2 บรรทัด:")
        print("       FACTSHEET_KEY=ใส่ key ตรงนี้")
        print("       DAILYINFO_KEY=ใส่ key ตรงนี้")
        print("  5. รัน: pip install python-dotenv  (ถ้ายังไม่ได้ติดตั้ง)")
        print("  6. รัน: python fetch_nav.py อีกครั้ง")
        print("=" * 60)
        sys.exit(1)

    refresh_map = "--refresh-map" in sys.argv
    today       = datetime.now()
    fund_names  = read_fund_names()
    _, old_rows, old_nav_col = read_full_csv()

    if not fund_names:
        print(f"ERROR: ไม่พบข้อมูลใน {FUNDS_CSV}")
        sys.exit(1)

    target_set = set(fund_names)
    print(f"\n[{today:%Y-%m-%d %H:%M:%S}] fetch_nav -- {len(target_set)} กองทุน\n")

    # ── Load or build fund mapping ────────────────────────────────────────────
    if MAP_CACHE.exists() and not refresh_map:
        mapping = json.loads(MAP_CACHE.read_text(encoding="utf-8"))
        print(f"Loaded fund map from cache: {MAP_CACHE.name} ({len(mapping)} entries)")
        missing = target_set - set(mapping.keys())
        if missing:
            print(f"  Missing in cache: {missing} -- fetching...")
            mapping.update(build_fund_map(missing))
            MAP_CACHE.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        mapping = build_fund_map(target_set)
        MAP_CACHE.parent.mkdir(parents=True, exist_ok=True)
        MAP_CACHE.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved fund map: {MAP_CACHE.name}")

    # ── Fetch NAV for each fund ───────────────────────────────────────────────
    print(f"\nFetching NAV (as of {today.strftime('%Y-%m-%d')}, lookback 7 days)...\n")
    nav_map  = {}
    failed   = []

    for name in fund_names:
        proj_id = mapping.get(name)
        if not proj_id:
            print(f"  {name:<22} proj_id not in map -- skip (run --refresh-map?)")
            failed.append(name)
            continue

        cls_suffix = _class_suffix(name)
        nav, date_used = latest_nav(proj_id, today, class_suffix=cls_suffix)
        if nav:
            nav_map[name] = nav
            tag = f"(as of {date_used})" if date_used != today.strftime("%Y-%m-%d") else "(today)"
            print(f"  {name:<22} NAV = {nav:.4f}  {tag}")
        else:
            print(f"  {name:<22} no data (7-day lookback) -- keeping existing")
            failed.append(name)

    if not nav_map:
        print("\nERROR: ดึง NAV ไม่ได้เลย -- ตรวจสอบ API keys และการเชื่อมต่อ")
        sys.exit(1)

    # ── Update CSV ────────────────────────────────────────────────────────────
    update_csv(nav_map, today, old_rows, old_nav_col)

    if failed:
        print(f"\nWarning: {len(failed)} กองที่อัปเดตไม่ได้: {failed}")
        print("  NAV คงค่าเดิมจาก CSV ก่อนหน้า")

    success = len(fund_names) - len(failed)
    print(f"\nDone: {success}/{len(fund_names)} กองอัปเดตสำเร็จ")
    print("Next: python generate_dashboard.py")


if __name__ == "__main__":
    main()
