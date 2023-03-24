
import subprocess
import re
import firewall_libs.fileUtils as fileUtils

# executa um comando no sistema operacional e retona o erro se tiver
def runCommand(command):
    if not command:
        return False
    try:
        args = command.split()
        subprocess.run(args, check=True)
        return False
    except subprocess.CalledProcessError as error:
        return str(error)

#verifica se uma chain existe
def checkExistChain(chain):
    command="sudo iptables -nL "+chain
    try:
        args = command.split()
        subprocess.run(args, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    
# verifica se tem uma referência no forward, se existir, retorna o numero da regra
def checkForwardReference(target):

    output = subprocess.Popen(['sudo', 'iptables', '-nL', 'FORWARD', '--line-numbers'], stdout=subprocess.PIPE)
    target=" "+target+" "
    # Analisa a saída para encontrar as linhas que contêm o alvo especificado e exclui as regras correspondentes
    for line in output.stdout:
        line = line.decode().strip()
        if target in line:
            rule_num = line.split()[0]
            return rule_num
    return False


def deleteForwardReference(target):
    while checkForwardReference(target):
        subprocess.run(['sudo', 'iptables', '-D', 'FORWARD',checkForwardReference(target) ])
            

    


def deleteChain(chain):
    deleteForwardReference(chain)
    commandF="sudo iptables -F "+chain
    commandX="sudo iptables -X "+chain
    runCommand(commandF)
    runCommand(commandX)


# cria uma chain e adiciona a referência no forward
def createChainService(chain,ip):
    deleteChain(chain)
    command="sudo iptables -N "+chain
    runCommand(command)
    referenceChain="sudo iptables -t filter -I FORWARD -d "+ip+" -j "+chain
    runCommand(referenceChain)


def setServiceRules(nome_arquivo,chain):
    listErros=[]
    with open(nome_arquivo, 'r') as arquivo:
        for num_linha, linha in enumerate(arquivo.readlines()):
            rule=""
            if linha.startswith('#'):
                continue
            origem = re.search(r'ORIGEM=(.*?)\s+', linha)
            ports = re.search(r'PORTS=(.*?)\s+', linha)
            protocol = re.search(r'PROTOCOL=(.*?)\s+', linha)
            regra = re.search(r'REGRA=(.*?)\s+', linha)          
            if origem and ports and protocol and regra:
                rule=(f' sudo iptables -t filter -A {chain} -s  {origem.group(1)} -p {protocol.group(1)} -m multiport --dport {ports.group(1)} -m conntrack --ctstate NEW -j {regra.group(1)} ')
                if runCommand(rule):
                    erro=f'Erro na linha Linha {num_linha + 1} ({chain}) - Arquivo: {nome_arquivo}'
                    listErros.append(erro)
    return listErros


def reloadServiceRules(dirPathServices):
   # dirPathServices="rules-files/"
    errosMsg=[]
    sucessMsg=[]
    alertMsg=[]
    sucessReload=[] 
    modifiedFiles=fileUtils.getChangedFiles(dirPathServices)

    if len(modifiedFiles) == 0:
        alertMsg.append("Não Existe arquivos modificados")
    else:                 
        for file in modifiedFiles:
            file=dirPathServices+file
            nome=fileUtils.getInFIle(file,'NAME')
            ip=fileUtils.getInFIle(file,'IP')
            reloadMsg=f"{nome} - {ip}"
            sucessReload.append(reloadMsg)
            createChainService(nome,ip)
            erros=setServiceRules(file,nome)
            if erros:
                msg2=f'Erros encontrados no serviço:{nome}'
                errosMsg.append(msg2)
                for  erro in (erros):
                    errosMsg.append(erro)
            else:
                sucessMsg=["Nenhum erro encontrado, regras recarregadas com sucesso!","Serviços Modificados:"]+sucessReload
    allMsg = {'alert':alertMsg,'error':errosMsg,'sucess':sucessMsg}
    return allMsg
