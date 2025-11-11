# 1_BSC_Dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go

# --- Configuração da Página ---
st.set_page_config(page_title="Dashboard BSC", 
                   layout="wide")

st.logo(
    'assets/logo_projeto.png',
    size="large",
)

# --- CSS Customizado ---
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

    /* Ajusta a cor de Fundo dos expanders */
    div[data-testid="stExpander"] {
        background-color: var(--background-light);
        border-radius: 10px;
    }
    div[data-testid="stExpander"] > details > summary {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--secondary-color);
    }

    /* Ajusta a cor dos botões de rádio */
    div[data-baseweb="radio"] {
        font-weight: 600;
        color: var(--text-color-light);
    }

    /* CSS da Sidebar */
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

    /* CSS do Footer */
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


# --- Sidebar ---
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

# --- Título Principal ---
st.markdown("""
<div class="main-header">
    <h1>🚀 Painel de Performance (BSC)</h1>
    <p>Uma visão de 360° do seu negócio, balanceando 4 pilares: Financeiro, Clientes, Processos e Aprendizado.</p>
</div>
""", unsafe_allow_html=True)


# --- Caminho para arquivo ---
# Tenta encontrar o caminho do CSV de forma flexível
try:
    ROOT_DIR = Path(__file__).resolve().parent.parent
    DATA_PATH = ROOT_DIR / "backend" / "utils" / "base_unificada.csv"
    if not DATA_PATH.exists():
        DATA_PATH = Path("backend/utils/base_unificada.csv")
except NameError:
    # Se __file__ não estiver definido (ex: rodando em certos notebooks)
    DATA_PATH = Path("backend/utils/base_unificada.csv")


# --- Funções utilitárias ---
@st.cache_data
def load_data(file_path):
    """
    Carrega os dados da 'base_unificada.csv'.
    Tenta diferentes codificações para robustez.
    Converte colunas numéricas essenciais e datas.
    """
    if not Path(file_path).exists():
        st.error(f"Erro Crítico: Arquivo de dados não encontrado em '{file_path}'. Verifique o caminho.")
        return pd.DataFrame() 

    encodings = ["utf-8", "latin1", "cp1252"]
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(file_path, sep=';', encoding=enc, low_memory=False)
            break 
        except Exception:
            continue 
    
    if df is None:
        st.error(f"Não foi possível ler o arquivo de dados em '{file_path}' com as codificações testadas.")
        return pd.DataFrame()

    # Limpeza e conversão de tipos
    for col in ['totalAmount', 'preparationTime', 'takeOutTimeInSeconds', 'quantidade']:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    for col_data in ['createdAt', 'updatedAt']:
         if col_data in df.columns:
             df[col_data] = pd.to_datetime(df[col_data], dayfirst=True, errors='coerce')
             
    df.dropna(subset=['totalAmount', 'id', 'customer', 'segmento', 'empresa', 'createdAt'], inplace=True)
    
    return df

@st.cache_data
def calculate_kpis(df):
    """
    Calcula os KPIs primários agrupados por 'segmento' e 'empresa'.
    Usa 'Tempo_de_Uso_Dias' (baseado no primeiro pedido) para Aprendizado.
    """
    if df.empty: return pd.DataFrame()
    
    group_cols = [c for c in ['segmento', 'empresa'] if c in df.columns]
    if not group_cols:
        st.warning("Colunas 'segmento' ou 'empresa' não encontradas. Agrupando no geral.")
        df['geral'] = 'Todos'
        group_cols = ['geral']
        
    agg_funcs = {
        'totalAmount': ['sum', 'mean'],
        'id': ['nunique'],
        'customer': ['nunique'],
        'preparationTime': ['mean'],
        'takeOutTimeInSeconds': ['mean'],
        'quantidade': ['sum'],
        'extraInfo': ['nunique'],
        'createdAt': ['min']
    }
    
    # Valida quais agregações são possíveis com as colunas existentes
    valid_agg = {}
    for col, funcs in agg_funcs.items():
        if col in df.columns:
            for func in funcs:
                new_col_name = f"{col}_{func}"
                valid_agg[new_col_name] = (col, func)
    
    if not valid_agg:
        st.error("Nenhuma coluna de KPI válida ('totalAmount', 'id', etc.) encontrada nos dados.")
        return pd.DataFrame()

    kpi_df = df.groupby(group_cols).agg(**valid_agg).reset_index()

    rename_map = {
        'totalAmount_sum': 'Faturamento_Total',
        'totalAmount_mean': 'Ticket_Medio',
        'id_nunique': 'Total_Pedidos',
        'customer_nunique': 'Clientes_Unicos',
        'preparationTime_mean': 'Tempo_Preparo_Medio',
        'takeOutTimeInSeconds_mean': 'Tempo_Retirada_Medio_Sec',
        'quantidade_sum': 'Total_Itens_Vendidos',
        'extraInfo_nunique': 'Variedade_Produtos',
        'createdAt_min': 'Data_Primeiro_Pedido'
    }
    kpi_df.rename(columns=rename_map, inplace=True)

    # KPIs derivados
    if 'Total_Pedidos' in kpi_df.columns and 'Clientes_Unicos' in kpi_df.columns:
        kpi_df['Pedidos_Por_Cliente'] = kpi_df['Total_Pedidos'] / kpi_df['Clientes_Unicos'].replace(0, np.nan)
    
    if 'Data_Primeiro_Pedido' in kpi_df.columns:
        hoje = pd.to_datetime('today')
        kpi_df['Tempo_de_Uso_Dias'] = (hoje - kpi_df['Data_Primeiro_Pedido']).dt.days
    
    return kpi_df

