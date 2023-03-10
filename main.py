import menuBase
import intefaceMenu


def main_menu():
    main_title='Qual Tabela você deseja configurar ?'
    opcoes=['Input',
            'Forward - (Para Gateways)',
            'NAT- (Mascaramentos)']
    opcoes = ["Olá", "Como vai você?", "Qual é o seu nome?", "Qual é a hora?", "Sair"]
    menuBase.menu_principal(main_menu,opcoes)


main_menu()
#menu_items=intefaceMenu.menu_interfaces()

