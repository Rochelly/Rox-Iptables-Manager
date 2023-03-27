
import subprocess
import re
import file_utils 



class Firewall_Handler:

    def __init__(self) -> None:
        pass

    def run_command(self, command):
        try:
            args = command.split()
            completed_process = subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True, completed_process.stdout
        except subprocess.CalledProcessError as error:
            return False,  error.stderr
     
    def run_command_no_out(self,command):
        try:
            args = command.split()
            subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError as e:
            return False
    
    def check_chain_exist(self,chain):
        command="sudo iptables -nL "+chain
        return self.run_command_no_out(command)

    def check_forward_reference(self, target):
        command = "sudo iptables -nL FORWARD --line-numbers"
        success, output = self.run_command(command)
        if not success:
            return False
        target = " " + target + " "
        for line in output.decode().splitlines():
            if target in line:
                rule_num = line.split()[0]
                return rule_num
        return False


    def delete_forward_reference(self,target):
        while self.check_forward_reference(target):
            subprocess.run(['sudo', 'iptables', '-D', 'FORWARD',self.check_forward_reference(target) ])
          
    def delete_chain(self,chain):
        if not chain:
            return
        self.delete_forward_reference(chain)
        commandF="sudo iptables -F "+chain
        commandX="sudo iptables -X "+chain
        self.run_command_no_out(commandF)
        self.run_command_no_out(commandX)

    def create_chain_destination(self,chain,ip):
        
        self.delete_chain(chain)
        command="sudo iptables -N "+chain
        self.run_command(command)  
        referenceChain="sudo iptables -t filter -I FORWARD -d "+ip+" -j "+chain
        self.run_command(referenceChain)
    
    def create_chain_soucer(self,chain,ip):
        self.delete_chain(chain)
        command="sudo iptables -N "+chain
        self.run_command(command)  
        referenceChain="sudo iptables -t filter -I FORWARD -s "+ip+" -j "+chain
        self.run_command(referenceChain)    

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






myFH=Firewall_Handler()


myFH.create_chain_destination('ROX',"10.0.101.7")
myFH.create_chain_soucer('ROX2',"10.0.101.7")