@st.cache_data
def calculate_bsc_scores(kpi_df):
    """
    Calcula os Scores BSC (0 a 1) para cada restaurante,
    normalizando os KPIs DENTRO de cada segmento.
    Usa Tempo_de_Uso_Dias para o pilar Aprendizado.
    """
    if kpi_df.empty: return pd.DataFrame()
    
    df = kpi_df.copy()
    
    all_cols = set(df.columns)
    higher_is_better = list(all_cols.intersection(['Faturamento_Total','Ticket_Medio','Total_Pedidos','Clientes_Unicos','Total_Itens_Vendidos','Pedidos_Por_Cliente', 'Tempo_de_Uso_Dias']))
    lower_is_better = list(all_cols.intersection(['Tempo_Preparo_Medio','Tempo_Retirada_Medio_Sec']))

    scaler = MinMaxScaler()
    
    if 'segmento' not in df.columns:
        df['segmento'] = 'Geral'
        
    segments = df['segmento'].unique()
    frames = []

    for seg in segments:
        seg_df = df[df['segmento'] == seg].copy()
        
        # Se houver apenas 1 restaurante no segmento, o MinMaxScaler falha (divide por zero).
        # Atribuímos um score médio (0.5) para evitar o erro.
        if len(seg_df) < 2:
            for col in higher_is_better + lower_is_better:
                if col in seg_df.columns:
                    seg_df[f'Norm_{col}'] = 0.5
            frames.append(seg_df)
            continue
            
        # Normaliza (Quanto mais alto, melhor)
        for col in higher_is_better:
            if col in seg_df.columns:
                seg_df_filled = seg_df[[col]].fillna(seg_df[col].mean())
                seg_df[f'Norm_{col}'] = scaler.fit_transform(seg_df_filled)
        
        # Normaliza (Quanto mais baixo, melhor)
        for col in lower_is_better:
            if col in seg_df.columns:
                seg_df_filled = seg_df[[col]].fillna(seg_df[col].mean())
                seg_df[f'Norm_{col}'] = 1.0 - scaler.fit_transform(seg_df_filled)
        
        frames.append(seg_df)
        
    if not frames:
        st.warning("Nenhum dado pôde ser normalizado.")
        return pd.DataFrame()

    final = pd.concat(frames)

    # Cálculo dos 4 Pilares do BSC
    cols_financeiro = [c for c in ['Norm_Faturamento_Total','Norm_Ticket_Medio','Norm_Total_Pedidos'] if c in final.columns]
    cols_cliente = [c for c in ['Norm_Clientes_Unicos','Norm_Pedidos_Por_Cliente'] if c in final.columns]
    cols_processos = [c for c in ['Norm_Tempo_Preparo_Medio','Norm_Tempo_Retirada_Medio_Sec','Norm_Total_Itens_Vendidos'] if c in final.columns]
    cols_aprendizado = [c for c in ['Norm_Tempo_de_Uso_Dias'] if c in final.columns]

    final['Score_Financeiro'] = final[cols_financeiro].mean(axis=1) if cols_financeiro else np.nan
    final['Score_Cliente'] = final[cols_cliente].mean(axis=1) if cols_cliente else np.nan
    final['Score_Processos'] = final[cols_processos].mean(axis=1) if cols_processos else np.nan
    final['Score_Aprendizado'] = final[cols_aprendizado].mean(axis=1) if cols_aprendizado else np.nan

    # Score BSC Final (Média dos 4 pilares)
    cols_bsc = [c for c in ['Score_Financeiro','Score_Cliente','Score_Processos','Score_Aprendizado'] if c in final.columns]
    final['Score_BSC'] = final[cols_bsc].mean(axis=1) if cols_bsc else np.nan

    # Cálculo de Rank
    final['Rank_Geral'] = final['Score_BSC'].rank(ascending=False, na_option='bottom').astype(int)
    if 'segmento' in final.columns:
        final['Rank_Segmento'] = final.groupby('segmento')['Score_BSC'].rank(ascending=False, na_option='bottom').astype(int)
    else:
        final['Rank_Segmento'] = final['Rank_Geral']

    return final.sort_values(['segmento','Score_BSC'], ascending=[True,False]).reset_index(drop=True)

