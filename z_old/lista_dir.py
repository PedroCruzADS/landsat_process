from pathlib import Path


def lista_dir() -> str:
    """Função que lista os diretórios pré-criados

    Returns:
        str: retorna os caminhos dos diretórios
    """
    diretorio_atual = Path.cwd()
    subdiretorios = []

    for path in diretorio_atual.iterdir():
        if not path.is_file():
            if not str(path).endswith('.git'):
                if not str(path).endswith('rotinas'):
                    if not str(path).endswith('rotinas_batch'):
                        subdiretorios.append(str(path))
    return subdiretorios
