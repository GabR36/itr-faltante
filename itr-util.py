import xml.etree.ElementTree as ET
import os
import filecmp
from datetime import date

dados2022 = 'C:\\Arquivos de Programas RFB\\ITR2022\\aplicacao\\dados'
dados2023 = 'C:\\Arquivos de Programas RFB\\ITR2023\\aplicacao\\dados'
saida = 'C:\\Users\\Vitor\\Documents\\codigo\\saida.txt'
with open(saida, 'w') as saida:
    now = date.today()
    saida.write(f'ITR 2022 feito mas 2023 não feito, em {now.strftime("%d/%m/%y")}\n\n')
    comparador = filecmp.dircmp(dados2022, dados2023)
    listaDiferença = comparador.left_only
    total2022 = len(comparador.left_list)
    total2023 = len(comparador.right_list)
    total = len(listaDiferença)
    saida.write(f'quantidade 2022: {total2022}\n')
    saida.write(f'quantidade 2023: {total2023}\n')
    saida.write(f'quantidade: {total}\n\n')
    saida.write('NIRF          NOME\n')
    for dir in listaDiferença:
        dec = os.path.join(dados2022, dir) + f'\\{dir}.xml'
        tree = ET.parse(dec)
        root = tree.getroot()
        nome = root[0][0].attrib['nomeContribuinte']
        nirf = root[0][0].attrib['nirf']
        saida.write(f'{nirf}   {nome}\n')

