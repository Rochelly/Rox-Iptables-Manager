import json
from firewall_libs.menu import Menu
from firewall_libs.firewall_handler import Firewall_Handler


def main():

    # load configuration file (json)
    conf_path_file = "/home/rochelly/Projetos/roxFirewallman/firewall_libs/confgs.json"
    with open(conf_path_file) as config:
        config_file = json.load(config)

    # load parameters from conf file
    header_menu = config_file["menu_config"]["menu_header"]
    log_file = config_file["paths_dir"]["log_file_tmp"]
    last_checked_file = config_file["paths_dir"]["last_checked_file"]

    # instancia uma novo firewall handler
    my_fw = Firewall_Handler(log_file, last_checked_file)

    # Opções do menu a ser criado em uma screen
    functionalities_Dic = {
        "Recarregar regras de serviços": my_fw.reloadRules,
        "Listar serviços recentemente alterados": my_fw.list_modified_services,
        "Cadastrar Novo Serviço": my_fw.create_new_service,
        "Cadastrar Nova Sub-rede": my_fw.create_new_sub_net,
        "sair": my_fw.reloadRules}

    # cria um menu (screen) que passa como parametro, as opções e funções, o cabeçalho, e o arquivo de logs
    my_menu = Menu(functionalities_Dic, header_menu, log_file)

    my_menu.show()


if __name__ == '__main__':
    main()
