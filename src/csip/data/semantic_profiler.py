from pathlib import Path
import re
import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes, load_wine


def fmt_num(val: float, unit: str = "") -> str:
    """Format angka jutaan/ribuan menjadi bahasa manusia yang ringkas."""
    if pd.isna(val):
        return "-"
    v = float(val)
    abs_v = abs(v)
    sign = "-" if v < 0 else ""

    if abs_v >= 1_000_000_000:
        core = f"{sign}{abs_v / 1_000_000_000:.2f} Miliar"
    elif abs_v >= 1_000_000:
        core = f"{sign}{abs_v / 1_000_000:.2f} Juta"
    elif abs_v >= 10_000:
        core = f"{sign}{abs_v / 1_000:.1f} Ribu"
    elif abs_v >= 100:
        core = f"{sign}{abs_v:,.1f}"
    elif abs_v == int(abs_v):
        core = f"{int(v)}"
    else:
        core = f"{v:,.2f}"

    if not unit:
        return core
    if unit in ("$", "Rp"):
        return f"{unit}{core}"
    if unit == "%":
        return f"{core}%"
    return f"{core} {unit}"


# Kamus Bahasa Alami yang sudah bebas dari pengulangan kata (No Redundancy)
# Format: (regex_pattern, ui_label, subject_phrase, verb_when_up, verb_when_down, unit, description, role)
NATURAL_LEXICON = [
    # Pasar Keuangan / Kripto (OHLCV)
    (r"^close$|harga_penutupan|closing_price", "Harga Pasar", "harga aset di pasar", "menguat naik", "terkoreksi turun", "$", "Nilai penutupan aset di akhir periode perdagangan", "target_utama"),
    (r"return_harian|daily_return", "Untung/Rugi Harian", "imbal hasil harian", "mencetak untung", "mengalami koreksi", "%", "Persentase perubahan harga dibandingkan hari sebelumnya", "target_kedua"),
    (r"gejolak_harga|volatility|rentang_harian", "Gejolak Harian (High-Low)", "ayunan harga harian", "bergejolak lebar", "bergerak tenang", "$", "Selisih antara titik harga tertinggi dan terendah dalam sehari", "faktor"),
    (r"momentum_7h|ma7_gap", "Posisi vs Tren Mingguan", "jarak harga dari rata-rata mingguan", "melaju di atas rata-rata mingguan", "turun ke bawah rata-rata mingguan", "%", "Persentase selisih harga saat ini terhadap tren 7 hari terakhir", "faktor"),
    (r"momentum_30h|ma30_gap", "Posisi vs Tren Bulanan", "jarak harga dari tren bulanan", "menembus ke atas garis tren bulanan", "melemah di bawah garis tren bulanan", "%", "Persentase selisih harga saat ini terhadap rata-rata 30 hari", "faktor"),
    (r"tekanan_beli|candle_body", "Dorongan Beli vs Jual", "tekanan transaksi harian", "didominasi akumulasi beli", "ditekan aksi jual", "%", "Perbandingan kekuatan dorongan pembeli melawan penjual", "faktor"),
    (r"^volume$|nilai_transaksi_pasar", "Volume Transaksi Pasar", "aktivitas transaksi di pasar", "melonjak ramai", "menyusut sepi", "", "Total nilai atau jumlah perpindahan aset yang diperdagangkan", "faktor"),

    # E-Commerce & Toko Online (Olist dll)
    (r"review_score|skor_kepuasan|rating|satisfaction", "Kepuasan Pembeli", "tingkat kepuasan pembeli", "meningkat puas", "merosot kecewa", "poin", "Penilaian ulasan pelanggan dari skala 1 sampai 5", "target_utama"),
    (r"payment_value|total_belanja|omzet|revenue|sales", "Nilai Belanja", "total nilai belanja", "bertumbuh besar", "menyusut turun", "", "Total uang yang dibayarkan pelanggan dalam satu transaksi", "target_kedua"),
    (r"price|harga_barang|unit_price", "Harga Barang", "harga jual produk", "dipasang lebih tinggi", "dibuat lebih terjangkau", "", "Harga murni produk sebelum ditambah biaya pengiriman", "faktor"),
    (r"freight_value|ongkir|shipping", "Ongkos Kirim", "biaya ongkos kirim", "bertambah mahal", "lebih hemat", "", "Tarif pengiriman yang ditanggung oleh pembeli", "faktor"),
    (r"freight_ratio|rasio_ongkir", "Beban Ongkir vs Harga", "porsi ongkir terhadap harga barang", "terasa memberatkan pembeli", "terasa ringan di kantong", "%", "Persentase perbandingan ongkir terhadap harga produk", "faktor"),
    (r"delivery_delay|keterlambatan|telat", "Keterlambatan Kirim", "jadwal pengiriman paket", "molor melewati estimasi", "tiba lebih cepat dari janji", "hari", "Selisih hari barang sampai dibanding janji awal (positif = telat)", "faktor"),
    (r"delivery_days|lama_kirim|waktu_tunggu", "Lama Pengiriman", "durasi tunggu pengiriman", "memakan waktu lama", "sampai lebih cepat", "hari", "Total hari tunggu sejak pesanan dibuat hingga diterima", "faktor"),
    (r"installment|cicilan", "Tenor Cicilan", "pilihan tenor cicilan", "diambil makin panjang", "dibayar lebih singkat", "kali", "Jumlah tahapan pembayaran cicilan oleh pembeli", "faktor"),

    # Kesehatan & Medis
    (r"progresi_risiko|risiko_kesehatan|disease", "Risiko Keparahan", "indeks risiko kesehatan", "memburuk naik", "lebih terkendali", "poin", "Tingkat perkembangan risiko penyakit pasien", "target_utama"),
    (r"^bmi$|berat_badan", "Indeks Massa Tubuh (BMI)", "indeks massa tubuh", "meningkat berlebih", "mendekati batas ideal", "poin", "Rasio berat badan terhadap tinggi badan", "faktor"),
    (r"^bp$|tekanan_darah", "Tekanan Darah", "tekanan darah arteri", "meninggi", "lebih stabil", "mmHg", "Rata-rata tekanan darah pasien", "faktor"),
    (r"glucose|gula_darah|^s6$", "Kadar Gula Darah", "kadar gula darah", "melonjak tinggi", "lebih terkontrol", "mg/dL", "Tingkat glukosa di dalam aliran darah", "faktor"),
    (r"cholesterol|kolesterol|^s1$", "Kolesterol Total", "kadar kolesterol total", "meningkat", "menurun", "mg/dL", "Total kandungan kolesterol darah", "faktor"),
    (r"^ldl$|^s2$", "Kolesterol Jahat (LDL)", "kolesterol jahat (LDL)", "menumpuk tinggi", "berkurang turun", "mg/dL", "Lemak pemicu penyempitan pembuluh darah", "faktor"),
    (r"^hdl$|^s3$", "Kolesterol Baik (HDL)", "kolesterol pelindung (HDL)", "bertambah tinggi", "menurun", "mg/dL", "Lemak baik pembersih pembuluh darah", "faktor"),
    (r"^age$|umur|usia", "Usia", " kelompok usia", "bertambah senior", "lebih muda", "tahun", "Umur subjek yang tercatat di data", "faktor"),

    # Mutu Produk
    (r"kelas_kualitas|quality|mutu|grade", "Mutu Produk", "peringkat mutu produk", "naik ke level premium", "turun kelas", "poin", "Tingkat kualitas akhir produk dari hasil uji", "target_utama"),
    (r"flavanoids|flavonoid", "Kadar Flavonoid", "kandungan antioksidan flavonoid", "makin kaya", "makin rendah", "poin", "Senyawa alami penentu kualitas rasa dan daya simpan", "faktor"),
    (r"alcohol|alkohol", "Kadar Alkohol", "kandungan alkohol", "meningkat", "menurun", "%", "Persentase kadar alkohol dalam komposisi", "faktor"),
    (r"color_intensity|warna", "Kepekatan Warna", "kepekatan warna produk", "tampil makin pekat", "terlihat lebih pucat", "poin", "Tingkat kecerahan dan kepekatan visual", "faktor"),
    (r"malic_acid|asam", "Tingkat Keasaman", "kadar asam alami", "terasa makin asam", "terasa lebih lembut", "poin", "Tingkat keasaman malat pada bahan baku", "faktor"),
    (r"proline", "Kadar Proline", "kandungan asam amino proline", "meningkat tinggi", "menurun", "mg", "Indikator kematangan bahan baku utama", "faktor"),
]


