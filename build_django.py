import os
import subprocess
import sys


def run(command):
    print(f"\n🛠️ Executando comando: {command}")
    subprocess.run(command, shell=True, check=True)
    print("✅ Comando finalizado com sucesso.")


def create_superuser():
    import django
    from django.contrib.auth import get_user_model

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_global.settings')
    django.setup()

    User = get_user_model()
    username = 'admin'
    email = 'admin@admin.adm'
    password = 'admin'

    if not User.objects.filter(username=username).exists():
        print(f"\n✨ Criando superusuário {username}...")
        User.objects.create_superuser(username=username, email=email, password=password)
        print("✅ Superusuário criado com sucesso!")
    else:
        print(f"\n⚠️ Superusuário {username} já existe. Ignorando criação.")


def criar_categorias():
    import django
    from app_contas.models import Categoria

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_global.settings')
    django.setup()
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
    from django.contrib.auth import get_user_model
    from app_contas.models import OngProfile, Categoria
    from django.utils.timezone import now
    User = get_user_model()

    dados_ongs = [
        {
            'username': 'ong_esperanca',
            'email': 'contato@ongesperanca.org',
            'categorias': ['Educação', 'Assistência Social'],
            'cidade': 'São Paulo',
            'descricao': 'Atua com foco em educação e assistência social.',
        },
        {
            'username': 'ong_saudavel',
            'email': 'contato@ongsaudavel.org',
            'categorias': ['Saúde', 'Nutrição'],
            'cidade': 'Campinas',
            'descricao': 'Promove saúde e boa alimentação para comunidades.',
        },
        {
            'username': 'ong_verde_vida',
            'email': 'contato@ongverdevida.org',
            'categorias': ['Meio Ambiente'],
            'cidade': 'Curitiba',
            'descricao': 'Trabalha na preservação ambiental e reflorestamento.',
        },
        {
            'username': 'ong_amor_animal',
            'email': 'contato@ongamoranimal.org',
            'categorias': ['Animais'],
            'cidade': 'Belo Horizonte',
            'descricao': 'Resgata e cuida de animais abandonados.',
        },
        {
            'username': 'ong_sonho_vivo',
            'email': 'contato@ongsonhovivo.org',
            'categorias': ['Cultura', 'Educação'],
            'cidade': 'Salvador',
            'descricao': 'Desenvolve projetos culturais e educacionais.',
        },
        {
            'username': 'ong_maos_dadas',
            'email': 'contato@ongmaosdadas.org',
            'categorias': ['Assistência Social'],
            'cidade': 'Fortaleza',
            'descricao': 'Apoia famílias em situação de vulnerabilidade.',
        },
        {
            'username': 'ong_paz_ativa',
            'email': 'contato@ongpazativa.org',
            'categorias': ['Direitos Humanos'],
            'cidade': 'Porto Alegre',
            'descricao': 'Defende direitos e promove a cidadania.',
        },
        {
            'username': 'ong_futuro_digital',
            'email': 'contato@ongfuturodigital.org',
            'categorias': ['Tecnologia', 'Educação'],
            'cidade': 'Recife',
            'descricao': 'Ensina programação e inclusão digital.',
        },
        {
            'username': 'ong_crianca_feliz',
            'email': 'contato@ongcriancafeliz.org',
            'categorias': ['Infância', 'Educação'],
            'cidade': 'Manaus',
            'descricao': 'Cuida de crianças em situação de risco.',
        },
        {
            'username': 'ong_vida_marinha',
            'email': 'contato@ongvidamarinha.org',
            'categorias': ['Meio Ambiente', 'Animais'],
            'cidade': 'Florianópolis',
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
                endereco='Rua das Flores',
                estado='SP',
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

    # caminhos = ["app_contas", "app_rotas", "app_doacoes", "app_alertas"]
    # for caminho in caminhos:
    #     print(f"🧹 Removendo migrações antigas em {caminho}/migrations...")
    #     run(DELETE_MIGRATIONS_CMD.format(caminho))

    print("🧹 Removendo arquivo do banco de dados SQLite (db.sqlite3)...")
    run(DELETE_DB_CMD)

    print("📦 Gerando novas migrações...")
    run(f'"{VENV_PYTHON}" manage.py makemigrations')

    print("🚀 Aplicando migrações no banco de dados...")
    run(f'"{VENV_PYTHON}" manage.py migrate')

    print("✨ Criando superusuário padrão...")
    create_superuser()
    criar_categorias()
    criar_ong()
    print("\n🎉 Build do projeto Django finalizado com sucesso!")


if __name__ == "__main__":
    main()
