import xml.etree.ElementTree as ET
import os
import filecmp
from datetime import date
import argparse

parser = argparse.ArgumentParser(description='Mostra quem falta fazer a declaração do ITR.')
parser.add_argument('--ano1', default='2022', type=int, help='Ano do ITR a ser tomado como guia')
parser.add_argument('--ano2', default='2023', type=int, help='Ano do ITR a ser analizado')
parser.add_argument('--saida', default='C:\\Users\\Vitor\\Documents\\saida.txt', help='Caminho do arquivo no qual será escrito o relatório')
args = parser.parse_args()
ano1 = args.ano1
ano2 = args.ano2
saida = args.saida
dados1 = f'C:\\Arquivos de Programas RFB\\ITR{ano1}\\aplicacao\\dados'
dados2 = f'C:\\Arquivos de Programas RFB\\ITR{ano2}\\aplicacao\\dados'
with open(saida, 'w') as saida:
    now = date.today().strftime("%d/%m/%y")
    saida.write(f'ITR {ano1} feito mas {ano2} não feito, em {now}\n\n')
    comparador = filecmp.dircmp(dados1, dados2)
    listaDiferença = comparador.left_only
    total1 = len(comparador.left_list)
    total2 = len(comparador.right_list)
    total = len(listaDiferença)
    saida.write(f'quantidade {ano1}: {total1}\n')
    saida.write(f'quantidade {ano2}: {total2}\n')
    saida.write(f'quantidade: {total}\n\n')
    saida.write('NIRF          NOME\n')
    for dir in listaDiferença:
        dec = os.path.join(dados1, dir) + f'\\{dir}.xml'
        tree = ET.parse(dec)
        root = tree.getroot()
        nome = root[0][0].attrib['nomeContribuinte']
        nirf = root[0][0].attrib['nirf']
        saida.write(f'{nirf}   {nome}\n')

