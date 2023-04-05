
import subprocess
import re
import os
import datetime


class Firewall_Handler:

    def __init__(self, log_file, last_checked_file) -> None:
        self.log_file = log_file  # arquivo de los

        # aquivo que armazena a ultima checagem
        self.last_checked_file = last_checked_file
        pass

    def run_command(self, command):
        try:
            args = command.split()
            completed_process = subprocess.run(
                args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True, completed_process.stdout
        except subprocess.CalledProcessError as error:
            return False,  error.stderr

    def run_command_no_out(self, command):
        try:
            args = command.split()
            subprocess.run(args, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError as e:
            return False

    def check_chain_exist(self, chain):
        command = "sudo iptables -nL "+chain
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

    def delete_forward_reference(self, target):
        while self.check_forward_reference(target):
            subprocess.run(['sudo', 'iptables', '-D', 'FORWARD',
                           self.check_forward_reference(target)])

    def delete_chain(self, chain):
        if not chain:
            return
        self.delete_forward_reference(chain)
        commandF = "sudo iptables -F "+chain
        commandX = "sudo iptables -X "+chain
        self.run_command_no_out(commandF)
        self.run_command_no_out(commandX)

    def create_chain_destination(self, chain, ip):

        self.delete_chain(chain)
        command = "sudo iptables -N "+chain
        self.run_command(command)
        referenceChain = "sudo iptables -t filter -I FORWARD -d "+ip+" -j "+chain
        self.run_command(referenceChain)

    def create_chain_soucer(self, chain, ip):
        self.delete_chain(chain)
        command = "sudo iptables -N "+chain
        self.run_command(command)
        referenceChain = "sudo iptables -t filter -I FORWARD -s "+ip+" -j "+chain
        self.run_command(referenceChain)

    def split_port_10(self, ports):
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

    def extract_filter_rules_from_file(self, file_name, chain):

        rules = []
        lines = []

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

                if not (source_address or destination_address or protocol or port_list):
                    continue
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
                            lines.append(line_num)
                else:
                    rule_cmd = f"sudo iptables -t filter -A {chain} {source} {destination} {protocol} {action}"
                    rules.append(rule_cmd)
                    lines.append(line_num)

        return lines, rules

    def aply_rules_from_file(self, file_name, chain):
        lines, rules = self.extract_filter_rules_from_file(file_name, chain)
        line_rules = list(zip(lines, rules))
        erros = []
        for line, rule in line_rules:
            sucesso, msg = self.run_command(rule)
            if not sucesso:
                erros.append(f"Erro na linha:  {line + 1} do arquivo")
        return erros

    def get_in_file(self, fileName, key):
        with open(fileName) as arquivo:
            value = ''
            for linha in arquivo:
                if linha.startswith(f'{key}='):
                    value = linha.strip().split('=')[1]
                    break
        return value

    def write_files(self, lista_strings, nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo:
            for linha in lista_strings:
                arquivo.write(linha + '\n')

    def get_key_in_file(self, file_name, key):
        with open(file_name) as file:
            value = ''
            for line in file:
                if line.startswith(f'{key}='):
                    value = line.strip().split('=')[1]
                    break
        return value

    def compare_files(self, ald, new):
        with open(ald, 'r') as f1, open(new, 'r') as f2:
            linhas1 = set(f1.readlines())
            linhas2 = set(f2.readlines())
            linhas_diferentes = linhas1 - linhas2
        return list(linhas_diferentes)

    def create_file_list(self, dir_path, filename):
        files = os.listdir(dir_path)
        filesChains = []
        for file in files:
            if file.endswith('.fw'):
                chain = self.get_in_file(dir_path+file, 'NAME')
                filesChains.append(f'{file}={chain}')
        self.write_files(filesChains, filename)

    def check_deleted_files(self, dir_Path):
        oldFileName = dir_Path+'.controller_deleted_files.txt'
        newFileName = dir_Path+'.controller_deleted_files.tmp'
        listDeletedFiles = []
        if os.path.exists(oldFileName):
            self.create_file_list(dir_Path, newFileName)
            listDeletedFiles = self.compare_files(oldFileName, newFileName)
            os.remove(oldFileName)
            os.rename(newFileName, oldFileName)
        else:
            self.create_file_list(dir_Path, oldFileName)
        return listDeletedFiles

    def remove_Chain_Deleted(self, dir_Path):
        listDeletedFiles = self.check_deleted_files(dir_Path)
        for fileName in listDeletedFiles:
            name = fileName.split('=')
            chain = name[1].strip()
            self.delete_chain(chain)

    def get_changed_files(self, dir_path):

        # Cria um arquivo auxiliar para armazenar a data da última verificação

        # Obtém a data da última verificação a partir do arquivo auxiliar ou usa uma data antiga se não existir
        if os.path.exists(self.last_checked_file):
            with open(self.last_checked_file, 'r') as f:
                last_checked = datetime.datetime.fromisoformat(
                    f.read().strip())
        else:
            last_checked = datetime.datetime.fromisoformat(
                '2000-01-01 00:00:00')

        # Lista os arquivos no diretório
        files = os.listdir(dir_path)

        # Cria uma lista para armazenar os arquivos que foram modificados
        changed_files = []

        # Verifica a data de modificação de cada arquivo e adiciona na lista de arquivos modificados se foi modificado após a última verificação
        for file in files:
            file_path = os.path.join(dir_path, file)
            mod_time = datetime.datetime.fromtimestamp(
                os.path.getmtime(file_path))
            if mod_time > last_checked and os.path.splitext(file)[-1] == '.fw':
                changed_files.append(file)

        # Atualiza a data da última verificação no arquivo auxiliar
        with open(self.last_checked_file, 'w') as f:
            f.write(datetime.datetime.now().isoformat())

        # Retorna a lista de arquivos modificados
        return changed_files

    def reload_dir_rules_services(self, dir_Path):

        errosMsg = []
        sucessMsg = []
        alertMsg = []
        sucessReload = []
        modified_files = self.get_changed_files(dir_Path)

        print(modified_files)

        self.remove_Chain_Deleted(dir_Path)

        if len(modified_files) == 0:
            print("Não Existe arquivos modificados")
        else:
            print("Existe aquivos modificados")

            for file in modified_files:
                file = dir_Path+file
                nome = self.get_in_file(file, 'NAME')
                ip = self.get_in_file(file, 'IP')
                if (not ip) or (not nome):
                    errosMsg.append(
                        f'O arquivo {file} não esta configurado corretamente')
                    # time.sleep(5)
                   # (f'touch {file}')
                    continue
                reloadMsg = f"{nome} - {ip}"
                sucessReload.append(reloadMsg)
                self.create_chain_destination(nome, ip)
                erros = self.aply_rules_from_file(file, nome)
                if erros:
                    msg2 = f'Erros encontrados no serviço:{nome}'
                    # time.sleep(5)
                    # runCommand(f'touch {file}')
                    errosMsg.append(msg2)
                    for erro in (erros):
                        errosMsg.append(erro)
                else:
                    sucessMsg = ["Nenhum erro encontrado, regras recarregadas com sucesso!",
                                 "Serviços Modificados:"]+sucessReload

                nome = ''
                ip = ''

        allMsg = {'alert': alertMsg, 'error': errosMsg, 'sucess': sucessMsg}
        print(allMsg)
        return allMsg






    
    def reloadRules(self):
        pass

    def list_modified_services(self):
        pass

    def create_new_service(self):
        pass

    def create_new_sub_net(self):
        pass
