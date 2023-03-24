import firewall_libs.interfaceDraw as interface
import firewall_libs.FirewallOptions as firewall 

def main():
    menu_items=['Recarregar regras de serviços',
                'Listar serviços recentemente alterados',
                'Cadastrar Novo Serviço',
                 'sair']

    functionsList=[firewall.reloadRules,
                   firewall.reloadRules,
                   firewall.reloadRules,
                   "sair"]

    interface.mainMenu(menu_items,functionsList)

main()
