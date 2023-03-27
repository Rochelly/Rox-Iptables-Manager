
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


    def split_port_10(self,ports):
        substrings = ports.split(",")
        sublists = []
        temp = []

        for s in substrings:
            temp.append(s)
            if len(temp) == 10:
                sublists.append(",".join(temp))
                temp = []

        if len(temp) > 0:
            sublists.append(",".join(temp))
        return sublists    

    def extract_filter_rules_from_file(self,file_name, chain):
        list_errors = []
        rules = []

        try:
            with open(file_name, 'r') as file:
                for line_num, line in enumerate(file.readlines()):
                    # Ignora as linhas de comentário
                    if line.startswith('#'):
                        continue

                # Extrai os parâmetros da regra de firewall a partir da linha de configuração
                    source_address = re.search(r'ORIGEM=([^\s]+)', line)
                    destination_address = re.search(r'DESTINO=([^\s]+)', line)
                    protocol = re.search(r'PROTOCOLO=([^\s]+)', line)
                    rule_action = re.search(r'REGRA=([^\s]+)', line)
                    port_list = re.search(r'PORTAS=([^\s]+)', line)

                # Cria o comando da regra de firewall com base nos parâmetros extraídos
                    if source_address and source_address.group(1) != '*':
                        source = f'-s {source_address.group(1)}'
                    else:
                        source = ''

                    if destination_address and destination_address.group(1) != '*':
                        destination = f'-d {destination_address.group(1)}'
                    else:
                        destination = ''

                    if protocol and protocol.group(1) != '*':
                        protocol = f'-p {protocol.group(1)}'
                    else:
                        protocol = ''

                    if rule_action and rule_action.group(1) != '*':
                        action = f'-j {rule_action.group(1)}'
                    else:
                        action = '-j ACCEPT'

                    if port_list:
                        ports = self.split_port_10(port_list.group(1))

                        for port_group in ports:
                            if port_group and port_group != '*':
                                ports_cmd = f'-m multiport --dport {port_group}'
                                rule_cmd = f"sudo iptables -t filter -A {chain} {source} {destination} {protocol} {ports_cmd} {action}"
                                rules.append(rule_cmd)
                    else:
                        rule_cmd = f"sudo iptables -t filter -A {chain} {source} {destination} {protocol} {action}"
                        rules.append(rule_cmd)

            return rules

        except FileNotFoundError:
            list_errors.append(f"File {file_name} not found.")
            return list_errors

        except Exception as e:
            list_errors.append(f"An error occurred: {e}")
            return list_errors




myFH=Firewall_Handler()


my_file_utils=Firewall_Handler()
print(my_file_utils.extract_filter_rules_from_file("/home/rochelly/roxFirewallman/em_classes/services-rules-files/biologia.fw",'ROX'))
