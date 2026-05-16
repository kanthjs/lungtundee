---
description: Research a stock ticker and save a 6-section brief to briefs/<TICKER>.md
---

You are running the /brief command.

## Inputs you need

- 1 stock ticker (เช่น AAPL, NVDA, GOOGL)
- ถ้าไม่มี ticker ให้ ask before doing anything else

## Steps

1. Confirm the ticker. ถ้า ambiguous ask user to confirm
2. Read `CLAUDE.md` ที่ root ของ project — สะท้อน investing voice ของ user ใน output
3. Research บริษัทจากความรู้ที่มี ถ้าไม่รู้ข้อมูลล่าสุดจริง say so honestly, don't guess ห้ามแต่งชื่อคน, วันที่, ตัวเลข ที่ verify ไม่ได้
4. ถ้า folder `briefs/` ยังไม่มี ให้สร้าง
5. Save brief ที่ `briefs/<TICKER>.md` (uppercase ticker)
6. แสดง brief เต็มกลับใน chat ด้วย

## Output format (6 sections, required, no skipping)

### 1. Company snapshot (3-4 ประโยคไทย)
บริษัททำอะไร, ขายให้ใคร, รายได้หลักมาจากไหน ภาษาคนปกติ

### 2. Fundamentals signal (3-5 bullets)
Revenue trend, margin trend, balance sheet feel, capital allocation pattern เน้น direction มากกว่าตัวเลข ถ้าไม่แน่ใจ ใส่ "(ตัวเลข ตรวจสอบใน 10-K ล่าสุด)" ต่อท้าย

### 3. Latest earnings
3-5 bullets อิงจาก quarterly earnings call ล่าสุดเท่าที่ training data รู้ ถ้าไม่แน่ใจว่า quarter ล่าสุดคืออะไร ให้บอกตรงๆ ห้ามแต่งตัวเลขเฉพาะเจาะจง

### 4. Bull case / Bear case
2-3 bullets แต่ละข้าง Bear case ต้อง specific to บริษัทนี้ ไม่ใช่ "เศรษฐกิจไม่ดี"

### 5. Kill conditions (สำคัญ อย่าข้าม)
2-3 bullets "ถ้าเห็นอะไรเกิดขึ้น ควรเลิกถือ" เช่น "margin ลดลง 3 quarter ติด", "ลูกค้า top-3 หายไป 1 ราย"

### 6. What to ask before owning it (3-5 questions)
คำถามที่ beginner ควรตอบให้ได้ก่อนกดซื้อ

## Voice rules

- Tone reflect investing voice ใน `CLAUDE.md` ของ project
- ห้าม ออก buy/sell recommendation
- ห้าม แต่ง verbatim quote ของ executive ใช้ indirect speech
- ห้าม ใช้คำว่า "moat" ตรงๆ ใช้ Helmer's 7 Powers ที่ specific
- ห้าม บอกว่า "ตลาดยังไม่ price in"

## When unsure

Honest > confident ถ้าข้อมูลไม่พอ พูดว่า "ไม่แน่ใจ" ดีกว่าแต่ง
