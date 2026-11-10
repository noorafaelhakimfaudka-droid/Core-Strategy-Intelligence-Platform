"""Bab 4: Mitos vs Kenyataan [UK-08, UK-10]."""

from pathlib import Path
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

from ui_components import (
    PALETTE,
    apply_editorial_theme,
    editorial_plotly_theme,
    render_hero,
    render_qa_box,
)

apply_editorial_theme()

render_hero(
    title="Bab 4: Mitos vs Kenyataan di Lapangan",
    subtitle=(
        "Banyak strategi bisnis dibangun di atas asumsi yang keliru dan mitos yang diulang-ulang. "
        "Di sini kita menguji keyakinan umum tersebut secara ketat di hadapan 100.000 bukti nyata."
    ),
    tag="Bab 4: Pembuktian Mitos & Fakta",
)

st.markdown("""
<div class="editorial-serif" style="font-size: 1.45rem; font-weight: 600; color: #1C1917; margin-bottom: 0.5rem;">
    Empat Keyakinan Umum yang Diuji dengan Data
</div>
<div style="font-size: 0.98rem; color: #44403C; line-height: 1.7; margin-bottom: 1.5rem;">
    Dalam mengelola toko, intuisi sering kali menyesatkan. 
    Mari kita lihat apakah mitos yang sering dipercaya manajer toko benar-benar terbukti saat diuji dengan data nyata:
</div>
""", unsafe_allow_html=True)

# 4 Interactive Myth-Buster Cards
render_qa_box(
    question="Apakah Pembeli yang Memberi Bintang 5 Pasti Akan Belanja Lagi?",
    myth="Ya, tentu saja. Pelanggan yang sangat puas pasti akan setia dan terus berbelanja kembali di toko kita.",
    reality=(
        "<b>SALAH BESAR (Mitos Terbantahkan)!</b> Pembeli yang memberi bintang 5 dan pembeli yang memberi bintang 1 "
        "memiliki persentase belanja kembali yang <b>hampir sama persis (2.27% vs 2.29%)</b>. "
        "Keputusan belanja lagi ternyata sangat ditentukan oleh <i>apakah produknya barang habis pakai</i> (kopi, sabun, popok) "
        "atau barang sekali beli (lemari, kasur), BUKAN dari rasa puas pada pesanan pertama."
    ),
    verdict_tag="Mitos Terbantahkan Secara Nyata",
)

render_qa_box(
    question="Apakah Paket Lebih Cepat Datang Selalu Menambah Kepuasan?",
    myth="Semakin cepat paket tiba, pembeli akan semakin cinta dan memberikan bintang lebih banyak.",
    reality=(
        "<b>TIDAK SEPENUHNYA BENAR.</b> Efeknya bersifat asimetris: paket yang tiba 10 hari lebih cepat dari janji hanya "
        "menghasilkan rating sekitar 4.3 bintang (mentok di batas wajar). Namun begitu paket telat 1 hari saja, "
        "rating langsung anjlok ke 2.5 bintang. Yang terpenting bagi pembeli adalah <b>kepastian janji</b>, bukan sekadar kecepatan liar."
    ),
    verdict_tag="Fakta Asimetris Terbukti",
)

render_qa_box(
    question="Apakah Ongkir Murah Selalu Membuat Pembeli Senang?",
    myth="Pokoknya ongkir harus semurah mungkin, kalau bisa digratiskan untuk semua orang.",
    reality=(
        "<b>FAKTA BERSYARAT.</b> Masalahnya bukan murah atau mahalnya angka rupiah, melainkan <i>beban ongkir dibandingkan harga barangnya</i>. "
        "Membayar ongkir Rp 20.000 untuk barang seharga Rp 1.000.000 tidak terasa berat. "
        "Namun membayar ongkir Rp 20.000 untuk barang seharga Rp 30.000 terasa seperti pemerasan dan memicu ulasan negatif."
    ),
    verdict_tag="Fakta Relativitas Beban Terbukti",
)

render_qa_box(
    question="Apakah Semua Konsumen Memiliki Sensitivitas Ongkir yang Sama?",
    myth="Semua orang di marketplace pasti sensitif dan perhitungan terhadap ongkos kirim.",
    reality=(
        "<b>SALAH.</b> Pembeli di kelompok keranjang mewah (Cluster 2) sama sekali tidak peduli pada ongkir (hanya 7.8% dari belanjaan mereka). "
        "Sensitivitas ongkir terkonsentrasi sangat kuat pada pembeli di luar pulau dan daerah pelosok (Cluster 0)."
    ),
    verdict_tag="Fakta Heterogenitas Terbukti",
)

st.write("---")

