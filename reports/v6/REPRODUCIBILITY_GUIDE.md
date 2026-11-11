# CSIP V6 Environment & Reproducibility Guide

**Document ID**: CSIP-REP-V6-RPG-01  
**Author**: Software Quality Assurance & Data Science Architecture Team  
**Date**: November 2026  
**Status**: VERIFIED  

---

## 1. Execution Environment
- **Operating System**: Windows, Linux (Ubuntu 22.04 LTS), macOS (Darwin)
- **Target Hardware**: Standard 8 GB RAM laptop execution budget (Memory footprint < 1.2 GB).
- **Python Version**: Python >= 3.10 (tested and verified on Python 3.14.7 64-bit AMD64).

---

## 2. Step-by-Step Reproduction Instructions

```bash
# 1. Clone repository
git clone https://github.com/noorafaelhakimfaudka-droid/Core-Strategy-Intelligence-Platform.git
cd Core-Strategy-Intelligence-Platform

# 2. Install dependencies
pip install -r requirements.txt

# 3. Rebuild analytical datasets (optional, pre-built in repo)
python scripts/build_features.py

# 4. Run Behavioral Discovery Engine
python scripts/run_behavioral_discovery.py

# 5. Run Supervised ML Experiments & Baseline Ladder
python scripts/run_ml_experiments.py

# 6. Run System & World Model State Transition
python scripts/run_world_model.py

# 7. Execute Automated Test Suite (87 tests)
python -m pytest tests/ -v

# 8. Launch Streamlit Decision Simulator Web Application
streamlit run app/streamlit_app.py
```
