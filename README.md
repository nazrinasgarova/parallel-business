# 🌌 PARALLEL BUSINESS — Alternativ Gələcəklərin AI Simulyatoru

> **"Real qərar verməzdən əvvəl, biznesinizin 4 alternativ gələcəyini canlı görün."**

**Parallel Business** — Sahibkarların və menecerlərin real kapital və vaxt itirmədən öncə strateji qərarlarının (qiymət dəyişikliyi, yeni filial açılışı, marketinq büdcəsi, işçi heyətinin artırılması) nəticələrini süni intellekt və riyazi modellərlə sınaqdan keçirməsi üçün hazırlanmış **B2B SaaS Qərar Simulyasiya Platformasıdır**.

---

## 💡 Həll Etdiyi Problem (Pain Point)
* **Yüksək Səhv Dəyəri:** İkinci filial açılışında uğursuzluq sahibkara 30,000 – 100,000+ AZN birbaşa zərər vurur.
* **Qeyri-Müəyyənlik Qorxusu:** "Qiyməti 10% qaldırsam müştərilər gedərmi?", "Reklama hər ay 3,000 AZN yatırsam nə vaxt bəhrəsini görərəm?" kimi suallara ənənəvi olaraq yalnız fərziyyə ilə cavab verilir.
* **Maliyyə Analitiki Çatışmazlığı:** Kiçik və orta bizneslərin (KOB) 92%-i daimi CFO və ya risk analitiki saxlaya bilmir.

---

## ⚡ Əsas İmkanlar & Xüsusiyyətlər

1. **Paralel Kainatlar Simulyatoru:**
   - **Kainat 0 (Status Quo):** Heç bir qərar verilmədikdə inflyasiya və orqanik artım dinamikası.
   - **Kainat 1 (Qiymət Siyasəti):** Qiymət Elastikliyi (Price Elasticity of Demand) modeli ilə müştəri itkisi və marja qazancının hesablanması.
   - **Kainat 2 (Ekspansiya / Filial):** İlkin investisiya (CAPEX), yeni icarə və maaşlar (OPEX) və 6 aylıq ramp-up adaptasiyası.
   - **Kainat 3 (Aqressiv Marketinq):** Aylıq büdcə, CAC (Müştəri Qazanma Dəyəri), LTV və churn nisbəti ilə müştəri axını.
   - **Kainat 4 (Sərbəst AI NLP Qərarı):** İstifadəçinin yazdığı istənilən qərar təbii dildə təhlil edilərək simulyasiya olunur.

2. **Dinamik 12 və 24 Aylıq Maliyyə Əyrisi:**
   - Xalis Mənfəət və Kassa Qalığı (Kumulyativ Cash Flow) üzrə interaktiv qrafiklər.

3. **Monte Carlo Simulyasiyası (1,000 İterasiya):**
   - Bazar volatilliyini təsadüfi dalğalanmalarla 1,000 dəfə sınaqdan keçirərək uğur ehtimalını (%) və ən pis halı (10-cu persentil) göstərir.

4. **"Qara Qu quşu" (Black Swan) Stress Testi:**
   - Qəfil -20% bazar böhranında hansı ssenarilərin iflas etdiyini dərhal xəbərdar edir.

5. **AI Virtual İdarə Heyəti (Executive Advisory):**
   - **CFO AI:** Likvidlik və nağd pul təhlükəsizliyi təhlili.
   - **CMO AI:** CAC/LTV, bazar payı və müştəri reaksiyası.
   - **CRO AI:** Ən pis risk dərəcələri və kredit riskləri.
   - **Yekun Qərar Tövsiyəsi:** Addım-addım tətbiq planı.

---

## 💰 Monetizasiya Modeli (Abunə / Subscription)

| Plan | Aylıq Qiymət | İllik (Endirimlə) | Hədəf Auditoriya | Əsas İmkanlar |
|---|---|---|---|---|
| **Starter** | **39 AZN** / ay | 31 AZN / ay | Tək mağaza, kafe | Ayda 15 simulyasiya, 3 paralel ssenari, 6 aylıq proqnoz |
| **Growth Pro** *(Ən Çox Seçilən)* | **89 AZN** / ay | 71 AZN / ay | Böyüyən şirkətlər | Limitsiz simulyasiyalar, 24 aylıq proqnoz, Monte Carlo 5,000 dövr, AI İdarə Heyəti, PDF Hesabat |
| **Enterprise** | **249 AZN** / ay | 199 AZN / ay | Şəbəkələr, Holdinqlər | 1C/ERP/Bank API sinxronizasiyası, 10 komanda hesabı, Fərdi AI modeli, 24/7 şəxsi analitik |

---

## 🚀 Başlama Təlimatı

Layihə 2 fərqli rejimdə istifadə oluna bilər:

### 1. Ultra-Müasir Veb Səhifəsi (Brauzerdə)
* Qovluqdakı `index.html` faylını iki dəfə klikləyərək istənilən brauzerdə açın.
* Və ya `run.bat` faylını işə salıb **[1]** seçin.
* Heç bir əlavə quraşdırma tələb etmir. Bütün interaktiv qrafiklər, kalkulyatorlar və abunə modalları tam işlək vəziyyətdədir.

### 2. Streamlit Dashboard (Python)
Terminaldan:
```bash
streamlit run app.py
```
və ya `run.bat` faylını işə salıb **[2]** seçin.
Dashboard avtomatik olaraq brauzerdə `http://localhost:8501` ünvanında açılacaq.

---

## 📊 Texnoloji Yığın (Tech Stack)
- **Frontend Web Platform:** HTML5, Tailwind CSS (Dark Glassmorphism UI), Chart.js, Lucide Icons, Canvas Confetti.
- **Backend / Python Engine:** Python 3.11+, Streamlit, Plotly, NumPy, Pandas.
- **Riyazi Modellər:** Price Elasticity of Demand ($\Delta Q = \epsilon \cdot \Delta P$), Customer Acquisition Cost ($CAC$), Customer Lifetime Value ($LTV$), Geometric Brownian Motion / Monte Carlo Random Walks.
