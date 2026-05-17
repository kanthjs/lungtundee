# Project: lungtundee (ลงทุนดี)

**What this is:** ลงทุนดี คือ "ผู้จัดการกองทุนส่วนตัวที่เป็น AI" (Personal AI Fund Manager) เพื่อมาช่วยดูแลพอร์ตหุ้น/หรือกองทุนรวม ที่ถืออยู่ และช่วยตัดสินใจว่าเงินสดที่มีอยู่ควรจะจัดการอย่างไร ครอบคลุมทั้งหุ้น และกองทุนรวม

## Core Architecture & Agents
ระบบใช้ Multi-Agent architecture ที่มี agents อยู่ใน `.claude/agents/` โดยแต่ละตัวมี Persona ชัดเจน:
- **Digital Twin — "มีตัง" (investor-self):** จุดเริ่มต้นการคิดแบบ Inner Monologue และเป็นคนสั่งงานทีม
- **CIO (Chief Investment Officer) — "พี่ขุน" (cio):** ผู้ตัดสินใจขั้นสุดท้าย ให้ "บทสรุป" ที่ชัดเจน
- **Fundamental Analyst — "พี่หมอเงิน" (fundamental-analyst):** วิเคราะห์คุณภาพธุรกิจ (Helmer's 7 Powers) และมูลค่าเหมาะสม
- **Technical Analyst — "พี่หมอดู" (technical-analyst):** วิเคราะห์กราฟ แนวรับ-แนวต้าน และ Technical Indicators
- **Portfolio Monitor — "ยาม" (portfolio-monitor):** เฝ้าพอร์ต แจ้งเตือน Stop Loss และสถานะ P&L

## Directory Structure
- `scripts/`: สคริปต์อัตโนมัติ (อยู่ที่ root)
  - `fetch_prices.py`, `fetch_fund_nav.py`, `fetch_fundamentals.py`
  - `analyze_portfolio.py`, `alert_monitor.py`
- `briefs/`: รายงานวิเคราะห์หุ้นรายตัวแยกตามตลาด (SET, US, Commodity)
- `sources/`: ข้อมูลดิบและไฟล์ติดตามพอร์ต
  - `portfolio/`: ข้อมูล `kant/` (พอร์ตจริง) และ `me-tang/` (พอร์ต AI)
  - `portfolio_summary.md`: **Source of Truth** สรุปภาพรวมพอร์ตที่คำนวณโดย Code (Auto-generated)
  - `live_prices.json`: ข้อมูลราคาและอินดิเคเตอร์ล่าสุด (Auto-generated)
- `logs/`: บันทึกการลงทุน, Portfolio Reviews และ `alerts.md`

## Investor Profile & Strategy
- **สไตล์:** Value Investing + Technical Timing (Medium Term 1–6 เดือน)
- **ตลาด:** SET (ไทย), US (NYSE/NASDAQ), Global ETF, Mutual Funds (SSF/RMF/General)
- **Risk Management:** 
  - Drawdown tolerance: 15–25%
  - Position Sizing: Max 20% ของเงินสดต่อหนึ่งการตัดสินใจ (กฎพี่ขุน)
  - Kill Condition: Thesis เปลี่ยน หรือ drawdown เกิน 25% โดยไม่มีเหตุผล

## Operational Workflows

### 1. Stock & Fund Research (`/brief`)
1. **Data Prep:** รัน `python fetch_fundamentals.py <TICKER>` เพื่อดึงตัวเลขการเงินล่าสุด
2. **Analysis:** ใช้ **พี่หมอเงิน** และ **พี่หมอดู** ทำรายงาน 6 หัวข้อมาตรฐาน
3. **Rules:** ห้ามเชียร์ซื้อ/ขายใน brief, ห้ามใช้คำว่า "moat" (ใช้ specific powers), เน้น Honest > Confident

### 2. Consolidated Portfolio Analysis & Advice
1. **Data Prep:** รัน **Automated Workflow** เพื่ออัปเดต `portfolio_summary.md`
2. **Analysis:** "มีตัง" อ่านสรุปพอร์ตเพื่อหาจุดเสี่ยงหรือโอกาส
3. **Verdict:** "พี่ขุน" สรุปขั้นตอนถัดไป (Path Forward) พร้อมระบุจำนวนเงินและจุดตัดขาดทุน
4. **Log:** บันทึกแผนงานลงใน `logs/YYYY-MM-DD-portfolio-review.md`

## Automated Workflow (รันตามลำดับนี้)
1. `python fetch_prices.py`: ดึงราคาหุ้น + คำนวณ RSI, MA
2. `python fetch_fund_nav.py`: ดึงราคา NAV กองทุนรวมไทย
3. `python analyze_portfolio.py`: คำนวณเลขคณิตศาสตร์พอร์ตทั้งหมด (Math Engine)
4. `python alert_monitor.py`: ตรวจสอบเงื่อนไขการตัดขาดทุนและแจ้งเตือน

## Development Conventions
- **ภาษา:** รองรับทั้งไทยและอังกฤษ **แต่ "บทสรุป" (Verdict) ต้องเป็นภาษาไทยเท่านั้น**
- **Data Integrity:** เชื่อถือตัวเลขจาก CSV และไฟล์สรุปที่คำนวณโดยสคริปต์เท่านั้น ห้าม AI คำนวณเอง
- **Safety:** ไม่แก้ไขไฟล์นอก project root, ไม่ลบไฟล์โดยไม่แจ้ง
- **Me-Tang Mandate:** ต้องให้ Solution เสมอ ไม่ใช่แค่รายงานสถานะ
