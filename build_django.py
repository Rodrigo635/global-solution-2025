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
    from django.core.files.uploadedfile import SimpleUploadedFile
    from django.utils.timezone import now
    User = get_user_model()

    username = 'ong_esperanca'
    email = 'contato@ongesperanca.org'
    password = 'senha123'

    if not User.objects.filter(username=username).exists():
        print(f"\n✨ Criando usuário para ONG '{username}'...")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            cidade='São Paulo',
            tipo='ong',
            )

        print("✅ Usuário criado com sucesso!")

        # Criação do perfil OngProfile
        ong = OngProfile.objects.create(
            user=user,
            cnpj='12.345.678/0001-99',
            descricao='A ONG Esperança atua com foco em educação e assistência social.',
            telefone='(11) 91234-5678',
            endereco='Rua das Flores',
            estado='SP',
            cep='12345678',
            bairro='Jardim das Esperanças',
            numero='123',
            complemento='Sala 5',
            pix='pix.pix@pix.pix',
            pixTipo='Email',
            site='https://www.ongesperanca.org',
            emergencia=True,
            data_criacao=now()
        )

        categorias = Categoria.objects.filter(nome__in=['Educação', 'Assistência Social'])
        ong.categorias.set(categorias)
        print("✅ ONG criada com categorias associadas!")

    else:
        print(f"\n⚠️ Usuário '{username}' já existe. Ignorando criação.")



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

    caminhos = ["app_contas", "app_rotas", "app_doacoes", "app_alertas"]
    for caminho in caminhos:
        print(f"🧹 Removendo migrações antigas em {caminho}/migrations...")
        run(DELETE_MIGRATIONS_CMD.format(caminho))

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