# --- Carregar dados ---
df = load_data(DATA_PATH)
if df.empty:
    st.stop() 

kpi_df = calculate_kpis(df)
if kpi_df.empty:
    st.warning("Não foi possível calcular os KPIs. Verifique os dados de entrada.")
    st.stop()

scored_df = calculate_bsc_scores(kpi_df)
if scored_df.empty:
    st.warning("Não foi possível calcular os Scores BSC. Verifique os KPIs.")
    st.stop()


st.markdown("### 📊 Visão Geral do Desempenho (Big Numbers)")
col1, col2, col3, col4 = st.columns(4)

# Funções helper para formatar métricas com segurança
def format_currency(value):
    return f"R$ {value:,.0f}".replace(",", ".") if pd.notnull(value) else "N/A"
def format_number(value):
    return f"{value:,.0f}".replace(",", ".") if pd.notnull(value) else "N/A"
def format_time(value):
    return f"{value:.1f} min" if pd.notnull(value) else "N/A"

col1.metric("💰 Faturamento Total", format_currency(kpi_df['Faturamento_Total'].sum()))
col2.metric("🛍️ Pedidos Totais", format_number(kpi_df['Total_Pedidos'].sum()))
col3.metric("👥 Clientes Únicos", format_number(kpi_df['Clientes_Unicos'].sum()))
col4.metric("🕒 Tempo Médio de Preparo", format_time(kpi_df['Tempo_Preparo_Medio'].mean()))

st.markdown("---")


st.header("🏆 Ranking de Performance")

col1, col2 = st.columns(2)
with col1:
    seg_rank = ['Todos'] + sorted(scored_df['segmento'].dropna().unique().tolist())
    seg_selected = st.selectbox("Filtrar por Segmento (Ranking)", seg_rank)
with col2:
    if seg_selected != 'Todos':
        rest_options = sorted(scored_df[scored_df['segmento'] == seg_selected]['empresa'].dropna().unique().tolist())
    else:
        rest_options = sorted(scored_df['empresa'].dropna().unique().tolist())
    
    rest_selected = st.selectbox("Filtrar por Restaurante (Ranking)", ['Todos'] + rest_options)

# Lógica de filtragem do Ranking
if seg_selected != 'Todos':
    df_rank = scored_df[scored_df['segmento'] == seg_selected].copy()
    rank_col = 'Rank_Segmento'
else:
    df_rank = scored_df.copy()
    rank_col = 'Rank_Geral'

if rest_selected != 'Todos':
    df_rank = df_rank[df_rank['empresa'] == rest_selected].copy()

df_rank = df_rank.sort_values(rank_col)
cols = [rank_col, 'segmento','empresa','Score_BSC','Score_Financeiro','Score_Cliente','Score_Processos','Score_Aprendizado']
cols_existentes = [c for c in cols if c in df_rank.columns]
df_display = df_rank[cols_existentes].copy()

# Formata scores para percentual
for c in ['Score_BSC','Score_Financeiro','Score_Cliente','Score_Processos','Score_Aprendizado']:
    if c in df_display.columns:
        df_display[c] = pd.to_numeric(df_display[c], errors='coerce').apply(lambda x: f"{x:.2%}" if pd.notnull(x) else "N/A")

df_display.rename(columns={rank_col: "Rank"}, inplace=True)
st.dataframe(df_display.set_index("Rank"), use_container_width=True)


st.header("📈 Comparativo de Desempenho (Radar)")

