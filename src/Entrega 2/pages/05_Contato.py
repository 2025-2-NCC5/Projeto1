import streamlit as st
import streamlit.components.v1 as components
from PIL import Image


st.set_page_config(
    page_title="Contatos - Cannoli 360",
    layout="wide", 
    page_icon="📞",
    menu_items={}
)

st.logo(
    'assets/logo_projeto.png',
    size="large",
)

# --- CSS Customizado (Laranja e Branco) ---
# (CSS da main.py + CSS do arquivo de referência "Help MEI" adaptado)
st.markdown("""
<style>
    /* Paleta de Cores Laranja (de main.py) */
    :root {
        --primary-color: #F97316; /* Laranja 500 */
        --secondary-color: #EA580C; /* Laranja 600 */
        --accent-color: #FB923C; /* Laranja 400 */
        --text-color: #0F172A; /* Slate 900 */
        --text-color-light: #475569; /* Slate 600 */
        --background-light: #FFF7ED; /* Laranja 50 */
        --white: #FFFFFF;
    }
    
    /* --- CSS da Nova Sidebar --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--secondary-color) 0%, var(--primary-color) 100%);
        color: var(--white);
    }
    [data-testid="stSidebar"] h2 {
        color: var(--white);
        font-weight: 700;
        padding-top: 1.5rem; /* Ajuste para o título da sidebar */
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

    /* Fundo de Partículas (do arquivo de referência) */
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

    /* Estilo para o Formulário (adaptado) */
    .contact-form {
        background: var(--white);
        padding: 2.5rem 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-top: 5px solid var(--primary-color);
        height: 100%;
    }
    
    /* Estilo para a Caixa de Info (Canais) */
    .info-box {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid var(--accent-color);
        height: 100%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .info-box h4 { color: var(--secondary-color); }
    .info-box p { color: var(--text-color-light); margin-bottom: 0.5rem; }

    /* Seção de Time (do arquivo de referência, adaptada) */
    .team-header {
        color: var(--secondary-color); /* Laranja */
        font-size: 28px !important;
        font-weight: 700;
        text-align: center;
        margin: 20px 0 10px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid var(--accent-color); /* Laranja */
    }
    .team-name {
        font-size: 24px !important;
        font-weight: 600;
        text-align: center;
        margin: 15px 0;
        color: var(--text-color); /* Cor de texto padrão */
    }
    .team-description {
        text-align: center;
        font-size: 1.1rem;
        color: var(--text-color-light);
        margin-bottom: 25px;
    }
    .team-card {
        background: var(--white);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-top: 5px solid var(--primary-color);
        margin: 1rem 0;
        height: 100%;
    }
    .team-card h3 {
        color: var(--secondary-color);
        border-bottom: 2px solid var(--background-light);
        padding-bottom: 0.5rem;
    }
    .team-card li {
        font-size: 1rem;
        color: var(--text-color-light);
        list-style-type: none; /* Remove bullets da lista de time */
        padding-left: 0;
    }
     .team-card a {
        text-decoration: none;
        font-weight: 500;
        color: var(--text-color);
    }
    .team-card a:hover {
        color: var(--primary-color);
    }


    /* Footer (do arquivo de referência) */
    .footer {
        text-align: center;
        padding: 10px;
        margin-top: 50px;
        color: var(--text-color-light);
    }
    .footer a {
        color: var(--primary-color);
    }

    /* Botão de Envio do Formulário */
    div[data-testid="stButton"] > button {
        background-color: var(--primary-color);
        color: var(--white);
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 4px 10px rgba(234, 88, 12, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- NOVA SIDEBAR ---
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
  
# --- Fundo de Partículas (do arquivo de referência) ---
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


# --- Título (ATUALIZADO) ---
st.markdown("""
<div class="main-header">
    <h1>📞 Entre em Contato</h1>
    <p style="font-size: 1.3rem;">Estamos prontos para ajudar a transformar seu negócio.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # --- Formulário (Mantido da v1, mas com classe CSS) ---
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    st.markdown("### 📝 Formulário de Contato")
    st.markdown("Envie sua mensagem e nossa equipe comercial responderá em até 24 horas.")
    
    with st.form(key="contact_form", clear_on_submit=True):
        col_nome, col_email = st.columns(2)
        with col_nome:
            nome = st.text_input("Seu Nome *", placeholder="João Silva")
        with col_email:
            email = st.text_input("Seu E-mail *", placeholder="joao.silva@restaurante.com")
        
        telefone = st.text_input("Telefone/WhatsApp", placeholder="(11) 99999-9999")
        nome_restaurante = st.text_input("Nome do Restaurante", placeholder="Pizzaria do João")
        
        assunto = st.selectbox(
            "Principal Interesse *",
            ["Selecione uma opção", "Demonstração da Plataforma", "Contratação", "Suporte Técnico", "Parcerias", "Outro"]
        )
        
        mensagem = st.text_area(
            "Sua Mensagem *",
            placeholder="Gostaria de agendar uma demonstração para entender como o Cannoli 360 pode se aplicar à minha pizzaria...",
            height=150
        )
        
        # Simulação de envio
        submitted = st.form_submit_button("🚀 Enviar Mensagem")
        if submitted:
            if not nome or not email or not assunto or not mensagem or assunto == "Selecione uma opção":
                st.error("Por favor, preencha todos os campos obrigatórios (*).")
            else:
                st.success(f"Obrigado, {nome}! Sua mensagem sobre '{assunto}' foi enviada. Entraremos em contato em breve.")
                st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)


