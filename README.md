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

## Instalacion
Este repositorio requiere Python 3.9.6. Se recomienda usar `pyenv` para gestionar las versiones de Python y `venv` para crear entornos virtuales.

## Instalación de `pyenv`

### En Linux y macOS

#### 1. Instala las dependencias necesarias:
   - En Debian/Ubuntu:
     ```
     sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
     ```
   - En Fedora/CentOS/RHEL:
     ```
     sudo yum install @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel git
     ```
   - En macOS (usando Homebrew):
     ```
     brew install openssl readline sqlite3 xz zlib
     ```

#### 2. Instala `pyenv`:
   - Clona el repositorio de `pyenv`:
     ```
     git clone https://github.com/pyenv/pyenv.git ~/.pyenv
     ```
   - Configura el entorno agregando lo siguiente a tu archivo `.bashrc` o `.zshrc`:
     ```
     export PYENV_ROOT="$HOME/.pyenv"
     export PATH="$PYENV_ROOT/bin:$PATH"
     eval "$(pyenv init --path)"
     ```

### En Windows
- `pyenv` no es compatible directamente con Windows, pero puedes usar `pyenv-win` a través de Git Bash o WSL.

## Instalación de Python 3.9.6

#### 1. Instala Python 3.9.6 usando `pyenv`:
   - Ejecuta:
     ```
     pyenv install 3.9.6
     ```
#### 2. Establece Python 3.9.6 como la versión predeterminada:
   - Globalmente:
     ```
     pyenv global 3.9.6
     ```
   - O en un directorio específico:
     ```
     pyenv local 3.9.6
     ```

## Uso de `venv` para Crear un Entorno Virtual

#### 1. Crea un entorno virtual:
   - Navega al directorio de tu proyecto.
   - Ejecuta:
     ```
     python -m venv <nombre_del_entorno>
     ```

#### 2. Activa el entorno virtual:
   - En Linux/macOS:
     ```
     source <nombre_del_entorno>/bin/activate
     ```
   - En Windows:
     ```
     <nombre_del_entorno>\Scripts\activate
     ```

#### 3. Instala los paquetes necesarios:
   - Asegúrate de que `pip` esté actualizado:
     ```
     pip install --upgrade pip
     ```
   - Instala los paquetes desde `requirements.txt`:
     ```
     pip install -r requirements.txt
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


## Instalación
Pasos y requerimientos para instalar el proyecto:

```bash
git clone https://github.com/tu_usuario/RewildingAI-ImageAnalysis.git
cd RewildingAI-ImageAnalysis
pip install -r requirements.txt
```

## Licencia
Este proyecto se encuentra bajo la licencia MIT. Consulta el archivo [LICENSE](https://opensource.org/licenses/MIT) para obtener más detalles.

## Agradecimientos
Agradecimiento especial a la Fundación Rewilding Argentina por su colaboración y apoyo continuo.
Reconocimientos a profesores y tutores de la materia Proyecto Final Analitica del Instituto Tecnologico de Buenos Aires (ITBA).
