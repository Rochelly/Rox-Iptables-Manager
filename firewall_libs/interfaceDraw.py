
import curses

def drawHeader(screen):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 8,"Bem-vindo ao assistente de configuração de firewall Iptables! " )
    screen.addstr(3, 5, "O que deseja fazer?")
    screen.addstr(4, 2, "Use as teclas de seta para cima e para baixo para selecionar uma opção:")
    screen.addstr(5, 2, "Pressione Enter para selecionar uma opção:")
    screen.addstr(14, 2,"Status Area:")
    screen.hline( 15, 2, '_',100)
    screen.refresh()
    return

def drawStatusArea(screen,listMsg,color,position):
    printline=position
    drawHeader(screen)
    for alert in (listMsg):
        screen.addstr(printline ,position, alert, curses.color_pair(color))
        printline=printline+1

def drawMsgStatusArea(allMsg,screen):
    drawHeader(screen)
    printline=17
    if allMsg['alert']:
        drawStatusArea(screen,allMsg['alert'],2,printline)
    if allMsg['error']:
        drawStatusArea(screen,allMsg['error'],3,printline)
    if allMsg['sucess']:
        drawStatusArea(screen,allMsg['sucess'],1,printline)

    
def startScreen():
    screen = curses.initscr()
    screen.keypad(True)
    drawHeader(screen)
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Cor verde
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # cor Amarela
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    return screen

def stopScreen(screen):
    screen.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def mainMenu(menu_items,functionsList):

    screen=startScreen()
    current_row = 0
    option = 0

    while True:    
        for index, item in enumerate(menu_items):
            if index == current_row:
                screen.addstr(7 + index, 4, item, curses.color_pair(1))
            else:
                screen.addstr(7 + index, 4, item, curses.color_pair(2))
        screen.refresh()
        key = screen.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            option = current_row
            if menu_items[option]=="sair":
                stopScreen(screen)   
                print("Até logo!") 
                break
            else:
                drawMsgStatusArea(functionsList[option](),screen)
    return
                
  
    

    



