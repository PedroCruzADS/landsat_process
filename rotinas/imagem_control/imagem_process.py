# -*- coding: utf-8 -*-

from pathlib import Path

import fiona
import rasterio
from rasterio import mask


class ImagemProcess:
    def __init__(self) -> None:
        pass

    def salvar_imagem(imagem_data: tuple, imagem_destino: str, imagem_nome: str) -> str:
        """Salva qualquer imagem .TIF desde que contenha tupla com array e metadados.

        Args:
            imagem_data (tuple): Tupla que contém array e metadados da imagem que irá ser salva
            imagem_destino (str): Path que contém destino e nome do arquivo.

        Returns:
            str: Retorna o path da imagem salva.
        """

        imagem_nome_destino = str(Path(imagem_destino, imagem_nome))

        with rasterio.open(imagem_nome_destino, "w", **imagem_data[1]) as dest:
            dest.write(imagem_data[0])
        return imagem_nome_destino

    def criar_stack(lista_bandas: list, nome_dir: str, nome_arquivo_produto: str):
        """Função que faz um stack de bandas de uma imagem.

        Args:
            lista_bandas (list): lista de bandas
            nome_dir (str): nome do diretório aonde o stack será salvo
            nome_arquivo (str): nome do arquivo
        """

        # Lê os metadados da primeira banda
        try:
            with rasterio.open(lista_bandas[0]) as src:
                meta = src.meta
        # Atualiza os metadados de acordo com o número de camadas
            meta.update(count=len(lista_bandas))

        # Lê cada camada e empilha
            with rasterio.open(str(Path(nome_dir, nome_arquivo_produto)) + '_' + str(len(lista_bandas)) + '.tif', 'w', **meta) as dst:
                for id, layer in enumerate(lista_bandas, start=1):
                    with rasterio.open(layer) as source:
                        dst.write_band(id, source.read(1))
        except IndexError:
            print("Erro: diretório vazio")

    def recortar(img: str, shp: str) -> tuple:
        """Recorta uma imagem com base no shapefile

        Args:
            img (str): path da imagem
            shp (str): shapefile correspondente da imagem

        Returns:
            tuple: Tupla com dados e metadados da imagem recortada
        """

        shapefile = fiona.open(shp)
        shapes = [feature["geometry"] for feature in shapefile]

        with rasterio.open(img, 'r') as src:
            out_image, out_transform = rasterio.mask.mask(
                src, shapes, crop=True)
            out_meta = src.meta

        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform})
        return (out_image, out_meta)
