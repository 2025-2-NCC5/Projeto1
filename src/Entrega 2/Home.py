# main.py
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Configuração da Página ---
st.set_page_config(
    page_title="Cannoli 360 - Inteligência para Restaurantes",
    page_icon="🍰",  # Ícone de Cannoli
    layout="wide",
    initial_sidebar_state="expanded"
)

st.logo(
    'assets/logo_projeto.png',
    size="large",
)

# --- CSS Customizado (Foco: Laranja e Branco) ---
st.markdown("""
<style>
    /* ... (CSS existente da main.py) ... */
    
    /* Paleta de Cores Laranja */
    :root {
        --primary-color: #F97316; /* Laranja 500 */
        --secondary-color: #EA580C; /* Laranja 600 */
        --accent-color: #FB923C; /* Laranja 400 */
        --text-color: #0F172A; /* Slate 900 */
        --text-color-light: #475569; /* Slate 600 */
        --background-light: #FFF7ED; /* Laranja 50 */
        --white: #FFFFFF;
    }

    /* --- Fundo de Partículas (ADICIONADO) --- */
    #particles-js {
        position: fixed;
        width: 100%;
        height: 100%;
        z-index: -1;
        top: 0;
        left: 0;
        background-color: var(--background-light); /* Fundo laranja claro */
    }
    
    /* Header Principal */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(234, 88, 12, 0.2);
    }
    
    .main-header h1 {
        color: var(--white);
        font-weight: 700;
        font-size: 3.2rem;
    }
    
    .main-header p {
        color: var(--white);
        font-size: 1.3rem;
        opacity: 0.9;
    }
    
    /* Cartões de Funcionalidade */
    .feature-card {
        background: var(--white);
        padding: 2.5rem 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-top: 5px solid var(--primary-color);
        height: 100%;
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }
    
    .feature-card h3 {
        color: var(--secondary-color);
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .feature-card .value-prop {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 1rem;
    }

    .feature-card p {
        color: var(--text-color-light);
        font-size: 1rem;
        line-height: 1.6;
    }

    .feature-card ul {
        list-style-type: '✅';
        padding-left: 1.2rem;
        margin-top: 1rem;
    }
    
    .feature-card li {
        color: var(--text-color-light);
        margin-bottom: 0.5rem;
        padding-left: 0.5rem;
    }

    /* Bloco de Call-to-Action (CTA) Final */
    .cta-box {
        text-align: center;
        padding: 3rem; 
        background: var(--white); /* Alterado para branco para destacar do fundo */
        border-radius: 20px; 
        border: 2px solid var(--accent-color);
        margin-top: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .cta-box h2 {
        color: var(--secondary-color);
        font-weight: 700;
    }

    .cta-box p {
        color: var(--text-color-light);
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* Botão do Streamlit */
    div[data-testid="stButton"] > button {
        background-color: var(--primary-color);
        color: var(--white);
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    div[data-testid="stButton"] > button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 4px 10px rgba(234, 88, 12, 0.3);
    }

    /* --- CSS da Nova Sidebar (ADICIONADO) --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--secondary-color) 0%, var(--primary-color) 100%);
        color: var(--white);
    }
    [data-testid="stSidebar"] h2 {
        color: var(--white);
        font-weight: 700;
        padding-top: 1.5rem;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] li, [data-testid="stSidebar"] a {
        color: var(--white);
        opacity: 0.9;
    }
    [data-testid="stSidebar"] a:hover {
        opacity: 1;
        color: var(--background-light);
    }
    [data-testid="stSidebar"] .stMarkdown {
        padding-top: 0;
    }
    .slogan {
        font-style: italic;
        font-size: 1.1rem;
        text-align: center;
        border: 1px solid var(--accent-color);
        border-radius: 10px;
        padding: 1rem;
        margin: 1.5rem 0;
        background-color: rgba(255, 255, 255, 0.05);
    }
    /* --- Fim do CSS da Sidebar --- */

    /* --- CSS do Footer (ADICIONADO) --- */
    .footer {
        text-align: center;
        padding: 10px;
        margin-top: 50px;
        color: var(--text-color-light);
    }
    .footer a {
        color: var(--primary-color);
    }
    /* --- Fim do CSS do Footer --- */

</style>
""", unsafe_allow_html=True)


