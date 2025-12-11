# DATABASE SISTEM PAKAR DIAGNOSA SMARTPHONE (EXPANDED VERSION)

# 1. DAFTAR GEJALA (Codes)
gejala_data = {
    # MASALAH DAYA & BATERAI
    'G01': 'Baterai cepat habis / Boros tidak wajar',
    'G02': 'Persentase baterai loncat-loncat (misal 40% ke 10%)',
    'G03': 'HP mati sendiri di persentase tertentu (misal 20% mati)',
    'G04': 'HP panas berlebihan (Overheat) di area mesin belakang',
    'G05': 'HP panas hanya saat di-charge',
    'G06': 'Tidak bisa nge-charge (Masuk tapi persentase tidak naik)',
    'G07': 'Cas lambat sekali (Slow charging) padahal adaptor ori',
    
    # MASALAH LAYAR & FISIK
    'G08': 'Layar menyentuh sendiri (Ghost Touch)',
    'G09': 'Layar ada garis warna-warni / tompel hitam / bintik putih',
    'G10': 'Layar gelap total tapi ada suara notifikasi/telepon',
    'G11': 'Kaca depan retak tapi gambar normal',
    'G12': 'Layar berkedip-kedip (Flickering) saat brightness rendah',

    # MASALAH SINYAL & KONEKSI
    'G13': 'Tidak ada sinyal (No Service) padahal kartu SIM terbaca',
    'G14': 'Sinyal 4G/5G hilang timbul tidak stabil',
    'G15': 'Wi-Fi tidak bisa ON (Tombol abu-abu / Grayed out)',
    'G16': 'Bluetooth tidak bisa connect / sering putus',
    'G17': 'GPS tidak akurat / Sering searching signal',

    # MASALAH AUDIO
    'G18': 'Suara speaker musik pecah / sember',
    'G19': 'Suara lawan bicara tidak terdengar (Earpiece mati)',
    'G20': 'Lawan bicara tidak bisa mendengar suara kita (Mic mati)',
    'G21': 'Mode headset aktif terus padahal tidak colok headset',

    # MASALAH KAMERA & SENSOR
    'G22': 'Kamera gagal fokus / Blur / Getar sendiri',
    'G23': 'Aplikasi kamera error / Blank hitam saat dibuka',
    'G24': 'Flash kamera tidak menyala',
    'G25': 'Face ID / Fingerprint tidak berfungsi',
    'G26': 'Layar tidak mati saat telepon ditempel ke kuping (Proximity)',

    # MASALAH SISTEM & MESIN
    'G27': 'Stuck di Logo (Bootloop) tidak masuk menu',
    'G28': 'Sering Restart sendiri (Random Reboot)',
    'G29': 'HP Lambat / Sering Hang (Freeze) saat buka aplikasi',
    'G30': 'HP pernah terkena air / Jatuh ke air sebelumnya'
}

# 2. ATURAN DIAGNOSA (Rules)
# Format: 'Nama Kerusakan': [List Kode Gejala]
# Semakin banyak gejala yang cocok, semakin tinggi akurasinya.
rules_data = {
    # KATEGORI: BATERAI & CHARGING
    'Baterai Health Drop / Bocor': ['G01', 'G02', 'G03'],
    'Konektor Charger / Port USB Rusak': ['G06', 'G07', 'G21'],
    'IC Charger Rusak (Logic Charging)': ['G05', 'G06', 'G04'],
    
    # KATEGORI: LAYAR (LCD)
    'LCD Panel Rusak (Wajib Ganti 1 Set)': ['G09', 'G10', 'G12'],
    'Touchscreen Error / Digitizer': ['G08'],
    'Kaca Depan Pecah (Bisa Glass Only)': ['G11'],
    'Masalah Flexible LCD (Loose Connection)': ['G10', 'G12'],

    # KATEGORI: SINYAL (RF)
    'IC Baseband / WTR (Masalah Sinyal Berat)': ['G13', 'G14', 'G04'],
    'Masalah Antena / Kabel Sinyal': ['G14', 'G17'],
    'Modul Wi-Fi / Bluetooth Rusak': ['G15', 'G16', 'G17'],

    # KATEGORI: MESIN UTAMA (MOTHERBOARD)
    'IC Power Bermasalah (Urgent)': ['G01', 'G04', 'G28', 'G03'],
    'EMMC / UFS (Memory Internal) Dying': ['G27', 'G28', 'G29'],
    'CPU Overheat / Dry Joint': ['G04', 'G28', 'G29'],
    'Korsleting Jalur VBAT (Short Circuit)': ['G30', 'G04', 'G01'],

    # KATEGORI: FITUR LAIN
    'Modul Kamera Rusak (OIS Fail)': ['G22', 'G23'],
    'Flexible Kamera Putus / Lepas': ['G23', 'G24'],
    'Kerusakan Microphone Bawah': ['G20'],
    'Kerusakan Speaker Earpiece (Atas)': ['G19', 'G26'],
    'Masalah Sensor Proximity': ['G26'],
    'IC Audio / Codec Audio Rusak': ['G18', 'G20', 'G21']
}

