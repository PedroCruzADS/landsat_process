import numpy as np
import rasterio


class algCalc:
    def __init__(self):
        pass

    def reescalar(img: str):
        """Função que reescalona imagem"""

        imagem_aberta = rasterio.open(img)
        banda_lida = imagem_aberta.read(masked=True)
        banda_reescalada_array = (banda_lida*0.0000275-0.2)/np.pi
        out_meta = imagem_aberta.meta
        out_meta.update({"driver": "GTiff", "dtype": rasterio.float32})
        return (banda_reescalada_array, out_meta)

    def tss(img: str):
        """Função que aplica algoritmo TSS na imagem"""
        np.seterr(divide='ignore')

        imagem_aberta = rasterio.open(img)
        banda_lida = imagem_aberta.read()
        tss_array = np.exp(9.656+1.672*np.log(abs(banda_lida)))
        out_meta = imagem_aberta.meta
        out_meta.update({"driver": "GTiff", "dtype": rasterio.float32})
        return (tss_array, out_meta)

    def tsi(img: str):
        """Função que aplica algoritmo TSI na imagem"""
        np.seterr(divide='ignore')

        imagem_aberta = rasterio.open(img)
        banda_lida = imagem_aberta.read()
        tsi_array = np.exp(10.73+2.08 * np.log(abs(banda_lida)))
        out_meta = imagem_aberta.meta
        out_meta.update({"driver": "GTiff", "dtype": rasterio.float32})
        return (tsi_array, out_meta)

    def aplicar_rf(self):
        """Função que aplica algoritmo RF na imagem"""
        return None  # array, meta
