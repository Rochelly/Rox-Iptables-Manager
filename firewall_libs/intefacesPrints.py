import curses
def drawHeader(screen):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 8,"Bem-vindo ao assistente de configuração de firewall Iptables! " )
    screen.addstr(3, 5, "O que deseja fazer?")
    screen.addstr(4, 2, "Use as teclas de seta para cima e para baixo para selecionar uma opção:")
    screen.addstr(5, 2, "Pressione Enter para selecionar uma opção:")
    screen.addstr( 14, 2,"Status Area:")
    screen.hline( 15, 2, '_',100)
    screen.refresh()
    return

def drawStatusArea(screen,listMsg,color,position):
    printline=position
    drawHeader(screen)
    for alert in (listMsg):
        screen.addstr(printline ,position, alert, curses.color_pair(color))
        printline=printline+1


