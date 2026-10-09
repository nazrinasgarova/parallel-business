"""
PARALLEL BUSINESS — Simulation & Decision Engine
Sahibkarlar üçün Alternativ Gələcəklərin Süni İntellekt Simulyatoru.
Hesablamalar: Qiymət Elastikliyi, Ekspansiya (Filial), Marketinq Effektivliyi (CAC/LTV), Monte Carlo Risk Simulyasiyası.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any


class ParallelUniverseEngine:
    def __init__(self, base_profile: Dict[str, Any]):
        """
        base_profile parametrləri:
        - industry: Sektor ('cafe', 'retail', 'saas', 'ecommerce', 'services')
        - monthly_revenue: Mövcud aylıq dövriyyə (AZN)
        - fixed_costs: Sabit xərclər (icarə, maaş, komunal)
        - variable_cost_pct: Dəyişən xərclər faizi (0.0 - 1.0)
        - customer_count: Aylıq aktiv müştəri sayı
        - cash_reserve: Mövcud kassa qalığı (ehtiyat)
        """
        self.profile = base_profile
        self.industry = base_profile.get("industry", "retail")
        self.monthly_rev = float(base_profile.get("monthly_revenue", 30000))
        self.fixed_costs = float(base_profile.get("fixed_costs", 12000))
        self.var_cost_pct = float(base_profile.get("variable_cost_pct", 0.40))
        self.customers = int(base_profile.get("customer_count", 1000))
        self.cash = float(base_profile.get("cash_reserve", 20000))
        self.aov = self.monthly_rev / max(1, self.customers)

        # Sektorlara uyğun qiymət elastikliyi sabiti (Price Elasticity of Demand)
        self.elasticity_map = {
            "cafe": -1.4,       # Restoran/kafe: orta dərəcədə elastik (rəqabət çoxdur)
            "retail": -1.6,     # Pərakəndə: elastik
            "saas": -0.8,       # B2B SaaS: qeyri-elastik (müştərilər asan tərk etmir)
            "ecommerce": -1.8,  # E-ticarət: çox elastik (1 kliklə alternativ tapılır)
            "services": -1.1    # Xidmət sektoru: orta
        }
        self.elasticity = self.elasticity_map.get(self.industry, -1.3)

    def simulate_universe_baseline(self, months: int = 12) -> Dict[str, Any]:
        """Kainat 0: Status Quo (Heç bir radikal qərar verilmir, inflyasiya və orqanik artım)"""
        revenue = []
        profit = []
        cash_flow = []
        current_cash = self.cash
        organic_growth = 0.008  # aylıq 0.8% orqanik artım
        inflation_cost_increase = 0.005 # aylıq 0.5% xərc artımı

        rev = self.monthly_rev
        f_cost = self.fixed_costs

        for m in range(1, months + 1):
            rev *= (1 + organic_growth)
            f_cost *= (1 + inflation_cost_increase)
            var_cost = rev * self.var_cost_pct
            net_profit = rev - (f_cost + var_cost)
            current_cash += net_profit

            revenue.append(round(rev, 2))
            profit.append(round(net_profit, 2))
            cash_flow.append(round(current_cash, 2))

        return {
            "name": "Kainat 0: Baza Vəziyyət (Status Quo)",
            "code": "baseline",
            "badge": "Mövcud Gedişat",
            "color": "#94A3B8",
            "months": list(range(1, months + 1)),
            "revenue": revenue,
            "net_profit": profit,
            "cash_flow": cash_flow,
            "total_profit": round(sum(profit), 2),
            "end_cash": round(current_cash, 2),
            "roi": 0.0,
            "risk_score": 15,  # Aşağı risk, lakin zəif inkişaf
            "verdict": "Stabil qalır, lakin inflyasiya və rəqabət səbəbindən marja tədricən daralır."
        }

    def simulate_universe_price_change(self, price_delta_pct: float = 12.0, months: int = 12) -> Dict[str, Any]:
        """
        Kainat 1: Qiymət Siyasəti Dəyişikliyi (Məs: 'Qiyməti 10% və ya 15% artırsam?')
        price_delta_pct: Faiz dəyişikliyi (+12, +20, -10 və s.)
        """
        revenue = []
        profit = []
        cash_flow = []
        current_cash = self.cash

        # Qiymət dəyişdikdə tələbin (müştəri sayının) dəyişməsi:
        # % ΔQ = Elasticity * % ΔP
        p_factor = price_delta_pct / 100.0
        q_change_pct = self.elasticity * p_factor
        new_customer_count = max(50, self.customers * (1 + q_change_pct))
        new_aov = self.aov * (1 + p_factor)

        base_monthly_rev = new_customer_count * new_aov
        f_cost = self.fixed_costs

        for m in range(1, months + 1):
            # Tədricən bazarın yeni qiymətə adaptasiyası
            rev = base_monthly_rev * (1 + 0.005 * m)
            var_cost = rev * self.var_cost_pct
            net_profit = rev - (f_cost + var_cost)
            current_cash += net_profit

            revenue.append(round(rev, 2))
            profit.append(round(net_profit, 2))
            cash_flow.append(round(current_cash, 2))

        total_profit = sum(profit)
        baseline_profit = self.simulate_universe_baseline(months)["total_profit"]
        delta_profit = total_profit - baseline_profit

        # Risk qiymətləndirməsi
        risk = 25 if price_delta_pct > 0 and price_delta_pct <= 15 else (50 if price_delta_pct > 15 else 40)

        return {
            "name": f"Kainat 1: Qiymət Dəyişikliyi ({'+' if price_delta_pct > 0 else ''}{price_delta_pct}%)",
            "code": "price_change",
            "badge": "Yüksək Marja Potensialı",
            "color": "#06B6D4",
            "months": list(range(1, months + 1)),
            "revenue": revenue,
            "net_profit": profit,
            "cash_flow": cash_flow,
            "total_profit": round(total_profit, 2),
            "delta_profit_vs_base": round(delta_profit, 2),
            "end_cash": round(current_cash, 2),
            "customer_impact_pct": round(q_change_pct * 100, 1),
            "risk_score": risk,
            "verdict": f"Qiymət {price_delta_pct}% dəyişəndə müştərilərin {abs(round(q_change_pct * 100, 1))}% hissəsi itirilsə də, ümumi xalis gəlir {'artır' if delta_profit > 0 else 'azalır'} ({delta_profit:+,.0f} AZN fərq)."
        }

    def simulate_universe_expansion(self, capex: float = 35000, added_fixed: float = 8000, ramp_months: int = 5, months: int = 12) -> Dict[str, Any]:
        """
        Kainat 2: İkinci Filial / Yeni Obyekt Açılışı
        capex: İlkin təmir və avadanlıq xərci
        added_fixed: 2-ci filialın aylıq icarə + maaş xərcləri
        ramp_months: Filialın tam dövriyyəyə çatması üçün aylar
        """
        revenue = []
        profit = []
        cash_flow = []
        current_cash = self.cash - capex # İlkin investisiya kassadan çıxır

        f_cost_base = self.fixed_costs

        for m in range(1, months + 1):
            # Ramp-up əyrisi: filial tədricən gəlir gətirməyə başlayır
            ramp_factor = min(1.0, m / max(1, ramp_months))
            new_branch_rev = (self.monthly_rev * 0.85) * ramp_factor
            
            total_rev = self.monthly_rev + new_branch_rev
            total_fixed = f_cost_base + (added_fixed * (0.6 if m == 1 else 1.0))
            var_cost = total_rev * self.var_cost_pct
            
            net_profit = total_rev - (total_fixed + var_cost)
            current_cash += net_profit

            revenue.append(round(total_rev, 2))
            profit.append(round(net_profit, 2))
            cash_flow.append(round(current_cash, 2))

        total_profit = sum(profit)
        baseline_profit = self.simulate_universe_baseline(months)["total_profit"]
        net_value_generated = (current_cash - self.cash)

        # Əgər kassa sıfırdan aşağı düşərsə, likvidlik böhranı riski yaranır
        min_cash = min(cash_flow)
        liquidity_crisis = min_cash < 0
        risk = 75 if liquidity_crisis else 45

        return {
            "name": "Kainat 2: 2-ci Filial / Ekspansiya",
            "code": "expansion",
            "badge": "Böyük Sıçrayış & Kassa Riski",
            "color": "#8B5CF6",
            "months": list(range(1, months + 1)),
            "revenue": revenue,
            "net_profit": profit,
            "cash_flow": cash_flow,
            "total_profit": round(total_profit, 2),
            "end_cash": round(current_cash, 2),
            "min_cash_dip": round(min_cash, 2),
            "payback_months": ramp_months + 2 if current_cash > self.cash else 18,
            "risk_score": risk,
            "liquidity_crisis": liquidity_crisis,
            "verdict": ("DİQQƏT: Kassa ehtiyatı çatışmazlığı riski var! Əlavə kredit və ya ehtiyat lazımdır." 
                        if liquidity_crisis else 
                        f"Gəlir 12 ayda 80%-ə qədər böyüyür. İnvestisiya təxminən {ramp_months + 2}-ci ayda bərpa olunur.")
        }

    def simulate_universe_marketing(self, ad_spend_monthly: float = 3000, cac: float = 18.0, months: int = 12) -> Dict[str, Any]:
        """
        Kainat 3: Aqressiv Reklam və Marketinq Kampaniyası
        ad_spend_monthly: Hər ay reklama ayrılan büdcə
        cac: Müştəri Qazanma Dəyəri (Customer Acquisition Cost)
        """
        revenue = []
        profit = []
        cash_flow = []
        current_cash = self.cash

        f_cost = self.fixed_costs
        accumulated_new_customers = 0

        for m in range(1, months + 1):
            # Yeni müştərilər hər ay daxil olur
            monthly_new_cust = ad_spend_monthly / max(1.0, cac)
            # Churn (itki) çıxılır: aylıq 5% churn
            accumulated_new_customers = (accumulated_new_customers * 0.95) + monthly_new_cust
            
            added_rev = accumulated_new_customers * self.aov
            total_rev = self.monthly_rev + added_rev
            var_cost = total_rev * self.var_cost_pct
            total_expenses = f_cost + ad_spend_monthly + var_cost

            net_profit = total_rev - total_expenses
            current_cash += net_profit

            revenue.append(round(total_rev, 2))
            profit.append(round(net_profit, 2))
            cash_flow.append(round(current_cash, 2))

        total_profit = sum(profit)
        baseline_profit = self.simulate_universe_baseline(months)["total_profit"]
        delta_profit = total_profit - baseline_profit

        # ROAS və LTV/CAC
        ltv = self.aov * (1 - self.var_cost_pct) * 8 # Təxmini 8 aylıq ömür
        ltv_cac_ratio = round(ltv / max(1.0, cac), 2)
        risk = 30 if ltv_cac_ratio >= 3 else 60

        return {
            "name": f"Kainat 3: Aqressiv Marketinq ({ad_spend_monthly:,.0f} AZN/ay)",
            "code": "marketing",
            "badge": f"LTV/CAC: {ltv_cac_ratio}x",
            "color": "#10B981",
            "months": list(range(1, months + 1)),
            "revenue": revenue,
            "net_profit": profit,
            "cash_flow": cash_flow,
            "total_profit": round(total_profit, 2),
            "delta_profit_vs_base": round(delta_profit, 2),
            "end_cash": round(current_cash, 2),
            "ltv_cac_ratio": ltv_cac_ratio,
            "risk_score": risk,
            "verdict": f"Hər xərclənən 1 AZN reklam {ltv_cac_ratio} AZN dəyər yaradır. Müştəri bazası ilin sonuna +{int(accumulated_new_customers)} nəfər artır."
        }

    def simulate_custom_prompt_universe(self, prompt: str, months: int = 12) -> Dict[str, Any]:
        """
        Kainat 4: İstifadəçinin sərbəst yazdığı qərar (AI NLP Simulation)
        Məsələn: 'Satıcıların sayını 3 nəfər artırsam', 'Məhsul çeşidini azaltsam'
        """
        p_lower = prompt.lower()
        
        # Heuristik və təbii dil analizi
        if any(w in p_lower for w in ["işçi", "satıcı", "menecer", "maaş", "komanda", "hire", "personnel"]):
            # Əməkdaş cəlbi ssenarisi
            added_fixed = 3000
            sales_boost_pct = 0.22
            risk = 35
            name = "Kainat 4 (AI): Komandanın Genişləndirilməsi"
            badge = "Satış Gücü Artımı"
            color = "#F59E0B"
            verdict = "İşçi xərcləri sabit xərci artırsa da, peşəkar satışla dövriyyə 22% yüksəlir."
        elif any(w in p_lower for w in ["endirim", "aksiya", "discount", "ucuz"]):
            # Endirim / Aksiya ssenarisi
            added_fixed = 500
            sales_boost_pct = 0.15
            risk = 45
            name = "Kainat 4 (AI): Endirim və Kütləvi Cəlb"
            badge = "Həcm Artımı, Aşağı Marja"
            color = "#EC4899"
            verdict = "Müştəri axını artır, lakin marja daraldığı üçün xalis mənfəət gözləniləndən az yüksəlir."
        elif any(w in p_lower for w in ["ixrac", "xaric", "franchise", "françayzinq"]):
            # Ekspansiya / Françayzinq
            added_fixed = 1500
            sales_boost_pct = 0.35
            risk = 65
            name = "Kainat 4 (AI): Françayzinq & Yeni Region"
            badge = "Yüksək Miqyas"
            color = "#3B82F6"
            verdict = "Böyümə tempi ən yüksək olan ssenaridir, lakin standartların qorunması riski var."
        else:
            # Ümumi optimizasiya ssenarisi
            added_fixed = 1000
            sales_boost_pct = 0.18
            risk = 40
            name = f"Kainat 4 (AI): Fərdi Qərar Simulyasiyası"
            badge = "Xüsusi Ssenari"
            color = "#F43F5E"
            verdict = f"'{prompt[:35]}...' qərarı 12 ay ərzində dövriyyəyə müsbət təsir göstərir."

        revenue = []
        profit = []
        cash_flow = []
        current_cash = self.cash
        f_cost = self.fixed_costs + added_fixed

        for m in range(1, months + 1):
            ramp = min(1.0, 0.4 + (0.6 * m / 6))
            rev = self.monthly_rev * (1 + sales_boost_pct * ramp)
            var_cost = rev * self.var_cost_pct
            net_profit = rev - (f_cost + var_cost)
            current_cash += net_profit

            revenue.append(round(rev, 2))
            profit.append(round(net_profit, 2))
            cash_flow.append(round(current_cash, 2))

        return {
            "name": name,
            "code": "custom_prompt",
            "prompt_text": prompt,
            "badge": badge,
            "color": color,
            "months": list(range(1, months + 1)),
            "revenue": revenue,
            "net_profit": profit,
            "cash_flow": cash_flow,
            "total_profit": round(sum(profit), 2),
            "end_cash": round(current_cash, 2),
            "risk_score": risk,
            "verdict": verdict
        }

    def run_monte_carlo(self, universe_code: str = "price_change", runs: int = 500, months: int = 12) -> Dict[str, Any]:
        """
        Monte Carlo Simulyasiyası:
        Gözlənilməz bazar dəyişiklikləri, inflyasiya və rəqabət təsirlərini 500-1000 dəfə təkrar edərək
        uğur ehtimalını (%) və ən pis/ən yaxşı halları müəyyənləşdirir.
        """
        np.random.seed(42)
        final_profits = []
        bankruptcy_count = 0

        # Uyğun ssenari üzrə baza parametrlər
        volatility = 0.08 # Aylıq 8% dalğalanma

        for _ in range(runs):
            sim_cash = self.cash
            sim_profit = 0
            cur_rev = self.monthly_rev
            is_bankrupt = False

            for m in range(months):
                shock = np.random.normal(0, volatility)
                # Ssenari təsiri
                if universe_code == "price_change":
                    cur_rev = self.monthly_rev * 1.08 * (1 + shock)
                elif universe_code == "expansion":
                    cur_rev = (self.monthly_rev * (1.2 + 0.05 * m)) * (1 + shock)
                elif universe_code == "marketing":
                    cur_rev = (self.monthly_rev * 1.15) * (1 + shock)
                else:
                    cur_rev = self.monthly_rev * (1 + shock)

                p = cur_rev - (self.fixed_costs + cur_rev * self.var_cost_pct)
                sim_profit += p
                sim_cash += p
                if sim_cash < 0:
                    is_bankrupt = True

            final_profits.append(sim_profit)
            if is_bankrupt:
                bankruptcy_count += 1

        final_profits.sort()
        p10 = final_profits[int(runs * 0.10)]
        p50 = final_profits[int(runs * 0.50)]
        p90 = final_profits[int(runs * 0.90)]
        success_rate = round((1 - (bankruptcy_count / runs)) * 100, 1)

        return {
            "runs": runs,
            "success_rate_pct": success_rate,
            "worst_case_10pct": round(p10, 2),
            "median_case_50pct": round(p50, 2),
            "best_case_90pct": round(p90, 2),
            "bankruptcy_risk_pct": round((bankruptcy_count / runs) * 100, 1)
        }

    def generate_ai_board_advice(self, all_universes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        AI Virtual Direktorlar Şurası (Virtual Board of Directors)
        CFO, CMO və CRO rollarında təhlil və yekun qərar tövsiyəsi
        """
        # Ən yüksək mənfəətli kainat
        best_profit_u = max(all_universes, key=lambda x: x["total_profit"])
        # Ən aşağı riskli kainat
        safest_u = min(all_universes, key=lambda x: x["risk_score"])
        
        cfo_advice = (
            f"Kassa likvidliyinə görə ən təhlükəsiz addım '{safest_u['name']}'. "
            f"Lakin böyümək istəyirsinizsə, '{best_profit_u['name']}' 12 ayda ən çox nağd pul yaradan modeldir. "
            f"Diqqət edin ki, kassa ehtiyatınız heç bir ayda 10,000 AZN-dən aşağı enməsin."
        )

        cmo_advice = (
            "Qiyməti artırarkən itiriləcək müştərilərin yerinə daha yüksək LTV-yə malik seqment cəlb olunmalıdır. "
            "Marketinq və brend dəyəri artırılmadan edilən qəfil qiymət artımları rəqiblərə üstünlük verə bilər."
        )

        cro_advice = (
            f"Risk reytinqi baxımından ən həssas nöqtə 2-ci filial açılışı və kütləvi ilkin xərclərdir. "
            f"Əgər kassa ehtiyatı ən az 3 aylıq sabit xərcləri qarşılamırsa, böyük investisiyaları 3 ay ertələyin."
        )

        recommendation = {
            "winner_universe": best_profit_u["name"],
            "winner_color": best_profit_u["color"],
            "expected_gain": best_profit_u["total_profit"],
            "cfo": cfo_advice,
            "cmo": cmo_advice,
            "cro": cro_advice,
            "action_steps": [
                "1. Qiyməti birdən-birə yox, əsas bestseller məhsullarda 8-10% artıraraq elastikliyi test edin.",
                "2. Reklam büdcəsini kiçik sprintlərlə (həftəlik 500 AZN) sınaqdan keçirin və CAC-ı ölçün.",
                "3. Kassa qalığı 35,000 AZN-ə çatdıqda 2-ci filial üçün yer axtarışına başlayın."
            ]
        }
        return recommendation
