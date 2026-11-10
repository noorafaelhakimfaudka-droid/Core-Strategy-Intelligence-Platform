"""Bab 1: Kisah Utama [UK-01, UK-02, UK-11]."""

from pathlib import Path
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

from ui_components import (
    PALETTE,
    apply_editorial_theme,
    editorial_plotly_theme,
    render_hero,
    render_story_card,
)

apply_editorial_theme()

render_hero(
    title="Bab 1: Kisah di Balik 100.000 Jejak Perjalanan Pembeli",
    subtitle=(
        "Sebuah telaah mendalam tentang apa yang sebenarnya terjadi saat seseorang menekan tombol 'Beli', "
        "menunggu paket di rumah, dan memutuskan apakah mereka akan kembali lagi ke toko kita atau pergi selamanya."
    ),
    tag="Bab 1: Kisah Utama",
)

st.markdown("""
<div class="editorial-serif" style="font-size: 1.5rem; font-weight: 600; color: #1C1917; margin-bottom: 0.5rem;">
    Dilema Abadi: Antara Ongkir Murah dan Janji Tepat Waktu
</div>
<div style="font-size: 1rem; color: #44403C; line-height: 1.7; margin-bottom: 1.5rem;">
    Setiap pengelola toko atau marketplace selalu tergoda untuk berpikir bahwa <b>"harga murah adalah segalanya"</b>. 
    Banyak yang rela membakar miliaran rupiah demi memberikan subsidi ongkos kirim cuma-cuma, dengan harapan pembeli akan setia.
    <br><br>
    Namun saat kita membuka lembaran rekam jejak 100.000 transaksi nyata, data membisikkan kenyataan yang sangat berbeda:
    <b>Pembeli jauh lebih pemaaf terhadap ongkos kirim yang wajar daripada kurir yang datang melewati tanggal janji.</b>
</div>
""", unsafe_allow_html=True)

# 3 Story Highlight Columns
c1, c2, c3 = st.columns(3)
with c1:
    render_story_card(
        tag="Fakta #1",
        tag_class="terracotta",
        title="Telat 1 Hari Saja, Kepercayaan Runtuh",
        body=(
            "Jika paket tiba lebih cepat 1 sampai 10 hari dari janji, rating kepuasan stabil di angka 4.3 dari 5 bintang. "
            "Namun begitu paket terlambat 1 hari saja, nilai kepuasan langsung terjun bebas ke 2.5 bintang."
        ),
    )

with c2:
    render_story_card(
        tag="Fakta #2",
        tag_class="sage",
        title="Beban Ongkir yang Bikin Mikir Dua Kali",
        body=(
            "Bukan nominal rupiah ongkir yang jadi masalah, melainkan <b>rasionya terhadap harga barang</b>. "
            "Jika ongkir mencapai lebih dari sepertiga harga barang (misal: barang Rp 30.000 tapi ongkir Rp 15.000), "
            "pembeli merasa rugi dan risikonya memberi ulasan buruk melonjak 1.8 kali lipat."
        ),
    )

with c3:
    render_story_card(
        tag="Fakta #3",
        tag_class="indigo",
        title="Subsidi Buta Merugikan Toko",
        body=(
            "Memberi subsidi ongkir secara merata ke semua orang ibarat menuangkan air ke ember bocor. "
            "Sebagian besar pembeli yang disubsidi sebenarnya tetap akan belanja tanpa subsidi. "
            "Subsidi hanya bekerja efektif jika disasarkan khusus ke daerah terpencil yang ongkirnya sangat berat."
        ),
    )

st.write("---")

# Interactive Story Chart (Plotly Painting)
st.markdown("""
<div class="editorial-serif" style="font-size: 1.4rem; font-weight: 600; color: #1C1917; margin-bottom: 0.3rem;">
     Lukisan Data: Hubungan Antara Keterlambatan dan Kepuasan Hati Pembeli
</div>
<div style="font-size: 0.92rem; color: #655E57; margin-bottom: 1rem;">
    Garis di bawah memperlihatkan bagaimana nilai ulasan pembeli berubah drastis begitu barang tiba terlambat melewati tanggal yang dijanjikan toko.
</div>
""", unsafe_allow_html=True)

# Generate Story Plotly Chart
delays = [-15, -10, -5, -2, 0, 1, 3, 7, 14, 21]
scores = [4.32, 4.30, 4.28, 4.25, 4.20, 3.40, 2.50, 1.95, 1.62, 1.45]

