import menuBase


def input_menu():
    main_title="O que você deseja configurar"
    opcoes=['Carregar a as configurações do arquivo - X',
            'Realizar a Liberação total do INPUT',
            'Adicionar uma regra manualmente',
            ]
    return menuBase.menu_factory(main_title,opcoes)

def loadInputConfig():
    print("Carrengando as configurações do arquivos X ...")

def liberaInput():
    print("Liberando o imput")

def addRule():
    print("Adicionando uma nova regra")






def conf_Input():    
    selected=input_menu()
    menus = {0:loadInputConfig,
             1:liberaInput,
             2:addRule}
    menus.get(selected)()



