import os
import json
import git
import sys
import subprocess
from git import Repo

# Função para clonar o repositório
def clone_repo(repo_url, token, local_dir):
    repo_url_with_token = repo_url.replace("https://", f"https://{token}:x-oauth-basic@")
    repo = Repo.clone_from(repo_url_with_token, local_dir)
    return repo


# Função para verificar se há diferenças entre dois branches
def has_diff_between_branches(repo, origin_branch, base_branch,):
    # Acessando os branches remotos explicitamente
    branch1 = f'refs/remotes/origin/{origin_branch}'  # Se for um branch remoto
    branch2 = f'refs/remotes/origin/{base_branch}'  # Se for um branch remoto
    
    # Obtendo os commits de cada branch
    commits1 = list(repo.iter_commits(branch1))
    commits2 = list(repo.iter_commits(branch2))
    
    # Criando sets para facilitar a comparação
    commits1_set = set(commit.hexsha for commit in commits1)
    commits2_set = set(commit.hexsha for commit in commits2)

    # Encontrando commits exclusivos para cada branch
    unique_commits1 = commits1_set - commits2_set
    unique_commits2 = commits2_set - commits1_set

    # Se houver commits exclusivos, significa que há diferenças
    if unique_commits1 or unique_commits2:
        return True

    # Caso não tenha commits exclusivos, comparando as diferenças nos arquivos dos commits
    for commit1 in commits1:
        for commit2 in commits2:
            # Obtendo as diferenças entre os commits
            diffs = commit1.diff(commit2)
            if diffs:
                return True  # Se houver qualquer diferença, retorna True

    return False  # Caso não haja diferenças entre os commits


def get_commit_from_branch(repo, branch_name): 
    """
    Obtém o commit de um branch remoto específico.
    """
    try:
        # Obtemos o commit mais recente do branch remoto
        commit = repo.commit(f'refs/remotes/origin/{branch_name}')
        print(f"Commit do branch {branch_name} obtido com sucesso: {commit.hexsha}")
    except Exception as e:
        print(f"Erro ao acessar o commit do branch {branch_name}: {e}")
        raise
    return commit

def get_modified_files(repo, old_commit, new_commit):
    """
    Obtém os arquivos modificados entre dois commits.
    """
    try:
        # Usando git diff para obter apenas os arquivos modificados entre dois commits
        diff = repo.git.diff('--name-only', old_commit.hexsha, new_commit.hexsha)
        if diff:
            print(f"Differences entre {old_commit.hexsha} e {new_commit.hexsha}:")
            print(diff)  # Exibe as diferenças encontradas
        else:
            print(f"Sem diferenças encontradas entre {old_commit.hexsha} e {new_commit.hexsha}.")
        modified_files = diff.splitlines()  # Divide a saída em uma lista de arquivos
        return modified_files
    except Exception as e:
        print(f"Erro ao executar git diff: {e}")
        return []
        
        
def get_modified_folders(modified_files):
    """
    Extrai as pastas das listas de arquivos modificados.
    """
    modified_folders = set()
    for file in modified_files:
        folder = file.split('/')[0]  # Considera a pasta como a parte antes da primeira barra "/"
        modified_folders.add(folder)
    return modified_folders


def compare_commits_and_folders(repo, origin_branch, base_branch): 
    """
    Compara dois branches e retorna as pastas alteradas entre os commits dos branches.
    
    Parameters:
    - repo: O repositório GitPython.
    - origin_branch: O branch de origem.
    - base_branch: O branch de destino.
    
    Retorna:
    - As pastas alteradas entre os dois branches.
    """
    # Obtendo os commits dos branches
    commit_origin = get_commit_from_branch(repo, origin_branch)
    commit_base = get_commit_from_branch(repo, base_branch)

    # Obtendo os arquivos modificados entre os commits
    modified_files = get_modified_files(repo, commit_origin, commit_base)

    # Extraindo as pastas modificadas
    modified_folders = get_modified_folders(modified_files)

    return modified_folders
    
