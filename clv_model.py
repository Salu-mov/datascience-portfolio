import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def run(lang='en'):
    content = {
        "title": {"en": "Customer Segmentation (3D + Radar)", "tr": "Müşteri Segmentasyonu (3D + Radar)"},
        "summary": {"en": "Project Overview", "tr": "ℹ️ Proje Özeti"},
        "metrics": {
            "en": ["**🎯 Goal:** Personalize marketing.", "**🧠 Tech:** RFM & K-Means.", "**💰 Impact:** Increase Retention."],
            "tr": ["**🎯 Amaç:** Kişiselleştirilmiş pazarlama.", "**🧠 Teknik:** RFM & K-Means.", "**💰 Kazanç:** Müşteri sadakati."]
        },
        "segments": {"en": ["VIP", "Loyal", "Potential", "At Risk"], "tr": ["VIP", "Sadık", "Potansiyel", "Riskli"]},
        "radar_title": {"en": "Average Profile of Selected Segment", "tr": "Seçilen Segmentin Ortalama Profili"}
    }

    with st.expander(content["summary"][lang], expanded=True):
        st.markdown(" | ".join(content["metrics"][lang]))

    st.subheader(content["title"][lang])

    @st.cache_data
    def get_rfm_data():
        np.random.seed(42)
        # Veri üretimi (Aynı kalıyor)
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

    # Segment İsimlendirme
    sorted_idx = df.groupby('Cluster')['Monetary'].mean().sort_values(ascending=False).index
    mapping = {old: new for old, new in zip(sorted_idx, content["segments"][lang])}
    df['Segment'] = df['Cluster'].map(mapping)

    col1, col2 = st.columns([2, 1])

    with col1:
        # 3D Grafik
        fig_3d = px.scatter_3d(df, x='Recency', y='Frequency', z='Monetary', color='Segment', opacity=0.7)
        fig_3d.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=400)
        st.plotly_chart(fig_3d, use_container_width=True)

    with col2:
        # RADAR GRAFİĞİ (YENİ)
        st.write(f"**{content['radar_title'][lang]}**")
        selected_segment = st.selectbox("Segment:", df['Segment'].unique())
        
        # Seçilen segmentin ortalamalarını al ve 0-1 arasına normalize et (görsel için)
        avg_df = df.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean()
        normalized_df = (avg_df - avg_df.min()) / (avg_df.max() - avg_df.min())
        
        values = normalized_df.loc[selected_segment].values.tolist()
        values += values[:1] # Kapatmak için
        categories = ['Recency', 'Frequency', 'Monetary', 'Recency']

        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values, theta=categories, fill='toself', name=selected_segment
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False, height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_radar, use_container_width=True)
