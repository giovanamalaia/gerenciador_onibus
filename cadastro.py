import json

__all__ = [
    "cadastrar_ponto",
    "remover_ponto",
    "cadastrar_linha",
    "adicionar_pontos_linha",
    "remover_pontos_linha",
    "remover_linha",
    "consultar_ponto",
    "consultar_linha"
]

# Dados encapsulados
pontos = []
linhas = []


# Objetivo: Carregar os dados de pontos e linhas do arquivo JSON para memória.
# Acoplamento:
#   - Parâmetros de entrada: Nenhum.
#   - Retorno: Nenhum.
# Assertivas de entrada:
#   - O arquivo "cadastro.json" deve existir ou ser tratado como ausente.
# Assertivas de saída:
#   - As listas globais 'pontos' e 'linhas' são atualizadas com os dados do arquivo.
def carregar_dados():
    global pontos, linhas
    try:
        with open("cadastro.json", "r") as file:
            data = json.load(file)
            pontos = data.get("pontos", [])
            linhas = data.get("linhas", [])
    except FileNotFoundError:
        pontos = []
        linhas = []


# Objetivo: Salvar os dados de pontos e linhas no arquivo JSON.
# Acoplamento:
#   - Parâmetros de entrada: Nenhum.
#   - Retorno: Nenhum.
# Assertivas de entrada:
#   - As listas globais 'pontos' e 'linhas' devem conter dados válidos.
# Assertivas de saída:
#   - Os dados em 'pontos' e 'linhas' são salvos em "cadastro.json".
def salvar_dados():
    global pontos, linhas
    pontos = list({p['id']: p for p in pontos}.values())
    linhas = list({l['id']: l for l in linhas}.values())
    with open("cadastro.json", "w") as file:
        json.dump({"pontos": pontos, "linhas": linhas}, file, indent=4)


# Objetivo: Cadastrar um novo ponto de ônibus.
# Acoplamento:
#   - Parâmetros de entrada:
#       - referencia (str): Referencia do ponto a ser cadastrado.
#   - Retorno:
#       - Tupla (mensagem: str, código: int).
# Assertivas de entrada:
#   - 'referencia' deve ser uma string não vazia.
# Assertivas de saída:
#   - Um novo ponto é adicionado à lista 'pontos'.
def cadastrar_ponto(referencia):
    if not referencia.strip():
        return "Erro: Referência inválida.", 3
    if any(ponto['referencia'] == referencia for ponto in pontos):
        return "Erro: Ponto já cadastrado.", 2
    novo_id = max([p['id'] for p in pontos], default=0) + 1
    novo_ponto = {"id": novo_id, "referencia": referencia}
    pontos.append(novo_ponto)
    from historico import registrar_modificacao
    registrar_modificacao(0, "ponto", novo_id)  # 0 = criação
    return f"Ponto cadastrado com sucesso! ID: {novo_ponto['id']}", 1


# Objetivo: Remover um ponto de ônibus existente.
# Acoplamento:
#   - Parâmetros de entrada:
#       - ponto_id (int): ID do ponto a ser removido.
#   - Retorno:
#       - Tupla (mensagem: str, código: int).
# Assertivas de entrada:
#   - 'ponto_id' deve ser um número inteiro positivo.
# Assertivas de saída:
#   - O ponto é removido da lista 'pontos' e de todas as linhas.
def remover_ponto(ponto_id):
    if not isinstance(ponto_id, int) or ponto_id <= 0:
        return "Erro: ID inválido.", 3
    ponto = next((p for p in pontos if p['id'] == ponto_id), None)
    if ponto:
        # Remover o ponto da lista de pontos
        pontos.remove(ponto)

        # Remover o ponto de todas as linhas que o contenham
        for linha in linhas:
            if ponto_id in linha["pontos"]:
                linha["pontos"].remove(ponto_id)

        # Registrar a modificação no histórico
        from historico import registrar_modificacao
        registrar_modificacao(2, "ponto", ponto_id)  # 2 = deleção
        return "Ponto removido com sucesso!", 1
    return "Erro: Ponto inexistente.", 2




# Objetivo: Consultar as informações de um ponto de ônibus por ID.
# Acoplamento:
#   - Parâmetros de entrada:
#       - ponto_id (int): ID do ponto a ser consultado.
#   - Retorno:
#       - Tupla (mensagem: dict ou str, código: int).
# Assertivas de entrada:
#   - 'ponto_id' deve identificar um ponto existente.
# Assertivas de saída:
#   - Retorna as informações do ponto ou uma mensagem de erro.
def consultar_ponto(ponto_id):
    ponto = next((p for p in pontos if p["id"] == ponto_id), None)
    if ponto:
        return f"Ponto encontrado: {ponto}", 1
    return "Erro: Ponto inexistente.", 2


