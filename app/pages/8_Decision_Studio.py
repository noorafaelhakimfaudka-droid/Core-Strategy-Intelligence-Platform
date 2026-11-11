"""Bab 8: Studio Keputusan Bisnis & Rekomendasi Strategis.

Human-First Editorial Design for CSIP (Fase: UK-01, UK-11).
"""

from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
import streamlit as st

from app.ui_components import (
    PALETTE,
    apply_editorial_theme,
    render_hero,
    render_story_card,
)

st.set_page_config(page_title="Bab 8: Studio Keputusan Bisnis | CSIP", page_icon="", layout="wide")
apply_editorial_theme()

# --- HERO SECTION ---
render_hero(
    title="Bab 8: Studio Keputusan Bisnis",
    subtitle=(
        "Dari ribuan baris data, puluhan model kecerdasan buatan, dan ratusan simulasi skenario, "
        "semua berujung pada satu pertanyaan krusial: Langkah nyata apa yang harus diambil oleh pimpinan platform hari ini? "
        "Halaman ini menyajikan 4 pilihan strategi teruji, kalkulator keuangan interaktif, "
        "dan peta jalan operasional 90 hari ke depan."
    ),
    tag="BAB 8: STRATEGI & PENGAMBILAN KEPUTUSAN",
)

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# --- 3 KEY EDITORIAL HIGHLIGHTS ---
c1, c2, c3 = st.columns(3)

with c1:
    render_story_card(
        title="1. Jangan Bagi Subsidi Rata",
        body=(
            "Memberikan diskon ongkir ke semua orang (universal) adalah <b>pemborosan anggaran terbesar</b>. "
            "Sebagian besar pembeli di kota besar tetap akan berbelanja meskipun tanpa subsidi ongkir."
        ),
        tag="PERINGATAN ANGGARAN",
        tag_class="terracotta",
    )

with c2:
    render_story_card(
        title="2. Fokus ke Ketepatan Kurir",
        body=(
            "Memperketat janji tiba kurir memiliki <b>efisiensi modal 2.8x lipat lebih tinggi</b> daripada bagi-bagi diskon ongkir. "
            "Biayanya murah, namun langsung memotong akar kekecewaan pembeli."
        ),
        tag="PRIORITAS TERTINGGI",
        tag_class="sage",
    )

with c3:
    render_story_card(
        title="3. Subsidi Hanya yang 'Sakit'",
        body=(
            "Subsidi ongkir hanya efektif bila diarahkan ke <b>Tipe Pembeli Pelosok (Klaster 0)</b>. "
            "Dengan separuh anggaran, platform bisa meraih 84% kepuasan maksimal."
        ),
        tag="STRATEGI CERDAS",
        tag_class="amber",
    )

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# --- BAGIAN 1: MATRIKS KEPUTUSAN STRATEGIS (EDITORIAL CARDS) ---
st.markdown("###  Matriks 4 Pilihan Kebijakan: Menimbang Untung & Rugi")
st.markdown("Berikut adalah evaluasi jujur terhadap 4 skenario intervensi yang paling sering diajukan dalam rapat eksekutif:")

col_m1, col_m2 = st.columns(2)

