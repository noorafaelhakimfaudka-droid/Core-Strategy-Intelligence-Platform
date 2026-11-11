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


# ==============================================================================
# 1. MULTI-DOMAIN NATURAL LEXICON (11 SEKTOR INDUSTRI UTAMA)
# Format: (regex_pattern, ui_label, subject_phrase, verb_when_up, verb_when_down, unit, description, role)
# ==============================================================================
NATURAL_LEXICON = [
    # 1. Pasar Keuangan, Bursa Saham & Kripto (OHLCV)
    (r"^close$|harga_penutupan|closing_price", "Harga Pasar", "harga penutupan aset di pasar", "menguat naik", "terkoreksi turun", "$", "Nilai penutupan aset di akhir periode perdagangan", "target_utama"),
    (r"return_harian|daily_return", "Untung/Rugi Harian", "imbal hasil harian", "mencetak untung", "mengalami koreksi", "%", "Persentase perubahan harga dibandingkan hari sebelumnya", "target_kedua"),
    (r"gejolak_harga|volatility|rentang_harian", "Gejolak Harian (High-Low)", "ayunan harga harian", "bergejolak lebar", "bergerak tenang", "$", "Selisih antara titik harga tertinggi dan terendah dalam sehari", "faktor"),
    (r"momentum_7h|ma7_gap", "Posisi vs Tren Mingguan", "jarak harga dari rata-rata mingguan", "melaju di atas rata-rata mingguan", "turun ke bawah rata-rata mingguan", "%", "Persentase selisih harga saat ini terhadap tren 7 hari terakhir", "faktor"),
    (r"momentum_30h|ma30_gap", "Posisi vs Tren Bulanan", "jarak harga dari tren bulanan", "menembus ke atas garis tren bulanan", "melemah di bawah garis tren bulanan", "%", "Persentase selisih harga saat ini terhadap rata-rata 30 hari", "faktor"),
    (r"tekanan_beli|candle_body", "Dorongan Beli vs Jual", "tekanan transaksi harian", "didominasi akumulasi beli", "ditekan aksi jual", "%", "Perbandingan kekuatan dorongan pembeli melawan penjual", "faktor"),
    (r"^volume$|nilai_transaksi_pasar", "Volume Transaksi Pasar", "aktivitas transaksi di pasar", "melonjak ramai", "menyusut sepi", "", "Total nilai atau jumlah perpindahan aset yang diperdagangkan", "faktor"),

    # 2. Keuangan Bisnis, Akuntansi & Perbankan Umum
    (r"profit|laba_bersih|net_income|keuntungan", "Laba Bersih", "laba bersih usaha", "bertumbuh meningkat", "menyusut turun", "Rp", "Total sisa keuntungan bersih operasional setelah dipotong seluruh beban", "target_utama"),
    (r"revenue|omset|omzet|pendapatan_total|sales_amount", "Total Pendapatan", "total arus pendapatan usaha", "bertumbuh melonjak", "mengalami penurunan", "Rp", "Total penerimaan kotor dari seluruh lini aktivitas bisnis", "target_utama"),
    (r"biaya_operasional|operational_cost|opex|expenses", "Biaya Operasional", "beban pengeluaran usaha", "membengkak naik", "berhasil dihemat turun", "Rp", "Pengeluaran rutin yang dikeluarkan untuk menjalankan aktivitas operasional", "faktor"),
    (r"cogs|beban_pokok|hpp|biaya_produksi", "Harga Pokok Penjualan", "beban pokok produksi", "membengkak mahal", "lebih efisien ditekan", "Rp", "Total biaya bahan baku dan tenaga kerja langsung untuk menghasilkan produk", "faktor"),
    (r"gross_margin|margin_kotor|profit_margin", "Margin Keuntungan", "margin keuntungan bisnis", "melebar menguntungkan", "menipis tergerus", "%", "Persentase selisih pendapatan terhadap biaya pokok", "target_kedua"),
    (r"tax|pajak|beban_pajak", "Beban Pajak", "kewajiban setor pajak", "meningkat", "lebih hemat", "Rp", "Kewajiban pajak yang harus disetor sesuai ketentuan", "faktor"),
    (r"cash_flow|arus_kas", "Arus Kas Bersih", "arus kas operasional", "mengalir surplus", "mengalami defisit", "Rp", "Selisih likuiditas kas masuk dibanding kas keluar", "target_kedua"),
    (r"loan_amount|jumlah_pinjaman|plafon_kredit", "Plafon Pinjaman", "nilai pengajuan pinjaman", "diambil lebih besar", "diajukan lebih terukur", "Rp", "Besaran kredit dana yang disalurkan kepada nasabah", "faktor"),
    (r"interest_rate|bunga_pinjaman|suku_bunga", "Suku Bunga", "beban suku bunga tahunan", "naik memberatkan", "turun bersahabat", "%", "Persentase tarif bunga pinjaman atau pembiayaan", "faktor"),

    # 3. E-Commerce, Ritel & Toko Online
    (r"review_score|skor_kepuasan|rating|satisfaction", "Kepuasan Pembeli", "tingkat kepuasan pembeli", "meningkat puas", "merosot kecewa", "poin", "Penilaian ulasan pelanggan dari skala 1 sampai 5", "target_utama"),
    (r"payment_value|total_belanja|nilai_belanja", "Nilai Belanja", "total nilai belanja", "bertumbuh besar", "menyusut turun", "", "Total uang yang dibayarkan pelanggan dalam satu transaksi", "target_kedua"),
    (r"price|harga_barang|unit_price", "Harga Barang", "harga jual produk", "dipasang lebih tinggi", "dibuat lebih terjangkau", "", "Harga murni produk sebelum ditambah biaya pengiriman", "faktor"),
    (r"freight_value|ongkir|shipping", "Ongkos Kirim", "biaya ongkos kirim", "bertambah mahal", "lebih hemat", "", "Tarif pengiriman yang ditanggung oleh pembeli", "faktor"),
    (r"freight_ratio|rasio_ongkir", "Beban Ongkir vs Harga", "porsi ongkir terhadap harga barang", "terasa memberatkan pembeli", "terasa ringan di kantong", "%", "Persentase perbandingan ongkir terhadap harga produk", "faktor"),
    (r"delivery_delay|keterlambatan|telat", "Keterlambatan Kirim", "jadwal pengiriman paket", "molor melewati estimasi", "tiba lebih cepat dari janji", "hari", "Selisih hari barang sampai dibanding janji awal (positif = telat)", "faktor"),
    (r"delivery_days|lama_kirim|waktu_tunggu", "Lama Pengiriman", "durasi tunggu pengiriman", "memakan waktu lama", "sampai lebih cepat", "hari", "Total hari tunggu sejak pesanan dibuat hingga diterima", "faktor"),
    (r"installment|cicilan", "Tenor Cicilan", "pilihan tenor cicilan", "diambil makin panjang", "dibayar lebih singkat", "kali", "Jumlah tahapan pembayaran cicilan oleh pembeli", "faktor"),
    (r"discount|diskon|potongan_harga", "Diskon Produk", "besaran potongan harga", "diberikan lebih royal", "dipangkas hemat", "%", "Persentase pengurangan harga normal produk untuk memikat pembeli", "faktor"),

    # 4. SDM, Manajemen Tenaga Kerja & Human Resources (HR)
    (r"salary|gaji|income|upah_karyawan", "Gaji Karyawan", "tingkat kompensasi gaji", "meningkat sejahtera", "berada di bawah pasar", "Rp", "Besaran imbalan gaji pokok dan tunjangan rutin karyawan", "target_utama"),
    (r"tenure|masa_kerja|lama_bekerja", "Masa Kerja", "lama pengabdian kerja", "bertambah loyal", "tergolong karyawan baru", "tahun", "Lama waktu seorang pegawai telah bergabung dalam organisasi", "faktor"),
    (r"working_hours|jam_kerja|overtime|lembur", "Jam Kerja Mingguan", "alokasi beban waktu kerja", "membengkak lembur", "terjaga seimbang", "jam", "Jumlah jam kerja aktual yang dihabiskan karyawan per pekan", "faktor"),
    (r"employee_satisfaction|kepuasan_karyawan|morale", "Kepuasan Karyawan", "indeks kepuasan kerja internal", "tumbuh termotivasi", "merosot jenuh", "poin", "Hasil survei kenyamanan dan loyalitas tim dalam lingkungan kerja", "target_kedua"),
    (r"performance_score|skor_kinerja|evaluasi", "Skor Kinerja", "pencapaian target KPI", "melampaui target", "di bawah ekspektasi", "poin", "Nilai penilaian performa berkala yang dicapai karyawan", "target_utama"),
    (r"absenteeism|absensi|jumlah_absen", "Hari Absensi", "tingkat ketidakhadiran kerja", "meningkat sering bolos", "terjaga disiplin hadir", "hari", "Total hari izin atau mangkir kerja dalam periode setahun", "faktor"),
    (r"training_hours|jam_pelatihan", "Waktu Pelatihan", "durasi pengasahan kompetensi", "diikuti intensif", "sangat minim", "jam", "Jumlah jam pelatihan pengembangan keterampilan yang diselesaikan", "faktor"),

    # 5. Pemasaran Digital, Periklanan & Retensi Pelanggan
    (r"conversion_rate|cvr|tingkat_konversi", "Tingkat Konversi", "efektivitas penutupan transaksi", "melonjak produktif", "tersendat rendah", "%", "Persentase pengunjung yang sukses melakukan transaksi atau aksi target", "target_utama"),
    (r"click_through_rate|ctr|rasio_klik", "Rasio Klik (CTR)", "daya tarik promosi", "memikat klik tinggi", "diabaikan sepi", "%", "Perbandingan jumlah klik terhadap total impresi tayangan", "faktor"),
    (r"clicks|jumlah_klik", "Jumlah Klik", "volume interaksi klik", "membanjir masuk", "menyusut sepi", "kali", "Total klik pengunjung terhadap tautan atau materi promosi", "faktor"),
    (r"impressions|tayangan_iklan", "Tayangan Iklan", "jangkauan eksposur materi", "meluas masif", "terbatas sempit", "kali", "Berapa kali materi promosi tampil di hadapan target audiens", "faktor"),
    (r"cac|acquisition_cost|biaya_akuisisi", "Biaya Akuisisi (CAC)", "biaya perolehan pelanggan baru", "membengkak boros", "berhasil hemat efisien", "Rp", "Uang pemasaran yang harus dibakar untuk mendatangkan satu pelanggan aktif", "faktor"),
    (r"churn_rate|tingkat_churn|batal_langganan", "Tingkat Churn", "laju kehilangan pelanggan", "membengkak kabur", "tertahan setia", "%", "Persentase pelanggan yang menghentikan kerja sama atau langganan", "target_utama"),
    (r"retention_rate|tingkat_retensi", "Tingkat Retensi", "daya lekat pelanggan", "makin awet setia", "mulai memudar", "%", "Persentase pelanggan yang terus aktif memperpanjang layanan", "target_utama"),

    # 6. Properti, Bangunan & Real Estate
    (r"house_price|property_price|harga_properti|harga_rumah", "Harga Properti", "nilai pasar properti", "melonjak tinggi", "terkoreksi terjangkau", "Rp", "Estimasi harga jual wajar unit rumah atau tanah di pasar", "target_utama"),
    (r"building_area|luas_bangunan|sqft_living|area_m2", "Luas Bangunan", "kapasitas ruang fisik bangunan", "lebih lapang lega", "berdimensi kompak", "m²", "Total luas lantai indoor yang dapat dimanfaatkan penghuni", "faktor"),
    (r"land_area|luas_tanah|lot_size", "Luas Tanah", "kavling tanah pekarangan", "sangat luas terbentang", "berukuran minimalis", "m²", "Luas keseluruhan bidang tapak tanah properti", "faktor"),
    (r"bedrooms|kamar_tidur|jumlah_kamar", "Kamar Tidur", "ketersediaan ruang tidur", "berjumlah banyak", "terbatas sedikit", "unit", "Jumlah ruangan kamar tidur yang tersedia di dalam unit", "faktor"),
    (r"bathrooms|kamar_mandi", "Kamar Mandi", "fasilitas sanitasi unit", "berlimpah lengkap", "terbatas minim", "unit", "Total kamar mandi yang terpasang di properti", "faktor"),
    (r"house_age|usia_bangunan|tahun_dibangun", "Usia Bangunan", "ketahanan umur fisik aset", "makin berumur tua", "tergolong gres baru", "tahun", "Hitungan berapa tahun gedung telah berdiri sejak masa konstruksi", "faktor"),
    (r"distance_to_center|jarak_pusat_kota|jarak_stasiun", "Jarak ke Pusat Kota", "aksesibilitas mobilitas harian", "makin jauh ke pinggiran", "sangat dekat strategis", "km", "Jarak fisik properti menuju pusat fasilitas umum terdekat", "faktor"),

    # 7. Logistik, Rantai Pasok & Transportasi
    (r"distance|jarak_tempuh|jarak_km", "Jarak Tempuh", "bentang lintasan ekspedisi", "membentang jauh", "berjarak dekat", "km", "Total kilometer yang harus ditempuh armada pengiriman", "faktor"),
    (r"transit_time|waktu_tempuh|travel_time", "Waktu Tempuh", "durasi laju pengiriman", "memakan waktu lama", "tiba cepat kilat", "jam", "Total jam yang dibutuhkan armada dari titik muat ke titik bongkar", "faktor"),
    (r"fuel_consumption|konsumsi_bbm|bensin", "Konsumsi Bahan Bakar", "kehausan bahan bakar armada", "membengkak boros", "terkendali irit", "liter", "Volume liter bbm yang terbakar untuk menyelesaikan satu rute", "faktor"),
    (r"payload_weight|berat_muatan|cargo_weight", "Bobot Muatan", "beban tonase kargo", "bermuatan berat penuh", "bermuatan ringan", "kg", "Berat total barang yang diangkut oleh unit kendaraan", "faktor"),

    # 8. Manufaktur, Mesin, Sensor & IoT
    (r"temperature|suhu_mesin|temp_c", "Suhu Operasional", "suhu panas komponen mesin", "memanas ekstrem", "terjaga dingin stabil", "°C", "Derajat suhu panas yang terekam pada sensor kerja perangkat", "faktor"),
    (r"pressure|tekanan_pipa|psi|bar", "Tekanan Hidrolik/Pipa", "daya dorong fluida/tekanan", "menekan tinggi", "melemah kendur", "psi", "Kekuatan tekanan pada sistem sirkulasi mesin produksi", "faktor"),
    (r"vibration|getaran_mesin|amplitudo", "Getaran Mesin", "stabilitas mekanik rotasi", "bergetar janggal kencang", "berputar halus stabil", "Hz", "Frekuensi getaran sensor poros perputaran mesin", "faktor"),
    (r"power_consumption|daya_listrik|watt|kwh", "Konsumsi Daya Listrik", "penggunaan energi listrik", "menyedot daya besar", "hemat energi", "kWh", "Daya listrik yang diserap lini manufaktur dalam beroperasi", "faktor"),
    (r"defect_rate|tingkat_cacat|reject_ratio", "Tingkat Produk Cacat", "kegagalan standar mutu", "membengkak banyak cacat", "sempurna nol cacat", "%", "Persentase barang yang gagal lolos kontrol kualitas (QC)", "target_utama"),
    (r"machine_downtime|waktu_rusak|jam_mogok", "Waktu Kerusakan Mesin", "gangguan mogok operasional", "terbengkalai macet lama", "berjalan lancar prima", "jam", "Durasi mesin terhenti akibat kerusakan komponen yang tidak terencana", "faktor"),

    # 9. Kesehatan, Medis & Gaya Hidup
    (r"progresi_risiko|risiko_kesehatan|disease", "Risiko Keparahan", "indeks risiko kesehatan", "memburuk naik", "lebih terkendali", "poin", "Tingkat perkembangan risiko penyakit pasien", "target_utama"),
    (r"^bmi$|berat_badan", "Indeks Massa Tubuh (BMI)", "indeks massa tubuh", "meningkat berlebih", "mendekati batas ideal", "poin", "Rasio berat badan terhadap tinggi badan", "faktor"),
    (r"^bp$|tekanan_darah", "Tekanan Darah", "tekanan darah arteri", "meninggi", "lebih stabil", "mmHg", "Rata-rata tekanan darah pasien", "faktor"),
    (r"glucose|gula_darah|^s6$", "Kadar Gula Darah", "kadar gula darah", "melonjak tinggi", "lebih terkontrol", "mg/dL", "Tingkat glukosa di dalam aliran darah", "faktor"),
    (r"cholesterol|kolesterol|^s1$", "Kolesterol Total", "kadar kolesterol total", "meningkat", "menurun", "mg/dL", "Total kandungan kolesterol darah", "faktor"),
    (r"^ldl$|^s2$", "Kolesterol Jahat (LDL)", "kolesterol jahat (LDL)", "menumpuk tinggi", "berkurang turun", "mg/dL", "Lemak pemicu penyempitan pembuluh darah", "faktor"),
    (r"^hdl$|^s3$", "Kolesterol Baik (HDL)", "kolesterol pelindung (HDL)", "bertambah tinggi", "menurun", "mg/dL", "Lemak baik pembersih pembuluh darah", "faktor"),
    (r"^age$|umur|usia", "Usia", "kelompok usia", "bertambah senior", "lebih muda", "tahun", "Umur subjek yang tercatat di data", "faktor"),

    # 10. Mutu Produk, Bahan Kimia & Komposisi
    (r"kelas_kualitas|quality|mutu|grade", "Mutu Produk", "peringkat mutu produk", "naik ke level premium", "turun kelas", "poin", "Tingkat kualitas akhir produk dari hasil uji laboratorium", "target_utama"),
    (r"flavanoids|flavonoid", "Kadar Flavonoid", "kandungan antioksidan flavonoid", "makin kaya", "makin rendah", "poin", "Senyawa alami penentu kualitas rasa dan daya simpan", "faktor"),
    (r"alcohol|alkohol", "Kadar Alkohol", "kandungan alkohol", "meningkat", "menurun", "%", "Persentase kadar alkohol dalam komposisi bahan", "faktor"),
    (r"color_intensity|warna", "Kepekatan Warna", "kepekatan warna produk", "tampil makin pekat", "terlihat lebih pucat", "poin", "Tingkat kecerahan dan kepekatan visual", "faktor"),
    (r"malic_acid|asam", "Tingkat Keasaman", "kadar asam alami", "terasa makin asam", "terasa lebih lembut", "poin", "Tingkat keasaman malat pada bahan baku", "faktor"),
    (r"proline", "Kadar Proline", "kandungan asam amino proline", "meningkat tinggi", "menurun", "mg", "Indikator kematangan bahan baku utama", "faktor"),

    # 11. Edukasi, Akademik & Kemahasiswaan
    (r"exam_score|nilai_ujian|final_score|gpa|ipk", "Nilai Kelulusan / IPK", "skor evaluasi kelulusan", "meraih nilai tinggi", "anjlok di bawah batas", "poin", "Indeks prestasi kumulatif atau nilai evaluasi ujian akhir", "target_utama"),
    (r"study_hours|jam_belajar|study_time", "Jam Belajar Mandiri", "intensitas belajar materi", "tekun bertambah lama", "sangat minim membaca", "jam", "Total jam belajar mandiri mingguan di luar jam tatap muka", "faktor"),
    (r"attendance_rate|kehadiran_kelas|presensi", "Tingkat Kehadiran", "disiplin kehadiran kelas", "hadir penuh konsisten", "sering absen bolos", "%", "Persentase kehadiran tatap muka dalam sesi pembelajaran", "faktor"),
]


