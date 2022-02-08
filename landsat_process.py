from rotinas.imagem_control.imagem_batch import ImagemProcessBatch
from rotinas.path_control.sat_utils import LandsatControl

shapefile = r''

landsat_process = LandsatControl(r'')

landsat_id_original_files_dir = landsat_process.landsat_wd()[0]
landsat_id_crop_dir = landsat_process.landsat_wd()[1]
landsat_id_product_dir = landsat_process.landsat_wd()[2]

landsat_process.landsat_org_files()
ImagemProcessBatch.recortar(landsat_id_original_files_dir, shapefile, landsat_id_crop_dir)
ImagemProcessBatch.reescalar(landsat_id_crop_dir, landsat_id_product_dir)
ImagemProcessBatch.aplicar_algoritmos(landsat_id_product_dir, landsat_id_product_dir)

