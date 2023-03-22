import menuBase
def conf_Forward():
    main_title="O que você deseja fazer"
    opcoes=['Carregar a as configurações do arquivo - X',
            'Realizar a Liberação total do Forward',
            'Adicionar uma regra manualmente']
    menuBase.menu_factory(main_title,opcoes)