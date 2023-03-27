import json
from firewall_libs.menu import Menu
import firewall_libs.FirewallOptions as firewall 


def main():

    functionsList=[firewall.reloadRules,
                   firewall.reloadRules,
                   firewall.reloadRules,
                   "sair"]


    with open("em_classes/firewall_libs/confgs.json") as config:
        config_file=json.load(config)
    

    
    my_menu = Menu(config_file["menu_config"]["menu_items"],functionsList
                   , config_file["menu_config"]["menu_header"])
    my_menu.show()


if __name__ == '__main__':
    main()