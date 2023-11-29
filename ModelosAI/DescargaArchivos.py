# Descarga de Archivos:
## Como los archivos resultan ser pesados se pueden obtener ejecutando el siguiente codigo:

import gdown
import os

# Función para asegurarse de que una carpeta exista, si no, la crea
def asegurar_carpeta_existente(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Asegurar que las carpetas existen
asegurar_carpeta_existente('ModelosAI/ArchivosUtiles')
asegurar_carpeta_existente('ModelosAI/ModelosFinales')

# Función para descargar un archivo solo si no existe
def descargar_si_no_existe(url_id, output_path):
    if not os.path.exists(output_path):
        gdown.download(url + url_id, output_path, quiet=False)

url = 'https://drive.google.com/uc?id='

### Archivos Utiles:
# descargar_si_no_existe('13AdSI0L25Oe-sfJ1qQVatbHMl9KLHa4u', 'ModelosAI/ArchivosUtiles/dataset_entrenamiento.pkl')
# descargar_si_no_existe('13A7vYStuquFek6ezfWP9tSsuzEx2NMXy', 'ModelosAI/ArchivosUtiles/dataset_entrenamiento_Especie.pkl')
descargar_si_no_existe('1Ne4HQshbEDHNj3V4oq4c9OQaKQFUKdXc', 'ModelosAI/ArchivosUtiles/trainingAnimal.pkl')
descargar_si_no_existe('1MIbQLvYoc8uO612tpwv8FgfeRACK--do', 'ModelosAI/ArchivosUtiles/testingAnimal.pkl')
descargar_si_no_existe('1zwjXEBB_vphcZ-MiSDHkKhodL9EDhqc2', 'ModelosAI/ArchivosUtiles/trainingGuanaco.pkl')
descargar_si_no_existe('120erB1Ffo7TuRzC0ZcQmi8mgJoZt-CEA', 'ModelosAI/ArchivosUtiles/testingGuanaco.pkl')
# descargar_si_no_existe('139S-PtPA3YJvF0R4SorOjNSM7StjU1Fx', 'ModelosAI/ArchivosUtiles/trainingCategoria.pkl')
# descargar_si_no_existe('137KY84Oy6m_ReaD1NgSYSxQlF3e0hJM9', 'ModelosAI/ArchivosUtiles/testingCategoria.pkl')
# descargar_si_no_existe('1346xbjSRLI_okOwZofYRlQrq26oivEZ7', 'ModelosAI/ArchivosUtiles/trainingEspecie.pkl')
# descargar_si_no_existe('133y0GQzsUu0f5J3TzeCPLNadtC5lly71', 'ModelosAI/ArchivosUtiles/testingEspecie.pkl')

### ModelosFinales
descargar_si_no_existe('1juJkifnzEC1DnSyhggA1Q4dU-RX-qx5o', 'ModelosAI/ModelosFinales/modeloAnimalVGG16.h5')
# descargar_si_no_existe('13HcriUZNyB5tzTmA8bA7oALwMZR8KNkP', 'ModelosAI/ModelosFinales/modeloGuanacoVGG16.h5')
# descargar_si_no_existe('139fxcJeYVwbVIYX0fL6qjcbB6dKu6Q_a', 'ModelosAI/ModelosFinales/modeloAnimalIV3.h5')
# descargar_si_no_existe('13CqX7oCyp3lX6Mk-lwMq1c8s5iQCd089', 'ModelosAI/ModelosFinales/modeloGuanacoIV3.h5')
# descargar_si_no_existe('13CGuPUT0PMY7dIrGdGCVDfhSmwZj3CNY', 'ModelosAI/ModelosFinales/modeloAnimalRN50.h5')
descargar_si_no_existe('1vQvGHsDaaHTrmFlJBLLN-s5Z72TdjIEJ', 'ModelosAI/ModelosFinales/modeloGuanacoRN50.h5')
descargar_si_no_existe('1RXYv-416CqXs56tR5K9LLvk0d-eP837Z', 'ModelosAI/ModelosFinales/modeloMegadetector.pt')