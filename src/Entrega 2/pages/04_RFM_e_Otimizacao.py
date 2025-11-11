# -*- coding: utf-8 -*-

"""
Dashboard de Segmentação (RFM) e Otimização de Descontos (v4.0)

Este script combina segmentação RFM (baseada em regras de negócio) com um 
motor de recomendação de descontos. 

Ele usa os dados originais para:
1. Carregar e filtrar dados por restaurante.
2. Calcular RFM (Recência, Frequência, Valor).
3. Aplicar regras de percentil para criar segmentos (Campeões, Leais, etc.).
4. Prescrever Risco de Churn e a Faixa de Desconto ideal para cada segmento.
5. Exibir as visualizações e a tabela de ação.
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import plotly.express as px
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Configura o layout da página para usar a tela inteira
st.set_page_config(layout="wide", page_title="Segmentação por Restaurante")

st.logo(
    'assets/logo_projeto.png',
    size="large",
)

# Injeta o CSS customizado para o design Laranja/Branco
st.markdown("""
<style>
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

    /* Expanders */
    div[data-testid="stExpander"] {
        background-color: var(--background-light);
        border-radius: 10px;
    }
    div[data-testid="stExpander"] > details > summary {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--secondary-color);
    }

    /* Abas (Tabs) */
    button[data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-color-light);
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--primary-color);
        border-bottom: 3px solid var(--primary-color);
    }

    /* Sidebar */
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

    /* Footer */
    .footer {
        text-align: center;
        padding: 10px;
        margin-top: 50px;
        color: var(--text-color-light);
    }
    .footer a {
        color: var(--primary-color);
    }
