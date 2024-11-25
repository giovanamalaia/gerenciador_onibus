import unittest
import json
from datetime import datetime

from viagens import (
    carregar_dados_viagens,
    salvar_dados_viagens,
    registrar_viagem,
    consultar_viagem,
    listar_viagens,
    calcula_tempo,
    calcula_passageiros
)

class TestViagens(unittest.TestCase):

    def setUp(self):
        global viagens
        viagens = []
        with open("viagens.json", "w") as file:
            json.dump([], file)
        carregar_dados_viagens()

    def test_registrar_viagem_valida(self):
        resultado = registrar_viagem(
            id_linha=1,
            data_saida="24/11/24",
            horario_saida="08:00",
            data_chegada="24/11/24",
            horario_chegada="10:00",
            numero_passageiros=30
        )
        self.assertEqual(resultado, (1, 1))

    def test_registrar_viagem_invalida_horario(self):
        resultado = registrar_viagem(
            id_linha=1,
            data_saida="24/11/24",
            horario_saida="10:00",
            data_chegada="24/11/24",
            horario_chegada="08:00",
            numero_passageiros=30
        )
        self.assertEqual(resultado, ("Erro: Data e horário de chegada devem ser posteriores aos de saída.", 2))

    def test_registrar_viagem_invalida_data(self):
        resultado = registrar_viagem(
            id_linha=1,
            data_saida="24-11-24",
            horario_saida="08:00",
            data_chegada="24/11/24",
            horario_chegada="10:00",
            numero_passageiros=30
        )
        self.assertEqual(resultado, ("Erro: Data ou horário inválidos. Use o formato DD/MM/AA para datas e HH:MM para horários.", 3))

    def test_consultar_viagem_existente(self):
        registrar_viagem(
            id_linha=1,
            data_saida="24/11/24",
            horario_saida="08:00",
            data_chegada="24/11/24",
            horario_chegada="10:00",
            numero_passageiros=30
        )
        viagem, codigo = consultar_viagem(1)
        self.assertEqual(codigo, 1)
        self.assertEqual(viagem["id_linha"], 1)
        self.assertEqual(viagem["numero_passageiros"], 30)

    def test_consultar_viagem_inexistente(self):
        resultado = consultar_viagem(99)
        self.assertEqual(resultado, ("Erro: Viagem não encontrada.", 2))

    def test_listar_viagens_existentes(self):
        registrar_viagem(
            id_linha=1,
            data_saida="24/11/24",
            horario_saida="08:00",
            data_chegada="24/11/24",
            horario_chegada="10:00",
            numero_passageiros=30
        )
        registrar_viagem(
            id_linha=1,
            data_saida="25/11/24",
            horario_saida="09:00",
            data_chegada="25/11/24",
            horario_chegada="11:00",
            numero_passageiros=40
        )
        viagens, codigo = listar_viagens(1)
        self.assertEqual(codigo, 1)
        self.assertEqual(len(viagens), 2)

    def test_listar_viagens_inexistentes(self):
        resultado = listar_viagens(99)
        self.assertEqual(resultado, ("Erro: Nenhuma viagem registrada para esta linha.", 2))

    def test_calcula_tempo_valido(self):
        registrar_viagem(
            id_linha=1,
            data_saida="24/11/24",
            horario_saida="08:00",
            data_chegada="24/11/24",
            horario_chegada="10:00",
            numero_passageiros=30
        )
        registrar_viagem(
            id_linha=1,
            data_saida="24/11/24",
            horario_saida="12:00",
            data_chegada="24/11/24",
            horario_chegada="14:30",
            numero_passageiros=40
        )
        relatorio, codigo = calcula_tempo(1)
        self.assertEqual(codigo, 1)
        self.assertAlmostEqual(relatorio["média"], 135.0)  # Corrigido para 135.0
        self.assertAlmostEqual(relatorio["mediana"], 135.0)
        self.assertAlmostEqual(relatorio["mínimo"], 120.0)
        self.assertAlmostEqual(relatorio["máximo"], 150.0)


    def test_calcula_tempo_invalido(self):
        resultado = calcula_tempo(99)
        self.assertEqual(resultado, ("Erro: Nenhuma viagem encontrada para esta linha.", 2))

    def test_calcula_passageiros_valido(self):
        registrar_viagem(
            id_linha=1,
            data_saida="24/11/24",
            horario_saida="08:00",
            data_chegada="24/11/24",
            horario_chegada="10:00",
            numero_passageiros=30
        )
        registrar_viagem(
            id_linha=1,
            data_saida="24/11/24",
            horario_saida="12:00",
            data_chegada="24/11/24",
            horario_chegada="14:30",
            numero_passageiros=40
        )
        relatorio, codigo = calcula_passageiros(1)
        self.assertEqual(codigo, 1)
        self.assertAlmostEqual(relatorio["média"], 35.0)
        self.assertEqual(relatorio["mediana"], 35.0)
        self.assertEqual(relatorio["mínimo"], 30)
        self.assertEqual(relatorio["máximo"], 40)

    def test_calcula_passageiros_invalido(self):
        resultado = calcula_passageiros(99)
        self.assertEqual(resultado, ("Erro: Nenhuma viagem encontrada para esta linha.", 2))


if __name__ == "__main__":
    unittest.main()
