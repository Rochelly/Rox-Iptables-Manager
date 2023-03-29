import json
from firewall_libs.menu import Menu
import firewall_libs.menu_funcions as firewall


def main():

    conf_path_file = "/home/rochelly/roxFirewallman/firewall_libs/confgs.json"


    functionalities_Dic = {
        "Recarregar regras de serviços": firewall.reloadRules,
        "Listar serviços recentemente alterados": firewall.reloadRules,
        "Cadastrar Novo Serviço": firewall.reloadRules,
        "sair": firewall.reloadRules}


    with open(conf_path_file) as config:
        config_file = json.load(config)
        
    header_menu = config_file["menu_config"]["menu_header"]
    log_file=config_file["paths_dir"]["log_file_tmp"]

    

    my_menu = Menu(functionalities_Dic, header_menu, log_file)
    my_menu.show()


if __name__ == '__main__':
    main()
