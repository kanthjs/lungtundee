# คัมภีร์หลัก: กฎการควบคุมพอร์ตกองทุนรวมของ Kant

> Agents ทุกตัวต้องอ่านไฟล์นี้ก่อนวิเคราะห์หรือแนะนำการซื้อ-ขายกองทุนรวมใดๆ
> ราคาทุนอ้างอิงจาก `Avg_NAV` ใน `mutual_funds.csv` — ราคาตลาดปัจจุบันจาก `Current_NAV` หรือที่ผู้ใช้อัปเดต

---

## 1. Target Asset Allocation (Core & Satellite Model)

| กลุ่ม | Target % | กองทุนที่นับรวม |
|------|----------|----------------|
| **Core** (US/Global Index) | 60% | KKP US500-UH-E, KKP NDQ100-UH-E, ES-GTECH |
| **Satellite** (Thematic / ประเทศเกิดใหม่) | 20% | UCHINA, UOBSJSM, UEMIF-N, DAOL-RARE, X-NUCTECH, KT-INDIA-D |
| **Commodities** (ทองคำ แร่ธาตุ เกษตร) | 20% | KT-PRECIOUS, KT-MINING, K-AGRI |

### วิธีคำนวณ Weight

```
fund_value_THB  = Current_NAV × Units          [กองทุนไทย NAV เป็น THB]
total_port_THB  = Σ fund_value_THB ของทุกกอง
weight%         = fund_value_THB / total_port_THB × 100
group_weight%   = Σ weight% ของกองในกลุ่มนั้น
variance%       = group_weight% − target%
```

> หากกองทุนใดตีราคาเป็น USD ให้ใช้ FX จาก `live_prices.json` (THB=X) แปลงก่อน

---

## 2. Concentration Risk (กฎเหล็ก)

| กฎ | เกณฑ์ |
|----|-------|
| กองทุนเฉพาะประเทศตัวเดียว (Single-Country) | ห้ามเกิน **15% ของพอร์ตรวม** |
| กองทุนที่นับเป็น Single-Country | UCHINA, KT-INDIA-D, UOBSJSM (สิงคโปร์/อาเซียน) |

**เมื่อ weight% ของกองใดเกิน 15%** → ระบบต้องออก Alert: 🟠 `CONCENTRATION BREACH` และแนะนำให้ Rebalance ภายใน 2 สัปดาห์

---

## 3. Stop-Loss และ Kill Condition

### จุดตัดขาดทุนตามกลุ่ม

| กลุ่ม | Stop-Loss Threshold | วิธีนับ |
|------|---------------------|--------|
| **Core** (KKP US500, KKP NDQ100, ES-GTECH) | **-20%** จากราคาทุน | (Current_NAV − Avg_NAV) / Avg_NAV |
| **Satellite** (UCHINA, UOBSJSM, UEMIF-N, DAOL-RARE, X-NUCTECH, KT-INDIA-D) | **-15%** จากราคาทุน | (Current_NAV − Avg_NAV) / Avg_NAV |
| **Commodities** (KT-PRECIOUS, KT-MINING, K-AGRI) | **-15%** จากราคาทุน | (Current_NAV − Avg_NAV) / Avg_NAV |

> ห้ามใช้เกณฑ์ -25% เหมารวมสำหรับกองทุน — ใช้ตารางนี้แทนทุกกรณี

### Kill Condition (สั่งลดความเสี่ยงทันที)

เมื่อ **Drawdown% ≤ Stop-Loss** ของกลุ่มนั้น **โดยไม่มีเหตุผลพื้นฐานรองรับ**:
1. ขาย 50% ของ position นั้นก่อน
2. ประเมิน Thesis ใหม่ภายใน 1 สัปดาห์
3. ถ้า Thesis ยังไม่กลับมา → ขายส่วนที่เหลือ

เงื่อนไขที่ทำให้ Kill Condition ทริกเกอร์แม้ยังไม่แตะ SL:
- บริษัทจัดการกองทุนเปลี่ยนนโยบายหรือผู้จัดการกอง
- Macro ปรับเป็น Risk-Off ชัดเจน (Fed ขึ้นดอกเบี้ยกระทันหัน, สงครามการค้ารอบใหม่)
- กองทุน Single-Country เผชิญวิกฤต Sovereign (เช่น จีนปิดตลาด, ประกาศ Capital Control)

---

## 4. Trailing Stop (ล็อกกำไร)

- เมื่อกองใดมีกำไร **≥ 30% จากราคาทุน** → เปิดใช้ Trailing Stop
- **Floor NAV = NAV สูงสุดที่เคยทำได้ × 0.90**
- ถ้า Current_NAV หล่นต่ำกว่า Floor → ออก Alert 🟠 `TRAILING STOP HIT` แนะนำขาย 50%

---

## 5. Rebalancing Rule

| เงื่อนไข | การกระทำ |
|----------|---------|
| กลุ่มใดเบี่ยงเบนจาก Target เกิน **±10%** | Rebalance ภายใน 2 สัปดาห์ |
| ตรวจสอบรอบปกติ | ทุก **1 เดือน** หรือเมื่อตลาดผันผวน ≥ 10% ในสัปดาห์เดียว |
| เงินที่ได้จาก Take Profit / Kill Condition | นำไปเติม **กลุ่มที่ Underweight มากที่สุด** ก่อน |
| Max ซื้อเพิ่มต่อครั้ง | **20% ของเงินสดที่มี** (Position Sizing Rule) |

---

## 6. Alert Reference สำหรับ Agents

| สัญลักษณ์ | ความหมาย | เงื่อนไข |
|----------|---------|---------|
| 🔴 `KILL CONDITION` | ขายทันที | Drawdown ≥ SL threshold |
| 🟠 `CONCENTRATION BREACH` | กองเดียวเกิน 15% | weight% > 15% |
| 🟠 `TRAILING STOP HIT` | NAV หล่นจาก Peak | Current_NAV < peak × 0.90 |
| 🟠 `STOP LOSS NEAR` | ใกล้ SL อีก ≤ 3% | drawdown ≥ (SL − 3%) |
| 🟡 `ALLOCATION DRIFT` | กลุ่มเบี่ยงเบน > ±10% | variance% > ±10% |
| 🟢 `ALL CLEAR` | ไม่มีอะไรน่ากังวล | — |

---

## 7. หมายเหตุสำหรับ Agents

- **ราคาทุน:** `Avg_NAV` ใน `mutual_funds.csv`
- **ราคาตลาด:** `Current_NAV` ใน `mutual_funds.csv` — ผู้ใช้ต้องอัปเดตเองเพราะ yfinance ไม่มีราคากองทุนไทย
- **อัตราแลกเปลี่ยน:** ดึงจาก `live_prices.json` เสมอ ห้ามใช้ค่าคงที่
- ถ้า `Current_NAV` เป็นค่าว่างหรือ 0 → แสดง `N/A` และแจ้งผู้ใช้ **ห้ามเดา**
