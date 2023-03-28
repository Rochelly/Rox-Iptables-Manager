import logging



log_file="/home/rochelly/roxFirewallman/firewall_libs/rox_firewall.log"
# Configurando o logger
logging.basicConfig(filename=log_file, level=logging.DEBUG)

# Usando o logger
logging.debug('Mensagem de debug')
logging.info('Mensagem de informação')
logging.warning('Mensagem de alerta')
logging.error('Mensagem de erro')
logging.critical('Mensagem crítica')


