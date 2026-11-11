# CSIP Evidence Handbook for LSP TRI / SKKNI Assessors
## Practical Demonstration Guide, Interactive Examination Script & Evidence Verification

**Standard:** SKKNI No. 299 Tahun 2020  
**Scheme:** LSP TRI — Sertifikasi Ilmuwan Data (*Data Scientist*), KKNI Level 7  
**Candidate Target:** Portofolio & Uji Kompetensi Data Scientist  

---

### 1. HOW ASSESSORS CAN VERIFY EVIDENCE IN 3 STEPS

Assessors can independently verify the authenticity and defensibility of CSIP within 5 minutes:

#### Step 1: Real-Time Hash Manifest Verification
```bash
python scripts/generate_sha256sums.py --verify
```
*Expected: "Verified 374+ files. ALL FILES VERIFIED 100% BITWISE IDENTICAL!"*

#### Step 2: Automated Model Artifact & Deserialization Check
```bash
python tools/validate_model_artifact_registry.py
```
*Expected: 8/8 physical models deserialized and validated with matching hashes.*

#### Step 3: Run Full Automated Acceptance Test Suite
```bash
pytest tests/ -q
```
*Expected: 199+ passed, 0 failed in ~65 seconds.*

---

### 2. CANDIDATE DEMONSTRATION SCRIPT (ORAL & PRACTICAL EXAMINATION)

For KUKs marked `CANDIDATE_DEMONSTRATION_REQUIRED`, the candidate should present the following live platform journeys:

#### Demonstration Journey 1: Business Framing & Objective Alignment (Unit 1 & Unit 2)
- **Action:** Open Chapter 1 (`1_Executive_Overview.py`) and explain the trade-off between freight cost ratio and delivery delay expectation.
- **Evidence Reference:** Point to `docs/methodology/BUSINESS_UNDERSTANDING.md` and demonstrate how the business problem maps directly to the classification target (`negative_review_flag`).

#### Demonstration Journey 2: Data Cleansing & Contract Adherence (Unit 4 & Unit 6)
- **Action:** Open Chapter 2 (`2_Data_Observatory.py`) and explain the deduplication of 1,000,163 GPS coordinates down to 19,015 clean centroids.
- **Evidence Reference:** Demonstrate `src/csip/data/contracts.py` running in terminal and catching invalid inputs.

#### Demonstration Journey 3: Model Calibration & Subgroup Robustness (Unit 9 & Unit 10)
- **Action:** Open Chapter 5 (`5_Predictive_Intelligence.py`) and explain why raw LightGBM probabilities require Platt Sigmoid calibration to achieve a Brier score of `0.0762`.
- **Evidence Reference:** Show the subgroup slice table demonstrating consistent performance across SP, RJ, MG, RS, and PR.

#### Demonstration Journey 4: Counterfactual Simulation & Policy Decision (Unit 8 & Unit 11)
- **Action:** Open Chapter 7 (`7_Alternative_World_Simulator.py`) and apply a 2-day delivery speedup lever. Show how the 500-step Monte Carlo Markov Chain predicts a reduction in negative reviews from 15.4% to 11.2%.
- **Evidence Reference:** Explain the asymptotic stability of the Ridge VAR transition matrix ($\rho(A) = 0.8412 < 1.000$).