def smart_transform_uploaded_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, str, dict]:
    """
    [UK-03, UK-04, UK-07] Menelaah, memvalidasi, dan mengkonstruksi fitur cerdas.
    1. Jika tabel OHLCV (Keuangan/Kripto), ekstrak indikator tren & volatilitas agar tidak kolinear.
    2. Jika ada kolom kategori/teks penting (2-12 kategori), lakukan frekuensi/ordinal encoding otomatis.
    """
    raw_rows, raw_cols = df.shape
    missing_cells = int(df.isna().sum().sum())
    dup_rows = int(df.duplicated().sum())

    cols_lower = {c.lower().strip(): c for c in df.columns}
    encoded_categories = []

    if {"open", "high", "low", "close"}.issubset(set(cols_lower.keys())):
        work = df.copy()
        for d_col in ["date", "timestamp", "time", "tanggal"]:
            if d_col in cols_lower:
                work[cols_lower[d_col]] = pd.to_datetime(work[cols_lower[d_col]], errors="coerce")
                work = work.sort_values(cols_lower[d_col]).reset_index(drop=True)
                break

        close_s = pd.to_numeric(work[cols_lower["close"]], errors="coerce")
        open_s = pd.to_numeric(work[cols_lower["open"]], errors="coerce")
        high_s = pd.to_numeric(work[cols_lower["high"]], errors="coerce")
        low_s = pd.to_numeric(work[cols_lower["low"]], errors="coerce")

        smart_df = pd.DataFrame()
        # Urutkan agar close (Harga Pasar) menjadi target utama secara default
        smart_df["gejolak_harga"] = (high_s - low_s).round(2)
        smart_df["tekanan_beli"] = (((close_s - open_s) / (open_s + 1e-9)) * 100.0).round(2)
        ma7 = close_s.rolling(7, min_periods=1).mean()
        ma30 = close_s.rolling(30, min_periods=1).mean()
        smart_df["momentum_7h"] = (((close_s - ma7) / (ma7 + 1e-9)) * 100.0).round(2)
        smart_df["momentum_30h"] = (((close_s - ma30) / (ma30 + 1e-9)) * 100.0).round(2)

        if "volume" in cols_lower:
            smart_df["volume"] = pd.to_numeric(work[cols_lower["volume"]], errors="coerce")

        smart_df["return_harian"] = (close_s.pct_change() * 100.0).round(2)
        smart_df["close"] = close_s.round(2)

        clean_out = smart_df.dropna().reset_index(drop=True)
        audit_info = {
            "raw_rows": raw_rows,
            "raw_cols": raw_cols,
            "clean_rows": len(clean_out),
            "missing_fixed": missing_cells,
            "duplicates_removed": dup_rows,
            "encoded_cats": ["Open/High/Low -> Gejolak & Momentum Tren"],
        }
        return (
            clean_out,
            "Data pergerakan pasar terdeteksi: kolom kembar (Open/High/Low) otomatis diringkas menjadi indikator tren & gejolak harian.",
            audit_info,
        )

    # Untuk tabel umum/bisnis: konversi juga kolom kategori/teks yang memiliki 2 s/d 12 nilai unik
    work = df.drop_duplicates().copy()
    cat_cols = work.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    for c in cat_cols:
        c_low = c.lower().strip()
        if any(skip in c_low for skip in ["id", "uuid", "nama", "name", "date", "tanggal", "time", "alamat"]):
            continue
        nunq = work[c].nunique(dropna=True)
        if 2 <= nunq <= 12:
            # Urutkan kode berdasarkan frekuensi kemunculan
            freq_order = work[c].value_counts().index.tolist()
            mapping = {val: idx + 1 for idx, val in enumerate(freq_order)}
            new_col_name = f"Kategori {c.replace('_', ' ').title()}"
            work[new_col_name] = work[c].map(mapping).astype(float)
            encoded_categories.append(f"{c} ({nunq} grup)")

    audit_info = {
        "raw_rows": raw_rows,
        "raw_cols": raw_cols,
        "clean_rows": len(work),
        "missing_fixed": missing_cells,
        "duplicates_removed": dup_rows,
        "encoded_cats": encoded_categories if encoded_categories else ["Tidak ada kolom teks yang perlu dikodekan"],
    }
    return work, "Data tabel siap dibedah: mencari hubungan sebab-akibat antar variabel secara otomatis.", audit_info


