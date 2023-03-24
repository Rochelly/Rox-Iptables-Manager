def  getServiceName(fileName):
    with open(fileName) as arquivo:
        for linha in arquivo:
            if linha.startswith('NAME='):
                nome = linha.strip().split('=')[1]
                break
    return nome


def  getServiceIP(fileName):
    with open(fileName) as arquivo:
        for linha in arquivo:
            if linha.startswith('IP='):
                nome = linha.strip().split('=')[1]
                break
    return nome