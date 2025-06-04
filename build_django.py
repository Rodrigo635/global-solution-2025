import os
import subprocess
import sys
import django
import requests
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_global.settings')
django.setup()

from app_global.models import *
from app_contas.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

def run(command):
    print(f"\n🛠️ Executando comando: {command}")
    subprocess.run(command, shell=True, check=True)
    print("✅ Comando finalizado com sucesso.")


def create_superuser():
    username = 'admin'
    email = 'admin@admin.adm'
    password = 'admin'
    cidade = Cidade.objects.get(id=1)

    if not User.objects.filter(username=username).exists():
        print(f"\n✨ Criando superusuário {username}...")
        User.objects.create_superuser(username=username, email=email, password=password, cidade=cidade)
        print("✅ Superusuário criado com sucesso!")
    else:
        print(f"\n⚠️ Superusuário {username} já existe. Ignorando criação.")


def criar_categorias():
    categorias = [
        "Educação",
        "Saúde",
        "Meio Ambiente",
        "Cultura",
        "Direitos Humanos",
        "Esportes",
        "Animais",
        "Tecnologia",
        "Assistência Social",
        "Habitação"
    ]

    for nome in categorias:
        categoria, criada = Categoria.objects.get_or_create(nome=nome)
        if criada:
            print(f"✅ Categoria '{nome}' criada.")
        else:
            print(f"⚠️ Categoria '{nome}' já existe. Ignorando.")
            

def criar_ong():
    from django.utils.timezone import now

    city = Cidade.objects.get(id=1)
    dados_ongs = [
        {
            'username': 'ong_esperanca',
            'email': 'contato@ongesperanca.org',
            'categorias': ['Educação', 'Assistência Social'],
            'cidade':  city,
            'descricao': 'Atua com foco em educação e assistência social.',
        },
        {
            'username': 'ong_saudavel',
            'email': 'contato@ongsaudavel.org',
            'categorias': ['Saúde', 'Nutrição'],
            'cidade':  city,
            'descricao': 'Promove saúde e boa alimentação para comunidades.',
        },
        {
            'username': 'ong_verde_vida',
            'email': 'contato@ongverdevida.org',
            'categorias': ['Meio Ambiente'],
            'cidade': city,
            'descricao': 'Trabalha na preservação ambiental e reflorestamento.',
        },
        {
            'username': 'ong_amor_animal',
            'email': 'contato@ongamoranimal.org',
            'categorias': ['Animais'],
            'cidade': city,
            'descricao': 'Resgata e cuida de animais abandonados.',
        },
        {
            'username': 'ong_sonho_vivo',
            'email': 'contato@ongsonhovivo.org',
            'categorias': ['Cultura', 'Educação'],
            'cidade': city,
            'descricao': 'Desenvolve projetos culturais e educacionais.',
        },
        {
            'username': 'ong_maos_dadas',
            'email': 'contato@ongmaosdadas.org',
            'categorias': ['Assistência Social'],
            'cidade': city,
            'descricao': 'Apoia famílias em situação de vulnerabilidade.',
        },
        {
            'username': 'ong_paz_ativa',
            'email': 'contato@ongpazativa.org',
            'categorias': ['Direitos Humanos'],
            'cidade': city,
            'descricao': 'Defende direitos e promove a cidadania.',
        },
        {
            'username': 'ong_futuro_digital',
            'email': 'contato@ongfuturodigital.org',
            'categorias': ['Tecnologia', 'Educação'],
            'cidade': city,
            'descricao': 'Ensina programação e inclusão digital.',
        },
        {
            'username': 'ong_crianca_feliz',
            'email': 'contato@ongcriancafeliz.org',
            'categorias': ['Infância', 'Educação'],
            'cidade': city,
            'descricao': 'Cuida de crianças em situação de risco.',
        },
        {
            'username': 'ong_vida_marinha',
            'email': 'contato@ongvidamarinha.org',
            'categorias': ['Meio Ambiente', 'Animais'],
            'cidade': city,
            'descricao': 'Protege a vida marinha e costeira.',
        },
    ]

    for dados in dados_ongs:
        if not User.objects.filter(username=dados['username']).exists():
            print(f"\n✨ Criando usuário para ONG '{dados['username']}'...")
            user = User.objects.create_user(
                username=dados['username'],
                email=dados['email'],
                password='senha123',
                cidade=dados['cidade'],
                tipo='ong',
            )

            categorias = Categoria.objects.filter(nome__in=dados['categorias'])
            user.categorias.set(categorias)

            OngProfile.objects.create(
                user=user,
                cnpj='12.345.678/0001-99',
                descricao=dados['descricao'],
                telefone='(11) 91234-5678',
                rua='Rua das Flores',
                cep='12345678',
                bairro='Centro',
                numero='123',
                complemento='',
                pix='pix@ong.org',
                pixTipo='Email',
                site=f'https://www.{dados["username"]}.org',
                emergencia=False,
                data_criacao=now()
            )

            print(f"✅ ONG '{dados['username']}' criada com sucesso!")
        else:
            print(f"\n⚠️ Usuário '{dados['username']}' já existe. Ignorando criação.")

