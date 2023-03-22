import os
import datetime
import subprocess

dir_path = './rules-files'
filepath="/home/rochelly/roxFirewallman/rules-files/agronomia.conf"


def  getServiceName(fileName):
    with open(fileName) as arquivo:
        for linha in arquivo:
            if linha.startswith('NAME='):
                nome = linha.strip().split('=')[1]
                break
    return nome

def  getServiceIP(fileName):
    with open(fileName) as arquivo:
        for linha in arquivo:
            if linha.startswith('IP='):
                nome = linha.strip().split('=')[1]
                break
    return nome

def get_changed_files(dir_path):
    # Define o diretório a ser verificado
    

    # Cria um arquivo auxiliar para armazenar a data da última verificação
    last_checked_file = 'last_checked.txt'

    # Obtém a data da última verificação a partir do arquivo auxiliar ou usa uma data antiga se não existir
    if os.path.exists(last_checked_file):
        with open(last_checked_file, 'r') as f:
            last_checked = datetime.datetime.fromisoformat(f.read().strip())
    else:
        last_checked = datetime.datetime.fromisoformat('2000-01-01 00:00:00')

    # Lista os arquivos no diretório
    files = os.listdir(dir_path)

    # Cria uma lista para armazenar os arquivos que foram modificados
    changed_files = []

    # Verifica a data de modificação de cada arquivo e adiciona na lista de arquivos modificados se foi modificado após a última verificação
    for file in files:
        file_path = os.path.join(dir_path, file)
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        if mod_time > last_checked and os.path.splitext(file)[-1] == '.fw':
            changed_files.append(file)

    # Atualiza a data da última verificação no arquivo auxiliar
    with open(last_checked_file, 'w') as f:
        f.write(datetime.datetime.now().isoformat())

    # Retorna a lista de arquivos modificados
    return changed_files


def checkExistChain(chain):
    command="sudo iptables -nL "+chain
    try:
        args = command.split()
        subprocess.run(args, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    

def runCommand(command):
    try:
        args = command.split()
        subprocess.run(args, check=True)
     
    except subprocess.CalledProcessError:
        return False
    

def createChain(chain,ip):
    command="sudo iptables -N "+chain
    runCommand(command)
    referenceChain="sudo iptables -t filter -I FORWARD -d "+ip+" -j "+chain
    runCommand(referenceChain)
   
  
def delete_rules_with_target(chain, target):
    # Executa o comando do iptables e captura a saída
    output = subprocess.Popen(['sudo', 'iptables', '-nL', chain, '--line-numbers'], stdout=subprocess.PIPE)

    # Analisa a saída para encontrar as linhas que contêm o alvo especificado e exclui as regras correspondentes
    for line in output.stdout:
        line = line.decode().strip()
        if target in line:
            rule_num = line.split()[0]
            subprocess.run(['sudo', 'iptables', '-D', chain, rule_num])

    # Aguarda o término do processo para garantir que todas as regras foram excluídas
    output.wait()


def clearChain(chain):
    delete_rules_with_target("FORWARD",chain)
    commandF="sudo iptables -F "+chain
    commandX="sudo iptables -X "+chain
    runCommand(commandF)
    runCommand(commandX)


def updateChains():
    #altere para o diretório base
    baseDir="rules-files/"
    modifiedFiles=get_changed_files(dir_path)
    if len(modifiedFiles) == 0:
        print("Não Existe Modificações nas regras")
        
    #para cada arquivo que sofreu modificação
    for file in modifiedFiles:
        file=baseDir+file
        nome=getServiceName(file)
        print("")
        print("As regras do serviço "+nome+" serão atualizadas...")
        ip=getServiceIP(file)
        clearChain(nome)
        createChain(nome,ip)
        command="/bin/bash "+file
        runCommand(command)
        print("")
        print("As Novas regras são:")
        command2="sudo iptables -v -L "+nome
        runCommand(command2)
      
updateChains()




