import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog,simpledialog,messagebox
from tkinter import messagebox
from tensorflow.keras.models import load_model
import tensorflow as tf
from datetime import datetime
from PIL import Image, ImageTk
import sys
from tqdm import tqdm
import concurrent
import concurrent.futures

# Agrega la carpeta padre al sys.path
current_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from funciones import load_and_convert_image, get_date_time_from_image

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

def procesar_imagen(full_path, modelPresencia, modelGuanaco, confianzaAnimalInf, confianzaAnimalSup, confianzaGuanaco, confianzaCantidad):
    global pbar
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
        animal = (animal_proba > 0.5).astype(int)
        validar = ((animal_proba >= (confianzaAnimalInf)) & (animal_proba <= confianzaAnimalSup))

        # Predecir Presencia de Guanaco si hay un animal
        guanaco_proba = None
        guanaco = None
        especie = None
        if animal == 1 and validar == False:
            guanaco_proba = modelGuanaco.predict(tensor, verbose=0)[0][0]
            guanaco = (guanaco_proba > 0.5).astype(int)
            validar = ((animal_proba >= (confianzaAnimalInf)) & (animal_proba <= confianzaAnimalSup) | (guanaco_proba <= (confianzaGuanaco)))

        # Predecir Cantidad de Guanacos si hay un guanaco
        cantidad = None
        cantidad_proba = None
        if guanaco == 1 and validar == False:
            especie = 'Guanaco'
            #  AGREGAR MEGADETECTOR
                # Para esa imagen --> group de detecciones "cant_pred" y "mean_confidence"
                # cantidad_proba = (cant_pred == 1) * mean_confidence + (1 - (cant_pred' == 1)) * (1 - mean_confidence)
                # cantidad = (cant_pred == 1).astype(int)
            cantidad_proba = None
            cantidad = None
            # validar = ((animal_proba >= (confianzaAnimalInf)) & (animal_proba <= confianzaAnimalSup) | (guanaco_proba <= (confianzaGuanaco))) | (cantidad_proba <= (confianzaCantidad))

        return full_path, sitio, año, camara, extra, archivo, fecha, hora, animal_proba, animal, guanaco_proba, guanaco, especie, cantidad_proba, cantidad, validar, 0

    except Exception as e:
        # print(f'Error al procesar la imagen {full_path}: {str(e)}')
        pbar.write(f'Error al procesar la imagen {ruta}: {str(e)}')
    return full_path, "error", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

def run_script():
    if not ruta:
        messagebox.showerror("Error", "Por favor, selecciona una ruta válida.")
        return

    # Inicializacion
    modelPresencia = load_model('ModelosAI/ModelosFinales/modeloAnimalVGG16.h5')
    modelGuanaco = load_model('ModelosAI/ModelosFinales/modeloGuanacoVGG16.h5')
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
    pbar = tqdm(total=total_imagenes, desc='Procesando imágenes', unit='img')

    # Número de procesos o subprocesos concurrentes que deseas ejecutar
    num_procesos_concurrentes = os.cpu_count()  # Puedes ajustar este valor

    # Cambio en la lógica de ejecución para almacenar resultados en una lista
    resultados = []
    imagenes_fallidas = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_procesos_concurrentes) as executor:
        futures = [executor.submit(procesar_imagen, path, modelPresencia, modelGuanaco, confianzaAnimalInf, confianzaAnimalSup, confianzaGuanaco, confianzaCantidad) for path in paths_filtrados]
        for future in concurrent.futures.as_completed(futures):
            resultado = future.result()
            if "error" in resultado:
                imagenes_fallidas.append(resultado[0])
            else:
                resultados.append(resultado)
                pbar.update(1)

            # Cada 1000 imágenes, guarda el DataFrame
            if len(resultados) > 1000:
                df_temporal = pd.DataFrame(resultados, columns=['Ruta', 'Sitio', 'Año', 'Camara', 'Extra', 'Archivo','Fecha','Hora','Animal_proba','Animal','Guanaco_proba','Guanaco','Especie','Cantidad_proba','Cantidad','Validar','Validado'])
                df = pd.concat([df, df_temporal], ignore_index=True)
                df.to_pickle('InterfazUsuario/ArchivosUtiles/df.pkl')
                pbar.write(f'Se guardaron los cambios después de procesar {len(df)} imágenes.')
                resultados = []

    # Reintentar procesar las imágenes que fallaron
    if imagenes_fallidas:
        pbar.reset(total=len(imagenes_fallidas))
        pbar.set_description("Reintentando imágenes fallidas")
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_procesos_concurrentes) as executor:
            futures = {executor.submit(procesar_imagen, path, ...): path for path in imagenes_fallidas}  # Tus argumentos aquí
            for future in concurrent.futures.as_completed(futures):
                resultado = future.result()
                if resultado[1] == "error":
                    resultados.append(resultado)
                else:
                    sitio, año, camara, extra, archivo = procesar_ruta(resultado[0])
                    resultados.append([resultado[0], sitio, año, camara, extra, archivo, None, None, None, None, None, None, None, None, None, None, 0])
                pbar.update(1)

    # Al final del procesamiento, guarda cualquier imagen restante
    if resultados:
        df_temporal = pd.DataFrame(resultados, columns=['Ruta', 'Sitio', 'Año', 'Camara', 'Extra', 'Archivo','Fecha','Hora','Animal_proba','Animal','Guanaco_proba','Guanaco','Especie','Cantidad_proba','Cantidad','Validar','Validado'])
        df = pd.concat([df, df_temporal], ignore_index=True)
        df.to_pickle('InterfazUsuario/ArchivosUtiles/df.pkl')
        pbar.write(f'Se guardaron los cambios después de procesar {len(df)} imágenes.')

    # Cerrar la barra de progreso
    pbar.close()

    #  Ordenar por sitio, año, cámara, fecha y hora
    df = df.sort_values(by=['Sitio', 'Año', 'Camara', 'Fecha', 'Hora'])

    hoy  = datetime.now().date()
    default_filename = "procesado_"+str(hoy)+".csv"
    filename = simpledialog.askstring("Guardar CSV", "Ingrese el nombre del archivo CSV:", initialvalue=default_filename)

    df.to_csv("InterfazUsuario/data/"+filename)
    messagebox.showinfo("Finalizado", "Se generó el archivo:"+filename)

# Crear la ventana principal
root = tk.Tk()
root.title("Procesamiento Imágenes")

ruta_label = tk.Label(root, text="Ruta (Carpeta de imágenes):")
ruta_label.pack()

ruta_entry = tk.Entry(root, width=40)
ruta_entry.pack()

browse_button = tk.Button(root, text="Seleccionar Carpeta", command=browse_folder,bg="black",fg="white")
browse_button.pack()

run_button = tk.Button(root, text="Procesar Imágenes", command=run_script,bg="black",fg="white")
run_button.pack()
imagen_logo = Image.open("InterfazUsuario/ArchivosUtiles/logo_rewilding.png")
imagen_logo = imagen_logo.resize((180, 60))
imagen_logo = ImageTk.PhotoImage(imagen_logo)

label_logo = tk.Label(root, image=imagen_logo)
label_logo.image = imagen_logo
label_logo.pack()

root.mainloop()
