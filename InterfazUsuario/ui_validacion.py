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

        # Configurar temporizador para filtrado
        self.temporizador_filtrado = None
        self.tiempo_espera_filtrado = 300  

        self.combobox_especies.bind('<Key>', self.iniciar_temporizador_filtrado)
        self.combobox_especies.bind('<<ComboboxSelected>>', self.on_especie_selected)
        

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

        self.button_guardar_cerrar = ttk.Button(self.frame_derecho, text="Guardar y Cerrar", command=self.guardar_y_cerrar, style='TButton')
        self.button_guardar_cerrar.grid(row=12, column=0, sticky="ew")

        imagen_logo = Image.open("InterfazUsuario/ArchivosUtiles/logo_rewilding.png")
        imagen_logo = imagen_logo.resize((180, 60))
        imagen_logo = ImageTk.PhotoImage(imagen_logo)

        self.label_logo = ttk.Label(self.frame_derecho, image=imagen_logo)
        self.label_logo.image = imagen_logo
        self.label_logo.grid(row=17,column=0, sticky="ew")


    def cargar_csv(self):
        self.ruta_csv = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.ruta_csv:
            self.df = pd.read_csv(self.ruta_csv)
            # Ordenar el DataFrame por cámara, fecha y hora
            if 'Camara' in self.df.columns and 'Fecha' in self.df.columns and 'Hora' in self.df.columns:
                # Asumimos que el formato de la fecha es día/mes/año y hora es en formato 24 horas.
                self.df['Fecha_Hora'] = pd.to_datetime(self.df['Fecha'] + ' ' + self.df['Hora'], dayfirst=True, format='%d/%m/%Y %H:%M:%S')
                self.df.sort_values(by=['Camara', 'Fecha_Hora'], inplace=True)
                self.ordenar_por_camara_fecha_hora = True

            if 'Burst' not in self.df.columns:
                self.df['Fecha_Hora'] = pd.to_datetime(self.df['Fecha'] + ' ' + self.df['Hora'])
                self.df = self.df.sort_values(by=['Camara', 'Fecha_Hora'])
                self.df['Dif_Tiempo'] = self.df.groupby('Camara')['Fecha_Hora'].diff()
                self.df['Burst'] = ((self.df['Dif_Tiempo'] > pd.Timedelta(minutes=5)) | self.df['Dif_Tiempo'].isnull()).cumsum()

                # Elimina la columna auxiliar 'Dif_Tiempo'
                self.df = self.df.drop(columns=['Dif_Tiempo'])

            self.combobox_especies.focus_set()
            self.mostrar_imagen()

    def iniciar_temporizador_filtrado(self, event):
        # Reiniciar el temporizador si ya está en funcionamiento
        if self.temporizador_filtrado:
            self.root.after_cancel(self.temporizador_filtrado)
        
        # Iniciar el temporizador para ejecutar la función de filtrado después de un tiempo de espera
        self.temporizador_filtrado = self.root.after(self.tiempo_espera_filtrado, self.filtrar_especies)


    def filtrar_especies(self, event = None):
        # Obtén el texto actual del combobox
        texto = self.combobox_especies.get()

        # Filtra las especies que coinciden con el texto introducido
        if texto:
            # De lo contrario, filtra las especies que contengan el texto introducido
            especies_filtradas = [especie for especie in self.especies if texto.lower() in especie.lower()]
            self.combobox_especies['values'] = especies_filtradas
            if not self.combobox_especies['values']:
                # Si no hay coincidencias, no muestra la lista desplegable
                self.combobox_especies.event_generate('<<ComboboxClosed>>')
            elif not self.combobox_especies['values'] == especies_filtradas:
                # Si las coincidencias han cambiado, actualiza la lista y muestra la primera coincidencia
                self.combobox_especies.set(texto)
                self.combobox_especies.event_generate('<Down>')
        else:
            # Si no hay texto, muestra todas las especies
            self.combobox_especies['values'] = self.especies

        # Coloca el texto del usuario de nuevo porque el filtrado lo elimina
        self.combobox_especies.set(texto)
        # Mueve el cursor al final del texto
        self.combobox_especies.icursor(len(texto))

    def on_especie_selected(self, event=None):
        # Mueve el enfoque al campo de entrada de cantidad
        self.entry_cantidad.focus_set()

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
            # Clear previous images and checkboxes
            for widget in self.frame_izquierdo.winfo_children():
                widget.destroy()

            # Reset grid configuration
            self.frame_izquierdo.grid_propagate(False)
            for i in range(20):
                self.frame_izquierdo.grid_rowconfigure(i, weight=0)
                self.frame_izquierdo.grid_columnconfigure(i, weight=0)

            # Update the frame to reflect the changes
            self.frame_izquierdo.update_idletasks()

            checkboxes = []

            # Get the images to validate
            images_to_validate = self.df[(self.df['Validado'] == 0) & self.df['Validar']]
            min_burst = images_to_validate['Burst'].min()
            images_to_validate = images_to_validate[images_to_validate['Burst'] == min_burst].index.tolist()
            cantImagenes = min(12, len(images_to_validate))

            # Determine the number of columns based on the number of images
            num_columns = max(1, min((cantImagenes + 2) // 3, 4))
            num_rows = max(1, (cantImagenes + num_columns - 1) // num_columns)

            # Calculate the available size for each image
            self.frame_izquierdo.update_idletasks()
            frame_width = self.frame_izquierdo.winfo_width()
            frame_height = self.frame_izquierdo.winfo_height()

            img_width = frame_width // num_columns
            img_height = frame_height // num_rows

            # Display the images for validation
            for i in range(cantImagenes):
                index = images_to_validate[i]
                ruta_imagen = self.df.loc[index, "Ruta"]
                imagen = Image.open(ruta_imagen)

                # Preserve aspect ratio
                aspect_ratio = imagen.width / imagen.height
                if imagen.width / img_width > imagen.height / img_height:
                    new_width = img_width
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = img_height
                    new_width = int(new_height * aspect_ratio)

                imagen = imagen.resize((new_width, new_height), Image.LANCZOS)
                imagen_tk = ImageTk.PhotoImage(imagen)

                # Create a Frame to contain the image and checkbox with a green background
                frame_imagen = tk.Frame(self.frame_izquierdo, bg='#122C12')
                frame_imagen.grid(row=i // num_columns, column=i % num_columns, sticky="nsew")
                frame_imagen.grid_propagate(False)

                # Agregar la imagen al Frame
                label_imagen = tk.Label(frame_imagen, image=imagen_tk, bg='#122C12')
                label_imagen.image = imagen_tk  # Mantener una referencia
                label_imagen.pack(fill='both', expand=True)

                # Agregar el Checkbox debajo de la imagen
                checkbox_var = tk.BooleanVar(value=True)  # Variable para rastrear el estado del checkbox
                checkbox = tk.Checkbutton(frame_imagen, variable=checkbox_var, bg='#122C12')
                checkbox.place(relx=0.9, rely=0, anchor='ne')

                checkboxes.append((index, checkbox_var))

            # Configure the resizing of the image frames
            for i in range(num_rows):
                self.frame_izquierdo.grid_rowconfigure(i, weight=1)
            for i in range(num_columns):
                self.frame_izquierdo.grid_columnconfigure(i, weight=1)

            # Update associated information
            if checkboxes:
                self.index = checkboxes[-1][0] + 1 if self.index in images_to_validate else images_to_validate[0]

            self.label_camara.config(text=f"{self.df.loc[self.index, 'Sitio']}")
            self.label_fecha.config(text=f"{self.df.loc[self.index, 'Fecha']}")

            remaining_images = len(self.df[(self.df['Validado'] == 0) & self.df['Validar']])
            self.label_restantes.config(text=f"Remaining images to validate: {remaining_images}")

            self.checkboxes = checkboxes


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