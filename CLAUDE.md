# Project: lungtundee (ลงทุนดี)

<<<<<<< HEAD
**What this is:** ลงทุนดี คือ "ผู้จัดการกองทุนส่วนตัวที่เป็น AI" (Personal AI Fund Manager) เพื่อมาช่วยดูแลพอร์ตหุ้น/หรือกองทุนรวม ที่ถืออยู่ และช่วยตัดสินใจว่าเงินสดที่มีอยู่ควรจะจัดการอย่างไร การออกแบบ Workflow, Agents และ Skills สำหรับตลาดหุ้น/กองทุนรวมโดยเฉพาะ

## Core Architecture & Agents
ระบบใช้ Multi-Agent architecture ที่มี agents อยู่ใน `.claude/agents/`:
- **CIO (Chief Investment Officer):** ตัดสินใจขั้นสุดท้าย สรุปรายงานจาก agents อื่น แล้วแนะนำว่าควรจะลงทุนเงินสดยังไง
- **Fundamental Analyst:** ประเมินคุณภาพธุรกิจและ Intrinsic Value (ซื้ออะไร)
- **Technical Analyst:** วิเคราะห์ price action และ indicators หาจังหวะเข้า-ออก (ซื้อ-ขายเมื่อไหร่)
- **Portfolio Monitor:** ติดตาม holdings ปัจจุบัน P&L และแจ้งเตือนสถานะ
=======
**What this is:** ลงทุนดี คือ "ผู้จัดการกองทุนส่วนตัวที่เป็น AI" (Personal AI Fund Manager) เพื่อมาช่วยดูแลพอร์ตที่ถืออยู่ และช่วยตัดสินใจว่าเงินสดที่มีอยู่ควรจะจัดการอย่างไร ครอบคลุมทั้งหุ้น และกองทุนรวม
>>>>>>> claude/charming-mcclintock-1c96d8

## What lives where

### Briefs & Research
- `briefs/` สำหรับ stock brief ที่ /brief สร้าง
  - `SET/` — หุ้นไทย
  - `US/` — หุ้นอเมริกา
  - `Commodity/` — สินค้าโภคภัณฑ์
  - `Funds/` — กองทุนรวม

### Portfolio Data
- `sources/portfolio/` ข้อมูลพอร์ต
  - `kant/` — Personal Portfolio (คุณ Kant)
    - `holdings.csv` — หุ้นที่ถืออยู่
    - `mutual_funds.csv` — กองทุนรวมที่ถืออยู่
    - `portfolio-plan-kant.md` — แผนการลงทุนระดับสูง
  - `me-tang/` — AI Autonomous Portfolio (20,000 THB)
    - `holdings.csv` — หุ้นของกองทุน AI
    - `mutual_funds.csv` — กองทุนรวมของกองทุน AI
    - `transactions.csv` — ประวัติธุรกรรมของกองทุน AI

### System & Logs
- `.claude/agents/` — คำนิยามและ system prompts ของแต่ละ agent
- `.claude/commands/` — สำหรับ slash command files
- `logs/` — บันทึก journal ของการลงทุน บันทึก "ทำไม" อยู่เบื้องหลังทุก trade และ portfolio reviews
- `sources/ai-compare/` — บันทึกความเห็นจากหลาย AI (Gemini, Claude) เปรียบเทียบ side-by-side
  - `TEMPLATE.md` — เทมเพลตมาตรฐานสำหรับสร้างไฟล์เปรียบเทียบ
- `sources/watchlist.md` — รายการสินทรัพย์ที่เฝ้าติดตาม

## Investor Profile

