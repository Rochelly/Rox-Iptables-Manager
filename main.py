import json
from firewall_libs.menu import Menu
from firewall_libs.firewall_handler import Firewall_Handler


def main():
    """
    Main function that loads configuration from a JSON file, creates a Firewall_Handler object with the configuration, 
    defines a dictionary of menu options and associated functions, creates a Menu object, and displays the menu.

    :return: None
    """
    # load configuration file (json)
    conf_path_file = "/home/rochelly/Projetos/roxFirewallman/firewall_libs/confgs.json"
    with open(conf_path_file) as config:
        config_file = json.load(config)


    # load parameters from conf file
    header_menu = config_file["menu_config"]["menu_header"]
    log_file = config_file["paths_dir"]["log_file_tmp"]

    # create a new firewall handler, passing the configuration file
    my_fw = Firewall_Handler(config_file)

    # dictionary of menu options and associated functions
    functionalities_Dic = {
        "Reload service rules": my_fw.reloadRules,
        "List recently modified services": my_fw.list_modified_services,
        "Create new service": my_fw.create_new_service,
        "Create new subnet": my_fw.create_new_sub_net,
        "Exit": my_fw.reloadRules}

    # create a menu screen that takes as parameters the options and functions, the header, and the log file
    my_menu = Menu(functionalities_Dic, header_menu, log_file)

    my_menu.show()


if __name__ == '__main__':
    main()
