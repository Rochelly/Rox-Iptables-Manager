import curses
# Configurando a biblioteca para que se possa navegar pelo menu



# Define the menu function
def menu_factory(title, menu_items):
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    screen.keypad(True)

    # Definuindo as cores
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Cor verde
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # cor Amarela
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, title)
    screen.addstr(4, 2, "Use as teclas de seta para cima e para baixo para selecionar uma opção:")
    screen.addstr(5, 2, "Pressione Enter para selecionar uma opção:")
    screen.refresh()

    # Initialize the menu
    current_row = 0
    option = 0
    while True:
        # Display the menu items
        for index, item in enumerate(menu_items):
            if index == current_row:
                screen.addstr(7 + index, 4, item, curses.color_pair(1))
            else:
                screen.addstr(7 + index, 4, item, curses.color_pair(2))
        screen.refresh()

        # Get user input
        key = screen.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            option = current_row
            break


    # Clean up the curses library
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    return option


