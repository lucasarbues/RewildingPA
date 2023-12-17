import tkinter as tk
import pandas as pd
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter.font import Font

class ValidacionImagenes:
    def __init__(self, root):
        self.root = root
        self.root.title("Validación de Imágenes")
        self.root.configure(bg='white')

        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

        # Estilos y Fuentes
        fuente_principal = Font(family="Verdana", size=12)
        fuente_botones = Font(family="Verdana", size=10, weight="bold")
        color_boton = "#122C12"
        color_texto = "white"

        style = ttk.Style()
        style.theme_use('alt')
        style.configure("TButton", font=fuente_botones, background=color_boton, foreground=color_texto)
        style.configure("White.TFrame", background="white")
        style.configure("Green.TFrame", background="#122C12")
        style.configure("TLabel", background="white", font=fuente_principal)
        style.configure("TEntry", font=fuente_principal)
        style.configure("Horizontal.TProgressbar", troughcolor='white', background=color_boton, lightcolor=color_boton, darkcolor=color_boton, bordercolor='white', thickness=10)

        # Configuración de la ventana y los frames
        self.frame_izquierdo = ttk.Frame(root, style='Green.TFrame')
        self.frame_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_derecho = ttk.Frame(root, style='White.TFrame')
        self.frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        # Asegurar que el frame derecho use el espacio verticalmente
        for i in range(20):
            self.frame_derecho.grid_rowconfigure(i, weight=1)

        # Configuración de Grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=12)
        self.root.grid_columnconfigure(1, weight=1)

        # Botones y Etiquetas
        self.button_cargar = ttk.Button(self.frame_derecho, text="Seleccionar datos", style='TButton', command=self.cargar_csv)
        self.button_cargar.grid(row=1, column=0, sticky="ew")

        self.label_camara = ttk.Label(self.frame_derecho, text="", anchor="w", style='TLabel', justify="left")
        self.label_camara.grid(row=2, column=0, sticky="ew")

        self.label_fecha = ttk.Label(self.frame_derecho, text="", anchor="w",justify="left")
        self.label_fecha.grid(row=3, column=0, sticky="ew")

        self.label_especie = ttk.Label(self.frame_derecho, text="Especie:", anchor="w")
        self.label_especie.grid(row=4, column=0, sticky="ew")

        self.especies = ['SIN ANIMAL', 'Guanaco', 'Zorro gris', 'Martineta', 'Choique', 'Gato montes',
                         'Passeriforme', 'Liebre', 'Peludo', 'Mara', 'Tucuquere', 'Gaviota',
                         'Jote', 'Piche', 'Chimango', 'Ave s/i', 'Flamenco', 'Aguila mora',
                         'Zorrino', 'Puma', 'Pato', 'Garza blanca', 'Halcon',
                         'Atahacaminos', 'Bandurria', 'Chingolo', 'Raton', 'Loica',
                         'Calandria', 'Zorzal chiguanco', 'Oveja', 'Yal negro', 'Torcaza',
                         'Zorro colorado', 'Carancho', 'Aguilucho comun',
                         'Cormoran imperial', 'Cauquen']
        
        self.especies_var = tk.StringVar()
        
        # Crear el combobox y configurarlo
        self.combobox_especies = ttk.Combobox(self.frame_derecho, textvariable=self.especies_var, values=self.especies)
        self.combobox_especies.grid(row=5, column=0, sticky="ew")
        self.combobox_especies.bind('<KeyRelease>', self.filtrar_especies)

        self.label_cantidad = ttk.Label(self.frame_derecho, text="Cantidad:", anchor="w")
        self.label_cantidad.grid(row=7, column=0, sticky="ew")

        self.validate_cantidad = root.register(self.validate_entry_cantidad)
        self.entry_cantidad = ttk.Entry(self.frame_derecho, validate="key", validatecommand=(self.validate_cantidad, '%P'))
        self.entry_cantidad.grid(row=8, column=0, sticky="ew")

        self.button_validar = ttk.Button(self.frame_derecho, text="Siguiente", command=self.validar, style='TButton')  
        self.button_validar.grid(row=9, column=0, sticky="ew")

        self.label_restantes = ttk.Label(self.frame_derecho, text="Imágenes restantes por validar: 0", anchor="w")
        self.label_restantes.grid(row=10, column=0, sticky="ew")

        self.label_finalizado = ttk.Label(self.frame_derecho, text="", style="Green.TLabel", anchor="w")
        self.label_finalizado.grid(row=11, column=0, sticky="ew")


        self.index = 0
        self.df = None
        self.ruta_csv = None
        self.ordenar_por_camara_fecha_hora = False

        # Agrega un enlace entre la tecla Enter y la función self.validar()
        self.root.bind('<Return>', self.validar)

        self.button_guardar_cerrar = ttk.Button(self.frame_derecho, text="Guardar y Cerrar", command=self.guardar_y_cerrar, style='TButton')
        self.button_guardar_cerrar.grid(row=12, column=0, sticky="ew")


        self.espacio_blanco4 = ttk.Label(self.frame_derecho)
        self.espacio_blanco4.grid(row=15,column=0, sticky="ew")

        self.espacio_blanco5 = ttk.Label(self.frame_derecho)
        self.espacio_blanco5.grid(row=16,column=0, sticky="ew")


        imagen_logo = Image.open("InterfazUsuario/ArchivosUtiles/logo_rewilding.png")
        imagen_logo = imagen_logo.resize((180, 60))
        imagen_logo = ImageTk.PhotoImage(imagen_logo)

        self.label_logo = ttk.Label(self.frame_derecho, image=imagen_logo)
        self.label_logo.image = imagen_logo
        self.label_logo.grid(row=17,column=0, sticky="ew")

        self.espacio_blanco = ttk.Label(self.frame_derecho)
        self.espacio_blanco.grid(row=18,column=0, sticky="ew")


        self.espacio_blanco2 = ttk.Label(self.frame_derecho)
        self.espacio_blanco2.grid(row=22,column=0, sticky="ew")

        self.espacio_blanco3 = ttk.Label(self.frame_derecho)
        self.espacio_blanco3.grid(row=24,column=0, sticky="ew")


    def cargar_csv(self):
        self.ruta_csv = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.ruta_csv:
            self.df = pd.read_csv(self.ruta_csv)
            # Ordenar el DataFrame por cámara, fecha y hora
            if 'Camara' in self.df.columns and 'Fecha' in self.df.columns and 'Hora' in self.df.columns:
                self.df.sort_values(by=['Camara', 'Fecha', 'Hora'], inplace=True)
                self.ordenar_por_camara_fecha_hora = True
            #aca
            if 'Burst' not in self.df.columns:
                self.df['Fecha_Hora'] = pd.to_datetime(self.df['Fecha'] + ' ' + self.df['Hora'])
                self.df = self.df.sort_values(by=['Camara', 'Fecha_Hora'])
                self.df['Dif_Tiempo'] = self.df.groupby('Camara')['Fecha_Hora'].diff()
                self.df['Burst'] = ((self.df['Dif_Tiempo'] > pd.Timedelta(minutes=5)) | self.df['Dif_Tiempo'].isnull()).cumsum()

                # Elimina la columna auxiliar 'Dif_Tiempo'
                self.df = self.df.drop(columns=['Dif_Tiempo'])

            self.mostrar_imagen()

    def filtrar_especies(self, event):
        # Obtén el texto actual del combobox
        texto = self.combobox_especies.get()
        
        # Evita actualizar si la tecla presionada es una tecla especial como las flechas
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Return', 'Tab'):
            return
        
        # Filtra las especies que coinciden con el texto introducido
        if texto == '':
            # Si no hay texto, muestra todas las especies
            self.combobox_especies['values'] = self.especies
        else:
            # De lo contrario, filtra las especies que contengan el texto introducido
            especies_filtradas = [especie for especie in self.especies if texto.lower() in especie.lower()]
            self.combobox_especies['values'] = especies_filtradas
        
        # Coloca el texto del usuario de nuevo porque el filtrado lo elimina
        self.combobox_especies.set(texto)
        # Mueve el cursor al final del texto
        self.combobox_especies.icursor(len(texto))


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

    def guardar_y_cerrar(self):
        # Guardar el DataFrame en el archivo CSV antes de cerrar la aplicación
        self.guardar_csv()
        self.root.destroy()


    def mostrar_imagen(self):
        if self.df is not None and not self.df.empty:
            # Limpiar imágenes y checkboxes anteriores
            for widget in self.frame_izquierdo.winfo_children():
                widget.destroy()

            checkboxes = []

            # Obtener las imágenes por validar
            #images_to_validate = self.df[(self.df['Validado'] == 0) & self.df['Validar']].index.tolist()
            images_to_validate = self.df[(self.df['Validado'] == 0) & self.df['Validar']]
            min_burst = images_to_validate['Burst'].min()
            images_to_validate = images_to_validate[images_to_validate['Burst']==min_burst]
            images_to_validate = images_to_validate.index.tolist()
            #aca
            ##images_to_validate tiene que ser la lista de índices

            # Mostrar hasta 12 imágenes por validar en cada iteración
            for i in range(min(12, len(images_to_validate))):
                index = images_to_validate[i]
                ruta_imagen = self.df.loc[index, "Ruta"]
                imagen = Image.open(ruta_imagen)
                imagen = imagen.resize((230, 210))  # Ajusta el tamaño según tus preferencias
                imagen = ImageTk.PhotoImage(imagen)

                # Crear un Frame para contener la imagen y el checkbox
                frame_imagen = tk.Frame(self.frame_izquierdo, bg='black')
                frame_imagen.grid(row=i // 4, column=(i % 4) * 2, sticky="nsew")

                # Agregar la imagen al Frame
                label_imagen = tk.Label(frame_imagen, image=imagen)
                label_imagen.image = imagen
                label_imagen.grid(row=0, column=0, sticky="nsew")

                # Agregar el Checkbutton al Frame
                checkbox_var = tk.BooleanVar()  # Variable para rastrear el estado del checkbox
                checkbox = tk.Checkbutton(frame_imagen, text=f"", variable=checkbox_var, bg='black') # Imagen {index+1}
                checkbox.grid(row=0, column=1, sticky="nw")
                checkboxes.append((index, checkbox_var))

            # Configurar el redimensionamiento de las filas y columnas en el frame_izquierdo
            for i in range(3):
                self.frame_izquierdo.grid_rowconfigure(i, weight=1)
                self.frame_izquierdo.grid_columnconfigure(i * 2, weight=1)

            # Actualizar información asociada
            if checkboxes:
                # Avanzar al siguiente índice después de la última imagen mostrada
                self.index = checkboxes[-1][0] + 1 if self.index in images_to_validate else images_to_validate[0]

            self.label_camara.config(text=f"{self.df.loc[self.index, 'Sitio']}")
            self.label_fecha.config(text=f"{self.df.loc[self.index, 'Fecha']}")

            animales_por_validar = len(self.df[(self.df['Validado'] == 0) & self.df['Validar']])
            self.label_restantes.config(text=f"Imágenes restantes: {animales_por_validar}")

            self.checkboxes = checkboxes  # Almacenar la lista de variables de checkbox

    def validar(self, event=None):  
        especie = self.especies_var.get()
        cantidad = self.entry_cantidad.get()

        if self.df is not None and hasattr(self, 'checkboxes'):
            for index, checkbox_var in self.checkboxes:
                if checkbox_var.get():  # Verificar si el checkbox está marcado
                    # Copiar la información de la imagen a df_validado
                    #self.df_validado = self.df_validado.append(self.df.loc[index])

                    # Actualizar la información en df
                    self.df.loc[index, "Especie"] = especie
                    self.df.loc[index, "Cantidad"] = cantidad
                    self.df.loc[index, "Validado"] = 1

            # Actualizar el conjunto de imágenes por validar después de la validación
            #self.df = self.df[(self.df['Validado'] == 0) & self.df['Validar']]

            # Mostrar las siguientes imágenes por validar
            self.mostrar_imagen()

            self.entry_cantidad.delete(0, tk.END)
            self.guardar_csv()

            # Guardar el DataFrame validado en un archivo CSV
            #self.guardar_csv_validado()


if __name__ == "__main__":
    root = tk.Tk()
    app = ValidacionImagenes(root)
    root.mainloop()