"""Omni Input: Single-Screen Unified Command Canvas.

Provides a unified input interface with quick prompt capsules, free-text form,
and CSV dropzone expander. 100% local processing, zero emojis, zero technical jargon.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple
import pandas as pd
import streamlit as st

from src.csip.engine.omni_router import PRESET_QUERIES, parse_user_query
from src.csip.engine.universal_csv_xray import UniversalCSVXRay


__all__ = ["render_omni_input", "QUICK_PROMPTS"]


QUICK_PROMPTS = [
    ("Kenapa Pelanggan Kabur?", "Mengapa orang rela membayar lebih mahal untuk barang yang datang cepat, tetapi tempat murah yang sering terlambat justru sepi?"),
    ("Uji Potong Biaya & Molor Waktu", "Bagaimana jika biaya tambahan dipotong 20 persen, namun waktu tunggu pengiriman bertambah 1 hari?"),
    ("Adu Pilihan: Subsidi vs Kurir", "Pilihan A: Subsidi biaya kirim untuk semua orang vs Pilihan B: Perbaikan disiplin waktu tiba mitra kurir."),
    ("Keluhan Keterlambatan Paket", "Paket terlambat lima hari dari tanggal janji, kurir lelet dan tidak ada kabar sama sekali hingga saya kapok belanja."),
    ("Pelayanan Kilat & Ramah", "Pengiriman kilat satu hari sampai, kurir sangat ramah dan kemasan rapi bintang lima."),
]


def render_omni_input(**kwargs: Any) -> Dict[str, Any]:
    """Render unified single-screen command input canvas."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.25em; color: #F5B041; text-transform: uppercase;">
            LAB KEPUTUSAN UNIVERSAL
        </div>
        <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 2.8rem; font-weight: 600; color: #F4F1EA; margin: 0.3rem 0; letter-spacing: -0.01em;">
            Kotak Tanya dan Uji Keputusan
        </div>
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.94rem; color: #8E95A5; max-width: 720px; margin: 0 auto; line-height: 1.5;">
            Ketik pertanyaan perilaku, uji rencana pengandaian, adu dua strategi, atau unggah tabel data milikmu.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for input query
    if "input_query_text" not in st.session_state:
        st.session_state["input_query_text"] = PRESET_QUERIES["bedah"]

    # Horizontal Quick Prompt Capsules
    st.markdown("""
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.1em; color: #8E95A5; text-transform: uppercase; margin-bottom: 0.5rem;">
        PILIHAN PERTANYAAN CEPAT:
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(QUICK_PROMPTS))
    for i, (label, prompt_text) in enumerate(QUICK_PROMPTS):
        with cols[i]:
            if st.button(label, key=f"quick_prompt_{i}", use_container_width=True):
                st.session_state["input_query_text"] = prompt_text
                st.session_state["active_csv_df"] = None
                st.rerun()

    uploaded_df: Optional[pd.DataFrame] = st.session_state.get("active_csv_df", None)

    # Main Command Form
    with st.form(key="unified_omni_form", clear_on_submit=False):
        user_input_val = st.text_area(
            "Ketik pertanyaan, skenario, atau masalah perilaku pelanggan:",
            value=st.session_state.get("input_query_text", ""),
            height=90,
            placeholder="Contoh: Mengapa orang kabur saat paket terlambat, meskipun harga barang sudah sangat murah?",
            label_visibility="collapsed",
        )

        with st.expander("Atau Jatuhkan File CSV Milikmu di Sini (Rontgen Data Mandiri)"):
            st.markdown("<div style='font-size:0.85rem; color:#8E95A5; margin-bottom:0.4rem;'>Unggah file tabel CSV apa saja untuk dibersihkan dan dianalisis secara instan:</div>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Unggah File CSV:",
                type=["csv"],
                key="unified_csv_uploader",
                label_visibility="collapsed",
            )
            if uploaded_file is not None:
                try:
                    uploaded_df = pd.read_csv(uploaded_file)
                    st.session_state["active_csv_df"] = uploaded_df
                    st.success(f"File CSV terbaca: {len(uploaded_df)} baris dan {len(uploaded_df.columns)} kolom.")
                except Exception as e:
                    st.error(f"Gagal membaca file CSV: {e}")

        col_submit, _ = st.columns([1.8, 4.2])
        with col_submit:
            submitted = st.form_submit_button("Bedah Sekarang", use_container_width=True)

    if submitted:
        st.session_state["input_query_text"] = user_input_val

    # Parse query using 100% local NLP Brain
    active_text = st.session_state.get("input_query_text", PRESET_QUERIES["bedah"])
    parsed = parse_user_query(active_text)

    # Attach CSV if uploaded
    if uploaded_df is not None and not uploaded_df.empty:
        parsed["mode"] = "csv"
        parsed["uploaded_df"] = uploaded_df

    st.session_state["engine_output"] = parsed
    return parsed
