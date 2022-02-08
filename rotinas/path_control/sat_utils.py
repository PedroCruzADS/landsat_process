import os
import shutil
from pathlib import Path


class LandsatControl:
    def __init__(self, diretorio_imagem_landsat: str):
        self.diretorio_imagem_landsat = diretorio_imagem_landsat
        self.arquivos_dir = Path(self.diretorio_imagem_landsat).glob('*')
        self.listar_arquivos = [x for x in self.arquivos_dir if str(
            x).endswith(('.TIF', '.xml', '.txt'))]

    def landsat_id(self) -> str:
        """Pega o id de uma cena

        Returns:
            str: ID da cena
        """
        arquivo_base = self.listar_arquivos[0]
        nome_arquivo = arquivo_base.name
        index_t1 = nome_arquivo.find('T1')
        id = nome_arquivo[:index_t1+2]

        return id

    def landsat_dir_control(self) -> Path:
        """Cria diretórios de cena landsat

        Returns:
            Path: Path da cena landsat
        """
        image_id = self.landsat_id()
        path_lc08 = Path(Path.cwd(), 'LC08')
        path_lc08_dir = Path(path_lc08, image_id)
        dirs = [Path(path_lc08_dir, 'original'),
                Path(path_lc08_dir, 'cropped'),
                Path(path_lc08_dir, 'product')]

        try:
            if path_lc08.exists():
                for dir in dirs:
                    if not dir.exists():
                        dir.mkdir(exist_ok=False, parents=True)
                    else:
                        pass
            else:
                path_lc08.mkdir()
                for dir in dirs:
                    dir.mkdir(exist_ok=False, parents=True)

        except FileExistsError:
            pass

        return path_lc08_dir

    def landsat_wd(self) -> tuple:
        """Lista diretórios da cena

        Returns:
            tuple: Retorna uma tupla com os diretórios
        """
        
        list_dir = [Path(self.landsat_dir_control(), subdir)
                    for subdir in os.listdir(self.landsat_dir_control())]
        cropped = list_dir[0]
        original = list_dir[1]
        product = list_dir[2]

        return (original, cropped, product)

    def landsat_org_files(self):
        """Organiza cena landsat por diretórios"""
        
        files_dst_path = self.landsat_wd()[0]
        files_src_list = self.listar_arquivos
        files_dst_list = [x for x in self.landsat_wd()[0].iterdir()]
        files_dst_names = [x.name for x in files_dst_list]

        for file_src in files_src_list:
            if file_src.name in files_dst_names:
                pass
            else:
                shutil.copy(file_src, files_dst_path)
