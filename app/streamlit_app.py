import sys
from pathlib import Path
import pandas as pd
import streamlit as st

# Pastikan root proyek selalu terbaca di sys.path agar tidak pernah ImportError
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.csip.data.semantic_profiler import build_fluent_schema, fmt_num, get_builtin_dataset
from src.csip.models.ml_engine import simulate_and_narrate, train_fluent_ml_pipeline
from app.components.charts import build_cluster_map_chart, build_impact_curve_chart, build_ranking_chart

st.set_page_config(
    page_title="CSIP Studio — Bedah Data & Simulasi Keputusan",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-base: #07090E;
    --border-subtle: rgba(255, 255, 255, 0.08);
    --text-primary: #F3F4F6;
    --text-secondary: #9CA3AF;
    --accent-gold: #F5A623;
    --accent-cyan: #38BDF8;
    --accent-rose: #FB7185;
    --accent-emerald: #34D399;
}

#MainMenu, header, footer, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"] {
    display: none !important;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
    background: radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.06) 0%, transparent 40%),
                radial-gradient(circle at 85% 25%, rgba(245, 166, 35, 0.06) 0%, transparent 45%),
                #07090E !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.block-container {
    padding-top: 1.1rem !important;
    padding-bottom: 1rem !important;
    padding-left: 2.2rem !important;
    padding-right: 2.2rem !important;
    max-width: 1580px !important;
}

