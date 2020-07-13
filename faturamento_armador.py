# -*- coding: utf-8 -*-
import glob,os
from datetime import datetime
# from pandas import read_csv
retorno = open('C:\\armador\\faturamento_5.csv','w+')
os.chdir('C:\\armador\\arq\\')
for file in glob.glob("*.*"):
    caminho_arquivo = 'C:\\armador\\arq\\'+file
    data_arquivo = os.path.getmtime(caminho_arquivo)
    data_str = datetime.fromtimestamp(data_arquivo)

    mes_arquivo = str(data_str)[5:7]
    ano_arquivo = str(data_str)[0:4]
    print(data_str)
    print(ano_arquivo)

    if ((int(mes_arquivo)>11) | (int(ano_arquivo)==2017) ):
   # if ((int(ano_arquivo) == 2017)):
        arquivo = open(caminho_arquivo,'r+')

        nome_arq = file.split('_')
        navio = nome_arq[1]
        operador = nome_arq[4]

        porto1 = ''
        porto2 = ''
        nome_tipo = ''

        for linha in arquivo:
            tipo = linha[0:2]
            if (tipo[1] == '5'):
                nome_tipo = 'Importacao'
            elif (tipo[1]=='7'):
                nome_tipo = 'Exportacao'
            elif (tipo[1]=='9'):
                nome_tipo = 'Passagem'
            elif (tipo[1]=='G'):
                nome_tipo = 'Transbordo Imp'
            elif (tipo[1]=='B'):
                nome_tipo = 'Transbordo Exp'

            num_ce=""

            # print(tipo[1])
            if ((tipo=="M5") | (tipo=="M7") | (tipo=="M9") | (tipo=="MG") | (tipo=="MB")):
                porto1 = linha[1166:1171]
                porto2 = linha[1171:1176]
            if ((tipo=="C5") | (tipo=="C7") | (tipo=="C9") | (tipo=="CG") | (tipo=="CB")):
                num_ce = linha[20:35].rstrip('\n')
                num_bl = linha[1181:].rstrip('\n')
                if (num_ce.strip()!=''):
                    retorno.write(operador+';'+num_bl+';'+num_ce+';'+navio+';'+porto1+';'+porto2+';'+nome_tipo+';'+str(data_str)+';'+file+'\n')
        arquivo.close()

retorno.close()
# for fn in os.listdir('c:\\python\\armador\\.txt'):
#     print(fn)