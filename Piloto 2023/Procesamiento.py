# Módulos estándar de Python
import concurrent
import concurrent.futures
import os
import pickle
import re
import signal
import sys
import time
import io
from io import BytesIO

# Módulos de terceros
import boto3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# TensorFlow y Keras
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img


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

# Leo el Archivo obtenido con todas las rutas de las imágenes del 2023.
df = pd.read_csv('Piloto 2023/ArchivosUtiles/Muestreo_CT_PatAzul.csv')
paths_filtrados = df['Ruta'].tolist()

# Verificar si el archivo CSV existe
archivo_existe = os.path.exists('Piloto 2023/ArchivosUtiles/datasetFechaHora.pkl')

# Si el archivo existe, cargarlo en un DataFrame
if archivo_existe:
    df_procesado = pd.read_pickle('Piloto 2023/ArchivosUtiles/datasetFechaHora.pkl')
else:
    df_procesado = pd.DataFrame(columns=['Ruta', 'Fecha', 'Hora'])

paths_filtrados = [valor for valor in paths_filtrados if valor not in df_procesado['Ruta'].values]

#  Funcion para extraer la fecha y hora de la metadata de una imagen
def get_date_time_from_image(path):
    """Extrae la fecha y hora de la metadata de una imagen."""
    try:
        with Image.open(path) as img:
            exif_data = img._getexif()
            if exif_data and 36867 in exif_data: 
                date_time = exif_data[36867]
                date, time = date_time.split(" ")
                return date, time
    except Exception as e:
        print(f"Error processing image {path}: {e}")

# Definir una función para cargar imágenes desde S3
def procesar_imagen(ruta):
    global df_procesado
    try:
        obj = s3.get_object(Bucket=nombre_bucket_s3, Key=ruta)
        # Leer el contenido del objeto S3
        imagen_bytes = io.BytesIO(obj['Body'].read())

        # Aplicar la función para obtener fecha y hora de la imagen
        fecha, hora = get_date_time_from_image(imagen_bytes)
        
        # Convertir la fecha y hora a objetos datetime y luego formatear
        fecha = pd.to_datetime(fecha, format="%Y:%m:%d").date()
        hora = pd.to_datetime(hora, format="%H:%M:%S").time()

        # Agregar la ruta y la imagen al DataFrame
        nueva_fila = pd.DataFrame([[ruta, fecha, hora]], columns=df_procesado.columns)
        df_procesado = pd.concat([df_procesado, nueva_fila], ignore_index=True)

        # Imprimir el progreso utilizando tqdm
        pbar.update(1)  # Incrementa el contador de progreso

        if (pbar.n + 1) % 1000 == 0:
            df_procesado.to_pickle('Piloto 2023/ArchivosUtiles/datasetFechaHora.pkl')
            pbar.write(f'se guardaron los cambios: {len(df_procesado)}')
    except Exception as e:
        print(f'Error al procesar la imagen {ruta}: {str(e)}')

# Función para manejar la señal de interrupción (Ctrl + C)
def manejar_interrupcion(signal, frame):
    global df_procesado
    # Guardar el DataFrame en un archivo CSV antes de salir
    df_procesado.to_pickle('Piloto 2023/ArchivosUtiles/datasetFechaHora.pkl')
    print('Proceso interrumpido. Guardando datos en "dataset_2023.pkl"')
    sys.exit(0)

# Configurar la señal de interrupción (Ctrl + C) para guardar los datos antes de salir
signal.signal(signal.SIGINT, manejar_interrupcion)


# Crear una barra de progreso con tqdm
total_imagenes = len(paths_filtrados)
pbar = tqdm(total=total_imagenes, desc='Procesando imágenes', unit='img')
i = 0

# Iniciar el tiempo
start_time = time.time()

# Número de procesos o subprocesos concurrentes que deseas ejecutar
num_procesos_concurrentes = os.cpu_count()  # Puedes ajustar este valor

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
df_procesado.to_pickle('Piloto 2023/ArchivosUtiles/datasetFechaHora.pkl')
print('Proceso completado. Datos guardados en "datasetFechaHora.pkl"')