def has_changes_in_directory(repo, origin_branch, base_branch, directory): 
    """
    Verifica se há alterações no diretório especificado entre dois branches.
    
    Parameters:
    - repo: O repositório GitPython.
    - origin_branch: O branch de origem.
    - base_branch: O branch de destino.
    - directory: O diretório a ser comparado.
    
    Retorna:
    - True se houver alterações no diretório, False caso contrário.
    """
    # Obtendo os commits dos branches
    commit_trunk = get_commit_from_branch(repo, origin_branch)
    commit_current = get_commit_from_branch(repo, base_branch)

    # Preparando as árvores dos commits
    old_tree = prepare_tree_parser(commit_trunk)
    new_tree = prepare_tree_parser(commit_current)

    # Comparando os diffs entre os dois commits no diretório especificado
    diffs = repo.git.diff(old_tree, new_tree, '--', directory)

    # Se houver qualquer diferença, retorna True
    return bool(diffs.strip())  # Se a string de diffs não estiver vazia, significa que há diferenças

 
# Função para ler a versão de version.txt
def get_version_from_file():
    version_file_path = 'version.txt'
    if not os.path.exists(version_file_path):
        print(f"Arquivo {version_file_path} não encontrado.")
        return None

    with open(version_file_path, 'r') as file:
        return file.read().strip()

