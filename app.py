import streamlit as st
from knowledge_base import gejala_data, rules_data, solusi_data

def main():
    st.set_page_config(page_title="Sistem Pakar HP", page_icon="🔧", layout="centered")
    
    # --- HEADER ---
    st.title("🔧 Dr. Gadget: Diagnosa Kerusakan")
    st.write("Sistem Pakar Deteksi Dini Kerusakan Smartphone")
    
    with st.sidebar:
        st.header("Tentang Sistem")
        st.info("Aplikasi ini mendeteksi kerusakan berdasarkan pola gejala (Forward Chaining).")
        st.warning("Disclaimer: Hasil hanya prediksi. Konsultasikan dengan teknisi asli.")

    st.markdown("---")
    st.subheader("Apa keluhan HP kamu?")
    st.caption("Silakan buka kategori di bawah dan centang gejala yang sesuai.")

    # --- INPUT USER (Dikelompokkan biar rapi di HP) ---
    selected_gejala = []

    # Fungsi helper untuk membuat checkbox per kategori
    def buat_checkbox(judul_kategori, range_kode_awal, range_kode_akhir):
        with st.expander(judul_kategori):
            # Loop data, ambil hanya yang kodenya sesuai range
            # Kita asumsi kode berurut G01, G02, dst.
            for kode, deskripsi in gejala_data.items():
                # Trik sederhana cek range string
                # Misalnya G01 sampai G07 untuk Baterai
                try:
                    nomor = int(kode[1:]) # Ambil angka dari G01 -> 1
                    if range_kode_awal <= nomor <= range_kode_akhir:
                        if st.checkbox(f"{kode} - {deskripsi}"):
                            selected_gejala.append(kode)
                except:
                    pass

    # Kita panggil fungsi di atas sesuai kelompok di knowledge_base
    buat_checkbox("🔋 Masalah Baterai & Charging", 1, 7)
    buat_checkbox("📱 Masalah Layar & Fisik", 8, 12)
    buat_checkbox("📡 Masalah Sinyal & Koneksi", 13, 17)
    buat_checkbox("🔊 Masalah Suara (Audio)", 18, 21)
    buat_checkbox("📷 Masalah Kamera & Sensor", 22, 26)
    buat_checkbox("⚙️ Masalah Sistem & Mesin", 27, 30)

    st.markdown("---")

    # --- PROSES DIAGNOSA (Sama seperti sebelumnya) ---
    if st.button("🔍 ANALISA KERUSAKAN", type="primary"):
        if not selected_gejala:
            st.error("Kamu belum memilih gejala apapun! Coba buka kategori di atas.")
        else:
            diagnosa_result = []

            # Algoritma Pencocokan
            for penyakit, gejala_penyakit in rules_data.items():
                matched = set(selected_gejala).intersection(gejala_penyakit)
                
                # Hitung skor
                if len(gejala_penyakit) > 0:
                    score = (len(matched) / len(gejala_penyakit)) * 100
                else:
                    score = 0
                
                if score > 0:
                    diagnosa_result.append({
                        'penyakit': penyakit,
                        'score': score,
                        'solusi': solusi_data.get(penyakit, "Hubungi teknisi.")
                    })

            diagnosa_result.sort(key=lambda x: x['score'], reverse=True)

            # Tampilan Hasil
            st.subheader("📋 Hasil Diagnosa:")
            
            if diagnosa_result:
                # Hasil Utama
                top_result = diagnosa_result[0]
                
                # Desain Card Hasil Utama
                container = st.container()
                container.success(f"**{top_result['penyakit']}**")
                container.progress(int(top_result['score']))
                container.caption(f"Tingkat Keyakinan Sistem: {top_result['score']:.1f}%")
                
                with container.expander("🛠️ LIHAT SOLUSI PERBAIKAN", expanded=True):
                    st.write(top_result['solusi'])
                
                # Hasil Alternatif (Jika ada)
                if len(diagnosa_result) > 1:
                    st.divider()
                    st.caption("Kemungkinan lain yang terdeteksi:")
                    for res in diagnosa_result[1:]:
                        # Hanya tampilkan jika skornya lumayan (di atas 20%)
                        if res['score'] >= 20: 
                            st.text(f"• {res['penyakit']} ({res['score']:.0f}%)")
            else:
                st.warning("Pola gejala tidak dikenali. Coba kombinasi gejala lain atau konsultasi teknisi langsung.")

if __name__ == '__main__':
    main()