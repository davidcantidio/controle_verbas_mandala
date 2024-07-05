import pandas as pd
import json

# Caminho do arquivo CSV fornecido
csv_file_path = '/home/debrito/Documentos/controle_verbas_mandala/data/Modelo - Planilha Cliente Tráfego Pago - dados do cliente.csv'
json_file_path = 'data/input/clientes.json'

# Ler o arquivo CSV
df = pd.read_csv(csv_file_path, dtype={
    "fb_ad_account_id": str,
    "id_instagram": str,
    "fb_page_id": str,
    "google_ads_account_id": str,
    "id_linkedin": str,
    "id_tiktok": str
})

# Transformar em JSON
clients_data = df.to_dict(orient='records')

# Salvar em um arquivo JSON
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(clients_data, json_file, indent=4, ensure_ascii=False)

print(f"JSON file saved at: {json_file_path}")
