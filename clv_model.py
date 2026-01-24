import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

def run(lang='en'):
    content = {
        "title": {
            "en": "Customer Segmentation Analysis",
            "tr": "Müşteri Segmentasyon Uzayı"
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
        "how_it_works": {"en": "🔍 How It Works", "tr": "🔍 Nasıl Çalışır?"},
        "workflow": {
            "en": """
            **RFM Clustering Pipeline:**
            
            1. **RFM Calculation** → Recency (days since last purchase), Frequency (# purchases), Monetary (total spent)
            2. **Standardization** → Scale features using StandardScaler (mean=0, std=1)
            3. **K-Means Clustering** → Unsupervised learning to find 4 natural customer groups
            4. **Segment Labeling** → Assign business-friendly names based on spending patterns
            5. **Action Planning** → Tailored marketing strategies per segment
            
            **Use Case:** Upload your own customer data (columns: Recency, Frequency, Monetary) to segment your audience.
            """,
            "tr": """
            **RFM Kümeleme Akışı:**
            
            1. **RFM Hesaplama** → Yenilik (son alışveriş), Sıklık (alışveriş sayısı), Parasal Değer (toplam harcama)
            2. **Standardizasyon** → StandardScaler ile özellikleri ölçeklendir (ort=0, std=1)
            3. **K-Means Kümeleme** → Denetimsiz öğrenme ile 4 doğal müşteri grubu bul
            4. **Segment İsimlendirme** → Harcama paternlerine göre iş dostu isimler ver
            5. **Aksiyon Planı** → Her segment için özel pazarlama stratejileri
            
            **Kullanım:** Kendi müşteri verinizi yükleyin (sütunlar: Recency, Frequency, Monetary) ve kitlenizi segmentlere ayırın.
            """
        },
        "performance": {"en": "📊 Clustering Quality", "tr": "📊 Kümeleme Kalitesi"},
        "segments": {
            "en": ["Champions", "Loyal", "Potential", "At Risk"],
            "tr": ["Şampiyonlar", "Sadık", "Potansiyel", "Riskli"]
        },
        "axis": {
            "en": {'Recency': 'Recency', 'Frequency': 'Frequency', 'Monetary': 'Monetary'},
            "tr": {'Recency': 'Yenilik', 'Frequency': 'Sıklık', 'Monetary': 'Harcama'}
        },
        "upload_label": {"en": "📂 Upload Your Customer Data (CSV)", "tr": "📂 Müşteri Verinizi Yükleyin (CSV)"},
        "upload_help": {"en": "Required columns: Recency, Frequency, Monetary", "tr": "Gerekli sütunlar: Recency, Frequency, Monetary"},
        "segment_stats": {"en": "Segment Statistics", "tr": "Segment İstatistikleri"},
        "marketing_actions": {"en": "💡 Marketing Actions by Segment", "tr": "💡 Segmentlere Göre Pazarlama Aksiyonları"}
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

    # DOSYA YÜKLEME
    uploaded_file = st.file_uploader(
        content["upload_label"][lang],
        type=["csv"],
        help=content["upload_help"][lang]
    )

    @st.cache_data
    def get_rfm_data():
        np.random.seed(42)
        data = pd.concat([
            pd.DataFrame({'Recency': np.random.randint(1, 30, 100), 'Frequency': np.random.randint(20, 50, 100), 'Monetary': np.random.normal(5000, 1000, 100)}),
            pd.DataFrame({'Recency': np.random.randint(1, 30, 150), 'Frequency': np.random.randint(1, 5, 150), 'Monetary': np.random.normal(500, 100, 150)}),
            pd.DataFrame({'Recency': np.random.randint(100, 365, 150), 'Frequency': np.random.randint(1, 10, 150), 'Monetary': np.random.normal(1000, 300, 150)}),
            pd.DataFrame({'Recency': np.random.randint(30, 90, 100), 'Frequency': np.random.randint(5, 15, 100), 'Monetary': np.random.normal(2000, 500, 100)})
        ]).reset_index(drop=True)
        return data

    # VERİ YÜKLEME KONTROLÜ
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if not all(col in df.columns for col in ['Recency', 'Frequency', 'Monetary']):
                st.error("❌ CSV must contain: Recency, Frequency, Monetary columns")
                df = get_rfm_data()
            else:
                st.success("✅ Data uploaded successfully!" if lang == 'en' else "✅ Veri başarıyla yüklendi!")
        except Exception as e:
            st.error(f"Error: {e}")
            df = get_rfm_data()
    else:
        st.info("Using demo data..." if lang == 'en' else "Demo verisi kullanılıyor...")
        df = get_rfm_data()

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(scaled_data)

    # Silhouette Score (Kümeleme Kalitesi)
    silhouette_avg = silhouette_score(scaled_data, df['Cluster'])

    sorted_idx = df.groupby('Cluster')['Monetary'].mean().sort_values(ascending=False).index
    mapping = {old: new for old, new in zip(sorted_idx, content["segments"][lang])}
    df['Segment'] = df['Cluster'].map(mapping)

    # PERFORMANS METRİĞİ
    st.subheader(content["performance"][lang])
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Silhouette Score", f"{silhouette_avg:.3f}", 
                help="Clustering quality (-1 to 1). Higher is better. >0.5 is excellent.")
    col2.metric("Number of Clusters", "4", help="K-Means with 4 customer segments")
    col3.metric("Total Customers", f"{len(df):,}", help="Dataset size")

    # 3D GÖRSEL
    color_map = {
        content["segments"][lang][0]: "#00CC96",
        content["segments"][lang][1]: "#636EFA",
        content["segments"][lang][2]: "#FFA15A",
        content["segments"][lang][3]: "#EF553B"
    }

    fig = px.scatter_3d(
        df, x='Recency', y='Frequency', z='Monetary', color='Segment',
        color_discrete_map=color_map, opacity=0.6, size_max=10,
        labels=content["axis"][lang], height=600
    )
    
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

    st.plotly_chart(fig, use_container_width=True)

    # SEGMENT İSTATİSTİKLERİ
    st.divider()
    st.subheader(content["segment_stats"][lang])
    
    segment_summary = df.groupby('Segment').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean'
    }).round(2)
    
    segment_summary['Count'] = df.groupby('Segment').size()
    segment_summary['Percentage'] = (segment_summary['Count'] / len(df) * 100).round(1)
    
    st.dataframe(segment_summary, use_container_width=True)

    # PAZARLAMA AKSİYONLARI
    st.divider()
    st.subheader(content["marketing_actions"][lang])
    
    actions = {
        "en": {
            "Champions": "🎯 **VIP Treatment:** Exclusive early access, loyalty rewards, personal account manager",
            "Loyal": "💎 **Retention Focus:** Premium membership offers, cross-sell opportunities",
            "Potential": "🚀 **Activation Campaigns:** Limited-time discounts, engagement emails",
            "At Risk": "⚠️ **Win-back Strategy:** Survey for feedback, special reactivation offers"
        },
        "tr": {
            "Şampiyonlar": "🎯 **VIP Muamele:** Özel erken erişim, sadakat ödülleri, kişisel hesap yöneticisi",
            "Sadık": "💎 **Elde Tutma:** Premium üyelik teklifleri, çapraz satış fırsatları",
            "Potansiyel": "🚀 **Aktivasyon:** Sınırlı süreli indirimler, etkileşim e-postaları",
            "Riskli": "⚠️ **Geri Kazanma:** Geri bildirim anketi, özel reaktivasyon teklifleri"
        }
    }
    
    for segment in content["segments"][lang]:
        st.markdown(actions[lang][segment])

    if lang == 'tr':
        st.success("🎯 Strateji: En yüksek CLV'ye sahip 'Şampiyonlar' segmentine odaklanın.")
    else:
        st.success("🎯 Strategy: Focus on 'Champions' segment with highest CLV potential.")
