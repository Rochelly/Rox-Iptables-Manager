import curses
import os
import datetime
import subprocess
import re


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
    

# def runCommand(command):
#     print(command)
#    # return
#     try:
#         args = command.split()
#         subprocess.run(args, check=True)
#         return ""
     
#     except subprocess.CalledProcessError as error:
#         return str(error)
    

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
            #descricao = re.search(r'DESCRICAO="(.*?)"', linha)
            regra = re.search(r'REGRA=(.*?)\s+', linha)
            
            if origem and ports and protocol and regra:
                #print(f'Linha {num_linha + 1}')
 
                rule=(f' sudo iptables -t filter -A {chain} -s  {origem.group(1)} -p {protocol.group(1)} -m multiport --dport {ports.group(1)} -m conntrack --ctstate NEW -j {regra.group(1)} ')
              #  print('\n')
               # print(rule)
                if runCommand(rule):
                    erro=f'Erro na linha Linha {num_linha + 1} ({chain}) - Arquivo: {nome_arquivo}'
                    print(erro)
                    listErros.append







def exec_shell_command(command):
    output = subprocess.check_output(command, shell=True)
    return output.decode()

#def screenTemplate(screen):

def main():
# Configurando a biblioteca para que se possa navegar pelo menu
    title='O que deseja fazer?'
    menu_items=['Recarregar regras persistidas',
                'Cadastrar Novo Serviço',
                 'sair']
    menu_items2=['Recarregar regras persistidas2',
                'Cadastrar Novo Serviço2',
                 'sair2']


    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    screen.keypad(True)

    # Definuindo as cores
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Cor verde
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # cor Amarela
    screen.clear()
    screen.border(0)
    screen.addstr(2, 5, title)
    screen.addstr(4, 2, "Use as teclas de seta para cima e para baixo para selecionar uma opção:")
    screen.addstr(5, 2, "Pressione Enter para selecionar uma opção:")
    screen.addstr( 14, 2,"Output Area:")
    screen.hline( 15, 2, '_',100)

    screen.refresh()

    # Initialize the menu
    current_row = 0
    option = 0
    while True:
        # Display the menu items
        for index, item in enumerate(menu_items):
            if index == current_row:
                screen.addstr(7 + index, 4, item, curses.color_pair(1))
            else:
                screen.addstr(7 + index, 4, item, curses.color_pair(2))
        screen.refresh()

        # Get user input
        key = screen.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            option = current_row
            if option==0: 
                baseDir="rules-files/"
                modifiedFiles=get_changed_files(dir_path)
                if len(modifiedFiles) == 0:
              
                    screen.clear()
                    screen.border(0)
                    screen.addstr(2, 5, title)
                    screen.addstr(4, 2, "Use as teclas de seta para cima e para baixo para selecionar uma opção:")
                    screen.addstr(5, 2, "Pressione Enter para selecionar uma opção:")
                    screen.addstr( 14, 2,"Output Area:")
                    screen.hline( 15, 2, '_',100)
                    screen.addstr(19 ,4, "Não Existe Modificações nas regras", curses.color_pair(2))
                   # screen.keypad(False)
                   # curses.echo()
                  #  curses.endwin()
                    
                    
                else:                       #para cada arquivo que sofreu modificação
                    printline=20
                    screen.clear()
                    screen.border(0)
                    screen.addstr(2, 5, title)
                    screen.addstr(4, 2, "Use as teclas de seta para cima e para baixo para selecionar uma opção:")
                    screen.addstr(5, 2, "Pressione Enter para selecionar uma opção:")
                    screen.addstr( 14, 2,"Output Area:")
                    screen.hline( 15, 2, '_',100)
                    for file in modifiedFiles:
                        file=baseDir+file
                        nome=getServiceName(file)
                        ip=getServiceIP(file)
                    
                        msg="As regras do serviço "+nome+"("+ip+") foram atualizadas..."
                        screen.addstr(printline ,4, msg, curses.color_pair(2))
                        printline=printline+1
                        clearChain(nome)
                        createChain(nome,ip)
                        command="/bin/bash "+file
                        #runCommand(command)
                        setServiceRules(file,nome)
                        msg2="As regras são:"
                        screen.addstr(printline ,4, msg2, curses.color_pair(2))
                        printline=printline+1
                        #command2="sudo iptables -v -L "+nome
                        #runCommand(command2)
                    

            if option==1:
                break
            if option==2:
                break
       


    # Clean up the curses library
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    return option



main()

#setServiceRules("/home/rochelly/roxFirewallman/rules-files/agronomia.fw","AGRONOMIA")

