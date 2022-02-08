from pathlib import Path


def cria_dir(diretorios: list):
    """Cria os diretórios para execução das rotinas
    """
    diretorio_atual = Path.cwd()
    try:
        for dir in diretorios:
            diretorio = Path(diretorio_atual, dir)
            if not diretorio.exists():
                diretorio.mkdir(parents=True)
    finally:
        print("Diretórios criados.")
