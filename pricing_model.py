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
                "**🎯 Goal:** Predict market value of properties instantly based on features.",
                "**🧠 Tech:** Random Forest Regressor & Spatial Feature Engineering.",
                "**💰 Impact:** Accelerating appraisal processes and preventing mispricing."
            ],
            "tr": [
                "**🎯 Amaç:** İstanbul genelinde konut özelliklerine göre piyasa değerini saniyelik tahmin etmek.",
                "**🧠 Teknik:** Random Forest Regressor & Konumsal Feature Engineering.",
                "**💰 Kazanç:** Ekspertiz süreçlerinin hızlanması ve hatalı fiyatlandırmanın önüne geçilmesi."
            ]
        },
        "labels": {
            "en": ["Select District", "Size (m2)", "Building Age", "Rooms", "Estimated Value", "Location",
                   "Unit Price"],
            "tr": ["İlçe Seçin", "Brüt Metrekare", "Bina Yaşı", "Oda Sayısı", "Tahmin Edilen Değer", "Konum",
                   "Birim Fiyat"]
        }
    }

    districts = {
        'Beşiktaş': {'base': 120000, 'mult': 1.8},
        'Kadıköy': {'base': 95000, 'mult': 1.5},
        'Şişli': {'base': 85000, 'mult': 1.4},
        'Üsküdar': {'base': 75000, 'mult': 1.3},
        'Başakşehir': {'base': 45000, 'mult': 0.9},
        'Esenyurt': {'base': 25000, 'mult': 0.6}
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
        for _ in range(1000):
            d_name = np.random.choice(list(_dist_map.keys()))
            d_props = _dist_map[d_name]

            size = np.random.randint(50, 250)
            age = np.random.randint(0, 40)
            rooms = np.random.randint(1, 6)

            price = (size * d_props['base'] * d_props['mult']) - (age * 5000) + (rooms * 200000)
            price += np.random.normal(0, price * 0.05)
            data.append([d_name, size, age, rooms, price])

        return pd.DataFrame(data, columns=['District', 'Size', 'Age', 'Rooms', 'Price'])

    df = generate_market_data(districts)

    df_encoded = pd.get_dummies(df, columns=['District'])
    X = df_encoded.drop('Price', axis=1)
    y = df_encoded['Price']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    c1, c2 = st.columns(2)
    labels = content["labels"][lang]

    with c1:
        st.subheader("🛠️ " + ("Konut Özellikleri" if lang == 'tr' else "Features"))
        s_dist = st.selectbox(labels[0], list(districts.keys()))
        s_size = st.slider(labels[1], 50, 250, 100)
        s_age = st.number_input(labels[2], 0, 50, 5)
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
        st.info(f"📍 **{labels[5]}:** {s_dist}\n\n📏 **{labels[6]}:** ~₺{prediction / s_size:,.0f}/m²")

        avg_price = df.groupby('District')['Price'].mean().sort_values()
        fig = px.bar(x=avg_price.index, y=avg_price.values)
        fig.update_layout(xaxis_title=None, yaxis_title=None, margin=dict(t=0, b=0, l=0, r=0), height=200)
        st.plotly_chart(fig, use_container_width=True)