.studio-topbar { display: flex; align-items: center; justify-content: space-between; }
.brand-wrap { display: flex; align-items: baseline; gap: 12px; }
.brand-mark { font-family: 'Instrument Serif', serif; font-size: 2rem; color: #FFFFFF; line-height: 1; }
.brand-badge {
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; text-transform: uppercase;
    letter-spacing: 0.12em; padding: 4px 10px; border-radius: 999px;
    background: rgba(52, 211, 153, 0.12); border: 1px solid rgba(52, 211, 153, 0.35); color: var(--accent-emerald);
}
.brand-sub { font-size: 0.82rem; color: var(--text-secondary); }
.section-tag {
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; text-transform: uppercase;
    letter-spacing: 0.14em; color: var(--accent-gold); margin-bottom: 0.45rem; display: block;
}

div[data-baseweb="slider"] div[role="slider"] {
    background-color: #F5A623 !important; box-shadow: 0 0 10px rgba(245, 166, 35, 0.6) !important;
}
div[data-testid="stSlider"] label p { font-size: 0.82rem !important; color: #F3F4F6 !important; font-weight: 600 !important; }
div[data-testid="stThumbValue"] { color: #F5A623 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.74rem !important; }

div[role="radiogroup"] {
    background: rgba(15, 19, 29, 0.88); padding: 4px; border-radius: 11px;
    border: 1px solid rgba(255, 255, 255, 0.07); display: inline-flex; gap: 5px;
}
div[role="radiogroup"] label { background: transparent !important; border: none !important; padding: 5px 12px !important; border-radius: 8px !important; margin: 0 !important; }
div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child { display: none !important; }
div[role="radiogroup"] label p { font-size: 0.79rem !important; color: #9CA3AF !important; }
div[role="radiogroup"] label:has(input:checked) { background: rgba(245, 166, 35, 0.16) !important; border: 1px solid rgba(245, 166, 35, 0.45) !important; }
div[role="radiogroup"] label:has(input:checked) p { color: #F5A623 !important; font-weight: 600 !important; }

.bento-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 12px; }
.bento-card {
    background: linear-gradient(180deg, rgba(22, 28, 42, 0.85) 0%, rgba(13, 17, 26, 0.95) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 15px 18px; position: relative; overflow: hidden;
}
.bento-card::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: var(--card-accent, #F5A623); }
.bento-label { font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.1em; color: #94A3B8; margin-bottom: 5px; }
.bento-value { font-size: 1.55rem; font-weight: 700; letter-spacing: -0.02em; color: #FFFFFF; line-height: 1.2; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bento-sub { display: flex; align-items: center; justify-content: space-between; font-size: 0.74rem; color: #9CA3AF; gap: 8px; }
.bento-pill { font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; padding: 2px 8px; border-radius: 6px; background: rgba(255,255,255,0.06); color: var(--card-accent, #F5A623); white-space: nowrap; }

.meaning-box {
    background: rgba(16, 22, 35, 0.85); border: 1px solid rgba(56, 189, 248, 0.22);
    border-left: 3px solid #38BDF8; border-radius: 11px; padding: 10px 13px; margin-bottom: 12px; font-size: 0.79rem; color: #E2E8F0; line-height: 1.48;
}
.stage-title { font-family: 'Instrument Serif', serif; font-size: 1.42rem; color: #F8FAFC; }
.stage-caption { font-size: 0.78rem; color: #94A3B8; }
.story-box {
    margin-top: 6px; background: linear-gradient(90deg, rgba(245, 166, 35, 0.08) 0%, rgba(14, 18, 28, 0.96) 28%);
    border: 1px solid rgba(255, 255, 255, 0.09); border-left: 3px solid var(--diag-color, #F5A623); border-radius: 12px; padding: 15px 20px;
}
.story-headline { font-family: 'Instrument Serif', serif; font-size: 1.28rem; color: #FFFFFF; margin-bottom: 6px; line-height: 1.3; }
.story-body { font-size: 0.88rem; color: #E2E8F0; line-height: 1.6; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource
def get_cached_pipeline(df_sig: int, df: pd.DataFrame, target_col: str, features: list[str], schema_info: dict, audit_info: dict):
    return train_fluent_ml_pipeline(df, target_col, features, schema_info, audit_info)


top_l, top_r = st.columns([2.9, 1.3], vertical_alignment="center")
with top_l:
    st.markdown(
        """
        <div class="studio-topbar">
            <div class="brand-wrap">
                <span class="brand-mark">CSIP Studio</span>
                <span class="brand-badge">Modular SKKNI Architecture</span>
                <span class="brand-sub">Bedah Data Otomatis & Simulator Keputusan Berbahasa Manusia</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.07); margin: 0.4rem 0 1.0rem 0;'>", unsafe_allow_html=True)

col_left, col_right = st.columns([1.15, 2.25], gap="large")

with col_left:
    st.markdown('<span class="section-tag">Langkah 1 — Pilih Kasus atau Masukkan CSV</span>', unsafe_allow_html=True)

    uploaded_csv = st.file_uploader(
        "Unggah File CSV Apa Saja (Bisnis, Toko Online, Keuangan, dll.):",
        type=["csv"],
    )

    if uploaded_csv is not None:
        raw_df = pd.read_csv(uploaded_csv)
        dataset_title = f"File: {uploaded_csv.name}"
    else:
        preset_choice = st.selectbox(
            "Atau Pilih Studi Kasus Bawaan:",
            options=[
                "Kasus 1: Toko Online & Kepuasan Pembeli (Data Olist)",
                "Kasus 2: Risiko Kesehatan & Gaya Hidup (Data Medis)",
                "Kasus 3: Kualitas Produk & Komposisi Bahan (Data Mutu)",
            ],
            label_visibility="collapsed",
        )
        raw_df = get_builtin_dataset(preset_choice)
        dataset_title = preset_choice

    active_df, schema_info, auto_target, audit_info = build_fluent_schema(raw_df)
    human_cols = list(schema_info.keys())

    if len(human_cols) < 2:
        st.error("Tabel ini membutuhkan minimal 2 kolom angka agar dapat dibedah.")
        st.stop()

    target_idx = human_cols.index(auto_target) if auto_target in human_cols else len(human_cols) - 1
    # Gunakan key dinamis berdasarkan nama dataset agar otomatis memilih target terbaik saat ganti CSV!
    target_col = st.selectbox(
        "Hasil Apa yang Ingin Kamu Bedah / Tingkatkan?",
        options=human_cols,
        index=target_idx,
        key=f"target_select_{dataset_title}",
    )

    t_meta = schema_info[target_col]
    st.markdown(
        f"""
        <div class="meaning-box">
            <b>{t_meta['banner_note']}</b><br>
            Fokus utama: <b>{target_col}</b> — <i>{t_meta['description'].lower()}</i>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    candidate_features = [c for c in human_cols if c != target_col]
    df_signature = hash((dataset_title, target_col, tuple(candidate_features), len(active_df)))
    pipeline = get_cached_pipeline(df_signature, active_df, target_col, candidate_features, schema_info, audit_info)

    st.markdown('<span class="section-tag">Langkah 2 — Uji Coba Geser 3 Faktor Utama</span>', unsafe_allow_html=True)

    custom_inputs = {}
    top_3_rows = pipeline["stats_df"].iloc[:3]
    for idx, row_meta in top_3_rows.iterrows():
        f_name = row_meta["Fitur"]
        f_min = float(row_meta["Min"])
        f_max = float(row_meta["Max"])
        f_med = float(row_meta["Median"])
        if f_max <= f_min:
            f_max = f_min + 1.0
        step_val = (f_max - f_min) / 100.0

        custom_inputs[f_name] = st.slider(
            f"{idx+1}. {f_name}",
            min_value=f_min,
            max_value=f_max,
            value=f_med,
            step=step_val,
            key=f"slider_{dataset_title}_{target_col}_{f_name}",
        )
        st.caption(f"↳ {row_meta['Kalimat_Alami']}")


sim = simulate_and_narrate(pipeline, custom_inputs, target_col, schema_info)
top1_row = pipeline["stats_df"].iloc[0]
t_unit = schema_info[target_col]["unit"]

with top_r:
    with st.popover("Bukti Ilmiah, Audit Data & 11 Unit SKKNI", use_container_width=True):
        tab1, tab2, tab3 = st.tabs(["1. Kamus & Korelasi", "2. Adu Model (UK-08..11)", "3. Audit Data (UK-03..07)"])
        with tab1:
            show_df = pipeline["stats_df"][["Fitur", "Arti_Kolom", "Kalimat_Alami", "Pengaruh_Persen", "Pearson_r"]].copy()
            show_df["Pengaruh_Persen"] = show_df["Pengaruh_Persen"].round(1).astype(str) + "%"
            show_df["Pearson_r"] = show_df["Pearson_r"].round(2)
            st.dataframe(show_df, use_container_width=True, hide_index=True)
            csv_bytes = pipeline["stats_df"].to_csv(index=False).encode("utf-8")
            st.download_button(
                "Unduh Laporan Analisis Faktor (CSV)",
                data=csv_bytes,
                file_name=f"laporan_csip_{target_col.lower().replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with tab2:
            st.markdown("###### Perbandingan Skenario Algoritma (Baseline vs Utama)")
            st.dataframe(pipeline["benchmark_df"], use_container_width=True, hide_index=True)
            st.caption("Membuktikan UK-08 (Skenario Model), UK-09 (Pembangunan Model), UK-10 (Evaluasi), dan UK-11 (Review).")
        with tab3:
            aud = pipeline["audit_summary"]
            audit_table = pd.DataFrame([
                {"Tahapan SKKNI": "UK-03 & UK-04 (Telaah & Validasi Baris Awal)", "Hasil Eksekusi": f"{aud['raw_rows']:,} baris x {aud['raw_cols']} kolom"},
                {"Tahapan SKKNI": "UK-06 (Imputasi Nilai Kosong & Hapus Duplikat)", "Hasil Eksekusi": f"{aud['missing_fixed']} sel kosong ditambal, {aud['duplicates_removed']} duplikat dihapus"},
                {"Tahapan SKKNI": "UK-07 (Konstruksi & Encoding Kategori)", "Hasil Eksekusi": ", ".join(aud["encoded_cats"])},
                {"Tahapan SKKNI": "UK-05 (Filter Kolom Kolinear >94%)", "Hasil Eksekusi": ", ".join(aud["dropped_collinear"])},
            ])
            st.dataframe(audit_table, use_container_width=True, hide_index=True)

with col_right:
    pred_color = "#34D399" if sim["diff_val"] >= 0 else "#F5A623"
    delta_color = "#34D399" if abs(sim["diff_pct"]) < 0.8 or sim["diff_val"] >= 0 else "#FB7185"
    status_pill = "Kondisi Standar" if abs(sim["diff_pct"]) < 0.8 else ("Lebih Tinggi" if sim["diff_val"] > 0 else "Lebih Rendah")

    bento_html = f"""
    <div class="bento-grid">
        <div class="bento-card" style="--card-accent: {pred_color};">
            <div class="bento-label">Perkiraan {target_col}</div>
            <div class="bento-value" style="color: {pred_color};">{fmt_num(sim['pred_val'], t_unit)}</div>
            <div class="bento-sub">
                <span>Kondisi standar (Median): {fmt_num(sim['base_val'], t_unit)}</span>
                <span class="bento-pill">Simulasi Aktif</span>
            </div>
        </div>
        <div class="bento-card" style="--card-accent: #38BDF8;">
            <div class="bento-label">Penentu Utama (#1)</div>
            <div class="bento-value" style="font-size: 1.32rem;">{top1_row['Fitur']}</div>
            <div class="bento-sub">
                <span>Memegang {top1_row['Pengaruh_Persen']:.0f}% kendali</span>
                <span class="bento-pill" style="color:#38BDF8;">{top1_row['Arah_Singkat']}</span>
            </div>
        </div>
        <div class="bento-card" style="--card-accent: {delta_color};">
            <div class="bento-label">Selisih dari Kondisi Standar</div>
            <div class="bento-value" style="color: {delta_color}; font-size: 1.42rem;">{fmt_num(sim['diff_val'], t_unit)} ({sim['diff_pct']:+.1f}%)</div>
            <div class="bento-sub">
                <span>{pipeline['model_quality_label']}</span>
                <span class="bento-pill" style="color:{delta_color};">{status_pill}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(bento_html, unsafe_allow_html=True)

    hdr_l, hdr_r = st.columns([1.25, 1.75], vertical_alignment="center")
    with hdr_l:
        st.markdown(
            f"""
            <div>
                <div class="stage-title">Peta Perilaku Data: {target_col}</div>
                <div class="stage-caption">Dihitung langsung dari {pipeline['n_rows']:,} baris bersih di '{dataset_title}'</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with hdr_r:
        active_lens = st.radio(
            "Pilih Tampilan Grafik",
            options=[
                "1. Kurva Simulasi & Titik Kritis",
                "2. Peringkat Faktor Penentu",
                "3. Sebaran Kelompok Data",
            ],
            horizontal=True,
            label_visibility="collapsed",
        )

    if active_lens == "1. Kurva Simulasi & Titik Kritis":
        fig = build_impact_curve_chart(pipeline, sim, target_col, schema_info)
    elif active_lens == "2. Peringkat Faktor Penentu":
        fig = build_ranking_chart(pipeline, target_col)
    else:
        fig = build_cluster_map_chart(pipeline, sim, target_col, custom_inputs, schema_info)

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        f"""
        <div class="story-box" style="--diag-color: {pred_color};">
            <div class="story-headline">{sim['headline']}</div>
            <div class="story-body">{sim['full_narrative']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