- **สไตล์:** Value investing — หาของถูกกว่ามูลค่าจริง ใช้ technicals จับจังหวะเข้า
- **Time horizon:** Medium (1–6 เดือน) — รอ catalyst ชัดๆ ไม่ hold ยาวโดยไม่มีเหตุผล
<<<<<<< HEAD
- **ตลาด:** SET (ไทย), US (NYSE/NASDAQ), Global ETF, Mutual Funds
- **Risk tolerance:** Moderate — รับ drawdown ได้ 15–25% ถ้า thesis ยังดี
- **Position sizing:** ไม่ all-in ทีเดียว scale เข้า (Max 20% ของเงินสดต่อการตัดสินใจ)
=======
- **ตลาด:** SET (ไทย), US (NYSE/NASDAQ), Global ETF
- **สินทรัพย์ที่ลงทุนได้:** หุ้นรายตัว, กองทุนรวม (ทั้ง SSF/RMF/กองทั่วไป), ETF
- **กองทุนรวม:** สนใจทั้งกองหุ้นไทย กองหุ้นต่างประเทศ และกองผสม — เลือกตาม fee, track record ของ บลจ. และ consistency ของผลตอบแทน
- **Risk tolerance:** Moderate — รับ drawdown ได้ 15–25% ถ้า thesis ยังดี
- **Position sizing:** ไม่ all-in ทีเดียว scale เข้า ใช้ได้ทั้งหุ้นและกองทุน
>>>>>>> claude/charming-mcclintock-1c96d8
- **Kill condition default:** ถ้า thesis เปลี่ยน หรือ drawdown เกิน 25% โดยไม่มีเหตุผล ออกก่อน

_อัปเดตได้เรื่อยๆ เมื่อเรียนรู้เพิ่ม_

## Operational Workflows

### 1. Stock & Fund Research (`/brief`)
เมื่อวิเคราะห์ asset ใหม่:
1. เรียก **Fundamental Analyst** (สำหรับหุ้น) หรือวิจัย Fund Policy (สำหรับกองทุนรวม)
2. เรียก **Technical Analyst** เพื่อหาโซนเข้า-ออก
3. บันทึกรายงานรวมใน `briefs/<CATEGORY>/<TICKER_OR_NAME>.md`

### 2. Consolidated Portfolio Analysis & Advice
เมื่อ user ถามเรื่องพอร์ต ของตัวเอง Me-Tang **ต้อง**:
1. **Synthesize:** รวมข้อมูลจากทั้ง `kant/` และ `me-tang/` (หุ้น + กองทุนรวม)
2. **Check Overlap:** ตรวจสอบว่าหุ้นไหนเป็น holding หลักในกองทุนรวมอยู่แล้วหรือไม่
3. **Advise:** ให้คำแนะนำ **"Path Forward"** (วิธีแก้ปัญหาที่ทำได้จริง)
4. **Decide:** ระบุคำแนะนำชัดเจน (**BUY / SELL / HOLD / REBALANCE**) พร้อมเหตุผล
5. **Execute:** เสนอขั้นตอนถัดไปที่ทำได้เลย และบันทึกใน `logs/YYYY-MM-DD-portfolio-review.md`

### 3. Portfolio Monitoring
1. **Portfolio Monitor** อ่านไฟล์ CSV จากทั้ง `kant/` และ `me-tang/`
2. แจ้งเตือน alerts (Stop loss breach, unusual moves, NAV updates) แยกแต่ละพอร์ต

## Development Conventions
- **ภาษา:** ใช้ทั้งภาษาไทยและอังกฤษได้ **ควรใช้ภาษาไทยสำหรับ verdicts ขั้นสุดท้าย**
- **Data Integrity:** **ต้อง** ใช้ไฟล์ CSV สำหรับคำนวณตัวเลข ไม่ใช้ Markdown
- **Safety:** ไม่แก้ไฟล์ข้างนอก project root ขออนุญาตก่อนลบอะไรเยอะๆ
- **Precision:** ไม่พูดวกวน ใช้ "BUY/WAIT/REDUCE/HOLD" ชัดๆ
- **Me-Tang Mandate:** ต้องให้ solution ไม่ใช่แค่ status report

## ห้าม
- อย่ารัน rm -rf หรือคำสั่งลบ folder โดยไม่ถามก่อน
- อย่าแก้ไฟล์ที่อยู่ข้างนอก folder นี้
