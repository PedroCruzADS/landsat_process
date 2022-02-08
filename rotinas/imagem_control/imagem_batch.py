from pathlib import Path

from rotinas.imagem_control.imagem_alg import algCalc
from rotinas.imagem_control.imagem_process import ImagemProcess


class ImagemProcessBatch:
    def __init__(self):
        pass
    
    def procurar_bandas(diretorio: str) -> list:
        """Procura bandas de imagem no diretório

        Args:
            diretorio (str): Path do diretório

        Returns:
            list: Lista com as bandas no diretorio
        """
        lista_de_arquivos = []
        iterar_arquivos = Path(diretorio).iterdir()
        for entrada in iterar_arquivos:
            if entrada.is_file():
                if str(entrada).endswith(".TIF"):
                    bandas = str(entrada).split('_')
                    for banda in bandas:
                        if banda.startswith('B'):
                            lista_de_arquivos.append(str(Path(diretorio, entrada.name)))
        return lista_de_arquivos
    
    def recortar(diretorio_imagem: str, shp: str, diretorio_destino: str):
        """Recorta uma número n de imagens com base num shapefile

        Args:
            diretorio_imagem (str): diretorio da imagem a ser recortada
            shp (str): shapefile correspondente
            diretorio_destino (str): path de destino da imagem recortada
        """
        bandas = ImagemProcessBatch.procurar_bandas(diretorio_imagem)
        for banda in bandas:
           nome_banda = Path(banda).stem
           recorte = ImagemProcess.recortar(banda, shp)
           ImagemProcess.salvar_imagem(recorte, diretorio_destino, nome_banda + '_recortada' + '.TIF')
           
    def reescalar(diretorio_imagem: str, diretorio_destino: str):
        """Reescala imagens no diretório

        Args:
            diretorio_imagem (str): diretório da imagem
            diretorio_destino (str): diretório de destino das imagens reescaladas
        """
        bandas = ImagemProcessBatch.procurar_bandas(diretorio_imagem)
        
        for banda in bandas:
            nome_banda = Path(banda).stem
            imagem_reescalada = algCalc.reescalar(banda)
            ImagemProcess.salvar_imagem(imagem_reescalada, diretorio_destino, nome_banda + '_reescalonada' + '.TIF')
           
    
    def aplicar_algoritmos(diretorio: str, diretorio_destino: str):
        """Aplica algoritmos em imagens já reescalonadas

        Args:
            diretorio (str): diretorio das imagens
            diretorio_destino (str): diretorio de destino dos produtos
        """
        
        iterar_dir = list(Path(diretorio).iterdir())
        bandas_reescalonadas = [str(x) for x in iterar_dir if 'reescalonada' in str(x)]
        
        for banda in bandas_reescalonadas:
           nome_banda = Path(banda).stem
           
           tss = algCalc.tss(banda)
           ImagemProcess.salvar_imagem(tss, diretorio_destino, nome_banda + '_TSS' + ".TIF")
           
           tsi = algCalc.tsi(banda)
           ImagemProcess.salvar_imagem(tsi, diretorio_destino, nome_banda + '_TSI' + ".TIF")
           
    
            
    