colA, colB = st.columns(2)
with colA:
    compare_mode = st.radio("Comparar por:", ["Segmentos", "Restaurantes"], horizontal=True)
with colB:
    metric_type = st.selectbox("Métricas:", ["Pilares BSC", "KPIs Normalizados"], index=0)

display_mode = st.radio(
    "Modo de Visualização:", 
    ["Sobreposto (para Comparação)", "Lado a Lado (para Foco)"], 
    horizontal=True,
    index=0 
)

metrics = ['Score_Financeiro','Score_Cliente','Score_Processos','Score_Aprendizado','Score_BSC'] if metric_type == "Pilares BSC" else [c for c in scored_df.columns if c.startswith('Norm_')]
metrics = [m for m in metrics if m in scored_df.columns]

if not metrics:
    st.warning("Nenhuma métrica de BSC ou KPI normalizado disponível para comparação.")
else:
    if compare_mode == "Segmentos":
        segs = sorted(scored_df['segmento'].dropna().unique().tolist())
        if len(segs) < 2:
            st.info("É necessário ao menos 2 segmentos para comparar.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                seg1 = st.selectbox("Primeiro segmento", segs, index=0)
            with c2:
                seg2 = st.selectbox("Segundo segmento", segs, index=1)
            
            rad1 = scored_df[scored_df['segmento'] == seg1][metrics].mean()
            rad2 = scored_df[scored_df['segmento'] == seg2][metrics].mean()
            rad1['entity'] = seg1
            rad2['entity'] = seg2
            entities = [seg1, seg2]

    else: # Comparar por Restaurantes
        rests = sorted(scored_df['empresa'].dropna().unique().tolist())
        if len(rests) < 2:
            st.info("É necessário ao menos 2 restaurantes para comparar.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                rest1 = st.selectbox("Primeiro restaurante", rests, index=0)
            with c2:
                rest2 = st.selectbox("Segundo restaurante", rests, index=1)
            
            rad1 = scored_df[scored_df['empresa'] == rest1].iloc[0][metrics].copy()
            rad2 = scored_df[scored_df['empresa'] == rest2].iloc[0][metrics].copy()
            rad1['entity'] = rest1
            rad2['entity'] = rest2
            entities = [rest1, rest2]
    
    if 'rad1' in locals() and 'rad2' in locals():
        rad_df = pd.DataFrame([rad1, rad2])
        entities = [rad1['entity'], rad2['entity']] 
        metrics = [m for m in metrics if m in rad_df.columns] 
        
        # Cores (Laranja e Roxo, bom contraste)
        colors = ["rgba(234, 88, 12, 0.5)", "rgba(124, 58, 237, 0.5)"] 

        if display_mode == "Sobreposto (para Comparação)":
            fig = go.Figure()
            
            r1_values = rad_df.iloc[0][metrics].tolist()
            fig.add_trace(go.Scatterpolar(
                r=r1_values + [r1_values[0]], 
                theta=metrics + [metrics[0]], 
                fill='toself',
                name=entities[0],
                line=dict(color=colors[0].replace("0.5", "1.0"), width=3),
                fillcolor=colors[0]
            ))
            
            r2_values = rad_df.iloc[1][metrics].tolist()
            fig.add_trace(go.Scatterpolar(
                r=r2_values + [r2_values[0]], 
                theta=metrics + [metrics[0]], 
                fill='toself',
                name=entities[1],
                line=dict(color=colors[1].replace("0.5", "1.0"), width=3),
                fillcolor=colors[1]
            ))
        
            fig.update_layout(
                title=f"<b>Comparativo: {entities[0]} vs {entities[1]}</b>",
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])), 
                showlegend=True,
                margin=dict(t=50, b=50, l=30, r=30) 
            )
            st.plotly_chart(fig, use_container_width=True)

        else: # Modo "Lado a Lado (para Foco)"
            colR1, colR2 = st.columns(2)
            for idx, col in enumerate([colR1, colR2]):
                r = rad_df.iloc[idx]
                entity_name = entities[idx]
                values = r[metrics].tolist() + [r[metrics].tolist()[0]]
                labels = metrics + [metrics[0]]
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=labels,
                    fill='toself',
                    name=entity_name,
                    line=dict(color=colors[idx].replace("0.5", "1.0"), width=3),
                    fillcolor=colors[idx]
                ))
                fig.update_layout(
                    title=f"<b>{entity_name}</b>",
                    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                    showlegend=False,
                    margin=dict(t=50, b=50, l=30, r=30)
                )
                col.plotly_chart(fig, use_container_width=True)


