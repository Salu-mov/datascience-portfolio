import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

def run(lang='en'):
    content = {
        "title": {"en": "A/B Test Statistical Analyzer", "tr": "A/B Test İstatistiksel Analiz"},
        "summary": {"en": "Project Overview & Business Value", "tr": "ℹ️ Proje Özeti ve İş Değeri"},
        "metrics": {
            "en": [
                "**🎯 Goal:** Determine if marketing changes significantly impact conversion rates.",
                "**🧠 Tech:** Hypothesis Testing (Z-test, Chi-square), Statistical Significance.",
                "**💰 Impact:** Optimize campaign budget by validating winning variants."
            ],
            "tr": [
                "**🎯 Amaç:** Pazarlama değişikliklerinin dönüşüm oranını anlamlı şekilde etkileyip etkilemediğini belirlemek.",
                "**🧠 Teknik:** Hipotez Testi (Z-test, Chi-square), İstatistiksel Anlamlılık.",
                "**💰 Kazanç:** Kazanan varyantı doğrulayarak kampanya bütçesini optimize etmek."
            ]
        },
        "how_it_works": {"en": "🔍 How It Works", "tr": "🔍 Nasıl Çalışır?"},
        "workflow": {
            "en": """
            **Hypothesis Testing Framework:**
            
            1. **Null Hypothesis (H₀):** Control and Test groups have the same conversion rate
            2. **Alternative Hypothesis (H₁):** Test group has different conversion rate
            3. **Statistical Test:** Two-proportion Z-test
            4. **Significance Level:** α = 0.05 (95% confidence)
            5. **Decision Rule:** If p-value < 0.05 → Reject H₀ (significant difference exists)
            
            **Interpretation:** Upload your A/B test results or use the simulator to see statistical validity.
            """,
            "tr": """
            **Hipotez Testi Çerçevesi:**
            
            1. **Sıfır Hipotezi (H₀):** Kontrol ve Test gruplarının dönüşüm oranı aynı
            2. **Alternatif Hipotez (H₁):** Test grubunun dönüşüm oranı farklı
            3. **İstatistiksel Test:** İki-oran Z-testi
            4. **Anlamlılık Seviyesi:** α = 0.05 (%95 güven)
            5. **Karar Kuralı:** p-değeri < 0.05 ise → H₀ red (anlamlı fark var)
            
            **Yorumlama:** A/B test sonuçlarınızı yükleyin veya simülatörü kullanarak istatistiksel geçerliliği görün.
            """
        },
        "simulator": {"en": "🎮 Interactive Simulator", "tr": "🎮 İnteraktif Simülatör"},
        "upload": {"en": "📂 Upload Your A/B Test Data", "tr": "📂 Kendi A/B Test Verinizi Yükleyin"},
        "results": {"en": "📊 Test Results", "tr": "📊 Test Sonuçları"},
        "conclusion": {"en": "Conclusion", "tr": "Sonuç"}
    }

    with st.expander(content["summary"][lang], expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.markdown(content["metrics"][lang][0])
        c2.markdown(content["metrics"][lang][1])
        c3.markdown(content["metrics"][lang][2])

    with st.expander(content["how_it_works"][lang], expanded=False):
        st.markdown(content["workflow"][lang])

    st.subheader(content["title"][lang])

    # DOSYA YÜKLEME
    uploaded_file = st.file_uploader(
        content["upload"][lang],
        type=["csv"],
        help="CSV format: group, conversions, visitors"
    )

    # SİMÜLATÖR VEYA GERÇEK VERİ
    use_simulator = uploaded_file is None

    if use_simulator:
        st.info("Using interactive simulator..." if lang == 'en' else "İnteraktif simülatör kullanılıyor...")
        
        st.subheader(content["simulator"][lang])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Control Group (A)**" if lang == 'en' else "**Kontrol Grubu (A)**")
            visitors_a = st.number_input("Visitors (A)" if lang == 'en' else "Ziyaretçi (A)", 1000, 100000, 10000, 1000)
            conv_rate_a = st.slider("Conversion Rate (A) %" if lang == 'en' else "Dönüşüm Oranı (A) %", 1.0, 20.0, 5.0, 0.1)
            conversions_a = int(visitors_a * conv_rate_a / 100)
        
        with col2:
            st.markdown("**Test Group (B)**" if lang == 'en' else "**Test Grubu (B)**")
            visitors_b = st.number_input("Visitors (B)" if lang == 'en' else "Ziyaretçi (B)", 1000, 100000, 10000, 1000)
            conv_rate_b = st.slider("Conversion Rate (B) %" if lang == 'en' else "Dönüşüm Oranı (B) %", 1.0, 20.0, 6.5, 0.1)
            conversions_b = int(visitors_b * conv_rate_b / 100)
        
        data = {
            'Group': ['Control (A)', 'Test (B)'],
            'Visitors': [visitors_a, visitors_b],
            'Conversions': [conversions_a, conversions_b],
            'Conversion_Rate': [conv_rate_a, conv_rate_b]
        }
        df = pd.DataFrame(data)
    
    else:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ Data loaded!" if lang == 'en' else "✅ Veri yüklendi!")
            df['Conversion_Rate'] = (df['Conversions'] / df['Visitors'] * 100).round(2)
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    # İSTATİSTİKSEL TEST
    st.divider()
    st.subheader(content["results"][lang])

    # Metrikler
    col1, col2, col3, col4 = st.columns(4)
    
    control = df[df['Group'].str.contains('A|Control', case=False, na=False)].iloc[0]
    test = df[df['Group'].str.contains('B|Test', case=False, na=False)].iloc[0]
    
    col1.metric("Control CVR", f"{control['Conversion_Rate']:.2f}%")
    col2.metric("Test CVR", f"{test['Conversion_Rate']:.2f}%")
    
    uplift = ((test['Conversion_Rate'] - control['Conversion_Rate']) / control['Conversion_Rate'] * 100)
    col3.metric("Uplift", f"{uplift:+.1f}%", delta=f"{test['Conversion_Rate'] - control['Conversion_Rate']:.2f}pp")
    
    # Z-TEST
    n1, n2 = control['Visitors'], test['Visitors']
    p1, p2 = control['Conversions']/n1, test['Conversions']/n2
    
    p_pool = (control['Conversions'] + test['Conversions']) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z_score = (p2 - p1) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    
    col4.metric("p-value", f"{p_value:.4f}", 
                delta="Significant ✅" if p_value < 0.05 else "Not Significant ❌")

    # GÖRSELLEŞTİRME
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Control (A)',
        x=['Conversion Rate'],
        y=[control['Conversion_Rate']],
        marker_color='#636EFA',
        text=[f"{control['Conversion_Rate']:.2f}%"],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Test (B)',
        x=['Conversion Rate'],
        y=[test['Conversion_Rate']],
        marker_color='#00CC96' if p_value < 0.05 else '#EF553B',
        text=[f"{test['Conversion_Rate']:.2f}%"],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Conversion Rate Comparison" if lang == 'en' else "Dönüşüm Oranı Karşılaştırması",
        barmode='group',
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # SONUÇ YORUMLAMA
    st.divider()
    st.subheader(content["conclusion"][lang])
    
    if p_value < 0.05:
        if lang == 'en':
            st.success(f"""
            ✅ **Statistically Significant Result**
            
            - The Test variant (B) performs **{uplift:+.1f}%** {'better' if uplift > 0 else 'worse'} than Control (A)
            - With 95% confidence, this difference is **not due to chance**
            - **Recommendation:** {'Deploy Test variant' if uplift > 0 else 'Keep Control variant'}
            - **Expected Annual Impact:** If you have 1M visitors/year, this translates to **{int(1000000 * abs(test['Conversion_Rate'] - control['Conversion_Rate']) / 100):,}** more conversions
            """)
        else:
            st.success(f"""
            ✅ **İstatistiksel Olarak Anlamlı Sonuç**
            
            - Test varyantı (B), Kontrol'den (A) **%{uplift:+.1f}** {'daha iyi' if uplift > 0 else 'daha kötü'} performans gösteriyor
            - %95 güvenle, bu fark **tesadüfi değil**
            - **Öneri:** {'Test varyantını devreye al' if uplift > 0 else 'Kontrol varyantını koru'}
            - **Beklenen Yıllık Etki:** Yılda 1M ziyaretçiniz varsa, bu **{int(1000000 * abs(test['Conversion_Rate'] - control['Conversion_Rate']) / 100):,}** ek dönüşüm demek
            """)
    else:
        if lang == 'en':
            st.warning(f"""
            ⚠️ **No Statistical Significance**
            
            - p-value ({p_value:.4f}) > 0.05 threshold
            - The observed {uplift:+.1f}% difference could be due to random chance
            - **Recommendation:** Either continue the test longer or stick with Control
            - **Required Sample Size:** Use power analysis to determine minimum sample needed
            """)
        else:
            st.warning(f"""
            ⚠️ **İstatistiksel Anlamlılık Yok**
            
            - p-değeri ({p_value:.4f}) > 0.05 eşiği
            - Gözlemlenen %{uplift:+.1f} fark tesadüften kaynaklanıyor olabilir
            - **Öneri:** Ya testi daha uzun süre çalıştır ya da Kontrol'de kal
            - **Gerekli Örnek Boyutu:** Minimum gerekli örnek için güç analizi yap
            """)

    # GÜÇ ANALİZİ
    st.divider()
    st.markdown("### " + ("📐 Power Analysis" if lang == 'en' else "📐 Güç Analizi"))
    
    effect_size = abs(p2 - p1)
    alpha = 0.05
    power = 0.8
    
    # Basitleştirilmiş örnek boyutu hesabı
    required_n = int((2 * (1.96 + 0.84)**2 * p_pool * (1 - p_pool)) / (effect_size**2)) if effect_size > 0 else 0
    
    if lang == 'en':
        st.info(f"""
        **Minimum Sample Size per Group:** ~{required_n:,} visitors
        
        - Current sample: Control={n1:,}, Test={n2:,}
        - To detect a {effect_size*100:.2f}pp difference with 80% power and 95% confidence
        """)
    else:
        st.info(f"""
        **Grup Başına Minimum Örnek Boyutu:** ~{required_n:,} ziyaretçi
        
        - Mevcut örnek: Kontrol={n1:,}, Test={n2:,}
        - {effect_size*100:.2f}pp farkı %80 güç ve %95 güvenle tespit etmek için
        """)
