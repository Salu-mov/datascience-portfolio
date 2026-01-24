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

    role = "Data Scientist & Machine Learning & Data Analysis"
    st.caption(role)

    st.markdown("---")

    # 3. Menü Seçenekleri
    menu_dict = {
        "tr": [
            "🏠 Ana Sayfa",
            "📈 Talep Tahmini (Yapay Zeka)",
            "🛍️ Müşteri Analizi (CLV)",
            "💰 Gayrimenkul Değerleme",
            "🧪 A/B Test Analizi"
        ],
        "en": [
            "🏠 Home",
            "📈 Demand Forecasting (AI)",
            "🛍️ Customer Analysis (CLV)",
            "💰 Real Estate Valuation",
            "🧪 A/B Test Analyzer"
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
            "tr": "Veri Bilimi ve Karar Destek Sistemleri",
            "en": "Data Science & Decision Support Systems"
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

    # IMPACT STORIES BÖLÜMÜ
    st.divider()
    
    impact_title = "💡 Gerçek Dünya Etkileri" if lang == 'tr' else "💡 Real-World Impact Stories"
    st.subheader(impact_title)
    
    # 3 Senaryo Tabları
    tab_names = ["🏪 Perakende", "🛒 E-Ticaret", "🏢 Emlak"] if lang == 'tr' else ["🏪 Retail", "🛒 E-Commerce", "🏢 Real Estate"]
    tab1, tab2, tab3 = st.tabs(tab_names)
    
    with tab1:
        if lang == 'tr':
            st.markdown("""
            ### 📊 Senaryo: 50 Mağazalı Perakende Zinciri
            
            **Durum:**
            - Aylık ortalama satış: ₺15M
            - Mevcut stok yönetimi: Manuel tahmin + güvenlik stoğu
            
            **Sorun:**
            ```
            ❌ Fazla Stok: %28 → ₺4.2M atıl sermaye
            ❌ Stok Eksikliği: %12 → ₺1.8M kayıp satış
            ❌ Fire/Eskime: %8 → ₺1.2M zarar
            
            Toplam Yıllık Kayıp: ₺7.2M
            ```
            
            **AI Talep Tahmini Sonrası:**
            ```
            ✅ Fazla Stok: %28 → %9 (68% iyileşme)
            ✅ Stok Eksikliği: %12 → %3 (75% iyileşme)
            ✅ Fire Azalması: %8 → %2
            
            Net Tasarruf: ₺5.1M/yıl
            ROI: İlk 6 ayda kendini amorti etti
            ```
            
            **Ek Faydalar:**
            - Nakit akışı iyileşmesi
            - Depo alanı optimizasyonu (%40 azalma)
            - Satın alma ekibi verimliliği (%60 zaman tasarrufu)
            """)
        else:
            st.markdown("""
            ### 📊 Scenario: 50-Store Retail Chain
            
            **Situation:**
            - Monthly average sales: ₺15M
            - Current inventory: Manual forecasting + safety stock
            
            **Problem:**
            ```
            ❌ Overstock: 28% → ₺4.2M tied capital
            ❌ Stockouts: 12% → ₺1.8M lost sales
            ❌ Waste/Obsolescence: 8% → ₺1.2M loss
            
            Total Annual Loss: ₺7.2M
            ```
            
            **After AI Demand Forecasting:**
            ```
            ✅ Overstock: 28% → 9% (68% improvement)
            ✅ Stockouts: 12% → 3% (75% improvement)
            ✅ Waste Reduction: 8% → 2%
            
            Net Savings: ₺5.1M/year
            ROI: Paid for itself in first 6 months
            ```
            
            **Additional Benefits:**
            - Improved cash flow
            - Warehouse space optimization (40% reduction)
            - Procurement team efficiency (60% time saved)
            """)
    
    with tab2:
        if lang == 'tr':
            st.markdown("""
            ### 🎯 Senaryo: Online Moda Platformu (50K Aktif Müşteri)
            
            **Durum:**
            - Yıllık pazarlama bütçesi: ₺2.4M
            - Generic kampanyalar (tüm müşterilere aynı mesaj)
            
            **Sorun:**
            ```
            ❌ Düşük Dönüşüm: Ortalama %2.1
            ❌ Yüksek Churn: %35 müşteri kaybı
            ❌ Düşük CLV: Ortalama ₺850/müşteri
            
            Pazarlama ROI: %140 (sektör ortalaması)
            ```
            
            **Müşteri Segmentasyonu Sonrası:**
            ```
            Şampiyonlar (%18 - 9,000 kişi):
            ├── Özel VIP kampanyalar
            ├── Dönüşüm: %2.1 → %8.5
            ├── CLV: ₺850 → ₺3,200
            └── Gelir Katkısı: %62
            
            Sadık Müşteriler (%24 - 12,000 kişi):
            ├── Cross-sell kampanyaları
            ├── Dönüşüm: %2.1 → %5.2
            └── Gelir Katkısı: %28
            
            At Risk (%15 - 7,500 kişi):
            ├── Win-back indirimleri
            ├── Churn Önleme: %35 → %18
            └── Kurtarılan Gelir: ₺1.2M/yıl
            ```
            
            **Sonuç:**
            ```
            ✅ Pazarlama ROI: %140 → %380 (+171%)
            ✅ Customer Retention: %65 → %82
            ✅ Bütçe Verimliliği: Aynı sonuç %45 daha az harcama
            
            Net Etki: ₺3.8M ek gelir, ₺1.1M tasarruf
            ```
            """)
        else:
            st.markdown("""
            ### 🎯 Scenario: Online Fashion Platform (50K Active Customers)
            
            **Situation:**
            - Annual marketing budget: ₺2.4M
            - Generic campaigns (same message to all)
            
            **Problem:**
            ```
            ❌ Low Conversion: Average 2.1%
            ❌ High Churn: 35% customer loss
            ❌ Low CLV: Average ₺850/customer
            
            Marketing ROI: 140% (industry average)
            ```
            
            **After Customer Segmentation:**
            ```
            Champions (18% - 9,000 people):
            ├── VIP exclusive campaigns
            ├── Conversion: 2.1% → 8.5%
            ├── CLV: ₺850 → ₺3,200
            └── Revenue Contribution: 62%
            
            Loyal Customers (24% - 12,000 people):
            ├── Cross-sell campaigns
            ├── Conversion: 2.1% → 5.2%
            └── Revenue Contribution: 28%
            
            At Risk (15% - 7,500 people):
            ├── Win-back discounts
            ├── Churn Prevention: 35% → 18%
            └── Saved Revenue: ₺1.2M/year
            ```
            
            **Results:**
            ```
            ✅ Marketing ROI: 140% → 380% (+171%)
            ✅ Customer Retention: 65% → 82%
            ✅ Budget Efficiency: Same results with 45% less spend
            
            Net Impact: ₺3.8M additional revenue, ₺1.1M savings
            ```
            """)
    
    with tab3:
        if lang == 'tr':
            st.markdown("""
            ### 🏠 Senaryo: Emlak Danışmanlık Ofisi (İstanbul)
            
            **Durum:**
            - Günlük müşteri talebi: 30-50 konut değerlendirmesi
            - Manuel ekspertiz süreci: 2-3 saat/konut
            
            **Sorun:**
            ```
            ❌ İnsan Gücü: 50 talep × 2.5 saat = 125 saat/gün
            ❌ Maliyet: 125 saat × ₺300 = ₺37,500/gün
            ❌ Yanıt Süresi: 24-48 saat (rekabet dezavantajı)
            ❌ Tutarsızlık: Farklı danışmanlar %15 farklı fiyat veriyor
            
            Aylık Operasyonel Maliyet: ₺825K (22 iş günü)
            Kaçırılan Fırsatlar: %40 müşteri rakiplere gidiyor
            ```
            
            **AI Değerleme Sistemi Sonrası:**
            ```
            ✅ Değerleme Süresi: 2.5 saat → 5 dakika (97% azalma)
            ✅ Kapasite: Günde 50 → 500 talep yanıtlanabiliyor
            ✅ Yanıt Süresi: 24-48 saat → Anında
            ✅ Tutarlılık: %15 varyasyon → %5 varyasyon
            
            Maliyet Azalması:
            ├── Ekspertiz maliyeti: ₺825K → ₺35K/ay
            ├── Tasarruf: ₺790K/ay (₺9.5M/yıl)
            
            Gelir Artışı:
            ├── Müşteri kaybı: %40 → %8
            ├── Ek anlaşmalar: +120/ay
            ├── Ortalama komisyon: ₺15K
            └── Ek gelir: ₺1.8M/ay (₺21.6M/yıl)
            ```
            
            **ROI Analizi:**
            ```
            Sistem Geliştirme: ₺150K (bir kerelik)
            İlk Yıl Faydası: ₺31.1M
            ROI: 20,733% 🚀
            
            Geri ödeme süresi: 4.8 gün
            ```
            """)
        else:
            st.markdown("""
            ### 🏠 Scenario: Real Estate Consultancy Office (Istanbul)
            
            **Situation:**
            - Daily client requests: 30-50 property valuations
            - Manual appraisal process: 2-3 hours/property
            
            **Problem:**
            ```
            ❌ Labor: 50 requests × 2.5 hours = 125 hours/day
            ❌ Cost: 125 hours × ₺300 = ₺37,500/day
            ❌ Response Time: 24-48 hours (competitive disadvantage)
            ❌ Inconsistency: Different appraisers give 15% varying prices
            
            Monthly Operational Cost: ₺825K (22 business days)
            Lost Opportunities: 40% clients go to competitors
            ```
            
            **After AI Valuation System:**
            ```
            ✅ Appraisal Time: 2.5 hours → 5 minutes (97% reduction)
            ✅ Capacity: 50 → 500 requests/day handled
            ✅ Response Time: 24-48 hours → Instant
            ✅ Consistency: 15% variance → 5% variance
            
            Cost Reduction:
            ├── Appraisal cost: ₺825K → ₺35K/month
            ├── Savings: ₺790K/month (₺9.5M/year)
            
            Revenue Increase:
            ├── Client loss: 40% → 8%
            ├── Additional deals: +120/month
            ├── Average commission: ₺15K
            └── Additional revenue: ₺1.8M/month (₺21.6M/year)
            ```
            
            **ROI Analysis:**
            ```
            System Development: ₺150K (one-time)
            First Year Benefit: ₺31.1M
            ROI: 20,733% 🚀
            
            Payback period: 4.8 days
            ```
            """)
    
    st.divider()

    # Alt kısımdaki Proje Özet Kartları
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

