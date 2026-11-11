# CSIP Security, Governance & Reliability Policy
## Secrets Management, Safe Deserialization, Data Provenance & Local Execution Boundaries

**Document Version:** 1.0.0-Definitive  
**Standard Compliance:** ISO/IEC 27001 Alignment & Data Science Governance  

---

### 1. SECRETS MANAGEMENT & CODEBASE HYGIENE

- **Zero Hardcoded Credentials:** An automated regex and AST scanner scanned all 384 repository files. No private API keys, database connection strings with passwords, cloud service account JSONs, or private certificates exist in the codebase.
- **Environment Isolation:** Local execution uses environment variables or local configuration files (`config/`).
- **No External Data Transmission:** CSIP operates 100% locally. Raw customer transaction data, customer locations, and model predictions are processed on the local CPU without transmitting telemetry or inputs to external cloud endpoints.

---

### 2. SAFE MODEL DESERIALIZATION & ARTIFACT INTEGRITY

- **Cryptographic Model Verification:** All 8 model binaries in `artifacts/models/` (`.joblib` and `.pt`) are tracked in `artifacts/metadata/MODEL_RESULTS_REGISTRY.csv` with SHA-256 cryptographic hashes.
- **Restricted Load Paths:** `tools/validate_model_artifact_registry.py` enforces that model deserialization occurs strictly from pre-verified, local repository paths.
- **PyTorch Safe Checkpoints:** Deep learning checkpoints store only state dictionaries (`model.state_dict()`) rather than arbitrary executable Python objects, mitigating Python pickle injection risks.

---

### 3. INPUT DATA VALIDATION & PATH SANITIZATION

- **Ad-Hoc File Upload Sanitization:** The Universal CSV X-Ray engine (`src/csip/engine/universal_csv_xray.py`) enforces strict filename sanitization, rejects path traversal sequences (`../`, `..\`), and caps input file parsing to 50 MB to prevent local memory exhaustion.
- **Contract Schema Validation:** Incoming datasets are evaluated via `src/csip/data/contracts.py` to prevent malformed or malicious data structures from propagating into model inference pipelines.

---

### 4. DATA RETENTION & LINEAGE PROVENANCE

- **Immutable Raw Ingestion:** Data in `data/raw/` is treated as immutable read-only source material with public provenance (Olist Public Dataset, Kaggle).
- **Automated Lineage Manifest:** Complete transformation provenance from raw CSVs to models is stored in `artifacts/metadata/DATA_LINEAGE.json`, supporting end-to-end enterprise reproducibility audits.

