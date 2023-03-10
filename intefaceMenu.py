import netifaces
import menuBase
import curses
# Configurando a biblioteca para que se possa navegar pelo menu
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad(True)

# Definuindo as cores
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Cor verde
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # cor Amarela



# Analisando as interfaces
interfaces = netifaces.interfaces()

# Pegando a rota padrão
gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]

# Create a menu with the interfaces
def list_interfaces():
    current_row = 0
    menu_items = []
    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            ips = [addr['addr'] for addr in addrs[netifaces.AF_INET]]
            netmasks = [addr['netmask'] for addr in addrs[netifaces.AF_INET]]
            for ip, netmask in zip(ips, netmasks):
                menu_items.append(f"{interface} ({ip}/{netmask})")
    menu_items.append("Exit")
    return menu_items




def menu_interfaces():
    menu_items=list_interfaces()
    option = menuBase.menu_principal("Selecione a Rede que deseja configurar o Firewall", menu_items)
    if option != len(menu_items) - 1:
        screen.clear()
        screen.addstr(0, 0, f"Interface selecionada: {menu_items[option]}")
        screen.addstr(1, 0, f"Endereço de rede: {menu_items[option].split()[1]}")
        screen.addstr(2, 0, f"Gateway padrão: {gateway}")
        screen.refresh()
        screen.getch()
        screen.keypad(False)
        curses.echo()
        curses.endwin()

   
