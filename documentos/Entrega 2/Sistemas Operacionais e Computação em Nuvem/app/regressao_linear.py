# app/modelo_ia.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

def treinar_modelo(input_path="/data/base_unificada.csv", modelo_path="/data/modelo_regressao.pkl"):
    # Leitura dos dados
    df = pd.read_csv(input_path, sep=";", encoding="cp1250")

    # Codificação de variáveis categóricas
    le = LabelEncoder()
    for col in ['segmento', 'empresa', 'produto', 'customer']:
        df[col] = le.fit_transform(df[col])

    # Seleciona variáveis preditoras e alvo
    features = ['quantidade', 'preparationTime', 'takeOutTimeInSeconds']
    target = 'totalAmount'

    X = df[features]
    y = df[target]

    # Normalização
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Divide em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Modelo simples
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Avaliação
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)

    print(f"Treinamento concluído.")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²: {r2:.3f}")

    # Salva o modelo treinado
    os.makedirs(os.path.dirname(modelo_path), exist_ok=True)
    joblib.dump({"modelo": model, "scaler": scaler}, modelo_path)
    print(f"Modelo salvo em {modelo_path}")

if __name__ == "__main__":
    treinar_modelo()
