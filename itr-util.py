import xml.etree.ElementTree as ET
import os
import filecmp
from datetime import date
import argparse


parser = argparse.ArgumentParser(description='Mostra quem falta fazer a declaração do ITR.')
parser.add_argument('--ano1', default=str(date.today().year-1), type=int, help='ano do ITR a ser tomado como guia')
parser.add_argument('--ano2', default=str(date.today().year), type=int, help='ano do ITR a ser analizado')
parser.add_argument('--saida', default='saida.txt', help='caminho do arquivo o qual será escrito o relatorio')
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
    listaAno2 = comparador.right_list
    listaAno1 = comparador.left_list
    total1 = len(listaAno1)
    total2 = len(listaAno2)
    total = len(listaDiferença)
    saida.write(f'quantidade {ano1}:     {total1}\n')
    saida.write(f'quantidade {ano2}:     {total2}\n')
    saida.write(f'quantidade faltante: {total}\n')
    semIncra = 0
    isento = 0
    for dir in listaAno2:
        if dir != "iddeclaracoes.conf" and dir != "iddeclaracoes.xml" and dir != "release_properties.xml":
            dec = os.path.join(dados2, dir) + f'\\{dir}.xml'
            tree = ET.parse(dec)
            root = tree.getroot()
            if (root[0].attrib['codigoIncra'] == ""):
                semIncra = semIncra + 1
            if root[0].attrib['isento'] == "1":
                isento = isento + 1
                saida.write(f'% com incra:         {round((total2 - semIncra)/total2*100, 2)}\n')
                saida.write(f'% isento:            {round(isento/total2*100, 2)}\n\n')
                
    saida.write('NIRF          NOME\n')

    dicFaltantes = {}
    for dir in listaDiferença:
        dec = os.path.join(dados1, dir) + f'\\{dir}.xml'
        tree = ET.parse(dec)
        root = tree.getroot()
        nome = root[0][0].attrib['nomeContribuinte']
        nirf = root[0][0].attrib['nirf']
        dicFaltantes[nirf] = nome
        # saida.write(f'{nirf}   {nome}\n')
    lista_registros = [(nome, nirf) for nirf, nome in dicFaltantes.items()]
    lista_registros_ordenada = sorted(lista_registros, key=lambda x: x[0])
    for nome, nirf in lista_registros_ordenada:
        saida.write(f'{nirf}   {nome}\n')
