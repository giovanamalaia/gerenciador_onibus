import os
import signal
from cadastro import (
    carregar_dados,
    salvar_dados,  
    cadastrar_ponto,
    remover_ponto,
    consultar_ponto,
    cadastrar_linha,
    adicionar_pontos_linha,
    remover_pontos_linha,
    remover_linha,
    consultar_linha
)
from viagens import (
    carregar_dados_viagens,
    salvar_dados_viagens,  
    registrar_viagem,
    consultar_viagem,
    listar_viagens,
    calcula_tempo,
    calcula_passageiros
)
from historico import (
    carregar_dados as carregar_historico,
    salvar_dados_historico,  # Adicionado aqui
    consultar_historico_ponto,
    consultar_historico_linha
)


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nPressione Enter para continuar...")

def salvar_todos_os_dados():
    print("\nSalvando todos os dados...")
    salvar_dados()
    salvar_dados_viagens()
    salvar_dados_historico()
    print("Dados salvos com sucesso!")

def signal_handler(sig, frame):
    print("\nSinal recebido! Salvando dados antes de encerrar...")
    salvar_todos_os_dados()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # Fechamento do terminal

def menu_principal():
    while True:
        clear_console()
        print("=== Gerenciador de Linhas de Ônibus ===")
        print("1. Gerenciar Pontos de Parada")
        print("2. Gerenciar Linhas de Ônibus")
        print("3. Registro de Viagens")
        print("4. Histórico de Modificações")
        print("5. Estatísticas de Linhas")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_pontos()
        elif opcao == "2":
            menu_linhas()
        elif opcao == "3":
            menu_viagens()
        elif opcao == "4":
            menu_historico()
        elif opcao == "5":
            menu_estatisticas()
        elif opcao == "6":
            print("Finalizando o programa e salvando os dados...")
            salvar_todos_os_dados()
            break
        else:
            print("Opção inválida.")
            pause()

