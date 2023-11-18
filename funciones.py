import re
import boto3
import cv2
import numpy as np
import io
import os
import tensorflow as tf
from PIL import Image
from PIL.ExifTags import TAGS
import pickle


# Leer objetos_s3
with open('ArchivosUtiles/objetos_s3.pkl', 'rb') as archivo:
    objetos_s3 = pickle.load(archivo)

# Importo Informacion del AccessKey.
accessKey = os.getenv("AccessKey")
secretKey = os.getenv("SecretKey")
# Configura tus credenciales de AWS si aún no lo has hecho
boto3.setup_default_session(aws_access_key_id=accessKey,
                           aws_secret_access_key=secretKey,
                           region_name='us-east-2')
# Nombre del bucket
nombre_bucket_s3 = 's3-pfa'
# Crea un cliente de S3
s3 = boto3.client('s3')

def definirRuta(fila):
    ruta = 'Muestreo ct '
    if fila['Sitio'] == "Sauce":
        if fila['Año'] == 2021:
            if (fila['Camara'] == 'S3') & (fila['Nombre'].find("S4") != -1):  
                ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/Estepa/' + fila['Nombre']
            elif fila['Camara'] == 'S4':
                ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/Tajamar/' + fila['Nombre']
            else:
                ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/' + fila['Nombre']
        elif fila['Año'] == 2022:
            if fila['Camara'] == 'S1': # SAUCE 2022 .1 (7).JPG
                ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/'
                if fila['Nombre'][0] == 'S':
                    resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                    segmentos = fila['Nombre'].split('.')
                    ruta +=  segmentos[1][0] + '/'+ segmentos[1][0] + '-S1- (' + resultado.group(1) + ').JPG'
                elif fila['Nombre'][0] == '3':
                    ruta += fila['Nombre']
                else:
                    ruta += fila['Nombre'][0] + '/' + fila['Nombre']
            elif fila['Camara'] == 'S2': # IMG_0001.JPG
                resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                if fila['Nombre'][0] == '5':
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/5/IMG_' + resultado.group(1).zfill(4) + '.JPG'
                else:    
                    # segmentos = str(int(fila['Nombre'].split('.')[1][0])+3)
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/4/IMG_' + resultado.group(1).zfill(4) + '.JPG'
            
            elif fila['Camara'] == 'S3': # IMG_0001.JPG
                resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                if fila['Nombre'][0] == '2':
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/2/IMG_' + resultado.group(1).zfill(4) + '.JPG'
                elif fila['Nombre'][0] == '3':
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/3/IMG_' + resultado.group(1).zfill(4) + '.JPG'
                else:    
                    # segmentos = str(int(fila['Nombre'].split('.')[1][0])+3)
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/1/IMG_' + resultado.group(1).zfill(4) + '.JPG'
            
            
            elif fila['Camara'] == 'S4': # IMG_0001.JPG
                ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara'])
                resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                if fila['Nombre'][0] == 'I':
                    ruta += '/1/'+ fila['Nombre']
                elif fila['Nombre'][0] == '2':
                    ruta += '/2/'+ fila['Nombre'][1:]  
                elif fila['Nombre'][0] == '0':
                    ruta += '/'+ fila['Nombre'][1:]     
                elif(len(resultado.group(1))>=5): 
                    ruta += '/1/IMG_' + resultado.group(1)[1:4].zfill(4) + '.JPG'
                else:
                    ruta += '/IMG_' + resultado.group(1).zfill(4) + '.JPG'
            elif fila['Camara'] == 'S5': 
                resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                if fila['Nombre'][0] == '2':
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/1/1 - S5 - (' + resultado.group(1) + ').JPG'
                else:
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/1/2 - S5 - (' + resultado.group(1) + ').JPG'
            
            elif fila['Camara'] == 'S6': 
                resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                if fila['Nombre'][0] == '2':
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/2 - S6 - (' + resultado.group(1) + ').JPG'
                else:
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/1/1-S6- (' + resultado.group(1) + ').JPG'
            
            elif (fila['Camara'] == 'S7'): 
                resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                if fila['Nombre'][0] == '2':
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/2/IMG_' + resultado.group(1).zfill(4) + '.JPG'
                elif fila['Nombre'][0] == '0':
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/IMG_' + resultado.group(1).zfill(4) + '.JPG'
                else:
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/1/IMG_' + resultado.group(1).zfill(4) + '.JPG'
            elif (fila['Camara'] == 'S8'):
                if fila['Fecha'] in ('2022-03-11','2022-03-15'): # ESTAS IMAGENES CON ESTAS FECHAS NO EXISTEN ESAS FECHAS EN S8
                    ruta = ''
                else:
                    resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/1/IMG_' + resultado.group(1).zfill(4) + '.JPG'
            elif (fila['Camara'] == 'S9'):  
                if fila['Nombre'] == 'IMG_0788.JPG':
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/100_BTCF/IMG_0788.JPG'
                else:
                    resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/IMG_' + resultado.group(1).zfill(4) + '.JPG'
            
            elif (fila['Camara'] == 'S10') or (fila['Camara'] == 'S11'):  
                resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                if fila['Nombre'][0] == '2':
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/2/2-S11- (' + resultado.group(1) + ').JPG'
                else:
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/IMG_' + resultado.group(1).zfill(4) + '.JPG'
                
            
            elif (fila['Camara'] == 'S13'):
                ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/'
                if fila['Nombre'][0] == '1':
                    ruta += '1/' + str(fila['Nombre'][1:])
                elif fila['Nombre'][0] == 'S': #2/2-S13- (426).JPG
                    resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                    ruta += '2/2-S13- (' + resultado.group(1) + ').JPG'
                else:
                    ruta += fila['Nombre']
            
            elif (fila['Camara'] == 'S14'):
                resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/'
                if fila['Nombre'][0] == 'S':
                    ruta += '1/IMG_' + resultado.group(1).zfill(4) + '.JPG'
                elif fila['Nombre'][0]=='2':
                    ruta += '2/2-S14- (' + resultado.group(1) + ').JPG'
                else:
                    ruta += 'IMG_' + resultado.group(1).zfill(4) + '.JPG'

            elif (fila['Camara'] == 'S15'):
                ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/'
                if fila['Nombre'][0] == '2':
                    ruta += '2/' + str(fila['Nombre'])
                elif fila['Nombre'][0] == 'S':
                    resultado = re.search(r'\((.*?)\)', str(fila['Nombre']))
                    ruta += 'IMG_' + str(resultado.group(1).zfill(4)) + '.JPG'
                else:
                    ruta += '1/' + str(fila['Nombre'])      
            elif (fila['Camara'] == 'S16'):
                ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/'
                if fila['Nombre'][0] == '1':
                    ruta += '1/' + str(fila['Nombre'][1:])
                elif fila['Nombre'][0] == '2':
                    ruta += '2/' + str(fila['Nombre'][1:])    
                else:
                    ruta += fila['Nombre']

            elif (fila['Camara'] == 'S17'):
                ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/'
                if fila['Nombre'][0] == '1':
                    ruta += '1/' + str(fila['Nombre'][1:])
                elif fila['Nombre'][0] == '5':
                    ruta += '5/' + str(fila['Nombre'][1:])    
                elif fila['Nombre'][0] == '4':
                    ruta += '4/' + str(fila['Nombre'][1:])    
                else:
                    ruta += fila['Nombre']

            elif (fila['Camara'] == 'S18'): 
                resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                if fila['Nombre'][0] == '0':
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/IMG_' + resultado.group(1).zfill(4) + '.JPG'
                else:
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/1 - ' + fila['Camara'] + ' - (' + resultado.group(1) + ').JPG'
            
            elif fila['Camara'] == 'S19': 
                resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                if fila['Nombre'][0] == '2':
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/2 - S19 - (' + resultado.group(1) + ').JPG'
                else:
                    ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/1 - ' + fila['Camara'] + ' - (' + resultado.group(1) + ').JPG'
            
            else:
                ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/' + fila['Nombre']
        else:
            ruta += 'sauce/CT S ' + str(fila['Año']) + '/' + str(fila['Camara']) + '/' + fila['Nombre']
        

    elif fila['Sitio'] == "Iberica":
        ruta += "Iberica/" + str(fila['Año']) + '/' 
        if fila['Año'] == 2021:
            ruta += fila['Camara'] + '/' + fila['Nombre']
        elif fila['Año'] == 2022:
            if (fila['Camara'] == 'IB1') and (fila['Nombre'][4] == 'b'):
                return ''
            else:
                resultado = re.search(r'\((.*?)\)', fila['Nombre'])
                ruta += 'Ib-22 (' + str(fila['Camara'][2]) + ')/IMG_' + resultado.group(1).zfill(4) + '.JPG'
        else:
            raise ValueError("No existe esa ruta.")
    else:
        raise ValueError("No existe esa ruta.")
    
    ruta = ruta.strip(' ')

    if ruta in objetos_s3:
        return ruta
    return ''

