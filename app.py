"""
PARALLEL BUSINESS — AI Biznes Qərarlarının Alternativ Gələcək Simulyatoru
Streamlit İnteraktiv İcraçı İdarəetmə Paneli (Dashboard).
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from simulation_engine import ParallelUniverseEngine

# ---------------------------------------------------------
# Səhifə Parametrləri və Konfiqurasiya
# ---------------------------------------------------------
st.set_page_config(
    page_title="Parallel Business — Kvant Qərar Simulyatoru",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Xüsusi CSS Dizaynı (Dark Modern Fintech Aesthetic)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: #070B14;
        color: #F8FAFC;
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.7) 100%);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(6, 182, 212, 0.15);
    }
    
    /* Vəziyyət Kartları */
    .universe-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 12px;
        transition: transform 0.2s ease;
    }
    .universe-card:hover {
        border-color: rgba(6, 182, 212, 0.4);
        transform: translateY(-2px);
    }
    
    .winner-badge {
        background: linear-gradient(90deg, #06B6D4, #3B82F6);
        color: #060911;
        font-weight: 800;
        font-size: 11px;
        padding: 3px 8px;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
    }
    
    /* Sidebar stilləri */
    section[data-testid="stSidebar"] {
        background-color: #0B1120;
        border-right: 1px solid #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Yan Panel (Sidebar): Biznes Profili və Giriş Parametrləri
# ---------------------------------------------------------
st.sidebar.markdown("""
<div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
    <div style="background:linear-gradient(135deg, #06B6D4, #8B5CF6); padding:8px; border-radius:10px;">
        <span style="font-size:20px;">🌌</span>
    </div>
    <div>
        <h3 style="margin:0; font-size:16px; font-weight:800; color:#fff;">PARALLEL BUSINESS</h3>
        <p style="margin:0; font-size:11px; color:#94A3B8;">AI Ssenari Simulyatoru</p>
    </div>
