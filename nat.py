import menuBase
def conf_nat():
    main_title="O que você deseja fazer"
    opcoes=['Carregar a as configurações do arquivo - X',
          'mascarar um rede interna',
          'escape de mascaramento']
    menuBase.menu_factory(main_title,opcoes)
