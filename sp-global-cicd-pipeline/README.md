<div align="center">

<!-- HERO BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,50:16213e,100:0f3460&height=200&section=header&text=Zero-Touch%20CI/CD%20Pipeline&fontSize=40&fontColor=e94560&animation=fadeIn&fontAlignY=38&desc=S%26P%20Global%20%7C%20DevOps%20Internship%20Demo&descAlignY=55&descColor=a8b2d8" width="100%"/>

<br/>

<!-- BADGES ROW 1 -->
[![CI/CD Pipeline](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/sp-global-cicd-pipeline/ci-cd-pipeline.yml?branch=main&label=CI%2FCD%20Pipeline&logo=github-actions&logoColor=white&style=for-the-badge&color=238636)](https://github.com/YOUR_USERNAME/sp-global-cicd-pipeline/actions)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Coverage](https://img.shields.io/badge/Coverage-%3E80%25-success?style=for-the-badge&logo=pytest&logoColor=white)](./reports/htmlcov)

<!-- BADGES ROW 2 -->
[![Flake8](https://img.shields.io/badge/Linter-Flake8-blue?style=for-the-badge&logo=python&logoColor=white)](https://flake8.pycqa.org/)
[![Black](https://img.shields.io/badge/Formatter-Black-black?style=for-the-badge&logo=python&logoColor=white)](https://black.readthedocs.io/)
[![Bandit](https://img.shields.io/badge/Security-Bandit%20SAST-red?style=for-the-badge&logo=security&logoColor=white)](https://bandit.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br/>

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🏦  Financial Data Validator  ·  Automated Quality Pipeline    ║
║   S&P Global Market Intelligence  ·  DevOps Internship Demo      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

</div>

---

## 🎯 Project Overview

> **Built for:** S&P Global — Salesforce DevOps Internship Application  
> **Goal:** Demonstrate production-grade CI/CD thinking, Python automation, and automated quality gates

This repository implements a **Zero-Touch CI/CD Pipeline** that automatically validates, lints, security-scans, and tests a Financial Data Validator on every push — with zero human intervention required after the initial setup.

The `validator.py` module simulates a real-world **stock price data ingestion guard** — the kind used in production systems at financial data providers like S&P Global to ensure data integrity before prices enter downstream analytics pipelines.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ZERO-TOUCH CI/CD PIPELINE                             │
│                                                                          │
│  git push → GitHub → Workflow Trigger                                    │
│                            │                                             │
│                            ▼                                             │
│              ┌─────────────────────────┐                                │
│              │   JOB 1: Security Scan  │  ← Bandit SAST                 │
│              │   🔒 Outermost Gate     │                                 │
│              └────────────┬────────────┘                                │
│                           │  (needs: security-scan)                      │
│                           ▼                                              │
│              ┌─────────────────────────┐                                │
│              │  JOB 2: Code Quality    │  ← Black + isort + Flake8      │
│              │  🎨 Style & Lint Gate   │                                 │
│              └────────────┬────────────┘                                │
│                           │  (needs: code-quality)                       │
│                           ▼                                              │
│              ┌─────────────────────────────────────────────┐            │
│              │       JOB 3: Automated Test Suite           │            │
│              │  🧪  Matrix: Python 3.10 / 3.11 / 3.12     │            │
│              │  pytest + coverage enforcement (≥80%)       │            │
│              └────────────┬────────────────────────────────┘            │
│                           │  (needs: all jobs)                           │
│                           ▼                                              │
│              ┌─────────────────────────┐                                │
│              │  JOB 4: Pipeline Summary│  ← GitHub Step Summary         │
│              │  📋 Final Status Report │                                 │
│              └─────────────────────────┘                                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
sp-global-cicd-pipeline/
│
├── 📄 validator.py              # Core financial data validator module
├── 🧪 test_validator.py         # Comprehensive pytest test suite (4 groups)
├── 📦 requirements.txt          # Python dependencies
├── ⚙️  setup.cfg                 # Flake8, pytest, isort, mypy config
├── ⚙️  pyproject.toml            # Black formatter config
├── 🙈 .gitignore
│
└── 📁 .github/
    └── 📁 workflows/
        └── 🚀 ci-cd-pipeline.yml   # GitHub Actions workflow (4 jobs)
```

---

## ⚡ Pipeline Stages Explained

| Stage | Tool | Purpose | Blocks Pipeline? |
|-------|------|---------|-----------------|
| 🔒 Security Scan | **Bandit** | SAST — detects security vulnerabilities in Python code | On critical issues |
| 🎨 Formatting | **Black** | Ensures consistent, opinionated code style | ✅ Yes |
| 📂 Import Order | **isort** | Enforces alphabetically sorted imports | ✅ Yes |
| 🔎 Linting | **Flake8** | PEP 8 compliance + bug pattern detection | ✅ Yes |
| 🧪 Unit Tests | **pytest** | Runs 20+ tests across 4 test groups | ✅ Yes |
| 📊 Coverage | **pytest-cov** | Enforces ≥80% line coverage | ✅ Yes |
| 📋 Summary | GitHub Summary | Writes final status to workflow summary page | N/A |

---

## 🧪 Test Suite — What's Tested?

The test suite in `test_validator.py` is organized into **4 logical groups**:

```
📦 TestValidData          — Happy-path validation (6 tests)
   ├── Standard positive prices (SPGI market data)
   ├── Single price entry
   ├── Integer-only prices
   ├── Very large prices (BRK.A class instruments)
   ├── Penny stocks ($0.01)
   └── Large dataset performance (10,000 prices)

📦 TestInvalidData        — Rejection scenarios (10 tests)
   ├── Negative price → NegativePriceError
   ├── All-negative feed
   ├── Zero price (default behaviour)
   ├── Zero price (allow_zero=True override)
   ├── String values → InvalidPriceTypeError
   ├── None values
   ├── Boolean values
   ├── Mixed invalid types
   ├── Empty list → EmptyDatasetError
   └── Type errors take precedence over sign errors

📦 TestBatchValidation    — Multi-ticker processing (4 tests)
   ├── All-clean batch passes
   ├── Mixed batch separates pass/fail correctly
   ├── Empty batch → empty report
   └── Report count matches input count

📦 TestCustomThreshold    — Price floor enforcement (2 tests)
   ├── Prices above custom threshold pass
   └── Prices at/below threshold fail
```

**Total: 22 tests across 4 test groups**

---

## 🚀 Quick Start — Local Development

### Prerequisites
- Python 3.10+
- Git

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/sp-global-cicd-pipeline.git
cd sp-global-cicd-pipeline

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate          # Linux/Mac
.venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the validator demo
python validator.py
```

### Run Quality Checks Locally

```bash
# ── Format code (Black)
black .

# ── Sort imports
isort .

# ── Lint (Flake8)
flake8 . --max-line-length=100

# ── Security scan (Bandit)
bandit -r . --severity-level medium

# ── Run tests with coverage
pytest --cov=validator --cov-report=term-missing --cov-fail-under=80 -v

# ── Generate HTML coverage report
pytest --cov=validator --cov-report=html:reports/htmlcov
open reports/htmlcov/index.html    # Mac
start reports/htmlcov/index.html   # Windows
```

---

## 📊 Expected Output

### `python validator.py`
```
════════════════════════════════════════════════════════════
  S&P GLOBAL — Financial Data Validator  (demo run)
  Timestamp: 2026-05-29 14:00:00
════════════════════════════════════════════════════════════

2026-05-29 14:00:00 | INFO     | FinancialValidator | 🔍 Initiating financial data validation pipeline…
2026-05-29 14:00:00 | INFO     | FinancialValidator |    ✔ Rule 1 PASSED: Dataset is non-empty.
2026-05-29 14:00:00 | INFO     | FinancialValidator |    ✔ Rule 2 PASSED: All values are numeric.
2026-05-29 14:00:00 | INFO     | FinancialValidator |    ✔ Rule 3 PASSED: All prices are above the floor (0.00).
2026-05-29 14:00:00 | INFO     | FinancialValidator |    📊 Feed Stats → count=5 | min=390.0000 | max=393.1000 | mean=391.4700 | …
2026-05-29 14:00:00 | INFO     | FinancialValidator | ✅ Validation PASSED — feed is clean and ready for processing.

📋 Batch Validation Report:
────────────────────────────────────────────────────────────
  SPGI            → ✅ PASS
  AAPL            → ✅ PASS
  MSFT            → ✅ PASS
  INVALID_FEED    → ❌ FAIL
                    ↳ Pipeline REJECTED: Non-numeric types detected
────────────────────────────────────────────────────────────
```

### `pytest -v`
```
================================= test session starts =================================
collected 22 items

test_validator.py::TestValidData::test_standard_positive_prices PASSED          [  4%]
test_validator.py::TestValidData::test_single_price_entry PASSED                [  9%]
...
test_validator.py::TestCustomThreshold::test_prices_at_or_below_threshold_fail PASSED [100%]

================================ 22 passed in 0.42s ==================================
```

---

## 🔧 Workflow Triggers

| Event | Behaviour |
|-------|-----------|
| `push` to `main` | Full pipeline runs automatically |
| `push` to `release/**` | Full pipeline runs automatically |
| `pull_request` to `main` | Full pipeline runs for PR validation |
| `workflow_dispatch` | Manual trigger with optional debug mode |
| `.md` or `docs/` changes | Pipeline **skipped** (path-ignore optimization) |

---

## 🏅 Key DevOps Concepts Demonstrated

| Concept | Implementation |
|---------|---------------|
| **CI/CD Automation** | GitHub Actions — zero manual steps |
| **Quality Gates** | 4 sequential jobs, each blocking the next |
| **Shift-Left Security** | Bandit SAST runs before linting or tests |
| **Multi-Version Testing** | Python 3.10, 3.11, 3.12 matrix |
| **Coverage Enforcement** | Pipeline fails if coverage drops below 80% |
| **Concurrency Control** | Stale runs auto-cancelled on same branch |
| **Artifact Retention** | Reports stored for 30 days per run |
| **Pipeline Summary** | Markdown summary written to GitHub UI |
| **Path Optimization** | Docs-only changes skip the pipeline |
| **Separation of Concerns** | Validator / tests / config cleanly separated |

---

## 👤 Author

**Applying for:** Salesforce DevOps Intern — S&P Global  
**Stack:** Python · GitHub Actions · pytest · Flake8 · Bandit · Black

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f3460,50:16213e,100:1a1a2e&height=120&section=footer&animation=fadeIn" width="100%"/>
</div>
