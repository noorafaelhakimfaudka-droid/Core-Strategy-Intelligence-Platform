"""Omni Router: Free-text natural language query parser and intent routing engine.

Parses unstructured Indonesian user queries, extracts numerical parameters,
identifies intent modes, and routes to appropriate simulation engines.
Compatible with 8 GB RAM environment (zero heavy dependencies).
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple


SAMPLE_TEXT_CORPUS = [
    "Barang sampai tepat waktu dan kurir sangat sopan, pelayanan luar biasa!",
    "Kecewa sekali, paket terlambat 5 hari dari tanggal janji dan tidak ada kabar sama sekali.",
    "Harga barang murah tapi ongkos kirimnya mahal sekali, terasa sangat memberatkan.",
    "Pesanan tiba dalam 2 hari, kemasan sangat rapi dan produk sesuai pesanan.",
    "Sudah menunggu seminggu barang belum juga tiba, kapok belanja di sini.",
    "Kualitas produk istimewa, sebanding dengan harga yang dibayar.",
    "Kurir ramah dan cepat, barang langsung saya gunakan hari ini juga.",
    "Barang rusak di jalan karena pengiriman terlalu lama dan kemasan penyok.",
    "Ongkir gratis sangat membantu, proses transaksi juga cepat dan nyaman.",
    "Keterlambatan 3 hari membuat acara ulang tahun anak saya berantakan.",
    "Pelayanan toko baik, pengiriman kilat, bintang lima untuk penjual.",
    "Ongkos kirim terlalu tinggi untuk jarak yang relatif dekat di dalam kota.",
    "Pengiriman cepat sekali, pesan kemarin siang sore ini sudah sampai pintu.",
    "Paket salah antar dan kurir tidak mau bertanggung jawab, sangat mengecewakan.",
    "Pilihan barang lengkap dan harga bersaing, pasti akan belanja kembali.",
    "Menunggu terlalu lama hingga lupa pernah memesan barang ini.",
    "Respon cepat dari penjual dan kurir datang tepat pada estimasi waktu.",
    "Biaya tambahan tak terduga saat pembayaran membuat saya batal membeli lagi.",
]

PRESET_QUERIES = {
    "bedah": "Mengapa orang rela membayar lebih mahal untuk barang yang datang cepat, tetapi tempat murah yang sering terlambat justru sepi?",
    "pengandaian": "Bagaimana jika biaya tambahan dipotong 20 persen, namun waktu tunggu pengiriman bertambah 1 hari?",
    "adu": "Pilihan A: Subsidi biaya kirim untuk semua orang vs Pilihan B: Perbaikan disiplin waktu tiba mitra kurir.",
    "teks": "\n".join(SAMPLE_TEXT_CORPUS[:10]),
    "csv": "Contoh Data Transaksi Toko Retail (Nilai Belanja, Biaya Ongkir, Hari Pengiriman, Skor Kepuasan)",
}


class OmniRouter:
    """Intelligent lightweight parser for human queries."""

    def __init__(self) -> None:
        self.presets = PRESET_QUERIES

    def parse(self, text: str, default_mode: str = "bedah") -> Dict[str, Any]:
        """Parse natural language query into intent and parameters."""
        raw_text = text.strip() if text else ""
        if not raw_text:
            return {
                "mode": default_mode,
                "clean_text": self.presets.get(default_mode, ""),
                "parameters": self._extract_parameters(self.presets.get(default_mode, "")),
                "is_preset": True,
            }

        lower_text = raw_text.lower()

        # 1. Detect Intent Mode
        detected_mode = default_mode
        if any(w in lower_text for w in ["vs", "versus", "pilihan a", "pilihan b", "bandingkan", "lebih baik mana"]):
            detected_mode = "adu"
        elif any(w in lower_text for w in ["bagaimana jika", "gimana kalau", "seandainya", "jika", "potong", "naikkan", "diskon", "turunkan"]):
            detected_mode = "pengandaian"
        elif any(w in lower_text for w in ["kenapa", "mengapa", "alasan", "fenomena", "tarik-menarik", "antre", "ragu", "sepi"]):
            detected_mode = "bedah"
        elif "\n" in raw_text or len(raw_text.split(".")) > 3:
            detected_mode = "teks"
        elif any(w in lower_text for w in ["csv", "file", "tabel", "unggah", "upload"]):
            detected_mode = "csv"

        # 2. Extract Numerical Parameters
        params = self._extract_parameters(raw_text)

        return {
            "mode": detected_mode,
            "clean_text": raw_text,
            "parameters": params,
            "is_preset": False,
        }

    def _extract_parameters(self, text: str) -> Dict[str, float]:
        """Extract percentage, days, and monetary numbers with safe defaults."""
        params: Dict[str, float] = {
            "subsidy_pct": 0.0,
            "delay_days_delta": 0.0,
            "cost_delta_pct": 0.0,
            "speed_gain_days": 0.0,
        }

        # Percentage detection (e.g. "20%", "20 persen", "diskon 15%")
        pct_match = re.search(r"(\d+(?:[\.,]\d+)?)\s*(?:%|persen)", text, re.IGNORECASE)
        if pct_match:
            try:
                params["subsidy_pct"] = float(pct_match.group(1).replace(",", "."))
                params["cost_delta_pct"] = -params["subsidy_pct"]
            except ValueError:
                pass

        # Days / time detection (e.g. "1 hari", "3 hari", "bertambah 2 hari", "terlambat 4 hari")
        day_matches = re.findall(r"(\d+(?:[\.,]\d+)?)\s*(?:hari|day)", text, re.IGNORECASE)
        if day_matches:
            try:
                first_day = float(day_matches[0].replace(",", "."))
                if any(w in text.lower() for w in ["pangkas", "kurang", "cepat"]):
                    params["speed_gain_days"] = first_day
                    params["delay_days_delta"] = -first_day
                else:
                    params["delay_days_delta"] = first_day
            except ValueError:
                pass

        # If no numbers found, provide calibrated real-world defaults based on intent
        if params["subsidy_pct"] == 0.0 and params["delay_days_delta"] == 0.0:
            params["subsidy_pct"] = 15.0
            params["delay_days_delta"] = -1.5  # 1.5 days faster

        return params


def parse_user_query(text: str, default_mode: str = "bedah") -> Dict[str, Any]:
    """Convenience helper function for parsing user queries."""
    router = OmniRouter()
    return router.parse(text, default_mode)

