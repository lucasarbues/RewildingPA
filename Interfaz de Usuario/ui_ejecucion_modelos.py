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

def run_script():
    if not ruta:
        messagebox.showerror("Error", "Por favor, selecciona una ruta válida.")
        return

    data = []

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


                data.append([full_path, sitio, año, camara, extra, archivo])

    df = pd.DataFrame(data, columns=['Ruta', 'Sitio', 'Año', 'Camara', 'Extra', 'Archivo'])

    df['Fecha'], df['Hora'] = zip(*df['Ruta'].apply(get_date_time_from_image))
    df['Fecha'] = pd.to_datetime(df['Fecha'], format="%Y:%m:%d")
    df['Hora'] = pd.to_datetime(df['Hora'], format="%H:%M:%S").dt.strftime("%H:%M:%S")

    image_tensors = [load_and_convert_image(img_path) for img_path in df['Ruta']]
    tensor = tf.stack(image_tensors)

    model = load_model('ModelosAI/ModelosFinales/modeloAnimalVGG16.h5')

    df['Animal_proba'] = model.predict(tensor)

    df['Animal'] = (df['Animal_proba'] > 0.5).astype(int)

    indices = [i for i, x in enumerate(df['Animal'].values) if x == 1]

    tensorAnimal = tf.gather(tensor, indices)

    model = load_model('ModelosAI/ModelosFinales/modeloGuanacoVGG16.h5')

    df.loc[df['Animal']==1, 'Guanaco_proba'] = model.predict(tensorAnimal)

    df.loc[df['Animal']==1,'Guanaco'] = (df.loc[df['Animal']==1,'Guanaco_proba'] > 0.5).astype(int)

    confianzaAnimal = 0.99
    confianzaGuanaco = 0.90

    df['Validar'] = ((df['Animal_proba'] >= (1-confianzaAnimal)) & (df['Animal_proba'] <= confianzaAnimal)) | (df['Guanaco_proba'] <= (confianzaGuanaco))
    df['Validado'] = 0
    df['Especie'] = pd.NA
    df['Cantidad']= pd.NA
    df.loc[df['Validar'] == False, 'Especie'] = 'Guanaco'
    df.loc[df['Validar'] == False, 'Cantidad'] = 1
    df.loc[df['Validar'] == False, 'Validado'] = 1

    hoy  = datetime.now().date()
    default_filename = "procesado_"+str(hoy)+".csv"
    filename = simpledialog.askstring("Guardar CSV", "Ingrese el nombre del archivo CSV:", initialvalue=default_filename)

    df.to_csv("Interfaz de Usuario/data/"+filename)
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
imagen_logo = Image.open("Interfaz de Usuario/ArchivosUtiles/logo_rewilding.png")
imagen_logo = imagen_logo.resize((180, 60))
imagen_logo = ImageTk.PhotoImage(imagen_logo)

label_logo = tk.Label(root, image=imagen_logo)
label_logo.image = imagen_logo
label_logo.pack()

root.mainloop()
