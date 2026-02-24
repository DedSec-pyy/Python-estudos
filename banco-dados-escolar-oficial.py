"""
SISTEMA DE BANCO DE DADOS ESCOLAR
V1.2

By: DedSec-pyy (2026)

"""

import json
import os
import hashlib

geral = list()
usuarios = dict()

def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def carregar_usuarios():
    global usuarios
    if os.path.isfile('usuarios.json'):
        try:
            with open('usuarios.json', 'r', encoding='utf-8') as users:
                usuarios = json.load(users)
        except:
            usuarios = dict()
    else:
        usuarios = dict()

def salvar_usuarios():
    with open('usuarios.json', 'w', encoding='utf-8') as saveusers:
        json.dump(usuarios, saveusers, indent=4)

def registrar():
    print('====REGISTRO====')
    username = input('Digite seu nome: ').strip()
    if username in usuarios:
        print('\033[31mUSUÁRIO JÁ CADASTRADO.\033[m')
        return

    senha = input('Digite sua senha: ').strip()
    while True:
        tipo = input('Cadastrar como: [admin/user] ').strip().lower()
        if tipo in ["admin", "user"]:
            break
        else:
            print("\033[31mOPÇÃO INVÁLIDA! TENTE NOVAMENTE.\033[m")

    usuarios[username] = {"senha": gerar_hash(senha), "tipo": tipo}

    salvar_usuarios()
    print('\033[32mUSUÁRIO REGISTRADO COM SUCESSO!\033[m')

def login_sistema():
    print('====LOGIN====')
    username = input('Digite seu nome: ').strip()
    senha = input('Digite sua senha: ').strip()

    senha_hash = gerar_hash(senha)

    if username in usuarios and usuarios[username]["senha"] == senha_hash:
        print('\033[32mLOGADO COM SUCESSO!\033[m')
        return username, usuarios[username]["tipo"]
    else:
        print('\033[31mCREDENCIAIS INVÁLIDAS!\033[m')
        return None, None

def salvar_arquivo():
    with open('geral.json', 'w', encoding='utf-8') as dadosescolares:
        json.dump(geral, dadosescolares, ensure_ascii=False, indent=4)

def carregar_dados():
    global geral

    if os.path.exists('geral.json'):
        try:
            with open('geral.json', 'r', encoding='utf-8') as dadosescolares:
                geral = json.load(dadosescolares)

                if not isinstance(geral, list):
                    print('\033[31mARQUIVO INVÁLIDO!\n\n RESETANDO BANCO...\033[m\n')
                    geral = []

        except json.JSONDecodeError:
            print('\033[31mARQUIVO CORROMPIDO!\n\n CRIANDO NOVO BANCO...\n\033[m')
            geral = []
            salvar_arquivo()

        except Exception as erro:
            print(f'\033[31mERRO INESPERADO:\033[m \033[32m{erro}!\033[m')
            geral = []
    else:
        geral = []
        salvar_arquivo()

carregar_dados()

def cadastrar():
    alunos = dict()
    while True:
        nome = input('Nome do aluno: ').strip().upper()
        if nome.replace(' ', '').isalpha():
            alunos['aluno'] = nome
            if any(aluno['aluno'] == nome for aluno in geral):
                print('\033[31mNOME JÁ CADASTRADO! TENTE NOVAMENTE.\033[m')
                continue
            else:
                break
        else:
            print('\033[31mNOME INVÁLIDO! TENTE NOVAMENTE.\033[m')
            continue

    controle3 = True
    while controle3:
        notas = list()
        while True:
            try:
                total = int(input('Quantas notas quer cadastrar?: [1-10]'))
                if 1 <= total <= 10:
                    for c in range(1, total+1):
                        while True:
                            try:
                                nota = float(input(f'Insira a {c}° nota de {nome}: '))
                                if c == total+1:
                                    break
                                if 0 <= nota <= 10:
                                    notas.append(nota)
                                    alunos['notas'] = notas
                                    media = sum(notas) / len(notas)
                                    alunos['media'] = media
                                    if media >= 7:
                                        alunos['resultado'] = "\033[32mAPROVADO!\033[m"
                                    elif 5 <= media < 7:
                                        alunos['resultado'] = "\033[33mRECUPERAÇÃO\033[m"
                                    else:
                                        alunos['resultado'] = "\033[31mREPROVADO\033[m"
                                else:
                                    print('\033[31mA NOTA DEVE ESTAR ENTRE\033[m \033[36m1.0 - 10.0\033[m!')
                                    continue
                            except(ValueError, TypeError):
                                print('\033[31mVALOR INVÁLIDO! TENTE NOVAMENTE. (Ex: 3.5)\033[m')
                                continue
                            controle3 = False
                            break
                    print(f"\033[35m{nome}\033[m \033[32mFOI CADASTRADO COM SUCESSO!\033[m\n")
                    break
                else:
                    print('\033[31mVALOR ESTÁ ABAIXO OU ULTRAPASSOU O LIMITE!\033[m')
                    continue
            except(ValueError, TypeError):
                print('\033[31mAPENAS NÚMEROS INTEIROS SÃO VÁLIDOS!\033[m')
                continue
    geral.append(alunos)
    salvar_arquivo()

