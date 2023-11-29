import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, messagebox, ttk
from tkinter.font import Font
import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')
from tensorflow.keras.models import load_model
from datetime import datetime
from PIL import Image, ImageTk
import sys
import concurrent
import concurrent.futures
import torch
import torchvision.transforms as transforms
from torchvision.transforms import Resize
import numpy as np
import time
import logging
import threading

# Configuración del logging
logging.basicConfig(filename='Piloto2023/log_warnings.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

# Suprimir advertencias de Intel MKL, NNPACK y TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['MKL_THREADING_LAYER'] = 'GNU'
tf.get_logger().setLevel('ERROR')

import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# # Agrega la carpeta padre al sys.path
current_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from funciones import convert_to_pytorch_tensor, YOLOV5Base

def procesar_imagen_dataframe(imagen, target_size=(150, 150)):
    # Asegurarse de que la imagen es un tensor
    if not isinstance(imagen, tf.Tensor):
        imagen = tf.convert_to_tensor(imagen, dtype=tf.float32)

    # Cambiar el tamaño si es necesario
    if imagen.shape[:2] != target_size:
        imagen = tf.image.resize(imagen, target_size)

    # Expandir las dimensiones para simular un lote de una sola imagen
    tensor = tf.expand_dims(imagen, axis=0)

    return tensor

def Megadetector(image_path, image_tensor , model):
    try:
        # Leer y transformar la imagen
        image = convert_to_pytorch_tensor(image_tensor)
        num_detections, average_confidence = model.single_image_detection(img=image, conf_thres=0.4)

        return average_confidence, num_detections

    except Exception as e:
        logger.error(f'Megadetector Falla: {image_path}: {str(e)}')
        return None, None

def procesar_imagen(full_path, dfTensor, modelPresencia, modelGuanaco, modelMegadetector, confianzaAnimalInf, confianzaAnimalSup, confianzaGuanaco, confianzaCantidad):
    try:
        # El DataFrame ya tiene la informacion de sitio, año, camara, extra, archivo, fecha, hora.

        # El tensor se obtiene de dfTensor
        image_tensor = dfTensor[dfTensor['Ruta'] == full_path]['Imagen'].values[0]
        tensor = procesar_imagen_dataframe(image_tensor)

        # Predecir Presencia de Animal
        animal_proba = modelPresencia.predict(tensor, verbose=0)[0][0]
        animal = int(animal_proba > 0.5)
        validar = ((animal_proba >= (confianzaAnimalInf)) & (animal_proba <= confianzaAnimalSup))

        # Predecir Presencia de Guanaco si hay un animal
        guanaco_proba = None
        guanaco = None
        especie = None
        if animal == 1 and validar == False:
            guanaco_proba = modelGuanaco.predict(tensor, verbose=0)[0][0]
            guanaco = int(guanaco_proba > 0.5) if guanaco_proba is not None else None
            validar = ((animal_proba >= (confianzaAnimalInf)) & (animal_proba <= confianzaAnimalSup) | (guanaco_proba <= (confianzaGuanaco)))

        # Predecir Cantidad de Guanacos si hay un guanaco
        cantidad = None
        cantidad_proba = None
        if guanaco == 1 and validar == False:
            especie = 'Guanaco'
            mean_confidence, cant_pred = Megadetector(full_path, image_tensor, modelMegadetector)
            cantidad_proba = (cant_pred == 1) * mean_confidence + (1 - (cant_pred == 1)) * (1 - mean_confidence)
            cantidad = int(cant_pred == 1) if cant_pred is not None else None
            validar = ((animal_proba >= (confianzaAnimalInf)) & (animal_proba <= confianzaAnimalSup) | (guanaco_proba <= (confianzaGuanaco))) | (cantidad == 0) | (cantidad_proba <= (confianzaCantidad))

        return full_path, animal_proba, animal, guanaco_proba, guanaco, especie, cantidad_proba, cantidad, validar, 0

    except Exception as e:
        logger.error(f'Error al procesar la imagen {full_path}: {str(e)}')
    return full_path, "error", None, None, None, None, None, None, None, None


# Variables para la barra de progreso
current = 0
total_imagenes = 0

def update_progress_bar():
    """Actualiza la barra de progreso en la interfaz de Tkinter."""
    if(total_imagenes > 0):
        progress = 100 * (current / total_imagenes)
        progress_var.set(progress)
        progress_label.config(text=f"{current}/{total_imagenes} ({progress_var.get():.2f}%)")
        root.after(1000, update_progress_bar)

# Variables para el temporizador
start_time = None  # Marca de tiempo para cuando se inicia el procesamiento
running = False  # Estado para saber si el temporizador está activo

# Función para actualizar el temporizador
def update_timer():
    if running:
        # Calcular el tiempo transcurrido
        elapsed_time = time.time() - start_time
        # Convertir a horas:minutos:segundos
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        # Actualizar la etiqueta del temporizador
        timer_label.config(text=f"Tiempo transcurrido: {elapsed_time_str}")
        # Llamar a esta función nuevamente después de 1000ms (1 segundo)
        root.after(1000, update_timer)

# Función para iniciar el temporizador
def start_timer():
    global start_time, running
    start_time = time.time()
    running = True
    progress_label.config(text=f"Iniciando...")
    update_timer()

# Función para detener el temporizador
def stop_timer():
    global running
    running = False
    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    # Convert to hours:minutes:seconds
    elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    return elapsed_time_str


def run_script():

    # Iniciar el temporizador al comenzar el procesamiento
    start_timer()

    # Iniciar el procesamiento de imágenes en un hilo separado
    processing_thread = threading.Thread(target=process_images)
    processing_thread.start()

def process_images():
    global current, total_imagenes

    modelPresencia = load_model('ModelosAI/ModelosFinales/modeloAnimalVGG16.h5')
    modelGuanaco = load_model('ModelosAI/ModelosFinales/modeloGuanacoRN50.h5')
    modelMegadetector = YOLOV5Base(weights='ModelosAI/ModelosFinales/modeloMegadetector.pt', device='cpu')

    confianzaAnimalInf = 0.01
    confianzaAnimalSup = 0.96
    confianzaGuanaco = 0.71
    confianzaCantidad = 0.69

    # Verificar si el archivo CSV existe
    archivo_existe = os.path.exists('Piloto2023/ArchivosUtiles/df.feather')

    # Si el archivo existe, cargarlo en un DataFrame
    if archivo_existe:
        df = pd.read_feather('Piloto2023/ArchivosUtiles/df.feather')
    else:
        df = pd.read_csv('Piloto2023/ArchivosUtiles/Muestreo_CT_PatAzul.csv', low_memory=False)
        for column in ['Ruta', 'Animal_proba', 'Animal', 'Guanaco_proba', 'Guanaco', 'Especie', 'Cantidad_proba', 'Cantidad', 'Validar', 'Validado']:
            if column not in df.columns:
                # Añadir la columna a `df` con valores por defecto NaN
                df[column] = np.nan

    dfTensor = pd.read_pickle('Piloto2023/ArchivosUtiles/datasetTensores.pkl')

    # Obtener las rutas de las imágenes
    paths_filtrados = list(set(df['Ruta']) - set(df[df['Animal'].notna()]['Ruta']))

    # Crear una barra de progreso con tqdm
    total_imagenes = len(paths_filtrados)
    update_progress_bar()

    # Número de procesos o subprocesos concurrentes que deseas ejecutar
    num_procesos_concurrentes = os.cpu_count()  # Puedes ajustar este valor

    # Cambio en la lógica de ejecución para almacenar resultados en una lista
    resultados = []
    imagenes_fallidas = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_procesos_concurrentes) as executor:
        futures = [executor.submit(procesar_imagen, path, dfTensor, modelPresencia, modelGuanaco, modelMegadetector, confianzaAnimalInf, confianzaAnimalSup, confianzaGuanaco, confianzaCantidad) for path in paths_filtrados]
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            resultado = future.result()
            if "error" in resultado:
                imagenes_fallidas.append(resultado[0])
            else:
                resultados.append(resultado)
            current += 1
            update_progress_bar()

            # Cada 1000 imágenes, guarda el DataFrame
            if len(resultados) > 10000:

                df_temporal = pd.DataFrame(resultados, columns=['Ruta','Animal_proba','Animal','Guanaco_proba','Guanaco','Especie','Cantidad_proba','Cantidad','Validar','Validado'])
                # Realiza la fusión
                df = df.merge(df_temporal, on='Ruta', how='left', suffixes=('', '_update'))

                # Para cada columna que se actualiza, reemplaza los valores de `df` con los de `df_temporal` si no son NaN
                for column in ['Animal_proba', 'Animal', 'Guanaco_proba', 'Guanaco', 'Especie', 'Cantidad_proba', 'Cantidad', 'Validar', 'Validado']:
                    df[column] = df[f'{column}_update'].combine_first(df[column])

                # Elimina las columnas temporales de actualización
                df.drop(columns=[col for col in df if col.endswith('_update')], inplace=True)
                # df.to_pickle('InterfazUsuario/ArchivosUtiles/df.pkl')
                df.to_feather('Piloto2023/ArchivosUtiles/df.feather')
                resultados = []

    # Reintentar procesar las imágenes que fallaron
    if imagenes_fallidas:
        total_imagenes = len(imagenes_fallidas)
        current = 0
        update_progress_bar()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_procesos_concurrentes) as executor:
            futures = {executor.submit(procesar_imagen, path, dfTensor, modelPresencia, modelGuanaco, modelMegadetector, confianzaAnimalInf, confianzaAnimalSup, confianzaGuanaco, confianzaCantidad): path for path in imagenes_fallidas}  # Tus argumentos aquí
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                resultado = future.result()
                if resultado[1] == "error":
                    resultados.append(resultado)
                else:
                    # sitio, año, camara, extra, archivo = procesar_ruta(resultado[0])
                    resultados.append([resultado[0], None, None, None, None, None, None, None, None, 0])
                current += 1
                update_progress_bar()

    # Al final del procesamiento, guarda cualquier imagen restante
    if resultados:
        df_temporal = pd.DataFrame(resultados, columns=['Ruta','Animal_proba','Animal','Guanaco_proba','Guanaco','Especie','Cantidad_proba','Cantidad','Validar','Validado'])
        # Realiza la fusión
        df = df.merge(df_temporal, on='Ruta', how='left', suffixes=('', '_update'))

        # Para cada columna que se actualiza, reemplaza los valores de `df` con los de `df_temporal` si no son NaN
        for column in ['Animal_proba', 'Animal', 'Guanaco_proba', 'Guanaco', 'Especie', 'Cantidad_proba', 'Cantidad', 'Validar', 'Validado']:
            df[column] = df[f'{column}_update'].combine_first(df[column])

        # Elimina las columnas temporales de actualización
        df.drop(columns=[col for col in df if col.endswith('_update')], inplace=True)

        # df.to_pickle('Piloto2023/ArchivosUtiles/df.pkl')
        df.to_feather('Piloto2023/ArchivosUtiles/dfFinal.feather')
        print(f'Se guardaron los cambios después de procesar {len(df)} imágenes.')


    #  Ordenar por sitio, año, cámara, fecha y hora
    df = df.sort_values(by=['Sitio', 'Año', 'Camara', 'Fecha', 'Hora'])

    hoy  = datetime.now().date()
    filename = "procesado_"+str(hoy)+".csv"

    df.to_csv("Piloto2023/data/"+filename)

    # At the end of your script where you want to stop the timer and show the message
    elapsed_time_str = stop_timer()  # This will stop the timer and return the elapsed time
    # Programar la llamada a show_final_message en el hilo principal
    root.after_idle(show_final_message, filename, elapsed_time_str)

