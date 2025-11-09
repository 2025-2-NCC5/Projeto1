import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA  
import matplotlib.pyplot as plt
import os

def gerar_visualizacao_pca(input_path="/data/base_unificada.csv", output_path="/data/pca_visualizacao.png"):
    # Leitura dos dados
    try:
        dataf = pd.read_csv(input_path, sep=";", encoding="cp1250")
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {input_path}")
        print("Verifique o caminho do arquivo e tente novamente.")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return

    # Label Encoding
    le = LabelEncoder()
    # Copia para evitar SettingWithCopyWarning
    dataf_proc = dataf.copy()
    for col in ['segmento', 'empresa', 'produto', 'customer']:
        if col in dataf_proc.columns:
            dataf_proc[col] = le.fit_transform(dataf_proc[col])
        else:
            print(f"Aviso: Coluna '{col}' não encontrada para Label Encoding.")

    # Seleciona colunas numéricas
    numerical_cols = ['quantidade', 'totalAmount', 'preparationTime', 'takeOutTimeInSeconds']
    # Verifica se as colunas numéricas existem
    cols_existentes = [col for col in numerical_cols if col in dataf_proc.columns]
    if not cols_existentes:
        print("Erro: Nenhuma das colunas numéricas especificadas foi encontrada.")
        return
    
    df_numerical = dataf_proc[cols_existentes]

    # Normalização
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_numerical)

    # Aplica PCA
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(df_scaled)

    # Informa a variância explicada
    variancia_explicada = pca.explained_variance_ratio_
    print(f"Variância explicada pelo Componente 1: {variancia_explicada[0]:.2%}")
    print(f"Variância explicada pelo Componente 2: {variancia_explicada[1]:.2%}")
    print(f"Variância total explicada pelos 2 componentes: {sum(variancia_explicada):.2%}")

    # Cria gráfico
    plt.figure(figsize=(8, 6))
    # Usa a coluna 'segmento' original (de 'dataf') para o 'c' 
    cor = dataf['segmento'] if 'segmento' in dataf.columns else None
    
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], s=50, alpha=0.7)
    
    
    plt.title('Visualização de Dados com PCA')
    plt.xlabel('Componente Principal 1') # Alterado
    plt.ylabel('Componente Principal 2') # Alterado

    # Salva no diretório data/
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()
        print(f"Gráfico salvo em {output_path}")
    except Exception as e:
        print(f"Erro ao salvar o gráfico: {e}")

if __name__ == "__main__":
    gerar_visualizacao_pca()