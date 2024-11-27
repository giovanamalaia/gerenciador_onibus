import unittest
from unittest.mock import patch
from datetime import datetime
import json

from historico import registrar_modificacao, consultar_historico_ponto, consultar_historico_linha, historico_pontos, historico_linhas

class TestModificacoes(unittest.TestCase):
    def setUp(self):
        historico_pontos.clear()
        historico_linhas.clear()

    # Teste para registrar modificação de ponto com sucesso
    @patch('cadastro.consultar_ponto')  # Mock para a função consultar_ponto
    def test_registrar_modificacao_ponto_sucesso(self, mock_consultar_ponto):
        # Configuração do mock
        mock_consultar_ponto.return_value = ("Ponto encontrado.", 1)
        
        tipo_modificacao = 0  # "criação"
        objeto_alterado = "ponto"
        id_objeto = 1
        
        # Chama a função registrar_modificacao
        mensagem, codigo = registrar_modificacao(tipo_modificacao, objeto_alterado, id_objeto)
        
        # Verificando as mensagens e o código
        self.assertEqual(mensagem, "Modificação registrada com sucesso!")
        self.assertEqual(codigo, 1)
        
        # Verificando se a modificação foi registrada corretamente no histórico
        self.assertEqual(len(historico_pontos), 1)  # Esperamos que o histórico de pontos tenha 1 item
        self.assertEqual(historico_pontos[0]['tipo'], tipo_modificacao)
        self.assertEqual(historico_pontos[0]['objeto'], objeto_alterado)
        self.assertEqual(historico_pontos[0]['id'], id_objeto)

    # Teste para registrar modificação de ponto com tipo inválido
    @patch('cadastro.consultar_ponto')  # Mock para a função consultar_ponto
    def test_registrar_modificacao_ponto_tipo_invalido(self, mock_consultar_ponto):
        # Tipo de modificação inválido
        tipo_modificacao = 5  # Inexistente
        objeto_alterado = "ponto"
        id_objeto = 1
        
        # Chama a função registrar_modificacao
        mensagem, codigo = registrar_modificacao(tipo_modificacao, objeto_alterado, id_objeto)
        
        # Verificando o erro
        self.assertEqual(mensagem, "Erro: Tipo de modificação inválido.")
        self.assertEqual(codigo, 3)

    # Teste para registrar modificação de ponto com ponto não encontrado
    @patch('cadastro.consultar_ponto')  # Mock para a função consultar_ponto
    def test_registrar_modificacao_ponto_nao_encontrado(self, mock_consultar_ponto):
        # Configuração do mock para erro
        mock_consultar_ponto.return_value = ("Ponto não encontrado.", 2)
        
        tipo_modificacao = 0  # "criação"
        objeto_alterado = "ponto"
        id_objeto = 1
        
        # Chama a função registrar_modificacao
        mensagem, codigo = registrar_modificacao(tipo_modificacao, objeto_alterado, id_objeto)
        
        # Verificando o erro
        self.assertEqual(mensagem, "Ponto não encontrado.")
        self.assertEqual(codigo, 2)

    # Teste para registrar modificação de linha com sucesso
    @patch('cadastro.consultar_linha')  # Mock para a função consultar_linha
    def test_registrar_modificacao_linha_sucesso(self, mock_consultar_linha):
        # Configuração do mock
        mock_consultar_linha.return_value = ("Linha encontrada.", 1)
        
        tipo_modificacao = 1  # "alteração"
        objeto_alterado = "linha"
        id_objeto = 2
        
        # Chama a função registrar_modificacao
        mensagem, codigo = registrar_modificacao(tipo_modificacao, objeto_alterado, id_objeto)
        
        # Verificando as mensagens e o código
        self.assertEqual(mensagem, "Modificação registrada com sucesso!")
        self.assertEqual(codigo, 1)
        
        # Verificando se a modificação foi registrada corretamente no histórico
        self.assertEqual(len(historico_linhas), 1)  # Esperamos que o histórico de linhas tenha 1 item
        self.assertEqual(historico_linhas[0]['tipo'], tipo_modificacao)
        self.assertEqual(historico_linhas[0]['objeto'], objeto_alterado)
        self.assertEqual(historico_linhas[0]['id'], id_objeto)

    # Teste para registrar modificação de linha com linha não encontrada
    @patch('cadastro.consultar_linha')  # Mock para a função consultar_linha
    def test_registrar_modificacao_linha_nao_encontrado(self, mock_consultar_linha):
        # Configuração do mock para erro
        mock_consultar_linha.return_value = ("Linha não encontrada.", 2)
        
        tipo_modificacao = 1  # "alteração"
        objeto_alterado = "linha"
        id_objeto = 2
        
        # Chama a função registrar_modificacao
        mensagem, codigo = registrar_modificacao(tipo_modificacao, objeto_alterado, id_objeto)
        
        # Verificando o erro
        self.assertEqual(mensagem, "Linha não encontrada.")
        self.assertEqual(codigo, 2)

    def test_registrar_modificacao_objeto_invalido(self):
        
        tipo_modificacao = 1  # "alteração"
        objeto_alterado = "Viagem"
        id_objeto = 2
        
        # Chama a função registrar_modificacao
        mensagem, codigo = registrar_modificacao(tipo_modificacao, objeto_alterado, id_objeto)
        
        # Verificando o erro
        self.assertEqual(mensagem, 'Erro: Tipo de objeto inválido.')
        self.assertEqual(codigo, 4)

    # Teste para consultar histórico de ponto com sucesso
    def test_consultar_historico_ponto_sucesso(self):
        # Simula o histórico de pontos com um ponto
        historico_pontos.append({'tipo': 0, 'objeto': 'ponto', 'id': 1, 'data': datetime.now().strftime("%Y-%m-%d %H:%M")})
        
        resultado, codigo = consultar_historico_ponto(1)
        
        # Verificando os resultados
        self.assertEqual(codigo, 1)
        self.assertTrue(isinstance(resultado, list))
        self.assertEqual(len(resultado), 1)

    # Teste para consultar histórico de ponto quando não encontrado
    def test_consultar_historico_ponto_nao_encontrado(self):
        resultado, codigo = consultar_historico_ponto(999)  # ID que não existe
        
        # Verificando o erro
        self.assertEqual(resultado, "Ponto não encontrado no histórico")
        self.assertEqual(codigo, 2)

    # Teste para consultar histórico de linha com sucesso
    def test_consultar_historico_linha_sucesso(self):
        # Simula o histórico de linhas com uma linha
        historico_linhas.append({'tipo': 1, 'objeto': 'linha', 'id': 2, 'data': datetime.now().strftime("%Y-%m-%d %H:%M")})
        
        resultado, codigo = consultar_historico_linha(2)
        
        # Verificando os resultados
        self.assertEqual(codigo, 1)
        self.assertTrue(isinstance(resultado, list))
        self.assertEqual(len(resultado), 1)

    # Teste para consultar histórico de linha quando não encontrado
    def test_consultar_historico_linha_nao_encontrado(self):
        resultado, codigo = consultar_historico_linha(999)  # ID que não existe
        
        # Verificando o erro
        self.assertEqual(resultado, "Linha não encontrada no histórico")
        self.assertEqual(codigo, 2)

if __name__ == '__main__':
    unittest.main()
