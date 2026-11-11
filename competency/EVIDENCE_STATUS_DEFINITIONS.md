# CSIP COMPETENCY EVIDENCE STATUS TAXONOMY & AUDIT DEFINITIONS
## Normative Evidence Governance Standard for LSP TRI / SKKNI Competency Certification
### Scheme: SKM/2905/LSP-TRI/VII/2025 | Standard: SKKNI No. 299 Tahun 2020 | Level: KKNI 7 (Data Scientist)

---

### 1. Purpose and Governing Principles

In professional Data Science certification under **SKKNI Nomor 299 Tahun 2020 (KKNI Level 7)**, evidence must be audited with the mindset of an independent regulatory inspector. Merely having a file on disk or asserting "100% VERIFIED" without substantive verification violates professional ethics and SKKNI audit standards.

To eliminate cosmetic compliance and ensure absolute transparency, CSIP Version 15 institutes this **Evidence Status Taxonomy**. Every KUK (Kriteria Unjuk Kerja) must be assigned exactly one of the six mutually exclusive statuses based on verifiable empirical criteria.

---

### 2. Six-Tier Evidence Status Definitions

```
                     ┌───────────────────────────────────────────────┐
                     │          TOTAL CANONICAL KUKs: 63             │
                     └───────────────────────┬───────────────────────┘
                                             │
      ┌──────────────────┬───────────────────┼───────────────────┬───────────────────┐
      ▼                  ▼                   ▼                   ▼                   ▼
  VERIFIED         ARTIFACT_ONLY       CANDIDATE_DEMO      EXTERNAL_CONFIRM     MISSING / PARTIAL
   (35 KUK)           (12 KUK)            (13 KUK)              (3 KUK)              (0 KUK)
  Code + Test       Static File         Live Defense         Governance         No Evidence
```

#### 1. `VERIFIED` (Count: 35 KUKs / 55.56%)
- **Definition**: Substantive evidence physically inspected, executed, and successfully verified.
- **Mandatory Criteria**:
  1. A production Python module exists in `src/csip/` or dedicated pipeline script.
  2. An automated unit, integration, or regression test in `tests/` explicitly verifies the criterion.
  3. The test has actually run and passed in the local execution environment (verified by automated pytest runner).
  4. The generated data or model artifact physically exists on disk and matches its registered SHA-256 hash.
- **Examples**: Data cleaning functions (`UK-06 KUK 1.1`), feature engineering pipelines (`UK-07 KUK 1.1`), model training (`UK-09 KUK 1.1`), probability calibration (`UK-10 KUK 1.3`).

#### 2. `ARTIFACT_ONLY` (Count: 12 KUKs / 19.05%)
- **Definition**: A tangible file exists on disk (e.g. data dictionary, schema specification, exploratory report, architecture diagram), but automated functional test execution is not applicable.
- **Mandatory Criteria**:
  1. A concrete document, JSON schema, or markdown report exists on disk at the declared relative path.
  2. The file is non-empty, syntactically valid, and carries a verifiable SHA-256 hash.
  3. While the artifact documents the required knowledge, operational competence must be confirmed by assessor inspection of the document contents.
- **Examples**: Relational data dictionary (`UK-03 KUK 2.1`), system architecture documentation (`UK-02 KUK 2.1`), data profile report (`UK-03 KUK 1.1`).

#### 3. `CANDIDATE_DEMONSTRATION_REQUIRED` (Count: 13 KUKs / 20.63%)
- **Definition**: Practical task or analytical reasoning that requires direct interactive demonstration or oral defense by the candidate before the SKKNI assessor.
- **Mandatory Criteria**:
  1. Supporting code or notebook artifacts exist to serve as the demonstrator basis.
  2. The candidate must walk through the problem formulation, trade-offs, and analytical decisions during the examination.
  3. Assessor verifies competency through live demonstration, code walkthrough, and oral question probing.
- **Examples**: Business problem formulation (`UK-01 KUK 1.1–1.4`), technical objective translation (`UK-02 KUK 1.1–1.2`), modeling scenario justification (`UK-11 KUK 1.1`).

#### 4. `EXTERNAL_CONFIRMATION_REQUIRED` (Count: 3 KUKs / 4.76%)
- **Definition**: The criterion explicitly requires third-party or client sign-off (e.g. formal customer approval of business objectives, risk acceptance, or cost-benefit budgets).
- **Mandatory Criteria & Ethical Boundary**:
  1. In secondary observational research (open-source e-commerce dataset), live executive signatures **CANNOT** be fabricated. Fabricating client emails or signatures is strictly prohibited.
  2. Enterprise governance review templates, formal project charters, risk mitigation matrices, and ROI calculations are provided in `competency/external_approvals/STAKEHOLDER_APPROVAL_DEFENSE_PACKET.md`.
  3. The status is honestly disclosed as requiring external confirmation, accompanied by a structured defense workflow for the candidate.
- **Affected KUKs**: `UK-01-KUK-2.2`, `UK-01-KUK-3.3`, `UK-01-KUK-4.3`.

#### 5. `PARTIALLY_VERIFIED` (Count: 0 KUKs / 0.00%)
- **Definition**: Evidence supports part of the performance criterion but does not satisfy the full requirement.
- **Rule**: Any KUK previously marked as partially verified must be explicitly categorized into its true substantive status (e.g., `EXTERNAL_CONFIRMATION_REQUIRED` or `CANDIDATE_DEMONSTRATION_REQUIRED`).

#### 6. `MISSING` (Count: 0 KUKs / 0.00%)
- **Definition**: Required evidence or artifact is completely absent from the repository.
- **Current Status**: All 63 KUKs have concrete, physically verifiable evidence artifacts linked.

---

### 3. Canonical Summary Table

| Evidence Status Category | KUK Count | Percentage of Scope | Verification Modality | Audit Standard Compliance |
| :--- | :---: | :---: | :--- | :--- |
| **VERIFIED** | **35** | **55.56%** | Automated Pytest + Production Code + Checkpoint | 100% Tested & Disk-Verified |
| **ARTIFACT_ONLY** | **12** | **19.05%** | Document & Specification Inspection | File Exists & SHA-256 Validated |
| **CANDIDATE_DEMONSTRATION_REQUIRED** | **13** | **20.63%** | Live Terminal/Notebook Walkthrough + Oral Defense | Practical Demonstration Ready |
| **EXTERNAL_CONFIRMATION_REQUIRED** | **3** | **4.76%** | Enterprise Governance Packet + Review Protocol | Honest Secondary Data Disclosure |
| **PARTIALLY_VERIFIED** | **0** | **0.00%** | N/A | No ambiguous classifications |
| **MISSING** | **0** | **0.00%** | N/A | Zero unmapped criteria |
| **TOTAL CANONICAL KUK** | **63** | **100.00%** | Complete 11 Units, 27 Elements | SKKNI 299/2020 Standard Satisfied |

