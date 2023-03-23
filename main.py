import firewall_libs.mainMenu as inteface
import firewall_libs.forwardReload as forward
def main():

    
    
    menu_items=['Recarregar regras persistidas',
                'Listar serviços recentemente alterados',
                'Cadastrar Novo Serviço',
                 'sair']

    functionsList=[forward.reloadRules,
                   forward.reloadRules,
                   forward.reloadRules,
                   "sair"]

    inteface.mainMenu(menu_items,functionsList)



main()
