import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import datetime 

def run(lang='en'):
    content = {
        "title": {
            "en": "AI-Powered Demand Forecasting",
            "tr": "AI Tabanlı Talep Öngörü Sistemi"
        },
        "summary": {
            "en": "Project Overview & Business Value",
            "tr": "ℹ️ Proje Özeti ve İş Değeri"
        },
        "metrics": {
            "en": [
                "**🎯 Goal:** Predict future sales to reduce inventory costs by 20-30%.",
                "**🧠 Tech:** XGBoost Regressor, Lag Features & Time Series Analysis.",
                "**💰 Impact:** Prevention of overstocking costs and optimized supply chain management."
            ],
            "tr": [
                "**🎯 Amaç:** Satış tahminleri yaparak stok maliyetlerini %20-30 oranında düşürmek.",
                "**🧠 Teknik:** XGBoost Regressor, Lag Features ve Zaman Serisi Analizi.",
                "**💰 Kazanç:** Yanlış stoklama maliyetinin önlenmesi ve optimize tedarik yönetimi."
            ]
        },
        "chart_title": {
            "en": "Forecast Performance (RMSE: {:.2f})",
            "tr": "Tahmin Performansı (RMSE: {:.2f})"
        },
        "alert": {
            "en": "💡 **System Suggestion:** Reorder required when stock level falls below **{:.0f}** units.",
            "tr": "💡 **Sistem Önerisi:** Stok seviyesi **{:.0f}** adetin altına düştüğünde sipariş verilmelidir."
        }
    }

    with st.expander(content["summary"][lang], expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.markdown(content["metrics"][lang][0])
        c2.markdown(content["metrics"][lang][1])
        c3.markdown(content["metrics"][lang][2])

    st.subheader(content["title"][lang])

    # --- TARİH OLUŞTURMA ---
    @st.cache_data
    def generate_synthetic_data():
        start_date = datetime.date(2023, 1, 1)
        dates = pd.date_range(start=start_date, periods=730, freq='D')
        
        trend = np.linspace(0, 50, 730)
        seasonality = 20 * np.sin(np.linspace(0, 3 * np.pi, 730))
        noise = np.random.normal(0, 10, 730)
        sales = 100 + trend + seasonality + noise
        return pd.DataFrame({"Date": dates, "Sales": np.maximum(sales, 0)})

    df = generate_synthetic_data()

    # Feature Engineering
    df['lag_7'] = df['Sales'].shift(7)
    df['rolling_mean'] = df['Sales'].shift(1).rolling(7).mean()
    df['day_of_week'] = df['Date'].dt.dayofweek
    df_clean = df.dropna()

    # Model Hazırlığı
    X = df_clean[['lag_7', 'rolling_mean', 'day_of_week']]
    y = df_clean['Sales']

    train_size = int(len(X) * 0.9)
    X_train, y_train = X.iloc[:train_size], y.iloc[:train_size]
    X_test, y_test = X.iloc[train_size:], y.iloc[train_size:]

    model = XGBRegressor(n_estimators=100, learning_rate=0.1)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    # Grafik
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_clean['Date'].iloc[train_size:], y=y_test, name="Actual" if lang == 'en' else "Gerçek"))
    fig.add_trace(go.Scatter(x=df_clean['Date'].iloc[train_size:], y=predictions, name="Forecast" if lang == 'en' else "Tahmin", line=dict(dash='dash')))
    fig.update_layout(title=content["chart_title"][lang].format(rmse))
    
    st.plotly_chart(fig, use_container_width=True)

    safety_stock = predictions.mean() * 0.2
    reorder_point = predictions.mean() * 5 + safety_stock
    
    st.info(content["alert"][lang].format(reorder_point))
