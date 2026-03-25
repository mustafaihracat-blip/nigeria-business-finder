import streamlit as st
import pandas as pd
import os
from main import find_nigeria_businesses # Mevcut fonksiyonunu çağırıyoruz

st.set_page_config(page_title="İhracat Fabrikası - Ajan Paneli", layout="wide")

st.title("🏭 İhracat Fabrikası: Nijerya Müşteri Bulucu")
st.write("Ürün grubunu yazın ve Nijerya pazarına ilk adımı atın.")

# Yan Menü / Ayarlar
with st.sidebar:
    st.header("Arama Ayarları")
    product = st.text_input("Hangi ürünü arıyoruz?", "electrical equipment")
    cities_count = st.slider("Kaç şehir taranacak?", 1, 10, 2)
    start_button = st.button("Taramayı Başlat 🚀")

# Ana Ekran
if start_button:
    with st.spinner('Ajan şu an Nijerya sokaklarında sizin için geziyor...'):
        # Burada mevcut fonksiyonunu streamlit'e uyumlu çalıştırıyoruz
        find_nigeria_businesses(product) 
        
    st.success(f"İşlem tamam! {product} için veriler toplandı.")
    
    # Çıktı dosyasını bul ve göster
    output_files = [f for f in os.listdir("output") if f.endswith(".xlsx")]
    if output_files:
        latest_file = os.path.join("output", output_files[-1])
        df = pd.read_excel(latest_file)
        st.dataframe(df) # Tabloyu ekranda göster
        
        with open(latest_file, "rb") as file:
            st.download_button(
                label="Excel Dosyasını İndir 📥",
                data=file,
                file_name=output_files[-1],
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
