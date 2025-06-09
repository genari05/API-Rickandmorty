import requests
import sqlite3
import re
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class Rickandmorty:
    def __init__(self):
        self.persona = []
        self.episodio = []
        self.localizacao = []

    def coletar(self):
        print("\nDigite vários IDs separados por ENTER. Digite 0 para pular para a próxima etapa.\n")

        while True:
            try:
                id_personagem = int(input('ID do Personagem (1 a 826 | 0 para continuar): '))
                if id_personagem == 0:
                    break
                if 1 <= id_personagem <= 826:
                    self.persona.append(id_personagem)
                else:
                    print("ID fora do intervalo. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")

        while True:
            try:
                id_episodio = int(input('ID do Episódio (1 a 51 | 0 para continuar): '))
                if id_episodio == 0:
                    break
                if 1 <= id_episodio <= 51:
                    self.episodio.append(id_episodio)
                else:
                    print("ID fora do intervalo. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")

        while True:
            try:
                id_localizacao = int(input('ID da Localização (1 a 127 | 0 para continuar): '))
                if id_localizacao == 0:
                    break
                if 1 <= id_localizacao <= 127:
                    self.localizacao.append(id_localizacao)
                else:
                    print("ID fora do intervalo. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")


class Processa:
    def __init__(self, listar_persona, listar_episodio, listar_localizacao):
        self.listar_persona = listar_persona
        self.listar_episodio = listar_episodio
        self.listar_localizacao = listar_localizacao

    def executar(self):
        personagens = []
        episodios = []
        localizacoes = []

        for persona in self.listar_persona:
            try:
                url = f'https://rickandmortyapi.com/api/character/{persona}'
                dados = requests.get(url).json()

                dados_persona = {
                    'nome': dados['name'],
                    'status': dados['status'],
                    'especie': dados['species'],
                    'genero': dados['gender'],
                    'origem': dados.get('origin', {}).get('name', 'N/A'),
                    'localizacao': dados.get('location', {}).get('name', 'N/A'),
                    'imagem': dados.get('image', '')
                }

                print(f"\n[Personagem] {dados_persona['nome']} coletado com sucesso.")
                personagens.append(dados_persona)
            except Exception as e:
                print(f"Erro ao processar personagem ID {persona}: {e}")

        for episodio in self.listar_episodio:
            try:
                url = f'https://rickandmortyapi.com/api/episode/{episodio}'
                dados = requests.get(url).json()

                dados_episodio = {
                    'nome': dados['name'],
                    'data': dados['air_date'],
                    'episodio': dados['episode'],
                    'criacao': dados['created']
                }

                print(f"\n[Episódio] {dados_episodio['nome']} coletado com sucesso.")
                episodios.append(dados_episodio)
            except Exception as e:
                print(f"Erro ao processar episódio ID {episodio}: {e}")

        for localizacao in self.listar_localizacao:
            try:
                url = f'https://rickandmortyapi.com/api/location/{localizacao}'
                dados = requests.get(url).json()

                dados_localizacao = {
                    'nome': dados['name'],
                    'tipo': dados['type'],
                    'dimensao': dados.get('dimension', 'N/A'),
                    'criacao': dados['created']
                }

                print(f"\n[Localização] {dados_localizacao['nome']} coletada com sucesso.")
                localizacoes.append(dados_localizacao)
            except Exception as e:
                print(f"Erro ao processar localização ID {localizacao}: {e}")

        self.salvar_no_banco(personagens, episodios, localizacoes)

    def processar_dados(self):
        dados_processados = []

        for persona in self.listar_persona:
            try:
                url = f'https://rickandmortyapi.com/api/character/{persona}'
                resposta = requests.get(url)
                dados = resposta.json()

                nome = dados.get('name', '')
                status = dados.get('status', '')
                especie = dados.get('species', '')
                origem = dados.get('origin', {}).get('name', '')
                imagem = dados.get('image', '')

                nome_valido = bool(re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome))
                especie_maiuscula = especie.upper()
                possui_https = 'https' in imagem

                dados_processados.append({
                    'nome': nome,
                    'nome_valido': nome_valido,
                    'especie_maiuscula': especie_maiuscula,
                    'status': status,
                    'origem': origem,
                    'tem_https_na_imagem': possui_https
                })

            except Exception as e:
                print(f"[ERRO PROCESSAMENTO] Personagem ID {persona}: {e}")

        with sqlite3.connect('projeto_rpa.db') as conexao:
            cursor = conexao.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dados_processados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    nome_valido BOOLEAN,
                    especie_maiuscula TEXT,
                    status TEXT,
                    origem TEXT,
                    tem_https_na_imagem BOOLEAN
                )
            ''')

            for d in dados_processados:
                cursor.execute('''
                    INSERT INTO dados_processados (
                        nome, nome_valido, especie_maiuscula,
                        status, origem, tem_https_na_imagem
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    d['nome'], d['nome_valido'], d['especie_maiuscula'],
                    d['status'], d['origem'], d['tem_https_na_imagem']
                ))

            conexao.commit()

    def salvar_no_banco(self, personagens, episodios, localizacoes):
        with sqlite3.connect('projeto_rpa.db') as conexao:
            cursor = conexao.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS personagens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT, status TEXT, especie TEXT, genero TEXT,
                    origem TEXT, localizacao TEXT, imagem TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS episodios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT, data TEXT, episodio TEXT, criacao TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS localizacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT, tipo TEXT, dimensao TEXT, criacao TEXT
                )
            ''')

            for p in personagens:
                cursor.execute('''
                    INSERT INTO personagens (nome, status, especie, genero, origem, localizacao, imagem)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (p['nome'], p['status'], p['especie'], p['genero'], p['origem'], p['localizacao'], p['imagem']))

            for e in episodios:
                cursor.execute('''
                    INSERT INTO episodios (nome, data, episodio, criacao)
                    VALUES (?, ?, ?, ?)''',
                    (e['nome'], e['data'], e['episodio'], e['criacao']))

            for l in localizacoes:
                cursor.execute('''
                    INSERT INTO localizacoes (nome, tipo, dimensao, criacao)
                    VALUES (?, ?, ?, ?)''',
                    (l['nome'], l['tipo'], l['dimensao'], l['criacao']))

            conexao.commit()
            print("\nTodos os dados foram salvos no banco de dados com sucesso!")


