# Descarga de Archivos:
## Como los archivos resultan ser pesados se pueden obtener ejecutando el siguiente codigo:

import gdown

url = 'https://drive.google.com/uc?id='

### Archivos Utiles:
#### dataset_entrenamiento.pkl https://drive.google.com/file/d/13AdSI0L25Oe-sfJ1qQVatbHMl9KLHa4u/view?usp=drive_link

id = '13AdSI0L25Oe-sfJ1qQVatbHMl9KLHa4u'
output = 'ModelosAI/ArchivosUtiles/dataset_entrenamiento.pkl'
gdown.download(url+id, output, quiet=False)

#### dataset_entrenamiento_Especie.pkl https://drive.google.com/file/d/13A7vYStuquFek6ezfWP9tSsuzEx2NMXy/view?usp=drive_link

id = '13A7vYStuquFek6ezfWP9tSsuzEx2NMXy'
output = 'ModelosAI/ArchivosUtiles/dataset_entrenamiento_Especie.pkl'
gdown.download(url+id, output, quiet=False)

#### trainingAnimal.pkl https://drive.google.com/file/d/138iQgkcXzjWZp-0FFOTd4NRBbRs2eymu/view?usp=drive_link

id = '138iQgkcXzjWZp-0FFOTd4NRBbRs2eymu'
output = 'ModelosAI/ArchivosUtiles/trainingAnimal.pkl'
gdown.download(url+id, output, quiet=False)

#### testingAnimal.pkl https://drive.google.com/file/d/13-2x6pbO7EZawW-oFhL1YXJD8qol4z_O/view?usp=drive_link

id = '13-2x6pbO7EZawW-oFhL1YXJD8qol4z_O'
output = 'ModelosAI/ArchivosUtiles/testingAnimal.pkl'
gdown.download(url+id, output, quiet=False)

#### trainingGuanaco.pkl https://drive.google.com/file/d/139S-PtPA3YJvF0R4SorOjNSM7StjU1Fx/view?usp=drive_link

id = '139S-PtPA3YJvF0R4SorOjNSM7StjU1Fx'
output = 'ModelosAI/ArchivosUtiles/trainingGuanaco.pkl'
gdown.download(url+id, output, quiet=False)

#### testingGuanaco.pkl https://drive.google.com/file/d/138ju2Jcsv_BbbmgxKUM_tP9YTim_DdE7/view?usp=drive_link

id = '138ju2Jcsv_BbbmgxKUM_tP9YTim_DdE7'
output = 'ModelosAI/ArchivosUtiles/testingGuanaco.pkl'
gdown.download(url+id, output, quiet=False)

#### trainingCategoria.pkl https://drive.google.com/file/d/139e2c20_dJv0QKezrDTEB4DPqDK1-mXg/view?usp=drive_link

id = '139S-PtPA3YJvF0R4SorOjNSM7StjU1Fx'
output = 'ModelosAI/ArchivosUtiles/trainingCategoria.pkl'
gdown.download(url+id, output, quiet=False)

#### testingCategoria.pkl https://drive.google.com/file/d/137KY84Oy6m_ReaD1NgSYSxQlF3e0hJM9/view?usp=drive_link

id = '137KY84Oy6m_ReaD1NgSYSxQlF3e0hJM9'
output = 'ModelosAI/ArchivosUtiles/testingCategoria.pkl'
gdown.download(url+id, output, quiet=False)

#### trainingEspecie.pkl https://drive.google.com/file/d/1346xbjSRLI_okOwZofYRlQrq26oivEZ7/view?usp=drive_link

id = '1346xbjSRLI_okOwZofYRlQrq26oivEZ7'
output = 'ModelosAI/ArchivosUtiles/trainingEspecie.pkl'
gdown.download(url+id, output, quiet=False)

#### testingEspecie.pkl https://drive.google.com/file/d/133y0GQzsUu0f5J3TzeCPLNadtC5lly71/view?usp=drive_link

id = '133y0GQzsUu0f5J3TzeCPLNadtC5lly71'
output = 'ModelosAI/ArchivosUtiles/testingEspecie.pkl'
gdown.download(url+id, output, quiet=False)

### ModelosFinales

#### modeloAnimalVGG16.h5 https://drive.google.com/file/d/13CiNIHUHP4NkA4ZczrnUG5PSQ4OkfeWD/view?usp=drive_link

id = '13CiNIHUHP4NkA4ZczrnUG5PSQ4OkfeWD'
output = 'ModelosAI/ModelosFinales/modeloAnimalVGG16.h5'
gdown.download(url+id, output, quiet=False)

#### modeloGuanacoVGG16.h5 https://drive.google.com/file/d/13HcriUZNyB5tzTmA8bA7oALwMZR8KNkP/view?usp=drive_link

id = '13HcriUZNyB5tzTmA8bA7oALwMZR8KNkP'
output = 'ModelosAI/ModelosFinales/modeloGuanacoVGG16.h5'
gdown.download(url+id, output, quiet=False)

#### modeloAnimalIV3.h5 https://drive.google.com/file/d/139fxcJeYVwbVIYX0fL6qjcbB6dKu6Q_a/view?usp=drive_link

id = '139fxcJeYVwbVIYX0fL6qjcbB6dKu6Q_a'
output = 'ModelosAI/ModelosFinales/modeloAnimalIV3.h5'
gdown.download(url+id, output, quiet=False)

#### modeloGuanacoIV3.h5 https://drive.google.com/file/d/13CqX7oCyp3lX6Mk-lwMq1c8s5iQCd089/view?usp=drive_link

id = '13CqX7oCyp3lX6Mk-lwMq1c8s5iQCd089'
output = 'ModelosAI/ModelosFinales/modeloGuanacoIV3.h5'
gdown.download(url+id, output, quiet=False)

#### modeloAnimalRN50.h5 https://drive.google.com/file/d/13CGuPUT0PMY7dIrGdGCVDfhSmwZj3CNY/view?usp=drive_link

id = '13CGuPUT0PMY7dIrGdGCVDfhSmwZj3CNY'
output = 'ModelosAI/ModelosFinales/modeloAnimalRN50.h5'
gdown.download(url+id, output, quiet=False)

#### modeloGuanacoRN50.h5 https://drive.google.com/file/d/13Gkkwq8g66L8A4efAaiGRM1FYNlaNIAm/view?usp=drive_link

id = '13Gkkwq8g66L8A4efAaiGRM1FYNlaNIAm'
output = 'ModelosAI/ModelosFinales/modeloGuanacoRN50.h5'
gdown.download(url+id, output, quiet=False)