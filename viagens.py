import json
from datetime import datetime
import statistics

__all__ = [
    "registrar_viagem",
    "consultar_viagem",
    "listar_viagens",
    "calcula_tempo",
    "calcula_passageiros"
]

viagens = []


# Objetivo: Carregar os dados de viagens do arquivo JSON para memória.
# Acoplamento:
#   - Parâmetros de entrada: Nenhum.
#   - Retorno: Nenhum.
# Assertivas de entrada:
#   - O arquivo "viagens.json" deve existir ou ser tratado como ausente.
# Assertivas de saída:
#   - A lista global 'viagens' é atualizada com os dados do arquivo.
def carregar_dados_viagens():
    global viagens
    try:
        with open("viagens.json", "r") as file:
            viagens = json.load(file)
    except FileNotFoundError:
        viagens = []


# Objetivo: Salvar os dados de viagens no arquivo JSON.
# Acoplamento:
#   - Parâmetros de entrada: Nenhum.
#   - Retorno: Nenhum.
# Assertivas de entrada:
#   - A lista global 'viagens' deve conter dados válidos.
# Assertivas de saída:
#   - Os dados em 'viagens' são salvos em "viagens.json".
def salvar_dados_viagens():
    global viagens
    with open("viagens.json", "w") as file:
        json.dump(viagens, file, indent=4)


# Objetivo: Registrar uma nova viagem com base nas informações fornecidas.
# Acoplamento:
#   - Parâmetros de entrada:
#       - id_linha (int): ID da linha da viagem.
#       - data_saida (str): Data de saída no formato "DD/MM/AA".
#       - horario_saida (str): Horário de saída no formato "HH:MM".
#       - data_chegada (str): Data de chegada no formato "DD/MM/AA".
#       - horario_chegada (str): Horário de chegada no formato "HH:MM".
#       - numero_passageiros (int): Número de passageiros na viagem.
#   - Retorno:
#       - Tupla (mensagem ou ID da viagem: int ou str, código: int).
# Assertivas de entrada:
#   - Os valores de data e horário devem ser válidos e bem formatados.
# Assertivas de saída:
#   - Uma nova viagem é adicionada à lista 'viagens'.
def registrar_viagem(id_linha, data_saida, horario_saida, data_chegada, horario_chegada, numero_passageiros):
    try:
        saida = datetime.strptime(f"{data_saida} {horario_saida}", "%d/%m/%y %H:%M")
        chegada = datetime.strptime(f"{data_chegada} {horario_chegada}", "%d/%m/%y %H:%M")
    except ValueError:
        return "Erro: Data ou horário inválidos. Use o formato DD/MM/AA para datas e HH:MM para horários.", 3

    if chegada <= saida:
        return "Erro: Data e horário de chegada devem ser posteriores aos de saída.", 2

    nova_viagem = {
        "id_viagem": len(viagens) + 1,
        "id_linha": id_linha,
        "data_saida": data_saida,
        "horario_saida": horario_saida,
        "data_chegada": data_chegada,
        "horario_chegada": horario_chegada,
        "numero_passageiros": numero_passageiros
    }
    viagens.append(nova_viagem)
    salvar_dados_viagens()
    return nova_viagem["id_viagem"], 1


# Objetivo: Consultar os detalhes de uma viagem específica pelo ID.
# Acoplamento:
#   - Parâmetros de entrada:
#       - id_viagem (int): ID da viagem a ser consultada.
#   - Retorno:
#       - Tupla (detalhes da viagem: dict ou mensagem: str, código: int).
# Assertivas de entrada:
#   - O ID da viagem deve identificar uma viagem existente.
# Assertivas de saída:
#   - Retorna os detalhes da viagem ou uma mensagem de erro.
def consultar_viagem(id_viagem):
    viagem = next((v for v in viagens if v["id_viagem"] == id_viagem), None)
    if viagem:
        return viagem, 1
    return "Erro: Viagem não encontrada.", 2


# Objetivo: Listar todas as viagens registradas para uma linha específica.
# Acoplamento:
#   - Parâmetros de entrada:
#       - id_linha (int): ID da linha.
#   - Retorno:
#       - Tupla (lista de viagens: list[dict] ou mensagem: str, código: int).
# Assertivas de entrada:
#   - O ID da linha deve ser válido.
# Assertivas de saída:
#   - Retorna uma lista de viagens ou uma mensagem de erro.
def listar_viagens(id_linha):
    viagens_linha = [v for v in viagens if v["id_linha"] == id_linha]
    if viagens_linha:
        return viagens_linha, 1
    return "Erro: Nenhuma viagem registrada para esta linha.", 2


# Objetivo: Calcular estatísticas de tempo dos trajetos de uma linha.
# Acoplamento:
#   - Parâmetros de entrada:
#       - id_linha (int): ID da linha.
#   - Retorno:
#       - Tupla (estatísticas: dict ou mensagem: str, código: int).
# Assertivas de entrada:
#   - O ID da linha deve ser válido.
# Assertivas de saída:
#   - Retorna estatísticas de tempo (média, mediana, mínimo, máximo) ou erro.
def calcula_tempo(id_linha):
    tempos = []
    for viagem in viagens:
        if viagem["id_linha"] == id_linha:
            try:
                saida = datetime.strptime(f"{viagem['data_saida']} {viagem['horario_saida']}", "%d/%m/%y %H:%M")
                chegada = datetime.strptime(f"{viagem['data_chegada']} {viagem['horario_chegada']}", "%d/%m/%y %H:%M")
            except ValueError:
                continue
            tempos.append((chegada - saida).total_seconds() / 60)

    if not tempos:
        return "Erro: Nenhuma viagem encontrada para esta linha.", 2

    return {
        "média": round(statistics.mean(tempos), 2),
        "mediana": round(statistics.median(tempos), 2),
        "mínimo": round(min(tempos), 2),
        "máximo": round(max(tempos), 2)
    }, 1


# Objetivo: Calcular estatísticas do número de passageiros por linha.
# Acoplamento:
#   - Parâmetros de entrada:
#       - id_linha (int): ID da linha.
#   - Retorno:
#       - Tupla (estatísticas: dict ou mensagem: str, código: int).
# Assertivas de entrada:
#   - O ID da linha deve ser válido.
# Assertivas de saída:
#   - Retorna estatísticas de passageiros (média, mediana, mínimo, máximo) ou erro.
def calcula_passageiros(id_linha):
    passageiros = [v["numero_passageiros"] for v in viagens if v["id_linha"] == id_linha]
    if not passageiros:
        return "Erro: Nenhuma viagem encontrada para esta linha.", 2

    return {
        "média": round(statistics.mean(passageiros), 2),
        "mediana": round(statistics.median(passageiros), 2),
        "mínimo": min(passageiros),
        "máximo": max(passageiros)
    }, 1


# Carregar os dados de viagens ao iniciar o módulo.
carregar_dados_viagens()