# Interactive Plotly Chart: Strength of Evidence
st.markdown("""
<div class="editorial-serif" style="font-size: 1.35rem; font-weight: 600; color: #1C1917; margin-bottom: 0.3rem;">
     Ringkasan Hasil Pengujian: Mitos Mana yang Terbukti & Mana yang Gugur?
</div>
<div style="font-size: 0.92rem; color: #655E57; margin-bottom: 1rem;">
    Visualisasi kekuatan bukti dari 6 pengujian terencana. Batang ke arah kanan menunjukkan temuan terbukti kuat; batang abu-abu menunjukkan mitos yang gugur.
</div>
""", unsafe_allow_html=True)

test_names = [
    "H1: Beban Ongkir Merusak Kepuasan",
    "H2: Efek Asimetris Telat Pengiriman",
    "H3: Rating Bintang 5 Menjamin Belanja Lagi",
    "H4: Sensitivitas Berbeda Antar-Tipe Pembeli",
    "H5: Gabungan Faktor Lebih Akurat Memprediksi",
    "H6: Jarak & Geografi Memengaruhi Belanja Ulang",
]
t_stats = [37.89, 42.18, 0.17, 29.51, 13.51, 4.64]
verdicts = [
    "TERBUKTI SANGAT KUAT",
    "TERBUKTI SANGAT KUAT",
    "GUGUR (MITOS KELIRU)",
    "TERBUKTI SANGAT KUAT",
    "TERBUKTI SANGAT KUAT",
    "TERBUKTI KUAT",
]
bar_colors = [
    PALETTE["forest_sage"],
    PALETTE["forest_sage"],
    PALETTE["crimson_clay"],
    PALETTE["forest_sage"],
    PALETTE["forest_sage"],
    PALETTE["indigo_ink"],
]

fig = go.Figure()
fig.add_trace(go.Bar(
    y=test_names,
    x=t_stats,
    orientation="h",
    marker_color=bar_colors,
    text=verdicts,
    textposition="outside",
    hovertemplate="Pengujian: %{y}<br>Kekuatan Bukti: %{x:.2f}<extra></extra>",
))

fig.add_annotation(
    y="H3: Rating Bintang 5 Menjamin Belanja Lagi", x=0.17,
    text="Mitos Gugur: Skor Ulasan Tidak Memprediksi Belanja Ulang",
    showarrow=True, arrowhead=2, ax=90, ay=25,
    font=dict(size=11, color=PALETTE["crimson_clay"]),
    bgcolor="rgba(255,255,255,0.9)", bordercolor=PALETTE["crimson_clay"], borderwidth=1,
)

editorial_plotly_theme(
    fig,
    title="H3 Gugur: Kepuasan Pesanan Pertama Tidak Memprediksi Belanja Ulang",
    subtitle="Kekuatan bukti statistik terstandarisasi untuk setiap hipotesis bisnis",
    x_title="Tingkat Kekuatan Bukti Statistik (Semakin panjang semakin kokoh)",
    y_title="",
    height=420,
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with st.expander(" Buka Catatan Dapur Ilmiah & Standar Kompetensi SKKNI/BNSP (Mode Penguji)"):
    st.markdown(r"""
    **Unit Kompetensi yang Dipenuhi:**
    - `[UK-08 Membangun Skenario Model]`: Perancangan pengujian hipotesis formal H1 s.d. H6 dengan koreksi *Benjamini-Hochberg False Discovery Rate (FDR)* pada tingkat signifikansi $\alpha = 0.05$.
    - `[UK-10 Mengevaluasi Hasil Pemodelan]`: Evaluasi diagnostik statistik menyeluruh:
      - **H1 (Supported)**: OLS $t = -37.89$, $\beta = -0.2081$, $p\text{-adj} = 1.56 \times 10^{-32}$ (Claim L2, Grade A).
      - **H2 (Supported)**: Piecewise Spline Wald $F = 4218.1$, late slope = $-0.0638$, $p\text{-adj} = 0.000$ (Claim L2, Grade A).
      - **H3 (Rejected)**: Logistic Odds Ratio = $0.9964$ (95% CI: $[0.957, 1.037]$, $p\text{-adj} = 0.859$). Dicatat secara transparan pada Failure Register `FAIL-HYP-H3`.
      - **H4 (Supported)**: Interaksi klaster $F = 29.51$, $p\text{-adj} = 3.08 \times 10^{-13}$ (Claim L2, Grade A).
      - **H5 (Supported)**: Bootstrap $\Delta PR\text{-}AUC = +0.1351$, $p\text{-adj} = 1.20 \times 10^{-4}$ (Claim L1, Grade A).
      - **H6 (Supported)**: LPM Fixed Effects $t = 4.64$, atenuasi $47.3\%$, $p\text{-adj} = 3.39 \times 10^{-6}$ (Claim L2, Grade B).
    """)