# --- NOVA SIDEBAR (ADICIONADO) ---
with st.sidebar:
    st.markdown("## 🍰 Cannoli 360")
    
    st.markdown("""
    <div class="slogan">
    "Transforme dados em ações
    e conquiste clientes enquanto
    otimiza sua operação."
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📞 Contato Rápido")
    st.markdown("""
    - 📧 **E-mail:** [contato@cannoli360.com](mailto:contato@cannoli360.com)
    - 📱 **WhatsApp:** [(11) 99999-9999](https://wa.me/5511999999999)
    """)
    
    st.markdown("---")
 
# --- Fundo de Partículas (ADICIONADO) ---
# Cores das partículas alteradas para laranja
particles_js_config = """
<div id="particles-js"></div>
<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
<script>
particlesJS("particles-js", {
    "particles": {
        "number": {
            "value": 180,
            "density": {
                "enable": true,
                "value_area": 500
            }
        },
        "color": {
            "value": "#FF6200" /* Laranja */
        },
        "shape": {
            "type": "circle"
        },
        "opacity": {
            "value": 0.7, /* Mais sutil */
            "random": false
        },
        "size": {
            "value": 3,
            "random": true
        },
        "line_linked": {
            "enable": true,
            "distance": 150,
            "color": "#FF6200", /* Laranja claro */
            "opacity": 0.7,
            "width": 1
        },
        "move": {
            "enable": true,
            "speed": 1,
            "direction": "none",
            "out_mode": "out"
        }
    },
    "interactivity": {
        "events": {
            "onhover": {
                "enable": true,
                "mode": "repulse"
            },
            "onclick": {
                "enable": true
            }
        },
        "modes": {
            "repulse": {
                "distance": 100
            }
        }
    },
    "retina_detect": true
});
</script>
"""
# Altura aumentada para preencher mais a página
components.html(particles_js_config, height=200, scrolling=False)


# ===========================================================
# 🔹 SEÇÃO 1: HEADER
# ===========================================================
st.markdown("""
<div class="main-header">
    <h1>🍰 Cannoli 360: A Inteligência que Faltava no seu Restaurante</h1>
    <p>Pare de adivinhar. Transforme seus dados de pedidos em lucro real, retenção de clientes e gestão eficiente.</p>
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 🔹 SEÇÃO 2: PITCH DAS FUNCIONALIDADES
# ===========================================================
st.markdown("<h2 style='text-align: center; color: #C2410C; font-weight: 700; margin-bottom: 2rem;'>Sua Plataforma Completa de Inteligência</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    # Pitch para rfm.py
    st.markdown("""
    <div class="feature-card">
        <h3>🎯 Segmentação e Otimização de Descontos (RFM)</h3>
        <p class="value-prop">Pare de desperdiçar descontos com quem já ia comprar.</p>
        <p>
            Nossa ferramenta analisa o RFM (Recência, Frequência, Valor) de cada cliente e 
            <strong>prescreve a faixa de desconto ideal</strong>.
        </p>
        <ul>
            <li>Identifique seus "Campeões" (e pare de dar descontos a eles).</li>
            <li>Salve clientes "Em Risco" com uma oferta cirúrgica.</li>
            <li>Incentive "Novos Clientes" a fazerem a segunda compra.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Pitch para 03_BSC.py
    st.markdown("""
    <div class="feature-card">
        <h3>🚀 Dashboard de Performance (BSC)</h3>
        <p class="value-prop">Tenha a gestão à vista de todas as suas lojas.</p>
        <p>
            O Balanced Scorecard monitora seus 4 pilares de sucesso: 
            <strong>Financeiro, Clientes, Processos e Aprendizado</strong>.
        </p>
        <ul>
            <li>Veja o ranking de performance entre suas lojas.</li>
            <li>Monitore KPIs cruciais como Tempo de Preparo e Custo por Pedido.</li>
            <li>Tome decisões baseadas em dados, não em achismos.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Pitch para 02_ROI_Casos_Sucesso.py
    st.markdown("""
    <div class="feature-card">
        <h3>🧮 Calculadora de ROI e Casos de Sucesso</h3>
        <p class="value-prop">Veja o futuro do seu lucro antes de investir.</p>
        <p>
            Nossa plataforma se paga. Use nossa calculadora para 
            <strong>simular o impacto financeiro</strong> da Cannoli 360 no seu faturamento.
        </p>
        <ul>
            <li>Projete seu aumento de receita, LTV e redução de churn.</li>
            <li>Entenda seu potencial de ganho anual.</li>
            <li>Veja casos de sucesso reais de restaurantes como o seu.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ===========================================================
# 🔹 SEÇÃO 3: CALL TO ACTION (CTA) FINAL
# ===========================================================
# Usando o container para centralizar
_, col_cta, _ = st.columns([1, 2, 1])

with col_cta:
    st.markdown("""
    <div class="cta-box">
        <h2>Pronto para Aumentar Seu Lucro Líquido?</h2>
        <p>
            Agende uma demonstração exclusiva e veja o Cannoli 360 em ação com os dados do <strong>seu</strong> restaurante.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 SOLICITAR DEMONSTRAÇÃO EXCLUSIVA", use_container_width=True):
        st.balloons()
        st.success("✅ Solicitação enviada! Nossa equipe entrará em contato em até 24h.")
        st.info("📧 Você receberá um e-mail com os próximos passos e um link para agendar sua demo personalizada.")

# --- NOVO: Footer Creative Commons (ADICIONADO) ---
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>
        <strong>Cannoli 360</strong> - Transformando Dados em Ações.<br>
        Um projeto de Data Science da FECAP.
    </p>
    <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
        <img alt="Licença Creative Commons" style="border-width:0" 
             src="https://i.creativecommons.org/l/by/4.0/88x31.png" />
    </a>
    <br />
    Este trabalho está licenciado sob uma 
    <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
        Licença Creative Commons Atribuição 4.0 Internacional
    </a>.
</div>
""", unsafe_allow_html=True)