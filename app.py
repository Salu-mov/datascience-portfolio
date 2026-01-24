import streamlit as st
import demand_forecasting
import clv_model
import pricing_model
import ab_test_simulator

# Sayfa Ayarları
st.set_page_config(
    page_title="Ulaş Aksaç | Portfolyo",
    page_icon="📊",
    layout="wide"
)

# --- DİL AYARLARI (SESSION STATE) ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'tr'

# --- SOL MENÜ (NAVİGASYON) ---
with st.sidebar:
    # 1. Dil Seçici En Üstte
    lang_choice = st.selectbox("Language / Dil", ["Türkçe", "English"])
    st.session_state.lang = 'tr' if lang_choice == "Türkçe" else 'en'
    lang = st.session_state.lang

    # 2. Profil
    st.title("Ulaş Aksaç")

    role = "Data Scientist & Machine Learning & Data Analysis" if lang == 'tr' else "Data Scientist & Machine Learning & Data Analysis"
    st.caption(role)

    st.markdown("---")

    # 3. Menü Seçenekleri
    menu_dict = {
        "tr": [
            "🏠 Ana Sayfa",
            "📈 Talep Tahmini (Yapay Zeka)",
            "🛍️ Müşteri Analizi (CLV)",
            "💰 Gayrimenkul Değerleme",
            "🧪 A/B Test Analizi"  # YENİ
        ],
        "en": [
            "🏠 Home",
            "📈 Demand Forecasting (AI)",
            "🛍️ Customer Analysis (CLV)",
            "💰 Real Estate Valuation",
            "🧪 A/B Test Analyzer"  # YENİ
        ]
    }# YENİ
        ],
        "en": [
            "🏠 Home",
            "📈 Demand Forecasting (AI)",
            "🛍️ Customer Analysis (CLV)",
            "💰 Real Estate Valuation",
            "🧪 A/B Test Analyzer"  # YENİ
        ]
    }

    label = "📌 Proje Seçimi:" if lang == 'tr' else "📌 Project Selection:"
    selection = st.radio(label, menu_dict[lang])

    st.markdown("---")
    contact = "İletişim" if lang == 'tr' else "Contact"

    # İLETİŞİM KISMI
    st.info(
        f"**{contact}:**\n\n🔗 [LinkedIn](https://www.linkedin.com/in/ulasaksac/)\n💻 [GitHub](https://github.com/Salu-mov)")

# --- İÇERİK YÖNETİMİ ---

