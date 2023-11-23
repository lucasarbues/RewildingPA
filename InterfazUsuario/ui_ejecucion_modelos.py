import os

# Suprimir advertencias de Intel MKL y NNPACK
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['MKL_THREADING_LAYER'] = 'GNU'

import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, messagebox, ttk
from tkinter.font import Font
from tensorflow.keras.models import load_model
import tensorflow as tf
from datetime import datetime
from PIL import Image, ImageTk
import sys
# from tqdm import tqdm
import concurrent
import concurrent.futures
import torch
import torchvision.transforms as transforms
from torchvision.transforms import Resize
import numpy as np


# Agrega la carpeta padre al sys.path
current_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from funciones import load_and_convert_image, get_date_time_from_image, YOLOV5Base

def browse_folder():
    global ruta
    ruta = filedialog.askdirectory()
    ruta_entry.delete(0, tk.END)
    ruta_entry.insert(0, ruta)

def procesar_ruta(full_path):
     # Obtener Sitio, Año, Camara y Archivo de la ruta
    parts = full_path.split(os.sep)

    # Encontrar el índice de inicio para las partes relevantes
    start_index = next((i for i, part in enumerate(parts) if "Muestreo ct" in part), None)

    sitio = parts[start_index]
    año = parts[start_index + 1]
    camara = parts[start_index + 2]
    extra = ''

    # Si hay más subdirectorios después de la cámara, los unimos
    if len(parts) > start_index + 4:
        extra = '/'.join(parts[start_index + 3:-1])

    archivo = parts[-1]
    return sitio, año, camara, extra, archivo

def Megadetector(image_path, model):
    try:
        # Leer y transformar la imagen
        image = Image.open(image_path)
        transform = transforms.Compose([
            Resize((640, 640)),
            transforms.ToTensor()
        ])
        image = transform(image)
        num_detections, average_confidence = model.single_image_detection(img=image, conf_thres=0.4)

        return average_confidence, num_detections

    except Exception as e:
        print(f'Megadetector Falla: {image_path}: {str(e)}')
        return None, None

def procesar_imagen(full_path, modelPresencia, modelGuanaco, modelMegadetector, confianzaAnimalInf, confianzaAnimalSup, confianzaGuanaco, confianzaCantidad):
    try:
        # Obtener la ruta de la imagen
        sitio, año, camara, extra, archivo = procesar_ruta(full_path)

        # Obtener Fecha y Hora de la imagen
        fecha, hora = get_date_time_from_image(full_path)
        fecha = pd.to_datetime(fecha, format="%Y:%m:%d").date()
        hora = pd.to_datetime(hora, format="%H:%M:%S").time()

        # Obtener Tensor de la imagen
        tensor = load_and_convert_image(full_path)

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
            mean_confidence, cant_pred = Megadetector(full_path, modelMegadetector)
            cantidad_proba = (cant_pred == 1) * mean_confidence + (1 - (cant_pred == 1)) * (1 - mean_confidence)
            cantidad = int(cant_pred == 1) if cant_pred is not None else None
            validar = ((animal_proba >= (confianzaAnimalInf)) & (animal_proba <= confianzaAnimalSup) | (guanaco_proba <= (confianzaGuanaco))) | (cantidad_proba <= (confianzaCantidad))

        return full_path, sitio, año, camara, extra, archivo, fecha, hora, animal_proba, animal, guanaco_proba, guanaco, especie, cantidad_proba, cantidad, validar, 0

    except Exception as e:
        print(f'Error al procesar la imagen {full_path}: {str(e)}')
    return full_path, "error", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

def update_progress_bar(current, total):
    """Actualiza la barra de progreso en la interfaz de Tkinter."""
    progress = 100 * (current / total)
    progress_var.set(progress)
    progress_label.config(text=f"{current}/{total} ({progress_var.get():.2f}%)")
    root.update_idletasks()

