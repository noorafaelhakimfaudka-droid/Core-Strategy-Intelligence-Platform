"""Bab 7: Simulasi 'Bagaimana Jika?' — Menguji Coba Kebijakan Toko.

Human-First Editorial Design for CSIP (SKKNI: UK-08, UK-10, UK-11).
"""

from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.ui_components import (
    PALETTE,
    apply_editorial_theme,
    editorial_plotly_theme,
    render_before_after,
    render_hero,
    render_story_card,
)

st.set_page_config(page_title="Bab 7: Simulasi 'Bagaimana Jika?' | CSIP", page_icon="", layout="wide")
apply_editorial_theme()

# --- HERO SECTION ---
render_hero(
    title="Bab 7: Simulasi 'Bagaimana Jika?'",
    subtitle=(
        "Mengubah kebijakan e-commerce di dunia nyata membutuhkan biaya dan risiko besar. "
        "Sebelum menggelontorkan miliaran rupiah untuk diskon ongkir atau merombak mitra kurir, "
        "kami menyediakan laboratorium simulasi 'Dunia Alternatif': Anda dapat menguji skenario kebijakan "
        "dan melihat dampaknya terhadap pesanan, kepuasan pembeli, dan laba platform selama 12 minggu ke depan."
    ),
    tag="BAB 7: UJI COBA KEBIJAKAN TANPA RISIKO",
)

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Load precomputed simulation results
res_path = Path("artifacts/reports/scenario_simulation_results.json")
if res_path.exists():
    with open(res_path, "r", encoding="utf-8") as f:
        sim_data = json.load(f)
else:
    sim_data = {}

# Map technical keys to human names
HUMAN_SCENARIO_NAMES = {
    "S0_baseline": "S0: Tanpa Intervensi (Biarkan Berjalan Normal)",
    "S1_freight_subsidy": "S1: Subsidi Ongkir Universal (Diskon Rata ke Semua Pembeli)",
    "S2_carrier_sla": "S2: Disiplin Kurir & Ketepatan Waktu (Perbaikan Logistik)",
    "S3_targeted_friction": "S3: Subsidi Terarah (Khusus Pembeli Ongkir Berat di Pelosok)",
    "S4_macro_shock": "S4: Uji Coba Ekstrem (Diskon 50% & Melampaui Batas Aman)",
    "S5_combined_blitz": "S5: Serangan Terpadu (Disiplin Kurir + Subsidi Akhir Tahun)",
}

# --- 3 KEY EDITORIAL HIGHLIGHTS ---
c1, c2, c3 = st.columns(3)

with c1:
    render_story_card(
        title="1. Pagar Pengaman Ekstrapolasi",
        body=(
            "Model kami dilengkapi sensor <i>'Anti-Halusinasi'</i>. Jika kebijakan yang Anda uji terlalu ekstrem dan melampaui "
            "rekam jejak sejarah pembeli, sistem akan langsung membunyikan tanda bahaya."
        ),
        tag="PENGAWAL KEBIJAKAN",
        tag_class="terracotta",
    )

with c2:
    render_story_card(
        title="2. Proyeksi Rentang Pesimis-Optimis",
        body=(
            "Hasil simulasi tidak disajikan dalam angka tunggal yang sombong. Kami memproyeksikan rentang kemungkinan "
            "dari <b>skenario pesimis hingga optimis (interval keyakinan 90%)</b>."
        ),
        tag="RENTANG REALISTIS",
        tag_class="sage",
    )

with c3:
    render_story_card(
        title="3. Perbandingan Sebelum vs Sesudah",
        body=(
            "Setiap kebijakan langsung dibandingkan dengan garis dasar (S0) sehingga pemilik toko tahu persis "
            "apakah kebijakan tersebut mendatangkan untung atau justru membuang anggaran percuma."
        ),
        tag="EFISIENSI BIAYA",
        tag_class="amber",
    )

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# --- BAGIAN 1: PEMILIH SKENARIO KEBIJAKAN ---
st.markdown("###  Pilih Uji Coba Kebijakan yang Ingin Dilihat Dampaknya:")

scenario_keys = list(sim_data.keys())
default_index = scenario_keys.index("S2_carrier_sla") if "S2_carrier_sla" in scenario_keys else 0

selected_key = st.selectbox(
    "Pilih Skenario Kebijakan Toko:",
    options=scenario_keys,
    format_func=lambda k: HUMAN_SCENARIO_NAMES.get(k, k),
    index=default_index,
    label_visibility="collapsed",
)