# Objetivo: Cadastrar uma nova linha de ônibus com pontos válidos.
# Acoplamento:
#   - Parâmetros de entrada:
#       - lista_pontos (list[int]): IDs dos pontos que compõem a linha.
#   - Retorno:
#       - Tupla (mensagem: str, código: int).
# Assertivas de entrada:
#   - 'lista_pontos' deve conter IDs válidos.
# Assertivas de saída:
#   - Uma nova linha é adicionada à lista 'linhas'.
def cadastrar_linha(lista_pontos):
    if not lista_pontos:
        return "Erro: A linha não pode ser vazia.", 2
    pontos_existentes = [p["id"] for p in pontos]
    if not all(p in pontos_existentes for p in lista_pontos):
        return "Erro: Um ou mais pontos são inválidos.", 3
    novo_id = max([l['id'] for l in linhas], default=0) + 1
    nova_linha = {"id": novo_id, "pontos": lista_pontos.copy()}
    linhas.append(nova_linha)
    from historico import registrar_modificacao
    registrar_modificacao(0, "linha", novo_id)  # 0 = criação
    return f"Linha cadastrada com sucesso! ID: {nova_linha['id']}", 1


# Objetivo: Adicionar pontos a uma linha de ônibus existente.
# Acoplamento:
#   - Parâmetros de entrada:
#       - linha_id (int): ID da linha.
#       - lista_pontos (list[int]): IDs dos pontos a serem adicionados.
#   - Retorno:
#       - Tupla (mensagem: str, código: int).
# Assertivas de entrada:
#   - 'linha_id' deve identificar uma linha existente.
#   - 'lista_pontos' deve conter IDs válidos.
# Assertivas de saída:
#   - Os pontos são adicionados à lista de pontos da linha.
def adicionar_pontos_linha(linha_id, lista_pontos):
    linha = next((l for l in linhas if l["id"] == linha_id), None)
    if not linha:
        return "Erro: Linha inexistente.", 3
    pontos_existentes = [p["id"] for p in pontos]
    if not all(p in pontos_existentes for p in lista_pontos):
        return "Erro: Um ou mais pontos são inválidos.", 2
    linha["pontos"].extend(p for p in lista_pontos if p not in linha["pontos"])
    from historico import registrar_modificacao
    registrar_modificacao(1, "linha", linha_id)  # 1 = alteração
    return "Pontos adicionados com sucesso!", 1


# Objetivo: Remover pontos de uma linha de ônibus existente.
# Acoplamento:
#   - Parâmetros de entrada:
#       - linha_id (int): ID da linha.
#       - lista_pontos (list[int]): IDs dos pontos a serem removidos.
#   - Retorno:
#       - Tupla (mensagem: str, código: int).
# Assertivas de entrada:
#   - 'linha_id' deve identificar uma linha existente.
#   - 'lista_pontos' deve conter IDs válidos.
# Assertivas de saída:
#   - Os pontos são removidos da lista de pontos da linha.
def remover_pontos_linha(linha_id, lista_pontos):
    linha = next((l for l in linhas if l["id"] == linha_id), None)
    if not linha:
        return "Erro: Linha inexistente.", 3
    pontos_existentes = [p["id"] for p in pontos]
    if not all(p in pontos_existentes for p in lista_pontos):
        return "Erro: Um ou mais pontos são inválidos.", 2
    linha["pontos"] = [p for p in linha["pontos"] if p not in lista_pontos]
    from historico import registrar_modificacao
    registrar_modificacao(1, "linha", linha_id)  # 1 = alteração
    return "Pontos removidos com sucesso!", 1


# Objetivo: Remover uma linha de ônibus existente.
# Acoplamento:
#   - Parâmetros de entrada:
#       - linha_id (int): ID da linha a ser removida.
#   - Retorno:
#       - Tupla (mensagem: str, código: int).
# Assertivas de entrada:
#   - 'linha_id' deve ser um número inteiro positivo.
# Assertivas de saída:
#   - A linha é removida da lista 'linhas'.
def remover_linha(linha_id):
    linha = next((l for l in linhas if l["id"] == linha_id), None)
    if linha:
        linhas.remove(linha)
        from historico import registrar_modificacao
        registrar_modificacao(2, "linha", linha_id)  # 2 = deleção
        return "Linha removida com sucesso!", 1
    return "Erro: Linha inexistente.", 2


# Objetivo: Consultar as informações de uma linha de ônibus por ID.
# Acoplamento:
#   - Parâmetros de entrada:
#       - linha_id (int): ID da linha a ser consultada.
#   - Retorno:
#       - Tupla (mensagem: dict ou str, código: int).
# Assertivas de entrada:
#   - 'linha_id' deve identificar uma linha existente.
# Assertivas de saída:
#   - Retorna as informações da linha ou uma mensagem de erro.
def consultar_linha(linha_id):
    linha = next((l for l in linhas if l["id"] == linha_id), None)
    if linha:
        return {"id": linha["id"], "pontos": linha["pontos"]}, 1
    return "Erro: Linha inexistente.", 2
