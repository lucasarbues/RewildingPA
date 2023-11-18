import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from tensorflow.keras.optimizers import Adam
import pandas as pd
import numpy as np
import boto3
from PIL import Image
from io import BytesIO
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import re
import sys
import signal
import concurrent
from tqdm import tqdm
import time
import concurrent.futures
import pickle
import os

# Importo Informacion del AccessKey.
accessKey = pd.read_csv("ANoguera_accessKeys.csv")

# Importo Informacion del AccessKey.
accessKey = os.getenv("AccessKey")
secretKey = os.getenv("SecretKey")
# Configura tus credenciales de AWS si aún no lo has hecho
boto3.setup_default_session(aws_access_key_id=accessKey,
                           aws_secret_access_key=secretKey,
                           region_name='us-east-2')

# Nombre del bucket
nombre_bucket_s3 = 's3-pfa'

# Crea un cliente de S3
s3 = boto3.client('s3')

# Leer objetos_s3
with open('objetos_s3.pkl', 'rb') as archivo:
    objetos_s3 = pickle.load(archivo)

paths_filtrados = []

for path in objetos_s3:
    # Buscar "Muestreo ct Iberica" o "Muestreo ct sauce" en el path
    if "Muestreo ct Iberica" in path or "Muestreo ct sauce" in path:
        # Buscar el año en el path
        year_start = path.find("20")
        if year_start != -1:
            # Intentar extraer el año en formato "20XX"
            try:
                año = int(path[year_start:year_start+4])
                if año == 2023:
                    paths_filtrados.append(path)
            except ValueError:
                # Si no se puede convertir a int, intentar encontrar un año en el formato "CT S 2020"
                match = re.search(r'\b(20\d{2})\b', path)
                if match:
                    año = int(match.group(0))
                    if año == 2023:
                        paths_filtrados.append(path)

# Definir una función para cargar imágenes desde S3
def cargar_imagen_desde_s3(ruta, target_size=(150, 150)):
    obj = s3.get_object(Bucket=nombre_bucket_s3, Key=ruta)
    img = Image.open(BytesIO(obj['Body'].read()))

    # Redimensionar la imagen al tamaño objetivo
    img = tf.image.resize(img, target_size)

    return img

df_procesado = pd.read_pickle('dataset_2023.pkl')
df_procesado2 = pd.read_pickle('dataset_2023_2.pkl')
df_procesado = pd.concat([df_procesado,df_procesado2], ignore_index=True)

# Función para procesar las imágenes y agregarlas al DataFrame
def procesar_imagen(ruta):
    try:
        # Cargar y redimensionar la imagen
        img = cargar_imagen_desde_s3(ruta, target_size=(150, 150))

        # Agregar la ruta y la imagen al DataFrame
        df_procesado2.loc[len(df_procesado2)] = [ruta, img]

        # Imprimir el progreso utilizando tqdm
        pbar.update(1)  # Incrementa el contador de progreso

        if (pbar.n + 1) % 1000 == 0:
            df_procesado2.to_pickle('dataset_2023_2.pkl')
            print('se guardaron los cambios: ', pbar.n)
        # print(f'Imagen {ruta} procesada y almacenada en DataFrame')
    except Exception as e:
        print(f'Error al procesar la imagen {ruta}: {str(e)}')

# Función para manejar la señal de interrupción (Ctrl + C)
def manejar_interrupcion(signal, frame):
    global df_procesado2
    # Guardar el DataFrame en un archivo CSV antes de salir
    df_procesado2.to_pickle('dataset_2023_2.pkl')
    print('Proceso interrumpido. Guardando datos en "dataset_2023_2.pkl"')
    sys.exit(0)

# Configurar la señal de interrupción (Ctrl + C) para guardar los datos antes de salir
signal.signal(signal.SIGINT, manejar_interrupcion)

paths_filtrados = [valor for valor in paths_filtrados if valor not in df_procesado['Ruta'].values]

# Crear una barra de progreso con tqdm
total_imagenes = len(paths_filtrados)

pbar = tqdm(total=total_imagenes, desc='Procesando imágenes', unit='img')
i = 0

# Iniciar el tiempo
start_time = time.time()

# Número de procesos o subprocesos concurrentes que deseas ejecutar
num_procesos_concurrentes = 8  # Puedes ajustar este valor

# Usar ThreadPoolExecutor o ProcessPoolExecutor según tus necesidades
# ThreadPoolExecutor para subprocesos o ProcessPoolExecutor para procesos
with concurrent.futures.ThreadPoolExecutor(max_workers=num_procesos_concurrentes) as executor:
    # Ejecutar la función de procesamiento en paralelo para cada ruta
    resultados = list(executor.map(procesar_imagen, paths_filtrados))

# Calcular el tiempo transcurrido
end_time = time.time()
elapsed_time = end_time - start_time
print(f'Tiempo total transcurrido: {elapsed_time:.2f} segundos')

# Cerrar la barra de progreso
pbar.close()

# Guardar el DataFrame en un archivo CSV al finalizar
df_procesado2.to_pickle('dataset_2023_2.pkl')
print('Proceso completado. Datos guardados en "dataset_2023.pkl"')