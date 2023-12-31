import re
# import boto3
# import cv2
import numpy as np
import io
# import os
import tensorflow as tf
from PIL import Image
from PIL.ExifTags import TAGS
import pickle
import torchvision.transforms as transforms
import contextlib
from tqdm import tqdm
# import supervision as sv
from torchvision import models
import torch
from torch.hub import load_state_dict_from_url
from yolov5.utils.general import non_max_suppression, scale_coords

# Leer objetos_s3
with open('ArchivosUtiles/objetos_s3.pkl', 'rb') as archivo:
    objetos_s3 = pickle.load(archivo)

# # Importo Informacion del AccessKey.
# accessKey = os.getenv("AccessKey")
# secretKey = os.getenv("SecretKey")
# # Configura tus credenciales de AWS si aún no lo has hecho
# boto3.setup_default_session(aws_access_key_id=accessKey,
#                            aws_secret_access_key=secretKey,
#                            region_name='us-east-2')
# # Nombre del bucket
# nombre_bucket_s3 = 's3-pfa'
# # Crea un cliente de S3
# s3 = boto3.client('s3')

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



class YOLOV5Base:
    """
    Base detector class for YOLO V5. This class provides utility methods for
    loading the model, generating results, and performing single and batch image detections.
    """

    # Placeholder class-level attributes to be defined in derived classes
    IMAGE_SIZE = None
    STRIDE = None
    CLASS_NAMES = None
    TRANSFORM = None

    def __init__(self, weights=None, device="cpu", url=None):
        """
        Initialize the YOLO V5 detector.

        Args:
            weights (str, optional): 
                Path to the model weights. Defaults to None.
            device (str, optional): 
                Device for model inference. Defaults to "cpu".
            url (str, optional): 
                URL to fetch the model weights. Defaults to None.
        """
        self.model = None
        self.device = device
        self._load_model(weights, self.device, url)
        self.model.to(self.device)

    def _load_model(self, weights=None, device="cpu", url=None):
        """
        Load the YOLO V5 model weights.

        Args:
            weights (str, optional): 
                Path to the model weights. Defaults to None.
            device (str, optional): 
                Device for model inference. Defaults to "cpu".
            url (str, optional): 
                URL to fetch the model weights. Defaults to None.
        Raises:
            Exception: If weights are not provided.
        """
        if weights:
            checkpoint = torch.load(weights, map_location=torch.device(device))
        elif url:
            checkpoint = load_state_dict_from_url(url, map_location=torch.device(self.device))
        else:
            raise Exception("Need weights for inference.")
        # self.model = checkpoint["model"].float().fuse().eval()  # Convert to FP32 model
        # Temporarily redirect standard output to suppress print statements
        with contextlib.redirect_stdout(io.StringIO()):
            self.model = checkpoint["model"].float().fuse().eval()


    def results_generation(self, preds):
        """
        Generate modified results for detection.

        Args:
            preds (numpy.ndarray): Model predictions.

        Returns:
            dict: Dictionary containing the count of detections and the average confidence.
        """
        num_detections = preds.shape[0]
        if num_detections == 0:
            return 0, 0

        avg_confidence = np.mean(preds[:, 4])
        return num_detections, avg_confidence

    def single_image_detection(self, img, conf_thres=0.2, iou_thres = 0.45):
        """
        Perform detection on a single image with modified results.

        Args:
            img (torch.Tensor): Input image tensor.
            conf_thres (float, optional): Confidence threshold for predictions.

        Returns:
            dict: Modified detection results.
        """
        # Asegúrate de que img no es None y tiene la forma esperada
        if img is None or len(img.shape) != 3:
            return 0, 0

        # Predicción del modelo
        preds = self.model(img.unsqueeze(0).to(self.device))[0]

        # Aplicar non-maximum suppression para filtrar las predicciones
        preds = non_max_suppression(preds, conf_thres, iou_thres, max_det=300)

        # Verifica si hay detecciones después de NMS
        if not preds or len(preds[0]) == 0:
            return 0, 0

        # Procesar detecciones
        preds = preds[0]
        # Asegurarse de que las dimensiones de la imagen son correctas para scale_coords
        img_shape = img.shape if len(img.shape) == 3 else img[0].shape
        preds[:, :4] = scale_coords(img_shape, preds[:, :4], img.shape).round()

        return self.results_generation(preds.cpu().numpy())

def convert_to_pytorch_tensor(tf_tensor, target_size=(640, 640)):
    # Asegurarte de que los valores del tensor están en el rango [0, 1]
    if tf.reduce_max(tf_tensor) > 1.0:
        tf_tensor = tf_tensor / 255.0

    # Convertir el tensor de TensorFlow a un array de NumPy
    numpy_array = tf_tensor.numpy()

    # Convertir el array de NumPy a un tensor de PyTorch
    torch_tensor = torch.from_numpy(numpy_array)

    # Cambiar el orden de las dimensiones a CHW si es necesario (PyTorch espera CHW en lugar de HWC)
    torch_tensor = torch_tensor.permute(2, 0, 1)

    # Cambiar el tamaño del tensor de PyTorch a target_size
    resize_transform = transforms.Resize(target_size)
    resized_torch_tensor = resize_transform(torch_tensor)

    return resized_torch_tensor