# ==============================================================================
# 2. ZERO-SHOT DYNAMIC SEMANTIC INFERENCE (UNTUK KOLOM APA SAJA)
# ==============================================================================
def infer_dynamic_semantics(c: str, s: pd.Series) -> tuple[str, str, str, str, str, str, str]:
    """
    [UK-01, UK-02] Inferensi semantik otomatis untuk kolom apa saja di luar kamus statis.
    Mendeduksi: ui_label, phrase, verb_up, verb_down, unit, description, dan role secara cerdas.
    """
    c_clean = c.replace("_", " ").replace("-", " ").strip()
    ui_label = c_clean.title()
    phrase = ui_label.lower()
    c_low = c.lower().strip()

    # 1. Infer Unit (Satuan) Berbasis Kata Kunci & Karakteristik Data
    unit = ""
    if any(k in c_low for k in ["pct", "percent", "persen", "ratio", "rasio", "rate", "tingkat", "margin", "share", "yield", "prob"]):
        unit = "%"
    elif any(k in c_low for k in ["_rp", "rupiah", "idr", "gaji", "omzet", "biaya", "tarif", "ongkos", "tagihan", "modal", "upah"]):
        unit = "Rp"
    elif any(k in c_low for k in ["usd", "dollar", "eur", "gbp", "price_usd", "cost_usd", "revenue_usd", "wage"]):
        unit = "$"
    elif any(k in c_low for k in ["hari", "day", "days", "lama_", "durasi_hari", "tenure_days"]):
        unit = "hari"
    elif any(k in c_low for k in ["jam", "hour", "hours", "durasi_jam", "overtime"]):
        unit = "jam"
    elif any(k in c_low for k in ["bulan", "month", "months", "tenure_months"]):
        unit = "bulan"
    elif any(k in c_low for k in ["tahun", "year", "years", "age", "umur", "usia"]):
        unit = "tahun"
    elif any(k in c_low for k in ["detik", "second", "sec", "latency"]):
        unit = "detik"
    elif any(k in c_low for k in ["kg", "kilogram", "berat", "weight"]):
        unit = "kg"
    elif any(k in c_low for k in ["gram", "gr"]):
        unit = "g"
    elif any(k in c_low for k in ["km", "kilometer", "jarak", "distance", "mile"]):
        unit = "km"
    elif any(k in c_low for k in ["meter", "tinggi", "panjang", "depth", "width"]):
        unit = "m"
    elif any(k in c_low for k in ["sqft", "luas", "area", "lot_size"]):
        unit = "m²"
    elif any(k in c_low for k in ["celsius", "suhu", "temp", "temperature"]):
        unit = "°C"
    elif pd.api.types.is_integer_dtype(s) and s.min() >= 0 and any(k in c_low for k in ["count", "total", "jumlah", "qty", "pesanan", "order", "frekuensi", "kali", "transaksi", "item"]):
        unit = "kali" if any(k in c_low for k in ["kali", "frekuensi"]) else "unit"
    elif s.min() >= 0.0 and s.max() <= 1.0 and s.nunique() > 2:
        unit = "%"

    # 2. Infer Polarity & Verbs (Arah Aksi & Dampak)
    neg_keywords = [
        "biaya", "cost", "expense", "loss", "rugi", "churn", "telat", "delay", "error",
        "cacat", "defect", "komplain", "complaint", "risiko", "risk", "downtime", "utang",
        "debt", "pajak", "tax", "keparahan", "drop", "fail", "cancellation", "batal"
    ]
    pos_keywords = [
        "profit", "laba", "untung", "revenue", "omzet", "pendapatan", "sales", "penjualan",
        "kepuasan", "satisfaction", "rating", "skor", "score", "retensi", "retention",
        "gaji", "salary", "efisiensi", "efficiency", "akurasi", "accuracy", "growth",
        "kualitas", "quality", "keuntungan", "margin", "bonus", "nilai", "grade"
    ]

    if any(k in c_low for k in neg_keywords):
        verb_up = "membengkak naik"
        verb_down = "berhasil ditekan turun"
    elif any(k in c_low for k in pos_keywords):
        verb_up = "meningkat naik"
        verb_down = "menurun berkurang"
    else:
        verb_up = "bergerak naik"
        verb_down = "bergerak turun"

    # 3. Infer Role (Target Utama vs Faktor Penentu)
    target_keywords = [
        "target", "label", "outcome", "y", "close", "price", "harga", "profit", "laba",
        "sales", "penjualan", "omzet", "revenue", "churn", "gaji", "salary", "score",
        "skor", "rating", "quality", "mutu", "result", "status", "risiko", "biaya", "cost"
    ]
    if any(k == c_low or k in c_low for k in target_keywords):
        role = "target_utama"
    else:
        role = "faktor"

    # 4. Dynamic Data-Driven Description
    s_clean = s.dropna()
    c_min = float(s_clean.min()) if len(s_clean) > 0 else 0.0
    c_max = float(s_clean.max()) if len(s_clean) > 0 else 0.0
    c_med = float(s_clean.median()) if len(s_clean) > 0 else 0.0
    u_str = f" {unit}".rstrip() if unit not in ("Rp", "$") else ""
    pfx = unit if unit in ("Rp", "$") else ""

    desc = (
        f"variabel data dengan sebaran nilai antara {pfx}{fmt_num(c_min)}{u_str} hingga "
        f"{pfx}{fmt_num(c_max)}{u_str} (median {pfx}{fmt_num(c_med)}{u_str})."
    )

    return ui_label, phrase, verb_up, verb_down, unit, desc, role


