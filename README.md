# RewildingAI-ImageAnalysis
Plataforma de análisis de imágenes basada en inteligencia artificial para la identificación y clasificación de fauna en el contexto de proyectos de conservación. Desarrollado en colaboración con la Fundación Rewilding Argentina.

## Resumen
Este proyecto forma parte de la tesis universitaria para la carrera de Data Science - ITBA. Se ha desarrollado con el objetivo de proporcionar herramientas avanzadas de análisis de imágenes a la Fundación Rewilding Argentina, mejorando así sus esfuerzos en proyectos de conservación.

## Autores
- [Abril Noguera](https://github.com/abrilnoguera)
- [Lucas Arbues](https://github.com/lucasarbues)
- [Ignacio De Achaval](https://github.com/IgnacioAchaval)

## Introducción
La Fundación Rewilding Argentina desempeña un papel esencial en la conservación y restauración de la biodiversidad de los ecosistemas argentinos. No obstante, al emplear cámaras trampa para determinar la abundancia de especies, se enfrenta a significativas limitaciones. Pese a la importancia de estas técnicas, el análisis manual de las vastas cantidades de imágenes no solo resulta arduo, sino que también está expuesto a inconsistencias y errores humanos, exacerbados por la proporción de imágenes que podrían no contener registros faunísticos.

La solución propuesta en este proyecto es la adopción de una tecnología basada en Inteligencia Artificial para el procesamiento y clasificación automatizada de dichas imágenes. Esta innovación no solo mejora la precisión del análisis, sino que también optimiza la eficiencia del proceso, permitiendo a la fundación fundamentar sus estrategias de conservación y restauración en datos más robustos y confiables.

## Overview del Proyecto
La Fundación Rewilding Argentina enfrenta desafíos críticos en la conservación de la biodiversidad, en un contexto donde un informe de la ONU (2020) alerta sobre una inminente sexta extinción masiva. La fundación, enfocada en restaurar ecosistemas y reintroducir especies nativas, opera en varias regiones (Chubut, Corrientes, Chaco, y Santa Cruz) implementando acciones como translocaciones de especies, manejo de pastizales, enriquecimiento de bosques, y control de especies exóticas.

Un método clave para evaluar la efectividad de estas acciones es el monitoreo de la vida silvestre, tradicionalmente realizado mediante transectas. Sin embargo, esta técnica tiene limitaciones, ya que gran parte de la fauna permanece oculta. Las cámaras trampa emergen como una solución tecnológica para observar indirectamente la fauna, pero generan un volumen masivo de datos. Anualmente, se capturan hasta 120,000 imágenes por zona, de las cuales un 70% podrían no contener fauna relevante, y el proceso manual de clasificación es lento y propenso a errores.

Para abordar este desafío, el proyecto propone la integración de inteligencia artificial buscando optimizar la clasificación y análisis de las imágenes capturadas. Esto acelera el proceso y mejora la precisión en la identificación de especies. Esta mejora en la recopilación de datos permitirá a los conservacionistas y formuladores de políticas tomar decisiones más informadas y efectivas, esenciales para la conservación y restauración de ecosistemas y la prevención de la extinción de especies.

El resultado ha sido una solución semi-automatizada que no solo mejora significativamente el proceso de clasificación de imágenes sino que también demuestra cómo la sinergia entre la inteligencia artificial y la intervención humana puede ser un catalizador potente para proyectos de conservación de la biodiversidad.

## Outputs del Proyecto
La adopción del proyecto proporcionará al cliente una interfaz visual intuitiva para la ejecución y validación de modelos de clasificación de imágenes, lo que facilita significativamente el proceso de monitoreo y análisis de datos. Esta interfaz permitiría a los usuarios interactuar de manera eficiente con el modelo, lo que agiliza la toma de decisiones basada en los datos obtenidos. Además, el proyecto incluye una base de datos robusta y organizada que asegura la consistencia en la clasificación de imágenes. Esto no solo optimiza la recuperación y el manejo de la información sino que también garantiza la integridad y la trazabilidad de los datos a lo largo del tiempo, lo que resulta crucial para estudios de estimación de poblaciones y para la verificación de la calidad de los datos en investigaciones de conservación y ecología.

- Modelos Predictivos:
  - Presencia de Animal
  - Especies
  - Cantidades
- Interfaces de Usuario:
  - Inferfaz de Modelos
  - Interfaz de Validacion
 
## Resultados de Proyectos
La adopción del proyecto proporcionará al cliente una interfaz visual intuitiva para la ejecución y validación de modelos de clasificación de imágenes, lo que facilita significativamente el proceso de monitoreo y análisis de datos. Esta interfaz permitiría a los usuarios interactuar de manera eficiente con el modelo, ajustar parámetros y validar los resultados de forma inmediata, lo que agiliza la toma de decisiones basada en los datos obtenidos. Además, el proyecto incluye una base de datos robusta y organizada que asegura la consistencia en la clasificación de imágenes. Esto no solo optimiza la recuperación y el manejo de la información sino que también garantiza la integridad y la trazabilidad de los datos a lo largo del tiempo, lo que resulta crucial para estudios de estimación de poblaciones y para la verificación de la calidad de los datos en investigaciones de conservación y ecología.

La implementación de la solución propuesta ha generado mejoras significativas en los indicadores relevantes para el proceso de clasificación automática de imágenes de animales capturadas por cámaras trampa. Se ha logrado una reducción del tiempo necesario para completar las jornadas totales en un 86.39%. En cuanto a la cantidad de imágenes procesadas por hora, se ha incrementado en un notable 638.1%.
La precisión del etiquetado, un aspecto crítico para la calidad del análisis de datos, se ha incrementado en un 38.7%. Este avance es fundamental para la precisión de estudios de biodiversidad y para el seguimiento de la fauna.
Desde una perspectiva económica, el costo total del proceso se ha reducido en un 41.17%. Finalmente, el ratio de imágenes utilizables se ha incrementado al darle valor a la totalidad de la información que se recolecta.

El análisis en este proyecto destacó la importancia de estandarizar las columnas categóricas para eliminar duplicados causados por pequeñas variaciones textuales, crucial para garantizar la coherencia y precisión de los datos, lo que mejoró los análisis subsecuentes. Se enfrentó al desafío de precisar las rutas de imágenes en la base de datos. Inicialmente, solo un 14.7% de las imágenes coincidían con las rutas generadas, debido a la variabilidad en la nomenclatura y almacenamiento de archivos. Tras un minucioso proceso, se logró una corrección del 99.4% de los datos. La estandarización y corrección de las rutas de los archivos en la base de datos se traduce en una mejora significativa para el proyecto, asegurando la consistencia y precisión en el manejo de la información y minimizando errores potenciales, vital en proyectos de gran escala y complejidad.

Estas mejoras no solo reflejan la eficacia de la solución propuesta, sino que también ponen de manifiesto la importancia de adoptar tecnologías avanzadas y metodologías optimizadas en la investigación y conservación de la vida silvestre. La capacidad para procesar y etiquetar eficientemente grandes volúmenes de imágenes abre nuevas posibilidades para el monitoreo ambiental y la toma de decisiones basada en datos en tiempo real, contribuyendo significativamente al campo de la ciencia de datos aplicada a la ecología y conservación.

## Instrucciones de Instalación

Este repositorio requiere Python 3.9.6. Se recomienda usar `conda` para crear entornos virtuales y gestionar las versiones de Python y paquetes.

### Clonar el Repositorio

```bash
git clone https://github.com/tu_usuario/RewildingAI-ImageAnalysis.git
cd RewildingAI-ImageAnalysis
pip install -r requirements.txt
```

### Instalación de Conda

Si aún no tienes Conda instalado, puedes descargar e instalar Anaconda o Miniconda desde sus respectivos sitios web. Anaconda incluye un conjunto de paquetes científicos por defecto, mientras que Miniconda es una versión más liviana que te permite instalar paquetes según sea necesario.

#### Crear un Nuevo Entorno Conda con Python 3.9.6

1. **Crear el Entorno**:
   - Abre tu terminal o Anaconda Prompt y ejecuta:
     ```
     conda create --name <name> python=3.9.6
     ```
     Esto crea un nuevo entorno llamado <name> con Python 3.9.6.

2. **Activar el Entorno**:
   - Activa el entorno con:
     ```
     conda activate <name>
     ```

### Instalación de Paquetes con Conda

1. **Instalar Paquetes Específicos**:
   - Dentro del entorno activado, instala TensorFlow, PyTorch y dependencias relacionadas utilizando Conda:
     ```
     conda install tensorflow
     ```
     ```
     pip install pytorchWildlife
     ```
     ```
     pip install charset_normalizer
     ```
     ```
     pip install pyarrow
     ```

## Metodología

#### 1. **Preparación de Datos**:
Los datos proporcionados, que comprenden aproximadamente 550 GB de imágenes, fueron recibidos mediante un disco rígido y posteriormente almacenados en Amazon Web Services (AWS), específicamente en un bucket de S3.

#### 2. **Plataforma y Lenguaje de Programación**:
Se eligió Python como lenguaje de programación debido a su vasta comunidad, librerías especializadas y frameworks de Aprendizaje Profundo como Pytorch y TensorFlow. Además, AWS se utilizó para el almacenamiento y gestión de los datos.

#### 3. **Técnicas de Construcción del Modelo**:

- **Redes Neuronales Convolucionales (CNN)**: Son redes diseñadas específicamente para el procesamiento de datos de imágenes y tienen la capacidad de aprender características en diferentes niveles de abstracción.

- **Data Augmentation**: Esta técnica implica la generación de versiones modificadas de las imágenes originales a través de rotaciones, reflejos, recortes, entre otros, para mejorar la generalización del modelo.

- **Upsampling/Downsampling**: Dadas las desigualdades en el balance del conjunto de datos, se utilizarán estas técnicas para garantizar un entrenamiento equilibrado del modelo.

- **Transfer Learning**: Implica el uso de una red neuronal previamente entrenada y su adaptación para el problema específico en cuestión.

#### 4. **Exploración de Arquitecturas**:

- **VGG16**: Esta arquitectura se destaca por su estructura simplificada y ha probado ser excepcionalmente eficaz en tareas de clasificación y localización.

- **InceptionV3**: Conocida por su módulo "Inception", esta arquitectura permite captar patrones en diferentes niveles de granularidad, optimizando el uso de recursos computacionales.

- **ResNet**: Introduce las "conexiones residuales" que facilitan el entrenamiento de redes más profundas, siendo una elección óptima para tareas que demandan una profundidad significativa.

Estas arquitecturas se han adaptado utilizando una estrategia de **transferencia de aprendizaje** basada en modelos entrenados en el dataset ImageNet.

## Instrucciones de Ejecucion de Interfaces:
### Interfaz de Ejecución de Modelos:
Se activa el entorno de ejecución.

```
conda activate <name>
```

Se descargan los archivos necesarios mediante el archivo **DescargaArchivos.py**.

```
python ModelosAI/DescargaArchivos.py
```

Se ejecuta la interfaz de ejecucion de modelos.

```
python InterfazUsuario/ui_ejecucion_modelos.py
```

### Interfaz de Validación:
Se activa el entorno de ejecución.

```
conda activate <name>
```

Se ejecuta la interfaz de validacion.

```
python InterfazUsuario/ui_validacion.py
```


## Licencia
Este proyecto se encuentra bajo la licencia MIT. Consulta el archivo [LICENSE](https://opensource.org/licenses/MIT) para obtener más detalles.

## Agradecimientos
Agradecimiento especial a la Fundación Rewilding Argentina por su colaboración y apoyo continuo.
Reconocimientos a profesores y tutores de la materia Proyecto Final Analitica del Instituto Tecnologico de Buenos Aires (ITBA).
