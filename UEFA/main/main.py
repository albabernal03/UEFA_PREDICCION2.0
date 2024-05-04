# script_menu_prediccion.py

import os
import papermill as pm

# Función para ejecutar un notebook
def ejecutar_notebook(notebook):
    try:
        pm.execute_notebook(
            notebook,
            notebook[:-6] + "_output.ipynb",  # Nombre del notebook de salida
            parameters=dict(),  # Parámetros opcionales si los necesitas
            log_output=True
        )
        print(f"Notebook {notebook} ejecutado exitosamente.")
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
    print(f"Utilizando {notebook_seleccionado} para predecir el ganador de la Champions League...")
    ejecutar_notebook(notebook_seleccionado)
else:
    print("Opción inválida.")