def build_fluent_schema(df: pd.DataFrame) -> tuple[pd.DataFrame, dict, str, dict]:
    """[UK-01, UK-02, UK-05] Membangun skema bahasa manusia dan memilih variabel target terbaik."""
    transformed_df, banner_note, audit_info = smart_transform_uploaded_dataframe(df)
    num_cols = [
        c for c in transformed_df.select_dtypes(include=[np.number]).columns
        if transformed_df[c].nunique() > 1 and not c.lower().endswith("_id")
    ]

    clean_df = pd.DataFrame()
    schema_info = {}
    primary_candidates = []
    secondary_candidates = []

    for c in num_cols:
        c_low = c.lower().strip()
        matched = None
        for entry in NATURAL_LEXICON:
            if re.search(entry[0], c_low):
                matched = entry
                break

        if matched:
            _, ui_label, phrase, verb_up, verb_down, unit, desc, role = matched
        else:
            ui_label = c.replace("_", " ").replace("-", " ").strip().title()
            phrase = ui_label.lower()
            verb_up = "meningkat naik"
            verb_down = "menurun"
            unit = ""
            desc = f"Variabel dengan nilai berkisar antara {fmt_num(transformed_df[c].min())} sampai {fmt_num(transformed_df[c].max())}"
            role = "target_utama" if any(w in c_low for w in ["target", "score", "skor", "profit", "laba", "hasil", "y"]) else "faktor"

        if ui_label in clean_df.columns:
            ui_label = f"{ui_label} ({c})"

        clean_df[ui_label] = pd.to_numeric(transformed_df[c], errors="coerce")
        schema_info[ui_label] = {
            "raw": c,
            "ui_label": ui_label,
            "phrase": phrase,
            "verb_up": verb_up,
            "verb_down": verb_down,
            "unit": unit,
            "description": desc,
            "role": role,
            "banner_note": banner_note,
        }

        if role == "target_utama":
            primary_candidates.append(ui_label)
        elif role == "target_kedua":
            secondary_candidates.append(ui_label)

    all_cols = list(clean_df.columns)
    if primary_candidates:
        auto_target = primary_candidates[0]
    elif secondary_candidates:
        auto_target = secondary_candidates[0]
    else:
        auto_target = all_cols[-1] if all_cols else ""

    return clean_df, schema_info, auto_target, audit_info


