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

def procesar_imagen(full_path, modelPresencia, modelGuanaco, confianzaAnimalInf, confianzaAnimalSup, confianzaGuanaco, confianzaCantidad):
    # global modelPresencia, modelGuanaco, confianzaAnimalInf, confianzaAnimalSup, confianzaGuanaco, confianzaCantidad
    try:
        # Obtener Fecha y Hora de la imagen
        fecha, hora = get_date_time_from_image(full_path)
        fecha = pd.to_datetime(fecha, format="%Y:%m:%d").date()
        hora = pd.to_datetime(hora, format="%H:%M:%S").time()

        # Obtener Tensor de la imagen
        tensor = load_and_convert_image(full_path)

        # Predecir Presencia de Animal
        animal_proba = modelPresencia.predict(tensor)[0][0]
        animal = (animal_proba > 0.5).astype(int)
        validar = ((animal_proba >= (confianzaAnimalInf)) & (animal_proba <= confianzaAnimalSup))

        # Predecir Presencia de Guanaco si hay un animal
        guanaco_proba = None
        guanaco = None
        especie = None
        if animal == 1 and validar == False:
            guanaco_proba = modelGuanaco.predict(tensor)[0][0]
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

        return full_path, fecha, hora, animal_proba, animal, guanaco_proba, guanaco, especie, cantidad_proba, cantidad, validar

    except Exception as e:
        print(f'Error al procesar la imagen {full_path}: {str(e)}')
        # pbar.write(f'Error al procesar la imagen {ruta}: {str(e)}')
    return full_path, None, None, None, None, None, None, None, None, None, None

def run_script():
    if not ruta:
        messagebox.showerror("Error", "Por favor, selecciona una ruta válida.")
        return

    # Inicializacion
    data = []
    # tensor = []
    modelPresencia = load_model('ModelosAI/ModelosFinales/modeloAnimalVGG16.h5')
    modelGuanaco = load_model('ModelosAI/ModelosFinales/modeloGuanacoVGG16.h5')
    confianzaAnimalInf = 0.01
    confianzaAnimalSup = 0.96
    confianzaGuanaco = 0.71
    confianzaCantidad = 0.69

    for root, dirs, files in os.walk(ruta):
        for file in files:
            if file.endswith('.JPG'):
                full_path = os.path.join(root, file)
                parts = full_path.split(os.sep)

                # Encontrar el índice de inicio para las partes relevantes
                start_index = next((i for i, part in enumerate(parts) if "Muestreo ct" in part), None)

                sitio = parts[start_index]
                año = parts[start_index + 1]
                camara = parts[start_index + 2]
                extra = None

                # Si hay más subdirectorios después de la cámara, los unimos
                if len(parts) > start_index + 4:
                    extra = '/'.join(parts[start_index + 3:-1])

                archivo = parts[-1]

                full_path, fecha, hora, animal_proba, animal, guanaco_proba, guanaco, especie, cantidad_proba, cantidad, validar = procesar_imagen(full_path, modelPresencia, modelGuanaco, confianzaAnimalInf, confianzaAnimalSup, confianzaGuanaco, confianzaCantidad)

                # tensor.append([full_path, tensor]) # Vale la pena guardar el tensor?
                data.append([full_path, sitio, año, camara, extra, archivo, fecha, hora, animal_proba, animal, guanaco_proba, guanaco, especie, cantidad_proba, cantidad, validar, 0])

    df = pd.DataFrame(data, columns=['Ruta', 'Sitio', 'Año', 'Camara', 'Extra', 'Archivo','Fecha','Hora','Animal_proba','Animal','Guanaco_proba','Guanaco','Especie','Cantidad_proba','Cantidad','Validar','Validado'])
    #  Ordenar por sitio, año, cámara, fecha y hora
    df = df.sort_values(by=['Sitio', 'Año', 'Camara', 'Fecha', 'Hora'])



    # df['Fecha'], df['Hora'] = zip(*df['Ruta'].apply(get_date_time_from_image))
    # df['Fecha'] = pd.to_datetime(df['Fecha'], format="%Y:%m:%d")
    # df['Hora'] = pd.to_datetime(df['Hora'], format="%H:%M:%S").dt.strftime("%H:%M:%S")

    # image_tensors = [load_and_convert_image(img_path) for img_path in df['Ruta']]
    # tensor = tf.stack(image_tensors)

    # modelPresencia = load_model('ModelosAI/ModelosFinales/modeloAnimalVGG16.h5')

    # df['Animal_proba'] = modelPresencia.predict(tensor)

    # df['Animal'] = (df['Animal_proba'] > 0.5).astype(int)

    # indices = [i for i, x in enumerate(df['Animal'].values) if x == 1]

    # tensorAnimal = tf.gather(tensor, indices)

    # modelGuanaco = load_model('ModelosAI/ModelosFinales/modeloGuanacoVGG16.h5')

    # df.loc[df['Animal']==1, 'Guanaco_proba'] = modelGuanaco.predict(tensorAnimal)

    # df.loc[df['Animal']==1,'Guanaco'] = (df.loc[df['Animal']==1,'Guanaco_proba'] > 0.5).astype(int)

    # confianzaAnimal = 0.99
    # confianzaGuanaco = 0.90

    # df['Validar'] = ((df['Animal_proba'] >= (1-confianzaAnimal)) & (df['Animal_proba'] <= confianzaAnimal)) | (df['Guanaco_proba'] <= (confianzaGuanaco))
    # df['Validado'] = 0
    # df['Especie'] = pd.NA
    # df['Cantidad']= pd.NA
    # df.loc[df['Validar'] == False, 'Especie'] = 'Guanaco'
    # df.loc[df['Validar'] == False, 'Cantidad'] = 1
    # df.loc[df['Validar'] == False, 'Validado'] = 1

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
