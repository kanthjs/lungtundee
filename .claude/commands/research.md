---
description: Research a stock ticker from the web and save raw findings to sources/ before running /brief
---

You are running the /research command.

## Inputs you need

- 1 stock ticker (เช่น AAPL, NVDA, PTT)
- ถ้าไม่มี ticker ให้ ask before doing anything else

## Steps

1. Confirm the ticker and which market (SET / US / HK)
2. Search and fetch the following — save each as a separate file under `sources/`:

### a) Latest earnings → `sources/earnings/<TICKER>_latest.md`
ค้นหา: "<TICKER> earnings call Q[latest quarter] transcript highlights"
เก็บ:
- Quarter และปีที่รายงาน
- Revenue, Net Income, EPS (actual vs estimate ถ้ามี)
- Key points จาก management (indirect speech เท่านั้น ห้ามแต่ง quote)
- Guidance ที่ให้ไว้

### b) Recent news → `sources/news/<TICKER>_news.md`
ค้นหา: "<TICKER> news site:reuters.com OR site:bloomberg.com OR site:set.or.th" (ปรับตามตลาด)
เก็บ: 3-5 ข่าวล่าสุด แต่ละข่าวมี date, headline, summary 2-3 ประโยค

### c) Key filing data → `sources/filings/<TICKER>_filing.md`
สำหรับ US: ค้นหา "<TICKER> 10-K annual report revenue operating income"
สำหรับ SET: ค้นหา "<TICKER> 56-1 one report" หรือ SET disclosure
เก็บ: Revenue 3 ปีล่าสุด, gross margin, D/E ratio, FCF ถ้ามี

3. หลังเก็บข้อมูลครบ รัน /brief command ต่อเลยโดยใช้ข้อมูลจาก sources/ ประกอบ

## Data quality rules

- ระบุ source URL ทุกครั้งที่ดึงข้อมูลมา
- ถ้าหาข้อมูลไม่ได้จาก web ให้บอกตรงๆ ว่าหาไม่เจอ อย่าแต่ง
- ระบุ date ที่ดึงข้อมูล ทุกไฟล์
- ห้ามแต่ง verbatim quote จาก executive

## Output

บอกผู้ใช้ว่าเก็บข้อมูลลง files ไหนบ้าง แล้วแสดง brief เต็มใน chat ต่อเลย
