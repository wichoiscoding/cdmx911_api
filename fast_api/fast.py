import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import os
import requests
import json
from fastapi import FastAPI
from google.cloud import storage
from io import BytesIO
import plotly.express as px

app = FastAPI()


@app.get('/name-alcaldia')
def get_name_alcaldia():

    with open('data/latlon.json', 'r') as archivo:
        data = json.load(archivo)

    names_alcaldias = data['Alcaldia']
    return {'alcaldias': names_alcaldias}


@app.get('/latlon')
def get_latlon(name_alcaldia: str):

    with open('data/latlon.json', 'r') as archivo:
        data = json.load(archivo)

    indice_alcaldia = data['Alcaldia'].index(name_alcaldia)

    # Obtener Latitud y Longitud
    latitud = data['Latitud'][indice_alcaldia]
    longitud = data['Longitud'][indice_alcaldia]

    return {'Latitud': latitud, 'Longitud': longitud}

@app.get('/main-map')
def get_main_map():
    mapa = gpd.read_file('data/joe_map.geojson')
    mapa = json.loads(mapa.to_json())
    return mapa

@app.get('/dynamic-data')
def get_dynamic_data(name_alcaldia: str):

    # Verificar si el archivo ya existe localmente
    local_file_path = f'data/{name_alcaldia}_data.csv'

    if os.path.exists(local_file_path):
        data_alcaldia = pd.read_csv(local_file_path)

    else:
        #gc info
        bucket_name = os.getenv('BUCKET_NAME')
        file_name = f'completa-alcaldia/{name_alcaldia}_data.csv'
        project_id = os.getenv('GCP_PROJECT')

        # Configura la conexión a gc
        client = storage.Client(project=project_id)
        bucket = client.bucket(bucket_name)

        # Descarga el archivo CSV como BytesIO
        blob = bucket.blob(file_name)
        content = blob.download_as_text()
        csv_data = BytesIO(content.encode('utf-8'))

        data_alcaldia = pd.read_csv(csv_data)

        # Convierte la columna 'fecha_creacion' a tipo datetime
        data_alcaldia['fecha_creacion'] = pd.to_datetime(data_alcaldia['fecha_creacion'])

        #Redondea la hora a horas
        data_alcaldia['hora_creacion'] = pd.to_datetime(data_alcaldia['hora_creacion'])
        data_alcaldia['hora_creacion'] = data_alcaldia['hora_creacion'].dt.round('H')


        # Extrae el año y el mes de la fecha de creación
        data_alcaldia['year'] = data_alcaldia['fecha_creacion'].dt.year
        data_alcaldia['month'] = data_alcaldia['fecha_creacion'].dt.month_name()

        # Guardar data local
        data_alcaldia.to_csv(local_file_path, index=False)


    # Agrupa por año, mes y tipo de incidente y cuenta la frecuencia
    data_grouped = data_alcaldia.groupby(['year', 'month', 'incidente_c4', 'hora_creacion']).size().reset_index(name='count')

    result = data_grouped.to_dict(orient='records')

    return {'data': result}

@app.get('/model-data')
def get_model_data(name_alcaldia: str):
    # Verificar si el archivo ya existe localmente
    local_file_path = f'data/predictions/{name_alcaldia}_pred.csv'
    if os.path.exists(local_file_path):
        pred_alcaldia = pd.read_csv(local_file_path)
    else:
        #gc info
        name_alcaldia = name_alcaldia.replace(' ', '_')
        bucket_name = os.getenv('BUCKET_NAME')
        file_name = f'predictions/{name_alcaldia}_pred.csv'
        project_id = os.getenv('GCP_PROJECT')
        # Configura la conexión a gc
        client = storage.Client(project=project_id)
        bucket = client.bucket(bucket_name)
        # Descarga el archivo CSV como BytesIO
        blob = bucket.blob(file_name)
        content = blob.download_as_text()
        csv_data = BytesIO(content.encode('utf-8'))
        pred_alcaldia = pd.read_csv(csv_data)
        # Convierte la columna 'fecha_creacion' a tipo datetime
        pred_alcaldia['semana_creacion'] = pd.to_datetime(pred_alcaldia['semana_creacion'])
        # Extrae el año y el mes de la fecha de creación
        pred_alcaldia['month'] = pred_alcaldia['semana_creacion'].dt.month_name()
        # Guardar data local
        pred_alcaldia.to_csv(local_file_path, index=False)
    # Agrupa por año, mes y tipo de incidente y cuenta la frecuencia
    data_grouped = pred_alcaldia.groupby('month')['numero_incidentes'].sum()
    meses = ["January", "February", "March", "April", "May", "June", "July", "August"]
    result = data_grouped.loc[meses].to_dict()
    return {'data': result}
