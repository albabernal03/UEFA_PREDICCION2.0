#Aqui estuvimos probando el uso de papermill para ejecutar notebooks desde un script de python
#El objetivo era ejecutar un notebook de jupyter y mostrar solo los resultados de una celda específica
#Esto se ha conseguido pero al final no se ha usado en el proyecto final

import os
import papermill as pm
import nbformat

def ejecutar_notebook(notebook_path, output_path):
    # Construir la ruta absoluta del notebook original y de salida
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, notebook_path)
    output_notebook = os.path.join(base_dir, output_path, f"output_{os.path.basename(notebook_path)}")

    # Ejecutar el notebook y guardar la salida
    pm.execute_notebook(
        input_path=input_path,
        output_path=output_notebook,
        parameters={}
    )
    return output_notebook

def mostrar_celda(output_notebook, cell_index):
    # Abrir el notebook de salida y mostrar solo los resultados de la celda específica
    with open(output_notebook, 'r', encoding='utf-8') as f:  # Especificar codificación utf-8
        nb = nbformat.read(f, as_version=4)
        if 'outputs' in nb.cells[cell_index]:
            print(f"Resultados de la celda {cell_index} en {output_notebook}:")
            for output in nb.cells[cell_index]['outputs']:
                if 'text' in output:
                    print(output['text'])
                elif 'data' in output:
                    for key, value in output['data'].items():
                        if key.startswith('text/plain'):
                            print(value)

def elegir_modelo():
    modelos = [
        ("Aprendizaje no supervisado", "clustering.ipynb", 10),
        ("Aprendizaje por refuerzo", "cadenas_markov.ipynb", 20),
        ("Aprendizaje profundo", "DNN.ipynb", 5),
        ("Aprendizaje supervisado", "clasificacion_mejorado.ipynb", 36)
    ]
    print("Elige un modelo para predecir los resultados de la Champions League:")
    for i, (categoria, modelo, _) in enumerate(modelos, 1):
        print(f"{i}. {categoria} - {modelo}")
    seleccion = int(input("Introduce el número del modelo: ")) - 1
    return modelos[seleccion]

if __name__ == "__main__":
    modelo_seleccionado = elegir_modelo()
    path, notebook, celda_index = modelo_seleccionado
    notebook_path = f"../modelos/{path}/{notebook}"
    output_path = "outputs"

    # Asegúrate de que el directorio de salida existe
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_output_path = os.path.join(base_dir, output_path)
    if not os.path.exists(full_output_path):
        os.makedirs(full_output_path)

    # Ejecutar el modelo seleccionado y mostrar solo los resultados de la celda especificada
    output_notebook = ejecutar_notebook(notebook_path, output_path)
    mostrar_celda(output_notebook, celda_index)

