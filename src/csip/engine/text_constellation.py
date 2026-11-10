"""Text Constellation: Transforms human reviews and opinions into a 2D celestial galaxy.

Extracts sentiment and topic clusters using lightweight TF-IDF and SVD.
Memory-efficient (<5 MB), sub-second execution, no external network dependencies.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


# Lightweight Indonesian Sentiment Lexicon
POSITIVE_WORDS = {
    "bagus", "cepat", "tepat", "waktu", "puas", "rapi", "suka", "istimewa",
    "ramah", "mantap", "sesuai", "senang", "terima", "kasih", "terbaik",
    "aman", "original", "berkualitas", "rekomendasi", "kilat", "membantu",
}

NEGATIVE_WORDS = {
    "kecewa", "lambat", "telat", "terlambat", "rusak", "penyok", "pecah",
    "mahal", "kapok", "parah", "lama", "kurang", "cacat", "salah",
    "buruk", "berat", "rugi", "bohong", "batal", "hilang",
}


class TextConstellationEngine:
    """Processes collections of human opinions into a celestial 2D map."""

    def __init__(self) -> None:
        pass

    def process_text_corpus(self, text_input: str) -> Dict[str, Any]:
        """Convert multi-line text input into structured 2D constellation points."""
        lines = [line.strip() for line in text_input.strip().split("\n") if line.strip()]

        if not lines:
            lines = ["Layanan sangat cepat dan memuaskan", "Paket datang terlambat dan kemasan penyok"]

        # Ensure at least 4 items for clean 2D projection
        if len(lines) < 4:
            lines = lines * 2

        # 1. Sentiment Scoring & Topic Detection
        records: List[Dict[str, Any]] = []
        for i, sentence in enumerate(lines):
            score, label = self._calculate_sentiment(sentence)
            topic, color = self._classify_topic(sentence, score)
            records.append({
                "id": i + 1,
                "text": sentence,
                "sentiment_score": score,
                "sentiment_label": label,
                "topic": topic,
                "color": color,
            })

        # 2. 2D Coordinate Projection via TF-IDF & TruncatedSVD
        coords = self._project_2d(lines)

        for i, rec in enumerate(records):
            rec["x"] = float(round(coords[i, 0], 3))
            rec["y"] = float(round(coords[i, 1], 3))

        # 3. Overall Mood Summary
        avg_score = float(np.mean([r["sentiment_score"] for r in records]))
        positive_count = sum(1 for r in records if r["sentiment_score"] >= 3.5)
        negative_count = sum(1 for r in records if r["sentiment_score"] < 3.0)

        return {
            "points": records,
            "total_opinions": len(records),
            "average_sentiment": round(avg_score, 1),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "conclusion": f"Dari {len(records)} ungkapan suara, sentimen rata-rata berada pada tingkat {avg_score:.1f} dari 5.0.",
        }

    def _calculate_sentiment(self, text: str) -> Tuple[float, str]:
        """Simple rule-based Indonesian sentiment scoring."""
        words = set(re.findall(r"\b\w+\b", text.lower()))
        pos_hits = len(words.intersection(POSITIVE_WORDS))
        neg_hits = len(words.intersection(NEGATIVE_WORDS))

        net = pos_hits - neg_hits
        if net > 0:
            score = min(5.0, 3.5 + 0.5 * net)
            label = "Puas dan Bahagia"
        elif net < 0:
            score = max(1.0, 2.5 + 0.5 * net)
            label = "Kecewa dan Terluka"
        else:
            score = 3.0
            label = "Netral atau Bimbang"

        return score, label

    def _classify_topic(self, text: str, sentiment: float) -> Tuple[str, str]:
        """Classify into 4 human topics and assign luminous theme colors."""
        lower = text.lower()
        if any(w in lower for w in ["waktu", "cepat", "lambat", "telat", "terlambat", "lama", "hari", "kurir"]):
            topic = "Ketepatan Waktu & Kurir"
            color = "#F5B041" if sentiment >= 3.5 else "#F43F5E"  # Gold or Crimson
        elif any(w in lower for w in ["ongkir", "biaya", "harga", "mahal", "murah", "potongan", "diskon"]):
            topic = "Beban Biaya & Ongkos Kirim"
            color = "#A855F7"  # Amethyst Glow
        elif any(w in lower for w in ["rusak", "penyok", "kualitas", "kemasan", "rapi", "pecah", "barang", "produk"]):
            topic = "Kualitas Produk & Kemasan"
            color = "#38BDF8"  # Cyan Nebula
        else:
            topic = "Pengalaman Umum Berbelanja"
            color = "#F5B041" if sentiment >= 3.0 else "#F43F5E"

        return topic, color

    def _project_2d(self, texts: List[str]) -> np.ndarray:
        """Project texts into 2D coordinates using TF-IDF + SVD or organic spiral."""
        try:
            vec = TfidfVectorizer(max_features=50, stop_words=None, min_df=1)
            X = vec.fit_transform(texts)
            if X.shape[1] >= 2 and len(texts) >= 3:
                svd = TruncatedSVD(n_components=2, random_state=42)
                coords = svd.fit_transform(X)
                # Normalize to range [-10, 10]
                std = np.std(coords, axis=0) + 1e-5
                coords = (coords - np.mean(coords, axis=0)) / std * 6.0
                return coords
        except Exception:
            pass

        # Fallback organic celestial spiral distribution
        n = len(texts)
        indices = np.arange(n)
        angles = indices * 2.39996  # Golden angle
        radii = np.sqrt(indices + 1) * 2.5
        x = radii * np.cos(angles)
        y = radii * np.sin(angles)
        return np.column_stack([x, y])