with col2:
    # --- Canais de Contato (CSS ATUALIZADO) ---
    st.markdown("### 📍 Nossos Canais")
    st.markdown("""
    <div class="info-box">
        <h4>📧 E-mail</h4>
        <p>contato@cannoli360.com</p>
        <h4>📱 WhatsApp Comercial</h4>
        <p>(11) 99999-9999</p>
        <h4>🏢 Endereço</h4>
        <p>Av. Paulista, 1000<br>
        São Paulo, SP - 01310-100</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Seção de Time (ADAPTADA do arquivo de referência) ---
st.markdown('<div class="team-header">NOSSO TIME</div>', unsafe_allow_html=True)
st.markdown('<div class="team-name">Cannoli 360</div>', unsafe_allow_html=True)
st.markdown('<div class="team-description">Grupo de desenvolvimento dedicado a criar soluções de dados para restaurantes.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="team-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Fundadores & Data Science")
    st.markdown("""
    <ul>
        <li><a href="https://www.linkedin.com/in/flaviojose-santos/" target="_blank">Flavio Santos</a></li>
        <li><a href="https://www.linkedin.com/in/mariaeflopes/" target="_blank">Eduarda Lopes</a></li>
        <li><a href="https://www.linkedin.com/in/jenifer-barreto-55022523b/" target="_blank">Jenifer Barreto</a></li>
        <li><a href="https://www.linkedin.com/in/felipecarpal/" target="_blank">Felipe Carvalho Paleari</a></li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="team-card">', unsafe_allow_html=True)
    st.markdown("### 🎓 Orientadores (FECAP)")
    st.markdown("""
    <ul>
        <li>Renata Muniz</li>
        <li>Rodrigo Rosa</li>
        <li>Victor Bruno Rosetti</li>
        <li>Rafael Diogo Rossetti</li>
        <li>Marcos Minouru</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --- FAQs (Mantido da v1) ---
st.markdown("---")
st.markdown("### ❓ FAQs")
st.markdown("Respostas rápidas para suas dúvidas mais comuns.")

with st.expander("⚙️ O Cannoli 360 integra com meu sistema de PDV?"):
# ... (restante da função inalterada) ...
    st.markdown("""
    **Sim!** Nossa plataforma foi construída para ser flexível.
    
    - **Integração Nativa:** Temos integração direta com os principais PDVs do mercado (como [Nome PDV 1], [Nome PDV 2], etc.).
    - **API Aberta:** Se você usa um sistema próprio, nossa API permite uma conexão rápida.
    - **Planilhas:** Também podemos importar dados via .csv ou planilhas Google Sheets.
    """)

with st.expander("🚀 Em quanto tempo vejo os primeiros resultados?"):
# ... (restante da função inalterada) ...
    st.markdown("""
    **Em 7 dias.** Nosso processo de *onboarding* é dividido:
    
    - **D+1:** Conexão e importação do seu histórico de dados.
    - **D+2:** Treinamento do modelo de RFM e geração dos primeiros segmentos.
    - **D+3:** Sessão de "Diagnóstico" com nosso especialista para analisar seus segmentos.
    - **D+7:** Você já pode rodar sua primeira campanha otimizada para os clientes "Em Risco (Leais)".
    """)

with st.expander("💸 Como funciona a cobrança?"):
# ... (restante da função inal_terada) ...
    st.markdown("""
    Trabalhamos com um modelo de **assinatura mensal (SaaS)**.
    
    - **Plano Fixo:** Um valor fixo por CNPJ (loja), sem surpresas.
    - **Sem Taxa de Setup:** Não cobramos pela implantação.
    - **Sem Fidelidade:** Você pode cancelar a qualquer momento.
    
    Nosso sucesso depende do seu sucesso. Acreditamos que o ROI gerado pela plataforma se paga em poucas semanas.
    """)

st.markdown("---")

# --- Footer (ADAPTADO do arquivo de referência, substituindo a Garantia) ---
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