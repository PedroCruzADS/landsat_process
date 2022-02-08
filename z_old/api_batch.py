from rotinas.imagemControl.imagem_batch import ImagemProcessBatch

# RECORTA E APLICA ALGORITMOS NO DIRETÓRIO QUE POSSUIR BANDAS SELECIONADAS, OU CRIA UM STACK DE BANDAS.

shapefile = r'C:\users\pedro\desktop\tss_curuai\shapefile'
diretorio_imagens = r'C:\users\pedro\desktop\tss_curuai\imagens'
diretorio_recortes = r'C:\users\pedro\desktop\tss_curuai\imagens_recortadas'
diretorio_produtos = r'C:\users\pedro\desktop\tss_curuai\produtos'


ImagemProcessBatch.recortar(diretorio_imagens, shapefile, diretorio_recortes)
ImagemProcessBatch.aplicar_algoritmos(diretorio_recortes, diretorio_produtos)
