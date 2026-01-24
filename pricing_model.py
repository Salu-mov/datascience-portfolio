import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import shap

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
        "how_it_works": {"en": "🔍 How It Works", "tr": "🔍 Nasıl Çalışır?"},
        "workflow": {
            "en": """
            **Valuation Algorithm:**
            
            1. **Input Features** → District (one-hot encoded), Size (m²), Building Age, # of Rooms
            2. **Base Price Calculation** → District coefficient × Size
            3. **Depreciation Model** → Age penalty: 1.5%/year (30+ years get extra 20% penalty for earthquake risk)
            4. **Room Premium** → +₺150,000 per room
            5. **Random Forest Ensemble** → 100 decision trees aggregate predictions
            6. **Output** → Market value estimate + unit price (₺/m²)
            
            **Try It:** Adjust sliders to see how features impact valuation in real-time.
            """,
            "tr": """
            **Değerleme Algoritması:**
            
            1. **Giriş Özellikleri** → İlçe (one-hot kodlanmış), Metrekare, Bina Yaşı, Oda Sayısı
            2. **Baz Fiyat** → İlçe katsayısı × Metrekare
            3. **Amortisman Modeli** → Yaş cezası: %1.5/yıl (30+ yaş için deprem riski sebebiyle ekstra %20 ceza)
            4. **Oda Primi** → Oda başına +₺150,000
            5. **Random Forest Topluluk** → 100 karar ağacı tahminleri birleştirir
            6. **Çıktı** → Piyasa değeri tahmini + birim fiyat (₺/m²)
            
            **Deneyin:** Kaydırıcıları ayarlayarak özelliklerin değere etkisini anında görün.
            """
        },
        "performance": {"en": "📊 Model Performance", "tr": "📊 Model Performansı"},
        "labels": {
            "en": ["Select District", "Size (m²)", "Building Age", "Rooms", "Estimated Value", "Location", "Unit Price"],
            "tr": ["İlçe Seçin", "Brüt Metrekare", "Bina Yaşı", "Oda Sayısı", "Tahmin Edilen Değer", "Konum", "Birim Fiyat"]
        },
        "upload_label": {"en": "📂 Upload Real Estate Data (CSV)", "tr": "📂 Emlak Verisi Yükleyin (CSV)"},
        "upload_help": {"en": "Columns: District, Size, Age, Rooms, Price", "tr": "Sütunlar: District, Size, Age, Rooms, Price"},
        "explainability": {"en": "🔍 Feature Importance", "tr": "🔍 Özellik Önem Sıralaması"}
    }

    # BÖLGE KATSAYILARI
    districts = {
        'Beşiktaş': {'base': 150000, 'mult': 2.0},
        'Kadıköy': {'base': 130000, 'mult': 1.8},
        'Şişli': {'base': 110000, 'mult': 1.6},
        'Üsküdar': {'base': 95000, 'mult': 1.4},
        'Başakşehir': {'base': 65000, 'mult': 1.1},
        'Esenyurt': {'base': 35000, 'mult': 0.8}
    }

    with st.expander(content["summary"][lang], expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.markdown(content["metrics"][lang][0])
        c2.markdown(content["metrics"][lang][1])
        c3.markdown(content["metrics"][lang][2])

    # NASIL ÇALIŞIR
    with st.expander(content["how_it_works"][lang], expanded=False):
        st.markdown(content["workflow"][lang])

    st.subheader(content["title"][lang])

    # VERİ YÜKLEME
    uploaded_file = st.file_uploader(
        content["upload_label"][lang],
        type=["csv"],
        help=content["upload_help"][lang]
    )

    @st.cache_data
    def generate_market_data(_dist_map):
        np.random.seed(42)
        data = []
        for _ in range(2000):
            d_name = np.random.choice(list(_dist_map.keys()))
            d_props = _dist_map[d_name]
            
            size = np.random.randint(50, 250)
            age = np.random.randint(0, 50)
            rooms = np.random.randint(1, 6)
            
            base_value = size * d_props['base'] * d_props['mult']
            age_penalty_rate = 0.015 * age
            if age > 30:
                age_penalty_rate += 0.20
            
            current_value = base_value * (1 - min(age_penalty_rate, 0.70))
            room_bonus = rooms * 150000
            final_price = current_value + room_bonus
            final_price += np.random.normal(0, final_price * 0.05)
            
            data.append([d_name, size, age, rooms, final_price])
            
        return pd.DataFrame(data, columns=['District', 'Size', 'Age', 'Rooms', 'Price'])

    # VERİ KONTROLÜ
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required_cols = ['District', 'Size', 'Age', 'Rooms', 'Price']
            if not all(col in df.columns for col in required_cols):
                st.error(f"❌ CSV must contain: {', '.join(required_cols)}")
                df = generate_market_data(districts)
            else:
                st.success("✅ Custom data loaded!" if lang == 'en' else "✅ Özel veri yüklendi!")
        except Exception as e:
            st.error(f"Error: {e}")
            df = generate_market_data(districts)
    else:
        st.info("Using synthetic Istanbul data..." if lang == 'en' else "Sentetik İstanbul verisi kullanılıyor...")
        df = generate_market_data(districts)

    # MODEL EĞİTİMİ
    df_encoded = pd.get_dummies(df, columns=['District'])
    X = df_encoded.drop('Price', axis=1)
    y = df_encoded['Price']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X, y)

    # MODEL PERFORMANSI
    train_pred = model.predict(X)
    mae = mean_absolute_error(y, train_pred)
    r2 = r2_score(y, train_pred)
    mape = np.mean(np.abs((y - train_pred) / y)) * 100

    st.subheader(content["performance"][lang])
    col1, col2, col3 = st.columns(3)
    col1.metric("MAE", f"₺{mae:,.0f}", help="Mean Absolute Error")
    col2.metric("R² Score", f"{r2:.3f}", help="Model explains {:.1f}% of variance".format(r2*100))
    col3.metric("MAPE", f"{mape:.1f}%", help="Mean Absolute Percentage Error")

    # KULLANICI GİRİŞİ
    st.divider()
    c1, c2 = st.columns(2)
    labels = content["labels"][lang]

    with c1:
        st.subheader("🛠️ " + ("Konut Özellikleri" if lang=='tr' else "Property Features"))
        s_dist = st.selectbox(labels[0], list(districts.keys()))
        s_size = st.slider(labels[1], 50, 250, 100)
        s_age = st.slider(labels[2], 0, 50, 5)
        s_rooms = st.radio(labels[3], [1, 2, 3, 4, 5], index=2, horizontal=True)

    # TAHMİN
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
        
        unit_price = prediction / s_size
        st.info(f"📍 **{labels[5]}:** {s_dist}\n\n📏 **{labels[6]}:** ~₺{unit_price:,.0f}/m²")
        
        if s_age > 30 and lang == 'tr':
            st.warning("⚠️ Bina yaşı 30'un üzerinde olduğu için amortisman düşüşü yüksektir.")
        elif s_age > 30:
            st.warning("⚠️ High depreciation due to building age > 30.")

        # BÖLGE KARŞILAŞTıRMA GRAFİĞİ
        avg_price = df.groupby('District')['Price'].mean().sort_values()
        fig_district = px.bar(
            x=avg_price.index,
            y=avg_price.values,
            color=avg_price.values,
            color_continuous_scale="Blues",
            labels={'x': 'District', 'y': 'Avg Price (₺)'}
        )
        fig_district.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            margin=dict(t=0, b=0, l=0, r=0),
            height=250,
            showlegend=False
        )
        st.plotly_chart(fig_district, use_container_width=True)

    # FEATURE IMPORTANCE
    st.divider()
    st.subheader(content["explainability"][lang])
    
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False).head(10)
    
    fig_importance = px.bar(
        feature_importance,
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale='Viridis'
    )
    
    fig_importance.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Importance Score" if lang == 'en' else "Önem Skoru",
        yaxis_title=""
    )
    
    st.plotly_chart(fig_importance, use_container_width=True)

    # PDF EXPORT BUTONU
    if st.button("📄 " + ("Download Report (PDF)" if lang == 'en' else "Rapor İndir (PDF)")):
        st.info("PDF export functionality will be implemented with ReportLab library" if lang == 'en' else "PDF dışa aktarma ReportLab kütüphanesi ile eklenecek")
