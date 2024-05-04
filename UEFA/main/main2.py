# script_menu_prediccion.py

import os
import papermill as pm
from nbformat import read

# Diccionario para asociar modelos con índices de celda específicos
modelos_indices_celda = {
    os.path.abspath('../modelos/Aprendizaje por refuerzo/cadenas_markov.ipynb'): 8,
    os.path.abspath("../modelos/modelo2.ipynb"): 1,
    os.path.abspath("../modelos/modelo3.ipynb"): 2,
    # Agrega más modelos y sus índices de celda aquí
}

# Función para ejecutar un notebook
def ejecutar_notebook(notebook, indice_celda):
    try:
        # Ejecutar el notebook y guardar el resultado en un archivo temporal
        output_path = notebook[:-6] + "_output.ipynb"
        pm.execute_notebook(
            notebook,
            output_path,
            parameters=dict(),  # Parámetros opcionales si los necesitas
            kernel_name='python3'
        )

        # Leer el resultado del notebook
        with open(output_path, 'r') as f:
            nb = read(f, 4)

        # Imprimir el contenido de la celda específica
        print(f"Utilizando {notebook} para predecir el ganador de la Champions League...")
        print("Resultado de la ejecución:")
        if indice_celda < len(nb.cells):
            print(nb.cells[indice_celda].source)
        else:
            print("El índice de la celda especificada está fuera de rango.")
    except Exception as e:
        print(f"Error al ejecutar el notebook {notebook}: {str(e)}")

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
        ejecutar_notebook(notebook_seleccionado, indice_celda)
    else:
        print("No se ha especificado un índice de celda para este modelo.")
else:
    print("Opción inválida.")
