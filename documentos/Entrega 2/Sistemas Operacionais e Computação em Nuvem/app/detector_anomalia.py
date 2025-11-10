# app/anomaly_detector.py
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import os

def analisar_anomalias(
    input_path="/data/historico.csv",
    output_graph_cpu="/data/grafico_cpu_anomalias.png",
    output_graph_mem="/data/grafico_memoria_anomalias.png"
):
    print("Iniciando detecção de anomalias com IsolationForest...")

    # --- 1. Carregar os Dados de Monitoramento ---
    try:
        df = pd.read_csv(input_path)
        if df.empty:
            print(f"Aviso: O arquivo {input_path} está vazio. Rode o 'monitor' primeiro.")
            return
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {input_path}")
        print("Por favor, rode a ação 'monitor' primeiro para gerar o arquivo.")
        return
    
    # Converter timestamp para datetime para usar no gráfico
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # --- 2. Preparar os Dados para a IA ---
    # CPU e Memória para encontrar anomalias
    features = ['cpu_percent', 'mem_percent']
    X = df[features]

    # --- 3. Aplicar o IsolationForest ---
    # contamination='auto' ou um valor (ex: 0.05 = 5%)
    model = IsolationForest(contamination='auto', random_state=42)
    
    # Treinar o modelo
    model.fit(X)

    # Obter as predições
    # O modelo retorna 1 para "normal" (inlier) e -1 para "anomalia" (outlier)
    df['anomalia'] = model.predict(X)

    # Criar um dataframe separado apenas com as anomalias para plotar
    anomalias = df[df['anomalia'] == -1]
    num_anomalias = len(anomalias)
    
    if num_anomalias > 0:
        print(f"Detecção concluída: {num_anomalias} anomalias encontradas.")
    else:
        print("Detecção concluída: Nenhuma anomalia significativa encontrada.")

    # --- 4. Gerar Gráficos de Monitoramento (Entregável) ---
    
    # Gráfico 1: Anomalias de CPU
    plt.figure(figsize=(15, 6))
    plt.plot(df['timestamp'], df['cpu_percent'], label='Uso de CPU', color='blue')
    # Destacar as anomalias em vermelho
    plt.scatter(anomalias['timestamp'], anomalias['cpu_percent'], color='red', label='Anomalia Detectada', zorder=5)
    plt.title('Monitoramento de CPU com Detecção de Anomalias')
    plt.ylabel('CPU (%)')
    plt.xlabel('Tempo')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_graph_cpu)
    plt.close()
    print(f"Gráfico de anomalias de CPU salvo em {output_graph_cpu}")

    # Gráfico 2: Anomalias de Memória
    plt.figure(figsize=(15, 6))
    plt.plot(df['timestamp'], df['mem_percent'], label='Uso de Memória', color='green')
    # Destacar as anomalias em vermelho
    plt.scatter(anomalias['timestamp'], anomalias['mem_percent'], color='red', label='Anomalia Detectada', zorder=5)
    plt.title('Monitoramento de Memória com Detecção de Anomalias')
    plt.ylabel('Memória (%)')
    plt.xlabel('Tempo')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_graph_mem)
    plt.close()
    print(f"Gráfico de anomalias de memória salvo em {output_graph_mem}")

if __name__ == "__main__":
    analisar_anomalias()