"""Omni Input: Interactive multi-mode command canvas for human input.

Provides 5 glass capsules, free-text box, and CSV dropzone without any emojis.
Adheres to the Nocturnal Gallery human-first design system.
"""

from __future__ import annotations

import io
from typing import Any, Dict, Optional, Tuple
import pandas as pd
import streamlit as st

from src.csip.engine.omni_router import PRESET_QUERIES, parse_user_query
from src.csip.engine.universal_csv_xray import UniversalCSVXRay


def render_omni_input() -> Dict[str, Any]:
    """Render universal interactive command input canvas with 5 mode capsules."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.25em; color: #F5B041; text-transform: uppercase;">
            LAB KEPUTUSAN UNIVERSAL
        </div>
        <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 2.8rem; font-weight: 600; color: #F4F1EA; margin: 0.3rem 0; letter-spacing: -0.01em;">
            Kotak Tanya dan Uji Keputusan
        </div>
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.92rem; color: #8E95A5; max-width: 720px; margin: 0 auto;">
            Ketik pertanyaan perilaku, uji pengandaian, adu dua rencana, atau jatuhkan file tabel milikmu di sini.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5 Glass Capsules (STRICTLY NO EMOJIS)
    mode_options = [
        "Bedah Fenomena",
        "Uji Pengandaian",
        "Adu Dua Pilihan",
        "Peta Suara Manusia",
        "Rontgen File CSV",
    ]

    selected_mode_label = st.radio(
        "Pilih Ragam Eksplorasi:",
        options=mode_options,
        horizontal=True,
        label_visibility="collapsed",
        key="active_capsule_mode",
    )

    mode_map = {
        "Bedah Fenomena": "bedah",
        "Uji Pengandaian": "pengandaian",
        "Adu Dua Pilihan": "adu",
        "Peta Suara Manusia": "teks",
        "Rontgen File CSV": "csv",
    }
    active_mode = mode_map[selected_mode_label]

    # Session state key for text input
    text_key = f"input_text_{active_mode}"
    if text_key not in st.session_state:
        st.session_state[text_key] = PRESET_QUERIES.get(active_mode, "")

    col_btn, _ = st.columns([1.5, 4.5])
    with col_btn:
        if st.button("Muat Contoh Nyata", key=f"btn_preset_{active_mode}", use_container_width=True):
            st.session_state[text_key] = PRESET_QUERIES.get(active_mode, "")

    uploaded_df: Optional[pd.DataFrame] = None

    if active_mode == "csv":
        # CSV Upload Zone
        st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Unggah File CSV Milikmu (Data Dagang, Sekolah, atau Keuangan):",
            type=["csv"],
            key="csv_uploader",
            label_visibility="visible",
        )
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                st.markdown(f"<div style='font-size:0.85rem; color:#F5B041; margin-top:0.3rem;'>File berhasil dimuat: {len(uploaded_df):,} baris dan {len(uploaded_df.columns)} kolom.</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Gagal membaca file CSV: {e}")
        else:
            # Use sample CSV generator as preset
            st.markdown("<div style='font-size:0.85rem; color:#8E95A5; margin-top:0.3rem;'>Belum ada file diunggah. Menjalankan contoh data transaksi retail 350 baris secara otomatis.</div>", unsafe_allow_html=True)
            uploaded_df = UniversalCSVXRay.generate_sample_csv(350)
        user_text = "Analisis file CSV"
    elif active_mode == "teks":
        # Multiline Text Area
        user_text = st.text_area(
            "Tempelkan Kumpulan Kalimat, Keluhan, atau Ulasan di Sini (Satu Kalimat per Baris):",
            value=st.session_state[text_key],
            height=130,
            key=f"area_{active_mode}",
        )
    else:
        # Single Line Elegant Query Box
        placeholder_text = {
            "bedah": "Contoh: Mengapa orang rela antre mahal, tapi tempat murah justru sepi?",
            "pengandaian": "Contoh: Bagaimana jika biaya kirim dipotong 20 persen tapi waktu tiba bertambah 1 hari?",
            "adu": "Contoh: Pilihan A: Subsidi biaya kirim vs Pilihan B: Perbaikan disiplin waktu kurir",
        }.get(active_mode, "Ketik pertanyaan atau rencana keputusanmu...")

        user_text = st.text_input(
            "Pertanyaan atau Rencana Keputusan:",
            value=st.session_state[text_key],
            placeholder=placeholder_text,
            label_visibility="collapsed",
            key=f"input_{active_mode}",
        )

    # Route and parse parameters
    parsed = parse_user_query(user_text, default_mode=active_mode)
    parsed["mode"] = active_mode  # enforce explicitly selected mode
    parsed["raw_text"] = user_text
    parsed["uploaded_df"] = uploaded_df

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    return parsed