# Función para obtener los datos de una imagen en S3
def extraerFechaHora(image_key):
    if image_key != '':
        try:
            # Obtiene el objeto de la imagen desde S3
            response = s3.get_object(Bucket='s3-pfa', Key=image_key)
            # Obtiene el cuerpo del objeto (que contiene los datos de la imagen)
            image_data = response['Body'].read()

            # A continuación, puedes procesar los datos de la imagen como desees.
            # Por ejemplo, puedes usar una biblioteca como Pillow (PIL) para trabajar con la imagen.

            # Aquí puedes agregar tu código para procesar la imagen y extraer los datos de metadatos.
            # Por ejemplo, si quieres extraer datos EXIF:
        
            image = Image.open(io.BytesIO(image_data))
            exif_data = image._getexif()
            
            # Crea un diccionario para almacenar los datos de metadata
            metadata = {}

            # Itera a través de los datos EXIF y los almacena en el diccionario
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                metadata[tag_name] = value


            fechahora = metadata.get('DateTime')
            fecha, hora = fechahora.split(' ')

            # Devuelve los datos de metadatos en el formato que necesites (por ejemplo, como un diccionario)
            return fecha, hora  # Cambia esto según tus necesidades

        except Exception as e:
            print(f'Error al procesar la imagen {image_key}: {str(e)}')
            return '',''
    return '',''

