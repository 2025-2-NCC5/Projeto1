import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import os

def gerar_visualizacao(input_path="/data/base_unificada.csv", output_path="/data/tsne_visualizacao.png"):
    # Leitura dos dados
    dataf = pd.read_csv(input_path, sep=";", encoding="cp1250")

    # Label Encoding
    le = LabelEncoder()
    for col in ['segmento', 'empresa', 'produto', 'customer']:
        dataf[col] = le.fit_transform(dataf[col])

    # Seleciona colunas numéricas
    numerical_cols = ['quantidade', 'totalAmount', 'preparationTime', 'takeOutTimeInSeconds']
    df_numerical = dataf[numerical_cols]

    # Normalização
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_numerical)

    # Aplica t-SNE
    tsne = TSNE(n_components=2, random_state=42, perplexity=30)
    X_tsne = tsne.fit_transform(df_scaled)

    # Cria gráfico
    plt.figure(figsize=(8, 6))
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=dataf['segmento'], cmap='viridis', s=50)
    plt.colorbar()
    plt.title('Visualização de Dados com t-SNE')
    plt.xlabel('Componente 1')
    plt.ylabel('Componente 2')

    # Salva no diretório data/
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfico salvo em {output_path}")

if __name__ == "__main__":
    gerar_visualizacao()