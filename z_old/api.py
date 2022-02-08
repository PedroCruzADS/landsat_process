from pathlib import Path

from rotinas.imagem_control.imagem_alg import algCalc
from rotinas.imagem_control.imagem_process import ImagemProcess

imagem = r'LC08_L2SP_228061_20210906_20210915_02_T1_SR_B3.TIF'
diretorio_recortes = str(Path(Path.cwd))
diretorio_produtos = str(Path(Path.cwd))
shapefile = r'curuai_recorte2.shp'

# APLICA FUNÇÕES DE RECORTE, REESCALONAMENTO, TSS E TSSI EM IMAGENS SELECIONADAS

# RECORTE
imagem_recortada = ImagemProcess.recortar(imagem, shapefile)
imagem_recortada_path = ImagemProcess.salvar_imagem(
    imagem_recortada, diretorio_recortes, 'B3_rec.TIF')
# MANIPULAR DICT DE DADOS E SALVAR

# REESCALONAMENTO
imagem_reescalada = algCalc.reescalar(imagem_recortada_path)
imagem_reescalada_path = ImagemProcess.salvar_imagem(
    imagem_reescalada, diretorio_produtos, 'B3_re_rec.TIF')
# MANIPULAR DICT DE DADOS E SALVAR

# TSS
imagem_tss = algCalc.tss(imagem_reescalada_path)
imagem_tss_path = ImagemProcess.salvar_imagem(
    imagem_tss, diretorio_produtos, 'B3_tss.TIF')
# MANIPULAR DICT DE DADOS E SALVAR

# TSI
imagem_tsi = algCalc.tsi(imagem_reescalada_path)
imagem_tsi_path = ImagemProcess.salvar_imagem(
    imagem_tsi, diretorio_produtos, 'B3_tsi.TIF')
# MANIPULAR DICT DE DADOS E SALVAR