def run_script():
    if not ruta:
        messagebox.showerror("Error", "Por favor, selecciona una ruta válida.")
        return

    # Inicializacion
    modelPresencia = load_model('ModelosAI/ModelosFinales/modeloAnimalVGG16.h5')
    modelGuanaco = load_model('ModelosAI/ModelosFinales/modeloGuanacoVGG16.h5')
    modelMegadetector = YOLOV5Base(weights='ModelosAI/ModelosFinales/modeloMegadetector.pt', device='cpu')


    confianzaAnimalInf = 0.01
    confianzaAnimalSup = 0.96
    confianzaGuanaco = 0.71
    confianzaCantidad = 0.69

    # Obtener las rutas de las imágenes a procesar
    paths_filtrados = []
    for root, dirs, files in os.walk(ruta):
        for file in files:
            paths_filtrados.append(os.path.join(root, file))

    # Verificar si el archivo CSV existe
    archivo_existe = os.path.exists('InterfazUsuario/ArchivosUtiles/df.pkl')

    # Si el archivo existe, cargarlo en un DataFrame
    if archivo_existe:
        df = pd.read_pickle('InterfazUsuario/ArchivosUtiles/df.pkl')
    else:
        df = pd.DataFrame(columns=['Ruta', 'Sitio', 'Año', 'Camara', 'Extra', 'Archivo','Fecha','Hora','Animal_proba','Animal','Guanaco_proba','Guanaco','Especie','Cantidad_proba','Cantidad','Validar','Validado'])

    # Obtengo las rutas que no se han procesado.
    # paths_filtrados que no esten en df_procesado['Ruta']
    paths_filtrados = list(set(paths_filtrados) - set(df['Ruta']))

    # Crear una barra de progreso con tqdm
    total_imagenes = len(paths_filtrados)

    # Número de procesos o subprocesos concurrentes que deseas ejecutar
    num_procesos_concurrentes = os.cpu_count()  # Puedes ajustar este valor

    # Cambio en la lógica de ejecución para almacenar resultados en una lista
    resultados = []
    imagenes_fallidas = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_procesos_concurrentes) as executor:
        futures = [executor.submit(procesar_imagen, path, modelPresencia, modelGuanaco, modelMegadetector, confianzaAnimalInf, confianzaAnimalSup, confianzaGuanaco, confianzaCantidad) for path in paths_filtrados]
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            resultado = future.result()
            if "error" in resultado:
                imagenes_fallidas.append(resultado[0])
            else:
                resultados.append(resultado)
            update_progress_bar(i+1, total_imagenes)

            # Cada 1000 imágenes, guarda el DataFrame
            if len(resultados) > 1000:
                df_temporal = pd.DataFrame(resultados, columns=['Ruta', 'Sitio', 'Año', 'Camara', 'Extra', 'Archivo','Fecha','Hora','Animal_proba','Animal','Guanaco_proba','Guanaco','Especie','Cantidad_proba','Cantidad','Validar','Validado'])
                df = pd.concat([df, df_temporal], ignore_index=True)
                df.to_pickle('InterfazUsuario/ArchivosUtiles/df.pkl')
                print(f'Se guardaron los cambios después de procesar {len(df)} imágenes.')
                resultados = []

    # Reintentar procesar las imágenes que fallaron
    if imagenes_fallidas:
        update_progress_bar(0, len(imagenes_fallidas))
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_procesos_concurrentes) as executor:
            futures = {executor.submit(procesar_imagen, path, modelPresencia, modelGuanaco, modelMegadetector, confianzaAnimalInf, confianzaAnimalSup, confianzaGuanaco, confianzaCantidad): path for path in imagenes_fallidas}  # Tus argumentos aquí
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                resultado = future.result()
                if resultado[1] == "error":
                    resultados.append(resultado)
                else:
                    sitio, año, camara, extra, archivo = procesar_ruta(resultado[0])
                    resultados.append([resultado[0], sitio, año, camara, extra, archivo, None, None, None, None, None, None, None, None, None, None, 0])
                update_progress_bar(i+1, len(imagenes_fallidas))

    # Al final del procesamiento, guarda cualquier imagen restante
    if resultados:
        df_temporal = pd.DataFrame(resultados, columns=['Ruta', 'Sitio', 'Año', 'Camara', 'Extra', 'Archivo','Fecha','Hora','Animal_proba','Animal','Guanaco_proba','Guanaco','Especie','Cantidad_proba','Cantidad','Validar','Validado'])
        df = pd.concat([df, df_temporal], ignore_index=True)
        df.to_pickle('InterfazUsuario/ArchivosUtiles/df.pkl')
        print(f'Se guardaron los cambios después de procesar {len(df)} imágenes.')


    #  Ordenar por sitio, año, cámara, fecha y hora
    df = df.sort_values(by=['Sitio', 'Año', 'Camara', 'Fecha', 'Hora'])

    hoy  = datetime.now().date()
    default_filename = "procesado_"+str(hoy)+".csv"
    filename = simpledialog.askstring("Guardar CSV", "Ingrese el nombre del archivo CSV:", initialvalue=default_filename)

    df.to_csv("InterfazUsuario/data/"+filename)
    messagebox.showinfo("Finalizado", "Se generó el archivo:"+filename)