def gerar_relatorio_resumo(nome_arquivo='relatorio.txt'):
    with sqlite3.connect('projeto_rpa.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute("SELECT COUNT(*) FROM personagens")
        total_personagens = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM episodios")
        total_episodios = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM localizacoes")
        total_localizacoes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM dados_processados")
        total_processados = cursor.fetchone()[0]

        cursor.execute("SELECT nome, especie_maiuscula, status FROM dados_processados LIMIT 3")
        exemplos = cursor.fetchall()

        exemplo_texto = "\n".join([f"- {nome}, {especie}, {status}" for nome, especie, status in exemplos])

        texto = f"""
RELATÓRIO AUTOMÁTICO - RICK & MORTY

Personagens coletados: {total_personagens}
Episódios coletados: {total_episodios}
Localizações coletadas: {total_localizacoes}
Dados processados: {total_processados}

Exemplos de dados processados:
{exemplo_texto}

Este relatório foi gerado automaticamente pelo script Python.
"""

        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(texto.strip())

        return nome_arquivo


def enviar_email(destinatario, caminho_anexo):
    remetente = 'tgenari791@gmail.com'
    senha = 'ymoo jqop oliq texj'  # Use senha de aplicativo, não sua senha normal!

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = 'Relatório - Rick and Morty (Automatizado)'

    corpo = 'Olá! Segue em anexo o relatório gerado automaticamente.'
    mensagem.attach(MIMEText(corpo, 'plain'))

    if os.path.exists(caminho_anexo):
        with open(caminho_anexo, 'rb') as arquivo:
            parte = MIMEBase('application', 'octet-stream')
            parte.set_payload(arquivo.read())
            encoders.encode_base64(parte)
            parte.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(caminho_anexo)}"')
            mensagem.attach(parte)
    else:
        print("⚠️ Arquivo de relatório não encontrado.")

    try:
        print("📤 Enviando e-mail...")
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(mensagem)
        print("✅ E-mail enviado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")


# === Execução Principal ===
if __name__ == '__main__':
    '''coleta = Rickandmorty()
    coleta.coletar()
    processa = Processa(coleta.persona, coleta.episodio, coleta.localizacao)
    processa.executar()
    processa.processar_dados()'''

    relatorio_gerado = gerar_relatorio_resumo()
    enviar_email('tiagogcaldeira@gmail.com', relatorio_gerado)
