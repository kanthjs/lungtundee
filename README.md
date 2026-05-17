# ลงทุนดี — Personal AI Fund Manager

ระบบ AI ส่วนตัวสำหรับดูแลและตัดสินใจลงทุน ครอบคลุมทั้งหุ้นและกองทุนรวม โดยใช้แนวคิด Multi-Agent Synthesis ร่วมกับ Python Automation

## ลงทุนในอะไรได้บ้าง

| ประเภท | ตัวอย่าง |
|--------|---------|
| หุ้นรายตัว (US) | NYSE, NASDAQ |
| หุ้นรายตัว (ไทย) | SET |
| ETF | Global ETF |
| กองทุนรวม | กองหุ้นไทย, กองหุ้นต่างประเทศ, กองผสม, SSF, RMF |

## ทีม AI (Persona)

- **มีตัง:** Digital twin — จุดเริ่มต้นความคิดแบบเจ้าของพอร์ต (Orchestrator)
- **พี่ขุน:** CIO — ตัดสินใจขั้นสุดท้ายและให้บทสรุป (Decision Maker)
- **พี่หมอเงิน:** Fundamental Analyst — วิเคราะห์งบการเงินและคุณภาพธุรกิจ
- **พี่หมอดู:** Technical Analyst — วิเคราะห์กราฟและจับจังหวะ Indicator
- **ยาม:** Portfolio Monitor — เฝ้าพอร์ตและแจ้งเตือน Stop Loss

## Automated Workflow

เพื่อให้ AI ทำงานได้แม่นยำ 100% ควรเลือกใช้สคริปต์อัตโนมัติตามลำดับ:

1. `python fetch_prices.py` — ดึงราคาหุ้น real-time และ Technical Indicators
2. `python fetch_fund_nav.py` — อัปเดตราคา NAV กองทุนรวมไทยล่าสุด
3. `python analyze_portfolio.py` — คำนวณ P&L และ Weights (Math Engine)
4. `python alert_monitor.py` — ตรวจสอบ Kill Conditions และแจ้งเตือนสถานะ

## Slash Commands

- `/brief <TICKER>` — สรุปวิเคราะห์หุ้น 6 หัวข้อมาตรฐาน
- `/research <TICKER>` — หาข้อมูลหุ้นเชิงลึกจากแหล่งข้อมูลภายนอก
