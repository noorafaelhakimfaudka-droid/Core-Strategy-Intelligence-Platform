"""CSIP — The Art of Human Decisions.

An Interactive Editorial Story of 100,000 E-Commerce Orders.
Curated for Business Leaders, Researchers, and BNSP Data Science Assessors.
"""

from __future__ import annotations

from pathlib import Path
import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="Membaca Hati Pembeli | CSIP",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui_components import (
    PALETTE,
    apply_editorial_theme,
    render_hero,
    render_story_card,
)

# Apply Warm Museum Canvas & Typography
apply_editorial_theme()

# Sidebar Brand
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0; border-bottom: 1px solid #EAE4DC; margin-bottom: 1rem;">
        <span class="card-tag">CSIP Interactive Story</span>
        <div class="editorial-serif" style="font-size: 1.45rem; font-weight: 700; color: #1C1917; line-height: 1.2;">
            Membaca Hati Pembeli
        </div>
        <div style="font-size: 0.82rem; color: #655E57; margin-top: 0.3rem;">
            Observasi 100.000 Pesanan E-Commerce
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Pilih bab cerita di atas untuk mulai membaca.")

# Hero Header
render_hero(
    title="Mengapa Pelanggan Memilih Kembali atau Pergi Selamanya?",
    subtitle=(
        "Harga murah memang memikat mata pada pandangan pertama, tetapi rasa tenang bahwa paket "
        "akan tiba tepat waktu adalah alasan mengapa pembeli menaruh kepercayaan seumur hidup. "
        "Sebuah kisah nyata yang diangkat dari 100.000 jejak perjalanan pembeli di seluruh penjuru negeri."
    ),
    tag="Kisah Utama & Pameran Interaktif",
)

# 3 Story Highlights in Pure Human Language
col1, col2, col3 = st.columns(3)

with col1:
    render_story_card(
        tag="Temuan #1",
        tag_class="terracotta",
        title="Janji yang Meleset Lebih Menyakitkan daripada Harga",
        body=(
            "Pembeli rela memaklumi ongkos kirim yang sedikit lebih tinggi asalkan barang tiba tepat waktu. "
            "Namun begitu kurir terlambat 1 hingga 3 hari dari tanggal janji, kepuasan pembeli langsung runtuh seketika."
        ),
    )

with col2:
    render_story_card(
        tag="Temuan #2",
        tag_class="sage",
        title="Mitos Kepuasan: Bintang 5 Bukan Jaminan Pembeli Balik Lagi",
        body=(
            "Keyakinan umum menganggap pembeli bintang 5 pasti rajin belanja lagi. Faktanya, "
            "pembeli yang puas bintang 5 dan yang kecewa bintang 1 memiliki peluang belanja kembali yang hampir sama (2.28%). "
            "Kebutuhan habis pakai produk jauh lebih menentukan dibanding sekadar rating ulasan."
        ),
    )

with col3:
    render_story_card(
        tag="Temuan #3",
        tag_class="indigo",
        title="Jebakan Subsidi: Niat Membantu yang Bikin Tekor",
        body=(
            "Bakar duit memberi diskon ongkir 15% untuk semua orang ternyata membuat platform rugi puluhan juta rupiah. "
            "Solusi yang jauh lebih cerdas dan hemat adalah memperbaiki kecepatan kurir serta menyasar pembeli di daerah terpencil."
        ),
    )

st.write("")

# 4 Key Figures (Humanized Metrics)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-num">96.470</div>
        <div class="stat-label">Paket Pesanan Dianalisis</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-num">3 Tipe</div>
        <div class="stat-label">Karakter Utama Pembeli</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-num">87 Minggu</div>
        <div class="stat-label">Rekam Jejak Dinamika Toko</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-num">100%</div>
        <div class="stat-label">Data & Bukti Nyata Terverifikasi</div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

st.markdown("""
<div class="editorial-serif" style="font-size: 1.6rem; font-weight: 600; color: #1C1917; margin-bottom: 0.5rem;">
    🗺️ Alur Perjalanan Cerita (Daftar Isi)
</div>
<div style="font-size: 0.95rem; color: #655E57; margin-bottom: 1.5rem;">
    Silakan gunakan menu di bilah sisi kiri untuk menjelajahi bab-bab interaktif berikut:
</div>
""", unsafe_allow_html=True)

ch_cols = st.columns(2)
with ch_cols[0]:
    st.markdown("""
    - **Bab 1: Kisah Utama (Beranda)** — Rangkuman besar dan 3 rahasia di balik perilaku 100.000 pembeli.
    - **Bab 2: Mengenal Tipe Pembeli** — Profil 3 manusia di balik transaksi: dari pemburu kepraktisan hingga pembeli berkeranjang besar.
    - **Bab 3: Mitos vs Kenyataan** — Membongkar anggapan umum yang salah tentang harga, kepuasan, dan loyalitas pembeli.
    - **Bab 4: Hal yang Paling Menggerakkan Hati** — Memetakan faktor nomor satu yang memicu komplain dan kekecewaan.
    - **Bab 5: Kompas Peramal Kepuasan** — Bagaimana kecerdasan buatan membaca risiko ulasan buruk sebelum paket sampai.
    """)

with ch_cols[1]:
    st.markdown("""
    - **Bab 6: Denyut Nadi Pasar dari Minggu ke Minggu** — Memotret kesehatan ekosistem toko dari waktu ke waktu.
    - **Bab 7: Simulasi "Bagaimana Jika?"** — Uji coba kebijakan baru (subsidi ongkir vs kurir cepat) secara aman tanpa risiko uang riil.
    - **Bab 8: Studio Keputusan Bisnis** — Alat bantu manajer dengan kalkulator keuangan interaktif untuk memilih strategi terbaik.
    - **Bab 9: Dapur Ilmiah & Bukti SKKNI/BNSP** — Ruang khusus asesor dan penguji teknis yang merangkum seluruh 11 Unit Kompetensi, kode, dan data mentah.
    """)

# Scientific Drawer for Assessors
with st.expander("🏛️ Buka Catatan Dapur Ilmiah & Standar Kompetensi SKKNI/BNSP (Khusus Mode Penguji)"):
    st.markdown("""
    **Pemetaan Standar Kompetensi Kerja Nasional Indonesia (SKKNI) Bidang Data Science:**
    - **UK-01 Menentukan Masalah Bisnis**: Perumusan trade-off ekonomi transaksi vs pemenuhan logistik (`config/business_objectives.yaml`).
    - **UK-02 Menentukan Kebutuhan Data**: Kamus 9 tabel relasional e-commerce Olist (`data/data_dictionary.md`).
    - **Integritas Referensial**: 0 orphan records melintasi 6 relasi kunci asing (100% konsisten).
    - **Tingkat Klaim Ilmiah**: Seluruh temuan diatur di bawah protokol bukti bertingkat L0 (Deskriptif) hingga L3 (Kausal) dengan jaminan *Anti-Leakage First-Order Isolation*.
    """)