# A) ANA SAYFA (HOME)
if selection in ["🏠 Ana Sayfa", "🏠 Home"]:

    # Metin Sözlüğü
    content = {
        "title": {
            "tr": "🚀 Veri Bilimi ve Karar Destek Sistemleri",
            "en": "🚀 Data Science & Decision Support Systems"
        },
        "intro": {
            "tr": """
            ### Merhaba, Portfolyoma Hoş Geldiniz.
            Bu platformda, karmaşık verilerin nasıl somut iş değerine dönüştürülebileceğini gösteren uçtan uca çözümler sunuyorum. 
            Projelerim; **Makine Öğrenmesi, Derin Öğrenme ve İstatistiksel Optimizasyon** teknikleri kullanılarak hazırlanmıştır.
            """,
            "en": """
            ### Hello, Welcome to My Portfolio.
            Here, I present end-to-end solutions showing how complex data is transformed into tangible business value.
            My projects are built using **Machine Learning, Deep Learning, and Statistical Optimization** techniques.
            """
        },
        "tech_title": {"tr": "🧠 Teknik Derinlik", "en": "🧠 Technical Depth"},
        "tech_desc": {
            "tr": "**Modeller:** XGBoost, LSTM, Random Forest, K-Means Clustering.\n\nİleri seviye algoritmalar ile tahminleme ve sınıflandırma.",
            "en": "**Models:** XGBoost, LSTM, Random Forest, K-Means Clustering.\n\nPrediction and classification with advanced algorithms."
        },
        "stack_title": {"tr": "🛠️ Teknoloji Stack", "en": "🛠️ Tech Stack"},
        "stack_desc": {
            "tr": "**Araçlar:** Python, Pandas, Scikit-Learn, Plotly, Streamlit.\n\nModern veri bilimi kütüphaneleri ve interaktif dashboard tasarımı.",
            "en": "**Tools:** Python, Pandas, Scikit-Learn, Plotly, Streamlit.\n\nModern data science libraries and interactive dashboard design."
        },
        "biz_title": {"tr": "💼 İş Odaklılık", "en": "💼 Business Focus"},
        "biz_desc": {
            "tr": "**KPI:** ROI Hesaplama, Stok Optimizasyonu, Müşteri Değeri.\n\nSadece kod değil, şirkete kazandırdığı para odaklı çözümler.",
            "en": "**KPI:** ROI Calculation, Inventory Optimization, Customer Value.\n\nSolutions focused on business value, not just code."
        },
        "gallery": {"tr": "📂 Proje Galerisi", "en": "📂 Project Gallery"},
        "info": {"tr": "👈 Canlı demoları incelemek için sol menüden proje seçebilirsiniz.",
                 "en": "👈 Select a project from the left menu to view live demos."}
    }

    st.title(content["title"][lang])
    st.markdown(content["intro"][lang])
    st.divider()

    # 3 Kolonlu Yapı
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader(content["tech_title"][lang])
        st.success(content["tech_desc"][lang])
    with c2:
        st.subheader(content["stack_title"][lang])
        st.warning(content["stack_desc"][lang])
    with c3:
        st.subheader(content["biz_title"][lang])
        st.error(content["biz_desc"][lang])

    st.divider()

    st.subheader(content["gallery"][lang])
    st.caption(content["info"][lang])

    # Alt kısımdaki Proje Özet Kartları (4 proje)
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)

    p_desc = {
        "demand": {"tr": "Gelecek satışları tahmin eden ve stok maliyetlerini optimize eden AI sistemi.",
                   "en": "AI system predicting future sales to optimize inventory costs."},
        "clv": {"tr": "Müşterileri harcama alışkanlıklarına göre segmentlere ayıran pazarlama motoru.",
                "en": "Marketing engine segmenting customers based on spending habits."},
        "real": {"tr": "İstanbul emlak verileriyle eğitilmiş saniyelik fiyat tahmin modeli.",
                 "en": "Instant price prediction model trained on Istanbul real estate data."},
        "ab": {"tr": "Kampanya etkisini istatistiksel olarak doğrulayan hipotez test aracı.",
               "en": "Hypothesis testing tool to validate campaign effectiveness statistically."}
    }

    with col_p1:
        st.markdown("### 📈 " + ("Talep Tahmini" if lang == 'tr' else "Demand Forecast"))
        st.info(p_desc["demand"][lang])
    with col_p2:
        st.markdown("### 🛍️ " + ("Müşteri Analizi" if lang == 'tr' else "Customer Analysis"))
        st.warning(p_desc["clv"][lang])
    with col_p3:
        st.markdown("### 💰 " + ("Emlak Değerleme" if lang == 'tr' else "Real Estate"))
        st.error(p_desc["real"][lang])
    with col_p4:
        st.markdown("### 🧪 " + ("A/B Test" if lang == 'tr' else "A/B Testing"))
        st.success(p_desc["ab"][lang])

# B) MODÜL ÇAĞRILARI
elif selection in ["📈 Talep Tahmini (Yapay Zeka)", "📈 Demand Forecasting (AI)"]:
    demand_forecasting.run(lang)

elif selection in ["🛍️ Müşteri Analizi (CLV)", "🛍️ Customer Analysis (CLV)"]:
    clv_model.run(lang)

elif selection in ["💰 Gayrimenkul Değerleme", "💰 Real Estate Valuation"]:
    pricing_model.run(lang)

elif selection in ["🧪 A/B Test Analizi", "🧪 A/B Test Analyzer"]:
    ab_test_simulator.run(lang)