with col_m1:
    st.markdown("""
    <div class="editorial-card" style="border-top: 4px solid #B83A2E;">
        <span class="card-tag terracotta">OPSI 1: SUBSIDI RATA (UNIVERSAL)</span>
        <div class="editorial-serif" style="font-size: 1.25rem; font-weight: 700; color: #1C1917; margin: 0.4rem 0;">
            Diskon Ongkir Bagi Rata ke Semua Pembeli
        </div>
        <div style="font-size: 0.92rem; color: #44403C; line-height: 1.6; margin-bottom: 0.75rem;">
            <b>Biaya Anggaran:</b> Sangat Tinggi (R$ 33.544 / 12 minggu)<br>
            <b>Dampak Kekecewaan:</b> Turun moderat (-2.44% komplain)<br>
            <b>Efisiensi Modal:</b> Sangat Buruk (Laba platform negatif)
        </div>
        <div style="background-color: #FEF2F2; padding: 0.6rem 0.8rem; border-radius: 6px; font-size: 0.88rem; color: #991B1B;">
            <b> Vonis Pimpinan: JANGAN DIJALANKAN.</b> Terjadi kebocoran subsidi pada pembeli yang sebenarnya tidak butuh diskon.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="editorial-card" style="border-top: 4px solid #D9822B;">
        <span class="card-tag amber">OPSI 3: SUBSIDI CERDAS TERARAH</span>
        <div class="editorial-serif" style="font-size: 1.25rem; font-weight: 700; color: #1C1917; margin: 0.4rem 0;">
            Subsidi Khusus Pembeli Ongkir Berat di Pelosok
        </div>
        <div style="font-size: 0.92rem; color: #44403C; line-height: 1.6; margin-bottom: 0.75rem;">
            <b>Biaya Anggaran:</b> Sedang (R$ 16.664 / 12 minggu)<br>
            <b>Dampak Kekecewaan:</b> Penurunan Kuat (-2.04% komplain)<br>
            <b>Efisiensi Modal:</b> Sangat Seimbang (Raih 84% manfaat di 50% biaya)
        </div>
        <div style="background-color: #FEF3C7; padding: 0.6rem 0.8rem; border-radius: 6px; font-size: 0.88rem; color: #92400E;">
            <b> Vonis Pimpinan: SANGAT DIREKOMENDASIKAN.</b> Alokasikan voucher ongkir khusus untuk pesanan antar-pulau / pelosok.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown("""
    <div class="editorial-card" style="border-top: 4px solid #2E6F40;">
        <span class="card-tag sage">OPSI 2: DISIPLIN MITRA KURIR</span>
        <div class="editorial-serif" style="font-size: 1.25rem; font-weight: 700; color: #1C1917; margin: 0.4rem 0;">
            Perombakan Kontrak & Janji Waktu Kurir (SLA)
        </div>
        <div style="font-size: 0.92rem; color: #44403C; line-height: 1.6; margin-bottom: 0.75rem;">
            <b>Biaya Anggaran:</b> Sangat Rendah (R$ 10.989 / 12 minggu)<br>
            <b>Dampak Kekecewaan:</b> Penurunan Solid (-0.90% komplain)<br>
            <b>Efisiensi Modal:</b> 2.8x Lipat Lebih Efisien daripada Subsidi
        </div>
        <div style="background-color: #F0FDF4; padding: 0.6rem 0.8rem; border-radius: 6px; font-size: 0.88rem; color: #166534;">
            <b> Vonis Pimpinan: PRIORITAS UTAMA.</b> Berikan sanksi tegas bagi kurir yang molor lebih dari 3 hari dari estimasi.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="editorial-card" style="border-top: 4px solid #2B4C7E;">
        <span class="card-tag indigo">OPSI 4: SERANGAN AKHIR TAHUN</span>
        <div class="editorial-serif" style="font-size: 1.25rem; font-weight: 700; color: #1C1917; margin: 0.4rem 0;">
            Kombinasi Disiplin Kurir + Subsidi Musiman
        </div>
        <div style="font-size: 0.92rem; color: #44403C; line-height: 1.6; margin-bottom: 0.75rem;">
            <b>Biaya Anggaran:</b> Tinggi (R$ 41.319 / 12 minggu)<br>
            <b>Dampak Kekecewaan:</b> Penurunan Maksimal (-3.76% komplain)<br>
            <b>Efisiensi Modal:</b> Investasi Musiman Agresif
        </div>
        <div style="background-color: #EFF6FF; padding: 0.6rem 0.8rem; border-radius: 6px; font-size: 0.88rem; color: #1E40AF;">
            <b> Vonis Pimpinan: TAKTIS MUSIMAN.</b> Simpan strategi ini khusus untuk periode belanja puncak (Black Friday / Harbolnas).
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

# --- BAGIAN 2: KALKULATOR DAMPAK KEUANGAN INTERAKTIF ---
st.markdown("###  Kalkulator Finansial Platform: Uji Simulasi Margin Anda")
st.markdown(
    "Gunakan tuas di bawah ini untuk melihat bagaimana perubahan komisi toko dan besaran subsidi per pesanan "
    "akan memengaruhi pendapatan kotor, beban anggaran, dan sisa keuntungan bersih platform:"
)

col_in, col_out = st.columns([1.0, 1.1])

with col_in:
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #EAE4DC; border-radius: 14px; padding: 1.25rem;">
        <div class="editorial-serif" style="font-size: 1.15rem; font-weight: 700; color: #1C1917; margin-bottom: 1rem;">
             Parameter Operasional Toko
        </div>
    """, unsafe_allow_html=True)

    take_rate_pct = st.slider("Komisi Platform (% Take Rate)", min_value=5.0, max_value=25.0, value=15.0, step=0.5)
    subsidy_per_order = st.slider("Alokasi Subsidi per Paket (R$)", min_value=0.0, max_value=10.0, value=3.5, step=0.5)
    projected_orders = st.number_input("Proyeksi Paket Belanja per Kuartal", min_value=1000, max_value=100000, value=9500, step=500)
    aov = st.number_input("Rata-rata Nilai Belanja per Paket (R$)", min_value=30.0, max_value=500.0, value=160.0, step=10.0)

    st.markdown("</div>", unsafe_allow_html=True)

with col_out:
    gross_gmv = projected_orders * aov
    platform_take = gross_gmv * (take_rate_pct / 100.0)
    total_subsidy = projected_orders * subsidy_per_order
    net_contrib = platform_take - total_subsidy
    subsidy_drag = (total_subsidy / platform_take) * 100 if platform_take > 0 else 0

    st.markdown(f"""
    <div style="background-color: #FFFFFF; border: 1px solid #EAE4DC; border-radius: 14px; padding: 1.25rem;">
        <div class="editorial-serif" style="font-size: 1.15rem; font-weight: 700; color: #1C1917; margin-bottom: 1rem;">
             Proyeksi Dampak Keuangan Toko
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid #F5F0E8;">
            <span style="font-size: 0.9rem; color: #655E57;">Total Transaksi Belanja (GMV)</span>
            <span style="font-size: 1.1rem; font-weight: 700; color: #1C1917;">R$ {gross_gmv:,.0f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid #F5F0E8;">
            <span style="font-size: 0.9rem; color: #655E57;">Pendapatan Kotor Toko ({take_rate_pct:.1f}% Komisi)</span>
            <span style="font-size: 1.1rem; font-weight: 700; color: #2B4C7E;">R$ {platform_take:,.0f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid #F5F0E8;">
            <span style="font-size: 0.9rem; color: #655E57;">Total Anggaran Subsidi Dikeluarkan</span>
            <span style="font-size: 1.1rem; font-weight: 700; color: #B83A2E;">R$ {total_subsidy:,.0f} ({subsidy_drag:.1f}% dari pendapatan)</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.8rem 0; margin-top: 0.4rem; background-color: #F8FAF8; border-radius: 8px; padding-left: 0.75rem; padding-right: 0.75rem;">
            <span style="font-size: 1.0rem; font-weight: 700; color: #1C1917;">Sisa Keuntungan Bersih Platform</span>
            <span style="font-size: 1.3rem; font-weight: 800; color: {'#2E6F40' if net_contrib >= 0 else '#B83A2E'};">R$ {net_contrib:,.0f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

# --- BAGIAN 3: PETA JALAN OPERASIONAL 90 HARI ---
st.markdown("###  Rencana Aksi Eksekusi 90 Hari ke Depan")
st.markdown("Agar rekomendasi ini tidak hanya menjadi wacana, berikut adalah linimasa tindakan nyata yang bertahap dan terukur:")

col_t1, col_t2, col_t3 = st.columns(3)

with col_t1:
    st.markdown("""
    <div class="editorial-card">
        <span class="card-tag terracotta">HARI 1 – 30</span>
        <div class="editorial-serif" style="font-size: 1.15rem; font-weight: 700; color: #1C1917; margin: 0.4rem 0;">
            1. Restrukturisasi Kontrak Kurir
        </div>
        <div style="font-size: 0.88rem; color: #44403C; line-height: 1.6;">
            - Perbarui kontrak kemitraan dengan seluruh ekspedisi logistik.<br>
            - Terapkan penalti pemotongan biaya ongkir jika paket terlambat lebih dari 3 hari dari estimasi janji.<br>
            - Berikan insentif prioritas jalur cepat untuk paket antar-pulau.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_t2:
    st.markdown("""
    <div class="editorial-card">
        <span class="card-tag amber">HARI 31 – 60</span>
        <div class="editorial-serif" style="font-size: 1.15rem; font-weight: 700; color: #1C1917; margin: 0.4rem 0;">
            2. Peluncuran Subsidi Terarah
        </div>
        <div style="font-size: 0.88rem; color: #44403C; line-height: 1.6;">
            - Luncurkan program voucher ongkir khusus wilayah pelosok (Klaster 0).<br>
            - Hentikan subsidi universal di kota-kota besar untuk mencegah pemborosan modal.<br>
            - Integrasikan kalkulator beban ongkir otomatis di halaman pembayaran (checkout).
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_t3:
    st.markdown("""
    <div class="editorial-card">
        <span class="card-tag sage">HARI 61 – 90</span>
        <div class="editorial-serif" style="font-size: 1.15rem; font-weight: 700; color: #1C1917; margin: 0.4rem 0;">
            3. Pengawasan & Rekalibrasi
        </div>
        <div style="font-size: 0.88rem; color: #44403C; line-height: 1.6;">
            - Pantau denyut nadi mingguan di World Model setiap hari Senin.<br>
            - Verifikasi apakah penurunan ulasan buruk mencapai target -0.9% hingga -2.0%.<br>
            - Pantau sensor pagar pengaman ekstrapolasi untuk memastikan sistem tetap di zona aman.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

# --- MODE ASESOR & DAPUR ILMIAH (EXPANDER DRAWER) ---
with st.expander(" Buka Catatan Metodologi & Audit Ilmiah (Technical & Governance Notes)"):
    st.markdown("#### Standar Metodologi Analitik yang Terpenuhi:")
    st.markdown("""
    - **`[UK-01 Menentukan Masalah Bisnis]`**: Perumusan tujuan bisnis optimasi margin platform dan minimasi churn pelanggan e-commerce.
    - **`[UK-11 Mengembangkan Solusi]`**: Penerjemahan temuan empiris menjadi actionable business rules, matriks optimasi kebijakan, dan financial impact model.
    """)

    st.markdown("---")
    st.markdown(r"""
    #### Formulasi Finansial Unit Economics Platform:
    $$\text{Gross GMV} = N_{\text{orders}} \times \overline{\text{AOV}}$$
    $$\text{Platform Take Revenue} = \text{Gross GMV} \times \tau_{\text{take}}$$
    $$\text{Total Subsidy Drag} = N_{\text{orders}} \times \sigma_{\text{subsidy}}$$
    $$\text{Net Contribution Margin} = \text{Platform Take Revenue} - \text{Total Subsidy Drag} - C_{\text{logistics}}$$
    """)

    st.markdown("##### Tabel Rekapitulasi Matriks Kebijakan Strategis Asli:")
    matrix_raw = [
        {"Strategic Option": "Option 1: Universal Freight Subsidy (S1)", "Capital Cost": "High (R$ 33,544 / 12 wks)", "Satisfaction Impact": "Moderate (-2.44 pp reviews)", "Capital Efficiency": "Very Poor (Negative Net Profit)", "Strategic Verdict": "DO NOT ADOPT (Deadweight loss on inframarginal orders)"},
        {"Strategic Option": "Option 2: Carrier Logistics SLA Overhaul (S2)", "Capital Cost": "Low (R$ 10,989 / 12 wks)", "Satisfaction Impact": "Solid (-0.90 pp reviews)", "Capital Efficiency": "2.8x Higher than Subsidies", "Strategic Verdict": "HIGH PRIORITY (Directly targets root driver of churn)"},
        {"Strategic Option": "Option 3: Targeted Friction Subsidy (S3)", "Capital Cost": "Medium (R$ 16,664 / 12 wks)", "Satisfaction Impact": "Strong (-2.04 pp reviews)", "Capital Efficiency": "Balanced (Captures 84% of S1 at 50% cost)", "Strategic Verdict": "RECOMMENDED (Deploy selectively to Cluster 0)"},
        {"Strategic Option": "Option 4: Combined Seasonal Blitz (S5)", "Capital Cost": "High (R$ 41,319 / 12 wks)", "Satisfaction Impact": "Maximum (-3.76 pp reviews)", "Capital Efficiency": "Seasonal Investment", "Strategic Verdict": "TACTICAL ONLY (Reserve for Q4 Black Friday surge)"},
    ]
    st.dataframe(pd.DataFrame(matrix_raw), use_container_width=True)
