import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

def run(lang='en'):
    content = {
        "title": {"en": "Istanbul Real Estate Valuation", "tr": "İstanbul Konut Fiyat Tahminleme"},
        "summary": {"en": "Project Overview & Business Value", "tr": "ℹ️ Proje Özeti ve İş Değeri"},
        "metrics": {
            "en": [
                "**🎯 Goal:** Predict market value based on location & features.",
                "**🧠 Tech:** Random Forest & Synthetic Data Engineering.",
                "**💰 Impact:** Instant appraisal for real estate professionals."
            ],
            "tr": [
                "**🎯 Amaç:** Konum ve özelliklere göre piyasa değerini tahmin etmek.",
                "**🧠 Teknik:** Random Forest & Sentetik Veri Mühendisliği.",
                "**💰 Kazanç:** Gayrimenkul uzmanları için anlık ekspertiz."
            ]
        },
        "labels": {
            "en": ["Select District", "Size (m2)", "Building Age", "Rooms", "Estimated Value", "Location", "Unit Price"],
            "tr": ["İlçe Seçin", "Brüt Metrekare", "Bina Yaşı", "Oda Sayısı", "Tahmin Edilen Değer", "Konum", "Birim Fiyat"]
        }
    }

    # BÖLGE KATSAYILARI
    districts = {
        'Beşiktaş': {'base': 150000, 'mult': 2.0},  # Lüks
        'Kadıköy': {'base': 130000, 'mult': 1.8},   # Popüler
        'Şişli': {'base': 110000, 'mult': 1.6},     # Merkezi
        'Üsküdar': {'base': 95000, 'mult': 1.4},    # Tarihi
        'Başakşehir': {'base': 65000, 'mult': 1.1}, # Yeni Yerleşim
        'Esenyurt': {'base': 35000, 'mult': 0.8}    # Uygun Fiyat
    }

    with st.expander(content["summary"][lang], expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.markdown(content["metrics"][lang][0])
        c2.markdown(content["metrics"][lang][1])
        c3.markdown(content["metrics"][lang][2])

    st.subheader(content["title"][lang])

    @st.cache_data
    def generate_market_data(_dist_map):
        np.random.seed(42)
        data = []
        for _ in range(2000): # Veri sayısını artırdık
            d_name = np.random.choice(list(_dist_map.keys()))
            d_props = _dist_map[d_name]
            
            size = np.random.randint(50, 250)
            age = np.random.randint(0, 50)
            rooms = np.random.randint(1, 6)
            
            # --- GELİŞMİŞ FİYAT FORMÜLÜ ---
            # 1. Metrekare baz fiyatı
            base_value = size * d_props['base'] * d_props['mult']
            
            # 2. Bina Yaşı Cezası 
            # 0-5 yaş: Değerli, 30+ yaş: Ciddi düşüş (Deprem riski simülasyonu)
            age_penalty_rate = 0.015 * age # Her yıl %1.5 değer kaybı
            if age > 30:
                age_penalty_rate += 0.20 # 30 yaş üstüne ekstra %20 ceza
            
            current_value = base_value * (1 - min(age_penalty_rate, 0.70)) # Maksimum %70 değer kaybedebilir
            
            # 3. Oda Bonusu
            room_bonus = rooms * 150000
            
            final_price = current_value + room_bonus
            
            # Gürültü (Piyasa dalgalanması)
            final_price += np.random.normal(0, final_price * 0.05)
            
            data.append([d_name, size, age, rooms, final_price])
            
        return pd.DataFrame(data, columns=['District', 'Size', 'Age', 'Rooms', 'Price'])

    df = generate_market_data(districts)
    
    # Model Eğitimi
    df_encoded = pd.get_dummies(df, columns=['District'])
    X = df_encoded.drop('Price', axis=1)
    y = df_encoded['Price']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    c1, c2 = st.columns(2)
    labels = content["labels"][lang]

    with c1:
        st.subheader("🛠️ " + ("Konut Özellikleri" if lang=='tr' else "Features"))
        s_dist = st.selectbox(labels[0], list(districts.keys()))
        s_size = st.slider(labels[1], 50, 250, 100)
        s_age = st.slider(labels[2], 0, 50, 5) # Input yerine Slider yaptık, daha kolay
        s_rooms = st.radio(labels[3], [1, 2, 3, 4, 5], index=2, horizontal=True)

    input_row = pd.DataFrame(columns=X.columns)
    input_row.loc[0] = 0
    input_row['Size'] = s_size
    input_row['Age'] = s_age
    input_row['Rooms'] = s_rooms
    if f'District_{s_dist}' in input_row.columns:
        input_row[f'District_{s_dist}'] = 1

    prediction = model.predict(input_row)[0]

    with c2:
        st.subheader(labels[4])
        st.metric(label="", value=f"₺{prediction:,.0f}")
        
        # Dinamik Yorum (Fiyata göre renk değişimi)
        unit_price = prediction / s_size
        st.info(f"📍 **{labels[5]}:** {s_dist}\n\n📏 **{labels[6]}:** ~₺{unit_price:,.0f}/m²")
        
        # Yaş Uyarısı
        if s_age > 30 and lang == 'tr':
            st.warning("⚠️ Bina yaşı 30'un üzerinde olduğu için amortisman düşüşü yüksektir.")
        elif s_age > 30:
            st.warning("⚠️ High depreciation due to building age > 30.")

        avg_price = df.groupby('District')['Price'].mean().sort_values()
        fig = px.bar(x=avg_price.index, y=avg_price.values, color=avg_price.values, color_continuous_scale="Blues")
        fig.update_layout(xaxis_title=None, yaxis_title=None, margin=dict(t=0, b=0, l=0, r=0), height=200, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