</div>
""", unsafe_allow_html=True)

industry_choice = st.sidebar.selectbox(
    "Biznes Sektoru:",
    options=["cafe", "retail", "saas", "ecommerce", "services"],
    format_func=lambda x: {
        "cafe": "☕ Kafe / Restoran",
        "retail": "🛒 Pərakəndə (Retail)",
        "saas": "💻 B2B SaaS / Texnologiya",
        "ecommerce": "📦 E-ticarət",
        "services": "💼 Peşəkar Xidmət / Klinika"
    }[x]
)

# Sektor şablon qiymətləri
preset_values = {
    "cafe": (28000, 11000, 38, 1100, 25000),
    "retail": (45000, 14000, 52, 1800, 35000),
    "saas": (32000, 16000, 15, 420, 50000),
    "ecommerce": (50000, 12000, 60, 2500, 30000),
    "services": (35000, 13000, 25, 150, 28000)
}

p_rev, p_fix, p_var, p_cust, p_cash = preset_values[industry_choice]

st.sidebar.markdown("---")
st.sidebar.markdown("#### 1. Mövcud Maliyyə Göstəriciləri")
rev_input = st.sidebar.number_input("Aylıq Dövriyyə (AZN):", min_value=1000, max_value=1000000, value=p_rev, step=1000)
fixed_input = st.sidebar.number_input("Sabit Xərclər (İcarə+Maaş):", min_value=500, max_value=500000, value=p_fix, step=500)
var_pct_input = st.sidebar.slider("Dəyişən Xərc Nisbəti (%):", min_value=5, max_value=90, value=p_var) / 100.0
cust_input = st.sidebar.number_input("Aylıq Müştəri Sayı:", min_value=10, max_value=500000, value=p_cust, step=50)
cash_input = st.sidebar.number_input("Mövcud Kassa Ehtiyatı (AZN):", min_value=1000, max_value=2000000, value=p_cash, step=5000)

st.sidebar.markdown("---")
st.sidebar.markdown("#### 2. Test Ediləcək Qərarlar")
price_delta = st.sidebar.slider("Ssenari 1: Qiymət Dəyişikliyi (%):", min_value=-20, max_value=40, value=12, step=1)
branch_capex = st.sidebar.slider("Ssenari 2: Filial İnvestisiyası (AZN):", min_value=10000, max_value=80000, value=30000, step=5000)
branch_opex = st.sidebar.number_input("Yeni Filial Aylıq Xərci (AZN):", min_value=1000, max_value=30000, value=6500, step=500)
ad_budget = st.sidebar.slider("Ssenari 3: Reklam Büdcəsi (AZN/ay):", min_value=500, max_value=15000, value=2500, step=500)
custom_prompt = st.sidebar.text_input("Ssenari 4 (AI Prompt):", value="2 yeni təcrübəli satış meneceri işə götürsəm")

# ---------------------------------------------------------
# Simulyasiya Mühərrikinin İcrası
# ---------------------------------------------------------
base_profile = {
    "industry": industry_choice,
    "monthly_revenue": rev_input,
    "fixed_costs": fixed_input,
    "variable_cost_pct": var_pct_input,
    "customer_count": cust_input,
    "cash_reserve": cash_input
}

engine = ParallelUniverseEngine(base_profile)

u0 = engine.simulate_universe_baseline(12)
u1 = engine.simulate_universe_price_change(price_delta, 12)
u2 = engine.simulate_universe_expansion(branch_capex, branch_opex, 5, 12)
u3 = engine.simulate_universe_marketing(ad_budget, 18.0, 12)
u4 = engine.simulate_custom_prompt_universe(custom_prompt, 12)

all_universes = [u0, u1, u2, u3, u4]
ai_board = engine.generate_ai_board_advice([u1, u2, u3, u4])

# ---------------------------------------------------------
# Əsas Səhifə: Başlıq və Qalib Ssenari Paneli
# ---------------------------------------------------------
st.markdown(f"""
<div class="hero-banner">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:15px;">
        <div>
            <div style="display:inline-flex; align-items:center; gap:6px; margin-bottom:8px;">
                <span class="winner-badge">AI SİMULYASİYA QALİBİ</span>
                <span style="font-size:12px; color:#38BDF8; font-weight:600;">Optimal Gələcək Tapıldı</span>
            </div>
            <h2 style="margin:0; font-size:26px; font-weight:800; color:#fff;">{ai_board['winner_universe']}</h2>
            <p style="margin:6px 0 0 0; font-size:13px; color:#CBD5E1;">
                Baza vəziyyətə nisbətən 12 ayda ən yüksək xalis gəlir və sabit risk balansı təmin edir.
            </p>
        </div>
        <div style="text-align:right;">
            <div style="font-size:11px; color:#94A3B8; text-transform:uppercase; font-family:'JetBrains Mono', monospace;">12 Aylıq Proqnozlaşdırılan Mənfəət</div>
            <div class="metric-value" style="color:#10B981;">{ai_board['expected_gain']:,.0f} AZN</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tablar: Təhlil, Qrafiklər, Monte Carlo və Abunə
# ---------------------------------------------------------
tab_chart, tab_matrix, tab_board, tab_monte, tab_pricing = st.tabs([
    "📈 12 Aylıq Maliyyə Qrafiki",
    "📊 Yan-Yana Müqayisə",
    "🤖 Virtual İdarə Heyəti (AI)",
    "🎲 Monte Carlo & Stress Test",
    "💳 Abunə Planları"
])

with tab_chart:
    st.subheader("Paralel Kainatların Müqayisəli Maliyyə Əyrisi")
    
    col_c1, col_c2 = st.columns([4, 1])
    with col_c2:
        chart_view = st.radio("Qrafik Metriki:", ["Aylıq Xalis Mənfəət", "Kassa Qalığı (Cash Flow)"])

    fig = go.Figure()
    months_labels = [f"Ay {m}" for m in range(1, 13)]

    for u in all_universes:
        y_data = u["net_profit"] if chart_view == "Aylıq Xalis Mənfəət" else u["cash_flow"]
        is_base = u["code"] == "baseline"
        
        fig.add_trace(go.Scatter(
            x=months_labels,
            y=y_data,
            mode='lines+markers',
            name=u["name"],
            line=dict(
                color=u["color"],
                width=2 if is_base else 3,
                dash='dot' if is_base else 'solid'
            ),
            marker=dict(size=5 if not is_base else 3)
        ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15, 23, 42, 0.6)',
        font=dict(color='#94A3B8', family='Plus Jakarta Sans'),
        hovermode="x unified",
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(gridcolor='#1E293B'),
        yaxis=dict(gridcolor='#1E293B', ticksuffix=" ₼")
    )

    st.plotly_chart(fig, use_container_width=True)

