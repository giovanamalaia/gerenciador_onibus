import unittest
import json

from cadastro import (
    salvar_dados,
    carregar_dados,
    cadastrar_ponto,
    remover_ponto,
    consultar_ponto,
    cadastrar_linha,
    adicionar_pontos_linha,
    remover_pontos_linha,
    consultar_linha,
    remover_linha
)

class TestCadastro(unittest.TestCase):

    def setUp(self):
        global pontos, linhas
        pontos = []
        linhas = []
        with open("cadastro.json", "w") as file:
            json.dump({"pontos": [], "linhas": []}, file)
        carregar_dados()

    # Pontos
    def test_cadastrar_ponto_valido(self):
        resultado = cadastrar_ponto("Ponto A")
        self.assertEqual(resultado, ("Ponto cadastrado com sucesso! ID: 1", 1))

    def test_cadastrar_ponto_duplicado(self):
        cadastrar_ponto("Ponto A")
        resultado = cadastrar_ponto("Ponto A")
        self.assertEqual(resultado, ("Erro: Ponto já cadastrado.", 2))

    def test_cadastrar_ponto_invalido(self):
        resultado = cadastrar_ponto("")
        self.assertEqual(resultado, ("Erro: Referência inválida.", 3))

    def test_remover_ponto_existente(self):
        cadastrar_ponto("Ponto A")
        resultado = remover_ponto(1)
        self.assertEqual(resultado, ("Ponto removido com sucesso!", 1))

    def test_remover_ponto_inexistente(self):
        resultado = remover_ponto(99)
        self.assertEqual(resultado, ("Erro: Ponto inexistente.", 2))

    def test_remover_ponto_id_invalido(self):
        resultado = remover_ponto(None)
        self.assertEqual(resultado, ("Erro: ID inválido.", 3))

    def test_consultar_ponto_existente(self):
        cadastrar_ponto("Ponto A")
        resultado = consultar_ponto(1)
        self.assertEqual(
            resultado,
            ("Ponto encontrado: {'id': 1, 'referencia': 'Ponto A'}", 1)
        )

    def test_consultar_ponto_inexistente(self):
        resultado = consultar_ponto(99)
        self.assertEqual(resultado, ("Erro: Ponto inexistente.", 2))

    # Linhas
    def test_cadastrar_linha_valida(self):
        cadastrar_ponto("Ponto A")
        cadastrar_ponto("Ponto B")
        resultado = cadastrar_linha([1, 2])
        self.assertEqual(resultado, ("Linha cadastrada com sucesso! ID: 1", 1))

    def test_cadastrar_linha_sem_pontos(self):
        resultado = cadastrar_linha([])
        self.assertEqual(resultado, ("Erro: A linha não pode ser vazia.", 2))

    def test_cadastrar_linha_com_pontos_invalidos(self):
        resultado = cadastrar_linha([99])
        self.assertEqual(resultado, ("Erro: Um ou mais pontos são inválidos.", 3))

    def test_adicionar_pontos_validos_linha_existente(self):
        cadastrar_ponto("Ponto A")
        cadastrar_ponto("Ponto B")
        cadastrar_linha([1])
        resultado = adicionar_pontos_linha(1, [2])
        self.assertEqual(resultado, ("Pontos adicionados com sucesso!", 1))

    def test_adicionar_pontos_invalidos_linha_existente(self):
        cadastrar_ponto("Ponto A")
        cadastrar_linha([1])
        resultado = adicionar_pontos_linha(1, [99])
        self.assertEqual(resultado, ("Erro: Um ou mais pontos são inválidos.", 2))

    def test_adicionar_pontos_linha_inexistente(self):
        resultado = adicionar_pontos_linha(99, [1])
        self.assertEqual(resultado, ("Erro: Linha inexistente.", 3))

    def test_remover_pontos_validos_linha_existente(self):
        cadastrar_ponto("Ponto A")
        cadastrar_ponto("Ponto B")
        cadastrar_ponto("Ponto C")
        cadastrar_linha([1, 2, 3])
        resultado = remover_pontos_linha(1, [2,3])
        self.assertEqual(resultado, ("Pontos removidos com sucesso!", 1))
        linha, _ = consultar_linha(1)
        self.assertEqual(linha["pontos"], [1])

    def test_remover_pontos_invalidos_linha_existente(self):
        cadastrar_ponto("Ponto A")
        cadastrar_linha([1])
        resultado = remover_pontos_linha(1, [99])
        self.assertEqual(resultado, ("Erro: Um ou mais pontos são inválidos.", 2))

    def test_remover_pontos_linha_inexistente(self):
        resultado = remover_pontos_linha(99, [1])
        self.assertEqual(resultado, ("Erro: Linha inexistente.", 3))

    def test_remover_linha_existente(self):
        cadastrar_ponto("Ponto A")
        cadastrar_linha([1])
        resultado = remover_linha(1)
        self.assertEqual(resultado, ("Linha removida com sucesso!", 1))

    def test_remover_linha_inexistente(self):
        resultado = remover_linha(99)
        self.assertEqual(resultado, ("Erro: Linha inexistente.", 2))

    def test_consultar_linha_existente(self):
        cadastrar_ponto("Ponto A")
        cadastrar_linha([1])
        linha, codigo = consultar_linha(1)
        self.assertEqual(linha["pontos"], [1])
        self.assertEqual(codigo, 1)

    def test_consultar_linha_inexistente(self):
        resultado = consultar_linha(99)
        self.assertEqual(resultado, ("Erro: Linha inexistente.", 2))

if __name__ == "__main__":
    unittest.main()
