# script_menu_prediccion_CNN_TL.py

import os
import papermill as pm
from nbformat import read

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

# Definir las rutas de los archivos de datos
rutas_datos = {
    "partidos": "../../data/partidos_limpio.csv",
    "partidos_2023-2024": "../../data/partidos_2023-2024.csv",
    "equipos": "../../data/equipos.csv",
    "jugadores": "../../data/jugadores.csv",
    "imagenes":"../../images",
    "imagenes_prueba":"../../imagenes_prueba",
    # Agrega más rutas de archivos según sea necesario
}

# Diccionario para asociar modelos con índices de celda específicos
modelos_indices_celda = {
    os.path.abspath("../modelos/Aprendizaje profundo /CNN.ipynb"): 3,
    os.path.abspath("../modelos/Aprendizaje profundo/TL.ipynb"): 4,
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

# Lista de modelos de interés
modelos_interes = ["CNN", "TL"]

# Mostrar los notebooks encontrados
print("Bienvenido al predictor de ganador de la Champions League!")
print("Por favor, seleccione un modelo para predecir el ganador:")

# Iterar sobre los modelos de interés
for i, modelo in enumerate(modelos_interes, start=1):
    notebooks_encontrados = [notebook for notebook in modelos_indices_celda.keys() if modelo in notebook]
    for notebook in notebooks_encontrados:
        print(f"{i}. {modelo} - {os.path.relpath(notebook, carpeta_raiz)}")

if notebooks_encontrados:
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
else:
    print("No se encontraron modelos disponibles.")  