with tab_matrix:
    st.subheader("4 Paralel Kainatın Yan-Yana Təhlil Matrisi")
    
    cols = st.columns(4)
    universe_cards = [u1, u2, u3, u4]

    for idx, (col, u) in enumerate(zip(cols, universe_cards)):
        with col:
            delta = u["total_profit"] - u0["total_profit"]
            st.markdown(f"""
            <div class="universe-card" style="border-top: 3px solid {u['color']};">
                <span style="font-size:11px; font-weight:700; color:{u['color']};">{u['badge']}</span>
                <h4 style="margin:5px 0 10px 0; font-size:14px; font-weight:800; color:#fff;">{u['name']}</h4>
                <div style="font-size:11px; color:#94A3B8;">12 Aylıq Mənfəət:</div>
                <div style="font-size:20px; font-weight:800; font-family:'JetBrains Mono'; color:#F8FAFC;">{u['total_profit']:,.0f} ₼</div>
                <div style="font-size:11px; color:{'#10B981' if delta >= 0 else '#EF4444'}; margin-top:2px;">
                    {delta:+,.0f} ₼ (Baza fərqi)
                </div>
                <hr style="border-color:#1E293B; margin:10px 0;">
                <div style="font-size:11px; color:#94A3B8; display:flex; justify-content:space-between;">
                    <span>Son Kassa:</span>
                    <strong style="color:#F8FAFC;">{u['end_cash']:,.0f} ₼</strong>
                </div>
                <div style="font-size:11px; color:#94A3B8; display:flex; justify-content:space-between; margin-top:4px;">
                    <span>Risk İndeksi:</span>
                    <strong style="color:{'#EF4444' if u['risk_score'] > 50 else '#10B981'};">{u['risk_score']}/100</strong>
                </div>
                <div style="font-size:11px; color:#CBD5E1; margin-top:8px; line-height:1.4;">
                    {u['verdict']}
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab_board:
    st.subheader("AI Direktorlar Şurasının Rəyi (Virtual Board of Directors)")
    
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        st.markdown(f"""
        <div class="universe-card" style="border-color: rgba(6, 182, 212, 0.4);">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="font-size:22px;">💼</span>
                <div>
                    <strong style="color:#fff; font-size:14px;">CFO AI (Maliyyə Direktoru)</strong><br>
                    <span style="font-size:11px; color:#06B6D4;">Nağd pul və likvidlik</span>
                </div>
            </div>
            <p style="font-size:12px; color:#CBD5E1; line-height:1.5;">{ai_board['cfo']}</p>
        </div>
        """, unsafe_allow_html=True)

    with b_col2:
        st.markdown(f"""
        <div class="universe-card" style="border-color: rgba(16, 185, 129, 0.4);">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="font-size:22px;">📈</span>
                <div>
                    <strong style="color:#fff; font-size:14px;">CMO AI (Böyümə Direktoru)</strong><br>
                    <span style="font-size:11px; color:#10B981;">Bazar payı və CAC/LTV</span>
                </div>
            </div>
            <p style="font-size:12px; color:#CBD5E1; line-height:1.5;">{ai_board['cmo']}</p>
        </div>
        """, unsafe_allow_html=True)

    with b_col3:
        st.markdown(f"""
        <div class="universe-card" style="border-color: rgba(244, 63, 94, 0.4);">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="font-size:22px;">🛡️</span>
                <div>
                    <strong style="color:#fff; font-size:14px;">CRO AI (Risk Direktoru)</strong><br>
                    <span style="font-size:11px; color:#F43F5E;">Şok və iflas ehtimalı</span>
                </div>
            </div>
            <p style="font-size:12px; color:#CBD5E1; line-height:1.5;">{ai_board['cro']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📋 Addım-Addım İcra Tövsiyələri:")
    for step in ai_board['action_steps']:
        st.info(step)

with tab_monte:
    st.subheader("Monte Carlo Qeyri-müəyyənlik Simulyasiyası (1,000 İterasiya)")
    st.markdown("Real həyatda bazar sabit qalmır. Monte Carlo modeli qərarınızın 1,000 müxtəlif bazar ssenarisində necə davranacağını sınaqdan keçirir.")
    
    mc_results = engine.run_monte_carlo("price_change", runs=1000, months=12)

    mc_c1, mc_c2, mc_c3, mc_c4 = st.columns(4)
    mc_c1.metric("Uğur Ehtimalı", f"{mc_results['success_rate_pct']}%", delta="Müsbət Nəticə")
    mc_c2.metric("Pessimist Hal (10% şans)", f"{mc_results['worst_case_10pct']:,.0f} ₼")
    mc_c3.metric("Median Hal (Ən çox ehtimal)", f"{mc_results['median_case_50pct']:,.0f} ₼")
    mc_c4.metric("Optimist Hal (10% şans)", f"{mc_results['best_case_90pct']:,.0f} ₼")

with tab_pricing:
    st.subheader("Sahibkarlar üçün Şəffaf Abunə Planları")
    st.markdown("Parallel Business abunə modeli ilə işləyir. Bir səhvin zərəri aylıq abunə haqqından onlarla dəfə çoxdur.")
    
    p_col1, p_col2, p_col3 = st.columns(3)
    
    with p_col1:
        st.markdown("""
        <div class="universe-card">
            <span style="color:#94A3B8; font-size:11px; font-weight:700;">BAŞLANĞIC</span>
            <h3 style="color:#fff; margin:4px 0;">Starter</h3>
            <div style="font-size:28px; font-weight:800; font-family:'JetBrains Mono'; margin:10px 0;">39 ₼ <span style="font-size:12px; color:#94A3B8;">/ ay</span></div>
            <ul style="font-size:12px; color:#CBD5E1; padding-left:15px; line-height:1.8;">
                <li>Ayda 15 canlı simulyasiya</li>
                <li>3 paralel ssenari müqayisəsi</li>
                <li>6 aylıq proqnoz dövrü</li>
                <li>Baza qiymət elastikliyi modeli</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.button("Starter Planına Keç", key="btn_sub_starter")

    with p_col2:
        st.markdown("""
        <div class="universe-card" style="border: 2px solid #06B6D4; background:rgba(6, 182, 212, 0.05);">
            <span style="color:#06B6D4; font-size:11px; font-weight:700;">ƏN POPULYAR</span>
            <h3 style="color:#fff; margin:4px 0;">Growth Pro</h3>
            <div style="font-size:28px; font-weight:800; font-family:'JetBrains Mono'; margin:10px 0; color:#38BDF8;">89 ₼ <span style="font-size:12px; color:#94A3B8;">/ ay</span></div>
            <ul style="font-size:12px; color:#CBD5E1; padding-left:15px; line-height:1.8;">
                <li><strong>Limitsiz simulyasiyalar</strong></li>
                <li>24 aylıq dərin maliyyə proqnozu</li>
                <li>5,000 dövr Monte Carlo risk analizi</li>
                <li>AI Direktorlar Şurası (CFO, CMO, CRO)</li>
                <li>Direktorlar Şurası üçün PDF ixracı</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("14 Gün Pulsuz Sına (Growth Pro)", key="btn_sub_pro", type="primary"):
            st.success("Təbriklər! 14 günlük limitsiz sınaq dövrü başladıldı.")

    with p_col3:
        st.markdown("""
        <div class="universe-card">
            <span style="color:#8B5CF6; font-size:11px; font-weight:700;">HOLDİNQLƏR ÜÇÜN</span>
            <h3 style="color:#fff; margin:4px 0;">Enterprise</h3>
            <div style="font-size:28px; font-weight:800; font-family:'JetBrains Mono'; margin:10px 0;">249 ₼ <span style="font-size:12px; color:#94A3B8;">/ ay</span></div>
            <ul style="font-size:12px; color:#CBD5E1; padding-left:15px; line-height:1.8;">
                <li>Bütün Pro imkanları</li>
                <li>1C, QuickBooks və Bank API inteqrasiyası</li>
                <li>10 nəfərlik komanda girişi</li>
                <li>Fərdi AI Maliyyə Modeli</li>
                <li>24/7 Şəxsi Analitik Dəstəyi</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.button("Enterprise Satışla Əlaqə", key="btn_sub_ent")