def banco():
    if not geral:
        print('\033[31mNÃO HÁ ALUNOS CADASTRADOS!\033[m\n')
        return
    while True:
        for k, aluno in enumerate(geral):
            print(f"{k} - {aluno['aluno']}")
        try:
            opcao = int(input(f'Qual aluno deseja ver informações? \n<\033[35m{usuario_logado}\033[m>: '))
            while True:
                if 0 <= opcao < len(geral):
                    print(f'O(A) aluno(a) {geral[opcao]["aluno"]} obteve média de {geral[opcao]["media"]:.1f}, com as notas {geral[opcao]["notas"]} e está(em) {geral[opcao]["resultado"]}.')
                    break
                else:
                    print('\033[31mALUNO INVÁLIDO OU INEXISTENTE NO BANCO DE DADOS! TENTE NOVAMENTE.\033[m')
                    continue
        except(ValueError, TypeError):
            print('\033[31mUTILIZE APENAS NÚMEROS AO SELECIONAR!\033[m')
            continue
        break

def editar():
    while True:
        for k, aluno in enumerate(geral):
            print(f"{k} - {aluno['aluno']}")
        try:
            opcao = int(input(f'Qual aluno deseja alterar/remover os dados?\n(\033[31mO ALUNO SERÁ REMOVIDO DO SISTEMA E PRECISARÁ SER ADICIONADO NOVAMENTE!\033[m \n\n<\033[35m{usuario_logado}\033[m>: '))
            if 0 <= opcao < len(geral):
                print(f'O(A) aluno(a) {geral[opcao]["aluno"]} foi \033[31mREMOVIDO!\033[m do sistema!')
                del geral[opcao]
                break
            else:
                print('\033[31mOPÇÃO INVÁLIDA! TENTE NOVAMENTE.\033[m')
                continue
        except(ValueError, TypeError):
            print('\033[31mUTILIZE APENAS NÚMEROS AO SELECIONAR!\033[m')
            continue
    salvar_arquivo()

def sair():
    try:
        print(f'OBRIGADO POR ACESSAR NOSSO PROGRAMA, {usuario_logado}.\nATÉ LOGO!')
    except NameError:
        print('OBRIGADO POR ACESSAR NOSSO PROGRAMA!')
    sleep(2)
    print('\033[31mFIM DO PROGRAMA!\033[m')

from time import sleep
from datetime import datetime

controle4 = True

print(27*'-')
print('\033[34mBANCO DE DADOS ESCOLAR\033[m \033[37mV1.0\033[m')
print(27*'-')
print()
for b in 'CARREGANDO...':
    print(f'{b}', end=' ', flush=True)
    sleep(0.25)
print('\n')

carregar_usuarios()

while True:
    print("1 - Login")
    print("2 - Registrar-se")
    print("3 - Sair\n")

    try:
        opc1 = int(input("Opção: "))
        if opc1 == 1:
            usuario_logado, tipo_usuario = login_sistema()
            if usuario_logado:
                break
        elif opc1 == 2:
            registrar()
        elif opc1 == 3:
            sair()
            exit()
        else:
            print('\033[31mOPÇÃO EXCEDEU A LISTA! \nTENTE NOVAMENTE.\033[m')
    except(ValueError, TypeError):
        print("\033[31mOPÇÃO INVÁLIDA! TENTE NOVAMENTE.\033[m")

print(18*'-\n')
horas = datetime.now().hour
if 6 <= horas <= 11:
    print(f'Bom dia, \033[35m{usuario_logado}\033[m!\nBem vindo(a)!\n\nComo vamos começar o dia hoje?: \n\n')
elif 12 <= horas <= 17:
    print(f'Boa tarde, \033[35m{usuario_logado}\033[m!\nBem vindo(a)!\n\nEspero que o dia esteja indo bem!\nO que vamos fazer hoje?:\n\n ')
else:
    print(f'Boa noite, \033[35m{usuario_logado}\033[m!\nBem vindo(a)!\n\nComo vamos finalizar o dia?: \n\n')

menu = True

while menu:
    print('1 - Cadastrar aluno(a).\n2 - Banco de alunos')
    if tipo_usuario == "admin":
        print('3 - Editar/Remover aluno')
    print('4 - Sair\n')
    try:
        opc = int(input(f'<\033[35m{usuario_logado}\033[m>: '))
        if opc == 1:
            if tipo_usuario == "admin":
                cadastrar()
                continue
            else:
                print("\033[31mAPENAS ADMINISTRADORES PODEM CADASTRAR UM ALUNO!\033[m")
        elif opc == 2:
            banco()
            continue
        elif opc == 3 and tipo_usuario != "admin":
                print("\033[31mAPENAS ADMINISTRADORES PODEM REMOVER UM ALUNO!\033[m")
                continue
        elif opc == 3 and tipo_usuario == "admin":
            if not geral:
                print('\033[31mNÃO HÁ ALUNOS CADASTRADOS!\033[m\n')
                continue
            if tipo_usuario == "admin":
                editar()
                continue
        elif opc == 4:
            sair()
            break
        else:
            print('\033[31mOPÇÃO INVÁLIDA! TENTE NOVAMENTE.\033[m')
            continue
    except(ValueError, TypeError):
        print('\033[31mOPÇÃO INVÁLIDA! TENTE NOVAMENTE.\033[m')
        continue
    menu = False
    break
