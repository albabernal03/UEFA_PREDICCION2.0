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
    "imagenes":"../../imagenes",
    "imagenes_prueba":"../../imagenes_prueba",
    # Agrega más rutas de archivos según sea necesario
}

# Diccionario para asociar modelos de predicción con índices de celda específicos
modelos_indices_celda = {
    os.path.abspath('../modelos/Aprendizaje por refuerzo/cadenas_markov.ipynb'): 21,
    os.path.abspath("../modelos/modelo2.ipynb"): 1,
    os.path.abspath("../modelos/modelo3.ipynb"): 2,
    # Agrega más modelos y sus índices de celda aquí
}

# Carpeta raíz donde se encuentran los modelos
carpeta_raiz_modelos = "../modelos"

# Función para listar todos los notebooks en una carpeta y sus subcarpetas
def listar_notebooks(carpeta_raiz):
    notebooks = []
    for ruta, _, archivos in os.walk(carpeta_raiz):
        for archivo in archivos:
            if archivo.endswith(".ipynb"):
                notebooks.append(os.path.join(ruta, archivo))
    return notebooks


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

# Mostrar menú de selección de modelos
print("Bienvenido al predictor de la Champions League e imágenes!")
print("Seleccione una opción:")
print("1. Predicción de la Champions League")
print("2. Análisis de imágenes (CNN o TL)")
print("3. Ver clusters (equipos o jugadores)")
print("4. Salir")

opcion = input("Ingrese el número de opción que desea ejecutar: ")

if opcion == "1":
    # Lista todos los notebooks en la carpeta raíz de modelos y subcarpetas, excluyendo los de CNN y TL
    notebooks_encontrados = [notebook for notebook in listar_notebooks(carpeta_raiz_modelos) if "CNN" not in notebook and "TL" not in notebook and "clustering" not in notebook and "clustering2" not in notebook]

    print("Por favor, seleccione un modelo para predecir el ganador de la Champions League:")

    for i, notebook in enumerate(notebooks_encontrados, start=1):
        print(f"{i}. {os.path.relpath(notebook, carpeta_raiz_modelos)}")

    opcion_modelo = input("Ingrese el número del modelo que desea utilizar: ")

    # Validar la opción ingresada por el usuario
    if opcion_modelo.isdigit() and 1 <= int(opcion_modelo) <= len(notebooks_encontrados):
        notebook_index = int(opcion_modelo) - 1
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

elif opcion == "2":
    print("Seleccione el tipo de modelo de imágenes:")
    print("1. Convolutional Neural Network (CNN)")
    print("2. Transfer Learning (TL)")

    opcion_modelo_imagenes = input("Ingrese el número del modelo de imágenes que desea utilizar: ")

    if opcion_modelo_imagenes == "1":
        # Ejecutar el notebook de DNN
        notebook_dnn = os.path.abspath("../modelos/Aprendizaje profundo/DNN.ipynb")
        indice_celda_dnn = modelos_indices_celda.get(notebook_dnn)
        if indice_celda_dnn is not None:
            output_resultado = ejecutar_notebook(notebook_dnn, indice_celda_dnn)
            if output_resultado:
                print("Resultado de la ejecución:")
                print(output_resultado)
            else:
                print("No se encontró ningún resultado de ejecución para la celda de salida.")
        else:
            print("No se ha especificado un índice de celda para el modelo DNN.")
            
    elif opcion_modelo_imagenes == "2":
        # Ejecutar el notebook de TL
        notebook_tl = os.path.abspath("../modelos/Aprendizaje profundo/TL.ipynb")
        indice_celda_tl = modelos_indices_celda.get(notebook_tl)
        if indice_celda_tl is not None:
            output_resultado = ejecutar_notebook(notebook_tl, indice_celda_tl)
            if output_resultado:
                print("Resultado de la ejecución:")
                print(output_resultado)
            else:
                print("No se encontró ningún resultado de ejecución para la celda de salida.")
        else:
            print("No se ha especificado un índice de celda para el modelo TL.")
    else:
        print("Opción inválida.")

elif opcion == "3":
    # Ejecutar clustering de equipos o jugadores
    print("Seleccione el tipo de clustering:")
    print("1. Clustering de equipos")
    print("2. Clustering de jugadores")

    opcion_cluster = input("Ingrese el número del clustering que desea ejecutar: ")

    if opcion_cluster == "1":
        # Ejecutar clustering de equipos (aquí debes agregar la lógica para ejecutar el clustering de equipos)
        print("Ejecutando clustering de equipos...")
        # Agrega aquí la lógica para ejecutar el clustering de equipos
    elif opcion_cluster == "2":
        # Ejecutar clustering de jugadores (aquí debes agregar la lógica para ejecutar el clustering de jugadores)
        print("Ejecutando clustering de jugadores...")
        # Agrega aquí la lógica para ejecutar el clustering de jugadores
    else:
        print("Opción inválida.")

elif opcion == "4":
    print("Saliendo del programa...")
else:
    print("Opción inválida.")
