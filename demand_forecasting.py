import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
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
        "chart_title": {"en": "Sales Forecast (Past vs Future)", "tr": "Satış Tahmini (Geçmiş ve Gelecek)"},
        "alert": {"en": "💡 **Insight:** Reorder point is **{:.0f}** units.", "tr": "💡 **Analiz:** Sipariş noktası: **{:.0f}** adet."},
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

    st.subheader(content["title"][lang])

    # --- DOSYA YÜKLEME ALANI ---
    uploaded_file = st.file_uploader(content["upload_label"][lang], type=["csv"], help=content["upload_help"][lang])

    # --- VERİ İŞLEME FONKSİYONU ---
    def process_data(df_input):
        # Tarih formatını düzelt
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

    # --- AKIŞ KONTROLÜ (YÜKLENDİ Mİ?) ---
    df = None
    
    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            # Sütun kontrolü
            if 'Date' in df_uploaded.columns and 'Sales' in df_uploaded.columns:
                df = process_data(df_uploaded)
                st.success("✅ Veri başarıyla yüklendi!" if lang == 'tr' else "✅ Data uploaded successfully!")
            else:
                st.error(content["error_cols"][lang])
        except Exception as e:
            st.error(f"Hata/Error: {e}")

    # Eğer dosya yoksa veya hatalıysa Demo verisi kullan
    if df is None:
        if uploaded_file is None:
            st.info(content["use_demo"][lang])
        df_raw = generate_synthetic_data()
        df = process_data(df_raw)

    # --- MODEL EĞİTİMİ ---
    X = df[['lag_7', 'rolling_mean', 'day_of_week']]
    y = df['Sales']

    
    split_point = int(len(X) * 0.9)
    X_train, y_train = X.iloc[:split_point], y.iloc[:split_point]
    X_test, y_test = X.iloc[split_point:], y.iloc[split_point:]

    
    model = XGBRegressor(n_estimators=100, learning_rate=0.05)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    # --- GRAFİK KISMI ---
    fig = go.Figure()

    # 1. Geçmiş Veri
    fig.add_trace(go.Scatter(
        x=df['Date'].iloc[:split_point], 
        y=y_train, 
        name="Geçmiş/History",
        line=dict(color='gray', width=1),
        opacity=0.6
    ))

    # 2. Gerçek Değerler
    fig.add_trace(go.Scatter(
        x=df['Date'].iloc[split_point:], 
        y=y_test, 
        name="Gerçek/Actual",
        line=dict(color='#636EFA', width=2)
    ))

    # 3. Tahmin
    fig.add_trace(go.Scatter(
        x=df['Date'].iloc[split_point:], 
        y=predictions, 
        name="AI Tahmini/Forecast",
        line=dict(color='#EF553B', width=3, dash='dot')
    ))

    # Ayırıcı Çizgi
    split_date = df['Date'].iloc[split_point]
    fig.add_vline(x=split_date, line_width=2, line_dash="dash", line_color="green")

    fig.update_layout(title=content["chart_title"][lang].format(rmse), template="plotly_white", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    reorder_point = predictions.mean()
    st.info(content["alert"][lang].format(reorder_point))
