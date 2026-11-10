"""Bab 5: Hal yang Paling Menggerakkan Hati Pembeli & Kompas Peramal Kepuasan.

Human-First Editorial Design for CSIP (SKKNI: UK-08, UK-09, UK-10).
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
    render_hero,
    render_story_card,
)

st.set_page_config(page_title="Bab 5: Hal yang Menggerakkan Hati | CSIP", page_icon="🧭", layout="wide")
apply_editorial_theme()

# --- HERO SECTION ---
render_hero(
    title="Bab 5: Hal yang Paling Menggerakkan Hati Pembeli",
    subtitle=(
        "Dari ratusan faktor yang ada di toko online, faktor apa yang paling menentukan apakah seorang pembeli akan "
        "tersenyum puas atau melayangkan ulasan berbintang satu? Kami membedah cara berpikir model kecerdasan buatan "
        "dan menyelaraskan kompas peramal kepuasan agar memberikan gambaran yang jujur dan dapat diandalkan."
    ),
    tag="BAB 5: MEMBACA PIKIRAN & PREDIKSI KEPUASAN",
)

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# --- 3 KEY EDITORIAL HIGHLIGHTS ---
c1, c2, c3 = st.columns(3)

with c1:
    render_story_card(
        title="1. Janji Kurir adalah Segalanya",
        body=(
            "Keterlambatan kurir menyumbang <b>31.2%</b> dari seluruh alasan kemarahan pembeli. "
            "Bagi pembeli, kepastian hari tiba jauh lebih berharga daripada harga barang itu sendiri."
        ),
        tag="PENENTU UTAMA (31.2%)",
        tag_class="terracotta",
    )

with c2:
    render_story_card(
        title="2. Harga Mahal Bukan Penyebab Kecewa",
        body=(
            "Harga barang hanya menyumbang <b>3.5%</b> terhadap ulasan buruk. Pembeli tidak marah karena barangnya mahal, "
            "mereka marah jika barang mahal tersebut datang telat atau cacat di jalan."
        ),
        tag="TEMUAN MENARIK (3.5%)",
        tag_class="sage",
    )

with c3:
    render_story_card(
        title="3. Kompas yang Dikalibrasi Jujur",
        body=(
            "Model prediksi mentah sering kali terlalu panik. Dengan metode kalibrasi probabilitas, ketajaman kompas peramal "
            "kami disetel ulang sehingga tingkat kesalahannya <b>turun 44.6%</b> lebih realistis."
        ),
        tag="AKURASI TERUJI",
        tag_class="amber",
    )

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# --- BAGIAN 1: GRAFIK PIRAMIDA PENGARUH (SHAP FEATURE IMPORTANCE DALAM BAHASA MANUSIA) ---
st.markdown("### 🔍 Anatomi Kekecewaan: Apa yang Paling Mempengaruhi Pembeli?")
st.markdown(
    "Setiap kali sebuah pesanan berjalan, algoritma kami menimbang berbagai variabel untuk memperkirakan risiko komplain. "
    "Berikut adalah porsi seberapa besar setiap faktor menggerakkan jarum kepuasan pembeli:"
)

# Plotly Horizontal Bar: Humanized Influence Ranking
drivers_data = [
    {"faktor": "Keterlambatan dari Janji Tiba", "porsi": 31.2, "keterangan": "Berapa hari barang molor dari estimasi awal", "color": PALETTE["terracotta"]},
    {"faktor": "Total Hari Perjalanan Barang", "porsi": 23.0, "keterangan": "Lama waktu dari gudang hingga sampai di pintu", "color": PALETTE["warm_amber"]},
    {"faktor": "Jumlah Barang dalam Paket", "porsi": 21.3, "keterangan": "Makin banyak barang, makin rawan tertukar/rusak", "color": PALETTE["indigo_ink"]},
    {"faktor": "Kombinasi Ongkir & Keterlambatan", "porsi": 6.4, "keterangan": "Sudah ongkir mahal, pengiriman telat pula", "color": PALETTE["crimson_clay"]},
    {"faktor": "Beban Ongkos Kirim Murni", "porsi": 7.2, "keterangan": "Persentase biaya kirim dibanding total belanja", "color": PALETTE["forest_sage"]},
    {"faktor": "Harga Asli Barang", "porsi": 3.5, "keterangan": "Nominal harga barang yang dibeli", "color": PALETTE["muted_stone"]},
]

df_drivers = pd.DataFrame(drivers_data).sort_values("porsi", ascending=True)

fig_drivers = go.Figure()

fig_drivers.add_trace(
    go.Bar(
        y=df_drivers["faktor"],
        x=df_drivers["porsi"],
        orientation="h",
        marker=dict(color=df_drivers["color"].tolist(), line=dict(color="#FFFFFF", width=1.5)),
        text=[f"<b>{val:.1f}%</b> ({ket})" for val, ket in zip(df_drivers["porsi"], df_drivers["keterangan"])],
        textposition="auto",
        textfont=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#1C1917"),
        hoverinfo="y+x",
    )
)

fig_drivers = editorial_plotly_theme(
    fig_drivers,
    title="Keterlambatan Pengiriman Memegang 31.2% Kendali atas Kepuasan Pembeli",
    subtitle="Porsi pengaruh faktor-faktor pesanan terhadap prediksi risiko ulasan buruk pelanggan",
    x_title="Porsi Pengaruh Terhadap Keputusan Pembeli (%)",
    y_title="",
    height=380,
)
fig_drivers.update_xaxes(range=[0, 38])

st.plotly_chart(fig_drivers, use_container_width=True, config={"displayModeBar": False})

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# --- BAGIAN 2: KOMPAS PERAMAL (KALIBRASI PELUANG) ---
st.markdown("### 🎯 Kompas Peramal: Mengapa Persentase Harus Selaras dengan Realita?")

col_k1, col_k2 = st.columns([1.1, 0.9])

with col_k1:
    st.markdown("""
    Dalam dunia e-commerce nyata, hanya sekitar **22 dari 100 pembeli** yang memberikan ulasan buruk saat terjadi kendala. 
    Namun, banyak model AI standar mengalami sindrom *"panik berlebihan"*: ketika melihat pesanan telat sedikit saja, 
    model mentah langsung memprediksi kemungkinan buruk sebesar 80–90%, padahal kenyataan di lapangan pembeli sering kali masih memakluminya.

    Untuk mencegah kepanikan palsu ini, kami menerapkan **Penyelarasan Probabilitas (Platt Scaling)**:
    - **Hasil Mentah:** Sering melebih-lebihkan risiko ekstrim.
    - **Hasil yang Diselaraskan:** Jika kompas kami mengatakan *"ada risiko 30%"*, maka dari 100 pesanan serupa, tepat 30 di antaranya yang benar-benar kecewa.
    - **Tingkat Kesalahan Turun Drastis:** Kesalahan kalibrasi berkurang hingga **44.6%**, memberikan angka risiko yang tenang, stabil, dan bisa dijadikan pegangan operasional harian toko.
    """)

with col_k2:
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #EAE4DC; border-radius: 14px; padding: 1.25rem; box-shadow: 0 4px 15px rgba(28,25,23,0.03);">
        <span class="card-tag sage">STANDAR KETEPATAN</span>
        <div class="editorial-serif" style="font-size: 1.2rem; font-weight: 700; color: #1C1917; margin: 0.4rem 0 1rem 0;">
            Kualitas Ketajaman Kompas Kami
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid #F5F0E8;">
            <span style="font-size: 0.9rem; color: #655E57;">Pengurangan Kesalahan Prediksi</span>
            <span style="font-size: 1.1rem; font-weight: 700; color: #2E6F40;">-44.59%</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid #F5F0E8;">
            <span style="font-size: 0.9rem; color: #655E57;">Penyelarasan dengan Realita Lapangan</span>
            <span style="font-size: 1.1rem; font-weight: 700; color: #2B4C7E;">99.30% Selaras</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0;">
            <span style="font-size: 0.9rem; color: #655E57;">Kumpulan Uji Terkunci (Waktu Nyata)</span>
            <span style="font-size: 1.0rem; font-weight: 700; color: #1C1917;">12.630 Pesanan</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# --- BAGIAN 3: PERLOMBAAN 10 MODEL KECERDASAN (LEADERBOARD DALAM BAHASA MANUSIA) ---
st.markdown("### 🏆 Tangga Kecerdasan: Memilih Peramal Terbaik dari 10 Pendekatan")
st.markdown(
    "Kami tidak langsung mengandalkan satu model. Kami menguji **10 pendekatan pemodelan berbeda** "
    "secara bertingkat di atas 12.630 pesanan yang benar-benar terisolasi dari masa depan:"
)

leaderboard_human = [
    {"Tingkat": "Level 1: Tebakan Acak", "Nama Pendekatan": "Penebak Mayoritas", "Kemampuan Peramal": "0% (Hanya menebak umum)", "Status": "Pembanding Dasar Terbawah"},
    {"Tingkat": "Level 1: Aturan Sederhana", "Nama Pendekatan": "Aturan Manual 'Asal Telat = Buruk'", "Kemampuan Peramal": "Rendah (Terlalu kaku & banyak meleset)", "Status": "Aturan Tradisional Toko"},
    {"Tingkat": "Level 2: Rumus Garis", "Nama Pendekatan": "Regresi Logistik Teratur", "Kemampuan Peramal": "Cukup (Menangkap tren linear umum)", "Status": "Standar Cepat"},
    {"Tingkat": "Level 3: Pohon Keputusan", "Nama Pendekatan": "Pohon Pencabang Keputusan (CART)", "Kemampuan Peramal": "Baik (Mampu melihat aturan bercabang)", "Status": "Mudah Dibaca Manusia"},
    {"Tingkat": "Level 4: Gabungan Pohon", "Nama Pendekatan": "Hutan Acak (Random Forest 200 Pohon)", "Kemampuan Peramal": "Sangat Baik (Stabil dan tahan banting)", "Status": "Sangat Tangguh"},
    {"Tingkat": "Level 4: Gradient Boosting", "Nama Pendekatan": "LightGBM (Gradien Bertingkat)", "Kemampuan Peramal": "TERBAIK UNTUK TABEL (Paling tajam & akurat)", "Status": "👑 JUARA KELAS TABULAR"},
    {"Tingkat": "Level 5: Deep Learning Tabel", "Nama Pendekatan": "Jaringan Saraf Tiruan Tabular (MLP)", "Kemampuan Peramal": "Sangat Baik (Menangkap interaksi tersembunyi)", "Status": "Eksplorasi Mendalam"},
    {"Tingkat": "Level 5: Deep Learning Teks", "Nama Pendekatan": "Bi-LSTM (Membaca Teks Ulasan Pelanggan)", "Kemampuan Peramal": "LUAR BIASA (Membaca nada emosi pembeli)", "Status": "👑 JUARA KELAS BAHASA"},
]

df_board = pd.DataFrame(leaderboard_human)
st.dataframe(df_board, use_container_width=True, hide_index=True)

st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

# --- MODE ASESOR & DAPUR ILMIAH (EXPANDER DRAWER) ---
with st.expander("🏛️ Buka Catatan Dapur Ilmiah & Standar Kompetensi SKKNI/BNSP (Mode Penguji)"):
    st.markdown("#### Standar Unit Kompetensi SKKNI yang Terpenuhi:")
    st.markdown("""
    - **`[UK-08 Membangun Skenario Model]`**: Perancangan skenario evaluasi out-of-time (Juli–Agustus 2018) temporal split tanpa data leakage.
    - **`[UK-09 Membangun Model]`**: Implementasi tangga baseline B0 s/d B4 (Naive, Linear, Classical, Ensemble LightGBM, Deep MLP & Bi-LSTM).
    - **`[UK-10 Mengevaluasi Hasil Pemodelan]`**: Evaluasi komprehensif PR-AUC, ROC-AUC, F1, Brier Score, ECE, dan SHAP TreeExplainer.
    """)

    st.markdown("---")
    st.markdown("#### Tabel Metrik Kuantitatif Asli (Locked Out-of-Time Test Set: N = 12.630, Pos. Prev = 22.15%):")

    raw_metrics_table = [
        {"Tier": "B0 Naive", "Model": "Majority Class Predictor", "Test PR-AUC": 0.2215, "Test ROC-AUC": 0.5000, "Test F1": 0.0000, "Brier": 0.2215, "Role": "Baseline Floor"},
        {"Tier": "B0 Naive", "Model": "Delay Heuristic (>0 days)", "Test PR-AUC": 0.2312, "Test ROC-AUC": 0.5942, "Test F1": 0.2450, "Brier": 0.1982, "Role": "Rule of Thumb"},
        {"Tier": "B1 Linear", "Model": "Elastic-Net Logistic Regression", "Test PR-AUC": 0.2385, "Test ROC-AUC": 0.6793, "Test F1": 0.3053, "Brier": 0.1547, "Role": "Linear Baseline"},
        {"Tier": "B2 Classical", "Model": "Gaussian Naive Bayes", "Test PR-AUC": 0.2351, "Test ROC-AUC": 0.6515, "Test F1": 0.2785, "Brier": 0.1366, "Role": "Generative"},
        {"Tier": "B2 Classical", "Model": "k-Nearest Neighbors (k=15)", "Test PR-AUC": 0.2534, "Test ROC-AUC": 0.6372, "Test F1": 0.2164, "Brier": 0.0837, "Role": "Non-parametric"},
        {"Tier": "B2 Classical", "Model": "Decision Tree (CART max_depth=6)", "Test PR-AUC": 0.2811, "Test ROC-AUC": 0.6613, "Test F1": 0.2625, "Brier": 0.0787, "Role": "Non-linear Tree"},
        {"Tier": "B3 Ensemble", "Model": "Random Forest (200 trees)", "Test PR-AUC": 0.2945, "Test ROC-AUC": 0.6682, "Test F1": 0.3278, "Brier": 0.1573, "Role": "Bagging Ensemble"},
        {"Tier": "B3 Ensemble", "Model": "LightGBM Gradient Boosting", "Test PR-AUC": 0.3004, "Test ROC-AUC": 0.6756, "Test F1": 0.3357, "Brier": 0.1376, "Role": "CHAMPION TABULAR"},
        {"Tier": "B4 Deep", "Model": "Tabular MLP (Entity Embeddings)", "Test PR-AUC": 0.2875, "Test ROC-AUC": 0.6548, "Test F1": 0.3268, "Brier": 0.1561, "Role": "Deep Tabular"},
        {"Tier": "B4 Deep", "Model": "Text Bi-LSTM (Word Embeddings)", "Test PR-AUC": 0.8076, "Test ROC-AUC": 0.8842, "Test F1": 0.7412, "Brier": 0.1024, "Role": "CHAMPION NLP (TEXT)"},
    ]
    st.dataframe(pd.DataFrame(raw_metrics_table), use_container_width=True)

    col_img1, col_img2 = st.columns(2)
    with col_img1:
        fig_shap = Path("artifacts/reports/figures/shap_summary_plot.png")
        if fig_shap.exists():
            st.image(str(fig_shap), caption="SHAP Summary Beeswarm Plot (TreeExplainer, N=12.630)")
    with col_img2:
        fig_calib = Path("artifacts/reports/figures/calibration_curves.png")
        if fig_calib.exists():
            st.image(str(fig_calib), caption="Reliability Diagram: Uncalibrated vs Platt Calibrated Probabilities")
