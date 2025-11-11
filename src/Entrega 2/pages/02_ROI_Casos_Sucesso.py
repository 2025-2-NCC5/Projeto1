import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pathlib import Path 

st.set_page_config(
    page_title="ROI & Casos de Sucesso - Cannoli CRM",
    page_icon="📊",
    layout="wide"
)

st.logo(
    'assets/logo_projeto.png',
    size="large",
)

# --- CSS (ATUALIZADO para paleta Laranja e Branco de main.py) ---
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

    /* Mapeamento: .success-header (antigo verde) -> .main-header (estilo laranja) */
    .success-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); 
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    
    /* Ajuste para o texto dentro do header */
    .success-header h1 {
        color: var(--white);
        font-weight: 700;
        font-size: 3.2rem;
    }
    
    .success-header p {
        color: var(--white);
        font-size: 1.3rem;
        opacity: 0.9;
    }

    /* Mapeamento: .case-card (usado para Casos de Sucesso E Depoimentos) */
    .case-card {
        background: var(--white);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-top: 5px solid var(--primary-color); /* Laranja Padrão */
        margin: 1rem 0;
    }
    
    /* Mapeamento: .roi-box (amarelo) -> .cta-box (estilo laranja claro) */
    .roi-box {
        background: var(--background-light); 
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid var(--accent-color); 
        text-align: center;
        margin: 2rem 0;
    }

    /* Funcionalidade mantida: .roi-box-negative (vermelho) */
    .roi-box-negative {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #DC2626;
        text-align: center;
        margin: 2rem 0;
    }
    
    /* Estilos para o CTA Final (importados de main.py) */
    .cta-box {
        text-align: center;
        padding: 3rem; 
        background: var(--background-light); 
        border-radius: 20px; 
        border: 2px solid var(--accent-color);
        margin-top: 2rem;
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

    /* Estilos para o Botão do CTA (importados de main.py) */
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

# --- Início da Aplicação ---

# --- HEADER (ATUALIZADO PARA NOVO DESIGN) ---
st.markdown("""
<div class="success-header">
    <h1>📊 ROI Comprovado & Casos de Sucesso</h1>
    <p style="font-size: 1.3rem;">Simule seu potencial de ganho e veja resultados reais de nossos parceiros.</p>
</div>
""", unsafe_allow_html=True)

# --- Calculadora de ROI (Versão Genérica/Padrão de Mercado) ---
st.markdown("## 🧮 Calculadora de ROI Personalizada")
st.markdown("Insira os dados estimados do seu restaurante para simular o impacto do Cannoli 360.")

col1, col2 = st.columns([1, 1])

# Custo Fixo da Plataforma
CUSTO_CANNOLI_MENSAL = 2997

with col1:
    st.markdown("### 📝 Dados do Seu Restaurante")
    
    receita_mensal = st.number_input(
        "Receita Mensal Atual (R$)",
        min_value=10000,
        max_value=1000000,
        value=150000,
        step=10000
    )
    
    clientes_ativos = st.number_input(
        "Clientes Ativos/Mês",
        min_value=100,
        max_value=10000,
        value=800,
        step=50
    )
    
    # Cálculo do ticket médio baseado nos inputs
    ticket_medio = receita_mensal / clientes_ativos if clientes_ativos > 0 else 0
    
    taxa_churn = st.slider(
        "Taxa de Churn Mensal Estimada (%)",
        min_value=5.0,
        max_value=40.0,
        value=20.0,
        step=0.5
    )
    
    investimento_marketing = st.number_input(
        "Investimento Mensal em Marketing (R$)",
        min_value=1000,
        max_value=50000,
        value=8000,
        step=500
    )
    st.info(f"Custo Cannoli 360 (Software): R$ {CUSTO_CANNOLI_MENSAL}/mês")
    investimento_total_crm = investimento_marketing + CUSTO_CANNOLI_MENSAL


with col2:
    st.markdown("### 📈 Projeção com Cannoli 360")
    
    # Cálculos de impacto (com base nos "padrões de mercado" fixos)
    reducao_churn_perc = 0.42  # 42% de redução
    aumento_ticket_perc = 0.18  # 18% de aumento
    aumento_frequencia_perc = 0.25  # 25% mais visitas

    reducao_churn_abs = taxa_churn * reducao_churn_perc
    nova_taxa_churn = taxa_churn - reducao_churn_abs
    
    aumento_ticket_abs = ticket_medio * aumento_ticket_perc
    novo_ticket = ticket_medio + aumento_ticket_abs
    
    novas_visitas_mes = clientes_ativos * (1 + aumento_frequencia_perc)
    
    nova_receita = novas_visitas_mes * novo_ticket
    incremento_receita_bruta = nova_receita - receita_mensal
    
    # ROI sobre o investimento TOTAL (Marketing + Cannoli)
    incremento_liquido_total = incremento_receita_bruta - investimento_total_crm
    roi_total = (incremento_liquido_total / investimento_total_crm) * 100 if investimento_total_crm > 0 else 0
    
    # Exibir métricas
    st.metric(
        "Nova Receita Mensal Projetada",
        f"R$ {nova_receita:,.2f}",
        f"+R$ {incremento_receita_bruta:,.2f}"
    )
    
    st.metric(
        "Novo Ticket Médio",
        f"R$ {novo_ticket:.2f}",
        f"+{aumento_ticket_perc*100:.0f}%"
    )
    
    st.metric(
        "Nova Taxa de Churn",
        f"{nova_taxa_churn:.1f}%",
        f"-{reducao_churn_abs:.1f}pp", # pp = pontos percentuais
        delta_color="inverse"
    )
    
    st.metric(
        "ROI Total (Marketing + Cannoli)",
        f"{roi_total:.0f}%",
        f"Lucro de R$ {incremento_liquido_total:,.2f}"
    )

# --- Bloco de ROI Dinâmico (com Assessoria) ---

# Cálculo focado apenas no Cannoli
incremento_liquido_cannoli_vs_receita = incremento_receita_bruta - CUSTO_CANNOLI_MENSAL
retorno_x_cannoli = incremento_receita_bruta / CUSTO_CANNOLI_MENSAL if CUSTO_CANNOLI_MENSAL > 0 else 0

# A "previsão não for boa" significa que o incremento líquido (lucro) não é positivo
if incremento_liquido_total > 0:
    # --- CENÁRIO POSITIVO (ATUALIZADO COM .roi-box) ---
    st.markdown(f"""
    <div class="roi-box">
        <h2 style="color: #92400E; margin-bottom: 1rem;">💰 Seu Potencial de Crescimento Anual (com Cannoli)</h2>
        <h1 style="color: #B45309; font-size: 3.5rem; margin: 1rem 0;">+ R$ {incremento_receita_bruta * 12:,.2f}</h1>
        <p style="color: #78350F; font-size: 1.2rem;">
            Investimento no Cannoli 360 (Software): <strong>R$ {CUSTO_CANNOLI_MENSAL:,.2f}/mês</strong><br>
            <strong>Retorno de {retorno_x_cannoli:.1f}x sobre o investimento na plataforma</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # --- CENÁRIO NEGATIVO (Assessoria) ---
    st.markdown(f"""
    <div class="roi-box-negative">
        <h2 style="color: #991B1B; margin-bottom: 1rem;">📈 Oportunidade de Otimização Identificada</h2>
        <h1 style="color: #B91C1C; font-size: 2.5rem; margin: 1rem 0;">Plano de Assessoria Cannoli 360 Ativado!</h1>
        <p style="color: #7F1D1D; font-size: 1.2rem;">
            Sua projeção (ROI de <strong>{roi_total:.0f}%</strong>) indica que seus custos operacionais
            ou de marketing podem estar altos demais para a receita incremental.
        </p>
        <p style="color: #7F1D1D; font-size: 1.1rem; margin-top: 1rem;">
            Com a <strong>Assessoria Estratégica Cannoli 360</strong>, nossos especialistas
            farão uma imersão no seu negócio para otimizar seus custos e processos
            antes de escalarmos seu crescimento com a plataforma.
        </p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")

# --- Casos de Sucesso (Sem alterações de funcionalidade, apenas estilo via CSS) ---
st.markdown("## 🏆 Casos de Sucesso Reais")

# Caso 1: Pizzaria
with st.expander("🍕 **Pizzaria Bella Napoli** - São Paulo, SP", expanded=True):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Desafio
        - Alta taxa de churn (32% ao mês)
        - Baixa frequência de pedidos (1.8x/mês)
        - Descontos genéricos de 20% para todos
        - ROI negativo em campanhas de e-mail
        
        ### Solução Cannoli CRM
        - Segmentação preditiva de 850 clientes
        - Otimização de descontos por perfil (5% a 25%)
        - Automação de reativação de inativos
        - Programa VIP para top 10%
        
        ### Resultados em 6 Meses
        """)
        
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            st.metric("Churn", "18.5%", "-13.5%", delta_color="inverse")
        with col_b:
            st.metric("Frequência", "2.7x/mês", "+50%")
        with col_c:
            st.metric("Ticket Médio", "R$ 87", "+22%")
        with col_d:
            st.metric("Receita", "R$ 198k", "+47%")
    
    with col2:
        # Gráfico de evolução
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
        receita = [135, 142, 158, 172, 185, 198]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=meses,
            y=receita,
            mode='lines+markers',
            line=dict(color='#10B981', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ))
        
        fig.update_layout(
            height=300,
            title="Evolução de Receita (R$ mil)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("💬 *'O Cannoli CRM pagou por si mesmo no primeiro mês. Hoje não consigo imaginar operar sem ele.'* - Marco Rossi, Proprietário")

# Caso 2: Hamburgueria
with st.expander("🍔 **Burger House** - Rio de Janeiro, RJ"):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Desafio
        - Concorrência agressiva no delivery
        - Margem apertada (18%)
        - Dificuldade em fidelizar clientes
        - Custo de aquisição alto (R$ 45/cliente)
        
        ### Solução Cannoli CRM
        - Análise de elasticidade de preço
        - Programa de cashback automatizado
        - Upsell inteligente de acompanhamentos
        - Reativação de clientes inativos
        
        ### Resultados em 4 Meses
        """)
        
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            st.metric("Margem", "26%", "+8%")
        with col_b:
            st.metric("CAC", "R$ 28", "-R$ 17", delta_color="inverse")
        with col_c:
            st.metric("LTV", "R$ 890", "+65%")
        with col_d:
            st.metric("ROI Mkt", "520%", "+320%")
    
    with col2:
        # Gráfico de margem
        categorias = ['Antes', 'Depois']
        margem = [18, 26]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categorias,
            y=margem,
            marker_color=['#EF4444', '#10B981'],
            text=margem,
            texttemplate='%{text}%',
            textposition='outside'
        ))
        
        fig.update_layout(
            height=300,
            title="Margem de Lucro",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis_title="%"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("💬 *'Conseguimos competir com as grandes redes mantendo margem saudável. Game changer!'* - Ana Paula, Sócia")

# Caso 3: Restaurante Japonês
with st.expander("🍱 **Sushi Premium** - Curitiba, PR"):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Desafio
        - Ticket alto (R$ 180) limitava frequência
        - Clientes VIP não identificados
        - Comunicação genérica
        - Baixa taxa de indicação
        
        ### Solução Cannoli CRM
        - Identificação automática de VIPs
        - Programa de experiências exclusivas
        - Comunicação hiperpersonalizada
        - Sistema de indicação gamificado
        
        ### Resultados em 5 Meses
        """)
        
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            st.metric("VIPs", "78", "+78")
        with col_b:
            st.metric("Freq. VIP", "6.2x/mês", "+85%")
        with col_c:
            st.metric("Indicações", "34/mês", "+340%")
        with col_d:
            st.metric("Receita VIP", "R$ 87k", "+156%")
    
    with col2:
        # Gráfico de composição de receita
        labels = ['VIPs', 'Regulares', 'Ocasionais']
        values = [45, 35, 20]
        colors = ['#10B981', '#3B82F6', '#F59E0B']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors)
        )])
        
        fig.update_layout(
            height=300,
            title="Composição de Receita",
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("💬 *'Nossos VIPs se sentem realmente especiais. O programa se paga só com as indicações.'* - Takeshi Yamamoto, Chef/Proprietário")

st.markdown("---")

# --- Depoimentos (RE-ADICIONADO) ---
st.markdown("## 💬 O Que Nossos Clientes Dizem")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="case-card">
        <h4>⭐⭐⭐⭐⭐</h4>
        <p style="font-style: italic; color: #475569;">
            "Em 3 meses, aumentamos a receita em 42% sem contratar mais gente. 
            O sistema praticamente se gerencia sozinho."
        </p>
        <p style="color: #64748B; margin-top: 1rem;">
            <strong>Carlos Mendes</strong><br>
            Proprietário - Churrascaria Gaúcha
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="case-card">
        <h4>⭐⭐⭐⭐⭐</h4>
        <p style="font-style: italic; color: #475569;">
            "Finalmente entendo meus clientes. O ML identifica padrões que eu nunca veria. 
            ROI de 520% em campanhas!"
        </p>
        <p style="color: #64748B; margin-top: 1rem;">
            <strong>Juliana Santos</strong><br>
            Gerente - Rede de Cafeterias (5 unidades)
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="case-card">
        <h4>⭐⭐⭐⭐⭐</h4>
        <p style="font-style: italic; color: #475569;">
            "A otimização de descontos salvou nossa margem. Antes dávamos 20% para todos, 
            agora damos o mínimo necessário."
        </p>
        <p style="color: #64748B; margin-top: 1rem;">
            <strong>Roberto Lima</strong><br>
            Sócio - Restaurante Italiano
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- CTA Final (RE-ADICIONADO e RE-ESTILIZADO) ---
_, col_cta, _ = st.columns([1, 2, 1]) # Centraliza o CTA

with col_cta:
    st.markdown("""
    <div class="cta-box">
        <h2 style="color: var(--secondary-color);">Pronto para Resultados Como Esses?</h2>
        <p style="font-size: 1.2rem; color: var(--text-color-light); margin-bottom: 2rem;">
            Agende uma demonstração e veja o potencial do seu restaurante
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 QUERO MINHA DEMONSTRAÇÃO", use_container_width=True):
        st.balloons()
        st.success("✅ Ótima decisão! Nossa equipe entrará em contato em até 24h.")
        st.info("📧 Você receberá um e-mail com um link para agendar sua demo personalizada.")

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