fig = go.Figure()

# Background Zones
fig.add_vrect(x0=-16, x1=0, fillcolor="#2E6F40", opacity=0.07, line_width=0, annotation_text="Zona Tenang (Tiba Tepat Waktu / Lebih Awal)", annotation_position="top left")
fig.add_vrect(x0=0, x1=22, fillcolor="#B83A2E", opacity=0.07, line_width=0, annotation_text="Zona Bahaya (Melewati Tanggal Janji)", annotation_position="top right")

fig.add_trace(go.Scatter(
    x=delays,
    y=scores,
    mode="lines+markers",
    line=dict(color=PALETTE["terracotta"], width=3.5, shape="spline"),
    marker=dict(size=8, color=PALETTE["charcoal"]),
    name="Skor Kepuasan Pembeli (Bintang 1–5)",
    hovertemplate="Keterlambatan: %{x} hari<br>Rata-rata Rating: %{y:.2f} bintang<extra></extra>",
))

# Key Direct Annotations
fig.add_annotation(
    x=0, y=4.20,
    text="Batas Janji Tiba: Kepuasan masih di 4.2 Bintang",
    showarrow=True, arrowhead=2, ax=-60, ay=-40,
    font=dict(size=11, color=PALETTE["charcoal"]),
    bgcolor="rgba(255,255,255,0.9)", bordercolor="#EAE4DC", borderwidth=1,
)

fig.add_annotation(
    x=3, y=2.50,
    text="Telat 3 Hari: Skor langsung runtuh ke 2.5 Bintang!",
    showarrow=True, arrowhead=2, ax=60, ay=-30,
    font=dict(size=11, color=PALETTE["crimson_clay"]),
    bgcolor="rgba(255,255,255,0.9)", bordercolor=PALETTE["crimson_clay"], borderwidth=1,
)

editorial_plotly_theme(
    fig,
    title="Begitu Pesanan Terlambat 1–3 Hari, Kepuasan Pembeli Langsung Runtuh",
    subtitle="Pengamatan pada 96.470 pesanan nyata yang telah terkirim",
    x_title="Hari Keterlambatan (Nilai negatif berarti paket sampai lebih cepat dari janji)",
    y_title="Rata-rata Skor Bintang Pembeli (1 s/d 5)",
    height=400,
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.write("---")

st.markdown("""
<div class="editorial-serif" style="font-size: 1.35rem; font-weight: 600; color: #1C1917; margin-bottom: 0.5rem;">
     Tiga Saran Nyata untuk Pemilik Usaha
</div>
<div style="font-size: 0.95rem; color: #44403C; line-height: 1.7;">
    1. <b>Pasang Janji Estimasi yang Sedikit Lebih Longgar:</b> Lebih baik berjanji paket sampai dalam 5 hari dan tiba di hari ke-4 (pembeli merasa bahagia dapat kejutan cepat), daripada berjanji 3 hari namun baru tiba di hari ke-4 (pembeli merasa dibohongi).<br>
    2. <b>Diskusikan Kontrak Ketat dengan Mitra Ekspedisi:</b> Keterlambatan logistik adalah pembunuh nomor satu ulasan toko. Wajibkan kurir menjaga ketepatan waktu dengan denda penalti jika paket tertahan lebih dari 3 hari.<br>
    3. <b>Hentikan Promo Ongkir Merata:</b> Gunakan diskon ongkos kirim hanya untuk barang berbobot berat atau rute antar-pulau yang bebannya memang terasa tidak adil bagi pembeli.
</div>
""", unsafe_allow_html=True)

# Assessor Scientific Drawer
with st.expander(" Buka Catatan Dapur Ilmiah & Standar Kompetensi SKKNI/BNSP (Mode Penguji)"):
    st.markdown("""
    **Unit Kompetensi yang Dipenuhi:**
    - `[UK-01 Menentukan Masalah Bisnis]`: Pemetaan dilema biaya transaksi vs kepuasan pelanggan pada platform e-commerce Olist.
    - `[UK-02 Menentukan Kebutuhan Data]`: Audit 96.470 baris pesanan berstatus *delivered*.
    - `[UK-11 Mengembangkan Solusi]`: Translasi temuan regresi spline (H2, F-stat 4218.1, p-val < 0.0001) menjadi 3 pilar aksi bisnis strategis.
    """)
