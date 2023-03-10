import netifaces



# Analisando as interfaces
interfaces = netifaces.interfaces()

# Pegando a rota padrão
gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]

# Create a menu with the interfaces
def menu_interfaces():
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
