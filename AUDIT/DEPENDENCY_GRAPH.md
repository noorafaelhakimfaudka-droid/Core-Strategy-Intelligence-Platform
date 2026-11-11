> [HISTORICAL ARCHIVE] - This document is preserved as an unedited historical audit record from previous versions.

# CSIP V14 ARCHITECTURE & SYSTEM DEPENDENCY GRAPH
## End-to-End Computational Society Intelligence Platform (SKKNI 299/2020 Compliant)

`mermaid
flowchart TD
    subgraph RawData [Raw Olist Data Layer]
        R1[olist_orders_dataset.csv]
        R2[olist_order_items_dataset.csv]
        R3[olist_order_payments_dataset.csv]
        R4[olist_order_reviews_dataset.csv]
        R5[olist_customers_dataset.csv]
        R6[olist_products_dataset.csv]
        R7[olist_sellers_dataset.csv]
        R8[olist_geolocation_dataset.csv]
    end

    subgraph Cleaning [Data Cleaning & Validation: cleaner.py & auto_cleaner.py]
        C1[clean_orders.parquet]
        C2[clean_order_items.parquet]
        C3[clean_order_payments.parquet]
        C4[clean_order_reviews.parquet]
        C5[clean_customers.parquet]
        C6[clean_products.parquet]
        C7[clean_sellers.parquet]
        C8[clean_geolocation_dedup.parquet]
    end

    subgraph FeatureEngineering [Multi-Grain Feature Engineering: engineer.py]
        F1[order_level.parquet - Order Grain]
        F2[customer_cohort.parquet - Customer Grain]
        F3[review_corpus.parquet - Text Grain]
        F4[weekly_system_state.parquet - Macro Grain]
    end

    subgraph Modeling [Baseline Ladder & Models: trainer.py, classic.py, deep_seq.py, state_transition.py]
        M1[B0 Naive Majority / Mean Baselines]
        M2[B1 Linear / Ridge / Logistic Models]
        M3[B2 Trees / KNN / Naive Bayes]
        M4[B3 LightGBM & Random Forest Champions]
        M5[Neural Models: Tabular MLP & Text Bi-LSTM]
        M6[World Model: Weekly Macro State Transition VAR/AR]
    end

    subgraph Evaluation [Evaluation & Explainability: explainer.py, bootstrap.py]
        E1[Probability Calibration & Reliability Diagrams]
        E2[SHAP Feature Attribution: TreeExplainer]
        E3[95% Bootstrap CIs & Statistical Significance]
        E4[ML Leaderboard: PR-AUC, ROC-AUC, Brier Score]
    end

    subgraph Competency [Competency & Evidence System: registry.py]
        K1[canonical_skkni_299_2020.json: 11 Units, 27 Elements, 63 KUK]
        K2[MASTER_COMPETENCY_MATRIX.csv & .xlsx]
        K3[EVIDENCE_REGISTRY.csv: Artifact & Code Links]
        K4[ASSESSOR_EVIDENCE_GUIDE.md & CANDIDATE_DEMONSTRATION_GUIDE.md]
    end

    subgraph StreamlitApp [Multi-Page Streamlit Showcase]
        P1[1_Executive_Overview.py]
        P2[2_Data_Observatory.py]
        P3[3_Behavioral_Discovery_Lab.py]
        P4[4_Hypothesis_Laboratory.py]
        P5[5_Predictive_Intelligence.py]
        P6[6_World_Model.py]
        P7[7_Alternative_World_Simulator.py]
        P8[8_Decision_Studio.py]
        P9[9_Evidence_Registry_Review.py]
    end

    RawData --> Cleaning
    Cleaning --> FeatureEngineering
    FeatureEngineering --> Modeling
    Modeling --> Evaluation
    Evaluation --> StreamlitApp
    Competency --> StreamlitApp
`

### Module Coupling and Interface Boundaries
1. **Core Data Ingestion (csip.data.loader)**: Pure pandas/pyarrow reader with schema validation and type coercion.
2. **Data Cleaning (csip.cleaning.cleaner)**: Split-before-transform compliant deterministic cleaning functions.
3. **Feature Engineering (csip.features.engineer)**: Strictly adheres to the **Temporal & Feature Isolation Protocol**. Features are divided into:
   - **Context A: Checkout-Time Prediction** (E1_checkout_retrospective_conditional / early warning features known at order checkout).
   - **Context B: Post-Delivery Fulfillment Prediction** (post_delivery_fulfillment features including delivery delays, transit times).
   - **Context C: Retrospective Analytical Diagnosis** (Post-outcome exploratory and root-cause analysis).
4. **Machine Learning Engines (csip.models)**:
   - 	rainer.py: Orchestrates baseline ladder B0-B3 with time-based train/val/test splits and embargo buffers.
   - classic.py: Implements B0 naive baselines, B1 linear models, B2 decision trees/KNN/Naive Bayes, and B3 ensemble models (LightGBM, Random Forest).
   - deep_tabular.py: PyTorch Tabular Embedding MLP.
   - deep_seq.py: PyTorch Bi-LSTM text sentiment classifier for review comments.
   - world.state_transition.py: Multi-equation linear dynamical system modeling macro-level e-commerce states.
5. **Evaluation & Explainability (csip.evaluation)**:
   - explainer.py: Computes TreeExplainer SHAP values, expected calibration error (ECE), and Platt-scaled probability calibration.
   - uncertainty.bootstrap.py: Calculates 95% bootstrap confidence intervals for test set evaluation metrics.
6. **Competency System (csip.evidence)**:
   - Programmatically verifies SHA256 hashes, file existence, and KUK mappings for all 63 KUKs across SKKNI 299/2020.
