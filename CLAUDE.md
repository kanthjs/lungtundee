# Project: lungtundee (ลงทุนดี)

**What this is:**ลงทุนดี  คือ "ผู้จัดการกองทุนส่วนตัวที่เป็น AI" (Personal AI Fund Manager) เพื่อมาช่วยดูแลพอร์ตหุ้นที่ถืออยู่ และช่วยตัดสินใจว่าเงินสดที่มีอยู่ควรจะจัดการอย่างไร การออกแบบ Workflow, Agents และ Skills  สำหรับตลาดหุ้นโดยเฉพาะ

## วิธีทำงาน
- ก่อนทำอะไรที่แก้ไฟล์เยอะหรือลบของ ให้ขออนุญาตก่อน
- แก้ไฟล์ที่มีอยู่แล้ว อย่าสร้างใหม่ถ้าไม่จำเป็น
- คำตอบให้ตรง อย่าอ้อม
- ภาษาไทยใช้ได้ ภาษาอังกฤษใช้ได้
## What lives where

- `briefs/` สำหรับ stock brief ที่ /brief สร้าง
- `.claude/commands/` สำหรับ slash command files

## Investor Profile

- **สไตล์:** Value investing — หาของถูกกว่ามูลค่าจริง ใช้ technicals จับจังหวะเข้า
- **Time horizon:** Medium (1–6 เดือน) — รอ catalyst ชัดๆ ไม่ hold ยาวโดยไม่มีเหตุผล
- **ตลาด:** SET (ไทย), US (NYSE/NASDAQ), Global ETF
- **Risk tolerance:** Moderate — รับ drawdown ได้ 15–25% ถ้า thesis ยังดี
- **Position sizing:** ไม่ all-in ทีเดียว scale เข้า
- **Kill condition default:** ถ้า thesis เปลี่ยน หรือ drawdown เกิน 25% โดยไม่มีเหตุผล ออกก่อน

_อัปเดตได้เรื่อยๆ เมื่อเรียนรู้เพิ่ม_

## ห้าม
- อย่ารัน rm -rf หรือคำสั่งลบ folder โดยไม่ถามก่อน
- อย่าแก้ไฟล์ที่อยู่ข้างนอก folder นี้
