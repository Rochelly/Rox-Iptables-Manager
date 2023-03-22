import curses


# Define the menu function
def menu_factory(title):
    screen = curses.initscr()
    curses.cbreak()
    curses.start_color()
    screen.keypad(True)

    # Definuindo as cores
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Cor verde
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # cor Amarela
    screen.clear()
    screen.border(0)

    screen.addstr(2, 2, title)
    # exiba uma mensagem pedindo ao usuário que digite uma string
    screen.addstr("Digite uma string: ")
    screen.refresh()

    # leia a string digitada pelo usuário
    user_input = screen.getstr()



    # exiba a string digitada
    screen.addstr("\nVocê digitou: {}".format(user_input))
    screen.refresh()


    # aguarde a tecla enter para sair
    screen.getch()

    # restaure as configurações do terminal
    curses.endwin()

    user_input_str = user_input.decode('utf-8')

    # Clean up the curses library
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    return user_input_str

print(menu_factory("Entre com o valor "))