def criar_estados():
    print("\n📡 Populando estados e municípios via API do IBGE...")
    
    if Estado.objects.exists():
        print("⚠️ Dados do IBGE já existem. Ignorando importação.")
        return
    
    try:
        with transaction.atomic():
            # Garante que o Brasil existe como país
            brasil, created = Pais.objects.get_or_create(
                nome='Brasil'
            )

            canada = Pais.objects.get_or_create(
                nome='Canada'
            )
            
            usa = Pais.objects.get_or_create(
                nome='Estados Unidos'
            )

            if created:
                print("🇧🇷 País Brasil criado")
            
            # Importa estados
            estados_data = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/estados').json()
            
            for estado in estados_data:
                Estado.objects.create(
                    nome=estado['nome'],
                    pais=brasil  # Associa ao país Brasil
                )
            
            # Importa municípios por estado
            total_municipios = 0
            for estado in Estado.objects.all():
                estado_nome_encoded = estado.nome.replace(' ', '%20')
                
                estado_api = next(
                    (e for e in estados_data if e['nome'] == estado.nome), 
                    None
                )
                
                if estado_api:
                    municipios_data = requests.get(
                        f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado_api["id"]}/municipios'
                    ).json()
                    
                    for municipio in municipios_data:
                        Cidade.objects.create(
                            nome=municipio['nome'],
                            estado=estado
                        )
                    
                    total_municipios += len(municipios_data)
                    print(f"📍 {estado.nome}: {len(municipios_data)} municípios")
            
            print(f"✅ Dados do IBGE importados! Estados: {Estado.objects.count()}, Municípios: {total_municipios}")
    
    except requests.RequestException as e:
        print(f"❌ Erro ao acessar API do IBGE: {e}")
    except Exception as e:
        print(f"❌ Erro durante importação: {e}")

    except Exception as e:
        print(f"❌ Erro ao importar dados do IBGE: {str(e)}")
        raise  # Interrompe o script se falhar

def main():

    if sys.platform == "win32":
        VENV_PYTHON = os.path.join(os.getcwd(), 'env', 'Scripts', 'python.exe')
        DELETE_DB_CMD = 'del db.sqlite3'
        DELETE_MIGRATIONS_CMD = 'del {}\\migrations\\0*.py'
    else:
        VENV_PYTHON = os.path.join(os.getcwd(), 'venv', 'bin', 'python')
        DELETE_DB_CMD = 'rm -f db.sqlite3'
        DELETE_MIGRATIONS_CMD = 'rm -rf {}/migrations/0*.py'

    print(f"📍 Caminho do Python no venv definido como: {VENV_PYTHON}")

    if not os.path.exists(VENV_PYTHON):
        print(f"❌ Python do venv não encontrado em {VENV_PYTHON}")
        sys.exit(1)

    caminhos = ["app_contas", "app_doacoes"]
    for caminho in caminhos:
        print(f"🧹 Removendo migrações antigas em {caminho}/migrations...")
        run(DELETE_MIGRATIONS_CMD.format(caminho))

    print("🧹 Removendo arquivo do banco de dados SQLite (db.sqlite3)...")
    run(DELETE_DB_CMD)

    for caminho in caminhos:
        print(f'📦 Gerando novas migrações para "{caminho}"')
        run(f'"{VENV_PYTHON}" manage.py makemigrations {caminho}')

    print("🚀 Aplicando migrações no banco de dados...")
    run(f'"{VENV_PYTHON}" manage.py migrate')

    print("✨ Criando superusuário padrão...")
    criar_estados()
    create_superuser()
    criar_categorias()
    print("populando banco de dados...")
    criar_ong()
    print("\n🎉 Build do projeto Django finalizado com sucesso!")


if __name__ == "__main__":
    main()
