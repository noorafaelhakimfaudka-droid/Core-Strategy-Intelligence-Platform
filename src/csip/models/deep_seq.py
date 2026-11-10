"""CSIP Sequence Deep Learning Module: Bi-LSTM for Review Text (Baseline Ladder B4).

SKKNI Compliance:
- [UK-09 Membangun Model]: Sequence modeling & Deep Learning untuk representasi teks ulasan.
- Modul Kompetensi 15 & 16: NLP, Word Embeddings, Bidirectional LSTM, dan Sentiment Classification.

Optimized for 8 GB RAM laptop execution with PyTorch CPU acceleration.
"""

from __future__ import annotations

import logging
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

logger = logging.getLogger(__name__)


class SimpleTokenizer:
    """Lightweight Portuguese regex tokenizer with vocabulary truncation."""

    def __init__(self, max_vocab_size: int = 5000, min_freq: int = 2) -> None:
        self.max_vocab_size = max_vocab_size
        self.min_freq = min_freq
        self.word2idx: Dict[str, int] = {"<PAD>": 0, "<UNK>": 1}
        self.idx2word: Dict[int, str] = {0: "<PAD>", 1: "<UNK>"}
        self.token_pattern = re.compile(r"\b\w+\b", re.UNICODE)

    def tokenize(self, text: str) -> List[str]:
        if not isinstance(text, str):
            return []
        return self.token_pattern.findall(text.lower())

    def fit(self, texts: List[str]) -> SimpleTokenizer:
        counter: Counter[str] = Counter()
        for text in texts:
            tokens = self.tokenize(text)
            counter.update(tokens)

        # Select top frequent tokens above min_freq
        vocab = [
            word for word, count in counter.most_common(self.max_vocab_size - 2)
            if count >= self.min_freq
        ]

        for idx, word in enumerate(vocab, start=2):
            self.word2idx[word] = idx
            self.idx2word[idx] = word

        logger.info(f"Fitted tokenizer vocabulary size: {len(self.word2idx)}")
        return self

    def transform(self, texts: List[str], max_len: int = 50) -> np.ndarray:
        sequences = np.zeros((len(texts), max_len), dtype=np.int64)
        for i, text in enumerate(texts):
            tokens = self.tokenize(text)[:max_len]
            for j, token in enumerate(tokens):
                sequences[i, j] = self.word2idx.get(token, 1)  # 1 is <UNK>
        return sequences


class TextBiLSTM(nn.Module):
    """Bidirectional LSTM with Embedding and pooling for review text classification."""

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int = 64,
        hidden_dim: int = 64,
        num_layers: int = 1,
        dropout_rate: float = 0.3,
    ) -> None:
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers=num_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout_rate if num_layers > 1 else 0.0,
        )
        # 2 * hidden_dim because bidirectional
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, 64),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(64, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch_size, seq_len)
        emb = self.embedding(x)  # (batch_size, seq_len, emb_dim)
        lstm_out, _ = self.lstm(emb)  # (batch_size, seq_len, 2 * hidden_dim)

        # Global Max Pooling over sequence dimension
        pooled, _ = torch.max(lstm_out, dim=1)  # (batch_size, 2 * hidden_dim)
        logits = self.classifier(pooled).squeeze(1)
        return logits


class TextBiLSTMClassifier:
    """Scikit-Learn style wrapper for TextBiLSTM with built-in Tokenizer."""

    def __init__(
        self,
        max_vocab_size: int = 5000,
        max_seq_len: int = 50,
        embedding_dim: int = 64,
        hidden_dim: int = 64,
        dropout_rate: float = 0.3,
        lr: float = 0.002,
        batch_size: int = 128,
        epochs: int = 6,
        random_state: int = 42,
    ) -> None:
        self.max_vocab_size = max_vocab_size
        self.max_seq_len = max_seq_len
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.dropout_rate = dropout_rate
        self.lr = lr
        self.batch_size = batch_size
        self.epochs = epochs
        self.random_state = random_state

        self.tokenizer = SimpleTokenizer(max_vocab_size=max_vocab_size)
        self.model: Optional[TextBiLSTM] = None
        self.loss_history: List[float] = []

    def fit(self, texts: List[str], y: np.ndarray) -> TextBiLSTMClassifier:
        torch.manual_seed(self.random_state)
        self.tokenizer.fit(texts)
        x_seq = self.tokenizer.transform(texts, max_len=self.max_seq_len)

        vocab_size = len(self.tokenizer.word2idx)
        self.model = TextBiLSTM(
            vocab_size=vocab_size,
            embedding_dim=self.embedding_dim,
            hidden_dim=self.hidden_dim,
            dropout_rate=self.dropout_rate,
        )
        self.model.train()

        t_x = torch.tensor(x_seq, dtype=torch.long)
        t_y = torch.tensor(y, dtype=torch.float32)

        dataset = TensorDataset(t_x, t_y)
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

        pos_count = float(np.sum(y == 1))
        neg_count = float(len(y) - pos_count)
        pos_weight = torch.tensor([neg_count / (pos_count + 1e-5)])

        criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr, weight_decay=1e-4)

        for epoch in range(self.epochs):
            epoch_loss = 0.0
            for b_x, b_y in loader:
                optimizer.zero_grad()
                logits = self.model(b_x)
                loss = criterion(logits, b_y)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item() * len(b_y)

            avg_loss = epoch_loss / len(dataset)
            self.loss_history.append(avg_loss)
            logger.info(f"Epoch {epoch + 1}/{self.epochs} - Loss: {avg_loss:.4f}")

        return self

    def predict_proba(self, texts: List[str]) -> np.ndarray:
        if self.model is None:
            raise RuntimeError("Model has not been fitted yet.")
        self.model.eval()
        x_seq = self.tokenizer.transform(texts, max_len=self.max_seq_len)
        t_x = torch.tensor(x_seq, dtype=torch.long)

        dataset = TensorDataset(t_x)
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=False)

        all_probs = []
        with torch.no_grad():
            for (b_x,) in loader:
                logits = self.model(b_x)
                probs = torch.sigmoid(logits).cpu().numpy()
                all_probs.append(probs)

        probs_pos = np.concatenate(all_probs)
        probs_neg = 1.0 - probs_pos
        return np.vstack([probs_neg, probs_pos]).T

    def predict(self, texts: List[str], threshold: float = 0.5) -> np.ndarray:
        probs = self.predict_proba(texts)[:, 1]
        return (probs >= threshold).astype(np.int8)

    def save_checkpoint(self, path: Union[str, Path]) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        torch.save({
            "model_state_dict": self.model.state_dict() if self.model else None,
            "word2idx": self.tokenizer.word2idx,
            "max_vocab_size": self.max_vocab_size,
            "max_seq_len": self.max_seq_len,
            "embedding_dim": self.embedding_dim,
            "hidden_dim": self.hidden_dim,
            "loss_history": self.loss_history,
        }, p)
