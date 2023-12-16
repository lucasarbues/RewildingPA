# Usar una imagen base oficial de Python
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requisitos y instalar las dependencias
RUN pip install tensorflow
RUN pip install pytorchwildlife
RUN pip install charset_normalizer
RUN pip install pyarrow


# Copiar los archivos necesarios al contenedor
COPY ModelosFinales/modeloMegadetector.pt ./ModelosFinales/
COPY ModelosFinales/modeloAnimalVGG16.h5 ./ModelosFinales/
COPY ModelosFinales/modeloGuanacoRN50.h5 ./ModelosFinales/
COPY funciones.py .
COPY ArchivosUtiles/logo_rewilding.png ./ArchivosUtiles/

# Asegúrate de que todos los directorios necesarios existan
RUN mkdir -p ./ModelosFinales
RUN mkdir -p ./ArchivosUtiles

# Copiar el resto del código fuente de la aplicación al contenedor
COPY . .

# Comando para ejecutar la aplicación
CMD ["python", "./ui_ejecucion_modelos.py"]