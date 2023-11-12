import tkinter as tk
import pandas as pd
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import ttk

class ValidacionImagenes:
    def __init__(self, root):
        self.root = root
        self.root.title("Validación de Imágenes")

        # Crear un frame para las imágenes en la parte izquierda (2/3 de la pantalla)
        self.frame_izquierdo = tk.Frame(root)
        self.frame_izquierdo.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")

        # Crear un frame para los elementos en la parte derecha (1/3 de la pantalla)
        self.frame_derecho = tk.Frame(root)
        self.frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Configurar el grid para que las columnas y filas sean redimensionables
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)

        self.button_cargar = tk.Button(self.frame_derecho, text="Cargar CSV", command=self.cargar_csv)
        self.button_cargar.grid(row=0, column=0)

        self.label_camara = tk.Label(self.frame_derecho, text="", anchor="w",justify="left")
        self.label_camara.grid(row=1, column=0)

        self.label_fecha = tk.Label(self.frame_derecho, text="", anchor="w",justify="left")
        self.label_fecha.grid(row=2, column=0)

        self.label_especie = tk.Label(self.frame_derecho, text="Especie:", anchor="w",justify="left")
        self.label_especie.grid(row=3, column=0)

        self.especies = ["Guanaco", "Puma", "Mara", "Ave", "Zorro", "No hay animal"]
        self.selected_especie = tk.StringVar()
        self.selected_especie.set(self.especies[0])
        self.option_menu = tk.OptionMenu(self.frame_derecho, self.selected_especie, *self.especies)
        self.option_menu.grid(row=3, column=1)

        self.label_cantidad = tk.Label(self.frame_derecho, text="Cantidad:", anchor="w")
        self.label_cantidad.grid(row=4, column=0)

        self.validate_cantidad = root.register(self.validate_entry_cantidad)
        self.entry_cantidad = tk.Entry(self.frame_derecho, validate="key", validatecommand=(self.validate_cantidad, '%P'))
        self.entry_cantidad.grid(row=4, column=1)

        self.button_validar = tk.Button(self.frame_derecho, text="Siguiente", command=self.validar)
        self.button_validar.grid(row=5, column=0, columnspan=1)

        self.label_restantes = tk.Label(self.frame_derecho, text="Imágenes restantes por validar: 0", anchor="w")
        self.label_restantes.grid(row=6, column=0, columnspan=2)

        self.label_finalizado = tk.Label(self.frame_derecho, text="", fg="green", anchor="w")
        self.label_finalizado.grid(row=7, column=0, columnspan=2)

        self.index = 0
        self.df = None
        self.ruta_csv = None
        self.ordenar_por_camara_fecha_hora = False

        # Agrega un enlace entre la tecla Enter y la función self.validar()
        self.root.bind('<Return>', self.validar)

    def cargar_csv(self):
        self.ruta_csv = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.ruta_csv:
            self.df = pd.read_csv(self.ruta_csv)

            # Ordenar el DataFrame por cámara, fecha y hora
            if 'Camara' in self.df.columns and 'Fecha' in self.df.columns and 'Hora' in self.df.columns:
                self.df.sort_values(by=['Camara', 'Fecha', 'Hora'], inplace=True)
                self.ordenar_por_camara_fecha_hora = True

            self.mostrar_imagen()

    def mostrar_imagen(self):
        if self.df is not None and self.index < len(self.df):
            ruta_imagen = self.df.loc[self.index, "Ruta"]
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((1000, 600), Image.ANTIALIAS)
            imagen = ImageTk.PhotoImage(imagen)
            self.label_imagen = tk.Label(self.frame_izquierdo, image=imagen)
            self.label_imagen.image = imagen
            self.label_imagen.grid(row=0, column=0, sticky="nsew")

            # Cambiar la etiqueta de la cámara por la etiqueta del sitio
            self.label_camara.config(text=f"Sitio: {self.df.loc[self.index, 'Sitio']}")  # Cambia 'Camara' a 'Sitio'
            self.label_fecha.config(text=f"Fecha: {self.df.loc[self.index, 'Fecha']}")
            self.label_restantes.config(text=f"Imágenes restantes por validar: {len(self.df) - self.index}")
        else:
            self.label_finalizado.config(text="Proceso de validación terminado")
            self.guardar_csv()

    def guardar_csv(self):
        if self.ruta_csv is not None:
            self.df.to_csv(self.ruta_csv, index=False)
            print(f"CSV guardado en: {self.ruta_csv}")

    def validate_entry_cantidad(self, new_value):
        if new_value.isdigit():
            cantidad = int(new_value)
            return 0 <= cantidad <= 20
        elif new_value == "":
            return True
        else:
            return False

    def validar(self, event=None):  # Agrega 'event=None' para manejar el evento Enter
        especie = self.selected_especie.get()
        cantidad = self.entry_cantidad.get()
        if self.df is not None and self.index < len(self.df):
            self.df.loc[self.index, "Especie"] = especie
            self.df.loc[self.index, "Cantidad"] = cantidad
            self.index += 1
            self.mostrar_imagen()
            self.entry_cantidad.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ValidacionImagenes(root)
    root.mainloop()
