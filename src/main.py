import csv
import json
import os
from datetime import datetime
import pandas as pd

# Função para ler o JSON e mapear clientes
def load_clients(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    client_map = {client['fb_ad_account_id']: client['client'] for client in data if 'fb_ad_account_id' in client}
    return client_map

# Função para obter o último dia do mês anterior no formato YYYY-MM-DD
def get_last_day_previous_month():
    today = datetime.today()
    first_day_current_month = datetime(today.year, today.month, 1)
    last_day_previous_month = first_day_current_month - pd.Timedelta(days=1)
    return last_day_previous_month.strftime('%Y-%m-%d')

# Função para processar os arquivos CSV
def process_csv_files(input_dir, output_file, client_map):
    records = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_dir, filename)
            
            # Leitura das primeiras 10 linhas para extrair informações do cliente
            with open(file_path, 'r', encoding='utf-8') as file:
                client_info = [next(file) for _ in range(10)]
            
            # Extrair ID da conta de anúncios do Facebook da linha com "Conta:"
            fb_ad_account_id = None
            for line in client_info:
                if 'Conta:' in line:
                    fb_ad_account_id = line.split('Conta: ')[1].split(',')[0].strip()
                    break
            
            client = client_map.get(fb_ad_account_id, 'Unknown')

            # Depuração: imprimir o ID da conta, o nome do cliente e o nome do arquivo
            print(f"Arquivo: {filename}, ID da conta: {fb_ad_account_id}, Cliente: {client}")

            # Leitura do arquivo CSV a partir da linha 11
            df = pd.read_csv(file_path, encoding='utf-8', skiprows=10)

            # Buscar "Valor total cobrado" e "Total de fundos adicionados"
            valor_total_cobrado = None
            total_fundos_adicionados = None

            for i, row in df.iterrows():
                if 'Valor total cobrado' in str(row.iloc[1]):
                    valor_total_cobrado = row.iloc[2]
                elif 'Total de fundos adicionados' in str(row.iloc[1]):
                    total_fundos_adicionados = row.iloc[2]

            # Se não houverem valores, setar para 0
            if not valor_total_cobrado:
                valor_total_cobrado = 0
            if not total_fundos_adicionados:
                total_fundos_adicionados = 0

            # Adicionar registro
            records.append([client, '[TP]', total_fundos_adicionados, valor_total_cobrado, get_last_day_previous_month()])

    # Escrever o arquivo de saída
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['client', 'serviço', 'entrada', 'saída', 'data'])
        writer.writerows(records)

# Caminhos dos arquivos
json_file_path = 'data/input/clientes.json'
input_dir = 'data/input'
output_file = 'data/output/summary.csv'

# Executar processamento
client_map = load_clients(json_file_path)
process_csv_files(input_dir, output_file, client_map)

print(f"Processamento concluído. Dados salvos em {output_file}")
