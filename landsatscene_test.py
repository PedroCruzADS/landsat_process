import json

from rotinas.imagem_control.imagem_data import ImagemData

imagem = ImagemData('LC08_L2SP_228061_20210906_20210915_02_T1_SR_B3_recortada.TIF')


a = 'indexedscene_model.json'

json_file = open(a)
indexedscene = json.load(json_file)


indexedscene['crs'] = imagem.get_crs()
indexedscene['grids']['default']['shape'] = imagem.get_shapes()
indexedscene['grids']['default']['transform'] = imagem.get_transform()

print(indexedscene)

