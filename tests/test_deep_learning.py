"""Unit tests for CSIP Deep Learning & Model Explainability Module (Milestone 8).

SKKNI Compliance:
- [UK-09 Membangun Model]: Verifikasi fungsional arsitektur Neural Network (Tabular MLP & Text Bi-LSTM).
- [UK-10 Mengevaluasi Model]: Verifikasi kalibrasi probabilitas dan metrik diagnostik (ECE, Brier).
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pytest
import torch

from csip.evaluation.explainer import ModelExplainer, compute_ece
from csip.models.deep_seq import SimpleTokenizer, TextBiLSTM, TextBiLSTMClassifier
from csip.models.deep_tabular import TabularEmbeddingMLP, TabularMLPClassifier


def test_tabular_mlp_forward_shape():
    """Verify TabularEmbeddingMLP forward pass shapes and dimensions."""
    embedding_sizes = [(10, 4), (5, 3)]  # 2 categorical features
    num_cont = 4
    batch_size = 16

    model = TabularEmbeddingMLP(
        embedding_sizes=embedding_sizes,
        num_continuous_features=num_cont,
        hidden_dims=[32, 16],
        dropout_rate=0.1,
    )
    model.eval()

    x_cat = torch.randint(0, 5, (batch_size, 2))
    x_cont = torch.randn(batch_size, num_cont)

    with torch.no_grad():
        out = model(x_cat, x_cont)

    assert out.shape == (batch_size,)
    assert not torch.isnan(out).any()


def test_tabular_mlp_fit_and_predict():
    """Verify TabularMLPClassifier training and prediction pipeline."""
    np.random.seed(42)
    n_samples = 100
    x_cat = np.random.randint(0, 4, (n_samples, 2))
    x_cont = np.random.randn(n_samples, 3).astype(np.float32)
    y = np.random.randint(0, 2, n_samples).astype(np.int8)

    clf = TabularMLPClassifier(
        embedding_sizes=[(5, 2), (5, 2)],
        num_continuous_features=3,
        hidden_dims=[16],
        epochs=2,
        batch_size=32,
    )
    clf.fit(x_cat, x_cont, y)

    probs = clf.predict_proba(x_cat, x_cont)
    preds = clf.predict(x_cat, x_cont)

    assert probs.shape == (n_samples, 2)
    np.testing.assert_allclose(probs.sum(axis=1), np.ones(n_samples), atol=1e-5)
    assert set(np.unique(preds)).issubset({0, 1})
    assert len(clf.loss_history) == 2

    # Verify checkpoint saving
    with tempfile.TemporaryDirectory() as tmpdir:
        ckpt_path = Path(tmpdir) / "test_mlp.pt"
        clf.save_checkpoint(ckpt_path)
        assert ckpt_path.exists()


def test_simple_tokenizer():
    """Verify SimpleTokenizer tokenization, vocabulary mapping, and transformation."""
    texts = [
        "Produto excelente e entrega rapida!",
        "Pessimo atendimento, nunca mais compro.",
        "Entrega antes do prazo, produto muito bom.",
    ]
    tokenizer = SimpleTokenizer(max_vocab_size=20, min_freq=1)
    tokenizer.fit(texts)

    assert len(tokenizer.word2idx) > 2
    assert "<PAD>" in tokenizer.word2idx
    assert "<UNK>" in tokenizer.word2idx

    seqs = tokenizer.transform(texts, max_len=6)
    assert seqs.shape == (3, 6)
    assert seqs.dtype == np.int64


def test_text_bilstm_classifier():
    """Verify TextBiLSTMClassifier end-to-end training and inference."""
    texts = [
        "Otimo produto, amei!",
        "Muito ruim, nao recomendo.",
        "Chegou quebrado e atrasado.",
        "Tudo perfeito, obrigado!",
        "Nao gostei da cor e do tamanho.",
    ] * 10
    y = np.array([0, 1, 1, 0, 1] * 10, dtype=np.int8)

    bilstm = TextBiLSTMClassifier(
        max_vocab_size=50,
        max_seq_len=10,
        embedding_dim=16,
        hidden_dim=16,
        epochs=2,
        batch_size=16,
    )
    bilstm.fit(texts, y)

    probs = bilstm.predict_proba(texts)
    preds = bilstm.predict(texts)

    assert probs.shape == (len(texts), 2)
    np.testing.assert_allclose(probs.sum(axis=1), np.ones(len(texts)), atol=1e-5)
    assert set(np.unique(preds)).issubset({0, 1})

    with tempfile.TemporaryDirectory() as tmpdir:
        ckpt_path = Path(tmpdir) / "test_bilstm.pt"
        bilstm.save_checkpoint(ckpt_path)
        assert ckpt_path.exists()


def test_compute_ece():
    """Verify Expected Calibration Error calculation."""
    # Perfect calibration
    y_true = np.array([1, 1, 0, 0])
    y_prob = np.array([1.0, 1.0, 0.0, 0.0])
    ece_perfect = compute_ece(y_true, y_prob, n_bins=5)
    assert ece_perfect == pytest.approx(0.0, abs=1e-4)

    # Completely wrong calibration
    y_prob_wrong = np.array([0.0, 0.0, 1.0, 1.0])
    ece_wrong = compute_ece(y_true, y_prob_wrong, n_bins=5)
    assert ece_wrong > 0.5


def test_model_explainer_calibration():
    """Verify ModelExplainer probability calibration analysis."""
    np.random.seed(42)
    n = 200
    y_val_true = np.random.binomial(1, 0.2, n)
    y_val_prob = np.clip(y_val_true * 0.7 + np.random.uniform(0, 0.3, n), 0.01, 0.99)

    y_test_true = np.random.binomial(1, 0.2, n)
    y_test_prob = np.clip(y_test_true * 0.7 + np.random.uniform(0, 0.3, n), 0.01, 0.99)

    explainer = ModelExplainer(random_state=42)
    with tempfile.TemporaryDirectory() as tmpdir:
        fig_path = Path(tmpdir) / "calib.png"
        res = explainer.evaluate_and_calibrate(
            y_val_true=y_val_true,
            y_val_prob=y_val_prob,
            y_test_true=y_test_true,
            y_test_prob=y_test_prob,
            output_fig_path=fig_path,
        )
        assert "uncalibrated_brier" in res
        assert "calibrated_brier" in res
        assert "calibrated_ece" in res
        assert fig_path.exists()
