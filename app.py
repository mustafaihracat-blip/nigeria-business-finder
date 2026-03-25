import streamlit as st
import pandas as pd
import os
import sys

# Bulunulan dizini yola ekle
sys.path.append(os.getcwd())

from main import find_nigeria_businesses

st.set_page_config(page_title="İhracat Fabrikası - Ajan Paneli", layout="wide")

st.title("🏭 İhracat Fabrikası: Nijerya Müşteri Bulucu")
st.write("Ürün grubunu yazın ve Nijerya pazarına ilk adımı atın.")

# Yan Menü
with st.sidebar:
    st.header("Arama Ayarları")
    product = st.text_input("Hangi ürünü arıyoruz?", "Electrical EPC contractors")
    cities_val = st.slider("Kaç şehir taranacak?", 1, 10, 2)
    start_button = st.button("Taramayı Başlat 🚀")

# Ana Ekran
if start_button:
    with st.spinner('Ajan Nijerya sokaklarında verileri topluyor...'):
        # Fonksiyona sadece 'product' ve 'max_cities' gönderiyoruz
        df, xlsx_path = find_nigeria_businesses(product=product, max_cities=cities_val)
        
    if df is not None and not df.empty:
        st.success(f"İşlem tamam! {len(df)} firma bulundu.")
        st.dataframe(df)
        
        with open(xlsx_path, "rb") as file:
            st.download_button(
                label="Excel Dosyasını İndir 📥",
                data=file,
                file_name=os.path.basename(xlsx_path),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.error("Maalesef sonuç bulunamadı. Lütfen arama terimini değiştirin.")
