import streamlit as st
from knowledge_base import gejala_data, rules_data, solusi_data
from fpdf import FPDF
import base64
from datetime import datetime

# --- FUNGSI GENERATOR PDF ---
def create_pdf(penyakit, score, solusi, gejala_user):
    class PDF(FPDF):
        def header(self):
            # Header Laporan
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Laporan Diagnosa Dr. Gadget', 0, 1, 'C')
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, f'Tanggal Cetak: {datetime.now().strftime("%d-%m-%Y %H:%M")}', 0, 1, 'C')
            self.line(10, 30, 200, 30) # Garis pemisah
            self.ln(10)

        def footer(self):
            # Footer
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, 'Dicetak otomatis oleh Sistem Pakar Dr. Gadget (AI)', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    
    # Bagian 1: Hasil Diagnosa
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'HASIL ANALISA UTAMA:', 0, 1)
    
    pdf.set_font('Arial', '', 12)
    pdf.set_fill_color(230, 230, 230) # Warna abu-abu muda
    pdf.multi_cell(0, 10, f"Kerusakan Terdeteksi: {penyakit}", 0, 1, 'L', True)
    pdf.multi_cell(0, 10, f"Tingkat Keyakinan Sistem: {score:.1f}%", 0, 1, 'L', True)
    pdf.ln(5)

    # Bagian 2: Solusi
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'SARAN PERBAIKAN:', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, solusi, 0, 1)
    pdf.ln(5)

    # Bagian 3: Detail Gejala (Bukti)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'GEJALA YANG DIKELUHKAN:', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    # Loop untuk menampilkan gejala yang dipilih user
    for kode in gejala_user:
        nama_gejala = gejala_data.get(kode, "Gejala tidak dikenal")
        pdf.cell(10, 8, "-", 0, 0)
        pdf.multi_cell(0, 8, f"({kode}) {nama_gejala}", 0, 1)

    # Output file sementara
    return pdf.output(dest='S').encode('latin-1')

# --- APLIKASI UTAMA (STREAMLIT) ---
def main():
    st.set_page_config(page_title="Sistem Pakar HP", page_icon="🔧", layout="centered")
    
    # CSS Hack untuk menyembunyikan menu default Streamlit biar bersih
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

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

    # --- INPUT USER ---
    selected_gejala = []

    def buat_checkbox(judul_kategori, range_kode_awal, range_kode_akhir):
        with st.expander(judul_kategori):
            for kode, deskripsi in gejala_data.items():
                try:
                    nomor = int(kode[1:]) 
                    if range_kode_awal <= nomor <= range_kode_akhir:
                        if st.checkbox(f"{kode} - {deskripsi}"):
                            selected_gejala.append(kode)
                except:
                    pass

    buat_checkbox("🔋 Masalah Baterai & Charging", 1, 7)
    buat_checkbox("📱 Masalah Layar & Fisik", 8, 12)
    buat_checkbox("📡 Masalah Sinyal & Koneksi", 13, 17)
    buat_checkbox("🔊 Masalah Suara (Audio)", 18, 21)
    buat_checkbox("📷 Masalah Kamera & Sensor", 22, 26)
    buat_checkbox("⚙️ Masalah Sistem & Mesin", 27, 30)

    st.markdown("---")

    # --- PROSES DIAGNOSA ---
    if st.button("🔍 ANALISA KERUSAKAN", type="primary"):
        if not selected_gejala:
            st.error("Kamu belum memilih gejala apapun! Coba buka kategori di atas.")
        else:
            diagnosa_result = []

            for penyakit, gejala_penyakit in rules_data.items():
                matched = set(selected_gejala).intersection(gejala_penyakit)
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

            st.subheader("📋 Hasil Diagnosa:")
            
            if diagnosa_result:
                top_result = diagnosa_result[0]
                
                # Container Hasil
                with st.container():
                    st.success(f"**{top_result['penyakit']}**")
                    st.progress(int(top_result['score']))
                    st.caption(f"Tingkat Keyakinan Sistem: {top_result['score']:.1f}%")
                    
                    with st.expander("🛠️ LIHAT SOLUSI PERBAIKAN", expanded=True):
                        st.write(top_result['solusi'])

                # --- FITUR BARU: DOWNLOAD PDF ---
                st.markdown("---")
                st.write("📄 **Ingin menyimpan hasil ini?**")
                
                # Generate PDF di memory
                html_pdf = create_pdf(top_result['penyakit'], top_result['score'], top_result['solusi'], selected_gejala)
                
                # Tombol Download
                st.download_button(
                    label="📥 Download Laporan Hasil Diagnosa (PDF)",
                    data=html_pdf,
                    file_name=f"laporan_diagnosa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
                # --------------------------------
                
                if len(diagnosa_result) > 1:
                    st.divider()
                    st.caption("Kemungkinan lain yang terdeteksi:")
                    for res in diagnosa_result[1:]:
                        if res['score'] >= 20: 
                            st.text(f"• {res['penyakit']} ({res['score']:.0f}%)")
            else:
                st.warning("Pola gejala tidak dikenali. Coba kombinasi gejala lain.")

if __name__ == '__main__':
    main()