# ==============================================================================
# 3. SMART DATA TRANSFORMATION & SCHEMA PROFILER
# ==============================================================================
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
            ui_label, phrase, verb_up, verb_down, unit, desc, role = infer_dynamic_semantics(c, transformed_df[c])

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


# ==============================================================================
# 4. BUILT-IN DATASETS & BACKWARD COMPATIBILITY
# ==============================================================================
def try_load_local_olist() -> pd.DataFrame | None:
    root = Path(__file__).resolve().parent.parent.parent.parent
    raw_dir = root / "data" / "raw"
    orders_f = raw_dir / "olist_orders_dataset.csv"
    items_f = raw_dir / "olist_order_items_dataset.csv"
    reviews_f = raw_dir / "olist_order_reviews_dataset.csv"

    if orders_f.exists() and items_f.exists() and reviews_f.exists():
        try:
            ord_df = pd.read_csv(orders_f, usecols=["order_id", "order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"])
            it_df = pd.read_csv(items_f, usecols=["order_id", "price", "freight_value"])
            rev_df = pd.read_csv(reviews_f, usecols=["order_id", "review_score"])

            it_agg = it_df.groupby("order_id").agg({"price": "sum", "freight_value": "sum"}).reset_index()
            rev_agg = rev_df.groupby("order_id")["review_score"].mean().reset_index()

            merged = ord_df.merge(it_agg, on="order_id", how="inner").merge(rev_agg, on="order_id", how="inner")
            merged["delivery_days"] = (pd.to_datetime(merged["order_delivered_customer_date"]) - pd.to_datetime(merged["order_purchase_timestamp"])).dt.total_seconds() / 86400.0
            merged["delivery_delay"] = (pd.to_datetime(merged["order_delivered_customer_date"]) - pd.to_datetime(merged["order_estimated_delivery_date"])).dt.total_seconds() / 86400.0
            merged["freight_ratio"] = ((merged["freight_value"] / (merged["price"] + 1e-9)) * 100.0).round(1)
            merged["payment_value"] = (merged["price"] + merged["freight_value"]).round(2)

            sub = merged[["price", "freight_value", "freight_ratio", "delivery_days", "delivery_delay", "payment_value", "review_score"]].dropna()
            if len(sub) > 500:
                return sub.sample(n=min(len(sub), 3500), random_state=42).reset_index(drop=True)
        except Exception:
            pass
    return None


