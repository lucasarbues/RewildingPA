import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tensorflow as tf
from tensorflow.keras.models import load_model
import shutil

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

    # Verificar si el archivo CSV existe
    archivo_existe = os.path.exists('Muestreo_CT_PatAzul.csv')

    # Si el archivo existe, cargarlo en un DataFrame
    if archivo_existe:
        df_existente = pd.read_csv('Muestreo_CT_PatAzul.csv')

    for root, dirs, files in os.walk(ruta):
        for file in files:
            if file.endswith('.JPG'):
                full_path = os.path.join(root, file)
                parts = full_path.split(os.sep)

                # Obtengo los datos de la imagen
                sitio = parts[0]
                año = parts[1]
                camara = parts[2]
                if len(parts) > 4:
                    extra = '/'.join(parts[3:-1])
                archivo = parts[-1]

                data.append([full_path, sitio, año, camara, extra, archivo])

    # Crear un DataFrame solo si hay datos nuevos para agregar
    if data:
        df = pd.DataFrame(data, columns=['Ruta', 'Sitio', 'Año', 'Camara', 'Extra', 'Archivo'])

        df['Fecha'], df['Hora'] = zip(*df['Ruta'].apply(get_date_time_from_image))
        df['Fecha'] = pd.to_datetime(df['Fecha'], format="%Y:%m:%d")
        df['Hora'] = pd.to_datetime(df['Hora'], format="%H:%M:%S").dt.strftime("%H:%M:%S")

        image_tensors = [load_and_convert_image(img_path) for img_path in df['Ruta']]
        tensor = tf.stack(image_tensors)

        model = load_model('../ModelosAI/ModelosFinales/modeloAnimalVGG16.h5')

        df['Animal_proba'] = model.predict(tensor)

        df['Animal'] = (df['Animal_proba'] > 0.5).astype(int)

        indices = [i for i, x in enumerate(df['Animal'].values) if x == 1]

        tensorAnimal = tf.gather(tensor, indices)

        model = load_model('../ModelosAI/ModelosFinales/modeloGuanacoVGG16.h5')

        df.loc[df['Animal']==1, 'Guanaco_proba'] = model.predict(tensorAnimal)

        df.loc[df['Animal']==1,'Guanaco'] = (df.loc[df['Animal']==1,'Guanaco_proba'] > 0.5).astype(int)

        confianzaAnimalInf = 0.01
        confianzaAnimalSup = 0.96
        confianzaGuanaco = 0.81

        df['Validar'] = ((df['Animal_proba'] >= (confianzaAnimalInf)) & (df['Animal_proba'] <= confianzaAnimalSup)) | (df['Guanaco_proba'] <= (confianzaGuanaco))

        # Si el archivo CSV existe, combinar df con df_existente
        if archivo_existe:
            df = pd.concat([df_existente, df], ignore_index=True)

        # Guardar el DataFrame combinado
        df.to_csv('Muestreo_CT_PatAzul.csv', index=False)
    
    # df_a_validar = df[df['Validar']==True]
    # df_animales = df[(df['Animal']==1) & (df['Validar']==False)]
    df_no_animales = df[(df['Animal']==0) & (df['Validar']==False)]

    # df_a_validar.to_csv("validar.csv")
    # df_animales.to_csv("animales.csv")

    for index, row in df_no_animales.iterrows():
        img_path = row['Ruta']
        img_name = row['Archivo']
        no_animales_dir = os.path.join(os.path.dirname(img_path), "noAnimales")

        os.makedirs(no_animales_dir, exist_ok=True)

        new_path = os.path.join(no_animales_dir, img_name)

        try:
            shutil.move(img_path, new_path)
        except Exception as e:
            print(f"Error al mover {img_name}: {str(e)}")

    messagebox.showinfo("Terminado", "El script se ha ejecutado exitosamente.")

# Crear la ventana principal
root = tk.Tk()
root.title("Ejecutar Script")

ruta_label = tk.Label(root, text="Ruta de las imágenes:")
ruta_label.pack()

ruta_entry = tk.Entry(root, width=40)
ruta_entry.pack()

browse_button = tk.Button(root, text="Seleccionar Ruta", command=browse_folder)
browse_button.pack()

run_button = tk.Button(root, text="Ejecutar Script", command=run_script)
run_button.pack()

root.mainloop()