</style>
""", unsafe_allow_html=True)


# Constrói a sidebar com slogan, contatos e navegação
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

# --- Funções de Processamento de Dados ---

@st.cache_data
def carregar_dados():
    """
    Carrega e limpa os dados brutos de pedidos e clientes.
    Usa 'latin1' para encoding e trata separadores/decimais.
    """
    try:
        df_pedidos = pd.read_csv('backend/utils/base_unificada.csv', sep=';', decimal=',', encoding='latin1')
        df_clientes = pd.read_csv('backend/utils/dados_clientes.csv', sep=',', encoding='latin1')
        
    except FileNotFoundError as e:
        st.error(f"Erro ao carregar o arquivo: {e}. Verifique os caminhos 'backend/utils/'.")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado durante o carregamento: {e}")
        return None

    # Converte colunas essenciais
    df_pedidos['createdAt'] = pd.to_datetime(df_pedidos['createdAt'], dayfirst=True, errors='coerce')
    df_pedidos['totalAmount'] = pd.to_numeric(df_pedidos['totalAmount'], errors='coerce')
    
    # Filtra pedidos de teste e remove linhas com dados faltantes
    df_pedidos_limpo = df_pedidos.loc[df_pedidos['isTest'] == False].copy()
    df_pedidos_limpo.dropna(subset=['createdAt', 'totalAmount', 'customer', 'segmento', 'empresa'], inplace=True)

    # Junta com os dados do cliente para pegar o nome
    df_clientes_selec = df_clientes[['id', 'name']].copy()
    df_pedidos_limpo.rename(columns={'id': 'id_pedido'}, inplace=True)

    df_merged = pd.merge(
        df_pedidos_limpo,
        df_clientes_selec,
        left_on='customer',
        right_on='id',
        how='left'
    )
    
    # Limpeza final dos dados
    df_merged['name'].fillna('Cliente Desconhecido', inplace=True)
    df_merged['segmento'] = df_merged['segmento'].str.strip()
    df_merged['empresa'] = df_merged['empresa'].str.strip()
    
    return df_merged


@st.cache_data
def calcular_rfm(df_restaurante):
    """
    Calcula as métricas RFM (Recência, Frequência, Valor Monetário) para cada cliente.
    """
    if df_restaurante.empty:
        return pd.DataFrame()

    # Define a data de "hoje" como 1 dia após a última compra registrada no filtro
    snapshot_date = df_restaurante['createdAt'].max() + dt.timedelta(days=1)
    
    # Agrupa por cliente e calcula R, F, M
    df_rfm = df_restaurante.groupby(['customer', 'name']).agg(
        Recência_raw=('createdAt', 'max'),
        Frequência=('displayId', 'nunique'),
        Valor_Monetário=('totalAmount', 'sum')
    ).reset_index()

    # Calcula Recência em dias
    df_rfm['Recência'] = (snapshot_date - df_rfm['Recência_raw']).dt.days
    df_rfm.rename(columns={'Valor_Monetário': 'Valor Monetário'}, inplace=True)
    
    colunas_finais = ['customer', 'name', 'Recência', 'Frequência', 'Valor Monetário']
    df_rfm = df_rfm[colunas_finais]
    
    return df_rfm.dropna()


@st.cache_data
def segmentar_por_regras(df_rfm):
    """
    Segmenta clientes usando regras de negócio (percentis).
    Score 4 = Melhor (ex: Recência Baixa)
    Score 1 = Pior (ex: Recência Alta)
    """
    if df_rfm.empty:
        return df_rfm

    df_rfm_regras = df_rfm.copy()

    # Cria scores de 1 a 4. Usamos rank(pct=True) para ser robusto a dados duplicados.
    # Recência: quanto menor, melhor a nota
    df_rfm_regras['R_Score'] = np.ceil(df_rfm_regras['Recência'].rank(method='min', ascending=False, pct=True) * 4).astype(int)
    # Frequência: quanto maior, melhor a nota
    df_rfm_regras['F_Score'] = np.ceil(df_rfm_regras['Frequência'].rank(method='min', ascending=True, pct=True) * 4).astype(int)
    # Valor Monetário: quanto maior, melhor a nota
    df_rfm_regras['M_Score'] = np.ceil(df_rfm_regras['Valor Monetário'].rank(method='min', ascending=True, pct=True) * 4).astype(int)

    # Regras de negócio para definir cada segmento
    conditions = [
        # Campeões: Bons em Recência e Frequência
        (df_rfm_regras['R_Score'] >= 3) & (df_rfm_regras['F_Score'] >= 3),
        # Em Risco (Leais): Ruins em Recência, mas bons em Frequência
        (df_rfm_regras['R_Score'] <= 2) & (df_rfm_regras['F_Score'] >= 3),
        # Novos: Bons em Recência, mas ruins em Frequência
        (df_rfm_regras['R_Score'] >= 3) & (df_rfm_regras['F_Score'] <= 2),
        # Hibernando: Ruins em Recência e Frequência
        (df_rfm_regras['R_Score'] <= 2) & (df_rfm_regras['F_Score'] <= 2)
    ]
    choices = [
        '🏆 Campeões',
        '👀 Em Risco (Leais)',
        '🌱 Novos Clientes',
        ' hibernando'
    ]

    df_rfm_regras['Segmento'] = np.select(conditions, choices, default='Outros')
    
    return df_rfm_regras

@st.cache_data
def adicionar_recomendacoes(df_segmentado):
    """
    Prescreve o Risco de Churn e a Faixa de Desconto ideal para cada segmento.
    """
    if 'Segmento' not in df_segmentado.columns:
        return df_segmentado
        
    mapa_risco = {
        '🏆 Campeões': 'Baixo Risco 💚',
        '🌱 Novos Clientes': 'Médio Risco 🟡',
        '👀 Em Risco (Leais)': 'Alto Risco 🟠',
        ' hibernando': 'Altíssimo Risco 💔',
        'Outros': 'Indefinido'
    }
    
    # Regras de desconto baseadas na estratégia de cada segmento
    mapa_desconto = {
        '🏆 Campeões': '0% - 5% (Foco: Fidelidade)',
        '🌱 Novos Clientes': '10% - 15% (Incentivo 2ª Compra)',
        '👀 Em Risco (Leais)': '15% - 20% (Reativação Urgente)',
        ' hibernando': '10% - 20% (Tentativa de Retorno)',
        'Outros': '0%'
    }
    
    df_segmentado['Risco Churn'] = df_segmentado['Segmento'].map(mapa_risco)
    df_segmentado['Desconto Recomendado'] = df_segmentado['Segmento'].map(mapa_desconto)
    
    return df_segmentado


# --- Layout Principal do App ---

st.markdown("""
<div class="main-header">
    <h1>🎯 Segmentação e Otimização de Descontos</h1>
    <p>Analise o comportamento (RFM) dos clientes e saiba exatamente qual desconto oferecer para cada segmento.</p>
