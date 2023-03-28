import json
from firewall_libs.menu import Menu
import firewall_libs.menu_funcions as firewall 


def main():

    functionalities_Dic={ 
        "Recarregar regras de serviços":firewall.reloadRules,
        "Listar serviços recentemente alterados":firewall.reloadRules,
        "Cadastrar Novo Serviço":firewall.reloadRules,
        "sair":firewall.reloadRules}
   
    with open("firewall_libs/confgs.json") as config:
        config_file=json.load(config)
    header_menu=config_file["menu_config"]["menu_header"]

    my_menu = Menu(functionalities_Dic,header_menu)
    my_menu.show()
   

if __name__ == '__main__':
    main()