# Configuración de la ventana principal
root = tk.Tk()
root.title("Procesamiento de Imágenes")
root.geometry("400x300")  # Ajusta según tus necesidades

# Estilos y fuentes
fuente_principal = Font(family="Verdana", size=12)
fuente_botones = Font(family="Verdana", size=10, weight="bold")
color_boton = "#122C12"
color_texto = "white"

# Configurar el estilo de ttk para forzar el fondo claro
style = ttk.Style(root)
style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic' son algunos temas que puedes probar
style.configure("TButton", font=fuente_botones, background=color_boton, foreground=color_texto)
style.configure("TFrame", background="white")
style.configure("TLabel", background="white", font=fuente_principal)
style.configure("TEntry", font=fuente_principal)
style.configure("Horizontal.TProgressbar", troughcolor='white', background=color_boton, lightcolor=color_boton, darkcolor=color_boton, bordercolor='white', thickness=20)

# Creación de widgets con estilo ttk
mainframe = ttk.Frame(root, padding="3 3 12 12", style='TFrame')
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=2)  # Columna central para botones
mainframe.columnconfigure(2, weight=1)
mainframe.rowconfigure(0, weight=1)

ruta_label = ttk.Label(mainframe, text="Ruta (Carpeta de imágenes):", style='TLabel')
ruta_label.grid(column=1, row=1, sticky=(tk.W, tk.E))
ruta_entry = ttk.Entry(mainframe, width=40, style='TEntry')
ruta_entry.grid(column=1, row=2, sticky=(tk.W, tk.E))

browse_button = ttk.Button(mainframe, text="Seleccionar Carpeta",command=browse_folder)
browse_button.grid(column=1, row=3, sticky=tk.EW)

run_button = ttk.Button(mainframe, text="Procesar Imágenes", command=run_script)
run_button.grid(column=1, row=4, sticky=tk.EW)

# Añadir la barra de progreso
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(mainframe, style="Horizontal.TProgressbar", variable=progress_var, maximum=100)
progress_bar.grid(column=1, row=5, sticky=(tk.W, tk.E))

# Label para mostrar el progreso actual y total
progress_label = ttk.Label(mainframe, text="0/0 (0%)", style='TLabel')
progress_label.grid(column=1, row=6, sticky=(tk.W, tk.E))

# Añadir el logo
imagen_logo = Image.open("InterfazUsuario/ArchivosUtiles/logo_rewilding.png").resize((180, 60))  # Asegúrate de poner la ruta correcta del logo
imagen_logo = ImageTk.PhotoImage(imagen_logo)
label_logo = ttk.Label(mainframe, image=imagen_logo)
label_logo.grid(column=1, row=7, pady=10)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()