def show_final_message(filename, elapsed_time_str):
    messagebox.showinfo("Finalizado", f"Se generó el archivo: {filename}\nTiempo transcurrido: {elapsed_time_str}")


# Configuración de la ventana principal
root = tk.Tk()
root.title("Piloto 2023")
root.geometry("400x300")  # Ajusta según tus necesidades


# Estilos y fuentes
fuente_principal = Font(family="Verdana", size=12)
fuente_botones = Font(family="Verdana", size=10, weight="bold")
color_boton = "#122C12"
color_texto = "white"

# Configurar el estilo de ttk para forzar el fondo claro
style = ttk.Style(root)
style.theme_use('alt')  # 'clam', 'alt', 'default', 'classic' son algunos temas que puedes probar
style.configure("TButton", font=fuente_botones, background=color_boton, foreground=color_texto)
style.configure("TFrame", background="white")
style.configure("TLabel", background="white", font=fuente_principal)
style.configure("TEntry", font=fuente_principal)
style.configure("Horizontal.TProgressbar", troughcolor='white', background=color_boton, lightcolor=color_boton, darkcolor=color_boton, bordercolor='white', thickness=20)

# Creación de widgets con estilo ttk
mainframe = ttk.Frame(root, padding="3 3 12 12", style='TFrame')
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configurar pesos de columnas para centrar el contenido
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=0)  # La columna del medio no se expandirá
mainframe.columnconfigure(2, weight=1)
mainframe.rowconfigure(0, weight=1)

