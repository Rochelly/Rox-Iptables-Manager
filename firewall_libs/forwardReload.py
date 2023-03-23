import os
import datetime
import subprocess
import re
import firewall_libs.intefacesPrints as interfacePrint
 
dir_path = './rules-files'



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
    if not command:
        return False
    
    try:
        args = command.split()
        subprocess.run(args, check=True)
        return False
     
    except subprocess.CalledProcessError as error:
        return str(error)

def createChain(chain,ip):
    command="sudo iptables -N "+chain
    runCommand(command)
    referenceChain="sudo iptables -t filter -I FORWARD -d "+ip+" -j "+chain
    runCommand(referenceChain)
  
def delete_rules_with_target(chain, target):
    # Executa o comando do iptables e captura a saída
    output = subprocess.Popen(['sudo', 'iptables', '-nL', chain, '--line-numbers'], stdout=subprocess.PIPE)
    target=" "+target+" "
    # Analisa a saída para encontrar as linhas que contêm o alvo especificado e exclui as regras correspondentes
    for line in output.stdout:
        
        line = line.decode().strip()

        if target in line:
            rule_num = line.split()[0]
           # print(line)
            subprocess.run(['sudo', 'iptables', '-D', chain, rule_num])

    # Aguarda o término do processo para garantir que todas as regras foram excluídas
    output.wait()

def clearChain(chain):
    delete_rules_with_target("FORWARD",chain)
    commandF="sudo iptables -F "+chain
    commandX="sudo iptables -X "+chain
    runCommand(commandF)
    runCommand(commandX)

def setServiceRules(nome_arquivo,chain,screen):

    listErros=[]

    with open(nome_arquivo, 'r') as arquivo:
        for num_linha, linha in enumerate(arquivo.readlines()):
            rule=""
            if linha.startswith('#'):
                continue
            origem = re.search(r'ORIGEM=(.*?)\s+', linha)
            ports = re.search(r'PORTS=(.*?)\s+', linha)
            protocol = re.search(r'PROTOCOL=(.*?)\s+', linha)
            #descricao = re.search(r'DESCRICAO="(.*?)"', linha)
            regra = re.search(r'REGRA=(.*?)\s+', linha)
            
            if origem and ports and protocol and regra:
                #print(f'Linha {num_linha + 1}')
 
                rule=(f' sudo iptables -t filter -A {chain} -s  {origem.group(1)} -p {protocol.group(1)} -m multiport --dport {ports.group(1)} -m conntrack --ctstate NEW -j {regra.group(1)} ')
              #  print('\n')
               # print(rule)
                if runCommand(rule):
                    erro=f'Erro na linha Linha {num_linha + 1} ({chain}) - Arquivo: {nome_arquivo}'
                    listErros.append(erro)
                    screen.clear()
    return listErros


def reloadRules(screen):

    listErros=[]
    sucessMsg=[]
    sucessReload=[]
    printline=17
    baseDir="rules-files/"
    modifiedFiles=get_changed_files(dir_path)
    if len(modifiedFiles) == 0:
        interfacePrint.drawStatusArea(screen,["Não Existe arquivos modificados"],4,printline)
        return
    else:                 
        for file in modifiedFiles:
            file=baseDir+file
            nome=getServiceName(file)
            ip=getServiceIP(file)
            reloadMsg=f"{nome} - {ip}"
            sucessReload.append(reloadMsg)
            clearChain(nome)
            createChain(nome,ip)
            erros=setServiceRules(file,nome,screen)
            if erros:
                msg2=f'Erros encontrados no serviço:{nome}'
                listErros.append(msg2)
                for  erro in (erros):
                    listErros.append(erro)
                    
    if listErros:
        interfacePrint.drawStatusArea(screen,listErros,3,printline)
       
    else:
        sucessMsg=["Nenhum erro encontrado, regras recarregadas com sucesso!","Serviços Modificados:"]+sucessReload
        interfacePrint.drawStatusArea(screen,sucessMsg,1,printline)

    return

