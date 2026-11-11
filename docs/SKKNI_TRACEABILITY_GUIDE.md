# CSIP SKKNI Traceability Guide: Normative Competency Mapping
## Mapping of 11 Units, 27 Elements & 63 KUKs to Platform Code & Artifacts

**Standard:** SKKNI Nomor 299 Tahun 2020 (*Bidang Data Management dan Data Science*)  
**Scheme:** LSP TRI — Sertifikasi Ilmuwan Data (*Data Scientist*), KKNI Level 7 (`SKM/2905/LSP-TRI/VII/2025`)  
**Normative Prefix:** `J.62DMI00.xxx.1`  
**Master Traceability Ledger:** `competency/SKKNI_TRACEABILITY_MATRIX.csv`  

---

### 1. STATUTORY UNIT BREAKDOWN (11 UNITS, KKNI LEVEL 7)

```
===================================================================================================================
SKKNI NOMOR 299 TAHUN 2020 — 11 UNIT KOMPETENSI ILMUWAN DATA (DATA SCIENTIST)
===================================================================================================================
Unit Code         Unit Title (Indonesian Statutory Official Title)        Elements  KUKs  Primary Platform Evidence
----------------  ------------------------------------------------------  --------  ----  -------------------------
J.62DMI00.001.1   Menentukan Objektif Bisnis                                 4       9    docs/methodology/BUSINESS_UNDERSTANDING.md
J.62DMI00.002.1   Menentukan Tujuan Teknis Data Science                      2       5    docs/methodology/PREDICTION_CONTRACT.md
J.62DMI00.005.1   Menelaah Data                                              2       5    reports/data/DATA_PROFILING_REPORT.md
J.62DMI00.006.1   Memvalidasi Data                                           3       7    src/csip/data/contracts.py
J.62DMI00.007.1   Menentukan Objek Data                                      2       5    docs/methodology/DATA_DICTIONARY.md
J.62DMI00.008.1   Membersihkan Data                                          3       7    src/csip/cleaning/cleaner.py
J.62DMI00.009.1   Mengkonstruksi Data (Feature Engineering)                  2       5    src/csip/features/engineer.py
J.62DMI00.012.1   Membangun Skenario Model                                   2       5    docs/EXPERIMENT_DOCUMENTATION.md
J.62DMI00.013.1   Membangun Model                                            3       7    src/csip/models/trainer.py
J.62DMI00.014.1   Mengevaluasi Hasil Pemodelan                               2       5    reports/models/MODEL_ROBUSTNESS_AND_SLICE_ANALYSIS.md
J.62DMI00.015.1   Melakukan Proses Review Pemodelan                          3       6    reports/final/CSIP_DEFINITIVE_INDEPENDENT_AUDIT.md
-------------------------------------------------------------------------------------------------------------------
TOTALS            11 Unit Kompetensi                                        27      63    63 KUKs Fully Traceable
===================================================================================================================
```

---

### 2. EVIDENCE VERIFICATION STATUS TAXONOMY

In strict adherence to systematic governance integrity, every KUK in `competency/CANONICAL_EVIDENCE_REGISTRY.csv` is assigned one of four honest statuses:

1. **`VERIFIED` (35 KUKs — 55.6%):**
   - The competency requirement is fully implemented in active code, verified by automated pytest suites, and backed by verifiable physical artifacts with matching cryptographic hashes.
2. **`ARTIFACT_ONLY` (12 KUKs — 19.0%):**
   - Documentation, configuration templates, or static schemas exist demonstrating competency knowledge, but full execution requires domain contextualization.
3. **`CANDIDATE_DEMONSTRATION_REQUIRED` (13 KUKs — 20.6%):**
   - The platform provides the technical foundation, but the candidate must provide oral explanations, live interactive navigation, or situational problem solving during the LSP TRI assessor interview.
4. **`EXTERNAL_CONFIRMATION_REQUIRED` (3 KUKs — 4.8%):**
   - Unit 1 (`J.62DMI00.001.1`) KUK 2.2, 3.3, and 4.3 strictly require external commercial client formal confirmation on business assumptions, risk mitigations, and budget. CSIP provides candidate mock approval templates without fabricating corporate authorizations.

