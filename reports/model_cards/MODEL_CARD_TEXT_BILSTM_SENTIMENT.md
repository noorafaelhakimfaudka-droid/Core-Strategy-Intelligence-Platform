# MODEL CARD: Text BiLSTM Customer Review Sentiment Classifier
## CSIP Deep Learning & NLP Artifact Governance

### 1. Model Details
- **Model Name**: Text Bi-directional LSTM Sentiment Classifier
- **Artifact Path**: `artifacts/models/text_bilstm_review_sentiment.pt`
- **Framework**: PyTorch (`torch.nn.Module`)
- **Version**: 17.0.0
- **Release Date**: November 2026
- **Architecture**:
  - Vocabulary Size: 5,000 tokens (Portuguese text)
  - Embedding Dimension: 64
  - Hidden Dimension: 64 (Bi-directional = 128 concatenated units)
  - Sequence Length: Padded/truncated to 50 tokens
  - Dropout: 0.20
  - Output: Binary classification (Negative Sentiment = Review Score 1 or 2)

### 2. Training Population & Population Reconciliation (Addressing F-V14-03)
- **Population Definition**: Unlike tabular models (which evaluate on all orders regardless of review text availability), the BiLSTM model is trained and evaluated strictly on the subset of orders with **non-empty review comment text** (`data/processed/review_corpus.parquet`, total $N = 41,524$ reviews).
- **Base Rate Difference**: Customers who write text feedback exhibit an elevated rate of severe dissatisfaction (~16.2% negative) compared to the overall order population (~9.85% negative).
- **Training Samples**: $N_{train} = 26,450$ reviews.
- **Validation Samples**: $N_{val} = 8,150$ reviews.
- **Test Samples**: $N_{test} = 4,142$ reviews.

### 3. Quantitative Performance (Holdout Text Test Set)
- **PR-AUC**: **0.3120** (vs. Text Prior Baseline: **0.1620**; +92.6% improvement).
- **ROC-AUC**: **0.7240** (vs. Chance: 0.5000).
- **F1-Score**: **0.3680**.
- **Test Brier Score**: **0.1140**.

### 4. Comparison with Tabular Models
- **Tabular Champion (LightGBM)**: Evaluated across all $N_{test} = 12,571$ orders using delivery and economic metadata (PR-AUC = 0.3061, base rate = 9.85%).
- **Deep NLP Model (BiLSTM)**: Evaluated across $N_{test} = 4,142$ text reviews using unigram/word sequence embeddings (PR-AUC = 0.3120, base rate = 16.2%).
- **Conclusion**: Both models provide distinct, complementary value: LightGBM flags logistics-driven dissatisfaction before or at delivery; BiLSTM analyzes qualitative customer sentiment post-survey.

### Deployment Maturity Level
- **Status**: `BENCHMARK_VALIDATED`
- **Operational Governance Assessment**: Offline test validated on written Portuguese customer reviews subset (PR-AUC 0.3120, ROC-AUC 0.7240). Validated as an NLP benchmark; requires low-latency inference optimization before pilot deployment.
