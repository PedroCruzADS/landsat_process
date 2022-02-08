from pathlib import Path

def listar_bandas(diretorio_de_imagens: str) -> list:
    """Lista as bandas existentes no diretório de imagens

    Args:
        diretorio_de_imagens (Path): diretório de imagens onde serão filtradas as bandas

    Returns:
        list: retorna uma lista com as bandas
    """
    
    lista_de_arquivos = []
    iterar_arquivos = Path(diretorio_de_imagens).iterdir()
    for entrada in iterar_arquivos:
        if entrada.is_file():
            if str(entrada).endswith(".TIF"):
                bandas = str(entrada).split('_')
                for banda in bandas:
                    if banda.startswith('B'):
                        lista_de_arquivos.append(str(Path(diretorio_de_imagens, entrada.name)))
    return lista_de_arquivos
