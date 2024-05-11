
import os
import papermill as pm
import nbformat
import pandas as pd

# Función para actualizar la ruta en un notebook
def actualizar_ruta_en_notebook(notebook_path, old_path, new_path):
    try:
        # Cargar el notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Actualizar la celda que contiene la ruta del archivo
        for cell in notebook['cells']:
            if old_path in cell['source']:
                cell['source'] = cell['source'].replace(old_path, new_path)
        
        # Guardar el notebook modificado
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(notebook, f)

    except Exception as e:
        print(f"Error al actualizar la ruta en el notebook {notebook_path}: {str(e)}")

# Función para ejecutar automáticamente los notebooks de web scraping y limpieza de datos
def ejecutar_scraping_limpieza():
    try:
        # Obtener la lista de archivos en la carpeta de web scraping
        carpeta_scraping = "../webscraping"
        archivos_scraping = [os.path.join(carpeta_scraping, archivo) for archivo in os.listdir(carpeta_scraping) if archivo.endswith(".ipynb")]

        # Ejecutar cada archivo de web scraping
        for archivo_scraping in archivos_scraping:
            try:
                pm.execute_notebook(
                    archivo_scraping,
                    None,  # No se guarda la salida en ningún archivo
                    parameters={},  # No se necesitan parámetros adicionales para el web scraping
                    kernel_name='python'
                )
                print(f"Ejecución de {archivo_scraping} completada correctamente.")
            except Exception as e:
                print(f"Error al ejecutar {archivo_scraping}: {str(e)}")

        # Ejecutar el notebook de limpieza de datos
        pm.execute_notebook(
            os.path.abspath('../analisis/limpieza.ipynb'),
            None,  # No se guarda la salida en ningún archivo
            parameters={},  # No se necesitan parámetros adicionales para la limpieza de datos
            kernel_name='python'
        )
    except Exception as e:
        print(f"Error al ejecutar el web scraping y la limpieza de datos: {str(e)}")

# Ejecutar automáticamente el web scraping y la limpieza de datos al inicio del programa
ejecutar_scraping_limpieza()

# Definir las rutas de los archivos a actualizar
rutas_a_actualizar = {
    "../../data/partidos_limpio.csv": "../data/partidos_limpio.csv",
    "../../data/partidos_2023-2024_limpio.csv": "../data/partidos_2023-2024_limpio.csv",
    "../../data/equipos.csv": "../data/equipos.csv",
    "../../data/jugadores.csv": "../data/jugadores.csv",
    "../../images": "../images",
    "../../imagenes_prueba": "../imagenes_prueba",

    # Agrega más rutas a actualizar aquí si es necesario
}


# Actualizar las rutas en todos los notebooks
for root, dirs, files in os.walk("../modelos"):
    for file in files:
        if file.endswith(".ipynb"):
            notebook_path = os.path.join(root, file)
            for old_path, new_path in rutas_a_actualizar.items():
                actualizar_ruta_en_notebook(notebook_path, old_path, new_path)

# Definir las rutas de los archivos de datos
rutas_datos = {
    "partidos": "../data/partidos_limpio.csv",
    "partidos_2023-2024": "../data/partidos_2023-2024.csv",
    "equipos": "../data/equipos.csv",
    "jugadores": "../data/jugadores.csv",
    "imagenes":"../images",
    "imagenes_prueba":"../imagenes_prueba",
}

# Diccionario para asociar modelos con índices de celda específicos
modelos_indices_celda = {
    os.path.abspath('../modelos/Aprendizaje por refuerzo/cadenas_markov.ipynb'): 21,
    os.path.abspath("../modelos/Aprendizaje profundo/DNN.ipynb"): 2,
    os.path.abspath("../modelos/modelo3.ipynb"): 2,
    # Agrega más modelos y sus índices de celda aquí
}

# Función para ejecutar un notebook y devolver el resultado
def ejecutar_notebook(notebook, indice_celda):
    try:
        # Ejecutar el notebook sin guardar la salida en un archivo temporal
        output_nb = pm.execute_notebook(
            notebook,
            None,  # No se guarda la salida en ningún archivo
            parameters={"rutas_datos": rutas_datos},  # Pasar el diccionario de rutas de archivos como parámetro
            kernel_name='python'
        )

        # Obtener el resultado de la ejecución de la celda de salida
        output_resultado = output_nb.cells[indice_celda].outputs[0].data['text/plain']
        
        # Devolver el resultado
        return output_resultado
    
    except Exception as e:
        print(f"Error al ejecutar el notebook {notebook}: {str(e)}")
        return None

# Carpeta raíz donde se encuentran los modelos
carpeta_raiz = "../modelos"

# Función para listar todos los notebooks en una carpeta y sus subcarpetas
def listar_notebooks(carpeta_raiz):
    notebooks = []
    for ruta, _, archivos in os.walk(carpeta_raiz):
        for archivo in archivos:
            if archivo.endswith(".ipynb"):
                notebooks.append(os.path.join(ruta, archivo))
    return notebooks

# Lista todos los notebooks en la carpeta raíz y subcarpetas
notebooks_encontrados = listar_notebooks(carpeta_raiz)

# Mostrar los notebooks encontrados
print("Bienvenido al predictor de ganador de la Champions League!")
print("Por favor, seleccione un modelo para predecir el ganador:")

for i, notebook in enumerate(notebooks_encontrados, start=1):
    print(f"{i}. {os.path.relpath(notebook, carpeta_raiz)}")

opcion = input("Ingrese el número del modelo que desea utilizar: ")

# Validar la opción ingresada por el usuario
if opcion.isdigit() and 1 <= int(opcion) <= len(notebooks_encontrados):
    notebook_index = int(opcion) - 1
    notebook_seleccionado = notebooks_encontrados[notebook_index]
    
    # Obtener el índice de celda asociado al modelo seleccionado
    indice_celda = modelos_indices_celda.get(os.path.abspath(notebook_seleccionado))
    
    if indice_celda is not None:
        # Ejecutar el notebook y obtener el resultado
        output_resultado = ejecutar_notebook(notebook_seleccionado, indice_celda)
        if output_resultado:
            print("Resultado de la ejecución:")
            print(output_resultado)
        else:
            print("No se encontró ningún resultado de ejecución para la celda de salida.")
    else:
        print("No se ha especificado un índice de celda para este modelo.")
else:
    print("Opción inválida.")

# TODO: Terminar de implementar rutas de archivos y modelos
