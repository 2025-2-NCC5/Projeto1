# app/monitor.py
import psutil
import time
import csv
import os
from datetime import datetime

def coletar_dados(intervalo=5, output_path="/data/historico.csv"):
    """
    Coleta o uso de CPU e memória em intervalos regulares e salva em um CSV.

    Args:
        intervalo (int): intervalo de coleta em segundos.
        output_path (str): caminho do arquivo CSV de saída.
    """
    #os.makedirs(os.path.dirname(output_path), exist_ok=True)
    arquivo_existe = os.path.isfile(output_path)

    with open(output_path, mode="a", newline="", encoding="utf-8") as csvfile:
        campos = ["timestamp", "cpu_percent", "mem_percent"]
        writer = csv.DictWriter(csvfile, fieldnames=campos)

        # Cria cabeçalho se o arquivo for novo
        if not arquivo_existe:
            writer.writeheader()

        print(f"⏱️ Iniciando coleta de métricas (a cada {intervalo}s)... Pressione Ctrl+C para parar.\n")
#
        try:
            while True:
                cpu_percent = psutil.cpu_percent(interval=None)
                mem_percent = psutil.virtual_memory().percent
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                writer.writerow({
                    "timestamp": timestamp,
                    "cpu_percent": cpu_percent,
                    "mem_percent": mem_percent
                })
                csvfile.flush()  # garante gravação imediata

                print(f"{timestamp} | CPU: {cpu_percent:.1f}% | MEM: {mem_percent:.1f}%")
                time.sleep(intervalo)

        except KeyboardInterrupt:
            print("\nColeta encerrada pelo usuário.")
            pass


if __name__ == "__main__":
    coletar_dados(intervalo=5)