def get_builtin_dataset(name: str) -> pd.DataFrame:
    if name == "Kasus 1: Toko Online & Kepuasan Pembeli (Data Olist)":
        olist_df = try_load_local_olist()
        if olist_df is not None:
            return olist_df

    elif name == "Kasus 2: Risiko Kesehatan & Gaya Hidup (Data Medis)":
        d = load_diabetes(as_frame=True)
        df = d.frame.copy()
        df = df.rename(columns={
            "target": "progresi_risiko", "bmi": "berat_badan", "bp": "tekanan_darah",
            "s1": "kolesterol", "s2": "ldl", "s3": "hdl", "s6": "glukosa",
        })
        return df

    elif name == "Kasus 3: Kualitas Produk & Komposisi Bahan (Data Mutu)":
        w = load_wine(as_frame=True)
        df = w.frame.copy()
        df["target"] = (df["target"] + 1.0).astype(float)
        df = df.rename(columns={
            "target": "kelas_kualitas", "color_intensity": "warna",
            "flavanoids": "flavonoid", "alcohol": "alkohol",
        })
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
    "target": [r"score", r"rating", r"target", r"label", r"close", r"hasil", r"profit", r"revenue"],
    "freight_cost": [r"ongkir", r"freight", r"shipping"],
    "time_delay": [r"delay", r"telat", r"terlambat", r"hari"],
    "price_value": [r"harga", r"price", r"value", r"nilai"],
    "quantity": [r"count", r"jumlah", r"qty"],
    "identifier": [r"id$", r"_id$", r"^id_"],
}


def interpret_column_meaning(col_name: str, series: pd.Series | None = None) -> dict:
    col_low = col_name.lower().strip()
    matched = None
    for entry in NATURAL_LEXICON:
        if re.search(entry[0], col_low):
            matched = entry
            break

    if matched:
        label = matched[1]
        cat = "target" if matched[7].startswith("target") else "price_value"
    else:
        dummy_series = series if series is not None else pd.Series([1.0, 2.0, 3.0])
        ui_label, _, _, _, _, _, role = infer_dynamic_semantics(col_name, dummy_series)
        label = ui_label
        cat = "target" if role.startswith("target") else "price_value"

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
