def limpar_texto(texto):
    """
    Função para limpar o texto removendo quebras de linha e outros caracteres indesejados.
    Você pode ajustar essa função para remover ou substituir outros caracteres conforme necessário.
    """
    if isinstance(texto, str):
        # Remove quebras de linha e substitui por espaço
        texto_limpo = texto.replace('\n', ' ').replace('\r', ' ').strip()
        # Opcional: remover outros caracteres especiais
        # texto_limpo = re.sub(r'[^\w\s]', '', texto_limpo)
        return texto_limpo
    return texto