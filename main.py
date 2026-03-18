from dotenv import load_dotenv 
import os
import boto3
import requests
import datetime 
from dateutil.relativedelta import relativedelta
import json


load_dotenv() 

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('BUCKET_NAME')

def write_files(data_inicial, months, file_path):
    for month in range(12):
        print(month+1)

        data_final = data_inicial + relativedelta(months=1)
        url = f'https://api.openf1.org/v1/sessions?date_start>={data_inicial}&date_start<{data_final}' 
        data = requests.get(url).json()
        
        file_name = f'senssion {data_final}'
        
        with open(f'{file_path}/{file_name}.json', "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        data_inicial = data_final 

    return f'Arquivos escritos com sucesso na pasta {file_path}'

def upload_files(client, file_path, bucket_name): 

    for file in os.listdir(file_path):
        print(f'Enviando arquivo {file}')
        client.upload_file(f'{file_path}/{file}', bucket_name, file)
        print('Envio concluído')


s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

data_inicial = datetime.date(2025,1,1)
file_path = 'sessions'
write_files(data_inicial,12,file_path)

upload_files(s3_client,file_path,BUCKET_NAME)