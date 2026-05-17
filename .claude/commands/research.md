---
description: Research a stock ticker from the web and save raw findings to sources/ before running /brief
---

You are running the /research command.

## Inputs you need

- 1 stock ticker (เช่น AAPL, NVDA, PTT)
- ถ้าไม่มี ticker ให้ ask before doing anything else

## Steps

1. Confirm the ticker and which market (SET / US / HK)

2. **Cache check ก่อน fetch ทุกครั้ง** — อ่านไฟล์ที่อาจมีอยู่แล้วและดูบรรทัด `fetched:` ที่ header:

   | ไฟล์ | Freshness window | ถ้ายังสด |
   |------|-----------------|----------|
   | `sources/news/<TICKER>_news.md` | 3 วัน | ข้ามการ fetch ใหม่ |
   | `sources/earnings/<TICKER>_latest.md` | 30 วัน | ข้ามการ fetch ใหม่ |
   | `sources/filings/<TICKER>_filing.md` | 90 วัน | ข้ามการ fetch ใหม่ |

   - คำนวณ freshness จาก `fetched:` field ใน header เทียบกับวันนี้ (today's date มาจาก `CLAUDE.md`)
   - แสดงสรุปก่อนเริ่ม เช่น: "📁 พบข้อมูลเก่า: news (2 วัน — ใช้ cache), earnings (45 วัน — fetch ใหม่), filings (ไม่มีไฟล์ — fetch ใหม่)"
   - ถ้าทุกไฟล์ยังสด → บอก user และกระโดดไป step 3 ได้เลย ไม่ต้อง fetch

3. Search and fetch เฉพาะส่วนที่ **ไม่มี cache** — save แต่ละส่วนลง `sources/`:

### a) Latest earnings → `sources/earnings/<TICKER>_latest.md`
ค้นหา: "<TICKER> earnings call Q[latest quarter] transcript highlights"
**Header บังคับ (บรรทัดแรกของไฟล์):**
```
ticker: <TICKER>
fetched: YYYY-MM-DD
source: <URL>
```
เก็บ:
- Quarter และปีที่รายงาน
- Revenue, Net Income, EPS (actual vs estimate ถ้ามี)
- Key points จาก management (indirect speech เท่านั้น ห้ามแต่ง quote)
- Guidance ที่ให้ไว้

### b) Recent news → `sources/news/<TICKER>_news.md`
ค้นหา: "<TICKER> news site:reuters.com OR site:bloomberg.com OR site:set.or.th" (ปรับตามตลาด)
**Header บังคับ (บรรทัดแรกของไฟล์):**
```
ticker: <TICKER>
fetched: YYYY-MM-DD
source: <URL>
```
เก็บ: 3-5 ข่าวล่าสุด แต่ละข่าวมี date, headline, summary 2-3 ประโยค

### c) Key filing data → `sources/filings/<TICKER>_filing.md`
สำหรับ US: ค้นหา "<TICKER> 10-K annual report revenue operating income"
สำหรับ SET: ค้นหา "<TICKER> 56-1 one report" หรือ SET disclosure
**Header บังคับ (บรรทัดแรกของไฟล์):**
```
ticker: <TICKER>
fetched: YYYY-MM-DD
source: <URL>
```
เก็บ: Revenue 3 ปีล่าสุด, gross margin, D/E ratio, FCF ถ้ามี

4. หลังเก็บข้อมูลครบ รัน /brief command ต่อเลยโดยใช้ข้อมูลจาก sources/ ประกอบ

## Data quality rules

- ระบุ source URL ทุกครั้งที่ดึงข้อมูลมา
- ถ้าหาข้อมูลไม่ได้จาก web ให้บอกตรงๆ ว่าหาไม่เจอ อย่าแต่ง
- ระบุ date ที่ดึงข้อมูล ทุกไฟล์
- ห้ามแต่ง verbatim quote จาก executive

## Output

บอกผู้ใช้ว่าเก็บข้อมูลลง files ไหนบ้าง แล้วแสดง brief เต็มใน chat ต่อเลย
