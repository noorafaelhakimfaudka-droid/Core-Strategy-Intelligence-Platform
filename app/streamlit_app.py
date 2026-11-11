import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.csip.data.semantic_profiler import build_fluent_schema, fmt_num, get_builtin_dataset
from src.csip.models.ml_engine import simulate_and_narrate, train_fluent_ml_pipeline
from app.components.charts import (
    build_cluster_map_chart,
    build_impact_curve_chart,
    build_ranking_chart,
    build_ranking_html,
)

st.set_page_config(
    page_title="CSIP Studio — Ilmuwan Data Otomatis & Simulator Keputusan",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PROTOTYPE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=Inter:wght@400;450;500;600;700&display=swap');

:root {
  --bg:            #F5F2EC;
  --bg-deep:       #EDE9E1;
  --surface:       #FFFFFF;
  --surface-soft:  #FBFAF7;
  --surface-tint:  #F1F6F3;
  --line:          rgba(34, 30, 24, .08);
  --line-strong:   rgba(34, 30, 24, .14);
  --ink:           #1A1814;
  --ink-2:         #3A362F;
  --ink-3:         #5A554B;
  --ink-4:         #6A655A;
  --accent:        #0E6B63;
  --accent-2:      #17A394;
  --accent-soft:   rgba(14, 107, 99, .10);
  --accent-ring:   rgba(14, 107, 99, .22);
  --good:          #25694A;
  --good-soft:     rgba(47, 125, 91, .12);
  --warn:          #8A5A0C;
  --warn-2:        #E8A23B;
  --warn-soft:     rgba(232, 162, 59, .16);
  --bad:           #B5432F;
  --bad-soft:      rgba(181, 67, 47, .10);
  --font-display:  "Fraunces", "Iowan Old Style", Georgia, serif;
  --font-ui:       "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --r-xs: 6px;
  --r-sm: 10px;
  --r-md: 14px;
  --r-lg: 20px;
  --r-pill: 999px;
}

#MainMenu, header, footer, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"] {
  display: none !important;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
  font-family: var(--font-ui) !important;
  color: var(--ink) !important;
  background: linear-gradient(155deg, #F8F4EC 0%, #F2EEE5 38%, #E8F0EB 72%, #F4EBDC 100%) !important;
  font-variant-numeric: tabular-nums;
}

.aurora-bg {
  position: fixed; inset: 0; z-index: 0; overflow: hidden; pointer-events: none;
}
.aurora-bg i { position: absolute; border-radius: 50%; filter: blur(90px); }
.aurora-bg i:nth-child(1) {
  width: 680px; height: 680px; right: -150px; top: -240px; opacity: .55;
  background: radial-gradient(circle at 35% 35%, #4FD1C0 0%, rgba(23,163,148,0) 68%);
}
.aurora-bg i:nth-child(2) {
  width: 620px; height: 620px; left: -180px; bottom: -260px; opacity: .52;
  background: radial-gradient(circle at 55% 45%, #F7C46C 0%, rgba(232,162,59,0) 68%);
}
.aurora-bg i:nth-child(3) {
  width: 520px; height: 520px; left: 34%; top: 26%; opacity: .30;
  background: radial-gradient(circle, #BDA8F2 0%, rgba(150,125,230,0) 70%);
}

.block-container {
  position: relative; z-index: 1;
  padding-top: 0.75rem !important;
  padding-bottom: 1.2rem !important;
  padding-left: 1.6rem !important;
  padding-right: 1.6rem !important;
  max-width: 1600px !important;
}

.topbar-wrap {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 4px 12px;
  margin-bottom: 10px;
  border-bottom: 1px solid var(--line);
  position: relative;
}
.topbar-wrap::after {
  content: ""; position: absolute; left: 0; right: 0; bottom: -1px; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(23,163,148,.55) 30%, rgba(232,162,59,.55) 70%, transparent);
}
.brand { display: flex; align-items: center; gap: 12px; }
.logo-box {
  width: 28px; height: 28px; border-radius: 8px;
  background: linear-gradient(145deg, var(--accent-2), var(--accent) 70%);
  box-shadow: 0 1px 0 rgba(255,255,255,.4) inset, 0 0 18px rgba(23,163,148,.55), 0 4px 10px -3px rgba(14,107,99,.5);
  display: grid; place-items: center;
}
.brand-name { font-weight: 600; font-size: 16.5px; color: var(--ink); }
.badge-status {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12.5px; font-weight: 500; color: var(--accent);
  padding: 2px 10px 2px 8px; border-radius: var(--r-pill);
  background: var(--accent-soft); border: 1px solid var(--accent-ring);
}
.badge-status i {
  width: 6px; height: 6px; border-radius: 50%; background: var(--accent-2);
  box-shadow: 0 0 0 3px rgba(23,163,148,.22);
}
.brand-sub {
  color: var(--ink-3); font-size: 13.8px; padding-left: 12px;
  border-left: 1px solid var(--line-strong);
}

div[data-testid="stPopover"] > button {
  background: rgba(255, 255, 255, 0.82) !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid var(--line-strong) !important;
  border-radius: var(--r-sm) !important;
  color: var(--ink-2) !important;
  font-size: 13.5px !important;
  font-weight: 500 !important;
  height: 36px !important;
  box-shadow: 0 1px 0 rgba(255,255,255,.9) inset, 0 1px 2px rgba(34,30,24,.05) !important;
  transition: all .2s ease !important;
}
div[data-testid="stPopover"] > button:hover {
  border-color: rgba(23,163,148,.5) !important;
  box-shadow: 0 0 0 3px var(--accent-ring), 0 8px 20px -8px rgba(23,163,148,.45) !important;
  color: var(--accent) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.teal-source-marker) {
  position: relative !important;
  overflow: hidden !important;
  border-radius: 20px !important;
  padding: 16px 16px 18px !important;
  background:
    radial-gradient(320px 170px at 100% 0%, rgba(232,162,59,.28), transparent 70%),
    radial-gradient(300px 200px at 0% 100%, rgba(23,163,148,.36), transparent 70%),
    radial-gradient(rgba(255,255,255,.06) 1px, transparent 1.3px) 0 0 / 18px 18px,
    linear-gradient(160deg, #0F5A52 0%, #0A3F3A 55%, #072C29 100%) !important;
  border: 1px solid rgba(143,233,218,.26) !important;
  box-shadow:
    0 1px 0 rgba(255,255,255,.14) inset,
    0 0 0 1px rgba(6,40,38,.5),
    0 0 40px -10px rgba(23,163,148,.4),
    0 22px 44px -22px rgba(6,40,38,.7) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.teal-source-marker) label p {
  color: rgba(214, 243, 238, 0.78) !important;
  font-size: 13px !important;
  font-weight: 600 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.teal-source-marker) [data-testid="stFileUploaderDropzone"] {
  background: linear-gradient(180deg, rgba(255,255,255,.09), rgba(255,255,255,.03)) !important;
  border: 1.5px dashed rgba(143,233,218,.5) !important;
  border-radius: 14px !important;
  padding: 12px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.teal-source-marker) [data-testid="stFileUploaderDropzone"] * {
  color: #EAF7F4 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.teal-source-marker) [data-testid="stFileUploaderDropzone"] button {
  background: rgba(23, 163, 148, 0.28) !important;
  border: 1px solid rgba(143, 233, 218, 0.45) !important;
  color: #FFFFFF !important;
  border-radius: 8px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.teal-source-marker) div[data-baseweb="select"] > div {
  background: rgba(255, 255, 255, 0.09) !important;
  border: 1px solid rgba(191, 237, 230, 0.28) !important;
  border-radius: 10px !important;
  color: #F4FBF9 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.teal-source-marker) div[data-baseweb="select"] * {
  color: #F4FBF9 !important;
}

.step-head-teal {
  display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
}
.step-no-teal {
  font-size: 12.5px; font-weight: 600; color: #BFEDE6;
  width: 22px; height: 22px; border-radius: 50%;
  background: rgba(255,255,255,.09); border: 1px solid rgba(191,237,230,.38);
  display: grid; place-items: center;
}
.step-title-teal { font-weight: 600; font-size: 15px; color: #F4FBF9; }
.step-hint-teal { margin-left: auto; font-size: 12.5px; color: rgba(214,243,238,.68); }

.explain-teal {
  margin-top: 8px; padding: 11px 13px 12px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(232,162,59,.24), rgba(232,162,59,.08));
  border: 1px solid rgba(246,199,122,.4);
  box-shadow: 0 0 24px -10px rgba(232,162,59,.45);
}
.explain-tag-teal {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12.5px; font-weight: 600; color: #F6C77A;
}
.explain-tag-teal::before {
  content: ""; width: 14px; height: 2px; background: #E8A23B; border-radius: 2px;
}
.explain-teal p {
  margin-top: 5px; font-size: 13.5px; line-height: 1.55; color: rgba(244,250,248,.92);
}
.explain-teal b { color: #FFFFFF; font-weight: 600; }

div[data-testid="stVerticalBlockBorderWrapper"]:has(.warm-levers-marker) {
  background: linear-gradient(180deg, rgba(255,255,255,.86), rgba(255,255,255,.64)) !important;
  backdrop-filter: blur(20px) saturate(1.35) !important;
  border: 1px solid rgba(255,255,255,.8) !important;
  border-radius: 20px !important;
  padding: 15px 16px 16px !important;
  box-shadow: 0 0 0 1px rgba(34,30,24,.055), 0 1px 0 rgba(255,255,255,.95) inset, 0 20px 44px -26px rgba(12,70,64,.28) !important;
}

.step-head-light {
  display: flex; align-items: center; gap: 10px; margin-bottom: 6px;
}
.step-no-light {
  font-size: 12.5px; font-weight: 600; color: var(--ink-3);
  width: 22px; height: 22px; border-radius: 50%;
  border: 1px solid var(--line-strong); display: grid; place-items: center;
  background: var(--surface-soft);
}
.step-title-light { font-weight: 600; font-size: 15px; color: var(--ink); }

div[data-testid="stVerticalBlockBorderWrapper"]:has(.warm-levers-marker) div.stButton > button {
  height: 28px !important; padding: 0 11px !important; border-radius: 999px !important;
  font-size: 12.5px !important; font-weight: 500 !important; color: var(--ink-2) !important;
  background: rgba(255,255,255,.8) !important; border: 1px solid var(--line-strong) !important;
  min-height: 28px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.warm-levers-marker) div.stButton > button:hover {
  color: var(--accent) !important; border-color: rgba(23,163,148,.5) !important;
  box-shadow: 0 0 0 3px var(--accent-ring) !important;
}

.lv-card-head {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px 6px; border-radius: 14px 14px 0 0;
  margin-top: 6px;
}
.lv-1 { --c1:#5FD8C6; --c2:#17A394; --ct:#0E6B63; --soft:rgba(23,163,148,.13); }
.lv-2 { --c1:#F6C77A; --c2:#E8A23B; --ct:#9A6317; --soft:rgba(232,162,59,.16); }
.lv-3 { --c1:#C9B8F5; --c2:#8F78E6; --ct:#5B43B5; --soft:rgba(143,120,230,.14); }

.lv-ico {
  flex: none; width: 34px; height: 34px; border-radius: 10px;
  display: grid; place-items: center; color: var(--ct);
  background: linear-gradient(145deg, #FFFFFF, var(--soft));
  box-shadow: 0 0 0 1px rgba(34,30,24,.06);
}
.lv-title { min-width: 0; flex: 1; }
.lv-name { display: block; font-weight: 600; font-size: 14px; color: var(--ink); line-height: 1.2; }
.lv-meta { display: flex; align-items: center; gap: 6px; margin-top: 3px; }
.lv-rank {
  font-size: 11.5px; color: var(--ink-3); padding: 1px 6px;
  border-radius: 6px; background: var(--bg); border: 1px solid var(--line);
}
.lv-weight {
  font-size: 11.5px; font-weight: 500; color: var(--ct);
  background: var(--soft); padding: 1px 8px; border-radius: 999px;
}
.lv-val {
  display: flex; align-items: baseline; gap: 3px; flex: none;
  font-family: var(--font-display); color: var(--ct);
}
.lv-val b { font-weight: 500; font-size: 25px; line-height: 1; letter-spacing: -.01em; }
.lv-val small { font-family: var(--font-ui); font-size: 12px; color: var(--ink-3); }

.lv-note {
  margin-top: -6px; margin-bottom: 8px; padding: 6px 10px 6px 12px;
  border-radius: 9px; font-size: 13px; line-height: 1.45; color: var(--ink-2);
  background: linear-gradient(90deg, var(--soft), rgba(255,255,255,0) 90%);
  border-left: 2.5px solid var(--c2);
}

div[data-baseweb="slider"] div[role="slider"] {
  width: 20px !important; height: 20px !important;
  background: #FFFFFF !important;
  border: 2.5px solid #0E6B63 !important;
  box-shadow: 0 2px 6px rgba(34,30,24,.22), 0 0 0 4px rgba(23,163,148,.15) !important;
}
div[data-testid="stThumbValue"] { display: none !important; }
div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] {
  font-size: 11.5px !important; color: var(--ink-4) !important;
}

@property --ang { syntax:"<angle>"; inherits:false; initial-value:0deg; }
@keyframes spin { to { --ang:360deg; } }

.bento { display: grid; grid-template-columns: 1.15fr 1fr 1fr; gap: 14px; margin-bottom: 14px; }
.bento-card {
  position: relative; overflow: hidden; border-radius: 20px;
  padding: 14px 16px 14px;
  border: 1px solid rgba(255,255,255,.8);
  box-shadow: 0 0 0 1px rgba(34,30,24,.055), 0 1px 0 rgba(255,255,255,.95) inset, 0 20px 44px -26px rgba(12,70,64,.28);
  backdrop-filter: blur(20px) saturate(1.35);
}
.bento-card.c1 {
  background: radial-gradient(300px 150px at 100% 0%, var(--tint, rgba(23,163,148,.25)), transparent 72%),
              linear-gradient(180deg, rgba(255,255,255,.88), rgba(255,255,255,.66));
}
.bento-card.c1::before {
  content: ""; position: absolute; inset: 0; border-radius: inherit; padding: 1.5px; pointer-events: none;
  background: conic-gradient(from var(--ang), rgba(23,163,148,0) 0deg, #17A394 70deg, #E8A23B 140deg, rgba(232,162,59,0) 220deg);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude;
  animation: spin 7s linear infinite; opacity: .9;
}
.bento-card.c2 {
  background: radial-gradient(300px 150px at 100% 0%, rgba(23,163,148,.28), transparent 72%),
              linear-gradient(180deg, rgba(255,255,255,.88), rgba(255,255,255,.66));
}
.bento-card.c3 {
  background: radial-gradient(300px 150px at 100% 0%, var(--tint, rgba(232,162,59,.28)), transparent 72%),
              linear-gradient(180deg, rgba(255,255,255,.88), rgba(255,255,255,.66));
}

.card-label {
  display: flex; align-items: center; justify-content: space-between;
  font-size: 13px; font-weight: 500; color: var(--ink-3); gap: 8px;
}
.pill {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 12.5px; font-weight: 500; padding: 2px 9px; border-radius: 999px; white-space: nowrap;
}
.pill i { width: 5px; height: 5px; border-radius: 50%; background: currentColor; }
.pill.good { color: var(--good); background: var(--good-soft); }
.pill.warn { color: var(--warn); background: var(--warn-soft); }
.pill.bad  { color: var(--bad);  background: var(--bad-soft); }

.big {
  display: flex; align-items: baseline; gap: 8px; margin-top: 8px;
  font-family: var(--font-display); font-weight: 500; letter-spacing: -.02em;
  font-size: 40px; line-height: 1.05;
  background: linear-gradient(100deg, #1D1B17 0%, #0E6B63 45%, #17A394 70%, #1D1B17 100%);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; color: transparent;
}
.big small {
  font-family: var(--font-ui); font-size: 13.5px; font-weight: 400;
  -webkit-text-fill-color: var(--ink-3); color: var(--ink-3); letter-spacing: 0;
}
.big.sm {
  font-size: 23px; letter-spacing: -.01em; line-height: 1.2;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block;
}
.big.pos { background-image: linear-gradient(100deg, #2F7D5B, #17A394 55%, #2F7D5B); }
.big.neg { background-image: linear-gradient(100deg, #B5432F, #E0763A 55%, #B5432F); }

.meter { height: 5px; border-radius: 999px; background: rgba(34,30,24,.08); overflow: hidden; margin-top: 10px; }
.meter i { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--accent-2), var(--accent)); box-shadow: 0 0 12px rgba(23,163,148,.55); }
.tol { position: relative; height: 5px; border-radius: 999px; background: rgba(34,30,24,.08); margin-top: 10px; }
.tol i { position: absolute; top: 0; bottom: 0; left: 36%; width: 28%; border-radius: 999px; background: var(--warn-2); box-shadow: 0 0 12px rgba(232,162,59,.65); }
.tol em { position: absolute; top: -3px; left: 50%; width: 2px; height: 11px; margin-left: -1px; background: var(--ink); border-radius: 2px; }

.card-foot { margin-top: 9px; font-size: 13px; color: var(--ink-3); display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.card-foot b { color: var(--ink-2); font-weight: 600; }

div[data-testid="stVerticalBlockBorderWrapper"]:has(.chart-stage-marker) {
  background: linear-gradient(180deg, rgba(255,255,255,.86), rgba(255,255,255,.64)) !important;
  backdrop-filter: blur(20px) saturate(1.35) !important;
  border: 1px solid rgba(255,255,255,.8) !important;
  border-radius: 20px !important;
  padding: 14px 18px 12px !important;
  box-shadow: 0 0 0 1px rgba(34,30,24,.055), 0 1px 0 rgba(255,255,255,.95) inset, 0 20px 44px -26px rgba(12,70,64,.28) !important;
}
.eyebrow { font-size: 12.5px; font-weight: 600; color: var(--ink-3); }
.chart-headline {
  margin-top: 2px; font-family: var(--font-display); font-weight: 500;
  font-size: 20px; letter-spacing: -.01em; line-height: 1.28; color: var(--ink);
}

div[role="radiogroup"] {
  background: rgba(237, 233, 225, 0.78) !important;
  padding: 3px !important; border-radius: 999px !important;
  border: 1px solid var(--line) !important;
  display: inline-flex !important; gap: 3px !important;
}
div[role="radiogroup"] label {
  background: transparent !important; border: none !important;
  padding: 5px 13px !important; border-radius: 999px !important;
  margin: 0 !important; cursor: pointer !important;
}
div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child { display: none !important; }
div[role="radiogroup"] label p {
  font-size: 13px !important; font-weight: 500 !important; color: var(--ink-3) !important; white-space: nowrap !important;
}
div[role="radiogroup"] label:has(input:checked) {
  background: linear-gradient(180deg, #FFFFFF, #EAF6F2) !important;
  box-shadow: 0 0 0 1px rgba(14,107,99,.25), 0 6px 18px -6px rgba(23,163,148,.55) !important;
}
div[role="radiogroup"] label:has(input:checked) p {
  color: var(--accent) !important; font-weight: 600 !important;
}

.rank-list { display: flex; flex-direction: column; justify-content: center; gap: 14px; padding: 18px 8px 14px; min-height: 335px; }
.rk { display: grid; grid-template-columns: 230px 1fr; align-items: center; gap: 16px; }
.rk-name { font-size: 14px; font-weight: 600; color: var(--ink-2); line-height: 1.25; }
.rk-name small { display: block; font-size: 12px; font-weight: 400; color: var(--ink-3); margin-top: 2px; }
.rk-track { display: flex; align-items: center; gap: 12px; }
.rk-bar {
  height: 22px; border-radius: 6px; width: var(--w, 40%);
  background: linear-gradient(90deg, rgba(14,107,99,.75), rgba(23,163,148,.45));
  box-shadow: 0 8px 18px -10px rgba(14,107,99,.5);
}
.rk.top .rk-bar {
  background: linear-gradient(90deg, #0E6B63, #17A394 60%, #5FD8C6);
  box-shadow: 0 0 0 1px rgba(23,163,148,.25), 0 0 22px rgba(23,163,148,.5), 0 10px 22px -8px rgba(23,163,148,.55);
}
.rk-num { font-size: 14px; font-weight: 600; color: var(--ink); white-space: nowrap; }
.rk.top .rk-num { color: var(--accent); }
.rk-num em { font-style: normal; font-size: 12.5px; color: var(--ink-3); font-weight: 400; margin-left: 8px; }

.narrative-card {
  margin-top: 14px;
  display: grid; grid-template-columns: auto .92fr 1.15fr; gap: 22px; align-items: center;
  padding: 16px 22px; border-radius: 20px;
  background:
    radial-gradient(540px 210px at 0% 0%, rgba(232,162,59,.28), transparent 70%),
    radial-gradient(540px 230px at 100% 100%, rgba(23,163,148,.20), transparent 70%),
    linear-gradient(180deg, rgba(255,255,255,.88), rgba(255,255,255,.68));
  border: 1px solid rgba(255,255,255,.82);
  box-shadow: 0 0 0 1px rgba(232,162,59,.24), 0 1px 0 rgba(255,255,255,.95) inset, 0 0 42px -10px rgba(232,162,59,.34), 0 22px 44px -26px rgba(12,70,64,.28);
}
.persona { position: relative; width: 108px; display: grid; justify-items: center; gap: 6px; }
.avatar-svg { width: 88px; height: 88px; filter: drop-shadow(0 8px 16px rgba(14,107,99,.42)); }
.nametag { display: flex; flex-direction: column; align-items: center; line-height: 1.15; text-align: center; }
.nametag b { font-family: var(--font-display); font-weight: 500; font-size: 16px; color: var(--ink); }
.nametag span { font-size: 12px; color: var(--ink-3); margin-top: 2px; }
.glyph {
  position: absolute; z-index: 2; font-size: 12px; font-weight: 600; line-height: 1;
  color: var(--accent); background: rgba(255,255,255,.9);
  border: 1px solid rgba(14,107,99,.28); border-radius: 7px; padding: 3px 5px;
  box-shadow: 0 0 12px rgba(23,163,148,.4);
}
.glyph.g1 { top: 0; left: -2px; }
.glyph.g2 { top: 24px; right: -4px; color: var(--warn); border-color: rgba(183,121,31,.35); }
.glyph.g3 { bottom: 36px; left: -4px; }

.narr-tag {
  display: inline-flex; align-items: center; gap: 8px; margin-bottom: 6px;
  font-size: 12.5px; font-weight: 600; color: var(--warn);
}
.narr-tag::before { content: ""; width: 16px; height: 1.5px; background: var(--warn-2); }
.headline {
  font-family: var(--font-display); font-weight: 500; font-size: 25px;
  line-height: 1.2; letter-spacing: -.01em; color: var(--ink);
}
.headline em {
  font-style: normal; font-weight: 600;
  background: linear-gradient(90deg, #0E6B63, #17A394, #D98A2B);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; color: transparent;
}
.narr-body {
  font-size: 13.8px; line-height: 1.62; color: var(--ink-2);
  border-left: 1px solid var(--line-strong); padding-left: 20px;
}
.narr-body b { font-weight: 600; color: var(--ink); }
.act-pills { display: flex; gap: 8px; margin-top: 9px; flex-wrap: wrap; }
.act-pills span {
  font-size: 12.5px; font-weight: 500; padding: 3px 10px; border-radius: 999px;
  background: var(--accent-soft); color: var(--accent); border: 1px solid var(--accent-ring);
}
</style>
<div class="aurora-bg" aria-hidden="true"><i></i><i></i><i></i></div>
"""
st.markdown(PROTOTYPE_CSS, unsafe_allow_html=True)

NARA_AVATAR_SVG = """
<div class="persona">
  <span class="glyph g1">&Sigma;</span>
  <span class="glyph g2">&pi;</span>
  <span class="glyph g3">&Delta;</span>
  <svg class="avatar-svg" viewBox="0 0 120 120" role="img" aria-label="Avatar Nara, penasihat strategi">
    <defs>
      <radialGradient id="avBg" cx="35%" cy="25%" r="90%">
        <stop offset="0" stop-color="#1B7C71"/><stop offset=".55" stop-color="#0B4540"/><stop offset="1" stop-color="#072725"/>
      </radialGradient>
      <linearGradient id="avCoat" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#1E5A53"/><stop offset="1" stop-color="#0A2F2C"/>
      </linearGradient>
      <linearGradient id="avSkin" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#F5D0AC"/><stop offset="1" stop-color="#DDA27A"/>
      </linearGradient>
      <linearGradient id="avRing" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#7FE3D3"/><stop offset=".55" stop-color="#17A394"/><stop offset="1" stop-color="#E8A23B"/>
      </linearGradient>
      <clipPath id="avClip"><circle cx="60" cy="60" r="55"/></clipPath>
    </defs>
    <circle cx="60" cy="60" r="56" fill="url(#avBg)"/>
    <g clip-path="url(#avClip)">
      <circle cx="60" cy="52" r="34" fill="rgba(127,227,211,.16)"/>
      <path d="M10 124 C12 96 32 85 60 85 C88 85 108 96 110 124 Z" fill="url(#avCoat)"/>
      <path d="M47 86 L60 110 L73 86 Z" fill="#F5F2EC"/>
      <path d="M60 93 L51 88 L51 98 Z M60 93 L69 88 L69 98 Z" fill="#E8A23B"/>
      <circle cx="60" cy="93" r="2.8" fill="#F6C77A"/>
      <path d="M51 72 L51 87 Q60 94 69 87 L69 72 Z" fill="#D69A72"/>
      <ellipse cx="60" cy="58" rx="21" ry="24" fill="url(#avSkin)"/>
      <path d="M38 58 C33 37 46 25 62 26 C80 27 89 42 82 58 C80 50 76 44 70 42 C62 48 48 46 38 58 Z" fill="#2B2420"/>
      <path d="M45 52 Q51.5 49 57 52 M63 52 Q68.5 49 75 52" stroke="#2B2420" stroke-width="1.7" fill="none" stroke-linecap="round"/>
      <circle cx="52" cy="60" r="1.6" fill="#1D1B17"/><circle cx="68" cy="60" r="1.6" fill="#1D1B17"/>
      <g fill="rgba(200,240,235,.22)" stroke="#1D1B17" stroke-width="2">
        <circle cx="52" cy="60" r="7.8"/><circle cx="68" cy="60" r="7.8"/>
      </g>
      <path d="M59.8 59 Q60 57.4 60.2 59" stroke="#1D1B17" stroke-width="1.8" fill="none"/>
      <path d="M53.5 75 Q60 79.5 66.5 75" stroke="#A5593F" stroke-width="1.7" fill="none" stroke-linecap="round"/>
    </g>
    <circle cx="60" cy="60" r="55" fill="none" stroke="url(#avRing)" stroke-width="2.2"/>
  </svg>
  <div class="nametag"><b>Nara</b><span>Penasihat strategi</span></div>
</div>
"""

LEVER_ICONS = [
    '<svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 5.5h9v7h-9z"/><path d="M11.5 8h3.2l2.3 2.5v2h-5.5z"/><circle cx="6" cy="14.5" r="1.6"/><circle cx="14" cy="14.5" r="1.6"/></svg>',
    '<svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4.5h14v9H9.5L6 16.5v-3H3z"/><path d="M6.5 8h7M6.5 10.5h4"/></svg>',
    '<svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3h7l7 7-7 7-7-7z"/><circle cx="7" cy="7" r="1.2"/></svg>',
]


@st.cache_resource
def get_cached_pipeline(df_sig: int, df: pd.DataFrame, target_col: str, features: list[str], schema_info: dict, audit_info: dict):
    return train_fluent_ml_pipeline(df, target_col, features, schema_info, audit_info)


top_l, top_r = st.columns([3.1, 1.1], vertical_alignment="center")
with top_l:
    st.markdown(
        """
        <div class="topbar-wrap" style="border:none; margin-bottom:0; padding-bottom:0;">
          <div class="brand">
            <div class="logo-box" aria-hidden="true">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 10 L5 6 L8 8.5 L12 3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
            <span class="brand-name">CSIP Studio</span>
            <span class="badge-status"><i></i>Mesin Lokal Aktif</span>
            <span class="brand-sub">Ilmuwan data otomatis dan simulator keputusan</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div style="height:1px; background:linear-gradient(90deg, transparent, rgba(23,163,148,.5) 30%, rgba(232,162,59,.5) 70%, transparent); margin: 6px 0 14px 0;"></div>', unsafe_allow_html=True)

col_deck, col_stage = st.columns([1.05, 2.22], gap="medium")

with col_deck:
    with st.container(border=True):
        st.markdown('<span class="teal-source-marker"></span>', unsafe_allow_html=True)

        uploaded_csv = st.file_uploader(
            "Tarik berkas CSV ke sini, atau pilih dari komputer",
            type=["csv"],
        )

        preset_choice = st.selectbox(
            "Atau pakai dataset bawaan",
            options=[
                "Kasus 1: Toko Online & Kepuasan Pembeli (Data Olist)",
                "Kasus 2: Risiko Kesehatan & Gaya Hidup (Data Medis)",
                "Kasus 3: Kualitas Produk & Komposisi Bahan (Data Mutu)",
            ],
        )

        if uploaded_csv is not None:
            raw_df = pd.read_csv(uploaded_csv)
            dataset_title = f"Berkas: {uploaded_csv.name}"
        else:
            raw_df = get_builtin_dataset(preset_choice)
            dataset_title = preset_choice

        active_df, schema_info, auto_target, audit_info = build_fluent_schema(raw_df)
        human_cols = list(schema_info.keys())

        if len(human_cols) < 2:
            st.error("Berkas CSV membutuhkan minimal 2 kolom angka untuk dibedah.")
            st.stop()

        st.markdown(
            f"""
            <div class="step-head-teal" style="margin-top:4px;">
              <span class="step-no-teal">1</span>
              <span class="step-title-teal">Sumber data dan fokus</span>
              <span class="step-hint-teal">{len(active_df):,} baris terbaca</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        target_idx = human_cols.index(auto_target) if auto_target in human_cols else len(human_cols) - 1
        target_col = st.selectbox(
            "Yang ingin dioptimalkan",
            options=human_cols,
            index=target_idx,
            key=f"target_select_{dataset_title}",
        )

        t_meta = schema_info[target_col]
        st.markdown(
            f"""
            <div class="explain-teal">
              <span class="explain-tag-teal">Artinya begini</span>
              <p><b>{target_col}</b> adalah {t_meta['description'].lower()}. {t_meta['banner_note']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    candidate_features = [c for c in human_cols if c != target_col]
    df_signature = hash((dataset_title, target_col, tuple(candidate_features), len(active_df)))
    pipeline = get_cached_pipeline(df_signature, active_df, target_col, candidate_features, schema_info, audit_info)

    with st.container(border=True):
        st.markdown('<span class="warm-levers-marker"></span>', unsafe_allow_html=True)

        head_c1, head_c2 = st.columns([2.2, 1.0], vertical_alignment="center")
        with head_c1:
            st.markdown(
                """
                <div class="step-head-light">
                  <span class="step-no-light">2</span>
                  <span class="step-title-light">Tuas simulasi</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with head_c2:
            reset_clicked = st.button("Setel ulang", use_container_width=True)

        custom_inputs = {}
        top_3_rows = pipeline["stats_df"].iloc[:3]

        for idx, row_meta in top_3_rows.iterrows():
            f_name = row_meta["Fitur"]
            f_min = float(row_meta["Min"])
            f_max = float(row_meta["Max"])
            f_med = float(row_meta["Median"])
            f_unit = row_meta["Unit"]
            if f_max <= f_min:
                f_max = f_min + 1.0
            step_val = (f_max - f_min) / 100.0

            s_key = f"slider_{dataset_title}_{target_col}_{f_name}"
            if reset_clicked or s_key not in st.session_state:
                st.session_state[s_key] = f_med

            cur_v = float(st.session_state[s_key])
            lv_cls = f"lv-{min(idx + 1, 3)}"
            ico_svg = LEVER_ICONS[min(idx, 2)]

            st.markdown(
                f"""
                <div class="lv-card-head {lv_cls}">
                  <span class="lv-ico">{ico_svg}</span>
                  <div class="lv-title">
                    <span class="lv-name">{f_name}</span>
                    <span class="lv-meta">
                      <span class="lv-rank">#{idx+1}</span>
                      <span class="lv-weight">Bobot {row_meta['Pengaruh_Persen']:.0f}%</span>
                    </span>
                  </div>
                  <div class="lv-val"><b>{fmt_num(cur_v)}</b><small>{f_unit}</small></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            val = st.slider(
                f_name,
                min_value=f_min,
                max_value=f_max,
                step=step_val,
                key=s_key,
                label_visibility="collapsed",
            )
            custom_inputs[f_name] = val

            st.markdown(
                f'<div class="lv-note {lv_cls}">{row_meta["Kalimat_Alami"]}</div>',
                unsafe_allow_html=True,
            )


sim = simulate_and_narrate(pipeline, custom_inputs, target_col, schema_info)
top1_row = pipeline["stats_df"].iloc[0]
top2_row = pipeline["stats_df"].iloc[1] if len(pipeline["stats_df"]) > 1 else top1_row
t_unit = schema_info[target_col]["unit"]

with top_r:
    with st.popover("Catatan Kurator & 11 Unit SKKNI", use_container_width=True):
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
        with tab3:
            aud = pipeline["audit_summary"]
            audit_table = pd.DataFrame([
                {"Tahapan SKKNI": "UK-03 & UK-04 (Telaah & Validasi Baris Awal)", "Hasil Eksekusi": f"{aud['raw_rows']:,} baris x {aud['raw_cols']} kolom"},
                {"Tahapan SKKNI": "UK-06 (Imputasi Nilai Kosong & Hapus Duplikat)", "Hasil Eksekusi": f"{aud['missing_fixed']} sel kosong ditambal, {aud['duplicates_removed']} duplikat dihapus"},
                {"Tahapan SKKNI": "UK-07 (Konstruksi & Encoding Kategori)", "Hasil Eksekusi": ", ".join(aud["encoded_cats"])},
                {"Tahapan SKKNI": "UK-05 (Filter Kolom Kolinear >94%)", "Hasil Eksekusi": ", ".join(aud["dropped_collinear"])},
            ])
            st.dataframe(audit_table, use_container_width=True, hide_index=True)

with col_stage:
    if abs(sim["diff_pct"]) < 1.0:
        tone_cls = "warn"
        pill_label = "Setara standar"
        delta_cls = "pos"
        tint_rgba = "rgba(232,162,59,.26)"
    elif sim["diff_val"] > 0:
        tone_cls = "good"
        pill_label = "Di atas standar"
        delta_cls = "pos"
        tint_rgba = "rgba(47,125,91,.28)"
    else:
        tone_cls = "bad" if sim["diff_pct"] < -8.0 else "warn"
        pill_label = "Perlu perhatian" if tone_cls == "bad" else "Di bawah standar"
        delta_cls = "neg"
        tint_rgba = "rgba(181,67,47,.26)" if tone_cls == "bad" else "rgba(232,162,59,.28)"

    dir_short_text = "Makin tinggi, hasil makin turun" if top1_row["Pearson_r"] < -0.05 else (
        "Makin tinggi, hasil ikut naik" if top1_row["Pearson_r"] > 0.05 else "Menentukan titik keseimbangan"
    )

    bento_html = f"""
    <div class="bento">
      <article class="bento-card c1" style="--tint:{tint_rgba};">
        <div class="card-label">{target_col} simulasi <span class="pill {tone_cls}"><i></i><span>{pill_label}</span></span></div>
        <div class="big"><span>{fmt_num(sim['pred_val'])}</span> <small>{t_unit if t_unit else 'satuan'}</small></div>
        <div class="card-foot">Kondisi standar (median) <b>{fmt_num(sim['base_val'], t_unit)}</b></div>
      </article>

      <article class="bento-card c2">
        <div class="card-label">Faktor penentu terkuat</div>
        <div class="big sm" title="{top1_row['Fitur']}">{top1_row['Fitur']}</div>
        <div class="meter"><i style="width:{min(100.0, top1_row['Pengaruh_Persen']):.0f}%"></i></div>
        <div class="card-foot"><b>{top1_row['Pengaruh_Persen']:.0f}% kendali</b> <span>{dir_short_text}</span></div>
      </article>

      <article class="bento-card c3" style="--tint:{tint_rgba};">
        <div class="card-label">Selisih dari standar</div>
        <div class="big {delta_cls}"><span>{sim['diff_val']:+,.1f}</span> <small>{t_unit} ({sim['diff_pct']:+.1f}%)</small></div>
        <div class="tol" aria-hidden="true"><i></i><em></em></div>
        <div class="card-foot">Evaluasi model: <b>{pipeline['model_quality_label']}</b></div>
      </article>
    </div>
    """
    st.markdown(bento_html, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<span class="chart-stage-marker"></span>', unsafe_allow_html=True)
        ch_l, ch_r = st.columns([1.15, 1.55], vertical_alignment="center")

        with ch_r:
            active_lens = st.radio(
                "Lensa tampilan",
                options=[
                    "1. Kurva Simulasi dan Titik Kritis",
                    "2. Peringkat Faktor Penentu",
                    "3. Sebaran Kelompok Data",
                ],
                horizontal=True,
                label_visibility="collapsed",
            )

        if active_lens == "1. Kurva Simulasi dan Titik Kritis":
            dynamic_chart_title = f"Perubahan {target_col.lower()} paling tajam terjadi di sekitar {top1_row['Fitur'].lower()} {fmt_num(sim['tipping_x'], top1_row['Unit'])}"
        elif active_lens == "2. Peringkat Faktor Penentu":
            dynamic_chart_title = f"{top1_row['Fitur']} memegang {top1_row['Pengaruh_Persen']:.0f}% kendali atas nasib {target_col.lower()}"
        else:
            dynamic_chart_title = f"Tiga kelompok {target_col.lower()} yang terbentuk nyata dari {pipeline['n_rows']:,} baris data"

        with ch_l:
            st.markdown(
                f"""
                <div>
                  <div class="eyebrow">Lensa tampilan • {dataset_title}</div>
                  <div class="chart-headline">{dynamic_chart_title}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if active_lens == "1. Kurva Simulasi dan Titik Kritis":
            fig = build_impact_curve_chart(pipeline, sim, target_col, schema_info)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        elif active_lens == "2. Peringkat Faktor Penentu":
            st.markdown(build_ranking_html(pipeline), unsafe_allow_html=True)
        else:
            fig = build_cluster_map_chart(pipeline, sim, target_col, custom_inputs, schema_info)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    headline_words = sim["headline"].split(" ")
    if len(headline_words) > 4:
        hl_main = " ".join(headline_words[:-3])
        hl_em = " ".join(headline_words[-3:])
        formatted_headline = f"{hl_main} <em>{hl_em}</em>"
    else:
        formatted_headline = f"<em>{sim['headline']}</em>"

    action_pill_1 = f"Jaga {top1_row['Fitur'].lower()} di sekitar {fmt_num(sim['tipping_x'], top1_row['Unit'])}"
    action_pill_2 = f"Pantau faktor #{2}: {top2_row['Fitur'].lower()} ({top2_row['Pengaruh_Persen']:.0f}%)"

    st.markdown(
        f"""
        <article class="narrative-card">
          {NARA_AVATAR_SVG}
          <div>
            <div class="narr-tag">Kesimpulan untuk posisi tuas saat ini</div>
            <h3 class="headline">{formatted_headline}</h3>
          </div>
          <div class="narr-body">
            {sim['full_narrative']}
            <div class="act-pills">
              <span>{action_pill_1}</span>
              <span>{action_pill_2}</span>
            </div>
          </div>
        </article>
        """,
        unsafe_allow_html=True,
    )
