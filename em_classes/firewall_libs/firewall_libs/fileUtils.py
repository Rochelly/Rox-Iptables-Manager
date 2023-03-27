import os
import datetime

#busca uma chave em um arquivo e retorna o valor da chave
def  getInFIle(fileName,key):
    with open(fileName) as arquivo:
        value=''
        for linha in arquivo:
            if linha.startswith(f'{key}='):
                value = linha.strip().split('=')[1]
                break
    return value

# Retorna a lista de arquivos modificados de um determinado diretório
def getChangedFiles(dir_path):
    
    # Cria um arquivo auxiliar para armazenar a data da última verificação
    last_checked_file = 'firewall_libs/last_checked.txt'

    # Obtém a data da última verificação a partir do arquivo auxiliar ou usa uma data antiga se não existir
    if os.path.exists(last_checked_file):
        with open(last_checked_file, 'r') as f:
            last_checked = datetime.datetime.fromisoformat(f.read().strip())
    else:
        last_checked = datetime.datetime.fromisoformat('2000-01-01 00:00:00')

    # Lista os arquivos no diretório
    files = os.listdir(dir_path)

    # Cria uma lista para armazenar os arquivos que foram modificados
    changed_files = []

    # Verifica a data de modificação de cada arquivo e adiciona na lista de arquivos modificados se foi modificado após a última verificação
    for file in files:
        file_path = os.path.join(dir_path, file)
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        if mod_time > last_checked and os.path.splitext(file)[-1] == '.fw':
            changed_files.append(file)

    # Atualiza a data da última verificação no arquivo auxiliar
    with open(last_checked_file, 'w') as f:
        f.write(datetime.datetime.now().isoformat())

    # Retorna a lista de arquivos modificados
    return changed_files

def writeFiles(lista_strings, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for linha in lista_strings:
            arquivo.write(linha + '\n')

#cria um aquivo com a lista de arquivos do tipo  .fw de um determinado diretório
def createFilesList(dir_path,filename):
    files = os.listdir(dir_path)
    filesChains=[]
    for file in files:
        if file.endswith('.fw'):
            chain=getInFIle(dir_path+file,'NAME')
            filesChains.append(f'{file}={chain}')
    writeFiles(filesChains,filename)


def comparar_arquivos(ald, new):
    with open(ald, 'r') as f1, open(new, 'r') as f2:
        linhas1 = set(f1.readlines())
        linhas2 = set(f2.readlines())
        linhas_diferentes = linhas1 - linhas2
    return list(linhas_diferentes)



def checkDeletedFiles(dirPathServices,serviceType):
    oldFileName=serviceType+'.old'
    newFileName=serviceType+'.new'
    listDeletedFiles=[]
    if os.path.exists(oldFileName):
        createFilesList(dirPathServices,newFileName)
        listDeletedFiles= comparar_arquivos(oldFileName,newFileName)
        os.remove(oldFileName)
        os.rename(newFileName,oldFileName)
    else:
        createFilesList(dirPathServices,oldFileName)
    return listDeletedFiles
    





#dirPathServices = '../services-rules-files/'

#print(checkDeletedFiles(dirPathServices,'Services'))

#createFilesList(dirPathServices,'Services.list')

#print(comparar_arquivos('../services-rules-files/antes','../services-rules-files/depois'))