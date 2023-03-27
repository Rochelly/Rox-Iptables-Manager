import os
import datetime
import re
class File_Utils:

    def __init__(self,dir_base) -> None:
        self.last_checked_file=dir_base+"last_checked.txt"
        self.dir_base=dir_base
        self.last_checked_date=datetime.datetime.fromisoformat('2000-01-01 00:00:00')

    
    def get_key_in_file(self, file_name, key):
        with open(file_name) as file:
            value = ''
            for line in file:
                if line.startswith(f'{key}='):
                    value = line.strip().split('=')[1]
                    break
        return value
    
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
        
    
    def extract_rules_in_file(self,file_name,chain):
        listErros=[]
        rules=[]

        print(file_name)
        with open(file_name, 'r') as arquivo:
            for num_linha, linha in enumerate(arquivo.readlines()):
                rule=""
                if linha.startswith('#'):
                    continue
                origem = re.search(r'ORIGEM=([^\s]+)', linha)
                porta = re.search(r'PORTAS=([^\s]+)', linha)
                protocolo = re.search(r'PROTOCOLO=([^\s]+)', linha)
                regra = re.search(r'REGRA=([^\s]+)', linha)
                destino = re.search(r'DESTINO=([^\s]+)', linha)


   
              




                if origem and origem.group(1) != '*':
                    source = f'-s {origem.group(1)}'  
                else:
                    source=''
                
                
                if destino and  destino.group(1) != '*':
                    destination=f'-d {destino.group(1)}'
                else:
                    destination=''

                if protocolo and  protocolo.group(1) != '*':
                    protocol=f'-p {protocolo.group(1)}'
                else:
                    protocol=''

                if regra and  regra.group(1) != '*':
                    action=f' -j {regra.group(1)}'
                else:
                    action=f' -j ACCEPT'    
                





                
                if porta:

                    port_list=self.split_port_10(porta.group(1))
                 
                    
                    for port_group in port_list:            
                
                        if port_group and port_group != '*':
                            ports=f' -m multiport --dport {port_group}'
                      #  elif port_group and port_group != '*' and destino:
                      #      ports=f' -m multiport --sport {port_group}'
                       
                        rule=f"sudo iptables -t  filter -A {chain} {source} {destination} {protocol} {ports} {action}"
                        print(rule)
   
                else:
                    if  protocol or destination or source:
                        rule=f"sudo iptables -t  filter -A {chain} {source} {destination} {protocol}{action}"
                        print(rule)

                # if origem:
                #   if origem and ports and protocol and regra:
                #     rule=(f' sudo iptables -t filter -A {chain} -s  {origem.group(1)} -p {protocol.group(1)} -m multiport --dport {ports.group(1)} -m conntrack --ctstate NEW -j {regra.group(1)} ')
                # elif destino:
                #             pass
                # else:
                #     erro=f'Erro na linha Linha {num_linha + 1} ({chain}) - Arquivo: {nome_arquivo}'
                #     listErros.append(erro)



              
        return listErros

        
                    

    def get_changed_files(self):
        if os.path.exists(self.last_checked_file):
            with open(self.last_checked_file, 'r') as f:
                last_checked_date = datetime.datetime.fromisoformat(f.read().strip())
        
        files = os.listdir(self.dir_base)
        modified_files = []

        for file in files:
            file_path = os.path.join(self.dir_base, file)
            modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if modification_time > last_checked_date and os.path.splitext(file)[-1] == '.fw':
                modified_files.append(file)

        with open(self.last_checked_file, 'w') as f:
            f.write(datetime.datetime.now().isoformat())

        return modified_files

my_file_utils=File_Utils("/home/rochelly/roxFirewallman/em_classes/services-rules-files")
my_file_utils.extract_rules_in_file("/home/rochelly/roxFirewallman/em_classes/services-rules-files/biologia.fw",'ROX')
#my_file_utils.split_port_10("22,23,24,25,25,26,27,28,26,26,22,23,24,25,27,28,26,26,25,26,27,28,26,26,22,23,24,251,1,2,25,26,27,28,26,26")