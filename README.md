# RewildingAI-ImageAnalysis
Plataforma de análisis de imágenes basada en inteligencia artificial para la identificación y clasificación de fauna en el contexto de proyectos de conservación. Desarrollado en colaboración con la Fundación Rewilding Argentina.

## Resumen
Este proyecto forma parte de la tesis universitaria para la carrera de Data Science - ITBA. Se ha desarrollado con el objetivo de proporcionar herramientas avanzadas de análisis de imágenes a la Fundación Rewilding Argentina, mejorando así sus esfuerzos en proyectos de conservación.

## Autores
- [Abril Noguera](https://github.com/abrilnoguera)
- [Lucas Arbues](https://github.com/lucasarbues)
- [Ignacio De Achaval](https://github.com/IgnacioAchaval)

## Índice
1. [Introducción](#introducción)
2. [Metodología](#metodología)
3. [Instalación](#instalación)
4. [Licencia](#licencia)
5. [Agradecimientos](#agradecimientos)

## Introducción
La Fundación Rewilding Argentina desempeña un papel esencial en la conservación y restauración de la biodiversidad de los ecosistemas argentinos. No obstante, al emplear cámaras trampa para determinar la abundancia de especies, se enfrenta a significativas limitaciones. Pese a la importancia de estas técnicas, el análisis manual de las vastas cantidades de imágenes no solo resulta arduo, sino que también está expuesto a inconsistencias y errores humanos, exacerbados por la proporción de imágenes que podrían no contener registros faunísticos.

La solución propuesta en este proyecto es la adopción de una tecnología basada en Inteligencia Artificial para el procesamiento y clasificación automatizada de dichas imágenes. Esta innovación no solo mejora la precisión del análisis, sino que también optimiza la eficiencia del proceso, permitiendo a la fundación fundamentar sus estrategias de conservación y restauración en datos más robustos y confiables.

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

## Licencia
Este proyecto se encuentra bajo la licencia MIT. Consulta el archivo [LICENSE](https://opensource.org/licenses/MIT) para obtener más detalles.

## Agradecimientos
Agradecimiento especial a la Fundación Rewilding Argentina por su colaboración y apoyo continuo.
Reconocimientos a profesores y tutores de la materia Proyecto Final Analitica del Instituto Tecnologico de Buenos Aires (ITBA).
