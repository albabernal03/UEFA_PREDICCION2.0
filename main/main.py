import os
from json import load
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

console = Console()

def execute_notebook(notebook_path):
    with open(notebook_path, encoding="utf8") as fp:
        nb = load(fp)
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(line for line in cell['source'] if not line.startswith('%'))
            exec(source, globals(), locals())
        elif cell['cell_type'] == 'markdown':
            markdown_string = ''.join(line for line in cell['source'] if not line.startswith('%'))
            md = Markdown(markdown_string)
            console.print(md)

def main():
    modelos_path = 'modelos'
    categorias = os.listdir(modelos_path)
    console.print("Seleccione la categoría de modelo que desea ejecutar:")
    for i, categoria in enumerate(categorias, 1):
        console.print(f"{i}. {categoria}")

    categoria_elegida = Prompt.ask("Ingrese el número de la categoría deseada")
    categoria_path = os.path.join(modelos_path, categorias[int(categoria_elegida) - 1])
    modelos = os.listdir(categoria_path)

    console.print("Seleccione el modelo que desea ejecutar:")
    for i, modelo in enumerate(modelos, 1):
        console.print(f"{i}. {modelo}")

    modelo_elegido = Prompt.ask("Ingrese el número del modelo deseado")
    notebook_path = os.path.join(categoria_path, modelos[int(modelo_elegido) - 1])



    # Ejecutar el modelo elegido
    execute_notebook(notebook_path)

if __name__ == "__main__":
    main()
