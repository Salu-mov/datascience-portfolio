import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def run(lang='en'):
    content = {
        "title": {
            "en": "Customer Segmentation Analysis (3D)",
            "tr": "Müşteri Segmentasyon Uzayı (3D)"
        },
        "summary": {
            "en": "Project Overview & Business Value",
            "tr": "ℹ️ Proje Özeti ve İş Değeri"
        },
        "metrics": {
            "en": [
                "**🎯 Goal:** Group customers by behavior to create personalized marketing strategies.",
                "**🧠 Tech:** RFM Analysis & K-Means Clustering (Unsupervised Learning).",
                "**💰 Impact:** Increase in Customer Retention Rate and marketing budget efficiency."
            ],
            "tr": [
                "**🎯 Amaç:** Müşterileri davranışlarına göre gruplayarak kişiselleştirilmiş kampanya yönetimi.",
                "**🧠 Teknik:** RFM Analizi ve K-Means Clustering (Denetimsiz Öğrenme).",
                "**💰 Kazanç:** Müşteri elde tutma oranında (Retention) artış ve pazarlama verimliliği."
            ]
        },
        "segments": {
            "en": ["Champions", "Loyal", "Potential", "At Risk"],
            "tr": ["Şampiyonlar", "Sadık", "Potansiyel", "Riskli"]
        },
        "axis": {
            "en": {'Recency': 'Recency', 'Frequency': 'Frequency', 'Monetary': 'Monetary'},
            "tr": {'Recency': 'Yenilik', 'Frequency': 'Sıklık', 'Monetary': 'Harcama'}
        }
    }

    with st.expander(content["summary"][lang], expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.markdown(content["metrics"][lang][0])
        c2.markdown(content["metrics"][lang][1])
        c3.markdown(content["metrics"][lang][2])

    st.subheader(content["title"][lang])

    @st.cache_data
    def get_rfm_data():
        np.random.seed(42)
        n_samples = 500
        data = pd.concat([
            pd.DataFrame({'Recency': np.random.randint(1, 30, 100), 'Frequency': np.random.randint(20, 50, 100), 'Monetary': np.random.normal(5000, 1000, 100)}),
            pd.DataFrame({'Recency': np.random.randint(1, 30, 150), 'Frequency': np.random.randint(1, 5, 150), 'Monetary': np.random.normal(500, 100, 150)}),
            pd.DataFrame({'Recency': np.random.randint(100, 365, 150), 'Frequency': np.random.randint(1, 10, 150), 'Monetary': np.random.normal(1000, 300, 150)}),
            pd.DataFrame({'Recency': np.random.randint(30, 90, 100), 'Frequency': np.random.randint(5, 15, 100), 'Monetary': np.random.normal(2000, 500, 100)})
        ]).reset_index(drop=True)
        return data

    df = get_rfm_data()
    
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(scaled_data)

    sorted_idx = df.groupby('Cluster')['Monetary'].mean().sort_values(ascending=False).index
    mapping = {old: new for old, new in zip(sorted_idx, content["segments"][lang])}
    df['Segment'] = df['Cluster'].map(mapping)

    color_map = {
        content["segments"][lang][0]: "#00CC96",
        content["segments"][lang][1]: "#636EFA",
        content["segments"][lang][2]: "#FFA15A",
        content["segments"][lang][3]: "#EF553B"
    }

    fig = px.scatter_3d(
        df, x='Recency', y='Frequency', z='Monetary', color='Segment',
        color_discrete_map=color_map, opacity=0.6, size_max=10,
        labels=content["axis"][lang]
    )
    
    # --- LEGEND AYARI ---
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        legend=dict(
            orientation="h",  
            yanchor="bottom",
            y=1.02,            
            xanchor="right",
            x=1               
        )
    )
    # ---------------------------------------

    st.plotly_chart(fig, use_container_width=True)
    
    if lang == 'tr':
        st.success("🎯 Strateji: 'Segment 0' grubundaki müşteriler için özel sadakat programı başlatılması önerilir.")
    else:
        st.success("🎯 Strategy: A loyalty program is recommended for 'Segment 0' customers.")
