import os

from pathlib import Path


def listar_shapefiles(diretorio_de_shapes):
    """Função que lista shapefiles de um diretório

    Args:
        diretorio_de_shapes (list): diretório com os arquivos shapefiles

    Returns:
        list: retorna uma lista com os arquivos shapefiles
    """
    lista_de_shapes = []
    iterar_arquivos = Path(diretorio_de_shapes).iterdir()
    for entrada in iterar_arquivos:
        if entrada.is_file():
            if str(entrada).endswith(".shp"):
                lista_de_shapes.append(str(Path(diretorio_de_shapes, entrada.name)))
    return lista_de_shapes


