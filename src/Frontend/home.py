import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import os

# Configuração da página
st.set_page_config(
    page_title="Cannoli CRM",
    layout="centered",
    page_icon="src/assets/logo_cannoli.jfif",
    menu_items={}
)

# Sidebar
with st.sidebar:
    st.title("🔗 Saiba mais sobre a Cannoli")
    st.markdown("""
        <p style="font-size:15px; margin-top:15px;">
            <a href="https://www.cannoli.food/" target="_blank" style="color:#FF5F15; text-decoration:none;">
                👉 Visite nosso site oficial
            </a>
        </p>

        <p style="font-size:16px; margin-top:20px;">Conheça nossas soluções para:</p>
        <ul style="font-size:16px; color:#FFFFFF;">
            <li>📈 CRM inteligente para restaurantes</li>
            <li>🤖 Automação de WhatsApp</li>
            <li>🧠 Segmentação baseada em comportamento</li>
            <li>📊 Painel de performance em tempo real</li>
            <li>💬 Campanhas personalizadas</li>
        </ul>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        """
        <span style='color: #FFFFFF; font-weight: bold;'>Cannoli CRM</span><br>
        <span style='color: #FF5F15; font-style: italic;'>Transformando dados em vendas automáticas.</span>
        """,
        unsafe_allow_html=True
    )

# Partículas de fundo
particles_background = """
<style>
    #particles-js {
        position: fixed;
        width: 100%;
        height: 100%;
        z-index: -1;
        top: 0;
        left: 0;
    }
</style>
<div id="particles-js"></div>
<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
<script>
particlesJS("particles-js", {
    "particles": {
        "number": {
            "value": 80,
            "density": {
                "enable": true,
                "value_area": 800
            }
        },
        "color": {
            "value": "#F59E0B"
        },
        "shape": {
            "type": "circle"
        },
        "opacity": {
            "value": 0.4
        },
        "size": {
            "value": 3,
            "random": true
        },
        "line_linked": {
            "enable": true,
            "distance": 150,
            "color": "#F59E0B",
            "opacity": 0.6,
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
                "enable": true,
                "mode": "push"
            }
        },
        "modes": {
            "repulse": {
                "distance": 100
            },
            "push": {
                "particles_nb": 4
            }
        }
    },
    "retina_detect": true
});
</script>
"""

components.html(particles_background, height=150, width=2000, scrolling=False)

# Conteúdo principal
st.markdown("""
# 👋 Bem-vindo à Plataforma Cannoli

A **Cannoli** é o CRM inteligente feito para o seu restaurante vender mais todos os dias.

Combinamos **segmentação automática**, **automação no WhatsApp** e **painéis de dados em tempo real** para transformar seus clientes em fãs fiéis da sua marca.

---

### 🍝 O que você vai encontrar aqui:

✅ **Painel com dados dos seus clientes ativos, inativos e em risco**  
✅ **Campanhas automáticas por WhatsApp com 1 clique**  
✅ **Funis de retorno e reativação em tempo real**  
✅ **Integração com PDVs e cardápios digitais**  
✅ **Visual moderno e intuitivo**

---

### 🚀 Comece agora a transformar dados em vendas!

""", unsafe_allow_html=True)

# Navegação entre páginas
st.page_link("/pages/01_dashboard.py", label="📊 Dashboard de Clientes e Vendas")
st.page_link("/pages/02_modelo.py", label="🤖 Criar Campanha Automática")
st.page_link("/pages/03_suporte.py", label="📞 Fale com o Suporte")

# Rodapé
st.markdown("""
<style>
    .footer {
        text-align: center;
        padding: 10px;
        margin-top: 50px;
        font-size: 14px;
        color: #888;
    }
</style>
<div class="footer">
    <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
        <img alt="Licença Creative Commons" style="border-width:0" 
             src="https://i.creativecommons.org/l/by/4.0/88x31.png" />
    </a>
    <br />
    Este sistema está licenciado sob uma 
    <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
        Licença Creative Commons Atribuição 4.0 Internacional
    </a>.
</div>
""", unsafe_allow_html=True)
