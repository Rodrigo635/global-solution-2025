from datetime import timedelta
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
    try:
        print(f"\n🛠️ Executando comando: {command}")
        subprocess.run(command, shell=True, check=True)
        print("✅ Comando finalizado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar o comando: {e}")

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

def criar_eventos_brasil():
    """
    Cria eventos de exemplo para diferentes cidades do Brasil
    """
    print("\n🚨 Criando eventos de exemplo para o Brasil...")
    
    # Verifica se já existem eventos
    if Eventos.objects.exists():
        print("⚠️ Já existem eventos cadastrados. Deseja continuar mesmo assim? (y/n)")
        resposta = input().lower()
        if resposta != 'y':
            print("❌ Operação cancelada.")
            return
    
    try:
        with transaction.atomic():
            # Busca o país Brasil
            brasil = Pais.objects.get(nome='Brasil')
            
            # Dados dos eventos de exemplo
            eventos_exemplo = [
                {
                    'nome': 'Chuvas Intensas no Rio Grande do Sul',
                    'descricao': 'Fortes chuvas causaram alagamentos em várias cidades da região metropolitana de Porto Alegre. Famílias desabrigadas precisam de ajuda.',
                    'tipo': 'chuva_forte',
                    'urgente': True,
                    'estados': ['Rio Grande do Sul'],
                    'cidades': ['Porto Alegre', 'Canoas', 'Novo Hamburgo', 'São Leopoldo'],
                    'dias_inicio': -2,  # Começou há 2 dias
                    'dias_fim': 1,      # Termina em 1 dia
                    'doar': 'https://www.defesacivil.rs.gov.br/doacoes'
                },
                {
                    'nome': 'Seca Extrema no Nordeste',
                    'descricao': 'Região enfrenta uma das piores secas dos últimos anos. Reservatórios em níveis críticos e agricultura prejudicada.',
                    'tipo': 'seca',
                    'urgente': False,
                    'estados': ['Ceará', 'Pernambuco', 'Bahia'],
                    'cidades': ['Fortaleza', 'Recife', 'Salvador', 'Juazeiro', 'Petrolina'],
                    'dias_inicio': -30,  # Começou há 30 dias
                    'dias_fim': 60,      # Vai durar mais 60 dias
                    'doar': 'https://www.gov.br/cidadania/pt-br'
                },
                {
                    'nome': 'Incêndios Florestais no Pantanal',
                    'descricao': 'Queimadas de grandes proporções atingem o Pantanal, ameaçando a fauna e flora local. Bombeiros trabalham no combate às chamas.',
                    'tipo': 'incendio',
                    'urgente': True,
                    'estados': ['Mato Grosso', 'Mato Grosso do Sul'],
                    'cidades': ['Cuiabá', 'Corumbá', 'Cáceres', 'Poconé'],
                    'dias_inicio': -5,   # Começou há 5 dias
                    'dias_fim': 10,      # Estimativa de 10 dias para controle
                    'doar': 'https://www.sosma.org.br/causas/pantanal/'
                },
                {
                    'nome': 'Deslizamentos em Petrópolis',
                    'descricao': 'Chuvas fortes provocaram deslizamentos de terra na região serrana. Equipes de resgate trabalham na busca por vítimas.',
                    'tipo': 'deslizamento',
                    'urgente': True,
                    'estados': ['Rio de Janeiro'],
                    'cidades': ['Petrópolis', 'Teresópolis', 'Nova Friburgo'],
                    'dias_inicio': -1,   # Começou há 1 dia
                    'dias_fim': 3,       # Operações de resgate por 3 dias
                    'doar': 'https://www.rj.gov.br/defesacivil'
                },
                {
                    'nome': 'Tempestade de Granizo em São Paulo',
                    'descricao': 'Forte tempestade com granizo atinge a Grande São Paulo, causando danos a veículos e residências.',
                    'tipo': 'granizo',
                    'urgente': False,
                    'estados': ['São Paulo'],
                    'cidades': ['São Paulo', 'Guarulhos', 'Osasco', 'Santo André'],
                    'dias_inicio': 0,    # Hoje
                    'dias_fim': 0,       # Evento pontual
                    'doar': None
                },
                {
                    'nome': 'Vendaval no Paraná',
                    'descricao': 'Ventos fortes derrubaram árvores e destelharam casas em várias cidades paranaenses.',
                    'tipo': 'vendaval',
                    'urgente': False,
                    'estados': ['Paraná'],
                    'cidades': ['Curitiba', 'Maringá', 'Londrina', 'Cascavel'],
                    'dias_inicio': -3,   # Há 3 dias
                    'dias_fim': -2,      # Já terminou
                    'doar': None
                },
                {
                    'nome': 'Enchente no Acre',
                    'descricao': 'Rio Acre transbordou causando enchentes na capital e cidades vizinhas. Centenas de famílias foram evacuadas.',
                    'tipo': 'enchente',
                    'urgente': True,
                    'estados': ['Acre'],
                    'cidades': ['Rio Branco', 'Cruzeiro do Sul', 'Sena Madureira'],
                    'dias_inicio': -4,   # Há 4 dias
                    'dias_fim': 5,       # Mais 5 dias
                    'doar': 'https://www.ac.gov.br/defesacivil'
                },
                {
                    'nome': 'Geada no Sul do Brasil',
                    'descricao': 'Forte geada atinge plantações no sul do país, causando prejuízos na agricultura.',
                    'tipo': 'geada',
                    'urgente': False,
                    'estados': ['Rio Grande do Sul', 'Santa Catarina'],
                    'cidades': ['Caxias do Sul', 'Passo Fundo', 'Lages', 'Chapecó'],
                    'dias_inicio': -1,   # Ontem
                    'dias_fim': -1,      # Já passou
                    'doar': None
                },
                {
                    'nome': 'Poluição Atmosférica em Brasília',
                    'descricao': 'Níveis elevados de poluição atmosférica devido às queimadas no Cerrado afetam a qualidade do ar na capital.',
                    'tipo': 'poluicao',
                    'urgente': False,
                    'estados': ['Distrito Federal'],
                    'cidades': ['Brasília'],
                    'dias_inicio': -7,   # Há uma semana
                    'dias_fim': 14,      # Mais 2 semanas
                    'doar': None
                },
                {
                    'nome': 'Ressaca Marinha no Litoral de Santa Catarina',
                    'descricao': 'Mar agitado com ondas de até 4 metros atinge o litoral catarinense. Navegação suspensa.',
                    'tipo': 'ressaca',
                    'urgente': False,
                    'estados': ['Santa Catarina'],
                    'cidades': ['Florianópolis', 'Balneário Camboriú', 'Itajaí', 'Joinville'],
                    'dias_inicio': 1,    # Amanhã
                    'dias_fim': 3,       # Mais 3 dias
                    'doar': None
                }
            ]
            
            eventos_criados = 0
            
            for evento_data in eventos_exemplo:
                try:
                    # Calcula as datas
                    data_inicio = timezone.now() + timedelta(days=evento_data['dias_inicio'])
                    data_fim = timezone.now() + timedelta(days=evento_data['dias_fim']) if evento_data['dias_fim'] is not None else None
                    
                    # Cria o evento
                    evento = Eventos.objects.create(
                        nome=evento_data['nome'],
                        descricao=evento_data['descricao'],
                        data_inicio=data_inicio,
                        data_fim=data_fim,
                        tipo=evento_data['tipo'],
                        urgente=evento_data['urgente'],
                        doar=evento_data.get('doar')
                    )
                    
                    # Adiciona o Brasil como país afetado
                    evento.paises.add(brasil)
                    
                    # Adiciona estados
                    for estado_nome in evento_data['estados']:
                        try:
                            estado = Estado.objects.get(nome=estado_nome)
                            evento.estados.add(estado)
                        except Estado.DoesNotExist:
                            print(f"⚠️ Estado '{estado_nome}' não encontrado")
                    
                    # Adiciona cidades
                    for cidade_nome in evento_data['cidades']:
                        try:
                            cidade = Cidade.objects.get(nome=cidade_nome)
                            evento.cidades.add(cidade)
                        except Cidade.DoesNotExist:
                            print(f"⚠️ Cidade '{cidade_nome}' não encontrada")
                        except Cidade.MultipleObjectsReturned:
                            # Se houver múltiplas cidades com o mesmo nome, pega a primeira
                            cidade = Cidade.objects.filter(nome=cidade_nome).first()
                            evento.cidades.add(cidade)
                            print(f"⚠️ Múltiplas cidades '{cidade_nome}' encontradas, usando a primeira")
                    
                    eventos_criados += 1
                    print(f"✅ Evento criado: {evento.nome}")
                    
                except Exception as e:
                    print(f"❌ Erro ao criar evento '{evento_data['nome']}': {e}")
            
            print(f"\n🎉 Script finalizado! Eventos criados: {eventos_criados}")
            
    except Pais.DoesNotExist:
        print("❌ País 'Brasil' não encontrado. Execute primeiro o script de criação de países.")
    except Exception as e:
        print(f"❌ Erro durante criação dos eventos: {e}")
        raise

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
    criar_eventos_brasil()
    create_superuser()
    criar_categorias()
    print("populando banco de dados...")
    criar_ong()
    print("\n🎉 Build do projeto Django finalizado com sucesso!")


if __name__ == "__main__":
    main()
