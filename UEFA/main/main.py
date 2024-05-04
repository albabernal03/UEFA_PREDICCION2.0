# script_menu_prediccion.py

import os
import papermill as pm
from nbformat import read

# Definir las rutas de los archivos de datos
rutas_datos = {
    "partidos": "../../data/partidos_limpio.csv",
    "partidos_2023-2024": "../../data/partidos_2023-2024.csv",
    "equipos": "../../data/equipos.csv",
    "jugadores": "../../data/jugadores.csv",
    # Agrega más rutas de archivos según sea necesario
}

# Diccionario para asociar modelos con índices de celda específicos
modelos_indices_celda = {
    os.path.abspath('../modelos/Aprendizaje por refuerzo/cadenas_markov.ipynb'): 21,
    os.path.abspath("../modelos/modelo2.ipynb"): 1,
    os.path.abspath("../modelos/modelo3.ipynb"): 2,
    # Agrega más modelos y sus índices de celda aquí
}

# Función para ejecutar un notebook y devolver el resultado
def ejecutar_notebook(notebook, indice_celda):
    try:
        # Ejecutar el notebook y guardar el resultado en un archivo temporal
        output_path = notebook[:-6] + "_output.ipynb"
        pm.execute_notebook(
            notebook,
            output_path,
            parameters={"rutas_datos": rutas_datos},  # Pasar el diccionario de rutas de archivos como parámetro
            kernel_name='python'
        )

        # Devolver la ruta del archivo de salida donde se guarda el resultado
        return output_path
    except Exception as e:
        print(f"Error al ejecutar el notebook {notebook}: {str(e)}")
        return None

# Función para obtener el resultado de la ejecución de la celda de salida
def obtener_output(output_notebook, indice_celda):
    try:
        # Leer el resultado del notebook de salida
        with open(output_notebook, 'r') as f:
            nb_output = read(f, 4)

        # Obtener el contenido de la celda de salida asociada al índice
        if nb_output.cells and indice_celda < len(nb_output.cells):
            output_source = nb_output.cells[indice_celda].outputs[0].data['text/plain']
            return output_source
        else:
            return None
    except Exception as e:
        print(f"Error al obtener el output del notebook {output_notebook}: {str(e)}")
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
        # Ejecutar el notebook
        output_notebook = ejecutar_notebook(notebook_seleccionado, indice_celda)
        if output_notebook:
            # Obtener el resultado de la ejecución de la celda de salida
            output_resultado = obtener_output(output_notebook, indice_celda)
            if output_resultado:
                print("Resultado de la ejecución:")
                print(output_resultado)
            else:
                print("No se encontró ningún resultado de ejecución para la celda de salida.")
    else:
        print("No se ha especificado un índice de celda para este modelo.")
else:
    print("Opción inválida.")

    print("Opción inválida.")
