# Kant Portfolio Rules & Targets

> ไฟล์นี้คือ "คัมภีร์หลัก" ของพอร์ต Kant — agents ทุกตัวต้องอ่านไฟล์นี้ก่อนวิเคราะห์หรือแนะนำการซื้อ-ขายใดๆ

---

## Target Asset Allocation

| กลุ่มสินทรัพย์ | Target % | สินทรัพย์ที่นับรวม |
|---|---|---|
| Core Growth | 40% | VOO, SCHD, JEPQ, KKP NDQ100-UH-E, KKP US500-UH-E, ES-GTECH |
| Thematic | 30% | UCHINA, UOBSJSM, UEMIF-N, DAOL-RARE, X-NUCTECH, KT-INDIA-D |
| Commodities | 15% | KT-PRECIOUS, KT-MINING, K-AGRI, SIVR, CTVA |
| หุ้นตรงไทย | 15% | SCB, LAND |

### Concentration Cap (ห้ามเกิน)
- **UCHINA ห้ามเกิน 15%** ของมูลค่าพอร์ตรวม — เพื่อคุม Concentration Risk
- ห้ามมี Position เดียวเกิน 20% ของพอร์ตรวม (ตาม Position Sizing Rule)

---

## Risk Management Rules

### Stop-Loss (จุดตัดขาดทุน)

| ประเภทสินทรัพย์ | Stop-Loss Threshold | วิธีนับ |
|---|---|---|
| กองทุน Commodities (KT-PRECIOUS, KT-MINING, K-AGRI) | -15% จากราคาทุน | นับจาก Avg_NAV |
| กองทุน Thematic (UCHINA, UOBSJSM, UEMIF-N, DAOL-RARE, X-NUCTECH, KT-INDIA-D) | -20% จากราคาทุน | นับจาก Avg_NAV |
| กองทุน Core Growth (KKP NDQ100, KKP US500, ES-GTECH) | -20% จากราคาทุน | นับจาก Avg_NAV |
| หุ้นตรง US (VOO, SCHD, JEPQ, CTVA, SIVR) | -20% จากราคาทุน | นับจาก Avg_Price |
| หุ้นตรงไทย (SCB) | -20% จากราคาทุน | นับจาก Avg_Price |
| LAND (US REIT) | -25% จากราคาทุน | ยืดได้เพราะ dividend yield สูง |

> ห้ามใช้เกณฑ์ Kill Condition 25% เหมารวมทุกตัว — ให้ใช้ตารางนี้แทน

### Trailing Stop (ล็อกกำไร)
- เมื่อ position ใดมีกำไร **≥ 30% จากราคาทุน** → ขยับ Floor ขึ้น
- **Floor = ราคาสูงสุดที่เคยทำได้ × 0.90** (ยอมให้ย่อได้ 10% จาก Peak)
- ถ้า NAV/ราคาหล่นต่ำกว่า Floor → ขาย 50% ก่อน แล้วประเมินใหม่

### Rebalancing Rule (ปรับสมดุล)
- ตรวจสอบ Allocation ทุก **1 เดือน** หรือเมื่อมี Shock ≥ 10% ในตลาด
- ถ้ากลุ่มใดเบี่ยงเบนจาก Target เกิน **±10%** → Rebalance ภายใน 2 สัปดาห์
- เงินที่ขาย Take Profit → นำไปเติม **กลุ่มที่ Underweight มากที่สุด** ก่อน
- Max ที่ซื้อเพิ่มต่อครั้ง: **20% ของเงินสดที่มี** (Position Sizing Rule)

---

## Kill Condition (เงื่อนไขออกทันที)

1. Drawdown เกิน Stop-Loss ของประเภทนั้นๆ (ดูตาราง) **โดยไม่มีเหตุผลใหม่**
2. Thesis หลักของสินทรัพย์เปลี่ยนไป (เช่น บริษัทเปลี่ยน CEO, นโยบายกองทุนเปลี่ยน)
3. Macro ปรับเป็น Risk-Off ชัดเจน (เช่น Fed ขึ้นดอกเบี้ยกระทันหัน, สงครามการค้ารอบใหม่)

---

## หมายเหตุสำหรับ Agents

- ราคาทุนอ้างอิง: ดูจาก `holdings.csv` (Avg_Price) และ `mutual_funds.csv` (Avg_NAV)
- ราคาตลาดปัจจุบัน: ต้องดึงมาใหม่ทุกครั้ง — ห้ามใช้ตัวเลขเก่าหรือเดาเอง
- ถ้าไม่มีราคาตลาดปัจจุบัน → แจ้งเตือนผู้ใช้ก่อน ไม่คำนวณ P&L จากทุนอย่างเดียว
- อัตราแลกเปลี่ยน USD/THB: ต้องดึงมาใหม่ทุกครั้ง — ห้ามใช้ค่าคงที่