st.divider()
st.header("🔍 Detalhe por Restaurante")

# Tenta usar o restaurante selecionado no filtro de Ranking
selected_restaurant_from_filter = rest_selected 

if 'empresa' in df_display.columns:
    rest_list = df_display['empresa'].dropna().unique().tolist()
else:
    rest_list = []

if not rest_list and selected_restaurant_from_filter == 'Todos':
     st.info("Nenhum restaurante disponível para o filtro atual.")
else:
    # Se um restaurante específico já foi filtrado no ranking, use-o
    if selected_restaurant_from_filter != 'Todos' and selected_restaurant_from_filter in scored_df['empresa'].values:
        current_rest = selected_restaurant_from_filter
    else:
        # Caso contrário, mostre um seletor
        if selected_restaurant_from_filter == 'Todos':
            rest_list = sorted(scored_df['empresa'].dropna().unique().tolist())
        current_rest = st.selectbox("Selecione o restaurante para ver detalhes:", ['Nenhum'] + rest_list, index=0)
        if current_rest == 'Nenhum':
            current_rest = None

    if current_rest:
        if not scored_df[scored_df['empresa'] == current_rest].empty:
            row = scored_df[scored_df['empresa'] == current_rest].iloc[0]
            kpi_row = kpi_df[kpi_df['empresa'] == current_rest].iloc[0] if not kpi_df[kpi_df['empresa'] == current_rest].empty else None

            st.subheader(f"Balanced Scorecard: {current_rest}")
            
            score_bsc_float = row['Score_BSC'] if pd.notnull(row['Score_BSC']) else 0.0
            
            # Mostra a barra de progresso com o texto
            st.progress(score_bsc_float, text=f"SCORE BSC GERAL: {score_bsc_float:.2%}")

            st.markdown("---")
            c1, c2, c3, c4 = st.columns(4)
            
            # Função interna para evitar repetição
            def write_kpi(kpi_row, kpi_name, label, kpi_format):
                if kpi_row is not None and kpi_name in kpi_row.index and pd.notnull(kpi_row[kpi_name]):
                    st.write(f"{label}: {kpi_format(kpi_row[kpi_name])}")
                else:
                    st.write(f"{label}: N/A")
            
            with c1:
                st.metric("💰 Score Financeiro", f"{row['Score_Financeiro']:.2%}" if pd.notnull(row['Score_Financeiro']) else "N/A")
                with st.expander("Ver KPIs"):
                    write_kpi(kpi_row, 'Faturamento_Total', "Faturamento", format_currency)
                    write_kpi(kpi_row, 'Ticket_Medio', "Ticket Médio", format_currency)
                    write_kpi(kpi_row, 'Total_Pedidos', "Pedidos", format_number)
            
            with c2:
                st.metric("🎯 Score Cliente", f"{row['Score_Cliente']:.2%}" if pd.notnull(row['Score_Cliente']) else "N/A")
                with st.expander("Ver KPIs"):
                    write_kpi(kpi_row, 'Clientes_Unicos', "Clientes", format_number)
                    write_kpi(kpi_row, 'Pedidos_Por_Cliente', "Pedidos/Cliente", lambda x: f"{x:.2f}")
            
            with c3:
                st.metric("⚙️ Score Processos", f"{row['Score_Processos']:.2%}" if pd.notnull(row['Score_Processos']) else "N/A")
                with st.expander("Ver KPIs"):
                    write_kpi(kpi_row, 'Tempo_Preparo_Medio', "T. Preparo (min)", format_time)
                    write_kpi(kpi_row, 'Tempo_Retirada_Medio_Sec', "T. Retirada (min)", lambda x: f"{(x/60):.1f} min")
                    write_kpi(kpi_row, 'Total_Itens_Vendidos', "Itens Vendidos", format_number)
            
            with c4:
                st.metric("💡 Score Aprendizado", f"{row['Score_Aprendizado']:.2%}" if pd.notnull(row['Score_Aprendizado']) else "N/A")
                with st.expander("Ver KPIs"):
                    write_kpi(kpi_row, 'Tempo_de_Uso_Dias', "Tempo de Uso", lambda x: f"{x:,.0f} dias")
        else:
            if current_rest: 
                 st.info(f"Restaurante '{current_rest}' não encontrado nos dados filtrados do ranking.")

# --- Rodapé ---
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