</div>
""", unsafe_allow_html=True)

df_merged_completo = carregar_dados()

if df_merged_completo is not None and not df_merged_completo.empty:
    
    st.header("Seleção do Restaurante")
    
    col1, col2 = st.columns(2)
    
    with col1:
        segmentos_loja_unicos = ['Todos'] + sorted(df_merged_completo['segmento'].unique())
        segmento_selecionado = st.selectbox(
            "Selecione o Segmento do Restaurante:",
            options=segmentos_loja_unicos
        )
    
    with col2:
        if segmento_selecionado == 'Todos':
            empresas_unicas = ['Todos (Visão Geral)']
        else:
            empresas_disponiveis = sorted(
                df_merged_completo[df_merged_completo['segmento'] == segmento_selecionado]['empresa'].unique()
            )
            empresas_unicas = ['Todos'] + empresas_disponiveis
        
        empresa_selecionada = st.selectbox(
            "Selecione o Restaurante Específico:",
            options=empresas_unicas,
            disabled=(segmento_selecionado == 'Todos')
        )
        
    # Filtra o DataFrame principal com base na seleção
    if segmento_selecionado == 'Todos':
        df_para_analise = df_merged_completo.copy()
        st.subheader("Analisando: Visão Geral de Todos os Restaurantes")
    elif empresa_selecionada == 'Todos' and segmento_selecionado != 'Todos':
        df_para_analise = df_merged_completo[
            df_merged_completo['segmento'] == segmento_selecionado
        ].copy()
        st.subheader(f"Analisando: Todos os Restaurantes do Segmento '{segmento_selecionado}'")
    else:
        df_para_analise = df_merged_completo[
            (df_merged_completo['segmento'] == segmento_selecionado) &
            (df_merged_completo['empresa'] == empresa_selecionada)
        ].copy()
        st.subheader(f"Analisando: {empresa_selecionada}")

    # Executa o pipeline de RFM e recomendação
    if not df_para_analise.empty:
        try:
            df_rfm = calcular_rfm(df_para_analise)
            df_segmentado = segmentar_por_regras(df_rfm)
            df_segmentado_final = adicionar_recomendacoes(df_segmentado)
            
            if df_segmentado_final.empty:
                raise ValueError("Nenhum cliente segmentado.")

            # Explicação dos segmentos e ações
            with st.expander("O que significa cada segmento e qual ação tomar?", expanded=False):
                st.markdown("""
                - **🏆 Campeões:** Seus melhores clientes. Recentes e Frequentes.
                  - **Ação:** Risco Baixo (💚). **Desconto: 0-5%**. Foco em fidelidade, não em preço (ex: brindes, acesso VIP).
                
                - **🌱 Novos Clientes:** Recentes, mas compraram pouco.
                  - **Ação:** Risco Médio (🟡). **Desconto: 10-15%**. Foco em gerar a *segunda compra* e criar o hábito.
                
                - **👀 Em Risco (Leais):** Clientes de alto valor/frequência que estão sumindo!
                  - **Ação:** Risco Alto (🟠). **Desconto: 15-20%**. Campanha de reativação *urgente* e personalizada.
                
                - ** hibernando:** Clientes antigos e com poucas compras.
                  - **Ação:** Risco Altíssimo (💔). **Desconto: 10-20%**. Campanha de "última chance" para reativar quem vale a pena.
                """)

            st.header("Análise de Segmentos e Otimização 📊")
            
            segmentos_unicos = sorted(df_segmentado_final['Segmento'].unique())
            
            with st.expander("Métricas Médias por Segmento", expanded=True):
                
                segmentos_selecionados = st.multiselect(
                    "Filtrar segmentos na visualização:",
                    options=segmentos_unicos,
                    default=segmentos_unicos
                )
                
                st.subheader("Perfil Médio e Desconto Recomendado")
                if not df_segmentado_final.empty:
                    # Tabela de métricas agregadas
                    df_metricas = df_segmentado_final.groupby('Segmento').agg(
                        Total_Clientes=('customer', 'nunique'),
                        Risco_Churn=('Risco Churn', 'first'),
                        Desconto_Recomendado=('Desconto Recomendado', 'first'),
                        Recência_Média=('Recência', 'mean'),
                        Frequência_Média=('Frequência', 'mean'),
                        Valor_Médio=('Valor Monetário', 'mean')
                    ).sort_values('Valor_Médio', ascending=False)
                    
                    st.dataframe(df_metricas.style.format({
                        'Recência_Média': '{:.1f} dias',
                        'Frequência_Média': '{:.1f} pedidos',
                        'Valor_Médio': 'R$ {:.2f}'
                    }), use_container_width=True)

            # Filtra o DF final para as abas com base no multiselect
            if not segmentos_selecionados:
                st.warning("Nenhum segmento selecionado. Ajuste o filtro acima.")
                df_filtrado_final = df_segmentado_final.iloc[0:0]
            else:
                df_filtrado_final = df_segmentado_final[
                    df_segmentado_final['Segmento'].isin(segmentos_selecionados)
                ]

            # Abas de Visualização
            tab1, tab2 = st.tabs([
                "📊 Visualização Gráfica", 
                "📋 Tabela de Clientes (Lista de Ação)"
            ])

            # Aba 1: Gráfico 3D
            with tab1:
                st.header(f"Visualização 3D ({df_filtrado_final.shape[0]} clientes)")
                if not df_filtrado_final.empty:
                    fig = px.scatter_3d(
                        df_filtrado_final,
                        x='Recência', y='Frequência', z='Valor Monetário',
                        color='Segmento',
                        hover_name='name',
                        hover_data={ 
                            'Risco Churn': True, 
                            'Desconto Recomendado': True,
                            'Recência': True, 
                            'Frequência': True, 
                            'Valor Monetário': ':.2f'
                        },
                        title="Segmentação RFM (Baseada em Regras)"
                    )
                    fig.update_layout(
                        margin=dict(l=0, r=0, b=0, t=40),
                        scene=dict(xaxis_title='Recência', yaxis_title='Frequência', zaxis_title='Valor Monetário')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Nenhum dado para exibir no gráfico.")

            # Aba 2: Tabela de Ação
            with tab2:
                st.header(f"Lista de Ação de Descontos ({df_filtrado_final.shape[0]} clientes)")
                st.markdown("Use esta tabela para criar suas campanhas de marketing. Exporte a lista abaixo.")
                
                @st.cache_data
                def convert_df_to_csv(df):
                    if df.empty:
                        return "".encode('utf-8-sig')
                    # 'utf-8-sig' garante que o Excel leia emojis 🏆 corretamente
                    return df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')

                csv_data = convert_df_to_csv(df_filtrado_final)
                
                st.download_button(
                    label="📥 Baixar Lista de Ação (CSV)",
                    data=csv_data,
                    file_name=f"lista_acao_descontos.csv",
                    mime="text/csv",
                    disabled=df_filtrado_final.empty
                )
                
                colunas_exibir = [
                    'name', 'Segmento', 'Risco Churn', 'Desconto Recomendado', 
                    'Recência', 'Frequência', 'Valor Monetário'
                ]
                if not df_filtrado_final.empty:
                    df_display = df_filtrado_final[colunas_exibir].set_index('name').sort_values('Valor Monetário', ascending=False)
                    st.dataframe(
                        df_display, 
                        use_container_width=True,
                        column_config={
                            "name": "Cliente",
                            "Segmento": "Segmento (Regra)",
                            "Risco Churn": "Risco (Regra)",
                            "Desconto Recomendado": st.column_config.TextColumn(
                                "Ação de Desconto Recomendada",
                                width="medium"
                            ),
                            "Recência": "Recência (dias)",
                            "Frequência": "Frequência (pedidos)",
                            "Valor Monetário": st.column_config.NumberColumn(
                                "Valor (LTV)", format="R$ %.2f"
                            )
                        }
                    )
                else:
                    st.warning("Nenhum dado para exibir na tabela.")
        
        except ValueError as e:
            st.error(f"Não foi possível processar a segmentação para este filtro. Causa provável: não há clientes suficientes ou diversidade de dados. Erro: {e}")
        except Exception as e:
             st.error(f"Ocorreu um erro inesperado durante a análise: {e}")
    
    else:
        st.error("Nenhum pedido encontrado para os filtros selecionados. Por favor, ajuste a seleção.")

else:
    st.error("Falha ao carregar os dados iniciais. Verifique os arquivos CSV.")

# Footer
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