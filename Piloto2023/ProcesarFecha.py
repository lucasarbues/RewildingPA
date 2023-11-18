# Módulos estándar de Python
import concurrent
import concurrent.futures
import os
import signal
import sys
import time
import io
from io import BytesIO

# Módulos de terceros
import boto3
import pandas as pd
from PIL import Image
from tqdm import tqdm

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

# Obtengo las rutas que no se han procesado.
# paths_filtrados que no esten en df_procesado['Ruta']
paths_filtrados = list(set(paths_filtrados) - set(df_procesado['Ruta']))

#  Funcion para extraer la fecha y hora de la metadata de una imagen
def get_date_time_from_image(path, pbar):
    try:
        with Image.open(path) as img:
            exif_data = img._getexif()
            if exif_data and 36867 in exif_data:
                date_time = exif_data[36867]
                date, time = date_time.split(" ")
                return date, time
    except Exception as e:
        pbar.write(f"Error processing image {path}: {e}")
    return None, None

# Definir una función para cargar imágenes desde S3
def procesar_imagen(ruta):
    try:
        obj = s3.get_object(Bucket=nombre_bucket_s3, Key=ruta)
        imagen_bytes = io.BytesIO(obj['Body'].read())
        fecha, hora = get_date_time_from_image(imagen_bytes, pbar)
        if fecha and hora:
            fecha = pd.to_datetime(fecha, format="%Y:%m:%d").date()
            hora = pd.to_datetime(hora, format="%H:%M:%S").time()
            return ruta, fecha, hora
    except Exception as e:
        pbar.write(f'Error al procesar la imagen {ruta}: {str(e)}')
    return ruta, None, None

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

# Iniciar el tiempo
start_time = time.time()

# Número de procesos o subprocesos concurrentes que deseas ejecutar
num_procesos_concurrentes = os.cpu_count()  # Puedes ajustar este valor

# Cambio en la lógica de ejecución para almacenar resultados en una lista
resultados = []
with concurrent.futures.ThreadPoolExecutor(max_workers=num_procesos_concurrentes) as executor:
    futures = [executor.submit(procesar_imagen, ruta) for ruta in paths_filtrados]
    for future in concurrent.futures.as_completed(futures):
        resultados.append(future.result())
        pbar.update(1)

        # Cada 1000 imágenes, guarda el DataFrame
        if len(resultados) > 1000:
            df_temporal = pd.DataFrame(resultados, columns=['Ruta', 'Fecha', 'Hora'])
            df_procesado = pd.concat([df_procesado, df_temporal], ignore_index=True)
            df_procesado.to_pickle('Piloto 2023/ArchivosUtiles/datasetFechaHora.pkl')
            pbar.write(f'Se guardaron los cambios después de procesar {len(df_procesado)} imágenes.')
            resultados = []  # Reiniciar la lista de resultados


# Al final del procesamiento, guarda cualquier imagen restante
if resultados:
    df_temporal = pd.DataFrame(resultados, columns=['Ruta', 'Fecha', 'Hora'])
    df_procesado = pd.concat([df_procesado, df_temporal], ignore_index=True)
    df_procesado.to_pickle('Piloto 2023/ArchivosUtiles/datasetFechaHora.pkl')
    pbar.write(f'Se guardaron los cambios después de procesar {len(df_procesado)} imágenes.')
    
# Cerrar la barra de progreso
pbar.close()

# Guardar el DataFrame en un archivo CSV al finalizar
df_procesado.to_pickle('Piloto 2023/ArchivosUtiles/datasetFechaHora.pkl')
print('Proceso completado. Datos guardados en "datasetFechaHora.pkl"')


