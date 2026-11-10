"""Omni Input: Interactive multi-mode command canvas for human input.

Provides 5 glass capsules, free-text form, submit button, and CSV dropzone.
Guarantees session state persistence and immediate reactive rendering without emojis.
"""

from __future__ import annotations

import io
from typing import Any, Dict, Optional, Tuple
import pandas as pd
import streamlit as st

from src.csip.engine.omni_router import PRESET_QUERIES, parse_user_query
from src.csip.engine.universal_csv_xray import UniversalCSVXRay


def render_omni_input(**kwargs: Any) -> Dict[str, Any]:
    """Render universal interactive command input canvas with 5 mode capsules and form."""
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

    mode_map = {
        "Bedah Fenomena": "bedah",
        "Uji Pengandaian": "pengandaian",
        "Adu Dua Pilihan": "adu",
        "Peta Suara Manusia": "teks",
        "Rontgen File CSV": "csv",
    }

    # Initialize active mode in session state
    if "active_mode" not in st.session_state:
        st.session_state["active_mode"] = "bedah"

    # Match current active index
    current_label = [k for k, v in mode_map.items() if v == st.session_state["active_mode"]][0]
    selected_mode_label = st.radio(
        "Pilih Ragam Eksplorasi:",
        options=mode_options,
        index=mode_options.index(current_label),
        horizontal=True,
        label_visibility="collapsed",
        key="active_capsule_mode_selector",
    )

    new_mode = mode_map[selected_mode_label]
    if new_mode != st.session_state["active_mode"]:
        st.session_state["active_mode"] = new_mode
        # Refresh current text to preset of new mode
        st.session_state[f"input_text_{new_mode}"] = PRESET_QUERIES.get(new_mode, "")

    active_mode = st.session_state["active_mode"]
    text_key = f"input_text_{active_mode}"
    if text_key not in st.session_state:
        st.session_state[text_key] = PRESET_QUERIES.get(active_mode, "")

    # Top shortcut button to load preset example
    col_preset, _ = st.columns([1.5, 4.5])
    with col_preset:
        if st.button("Muat Contoh Nyata", key=f"btn_preset_{active_mode}", use_container_width=True):
            st.session_state[text_key] = PRESET_QUERIES.get(active_mode, "")
            st.session_state["trigger_analysis"] = True

    uploaded_df: Optional[pd.DataFrame] = None
    user_text = st.session_state.get(text_key, "")

    # Main Command Form to prevent unsubmitted rerun loss
    with st.form(key=f"omni_form_{active_mode}", clear_on_submit=False):
        if active_mode == "csv":
            st.markdown("<div style='font-size:0.85rem; color:#8E95A5; margin-bottom:0.5rem;'>Unggah file CSV Anda atau gunakan data retail bawaan:</div>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Unggah File CSV:",
                type=["csv"],
                key=f"uploader_{active_mode}",
                label_visibility="collapsed",
            )
            if uploaded_file is not None:
                try:
                    uploaded_df = pd.read_csv(uploaded_file)
                except Exception as e:
                    st.error(f"Gagal membaca file CSV: {e}")
            else:
                uploaded_df = UniversalCSVXRay.generate_sample_csv(350)

            user_text = "Rontgen file CSV aktif"
            btn_label = "Rontgen File Sekarang"

        elif active_mode == "teks":
            user_text = st.text_area(
                "Tempelkan Kumpulan Kalimat, Keluhan, atau Ulasan:",
                value=st.session_state[text_key],
                height=120,
                key=f"area_widget_{active_mode}",
                placeholder="Tempelkan ulasan atau kalimat di sini...",
            )
            btn_label = "Petakan Suara Sekarang"

        else:
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
                key=f"input_widget_{active_mode}",
            )
            btn_label = "Bedah Sekarang"

        col_submit, _ = st.columns([1.5, 4.5])
        with col_submit:
            submitted = st.form_submit_button(btn_label, use_container_width=True)

    # If submitted or triggered, update text in session state
    if submitted or st.session_state.get("trigger_analysis", False):
        st.session_state[text_key] = user_text
        st.session_state["trigger_analysis"] = False

    # Route and parse parameters with intelligent fallback
    parsed = parse_user_query(user_text, default_mode=active_mode)
    parsed["mode"] = active_mode
    parsed["raw_text"] = user_text
    parsed["uploaded_df"] = uploaded_df

    # Save to session_state as required
    st.session_state["current_query"] = parsed
    st.session_state["active_result"] = parsed

    # Render Primary Story Conclusion Card directly below input
    story = parsed.get("story_summary", {})
    headline = story.get("headline", "Hasil Analisis Perilaku")
    insight = story.get("insight", "Sistem telah memetakan dinamika perilaku dari masalah yang Anda masukkan.")
    metric_label = story.get("metric_label", "Fokus Utama")
    metric_val = story.get("metric_val", "Teranalisis")
    driver_focus = story.get("driver_focus", "Waktu dan Biaya")

    st.markdown(f"""
    <div style="background: rgba(20, 25, 38, 0.78); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); border-left: 4px solid #F5B041; border-radius: 16px; padding: 1.25rem 1.75rem; margin-top: 1.25rem; margin-bottom: 2.25rem; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);">
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.16em; color: #F5B041; font-weight: 600; margin-bottom: 0.35rem;">
            KESIMPULAN DARI MASALAH ANDA
        </div>
        <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 1.65rem; font-weight: 600; color: #F4F1EA; margin-bottom: 0.4rem; line-height: 1.3;">
            "{headline}"
        </div>
        <div style="font-size: 0.94rem; color: #F4F1EA; line-height: 1.6; margin-bottom: 0.85rem;">
            {insight}
        </div>
        <div style="display: flex; gap: 2rem; align-items: center; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 0.65rem; flex-wrap: wrap;">
            <div>
                <span style="font-size: 0.82rem; color: #8E95A5;">{metric_label}:</span>
                <span style="font-size: 1.1rem; font-weight: 700; color: #F5B041; margin-left: 0.4rem;">{metric_val}</span>
            </div>
            <div>
                <span style="font-size: 0.82rem; color: #8E95A5;">Faktor Penggerak:</span>
                <span style="font-size: 0.95rem; font-weight: 600; color: #38BDF8; margin-left: 0.4rem;">{driver_focus}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    return parsed