def try_load_local_olist() -> pd.DataFrame | None:
    root = Path(__file__).resolve().parent.parent.parent.parent
    raw_dir = root / "data" / "raw"
    orders_f = raw_dir / "olist_orders_dataset.csv"
    items_f = raw_dir / "olist_order_items_dataset.csv"
    reviews_f = raw_dir / "olist_order_reviews_dataset.csv"

    if orders_f.exists() and items_f.exists():
        orders = pd.read_csv(orders_f, nrows=25000)
        items = pd.read_csv(items_f, nrows=25000)
        agg = items.groupby("order_id", as_index=False).agg(price=("price", "sum"), freight_value=("freight_value", "sum"))
        merged = pd.merge(orders, agg, on="order_id", how="inner")
        if "order_delivered_customer_date" in merged.columns and "order_purchase_timestamp" in merged.columns:
            p_dt = pd.to_datetime(merged["order_purchase_timestamp"], errors="coerce")
            d_dt = pd.to_datetime(merged["order_delivered_customer_date"], errors="coerce")
            e_dt = pd.to_datetime(merged["order_estimated_delivery_date"], errors="coerce")
            merged["delivery_days"] = ((d_dt - p_dt).dt.total_seconds() / 86400.0).round(1)
            merged["delivery_delay"] = ((d_dt - e_dt).dt.total_seconds() / 86400.0).round(1)
        if reviews_f.exists():
            rev = pd.read_csv(reviews_f, usecols=["order_id", "review_score"], nrows=25000)
            merged = pd.merge(merged, rev, on="order_id", how="left")
        merged["freight_ratio"] = ((merged["freight_value"] / (merged["price"] + 1.0)) * 100.0).round(1)
        merged["payment_value"] = (merged["price"] + merged["freight_value"]).round(2)
        cols = [c for c in ["price", "freight_value", "freight_ratio", "delivery_days", "delivery_delay", "payment_value", "review_score"] if c in merged.columns]
        return merged[cols].dropna().reset_index(drop=True)
    return None


