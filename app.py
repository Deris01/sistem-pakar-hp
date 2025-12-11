import streamlit as st
from knowledge_base import gejala_data, rules_data, solusi_data
from fpdf import FPDF
from datetime import datetime

# --- FUNGSI GENERATOR PDF ---
def create_pdf(penyakit, score, solusi, gejala_user):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Laporan Diagnosa Dr. Gadget', 0, 1, 'C')
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, f'Tanggal Cetak: {datetime.now().strftime("%d-%m-%Y %H:%M")}', 0, 1, 'C')
            self.line(10, 30, 200, 30)
            self.ln(10)
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, 'Dicetak otomatis oleh Sistem Pakar Dr. Gadget (AI)', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    
    # Isi PDF
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'HASIL ANALISA UTAMA:', 0, 1)
    
    pdf.set_font('Arial', '', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.multi_cell(0, 10, f"Diagnosa: {penyakit}", 0, 1, 'L', True)
    pdf.multi_cell(0, 10, f"Keyakinan: {score:.1f}%", 0, 1, 'L', True)
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'SARAN PERBAIKAN:', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, solusi, 0, 1)
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'GEJALA TERDETEKSI:', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    for kode in gejala_user:
        nama_gejala = gejala_data.get(kode, "Unknown")
        pdf.cell(10, 8, "-", 0, 0)
        pdf.multi_cell(0, 8, f"({kode}) {nama_gejala}", 0, 1)

    return pdf.output(dest='S').encode('latin-1')

# --- APLIKASI UTAMA ---
def main():
    st.set_page_config(page_title="Dr. Gadget AI", page_icon="🤖", layout="wide")
    
    # --- CSS CUSTOM: MONTSERRAT (FINAL FIX) ---
    st.markdown("""
        <style>
        /* Import Font */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

        /* 1. Paksa Font Utama ke Montserrat */
        html, body, [class*="css"], h1, h2, h3, h4, h5, h6, p, li, span, div, button, input, textarea {
            font-family: 'Montserrat', sans-serif !important;
        }

        /* 2. PERBAIKAN IKON EXPANDER (Kuncinya di sini) */
        /* Target spesifik elemen ikon panah di Streamlit */
        div[data-testid="stExpander"] details summary svg {
            font-family: 'Source Sans Pro', sans-serif !important; /* Kembalikan ke default */
            vertical-align: middle;
        }
        
        /* Mencegah teks aneh muncul di sebelah ikon */
        div[data-testid="stExpander"] details summary span {
             font-family: 'Source Sans Pro', sans-serif !important;
        }

        /* Pastikan JUDUL Expander tetap Montserrat dan Tebal */
        div[data-testid="stExpander"] details summary p {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 600 !important;
            font-size: 16px !important;
        }

        /* Styling Judul Halaman */
        h1, h2, h3 {
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }
        
        /* Tombol Utama */
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            height: 3em;
            font-weight: 600 !important;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=100)
        st.title("Dr. Gadget v2.0")
        st.caption("AI Diagnostic System")
        st.markdown("---")
        st.info("💡 **Tips:** Pilih gejala selengkap mungkin agar diagnosa akurat.")
        
        if st.button("🔄 Reset Diagnosa"):
            st.rerun()

    # --- MAIN CONTENT ---
    col1, col2 = st.columns([1, 5])
    with col1:
        st.write("") 
    with col2:
        st.title("Diagnosa Kerusakan HP")
        st.write("Silakan centang gejala yang kamu alami di bawah ini.")

    st.markdown("---")

    # --- INPUT SECTION ---
    selected_gejala = []

    def buat_kategori(judul, icon, start, end):
        with st.expander(f"{icon} {judul}"):
            cols = st.columns(2)
            for i, (kode, deskripsi) in enumerate(gejala_data.items()):
                try:
                    nomor = int(kode[1:])
                    if start <= nomor <= end:
                        with cols[i % 2]: 
                            if st.checkbox(f"{kode} - {deskripsi}"):
                                selected_gejala.append(kode)
                except: pass

    col_a, col_b = st.columns(2)
    with col_a:
        buat_kategori("Baterai & Power", "🔋", 1, 7)
        buat_kategori("Sinyal & Koneksi", "📡", 13, 17)
        buat_kategori("Kamera & Sensor", "📷", 22, 26)
    with col_b:
        buat_kategori("Layar & Fisik", "📱", 8, 12)
        buat_kategori("Audio / Suara", "🔊", 18, 21)
        buat_kategori("Sistem & Mesin", "⚙️", 27, 30)

    st.markdown("---")

    # --- TOMBOL ANALISA ---
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        analisa_btn = st.button("🔍 JALANKAN DIAGNOSA", type="primary")

    # --- PROSES & HASIL ---
    if analisa_btn:
        if not selected_gejala:
            st.toast("⚠️ Pilih minimal satu gejala dulu ya!", icon="⚠️")
        else:
            with st.spinner('Sedang menganalisa sirkuit...'):
                diagnosa_result = []
                for penyakit, gejala_penyakit in rules_data.items():
                    matched = set(selected_gejala).intersection(gejala_penyakit)
                    score = (len(matched) / len(gejala_penyakit)) * 100 if gejala_penyakit else 0
                    if score > 0:
                        diagnosa_result.append({'p': penyakit, 's': score, 'sol': solusi_data.get(penyakit, "-")})
                
                diagnosa_result.sort(key=lambda x: x['s'], reverse=True)

            if diagnosa_result:
                top = diagnosa_result[0]
                
                st.markdown("### 📊 Hasil Analisa AI")
                
                m1, m2 = st.columns([3, 1])
                with m1:
                    st.error(f"Terdeteksi: **{top['p']}**")
                with m2:
                    st.metric("Tingkat Keyakinan", f"{top['s']:.0f}%", delta="High Risk", delta_color="inverse")

                st.progress(int(top['s']))
                st.info(f"🛠️ **Solusi:** {top['sol']}")

                html_pdf = create_pdf(top['p'], top['s'], top['sol'], selected_gejala)
                st.download_button(
                    label="📥 Download Laporan (PDF)",
                    data=html_pdf,
                    file_name=f"DrGadget_Report.pdf",
                    mime="application/pdf",
                    key="pdf-btn"
                )

                if len(diagnosa_result) > 1:
                    with st.expander("Lihat Kemungkinan Lain"):
                        for res in diagnosa_result[1:]:
                            if res['s'] >= 20:
                                st.write(f"• **{res['p']}** - {res['s']:.0f}%")
            else:
                st.warning("Gejala tidak spesifik. Coba tambahkan detail gejala lain.")

if __name__ == '__main__':

    main()
