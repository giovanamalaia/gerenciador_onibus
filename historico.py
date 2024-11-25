from datetime import datetime
from cadastro import consultar_ponto, consultar_linha
import json

__all__ = [
    "registrar_modificacao",
    "salvar_dados_historico",
    "consultar_historico_linha", 
    "consultar_historico_ponto"
]

listaTipos = ["criação", "alteração", "deleção"]

historico_pontos = []

historico_linhas = []

def carregar_dados():
    global historico_pontos
    global historico_linhas
    try:
        with open("historico.json", "r") as file:
            data = json.load(file)
            historico_pontos = data.get("pontos", [])
            historico_linhas = data.get("linhas", [])
    except:
        historico_pontos = []
        historico_linhas = []

# Objetivo: Persistir as modificações
# Acoplamento:
#   - Parâmetros de entrada: Nenhum
#   - Retorno: Nenhum
# Assertivas de entrada:
#   - As listas globais 'historico_pontos' e 'historico_linhas' devem conter dados válidos.
# Assertivas de saída:
#   - Os dados em 'historico_pontos' e 'historico_linhas' são salvos em "historico.json"
def salvar_dados_historico():
    global historico_pontos
    global historico_linhas
    with open("historico.json", "w") as file:
        json.dump({"pontos": historico_pontos, "linhas": historico_linhas}, file, indent=4)


# Objetivo: Registrar uma modificação sofrida por um ponto ou linha
# Acoplamento:
#   - Parâmetros de entrada:
#       - tipo_modificacao (int): valor que define se a modificação foi de criação, alteração ou deleção.
#       - objeto_alterado (str): "ponto" ou "linha".
#       - id_objeto (int): ID do objeto que foi modificado.
#   - Retorno:
#       - Tupla (mensagem: str, codigo : int)
# Assertivas de entrada:
#   - 'tipo_modificacao' deve ter um valor valido
#   - 'objeto_alterado' deve ser ou "ponto" ou "linha"
#   - 'id_ponto' deve identificar um objeto existente 
# Assertivas de saída:
#   - A modificação é registrada no historico de pontos ou de linhas.
def registrar_modificacao(tipo_modificacao, objeto_alterado, id_objeto):
    if tipo_modificacao not in [0,1,2]:
        return  "Erro: Tipo de modificação inválido.", 3
    
    if objeto_alterado == "ponto":
        msg, codigo = consultar_ponto(id_objeto)
        if codigo == 1:
            historico_pontos.append({'tipo' : tipo_modificacao, "objeto" : objeto_alterado, 'id' : id_objeto, "data": datetime.now().strftime("%Y-%m-%d %H:%M")})
            return "Modificação registrada com sucesso!", 1
        else:
            return msg, codigo
        
    elif objeto_alterado == "linha":
        msg, codigo = consultar_linha(id_objeto)
        if codigo == 1:
            historico_linhas.append({'tipo' : tipo_modificacao, "objeto" : objeto_alterado, 'id' : id_objeto, "data": datetime.now().strftime("%Y-%m-%d %H:%M")})
            return "Modificação registrada com sucesso!", 1
        else:
            return msg, 2
    else:
        return "Erro: Tipo de objeto inválido.", 4
    

# Objetivo: Consultar o historico de alterções de um ponto
# Acoplamento:
#   - Parâmetros de entrada:
#       - id_ponto (int): ID do ponto a ser consultado.
#   - Retorno:
#       - Tupla (mensagem: list ou str, codigo : int)
# Assertivas de entrada:
#   - 'id_ponto' deve identificar um ponto existente 
# Assertivas de saída:
#   - Retorna as alterações sofridas pela ponto ou uma mensagem de erro.
def consultar_historico_ponto(id_ponto):
    resultado = []

    for item in historico_pontos:
        if item.get("id") == id_ponto:
            item["tipo"] = listaTipos[item["tipo"]]
            resultado.append(item) 
    if resultado == []:
        return "Ponto não encontrado no histórico", 2
    else:
        return resultado, 1

# Objetivo: Consultar o historico de alterções de uma linha
# Acoplamento:
#   - Parâmetros de entrada:
#       - id_linha (int): ID da linha a ser consultada.
#   - Retorno:
#       - Tupla (mensagem: list ou str, codigo : int)
# Assertivas de entrada:
#   - 'id_linha' deve identificar uma linha existente 
# Assertivas de saída:
#   - Retorna as alterações sofridas pela linha ou uma mensagem de erro.
def consultar_historico_linha(id_linha):
    resultado = []

    for item in historico_linhas:
        if item.get("id") == id_linha:
            item["tipo"] = listaTipos[item["tipo"]]
            print(item)
            resultado.append(item) 
    if resultado == []:
        return "Linha não encontrada no histórico", 2
    else:
        return resultado, 1

carregar_dados()