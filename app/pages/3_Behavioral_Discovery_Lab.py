"""Bab 3: Mengenal Tipe Pembeli [UK-03, UK-07]."""

from pathlib import Path
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

from app.ui_components import (
    PALETTE,
    apply_editorial_theme,
    editorial_plotly_theme,
    render_hero,
    render_persona_card,
)

apply_editorial_theme()

render_hero(
    title="Bab 3: Tiga Kepribadian Manusia di Balik Layar Belanja",
    subtitle=(
        "Tidak ada pembeli yang benar-benar sama. Namun ketika puluhan ribu kebiasaan dipertemukan, "
        "mereka secara alami terbagi ke dalam 3 kelompok kepribadian dengan harapan dan ketakutan yang berbeda."
    ),
    tag="SKKNI Subbidang Data Science: J.62DMI00.012.1 & J.62DMI00.013.1 (Unsupervised Clustering)",
)

st.markdown("""
<div style="background: rgba(56, 189, 248, 0.12); border-left: 4px solid #38BDF8; padding: 0.5rem 1rem; border-radius: 4px; margin-bottom: 1rem; font-size: 0.86rem; color: #F4F1EA;">
    <b>UNIT KOMPETENSI INTI UNSUPERVISED:</b> Memenuhi <code>J.62DMI00.012.1</code> (Skenario Model) & <code>J.62DMI00.013.1</code> (Membangun Model) 
    melalui algoritma K-Means Clustering dengan metrik validasi Silhouette Score = 0.3865 dan stabilitas bootstrap ARI = 0.9832.
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="editorial-serif" style="font-size: 1.45rem; font-weight: 600; color: #1C1917; margin-bottom: 0.5rem;">
    Siapa Sebenarnya Orang yang Membuka Aplikasi Kita?
</div>
<div style="font-size: 0.98rem; color: #44403C; line-height: 1.7; margin-bottom: 1.5rem;">
    Memperlakukan semua pembeli dengan cara yang sama adalah resep kegagalan. 
    Seorang ibu yang membeli sabun cuci piring seharga tiga puluh ribu rupiah memiliki kecemasan yang jauh berbeda 
    dengan seorang pekerja yang membeli laptop seharga delapan juta rupiah. 
    Inilah potret 3 manusia yang kita layani setiap hari:
</div>
""", unsafe_allow_html=True)

# 3 Persona Cards
c1, c2, c3 = st.columns(3)

with c1:
    render_persona_card(
        name="Si Praktis Barang Tunggal",
        share_pct="51.0% (Mayoritas Toko)",
        avatar_emoji="",
        tag="Tulang Punggung Toko",
        habits="Membeli 1 barang yang langsung dibutuhkan saat itu juga. Nilai pesanan wajar dan ongkir terjangkau.",
        likes="Paket cepat sampai dalam hitungan hari dan kurir yang ramah.",
        dislikes="Ongkir dinaikkan tiba-tiba atau proses checkout yang berbelit-belit.",
    )

with c2:
    render_persona_card(
        name="Si Pejuang Ongkir Pelosok",
        share_pct="40.2% (Paling Rentan Kecewa)",
        avatar_emoji="",
        tag="Sensitif Ongkir & Waktu",
        habits="Tinggal jauh dari pusat kota. Membeli barang penting, namun ongkos kirimnya bisa menelan 38% dari total belanjaan.",
        likes="Kupon potongan ongkir dan kepastian tanggal paket mendarat di rumah.",
        dislikes="Sudah bayar ongkir mahal, paketnya malah telat berhari-hari. Kelompok ini 1.8x lebih sering memberi bintang 1.",
    )

with c3:
    render_persona_card(
        name="Si Pembeli Keranjang Mewah",
        share_pct="8.8% (Paling Bernilai)",
        avatar_emoji="",
        tag="Konsumen Premium",
        habits="Belanja dalam jumlah besar atau barang berharga tinggi. Beban ongkir tidak mereka permasalahkan.",
        likes="Kemasan ekstra aman, asuransi terpercaya, dan pelacakan kurir yang akurat.",
        dislikes="Barang penyok, cacat, atau perlakuan kurir yang sembrono.",
    )

st.write("---")

# Interactive Story Chart: Persona Composition & Behavior
st.markdown("""
<div class="editorial-serif" style="font-size: 1.35rem; font-weight: 600; color: #1C1917; margin-bottom: 0.3rem;">
     Perbandingan Nyata: Seberapa Besar Beban Ongkir Mereka?
</div>
<div style="font-size: 0.92rem; color: #655E57; margin-bottom: 1rem;">
    Grafik di bawah memperlihatkan perbandingan beban ongkos kirim terhadap harga barang di antara ketiga kepribadian pembeli.
</div>
""", unsafe_allow_html=True)

fig = go.Figure()

personas_list = ["Si Praktis Barang Tunggal", "Si Pejuang Ongkir Pelosok", "Si Pembeli Keranjang Mewah"]
freight_pcts = [14.1, 38.2, 7.8]
delivery_days = [9.2, 15.4, 12.8]

fig.add_trace(go.Bar(
    x=personas_list,
    y=freight_pcts,
    name="Persentase Beban Ongkir terhadap Nilai Barang (%)",
    marker_color=[PALETTE["indigo_ink"], PALETTE["terracotta"], PALETTE["forest_sage"]],
    text=[f"{v:.1f}%" for v in freight_pcts],
    textposition="outside",
    hovertemplate="Tipe: %{x}<br>Beban Ongkir: %{y:.1f}%<extra></extra>",
))

fig.add_annotation(
    x="Si Pejuang Ongkir Pelosok", y=38.2,
    text="Beban Sangat Berat: 38% uang keluar hanya untuk kurir!",
    showarrow=True, arrowhead=2, ax=70, ay=-35,
    font=dict(size=11, color=PALETTE["crimson_clay"]),
    bgcolor="rgba(255,255,255,0.9)", bordercolor=PALETTE["crimson_clay"], borderwidth=1,
)

editorial_plotly_theme(
    fig,
    title="Si Pejuang Ongkir Memikul Beban Biaya Kirim Terberat",
    subtitle="Perbandingan beban ongkir rata-rata untuk setiap kelompok pembeli",
    x_title="Tipe Karakter Pembeli",
    y_title="Porsi Ongkir dibandingkan Harga Barang (%)",
    height=400,
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with st.expander(" Buka Catatan Metodologi & Audit Ilmiah (Technical & Governance Notes)"):
    st.markdown(r"""
    **Fase Metodologi yang Dipenuhi:**
    - `[UK-07 Menentukan Objek Data]`: Algoritma *K-Means Clustering* dengan evaluasi $k \in [3, 4, 5, 6]$.
    - **Metrik Klasterisasi Objektif**: Terpilih $k=3$ dengan **Silhouette Score = 0.3865** (melampaui syarat Spesifikasi Sistem $\ge 0.35$), **Davies-Bouldin Index = 1.2168**, dan Calinski-Harabasz = 8.142,1.
    - **Deteksi Anomali Friksi**: Mengidentifikasi 4.824 pesanan ekstrem (5.0%) menggunakan Isolation Forest.
    - **Pencatatan Penemuan Ilmiah**: Terdaftar sebagai `DISC-01` (Tipe Friksi Tinggi) dan `DISC-03` (Mayoritas Barang Tunggal) dalam `EvidenceRegistry`.
    """)
