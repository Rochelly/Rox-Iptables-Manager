import menuBase


def input_menu():
    main_title="O que você deseja configurar"
    opcoes=['Carregar a as configurações do arquivo - X',
            'Realizar a Liberação total do INPUT',
            'Adicionar um regra manualmente']
    return menuBase.menu_factory(main_title,opcoes)




def conf_Input():    
    input_menu()