# Label para mostrar el temporizador
timer_label = ttk.Label(mainframe, text="Tiempo transcurrido: 00:00:00", style='TLabel')

run_button = ttk.Button(mainframe, text="Procesar Imágenes", command=run_script)

# Añadir la barra de progreso
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(mainframe, style="Horizontal.TProgressbar", variable=progress_var, maximum=100)

# Label para mostrar el progreso actual y total
progress_label = ttk.Label(mainframe, text="", style='TLabel')

# Añadir el logo
imagen_logo = Image.open("InterfazUsuario/ArchivosUtiles/logo_rewilding.png").resize((180, 60))
imagen_logo = ImageTk.PhotoImage(imagen_logo)
label_logo = ttk.Label(mainframe, image=imagen_logo)

# Ajusta los widgets para que se expandan y llenen el espacio
# Asegúrate de que los widgets estén en la columna del medio y se expandan hacia los lados
run_button.grid(column=1, row=4, sticky=(tk.EW), padx=10)
progress_bar.grid(column=1, row=5, sticky=(tk.EW), padx=10)
progress_label.grid(column=1, row=6, sticky=(tk.EW), padx=10)
label_logo.grid(column=1, row=7, pady=10, sticky=(tk.EW), padx=10)
timer_label.grid(column=1, row=8, sticky=(tk.EW), padx=10)

# Asegúrate de que cada hijo de mainframe se expanda y llene el espacio
for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=5, sticky=(tk.EW))

root.mainloop()