# Função para atualizar o arquivo versao.json com a versão de version.txt
def update_version_json(directory):
    version_file_path = os.path.join(directory, 'versao.json')

    if not os.path.exists(version_file_path):
        print(f"Arquivo versao.json não encontrado em {directory}.")
        return

    with open(version_file_path, 'r') as f:
        data = json.load(f)

    # Obtendo a versão do arquivo version.txt
    versao = get_version_from_file()
    if not versao:
        print("Versão não encontrada no arquivo version.txt.")
        return

    print(f"Versão do arquivo version.txt: {versao}.")
    # Definindo a versão obtida de version.txt no arquivo JSON
    data['versao'] = versao

    # Atualizar o arquivo JSON
    with open(version_file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Versão atualizada para {versao} no arquivo versao.json em {directory}")
# Função para atualizar o arquivo versao.json
# def update_version_json(directory):
#     version_file_path = os.path.join(directory, 'versao.json')

#     if not os.path.exists(version_file_path):
#         print(f"Arquivo versao.json não encontrado em {directory}.")
#         return

#     with open(version_file_path, 'r') as f:
#         data = json.load(f)

#     # Incrementar a versão
#     current_version = data.get('versao', '1.0.0.0')
#     new_version = increment_version(current_version)
#     data['versao'] = new_version

#     # Atualizar o JSON
#     with open(version_file_path, 'w') as f:
#         json.dump(data, f, indent=4)

#     print(f"Versão atualizada para {new_version} no arquivo versao.json em {directory}")

# # Função para incrementar a versão
# def increment_version(version):
#     version_parts = version.split('.')
#     build = int(version_parts[3])
#     build += 1
#     version_parts[3] = str(build)
#     return '.'.join(version_parts)

# Função para fazer commit e push das alterações
def commit_and_push(repo, branch, token):
    # Adiciona todas as mudanças ao índice
    repo.git.add(update=True) 
    # Realiza o commit
    repo.index.commit("Atualizando a versão no arquivo versao.json")
    # URL do repositório com autenticação via token
    remote_url = f'https://{token}@github.com/deyvidksc/winthor-smart-hub-layouts.git'
    # Acessa o remote
    origin = repo.remotes.origin
    # Configura a URL com o token de autenticação
    origin.set_url(remote_url)
    # Realiza o push para o branch remoto
    origin.push(refspec=f"{branch}:{branch}")




def comparar_diferencas(repo, branch_base, branch_origem):
    # Listar branches locais
    print("Branches locais:")
    for branch in repo.branches:
        print(f"- {branch.name}")

    # Listar branches remotos
    print("\nBranches remotos:")
    for remote in repo.remotes:
        for ref in remote.refs:
            print(f"- {ref.name}")

    # Atualizar os branches remotos
    print(f"Atualizando o repositório...")
    repo.git.fetch()

    # Garantir que o branch base esteja correto
    print(f"Fazendo checkout no branch {branch_base}...")
    repo.git.checkout(branch_base)
    repo.git.pull()

    # Garantir que o branch de origem remoto esteja correto (checkout direto no branch remoto)
    print(f"Fazendo checkout no branch remoto {branch_origem}...")
    try:
        # Criar um novo branch local que acompanha o branch remoto
        repo.git.checkout('-b', branch_origem, f'origin/{branch_origem}')
        repo.git.pull()
    except git.exc.GitCommandError as e:
        print(f"Erro ao fazer checkout no branch remoto {branch_origem}: {e}")
        sys.exit(1)

    # Verificar o estado atual do repositório
    print(f"Estado atual do repositório:")

    # Verificando o estado da HEAD
    if repo.head.is_detached:
        print(f"Você está em um estado de detached HEAD em {repo.head.commit.hexsha}")
    else:
        print(f"Branch ativo: {repo.active_branch}")

    print(f"Branch base: {branch_base}")
    print(f"Branch de origem: {branch_origem}")

    # Comparando as diferenças entre o branch base (local) e o branch de origem (remoto)
    print(f"Comparando {branch_base} com {branch_origem}...")
    diff = repo.git.diff(f"{branch_base}..origin/{branch_origem}", '--name-only')

    # Caso haja diferenças
    if diff:
        print(f'Diferenças encontradas entre {branch_base} e {branch_origem}:')
        dirs = set()
        for line in diff.splitlines():
            # Verifica se o item é uma pasta (diretório)
            if line.endswith('/'):  # Verifica se o caminho termina com '/'
                dirs.add(line)
            else:
                # Adiciona o diretório pai se for um arquivo dentro de um diretório
                dir_name = os.path.dirname(line)
                if dir_name:
                    dirs.add(dir_name + '/')

        # Se houver diretórios com diferenças
        if dirs:
            print("Pastas com diferenças:")
            for dir in dirs:
                print(f"- {dir}")
            return dirs  # Retorna as pastas com diferenças
        else:
            print("Nenhuma pasta com diferenças encontrada.")
            return []  # Nenhuma pasta com diferença
    else:
        print(f'Não há diferenças entre {branch_base} e {branch_origem}.')
        return []  # Nenhuma diferença detectada

     
       
        
# Função principal
def main():
    if len(sys.argv) < 4:
        print("Erro: é necessário passar o token, o branch origem e o branch destino.")
        sys.exit(1)

    # Parâmetros
    token = sys.argv[1]
    origin_branch = sys.argv[2]
    base_branch = sys.argv[3]
    repo_url = "https://github.com/deyvidksc/winthor-smart-hub-layouts.git"
    local_folder = "/tmp/git_repo"  # Defina o diretório local onde o repositório será clonado


    # Clonar o repositório
    repo = clone_repo(repo_url, token, local_folder)
    
    
    #checkout_branch(repo, origin_branch, local_folder)
    modified_folders = comparar_diferencas(repo, base_branch, origin_branch)
    # Verificar diferenças entre os branches
    #if has_diff_between_branches(repo, origin_branch, base_branch):
    if modified_folders:
        print(f"O branch '{origin_branch}' tem diferenças em relação ao '{base_branch}'.")
 
        try:               
            # Iterar pelas pastas e atualizar o versao.json
            #for dirpath, dirnames, filenames in os.walk(local_folder):
                # Verificando se o diretório contém um arquivo versao.json
                #if 'versao.json' in filenames:
                   # print(f"Verificando alterações na pasta: {dirpath}")
                    # Verificando se houve alterações no diretório entre os dois branches remotos
                    #if has_changes_in_directory(repo, origin_branch, base_branch, dirpath):
            for dirpath in modified_folders:        
                print(f"Alterações detectadas em: {dirpath}")
                # Se houver alterações, atualizar o versao.json
                update_version_json(dirpath)       
        except Exception as e:
            print(f"Erro: {e}")
            sys.exit(1)


        # Fazer commit e push das alterações
        commit_and_push(repo, base_branch, token)
    else:
        print(f"Não há diferenças entre os branches '{origin_branch}' e '{base_branch}'.")

if __name__ == "__main__":
    main()