# def load_and_convert_image(img_path):
#     # Leer y decodificar la imagen
#     img = tf.io.read_file(img_path)
#     img = tf.image.decode_image(img, channels=3, expand_animations=False)  # asumimos imágenes en color (3 canales)
    
#     # Cambiar el tamaño de la imagen a 150x150
#     img_resized = tf.image.resize(img, [150, 150])
    
#     return tf.convert_to_tensor(img_resized)

def load_and_convert_image(img_path):
    # Leer y decodificar la imagen
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3, expand_animations=False)  # asumimos imágenes en color (3 canales)
    
    # Cambiar el tamaño de la imagen a 150x150
    img_resized = tf.image.resize(img, [150, 150])
    
    # Expandir las dimensiones para simular un batch de una sola imagen
    img_batch = tf.expand_dims(img_resized, axis=0)
    
    return img_batch

def get_date_time_from_image(path):
    """Extrae la fecha y hora de la metadata de una imagen."""
    try:
        with Image.open(path) as img:
            exif_data = img._getexif()
            if exif_data and 36867 in exif_data:  # 36867 es el tag para DateTimeOriginal
                date_time = exif_data[36867]
                date, time = date_time.split(" ")
                return date, time
    except Exception as e:
        print(f"Error processing image {path}: {e}")
    return None, None
