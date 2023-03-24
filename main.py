import firewall_libs.interfaceDraw as interface
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

    interface.mainMenu(menu_items,functionsList)

main()
