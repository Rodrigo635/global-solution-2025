## 🛠️ Instruções para Rodar o Projeto

Este projeto é uma aplicação Web desenvolvida com Django, com o objetivo de exibir alertas sobre eventos climáticos extremos e facilitar o processo de doações para ONGs e regiões afetadas por desastres.

### ✅ Pré-requisitos

Certifique-se de ter os seguintes softwares instalados:

* [Python 3.10 ou superior](https://www.python.org/) (lembre-se de baixar o Python de forma personalizada e ativar para que ele crie um caminho nas suas variáveis de ambiente) 
* [pip](https://pip.pypa.io/)
* Git (opcional, caso vá clonar o repositório)

---

### 📂 1. Clone ou baixe o projeto

**Via Git:**

```bash
git clone https://github.com/Rodrigo635/global-solution-2025.git
cd global-solution
```

**Ou:** baixe o `.zip` do projeto e extraia, em seguida abra a pasta no terminal.

---

### 🧪 2. Baixe, crie e ative um ambiente virtual
**Baixe ambiente virtual:**
```bash
pip install virtualenv
```

**Criação do ambiente virtual:**
```bash
python -m venv env
```

**Ativação do ambiente virtual:**

* **Windows:**

  ```bash
  env\scripts\activate
  ```

* **Linux/macOS:**

  ```bash
  source env/bin/activate
  ```

---

### 📦 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 🛠️ 4. Rode a build do projeto
```bash
python build_django.py
```

---

### 🚀 5. Execute o servidor local

```bash
python manage.py runserver
```

Abra no navegador ou clique no link exibido no terminal usando CTRL após rodar o runserver:

```
http://127.0.0.1:8000/
```

---