# 3. SOLUSI & SARAN PERBAIKAN
solusi_data = {
    'Baterai Health Drop / Bocor': 'Ganti unit baterai dengan yang original. Hindari penggunaan powerbank kualitas rendah.',
    'Konektor Charger / Port USB Rusak': 'Bersihkan lubang charger dari debu. Jika tetap tidak bisa, ganti port USB (Papan Cas Bawah).',
    'IC Charger Rusak (Logic Charging)': 'Perlu perbaikan mesin (Microsoldering). IC Charging gagal mengatur arus masuk.',
    'LCD Panel Rusak (Wajib Ganti 1 Set)': 'Pixel atau jalur LCD sudah pecah. Harus ganti LCD satu set full.',
    'Touchscreen Error / Digitizer': 'Jika LCD masih bagus, bisa coba ganti kaca touchscreen saja (hanya di teknisi ahli). Jika tidak, ganti satu set.',
    'Kaca Depan Pecah (Bisa Glass Only)': 'Kabar baik, LCD dalam masih aman. Bisa repair kaca saja (Glass Replacement) biaya lebih murah dari ganti LCD.',
    'Masalah Flexible LCD (Loose Connection)': 'Kemungkinan soket LCD kendor akibat jatuh. Coba bongkar dan pasang ulang soket LCD.',
    'IC Baseband / WTR (Masalah Sinyal Berat)': 'Kerusakan berat pada modem sinyal HP (IC WTR/Transceiver). Perlu teknisi hardware jam terbang tinggi.',
    'Masalah Antena / Kabel Sinyal': 'Cek kabel antena yang menghubungkan mesin atas dan bawah. Mungkin lepas atau putus.',
    'Modul Wi-Fi / Bluetooth Rusak': 'IC Wi-Fi bermasalah. Sering terjadi pada iPhone (IC Wi-Fi) atau Android panas.',
    'IC Power Bermasalah (Urgent)': 'Jantung kelistrikan HP bermasalah. Segera servis sebelum HP mati total permanen.',
    'EMMC / UFS (Memory Internal) Dying': 'Gejala usia pakai memori habis (Wear out). Segera BACKUP DATA. Ganti IC EMMC atau ganti HP baru.',
    'CPU Overheat / Dry Joint': 'Timah di bawah CPU retak (biasanya karena panas buat game). Perlu Reballing CPU (Risiko tinggi).',
    'Korsleting Jalur VBAT (Short Circuit)': 'Ada jalur positif dan negatif bertemu, biasanya karena air. Cuci mesin dengan ultrasonic cleaner segera.',
    'Modul Kamera Rusak (OIS Fail)': 'Stabilizer lensa rusak (sering karena getaran motor/jatuh). Harus ganti modul kamera baru.',
    'Flexible Kamera Putus / Lepas': 'Coba copot pasang soket kamera. Jika masih blank, ganti kamera.',
    'Kerusakan Microphone Bawah': 'Cek lubang mic, bersihkan dari debu. Jika tidak bisa, ganti board bawah satu set.',
    'Kerusakan Speaker Earpiece (Atas)': 'Ganti speaker kuping. Murah dan mudah.',
    'Masalah Sensor Proximity': 'Biasanya tertutup anti gores atau debu. Bersihkan area atas layar.',
    'IC Audio / Codec Audio Rusak': 'Penyakit umum (sering di iPhone 7/Audio Disease). Perlu jumper jalur IC Audio.'
}