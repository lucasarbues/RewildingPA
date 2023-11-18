import tkinter as tk
import pandas as pd
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import ttk

class ValidacionImagenes:
    def __init__(self, root):
        self.root = root
        self.root.title("Validación de Imágenes")
        self.root.configure(bg='black')

        # Crear un frame para las imágenes en la parte izquierda (2/3 de la pantalla)
        self.frame_izquierdo = tk.Frame(root,bg="black")
        self.frame_izquierdo.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")

        # Crear un frame para los elementos en la parte derecha (1/3 de la pantalla)
        self.frame_derecho = tk.Frame(root)
        self.frame_derecho.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Configurar el grid para que las columnas y filas sean redimensionables
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)

        self.button_cargar = tk.Button(self.frame_derecho, text="Seleccionar datos", command=self.cargar_csv,bg="black",fg="white")
        self.button_cargar.grid(row=0, column=0)

        self.label_camara = tk.Label(self.frame_derecho, text="", anchor="w",justify="left")
        self.label_camara.grid(row=1, column=0,columnspan=2)

        self.label_fecha = tk.Label(self.frame_derecho, text="", anchor="w",justify="left")
        self.label_fecha.grid(row=2, column=0,columnspan=2)

        self.label_especie = tk.Label(self.frame_derecho, text="Especie:", anchor="w")
        self.label_especie.grid(row=3, column=0)

        self.especies = ['SIN ANIMAL','guanaco', 'zorro gris', 'martineta', 'choique', 'gato montes',
       'passeriforme', 'liebre', 'peludo', 'mara', 'tucuquere', 'gaviota',
       'jote', 'piche', 'chimango', 'ave s/i', 'flamenco', 'aguila mora',
       'zorrino', 'puma', 'pato', 'garza blanca', 'halcon',
       'atahacaminos', 'bandurria', 'chingolo', 'raton', 'loica',
       'calandria', 'zorzal chiguanco', 'oveja', 'yal negro', 'torcaza',
       'zorro colorado', 'carancho', 'aguilucho comun',
       'cormoran imperial', 'cauquen']
        self.selected_especie = tk.StringVar()
        self.selected_especie.set(self.especies[0])
        self.option_menu = tk.OptionMenu(self.frame_derecho, self.selected_especie, *self.especies)
        self.option_menu.grid(row=3, column=1)

        self.label_cantidad = tk.Label(self.frame_derecho, text="Cantidad:", anchor="w")
        self.label_cantidad.grid(row=4, column=0)

        self.validate_cantidad = root.register(self.validate_entry_cantidad)
        self.entry_cantidad = tk.Entry(self.frame_derecho, validate="key", validatecommand=(self.validate_cantidad, '%P'))
        self.entry_cantidad.grid(row=4, column=1)

        self.button_validar = tk.Button(self.frame_derecho, text="Siguiente", command=self.validar,bg="black",fg="white")
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

        self.button_guardar_cerrar = tk.Button(self.frame_derecho, text="Guardar y Cerrar", command=self.guardar_y_cerrar,bg="black",fg="white")
        self.button_guardar_cerrar.grid(row=8, column=0, columnspan=2)

        
        self.espacio_blanco4 = tk.Label(self.frame_derecho)
        self.espacio_blanco4.grid(row=15,column=0,columnspan=2)
        
        self.espacio_blanco5 = tk.Label(self.frame_derecho)
        self.espacio_blanco5.grid(row=16,column=0,columnspan=2)


        imagen_logo = Image.open("../Interfaz de Usuario/ArchivosUtiles/logo_rewilding.png")
        imagen_logo = imagen_logo.resize((180, 60))
        imagen_logo = ImageTk.PhotoImage(imagen_logo)

        self.label_logo = tk.Label(self.frame_derecho, image=imagen_logo)
        self.label_logo.image = imagen_logo
        self.label_logo.grid(row=20,column=0,columnspan=2)

        self.espacio_blanco = tk.Label(self.frame_derecho)
        self.espacio_blanco.grid(row=18,column=0,columnspan=2)

        #imagen_logo2 = Image.open("interfaces_de_usuario/logo-itba-site.png")
        #imagen_logo2 = imagen_logo2.resize((180, 60))
        #imagen_logo2 = ImageTk.PhotoImage(imagen_logo2)

        self.espacio_blanco2 = tk.Label(self.frame_derecho)
        self.espacio_blanco2.grid(row=22,column=0,columnspan=2)

        self.espacio_blanco3 = tk.Label(self.frame_derecho)
        self.espacio_blanco3.grid(row=24,column=0,columnspan=2)

        #self.label_logo2 = tk.Label(self.frame_derecho, image=imagen_logo2)
        #self.label_logo2.image = imagen_logo2
        #self.label_logo2.grid(row=25,column=0,columnspan=2)


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
            while self.index < len(self.df) and (self.df.loc[self.index, "Validado"] != 0 or not self.df.loc[self.index, "Validar"]):
                self.index += 1

            if self.index < len(self.df):
                ruta_imagen = self.df.loc[self.index, "Ruta"]
                imagen = Image.open(ruta_imagen)
                imagen = imagen.resize((1000, 600), Image.ANTIALIAS)
                imagen = ImageTk.PhotoImage(imagen)
                self.label_imagen = tk.Label(self.frame_izquierdo, image=imagen)
                self.label_imagen.image = imagen
                self.label_imagen.grid(row=0, column=0, sticky="nsew")

                self.label_camara.config(text=f"{self.df.loc[self.index, 'Sitio']}")
                self.label_fecha.config(text=f"{self.df.loc[self.index, 'Fecha']}")
                
                # Contar filas donde Validado = 0 y Validar = True
                animales_por_validar = len(self.df[(self.df['Validado'] == 0) & self.df['Validar']])
                self.label_restantes.config(text=f"Imágenes restantes: {animales_por_validar}")
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
            self.df.loc[self.index, "Validado"] = 1
            self.index += 1
            self.mostrar_imagen()
            self.entry_cantidad.delete(0, tk.END)
            self.guardar_csv()
    
    def guardar_y_cerrar(self):
        # Guardar el DataFrame en el archivo CSV antes de cerrar la aplicación
        self.guardar_csv()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ValidacionImagenes(root)
    root.mainloop()
