"""CSIP UI Theme, Styling and Presentation Components.

Provides:
- Midnight Obsidian Design System CSS
- Bento Metric Cards
- Diagnostic Summary Box

100% Zero Emojis, Zero Technical Jargon on Primary Screens.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-base: #07090E;
    --border-subtle: rgba(255, 255, 255, 0.08);
    --text-primary: #F3F4F6;
    --text-secondary: #9CA3AF;
    --text-muted: #64748B;
    --accent-gold: #F5A623;
    --accent-cyan: #38BDF8;
    --accent-rose: #FB7185;
    --accent-emerald: #34D399;
}

#MainMenu, header, footer, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"] {
    display: none !important;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
    background: radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.06) 0%, transparent 40%),
                radial-gradient(circle at 85% 25%, rgba(245, 166, 35, 0.06) 0%, transparent 45%),
                #07090E !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.block-container {
    padding-top: 1.1rem !important;
    padding-bottom: 1rem !important;
    padding-left: 2.2rem !important;
    padding-right: 2.2rem !important;
    max-width: 1580px !important;
}

.studio-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.brand-wrap {
    display: flex;
    align-items: baseline;
    gap: 12px;
}
.brand-mark {
    font-family: 'Instrument Serif', serif;
    font-size: 2rem;
    color: #FFFFFF;
    line-height: 1;
}
.brand-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(52, 211, 153, 0.12);
    border: 1px solid rgba(52, 211, 153, 0.35);
    color: var(--accent-emerald);
}
.brand-sub {
    font-size: 0.82rem;
    color: var(--text-secondary);
}

.section-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
    display: block;
}

div[data-baseweb="slider"] div[role="slider"] {
    background-color: #F5A623 !important;
    box-shadow: 0 0 10px rgba(245, 166, 35, 0.6) !important;
}
div[data-testid="stSlider"] label p {
    font-size: 0.8rem !important;
    color: #E2E8F0 !important;
    font-weight: 500 !important;
}
div[data-testid="stThumbValue"] {
    color: #F5A623 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.74rem !important;
}

div[role="radiogroup"] {
    background: rgba(15, 19, 29, 0.88);
    padding: 4px;
    border-radius: 11px;
    border: 1px solid rgba(255, 255, 255, 0.07);
    display: inline-flex;
    gap: 5px;
}
div[role="radiogroup"] label {
    background: transparent !important;
    border: none !important;
    padding: 5px 12px !important;
    border-radius: 8px !important;
    margin: 0 !important;
}
div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
    display: none !important;
}
div[role="radiogroup"] label p {
    font-size: 0.79rem !important;
    color: #9CA3AF !important;
}
div[role="radiogroup"] label:has(input:checked) {
    background: rgba(245, 166, 35, 0.16) !important;
    border: 1px solid rgba(245, 166, 35, 0.45) !important;
}
div[role="radiogroup"] label:has(input:checked) p {
    color: #F5A623 !important;
    font-weight: 600 !important;
}

.bento-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 12px;
}
.bento-card {
    background: linear-gradient(180deg, rgba(22, 28, 42, 0.82) 0%, rgba(13, 17, 26, 0.92) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 14px 18px;
    position: relative;
    overflow: hidden;
}
.bento-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--card-accent, #F5A623);
}
.bento-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #94A3B8;
    margin-bottom: 4px;
}
.bento-value {
    font-size: 1.62rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #FFFFFF;
    line-height: 1.18;
    margin-bottom: 6px;
}
.bento-sub {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.74rem;
    color: #9CA3AF;
}
.bento-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    padding: 2px 8px;
    border-radius: 6px;
    background: rgba(255,255,255,0.06);
    color: var(--card-accent, #F5A623);
}

.stage-title {
    font-family: 'Instrument Serif', serif;
    font-size: 1.38rem;
    color: #F8FAFC;
}
.stage-caption {
    font-size: 0.77rem;
    color: #94A3B8;
}

.diagnosis-box {
    margin-top: 6px;
    background: linear-gradient(90deg, rgba(56, 189, 248, 0.08) 0%, rgba(14, 18, 28, 0.95) 28%);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-left: 3px solid var(--diag-color, #38BDF8);
    border-radius: 12px;
    padding: 13px 18px;
}
.diag-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 5px;
}
.diag-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--diag-color, #38BDF8);
}
.diag-mechanism {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem;
    color: #94A3B8;
}
.diag-body {
    font-size: 0.85rem;
    color: #F1F5F9;
    line-height: 1.54;
}
</style>
"""