def get_builtin_dataset(name: str) -> pd.DataFrame:
    if name == "Kasus 1: Toko Online & Kepuasan Pembeli (Data Olist)":
        olist_df = try_load_local_olist()
        if olist_df is not None:
            return olist_df

    if name == "Kasus 2: Risiko Kesehatan & Gaya Hidup (Data Medis)":
        raw = load_diabetes(as_frame=True)
        return pd.DataFrame({
            "age": (raw.data["age"] * 150 + 48).round(0),
            "bmi": (raw.data["bmi"] * 50 + 26.5).round(1),
            "bp": (raw.data["bp"] * 120 + 95).round(0),
            "cholesterol": (raw.data["s1"] * 180 + 190).round(0),
            "ldl": (raw.data["s2"] * 150 + 115).round(0),
            "hdl": (raw.data["s3"] * 80 + 50).round(0),
            "glucose": (raw.data["s6"] * 110 + 92).round(0),
            "progresi_risiko": raw.target,
        })

    if name == "Kasus 3: Kualitas Produk & Komposisi Bahan (Data Mutu)":
        raw = load_wine(as_frame=True)
        df = raw.frame[["alcohol", "malic_acid", "flavanoids", "color_intensity", "proline", "target"]].copy()
        df.rename(columns={"target": "kelas_kualitas"}, inplace=True)
        df["kelas_kualitas"] = df["kelas_kualitas"] + 1
        return df

    rng = np.random.default_rng(42)
    n = 1500
    harga = rng.lognormal(mean=4.5, sigma=0.65, size=n).round(2)
    ongkir = (harga * rng.uniform(0.05, 0.35, size=n) + rng.normal(5, 2, size=n)).clip(2.0, 120.0).round(2)
    lama_kirim = rng.gamma(shape=2.5, scale=3.2, size=n).round(1)
    telat = (lama_kirim - rng.uniform(5, 11, size=n)).round(1)
    rasio = ((ongkir / (harga + 1.0)) * 100.0).round(1)
    skor_ulasan = np.clip(4.8 - 0.22 * np.maximum(0, telat) - 0.018 * rasio + rng.normal(0, 0.4, size=n), 1.0, 5.0).round(1)
    return pd.DataFrame({
        "price": harga, "freight_value": ongkir, "freight_ratio": rasio,
        "delivery_days": lama_kirim, "delivery_delay": telat,
        "payment_value": (harga + ongkir).round(2), "review_score": skor_ulasan,
    })


# Compatibility definitions for legacy modules
SEMANTIC_PATTERNS = {
    "target": [r"score", r"rating", r"target", r"label", r"close", r"hasil"],
    "freight_cost": [r"ongkir", r"freight", r"shipping"],
    "time_delay": [r"delay", r"telat", r"terlambat", r"hari"],
    "price_value": [r"harga", r"price", r"value", r"nilai"],
    "quantity": [r"count", r"jumlah", r"qty"],
    "identifier": [r"id$", r"_id$", r"^id_"],
}


def interpret_column_meaning(col_name: str, series: pd.Series | None = None) -> dict:
    matched = None
    col_low = col_name.lower().strip()
    for entry in NATURAL_LEXICON:
        if re.search(entry[0], col_low):
            matched = entry
            break
    cat = "price_value" if "price" in col_low else ("freight_cost" if "freight" in col_low else "target")
    label = matched[1] if matched else col_name.title()
    return {
        "column_name": col_name,
        "is_numeric": True,
        "semantic_category": cat,
        "human_label": label,
        "null_count": 0,
        "unique_count": 10,
    }


def build_semantic_schema(df: pd.DataFrame) -> dict:
    clean_df, schema_info, auto_target, audit_info = build_fluent_schema(df)
    return {
        "n_rows": len(df),
        "n_cols": len(df.columns),
        "numeric_columns": list(clean_df.columns),
        "categorical_columns": [],
        "recommended_target": auto_target,
    }

