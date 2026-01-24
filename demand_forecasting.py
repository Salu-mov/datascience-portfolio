import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import datetime

def run(lang='en'):
    # --- DİL AYARLARI ---
    content = {
        "title": {"en": "AI-Powered Demand Forecasting", "tr": "AI Tabanlı Talep Öngörü Sistemi"},
        "summary": {"en": "Project Overview", "tr": "ℹ️ Proje Özeti"},
        "metrics": {
            "en": ["**🎯 Goal:** Predict future sales to optimize stock.", "**🧠 Tech:** XGBoost & Time Series.", "**💰 Impact:** Reduce inventory costs."],
            "tr": ["**🎯 Amaç:** Gelecek satışları tahmin edip stoku optimize etmek.", "**🧠 Teknik:** XGBoost & Zaman Serisi.", "**💰 Kazanç:** Stok maliyetini düşürmek."]
        },
        "how_it_works": {"en": "🔍 How It Works", "tr": "🔍 Nasıl Çalışır?"},
        "workflow": {
            "en": """
            **Pipeline Architecture:**
            
            1. **Data Ingestion** → Historical sales data (Date + Sales columns)
            2. **Feature Engineering** → Create lag features (7-day) + rolling averages + day-of-week encoding
            3. **Model Training** → XGBoost Regressor with 100 estimators
            4. **Prediction** → Forecast next period sales
            5. **Business Action** → Calculate reorder point for inventory optimization
            
            **Why This Works:** Time series patterns + gradient boosting captures both trend and seasonality.
            """,
            "tr": """
            **Pipeline Mimarisi:**
            
            1. **Veri Alımı** → Geçmiş satış verisi (Tarih + Satış sütunları)
            2. **Özellik Mühendisliği** → Lag özellikleri (7-gün) + hareketli ortalama + haftanın günü
            3. **Model Eğitimi** → 100 ağaç içeren XGBoost Regressor
            4. **Tahmin** → Gelecek dönem satışlarını öngör
            5. **İş Aksiyonu** → Sipariş noktası hesapla, stok optimize et
            
            **Neden Çalışır:** Zaman serisi desenleri + gradient boosting hem trend hem mevsimselliği yakalar.
            """
        },
        "performance": {"en": "📊 Model Performance", "tr": "📊 Model Performansı"},
        "chart_title": {"en": "Sales Forecast (Past vs Future)", "tr": "Satış Tahmini (Geçmiş ve Gelecek)"},
        "alert": {"en": "💡 **Insight:** Reorder point is **{:.0f}** units.", "tr": "💡 **Analiz:** Sipariş noktası: **{:.0f}** adet."},
        "roi_calc": {"en": "💰 Business Impact Calculator", "tr": "💰 İş Etkisi Hesaplayıcısı"},
        "monthly_sales": {"en": "Monthly Average Sales (₺)", "tr": "Aylık Ortalama Satış (₺)"},
        "overstock": {"en": "Current Overstock Rate (%)", "tr": "Mevcut Fazla Stok Oranı (%)"},
        "savings": {"en": "Annual Savings Potential: ₺{:,.0f}", "tr": "Yıllık Tasarruf Potansiyeli: ₺{:,.0f}"},
        "upload_label": {"en": "📂 Upload your own CSV file", "tr": "📂 Kendi CSV dosyanızı yükleyin"},
        "upload_help": {"en": "Columns must be: 'Date' and 'Sales'", "tr": "Sütun adları 'Date' ve 'Sales' olmalıdır"},
        "error_cols": {"en": "❌ Error: CSV must contain 'Date' and 'Sales' columns.", "tr": "❌ Hata: CSV dosyası 'Date' ve 'Sales' sütunlarını içermelidir."},
        "use_demo": {"en": "Using synthetic demo data...", "tr": "Sentetik demo verisi kullanılıyor..."}
    }

    with st.expander(content["summary"][lang], expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.markdown(content["metrics"][lang][0])
        c2.markdown(content["metrics"][lang][1])
        c3.markdown(content["metrics"][lang][2])

    # NASIL ÇALIŞIR
    with st.expander(content["how_it_works"][lang], expanded=False):
        st.markdown(content["workflow"][lang])
        
        # Pipeline görselleştirmesi
        st.markdown("```mermaid\ngraph LR\n    A[Raw Data] --> B[Feature Engineering]\n    B --> C[XGBoost Model]\n    C --> D[Predictions]\n    D --> E[Reorder Point]\n```")

    st.subheader(content["title"][lang])

    # --- DOSYA YÜKLEME ALANI ---
    uploaded_file = st.file_uploader(content["upload_label"][lang], type=["csv"], help=content["upload_help"][lang])

    # --- VERİ İŞLEME FONKSİYONU ---
    def process_data(df_input):
        df_input['Date'] = pd.to_datetime(df_input['Date'], errors='coerce')
        df_input = df_input.dropna(subset=['Date'])
        df_input = df_input.sort_values('Date')
        
        # Feature Engineering
        df_input['lag_7'] = df_input['Sales'].shift(7)
        df_input['rolling_mean'] = df_input['Sales'].shift(1).rolling(7).mean()
        df_input['day_of_week'] = df_input['Date'].dt.dayofweek
        return df_input.dropna()

    # --- SENTETİK VERİ ÜRETİCİ ---
    @st.cache_data
    def generate_synthetic_data():
        start_date = datetime.date(2023, 1, 1)
        dates = pd.date_range(start=start_date, periods=730, freq='D')
        trend = np.linspace(0, 50, 730)
        seasonality = 20 * np.sin(np.linspace(0, 3 * np.pi, 730))
        noise = np.random.normal(0, 10, 730)
        sales = 100 + trend + seasonality + noise
        return pd.DataFrame({"Date": dates, "Sales": np.maximum(sales, 0)})

    # --- AKIŞ KONTROLÜ ---
    df = None
    
    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            if 'Date' in df_uploaded.columns and 'Sales' in df_uploaded.columns:
                df = process_data(df_uploaded)
                st.success("✅ Veri başarıyla yüklendi!" if lang == 'tr' else "✅ Data uploaded successfully!")
            else:
                st.error(content["error_cols"][lang])
        except Exception as e:
            st.error(f"Hata/Error: {e}")

    if df is None:
        if uploaded_file is None:
            st.info(content["use_demo"][lang])
        df_raw = generate_synthetic_data()
        df = process_data(df_raw)

    # --- MODEL EĞİTİMİ ---
    X = df[['lag_7', 'rolling_mean', 'day_of_week']]
    y = df['Sales']

    split_point = int(len(X) * 0.8)
    
    X_train, y_train = X.iloc[:split_point], y.iloc[:split_point]
    X_test, y_test = X.iloc[split_point:], y.iloc[split_point:]

    model = XGBRegressor(n_estimators=100, learning_rate=0.05, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    
    # PERFORMANS METRİKLERİ
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100

    # --- PERFORMANS KARTLARI ---
    st.subheader(content["performance"][lang])
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("RMSE", f"{rmse:.2f}", help="Root Mean Squared Error - Lower is better")
    col2.metric("MAE", f"{mae:.2f}", help="Mean Absolute Error")
    col3.metric("R² Score", f"{r2:.3f}", help="Coefficient of Determination (0-1)")
    col4.metric("MAPE", f"{mape:.1f}%", help="Mean Absolute Percentage Error")

    # --- GRAFİK KISMI ---
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Date'].iloc[:split_point], 
        y=y_train, 
        name="Geçmiş/History",
        line=dict(color='gray', width=1),
        opacity=0.6
    ))

    fig.add_trace(go.Scatter(
        x=df['Date'].iloc[split_point:], 
        y=y_test, 
        name="Gerçek/Actual",
        line=dict(color='#636EFA', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=df['Date'].iloc[split_point:], 
        y=predictions, 
        name="AI Tahmini/Forecast",
        line=dict(color='#EF553B', width=3, dash='dot')
    ))

    split_date = df['Date'].iloc[split_point]
    fig.add_vline(x=split_date, line_width=2, line_dash="dash", line_color="green")

    fig.update_layout(
        title=content["chart_title"][lang],
        template="plotly_white",
        hovermode="x unified",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    reorder_point = predictions.mean()
    st.info(content["alert"][lang].format(reorder_point))

    # --- ROI HESAPLAYICI ---
    st.divider()
    st.subheader(content["roi_calc"][lang])
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        monthly_sales = st.number_input(
            content["monthly_sales"][lang],
            min_value=10000,
            max_value=10000000,
            value=500000,
            step=50000
        )
    
    with col_b:
        overstock_rate = st.slider(
            content["overstock"][lang],
            min_value=5,
            max_value=40,
            value=20
        )
    
    # Tasarruf hesaplama: Fazla stoğun %60'ı optimize edilebilir
    savings = monthly_sales * (overstock_rate / 100) * 0.6 * 12
    
    st.success(content["savings"][lang].format(savings))
    
    # Mini görselleştirme
    savings_breakdown = pd.DataFrame({
        'Category': ['Before AI' if lang == 'en' else 'AI Öncesi', 
                     'After AI' if lang == 'en' else 'AI Sonrası'],
        'Cost': [monthly_sales * (overstock_rate / 100) * 12, 
                 monthly_sales * (overstock_rate / 100) * 12 - savings]
    })
    
    fig_roi = go.Figure(data=[
        go.Bar(x=savings_breakdown['Category'], 
               y=savings_breakdown['Cost'],
               marker_color=['#EF553B', '#00CC96'])
    ])
    
    fig_roi.update_layout(
        title="Annual Inventory Cost Comparison" if lang == 'en' else "Yıllık Stok Maliyeti Karşılaştırması",
        showlegend=False,
        height=300
    )
    
    st.plotly_chart(fig_roi, use_container_width=True)
