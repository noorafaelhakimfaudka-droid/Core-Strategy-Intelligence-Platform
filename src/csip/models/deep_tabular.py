"""CSIP Tabular Neural Network with Entity Embeddings (Baseline Ladder B4).

SKKNI Compliance:
- [UK-09 Membangun Model]: Arsitektur Neural Network & Deep Learning untuk data tabular.
- Modul Kompetensi 14 & 15: MLP, Batch Normalization, Dropout, dan Entity Embeddings.

Optimized for 8 GB RAM laptop execution with PyTorch CPU acceleration.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

logger = logging.getLogger(__name__)


class TabularEmbeddingMLP(nn.Module):
    """PyTorch MLP with Categorical Entity Embedding layers for tabular e-commerce data."""

    def __init__(
        self,
        embedding_sizes: List[Tuple[int, int]],
        num_continuous_features: int,
        hidden_dims: List[int] = [128, 64],
        dropout_rate: float = 0.2,
    ) -> None:
        super().__init__()
        self.embeddings = nn.ModuleList([
            nn.Embedding(num_classes, emb_dim)
            for num_classes, emb_dim in embedding_sizes
        ])
        total_emb_dim = sum(emb_dim for _, emb_dim in embedding_sizes)

        # Batch normalization for continuous inputs
        self.bn_cont = nn.BatchNorm1d(num_continuous_features) if num_continuous_features > 0 else nn.Identity()

        # Feed-forward dense layers
        in_dim = total_emb_dim + num_continuous_features
        layers: List[nn.Module] = []
        for h_dim in hidden_dims:
            layers.append(nn.Linear(in_dim, h_dim))
            layers.append(nn.BatchNorm1d(h_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            in_dim = h_dim

        layers.append(nn.Linear(in_dim, 1))
        self.network = nn.Sequential(*layers)

    def forward(
        self,
        x_cat: torch.Tensor,
        x_cont: torch.Tensor,
    ) -> torch.Tensor:
        embedded = []
        for i, emb_layer in enumerate(self.embeddings):
            embedded.append(emb_layer(x_cat[:, i]))

        if embedded:
            x_emb = torch.cat(embedded, dim=1)
        else:
            x_emb = torch.empty((x_cat.size(0), 0), device=x_cat.device)

        if x_cont.size(1) > 0:
            x_cont_norm = self.bn_cont(x_cont)
            x_all = torch.cat([x_emb, x_cont_norm], dim=1)
        else:
            x_all = x_emb

        logits = self.network(x_all).squeeze(1)
        return logits


class TabularMLPClassifier:
    """Scikit-Learn style wrapper for TabularEmbeddingMLP."""

    def __init__(
        self,
        embedding_sizes: List[Tuple[int, int]],
        num_continuous_features: int,
        hidden_dims: List[int] = [128, 64],
        dropout_rate: float = 0.2,
        lr: float = 0.001,
        batch_size: int = 128,
        epochs: int = 10,
        random_state: int = 42,
    ) -> None:
        self.embedding_sizes = embedding_sizes
        self.num_continuous_features = num_continuous_features
        self.hidden_dims = hidden_dims
        self.dropout_rate = dropout_rate
        self.lr = lr
        self.batch_size = batch_size
        self.epochs = epochs
        self.random_state = random_state

        torch.manual_seed(random_state)
        self.model = TabularEmbeddingMLP(
            embedding_sizes=embedding_sizes,
            num_continuous_features=num_continuous_features,
            hidden_dims=hidden_dims,
            dropout_rate=dropout_rate,
        )
        self.loss_history: List[float] = []

    def fit(
        self,
        x_cat: np.ndarray,
        x_cont: np.ndarray,
        y: np.ndarray,
    ) -> TabularMLPClassifier:
        self.model.train()
        t_cat = torch.tensor(x_cat, dtype=torch.long)
        t_cont = torch.tensor(x_cont, dtype=torch.float32)
        t_y = torch.tensor(y, dtype=torch.float32)

        dataset = TensorDataset(t_cat, t_cont, t_y)
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

        # Handle class imbalance via pos_weight
        pos_count = float(np.sum(y == 1))
        neg_count = float(len(y) - pos_count)
        pos_weight = torch.tensor([neg_count / (pos_count + 1e-5)])

        criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr, weight_decay=1e-4)

        for epoch in range(self.epochs):
            epoch_loss = 0.0
            for b_cat, b_cont, b_y in loader:
                optimizer.zero_grad()
                logits = self.model(b_cat, b_cont)
                loss = criterion(logits, b_y)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item() * len(b_y)

            avg_loss = epoch_loss / len(dataset)
            self.loss_history.append(avg_loss)

        return self

    def predict_proba(
        self,
        x_cat: np.ndarray,
        x_cont: np.ndarray,
    ) -> np.ndarray:
        self.model.eval()
        t_cat = torch.tensor(x_cat, dtype=torch.long)
        t_cont = torch.tensor(x_cont, dtype=torch.float32)

        with torch.no_grad():
            logits = self.model(t_cat, t_cont)
            probs_pos = torch.sigmoid(logits).cpu().numpy()

        probs_neg = 1.0 - probs_pos
        return np.vstack([probs_neg, probs_pos]).T

    def predict(
        self,
        x_cat: np.ndarray,
        x_cont: np.ndarray,
        threshold: float = 0.5,
    ) -> np.ndarray:
        probs = self.predict_proba(x_cat, x_cont)[:, 1]
        return (probs >= threshold).astype(np.int8)

    def save_checkpoint(self, path: Union[str, Path]) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        torch.save({
            "model_state_dict": self.model.state_dict(),
            "embedding_sizes": self.embedding_sizes,
            "num_continuous": self.num_continuous_features,
            "hidden_dims": self.hidden_dims,
            "loss_history": self.loss_history,
        }, p)
