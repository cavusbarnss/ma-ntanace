import streamlit as st
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Monthly Maintenance Record", page_icon="🚛", layout="centered")

st.title("🚛 Monthly Maintenance Record")
st.write("Aşağıdaki alanları doldurarak formunuzu anında PDF olarak oluşturabilirsiniz.")

with st.form("maintenance_form"):
    st.subheader("1. Ay ve Yıl Bilgileri")
    col1, col2 = st.columns(2)
    with col1:
        month = st.text_input("Ay (Örn: November)", value="November")
    with col2:
        year = st.text_input("Yıl (Örn: 2026)", value="2026")
    
    st.subheader("2. 4 Haftalık Bakım ve Onarım Girişi")
    
    records = []
    for i in range(1, 5):
        st.markdown(f"**{i}. Hafta**")
        w_col1, w_col2, w_col3 = st.columns(3)
        with w_col1:
            d_val = st.text_input(f"Tarih {i}", key=f"date_{i}", placeholder="Örn: 9.1.2026")
        with w_col2:
            m_val = st.text_input(f"Mil {i}", key=f"mil_{i}", placeholder="Örn: 851000")
        with w_col3:
            desc_val = st.text_input(f"Açıklama {i}", key=f"desc_{i}", placeholder="Örn: oil change")
        records.append((d_val, m_val, desc_val))

    st.subheader("3. İmza ve Alt Bilgiler")
    sig_col1, sig_col2 = st.columns(2)
    with sig_col1:
        signature_name = st.text_input("İmza Sahibi (İsim / Soyisim)", value="Ahmet Parlakalin")
    with sig_col2:
        bottom_date = st.text_input("Form Tarihi", value="10.10.2026")

    submitted = st.form_submit_button("PDF Raporu Oluştur ve İndir")

if submitted:
    output_pdf_path = f"{month}_{year}_Maintenance_Report.pdf"
    
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    
    # Üst Başlıklar
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 750, "MONTHLY MAINTENANCE RECORD")
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(410, 750, "MONTH")
    c.setLineWidth(1)
    c.line(455, 748, 525, 748)
    c.drawString(470, 752, month)
    
    c.drawString(535, 750, "YEAR")
    c.line(565, 748, 605, 748)
    c.drawString(572, 752, year)

    # Sabit Firma Bilgileri
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, 715, "OWNER")
    c.line(110, 713, 290, 713)
    c.drawString(120, 717, "Fda auto transport llc")
    
    c.drawString(330, 715, "MAKE")
    c.line(390, 713, 470, 713)
    c.drawString(400, 717, "Freightliner")
    
    c.drawString(490, 715, "1fujghdv3dlbw1902")

    c.drawString(40, 690, "ADDRESS")
    c.line(110, 688, 290, 688)
    c.drawString(120, 692, "100 Villa Dest Drive")
    
    c.drawString(330, 690, "YEAR")
    c.line(390, 688, 470, 688)
    c.drawString(410, 692, "2013")

    c.line(110, 665, 290, 665)
    c.drawString(120, 669, "Coram Ny 11727")
    
    c.drawString(330, 665, "VEH. #")
    c.line(390, 663, 470, 663)
    c.drawString(410, 667, "Parlah")

    c.drawString(40, 635, "Annual Inspection Due")
    c.line(145, 633, 220, 633)

    # Tablo Çerçevesi
    c.rect(38, 360, 555, 240)
    c.line(135, 360, 135, 600)  
    c.line(235, 360, 235, 600)  
    c.line(38, 560, 593, 560)

    c.setFont("Helvetica-Bold", 9)
    c.drawString(65, 575, "DATE")
    c.drawString(155, 575, "MILEAGE")
    c.drawString(355, 575, "MAINTENANCE / REPAIRS - DESCRIBE BELOW")

    row_y = 560
    for _ in range(7):
        row_y -= 28
        c.line(38, row_y, 593, row_y)

    # Tablo Verileri (Toplam 7 satıra tamamla)
    full_records = list(records)
    while len(full_records) < 7:
        full_records.append(("", "", ""))

    c.setFont("Helvetica", 9)
    start_y = 540
    row_height = 28
    
    for idx, (d_val, m_val, des_val) in enumerate(full_records):
        current_y = start_y - (idx * row_height)
        if d_val:
            c.drawString(43, current_y, d_val)
        if m_val:
            c.drawString(145, current_y, m_val)
        if des_val:
            c.drawString(245, current_y, des_val)

    # Alt Bilgiler ve İmza
    c.setFont("Helvetica", 8)
    c.drawString(40, 335, "Please describe all maintenance / repairs performed on this vehicle for the month.")
    
    c.setFont("Helvetica", 7)
    c.drawString(40, 290, "This document must be completed once each month and submitted to the Safety Department by the 10th day")
    c.drawString(40, 280, "of the following month. Repairs and maintenance listed on this form are subject to verification by a qualified")
    c.drawString(40, 270, "representative of George Hildebrandt, Inc.")

    # Owner's Signature ve Çizgisi (Fazlalık C harfi tamamen temizlendi)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, 215, "Owner's Signature")
    c.line(40, 205, 220, 205)
    
    if signature_name:
        c.setFont("Helvetica", 9)
        c.drawString(140, 215, signature_name)

    c.setFont("Helvetica", 7)
    c.drawString(40, 180, "File: safety/monthly maintenance reports 1/2010")

    # Sağ taraftaki Date alanı ve çizgisi
    c.setFont("Helvetica-Bold", 9)
    c.line(320, 205, 420, 205)
    
    if bottom_date:
        c.setFont("Helvetica", 9)
        c.drawString(340, 215, bottom_date)
        
    c.drawString(320, 190, "Date")

    c.save()
    
    st.success("Rapor başarıyla oluşturuldu!")
    with open(output_pdf_path, "rb") as pdf_file:
        st.download_button(
            label="📄 PDF Dosyasını İndir",
            data=pdf_file,
            file_name=output_pdf_path,
            mime="application/pdf"
        )