def apply_theme() -> None:
    """Inject the dark studio CSS stylesheet into Streamlit."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_bento_cards(sim: Dict[str, Any], pipeline: Dict[str, Any], target_col: str) -> None:
    """Render 3 modern glass Bento cards displaying prediction, top driver, and deviation."""
    top1_row = pipeline["stats_df"].iloc[0]
    pred_color = "#34D399" if sim["diff_val"] >= 0 else "#F5A623"
    delta_color = "#34D399" if sim["diff_val"] >= 0 else "#FB7185"

    bento_html = f"""
    <div class="bento-grid">
        <div class="bento-card" style="--card-accent: {pred_color};">
            <div class="bento-label">Prediksi {target_col}</div>
            <div class="bento-value" style="color: {pred_color};">{sim['pred_val']:,.2f}</div>
            <div class="bento-sub">
                <span>Rata-rata populasi: {sim['base_val']:,.2f}</span>
                <span class="bento-pill">Simulasi ML Aktif</span>
            </div>
        </div>
        <div class="bento-card" style="--card-accent: #38BDF8;">
            <div class="bento-label">Penggerak #1 Terkuat di Data</div>
            <div class="bento-value" style="font-size: 1.35rem;">{top1_row['Fitur']}</div>
            <div class="bento-sub">
                <span>Kontribusi model: {top1_row['Importance']*100:.1f}%</span>
                <span class="bento-pill" style="color:#38BDF8;">r = {top1_row['Pearson_r']:+.2f}</span>
            </div>
        </div>
        <div class="bento-card" style="--card-accent: {delta_color};">
            <div class="bento-label">Selisih Skenario vs Rata-Rata</div>
            <div class="bento-value" style="color: {delta_color}; font-size: 1.55rem;">{sim['diff_val']:+,.2f} ({sim['diff_pct']:+.1f}%)</div>
            <div class="bento-sub">
                <span>{pipeline['primary_metric_name']}: {pipeline['primary_metric_val']:.1f}%</span>
                <span class="bento-pill" style="color:{delta_color};">{pipeline['secondary_metric_str']}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(bento_html, unsafe_allow_html=True)


def render_diagnosis_box(
    dataset_title: str,
    target_col: str,
    pipeline: Dict[str, Any],
    sim: Dict[str, Any],
    filter_query: str = "",
) -> None:
    """Render human-first data finding box derived directly from model and statistics."""
    top1_row = pipeline["stats_df"].iloc[0]
    focus_row = top1_row
    if filter_query.strip():
        q_low = filter_query.strip().lower()
        matched_rows = pipeline["stats_df"][pipeline["stats_df"]["Fitur"].str.lower().str.contains(q_low)]
        if not matched_rows.empty:
            focus_row = matched_rows.iloc[0]

    direction_word = "meningkatkan" if focus_row["Pearson_r"] >= 0 else "menurunkan"
    sig_word = "signifikan secara statistik" if focus_row["p_value"] < 0.05 else "lemah secara linier (non-linier)"
    pred_color = "#34D399" if sim["diff_val"] >= 0 else "#F5A623"

    real_data_finding = (
        f"Berdasarkan komputasi langsung pada <b>{pipeline['n_rows']:,} baris data</b> untuk target <b>{target_col}</b>, "
        f"model Random Forest menemukan bahwa variabel <b>{focus_row['Fitur']}</b> menyumbang pengaruh sebesar "
        f"<b>{focus_row['Importance']*100:.1f}%</b> dengan korelasi Pearson <b>r = {focus_row['Pearson_r']:+.3f} "
        f"(p-value = {focus_row['p_value']:.2e}, {sig_word})</b>. Artinya, kenaikan nilai pada <b>{focus_row['Fitur']}</b> "
        f"cenderung {direction_word} nilai <b>{target_col}</b>. Pada posisi tuas simulasi yang kamu atur saat ini, "
        f"prediksi {target_col} berada di angka <b>{sim['pred_val']:,.2f}</b> ({sim['diff_pct']:+.1f}% dibandingkan rata-rata populasi {sim['base_val']:,.2f})."
    )

    st.markdown(
        f"""
        <div class="diagnosis-box" style="--diag-color: {pred_color};">
            <div class="diag-header">
                <span class="diag-badge">TEMUAN KOMPUTASI DATA ASLI — {dataset_title.upper()}</span>
                <span class="diag-mechanism">Metode: Random Forest + K-Means + Uji Pearson ({pipeline['secondary_metric_str']})</span>
            </div>
            <div class="diag-body">{real_data_finding}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
