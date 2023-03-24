
import firewall_libs.handlerFirewall as fw
 
dirPathServices = './services-rules-files/'







def reloadRules():
    return   fw.reloadServiceRules(dirPathServices)





