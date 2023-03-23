
import curses
import firewall_libs.intefacesPrints as interfacePrints



def startScreen():
    screen = curses.initscr()
    screen.keypad(True)
    interfacePrints.drawHeader(screen)
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
                functionsList[option](screen)
    return
                
  
    

    



