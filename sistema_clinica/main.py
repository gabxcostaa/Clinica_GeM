from sistema_clinica.dados import (opcoes_menu_inicial,opcoes_menu_pricipal,opcoes_menu_crud_pessoa,opcoes_menu_crud_consulta)
from sistema_clinica.funcoes_auxiliares import limpa_tela, sair,sobre
from sistema_clinica.funcoes_crud import adicionar_pessoa,adicionar_consulta,ver_tabela,ver_tabela_consulta,ver_tabela,buscar_pessoa,buscar_consulta,remover_pessoa,remover_consulta,atualizar_consulta
from sistema_clinica.manipulacao_json import inicializar_dados_ao_abrir_o_app
import time

# MENUS #

def menu_inicial():
    while True:
        funcoes = [menu_principal,sobre, sair]
        criar_menu(opcoes_menu_inicial, funcoes, "\n🏥 Consultas Médicas G&M\n")

def menu_principal():
    while True:
        funcoes = [lambda: menu_crud("paciente"),lambda: menu_crud("médico"),menu_consultas,menu_inicial]
        criar_menu(opcoes_menu_pricipal, funcoes, "\n📋 Menu Principal\n")

def menu_consultas():
     while True:
        funcoes = [adicionar_consulta,ver_tabela_consulta,remover_consulta,buscar_consulta,atualizar_consulta,menu_principal]
        criar_menu(opcoes_menu_crud_consulta,funcoes,"\n📅 Gerenciar Consulta\n")

def menu_crud(tipo):
    while True:
        emoji = "👤" if tipo == "paciente" else "🩺"
        titulo = f"\n{emoji} Gerenciar {tipo.capitalize()}\n"

        funcoes = [lambda: adicionar_pessoa(tipo),lambda: ver_tabela(tipo),lambda: remover_pessoa(tipo),lambda: buscar_pessoa(tipo),menu_principal]
        criar_menu(opcoes_menu_crud_pessoa, funcoes, titulo)

def exibir_opcoes(lista):
    for numero, opcao in enumerate(lista, start=1):
        print(f"[{numero}] {opcao}")

def criar_menu(lista, funcoes, titulo):
    while True:
        print(titulo)
        exibir_opcoes(lista)
        escolha_str = input("\n💡 Escolha uma opção: ").strip()
        limpa_tela()

        if escolha_str.isdigit():
            escolha = int(escolha_str)

            if 1 <= escolha <= len(funcoes):
                funcoes[escolha - 1]()
                break
            else:
                print(f"❌ Escolha de 1 a {len(funcoes)}.")
        else:
            print("❌ Digite apenas números.")

        time.sleep(2)
        limpa_tela()

if __name__ == "__main__":
    inicializar_dados_ao_abrir_o_app()
    menu_inicial()