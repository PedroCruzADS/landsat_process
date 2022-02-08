from pathlib import Path

import rasterio
import rasterio.crs
import rasterio.features
import rasterio.warp


class ImagemData:
    def __init__(self, path: str):
        """Classe que retira dados da imagem de acordo com o método

        Args:
            path (str): Path da imagem
        """
        self.path = path
        self.raster = rasterio.open(path)

    def get_shapes(self):
        """tamanho e altura do raster"""
        
        return [self.raster.meta['width'], self.raster.meta['height']]

    def get_crs(self):
        """CRS da imagem"""
        crs = str(self.raster.meta['crs'])
        return crs

    def get_transform(self):
        """transform do raster"""
        transform = str(self.raster.meta['transform'])
        mod_t = transform.replace('|', '')
        transform = mod_t.replace('\n', '')
        transform = transform.replace(' ', '', 1)
        transform = [transform]
        return transform

    def get_geom(self):
        """geom da imagem"""
        with self.raster as dataset:
            mask = dataset.dataset_mask()
        
        for geom, val in rasterio.features.shapes(mask, transform=dataset.transform):
            geom = rasterio.warp.transform_geom(dataset.crs, 'EPSG:4326', geom, precision=6)
        return (geom['type'], geom['coordinates'])

    def get_banda(self):
        """Retira a banda da imagem do path"""
        list = self.path.split("B")
        for b in list:
            if b[0].isnumeric():
                banda = f"B{b[0]}"
                return banda

