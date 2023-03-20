import menuBase
import input
import forward
import nat
import intefaceMenu


def main_menu():
    main_title='Qual Tabela você deseja configurar ?'
    opcoes_Main=['Input',
            'Forward - (Para Gateways)',
            'NAT- (Mascaramentos)',
            'sair']
    return   menuBase.menu_factory(main_title,opcoes_Main)


def main():
    selected= main_menu()
    # lista de funções do menu principal
    menus = {0:input.conf_Input,
             1:forward.conf_Forward,
             2:nat.conf_nat}
    menus.get(selected)()

main()
#menu_items=intefaceMenu.menu_interfaces()

