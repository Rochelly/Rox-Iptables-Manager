import netifaces
import curses
import menuBase
import intefaceMenu
# Configurando a biblioteca para que se possa navegar pelo menu
#screen = curses.initscr()
#curses.noecho()
#curses.cbreak()
#curses.start_color()
#screen.keypad(True)

# Definuindo as cores
#curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Cor verde
#curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # cor Amarela

# Analisando as interfaces
interfaces = netifaces.interfaces()

# Pegando a rota padrão
gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]

# Create a menu with the interfaces

menu_items=intefaceMenu.menu_interfaces()

# Display the menu and get the user's selection
option = menuBase.menu_principal("Selecione a Rede que deseja configurar o Firewall", menu_items)

# Print the selected interface and network address
#if option != len(menu_items) - 1:
#    screen.clear()
#    screen.addstr(0, 0, f"Interface selecionada: {menu_items[option]}")
#    screen.addstr(1, 0, f"Endereço de rede: {menu_items[option].split()[1]}")
#    screen.addstr(2, 0, f"Gateway padrão: {gateway}")
#    screen.refresh()
#    screen.getch()

# Clean up the curses library
#screen.keypad(False)
#curses.echo()
#curses.endwin()
