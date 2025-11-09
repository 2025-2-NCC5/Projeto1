Projeto: Monitoramento de Instância na Nuvem com IA

Este projeto implementa um sistema de monitoramento de recursos (CPU e Memória) e aplica um conjunto de modelos de Inteligência Artificial para analisar tanto os dados de monitoramento quanto um conjunto de dados de negócio (base_unificada.csv).

O sistema é totalmente containerizado usando Docker e Docker Compose.

## Modelos de IA Implementados
Este projeto cumpre o requisito de aplicar múltiplos exercícios de IA:

Detecção de Anomalias (Isolation Forest):
Arquivo: app/detector_anomalia.py
Objetivo: Analisa o histórico de monitoramento (historico.csv) para encontrar picos e padrões de uso inesperados de CPU e Memória.
Tipo: IA Não Supervisionada.

Regressão Linear (LinearRegression):
Arquivo: app/regressao_linear.py
Objetivo: Prevê o totalAmount com base em outras features (como quantidade, preparationTime) do arquivo base_unificada.csv.
Tipo: IA Supervisionada.

Redução de Dimensionalidade (PCA):
Arquivo: app/pca.py
Objetivo: Visualiza os dados da base_unificada.csv em 2D para identificar padrões.
Tipo: IA Não Supervisionada.

Visualização (t-SNE):
Arquivo: app/tsne_visualizacao.py
Objetivo: Visualiza os dados da base_unificada.csv em 2D, focado em agrupar vizinhos próximos.
Tipo: IA Não Supervisionada.

Como Rodar o Projeto com Docker

Este projeto é gerenciado com docker-compose. Cada ação é executada como um serviço separado.
Pré-requisitos
Docker
Docker Compose

Etapa 1: Coletar Dados de Monitoramento
Primeiro, precisamos gerar o arquivo historico.csv com os dados de CPU e Memória.

Abra seu terminal na raiz do projeto.
# Execute o serviço monitor:
docker-compose up monitor
Deixe o terminal rodando por 1-2 minutos para coletar dados.
Pressione Ctrl + C para parar o monitor.

Etapa 2: Executar os Modelos de IA
Agora você pode executar qualquer um dos serviços de IA. Eles lerão os dados da pasta /data e salvarão seus resultados (gráficos ou modelos .pkl) lá.

# Para analisar os dados de monitoramento (CPU/Memória):
docker-compose up detector_anomalia-ia
Ação: Roda o Isolation Forest nos dados do historico.csv.
Resultado: Salva os gráficos grafico_cpu_anomalias.png e grafico_memoria_anomalias.png na pasta data/.

Para rodar os modelos sobre os dados de negócio (base_unificada.csv):

# Para treinar a Regressão Linear
docker-compose up regressao_linear-ia

# Para gerar o gráfico PCA
docker-compose up pca-ia

# Para gerar o gráfico t-SNE
docker-compose up tsne-ia

Resultado: Salva os respectivos gráficos e arquivos na pasta data/.

Dica: Se Você Alterar o Código

Se você modificar qualquer arquivo .py, force o Docker a reconstruir a imagem com suas alterações usando a flag --build:

# Exemplo: Re-rodando o PCA após uma mudança no código
docker-compose up --build pca-ia