if selected_key in sim_data:
    sc = sim_data[selected_key]
    cmp = sc.get("comparison_to_s0", {})
    guard = sc.get("guardrail", {})
    s0 = sim_data.get("S0_baseline", {})

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Humanized Guardrail Banner
    if guard.get("is_out_of_distribution", False):
        st.markdown(f"""
        <div style="background-color: #FEF2F2; border-left: 4px solid #B83A2E; padding: 1rem 1.25rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <div style="font-weight: 700; color: #991B1B; font-size: 1.05rem; margin-bottom: 0.25rem;">
                 Peringatan: Kebijakan Ini Terlalu Ekstrem (Melampaui Rekam Jejak Sejarah)
            </div>
            <div style="color: #7F1D1D; font-size: 0.92rem; line-height: 1.5;">
                Tingkat deviasi kebijakan ini mencapai <b>{guard.get('max_z_score', 0):.2f}x lipat</b> di atas kebiasaan normal pembeli. 
                Sistem menandai hasil ini sebagai <b>{guard.get('evidence_grade', 'Grade C Spekulatif')}</b>. 
                Di dunia nyata, pembeli mungkin akan berperilaku di luar kalkulasi matematis karena tidak ada riwayat serupa.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color: #F0FDF4; border-left: 4px solid #2E6F40; padding: 1rem 1.25rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <div style="font-weight: 700; color: #166534; font-size: 1.05rem; margin-bottom: 0.25rem;">
                 Kebijakan Berada di Zona Aman (Dapat Dipercaya)
            </div>
            <div style="color: #14532D; font-size: 0.92rem; line-height: 1.5;">
                Simulasi ini beroperasi di dalam zona kebiasaan belanja yang realistis. 
                Tingkat keyakinan bukti: <b>{guard.get('evidence_grade', 'Grade B (Empiris & Kokoh)')}</b>.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Narrative Description of Scenario
    st.markdown(f"""
    <div style="background-color: #FFFFFF; border: 1px solid #EAE4DC; border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1.5rem;">
        <b> Rancangan Kebijakan:</b> {sc.get('description', '')}
    </div>
    """, unsafe_allow_html=True)

    # Before-and-After Comparison Card
    st.markdown("####  Perbandingan Sebelum vs Sesudah (Proyeksi 12 Minggu)")
    col_comp1, col_comp2 = st.columns(2)

    with col_comp1:
        # Volume & Review comparison
        delta_rev = cmp.get("delta_negative_review_pp", 0)
        is_good_rev = delta_rev <= 0
        render_before_after(
            current_label="Persentase Pembeli Kecewa (Ulasan Buruk)",
            current_val=f"{s0.get('avg_negative_review_rate', 0.0988)*100:.2f}%",
            simulated_label="Persentase Setelah Kebijakan Diterapkan",
            simulated_val=f"{sc.get('avg_negative_review_rate', 0)*100:.2f}% ({delta_rev:+.2f}%)",
            verdict_summary=(
                f"Kekecewaan pembeli berhasil diredam sebesar {abs(delta_rev):.2f}% dibandingkan skenario normal."
                if is_good_rev else
                f"Kekecewaan pembeli meningkat sebesar {delta_rev:.2f}%."
            ),
            is_favorable=is_good_rev,
        )

    with col_comp2:
        # Financial / Volume comparison
        subsidy = sc.get("subsidy_cost_brl", 0)
        net_profit = cmp.get("net_incremental_profit_brl", 0)
        is_profitable = net_profit >= 0
        render_before_after(
            current_label="Total Pesanan Selama 12 Minggu",
            current_val=f"{int(round(s0.get('cumulative_volume', 9196))):,} pesanan",
            simulated_label="Proyeksi Pesanan dengan Kebijakan",
            simulated_val=f"{int(round(sc.get('cumulative_volume', 0))):,} pesanan ({cmp.get('delta_volume_pct', 0):+.2f}%)",
            verdict_summary=(
                f"Kebijakan ini membutuhkan anggaran subsidi sebesar R$ {subsidy:,.0f} "
                f"dengan estimasi perubahan keuntungan bersih R$ {net_profit:,.0f}."
            ),
            is_favorable=is_profitable,
        )

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# --- BAGIAN 2: GRAFIK TREN 12 MINGGU MULTI-SKENARIO ---
st.markdown("###  Peta Proyeksi 12 Minggu ke Depan")
st.markdown(
    "Gambar di bawah ini memperlihatkan bagaimana volume belanja dan tingkat komplain pembeli berkembang "
    "dari minggu ke minggu di bawah berbagai pilihan kebijakan, lengkap dengan pita ketidakpastian (rentang keyakinan 90%):"
)

fig_sc = Path("artifacts/reports/figures/scenario_simulations.png")
if fig_sc.exists():
    st.image(str(fig_sc), caption="Simulasi 12 Minggu ke Depan: Perbandingan Tren Volume, Kekecewaan, dan Dampak Finansial")

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# --- BAGIAN 3: KARTU RAPOR 6 KEBIJAKAN (TABEL BAHASA MANUSIA) ---
st.markdown("###  Rapor Ringkas 6 Pilihan Kebijakan Toko")
st.markdown("Bandingkan keenam pilihan kebijakan secara menyeluruh untuk mengambil keputusan strategis terbaik:")

if sim_data:
    table_human = []
    for s_id, s in sim_data.items():
        c = s.get("comparison_to_s0", {})
        g = s.get("guardrail", {})
        is_ood = g.get("is_out_of_distribution", False)

        table_human.append({
            "Kode": s_id.split("_")[0],
            "Nama Kebijakan": HUMAN_SCENARIO_NAMES.get(s_id, s["name"]),
            "Proyeksi Pesanan": f"{int(round(s['cumulative_volume'])):,} paket",
            "Dampak Kekecewaan": f"{c.get('delta_negative_review_pp', 0):+.2f}%",
            "Anggaran Subsidi": f"R$ {s['subsidy_cost_brl']:,.0f}",
            "Laba Bersih Tambahan": f"R$ {c.get('net_incremental_profit_brl', 0):,.0f}",
            "Status Keamanan": " Terlalu Ekstrem" if is_ood else " Aman & Teruji",
        })

    df_scorecard = pd.DataFrame(table_human)
    st.dataframe(df_scorecard, use_container_width=True, hide_index=True)

st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

# --- MODE ASESOR & DAPUR ILMIAH (EXPANDER DRAWER) ---
with st.expander(" Buka Catatan Dapur Ilmiah & Standar Kompetensi SKKNI/BNSP (Mode Penguji)"):
    st.markdown("#### Standar Unit Kompetensi SKKNI yang Terpenuhi:")
    st.markdown(r"""
    - **`[UK-08 Membangun Skenario Model]`**: Perumusan intervensi kebijakan S0 hingga S5 dengan action vector $\mathbf{A}_t$.
    - **`[UK-10 Mengevaluasi Hasil Pemodelan]`**: Kuantifikasi ketidakpastian melalui Residual Bootstrap 500 draws (90% prediction intervals).
    - **`[UK-11 Mengembangkan Solusi]`**: Penerapan Extrapolation Guardrail (Z-Score cutoff $3.5\sigma$) dan estimasi dampak ekonomi inkremental.
    """)

    st.markdown("---")
    st.markdown(r"""
    #### Formulasi Kuatifikasi Ketidakpastian & Guardrail:
    1. **Residual Bootstrap Trajectory Sampling**:
       $$\mathbf{S}_{t+1}^{(b)} = \mathbf{C} + \mathbf{\Phi}\mathbf{S}_t^{(b)} + \mathbf{\Gamma}\mathbf{A}_t + \boldsymbol{\epsilon}_t^{(b)}, \quad b = 1, \dots, 500$$
    2. **Extrapolation Guardrail Condition**:
       $$Z_{\max} = \max_t \|\mathbf{S}_t - \boldsymbol{\mu}_{\text{hist}}\|_{\boldsymbol{\Sigma}^{-1}} \le 3.5$$
       Jika $Z_{\max} > 3.5$, skenario dinyatakan Out-of-Distribution (OOD) dan evidence grade diturunkan ke Grade C.
    """)

    if sim_data:
        st.markdown("##### Ringkasan Metrik Kuantitatif Asli (S0–S5):")
        raw_rows = []
        for s_id, s in sim_data.items():
            c = s.get("comparison_to_s0", {})
            raw_rows.append({
                "Scenario ID": s_id,
                "Cumulative Volume": f"{s['cumulative_volume']:.1f}",
                "Volume Lift (%)": f"{c.get('delta_volume_pct', 0):+.2f}%",
                "Avg Neg Review": f"{s['avg_negative_review_rate']*100:.2f}%",
                "Review Lift (pp)": f"{c.get('delta_negative_review_pp', 0):+.2f} pp",
                "Subsidy Cost (BRL)": f"R$ {s['subsidy_cost_brl']:,.2f}",
                "Net Profit (BRL)": f"R$ {c.get('net_incremental_profit_brl', 0):,.2f}",
                "ROI Ratio": f"{c.get('roi_ratio', 0):.2f}",
                "OOD Triggered": s["guardrail"]["is_out_of_distribution"],
            })
        st.dataframe(pd.DataFrame(raw_rows), use_container_width=True)
