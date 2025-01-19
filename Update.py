import os
import subprocess

# URLs dos arquivos no repositório
VERSION_URL = "https://raw.githubusercontent.com/Math14s/TORRE/refs/heads/main/version.txt"
GAME_URL = "https://raw.githubusercontent.com/Math14s/TORRE/refs/heads/main/jogo.py"

# Função para baixar arquivos usando wget
def download_file(url, local_name):
    print(f"Baixando {local_name}...")
    result = subprocess.run(["wget", "-q", "-O", local_name, url], capture_output=True)
    if result.returncode == 0:
        print(f"{local_name} baixado com sucesso.")
    else:
        print(f"Erro ao baixar {local_name}: {result.stderr.decode()}")

# Função para obter a versão local
def get_local_version():
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# Função para atualizar o jogo
def update_game():
    # Baixa a versão mais recente do repositório
    download_file(VERSION_URL, "repo_version.txt")

    # Lê a versão do repositório
    try:
        with open("repo_version.txt", "r") as f:
            repo_version = f.read().strip()
    except FileNotFoundError:
        print("Erro ao ler a versão do repositório.")
        return

    # Lê a versão local
    local_version = get_local_version()

    # Verifica se é necessário atualizar
    if local_version is None or repo_version > local_version:
        print(f"Nova versão {repo_version} encontrada! Atualizando...")

        # Deleta arquivos antigos
        if os.path.exists("jogo.py"):
            os.remove("jogo.py")
        if os.path.exists("version.txt"):
            os.remove("version.txt")

        # Baixa os arquivos atualizados
        download_file(GAME_URL, "jogo.py")
        download_file(VERSION_URL, "version.txt")

        print("Atualização concluída!")
    else:
        print(f"Você já está com a versão mais recente: {local_version}.")

    # Remove o arquivo temporário de versão
    if os.path.exists("repo_version.txt"):
        os.remove("repo_version.txt")

# Executar a atualização
update_game()
