import menuBase
import input
import forward
import nat
import checkLogs
import intefaceMenu
import reloadRules
import registreService

def main_menu():
    main_title='O que deseja fazer?'
    opcoes_Main=['Recarregar regras persistidas',
                 'Cadastrar Novo Serviço',
            'Input',
            'Forward - (Para Gateways)',
            'NAT- (Mascaramentos)',
            'Verificar os logs de bloqueios e tentativas de acesso',
            'sair']
    return   menuBase.menu_factory(main_title,opcoes_Main)

def quit():
    return




def main():

    while True:
        selected= main_menu()
        if selected==6:
            break
        # lista de funções do menu principal
        menus = { 0: reloadRules.updateChains,
                1: registreService.registreService,
                2:input.conf_Input,
                3:forward.conf_Forward,
                4:nat.conf_nat,
                5:checkLogs.logs,
                6:quit}
        
        menus.get(selected)()

main()
#menu_items=intefaceMenu.menu_interfaces()

