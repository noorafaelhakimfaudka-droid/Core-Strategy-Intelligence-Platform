# CSIP Installation & Environment Setup Guide
## Hardware Requirements, Python Environment, Dependency Locking & Containerization

**Document Version:** 1.0.0-Definitive  
**Target Release:** CSIP Definitive Consolidated Release  
**Tested Operating Systems:** Windows 10/11 x64, Ubuntu 22.04 LTS, macOS Sonoma (Apple Silicon / Intel)  

---

### 1. HARDWARE & SYSTEM REQUIREMENTS

- **Processor:** Quad-Core x86_64 or ARM64 processor (Intel Core i5+, AMD Ryzen 5+, Apple M1+).
- **RAM:** Minimum 8 GB RAM (Optimized for standard laptop execution; peak memory usage < 2.5 GB).
- **Disk Space:** Minimum 1.5 GB free disk space (to accommodate raw CSVs, interim parquets, models, and test caches).
- **Python Version:** Python 3.10, 3.11, 3.12, 3.13, or 3.14.

---

### 2. LOCAL INSTALLATION STEP-BY-STEP

#### Step 1: Clone or Unpack the Release Archive
```bash
unzip CSIP_DEFINITIVE_RELEASE.zip -d csip_platform
cd csip_platform
```

#### Step 2: Create and Activate an Isolated Virtual Environment
```bash
# On Linux / macOS
python -m venv .venv
source .venv/bin/activate

# On Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Step 3: Install Core Dependencies via Locked Requirements
```bash
# Core execution dependencies (Fast install)
pip install -r requirements.txt

# Or install from full pinned lockfile for 100% bitwise parity
pip install -r requirements.lock
```

#### Step 4: Verify Installation with the Master Quality Gates
```bash
python tools/run_final_validation.py --quick
```
*Expected output: 19/19 PASSED in under 15 seconds.*

#### Step 5: Launch the Interactive Analytical Dashboard
```bash
streamlit run app/streamlit_app.py
```
Open your browser to `http://localhost:8501` to access the platform.

---

### 3. DOCKER CONTAINER INSTALLATION (OPTIONAL)

For completely isolated, reproducible containerized execution:

```bash
# Build the Docker image
docker build -t csip-platform:1.0.0 .

# Run the container exposing port 8501
docker run -p 8501:8501 csip-platform:1.0.0
```
Access the application at `http://localhost:8501`.

