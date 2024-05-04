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

# Resto del código del script...


