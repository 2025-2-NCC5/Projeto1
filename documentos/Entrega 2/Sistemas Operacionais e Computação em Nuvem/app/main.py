import argparse
import sys

# --- 1. Importar TODAS as suas funções ---
try:
    from monitor import coletar_dados
    from regressao_linear import treinar_modelo 
    from tsne import gerar_visualizacao 
    from pca import gerar_visualizacao_pca   
    from detector_anomalia import analisar_anomalias 
except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Verifique se todos os arquivos .py (monitor, tsne_visualizacao, pca, anomaly_detector) estão na pasta /app.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Monitoramento e Modelos de IA - Projeto Integrado"
    )

    # --- 2. Definir as 'choices' EXATAMENTE como no docker-compose.yml ---
    parser.add_argument(
        "acao",
        type=str,
        choices=[
            "monitor", 
            "regressao_linear",  # <- Corresponde ao seu docker-compose
            "tsne", 
            "pca",                 # <- Corresponde ao seu docker-compose
            "detector_anomalia"  # <- Corresponde ao seu docker-compose
        ],
        help="Escolha a ação a ser executada."
    )

    parser.add_argument(
        "--intervalo",
        type=int,
        default=5,
        help="Intervalo em segundos para coleta (usado apenas em 'monitor')."
    )

    args = parser.parse_args()

    # --- 3. Criar a lógica para chamar cada script ---
    if args.acao == "monitor":
        print("Iniciando modo: Monitoramento de Recursos")
        coletar_dados(intervalo=args.intervalo)

    elif args.acao == "regressao_linear":
        print("Iniciando modo: Treinamento - Regressão Linear")
        # Chama a função do regressao_linear.py
        treinar_modelo() 

    elif args.acao == "tsne":
        print("Iniciando modo: Visualização - t-SNE")
        # Chama a função do tsne_visualizacao.py
        gerar_visualizacao() 

    elif args.acao == "pca":
        print("Iniciando modo: Visualização - PCA")
        # Chama a função do pca.py
        gerar_visualizacao_pca() 

    elif args.acao == "detector_anomalia":
        print("Iniciando modo: Análise - Detecção de Anomalias")
        # Chama a função do anomaly_detector.py
        analisar_anomalias() 


if __name__ == "__main__":
    main()