def menu_pontos():
    while True:
        clear_console()
        print("=== Gerenciar Pontos de Parada ===")
        print("1. Cadastrar Ponto")
        print("2. Consultar Ponto")
        print("3. Remover Ponto")
        print("4. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            referencia = input("Digite a referência do ponto: ")
            msg, codigo = cadastrar_ponto(referencia)
            print(msg)
            pause()
        elif opcao == "2":
            try:
                ponto_id = int(input("Digite o ID do ponto: "))
                msg, codigo = consultar_ponto(ponto_id)
                print(msg)
            except ValueError:
                print("ID inválido.")
            pause()
        elif opcao == "3":
            try:
                ponto_id = int(input("Digite o ID do ponto: "))
                msg, codigo = remover_ponto(ponto_id)
                print(msg)
            except ValueError:
                print("ID inválido.")
            pause()
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")
            pause()

def menu_linhas():
    while True:
        clear_console()
        print("=== Gerenciar Linhas de Ônibus ===")
        print("1. Cadastrar Linha")
        print("2. Consultar Linha")
        print("3. Adicionar Pontos à Linha")
        print("4. Remover Pontos da Linha")
        print("5. Remover Linha")
        print("6. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                lista_pontos = list(map(int, input("Digite os IDs dos pontos separados por vírgula: ").split(",")))
                msg, codigo = cadastrar_linha(lista_pontos)
                print(msg)
            except ValueError:
                print("Entrada inválida.")
            pause()
        elif opcao == "2":
            try:
                linha_id = int(input("Digite o ID da linha: "))
                msg, codigo = consultar_linha(linha_id)
                print(msg)
            except ValueError:
                print("ID inválido.")
            pause()
        elif opcao == "3":
            try:
                linha_id = int(input("Digite o ID da linha: "))
                lista_pontos = list(map(int, input("Digite os IDs dos pontos separados por vírgula: ").split(",")))
                msg, codigo = adicionar_pontos_linha(linha_id, lista_pontos)
                print(msg)
            except ValueError:
                print("Entrada inválida.")
            pause()
        elif opcao == "4":
            try:
                linha_id = int(input("Digite o ID da linha: "))
                lista_pontos = list(map(int, input("Digite os IDs dos pontos separados por vírgula: ").split(",")))
                msg, codigo = remover_pontos_linha(linha_id, lista_pontos)
                print(msg)
            except ValueError:
                print("Entrada inválida.")
            pause()
        elif opcao == "5":
            try:
                linha_id = int(input("Digite o ID da linha: "))
                msg, codigo = remover_linha(linha_id)
                print(msg)
            except ValueError:
                print("ID inválido.")
            pause()
        elif opcao == "6":
            break
        else:
            print("Opção inválida.")
            pause()

def menu_viagens():
    while True:
        clear_console()
        print("=== Registro de Viagens ===")
        print("1. Registrar Viagem")
        print("2. Consultar Viagem")
        print("3. Listar Viagens")
        print("4. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                id_linha = int(input("ID da linha: "))
                data_saida = input("Data de saída (DD/MM/AA): ")
                horario_saida = input("Horário de saída (HH:MM): ")
                data_chegada = input("Data de chegada (DD/MM/AA): ")
                horario_chegada = input("Horário de chegada (HH:MM): ")
                numero_passageiros = int(input("Número de passageiros: "))
                msg, codigo = registrar_viagem(id_linha, data_saida, horario_saida, data_chegada, horario_chegada, numero_passageiros)
                print(msg)
            except ValueError:
                print("Entrada inválida.")
            pause()
        elif opcao == "2":
            try:
                id_viagem = int(input("Digite o ID da viagem: "))
                msg, codigo = consultar_viagem(id_viagem)
                print(msg)
            except ValueError:
                print("ID inválido.")
            pause()
        elif opcao == "3":
            try:
                id_linha = int(input("Digite o ID da linha: "))
                viagens, codigo = listar_viagens(id_linha)
                if codigo == 1:
                    print("\n=== Viagens da Linha ===")
                    for viagem in viagens:
                        print(f"- ID da Viagem: {viagem['id_viagem']}")
                        print(f"  Data e Hora de Saída: {viagem['data_saida']} às {viagem['horario_saida']}")
                        print(f"  Data e Hora de Chegada: {viagem['data_chegada']} às {viagem['horario_chegada']}")
                        print(f"  Número de Passageiros: {viagem['numero_passageiros']}\n")
                else:
                    print(viagens)
            except ValueError:
                print("ID inválido.")
            pause()
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")
            pause()

def menu_historico():
    while True:
        clear_console()
        print("=== Histórico de Modificações ===")
        print("1. Consultar Histórico de Pontos")
        print("2. Consultar Histórico de Linhas")
        print("3. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                id_ponto = int(input("Digite o ID do ponto: "))
                historico, codigo = consultar_historico_ponto(id_ponto)
                if codigo == 1:
                    print(f"\nHistórico de Modificações do Ponto ID {id_ponto}:")
                    for item in historico:
                        print(f" - Tipo: {item['tipo']}, Data: {item['data']}")
                else:
                    print(historico)
            except ValueError:
                print("ID inválido.")
            pause()
        elif opcao == "2":
            try:
                id_linha = int(input("Digite o ID da linha: "))
                historico, codigo = consultar_historico_linha(id_linha)
                if codigo == 1:
                    print(f"\nHistórico de Modificações da Linha ID {id_linha}:")
                    for item in historico:
                        print(f" - Tipo: {item['tipo']}, Data: {item['data']}")
                else:
                    print(historico)
            except ValueError:
                print("ID inválido.")
            pause()
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")
            pause()

def menu_estatisticas():
    while True:
        clear_console()
        print("=== Estatísticas de Linhas ===")
        print("1. Tempo Médio de Trajeto")
        print("2. Número Médio de Passageiros")
        print("3. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                id_linha = int(input("Digite o ID da linha: "))
                estatisticas, codigo = calcula_tempo(id_linha)
                if codigo == 1:
                    print("\n=== Estatísticas de Tempo de Trajeto ===")
                    print(f"- Tempo Médio: {estatisticas['média']} minutos")
                    print(f"- Tempo Mediano: {estatisticas['mediana']} minutos")
                    print(f"- Tempo Mínimo: {estatisticas['mínimo']} minutos")
                    print(f"- Tempo Máximo: {estatisticas['máximo']} minutos")
                else:
                    print(estatisticas)
            except ValueError:
                print("ID inválido.")
            pause()
        elif opcao == "2":
            try:
                id_linha = int(input("Digite o ID da linha: "))
                estatisticas, codigo = calcula_passageiros(id_linha)
                if codigo == 1:
                    print("\n=== Estatísticas de Passageiros ===")
                    print(f"- Média de Passageiros: {estatisticas['média']}")
                    print(f"- Mediana de Passageiros: {estatisticas['mediana']}")
                    print(f"- Número Mínimo de Passageiros: {estatisticas['mínimo']}")
                    print(f"- Número Máximo de Passageiros: {estatisticas['máximo']}")
                else:
                    print(estatisticas)
            except ValueError:
                print("ID inválido.")
            pause()
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")
            pause()


# Inicialização do sistema
if __name__ == "__main__":
    carregar_dados()
    carregar_dados_viagens()
    carregar_historico()
    menu_principal()
