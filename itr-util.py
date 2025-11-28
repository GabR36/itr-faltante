import xml.etree.ElementTree as ET
import os
from datetime import date
import argparse
import sqlite3
from tabulate import tabulate
from itertools import islice
import re

parser = argparse.ArgumentParser(description='Ferramenta para análise de ITR.')
subparsers = parser.add_subparsers(dest='comando', required=True)

anoAtual = default=date.today().year
anoPassado = anoAtual - 1

parser_diff = subparsers.add_parser('diff', help='Mostra quem falta fazer a declaração do ITR.')
parser_diff.add_argument('--ano1', type=str, default=str(anoPassado), help='Ano do ITR a ser tomado como guia')
parser_diff.add_argument('--ano2', type=str, default=str(anoAtual), help='Ano do ITR a ser analisado')
parser_diff.add_argument('--ordem', default='alf', help='ordem: alf: alfabetica, isent: não isentos primeiro')
parser_diff.add_argument('--saida', default='saida.txt', help='caminho do arquivo o qual será escrito o relatorio')

parser_procura = subparsers.add_parser('procura', help='Mostra anos do ITR em que se tem informações')
parser_procura.add_argument('--nirf', type=str, help='NIRF a ser pesquisado')
parser_procura.add_argument('--cpf', type=str, help='CPF a ser pesquisado')

parser_importa = subparsers.add_parser('importa', help='Importa os dados para um banco SQLite')
parser_importa.add_argument('--db', default='itr.db', help='Caminho do arquivo SQLite (padrão: itr.db)')

parser_infocpf = subparsers.add_parser('info-cpf', help='Mostra as informações relevantes de todos os ITRs de um ano a partir de CPF')
parser_infocpf.add_argument('--ano', type=str, default=str(anoPassado), help='ano a ser pesquisado')
parser_infocpf.add_argument('--cpf', type=str, help='CPF a ser pesquisado')

parser_nomecpf = subparsers.add_parser('nome-cpf', help='Procura CPF na base de dados por meio do nome')
parser_nomecpf.add_argument('--nome', type=str, help='Nome a ser pesquisado')

parser_estatano = subparsers.add_parser('estat-ano', help='Mostra estatisticas do ITR sobre um ano')
parser_estatano.add_argument('--ano', type=str, default=str(anoAtual), help='ano a ser pesquisado')

parser_aband = subparsers.add_parser('abandonados', help='Mostra quem teve algum ITR que não foram transmitidos')
parser_aband.add_argument('--ano', type=str, default=str(anoAtual), help='ano a ser pesquisado')

args = parser.parse_args()

installDir = 'C:'
itrDir = f'{installDir}\\Arquivos de Programas RFB'

# iterar por todos os anos do itr e por todos itrs feitos e armazenar numa estrutura de dados
itrAnosDir = [item for item in os.listdir(itrDir) if item.startswith('ITR')]
dados = []
for ano in itrAnosDir:
    fullPath = f'{itrDir}\\{ano}\\aplicacao\\dados'
    transPath = f'{itrDir}\\{ano}\\transmitidas'
    nirfsTransmitidos = [
        re.search(r'^(\d+)-ITR', x).group(1) 
        for x in os.listdir(transPath) 
        if x.endswith('.DEC') and re.search(r'^(\d+)-ITR', x)
    ]
    excludeFiles = ['iddeclaracoes.conf', 'iddeclaracoes.xml', 'release_properties.xml']
    nirfDirs = [x for x in os.listdir(fullPath) if x not in excludeFiles]
    for nirf in nirfDirs:
        # ver se foi transmitido
        itrTransmitido = False
        for arquivo in nirfsTransmitidos:
            if arquivo == nirf:
                itrTransmitido = True
                break
            
        dec = os.path.join(fullPath, nirf) + f'\\{nirf}.xml'
        tree = ET.parse(dec)
        root = tree.getroot()
        dados.append({
            'ano': ano.replace('ITR', ''),
            'transmitido': itrTransmitido,
            'nirf': nirf,
            'incra': root[0].attrib['codigoIncra'],
            'isento': root[0].attrib['isento'],
            'motivo': root[0].attrib['motivoIsencao'],
            'area': root[0].attrib['areaTotal'],
            'logradouro': root[0].attrib['logradouro'],
            'condomino': root[0].attrib['pertenceCondominio'],
            'cpf': root[1].attrib['ni'].replace(".", "").replace("-", ""),
            'nome': root[1].attrib['nomeContribuinte'],
            'data_nasc': root[1].attrib['dataNascimento'],
            'logradouroCont': root[1].attrib['logradouro'],
            # utilização
            #'areaTotalImovel': root[4][0].attrib['areaTotalImovel'],
            'areaPreservacaoPermanente': root[4][0].attrib['areaPreservacaoPermanente'],
            'areaReservaLegal': root[4][0].attrib['areaReservaLegal'],
            'areaReservaParticular': root[4][0].attrib['areaReservaParticular'],
            'areaInteresseEcologico': root[4][0].attrib['areaInteresseEcologico'],
            'areaServidaoFlorestal': root[4][0].attrib['areaServidaoFlorestal'],
            'areaFlorestasNativas': root[4][0].attrib['areaFlorestasNativas'],
            'areaAlagada': root[4][0].attrib['areaAlagada'], 
            #'areaTributavel': root[4][0].attrib['areaTributavel'],
            'areaOcupada': root[4][0].attrib['areaOcupada'],
            #'areaAproveitavel': root[4][0].attrib['areaAproveitavel'],
            'areaProdutosVegetais': root[4][1].attrib['areaProdutosVegetais'],
            'areaEmDescanso': root[4][1].attrib['areaEmDescanso'],
            'areaReflorestamento': root[4][1].attrib['areaReflorestamento'],
            'areaPastagens': root[4][1].attrib['areaPastagens'],
            'areaExploracaoExtrativa': root[4][1].attrib['areaExploracaoExtrativa'],
            'areaAtividadeGranjeira': root[4][1].attrib['areaAtividadeGranjeira'],
            'areaFrustracaoSafra': root[4][1].attrib['areaFrustracaoSafra'],
            'areaUtilizadaPelaAR': root[4][1].attrib['areaUtilizadaPelaAR'],
            # imposto
            'valorTotalImovel': root[6].attrib['valorTotalImovel'],
            'valorBenfeitorias': root[6].attrib['valorBenfeitorias'],
            'valorCulturas': root[6].attrib['valorCulturas'],
            #'valorTerraNua': root[6].attrib['valorTerraNua'],
            'impostoDevido': root[6].attrib['impostoDevido'],
        })

# controllers

def extrair_parte(dicionario, chave_inicio, chave_fim):
    """Extrai uma parte do dicionário da chave_inicio até chave_fim (inclusive)"""
    chaves = list(dicionario)
    inicio = chaves.index(chave_inicio)
    fim = chaves.index(chave_fim)
    
    fatia = chaves[inicio:fim+1]
    return {chave: dicionario[chave] for chave in fatia}
 
def anosNirf (nirf, dados):
    resultado = [registro['ano'] for registro in dados if registro['nirf'] == nirf]
    resultado = sorted(resultado, key=int)
    return resultado

def anosCpf (cpf, dados):
    cpf = cpf.replace(".", "").replace("-", "")
    resultado = list({registro['ano'] for registro in dados if registro['cpf'] == cpf})
    resultado = sorted(resultado, key=int)
    return resultado
     
def infoCpf (cpf, ano, dados):
    cpf = cpf.replace(".", "").replace("-", "")
    resultado = [registro for registro in dados if registro['ano'] == ano and registro['cpf'] == cpf]
    return resultado
           
def nomeCpf (nome, dados):
    cpf = list({registro['cpf'] for registro in dados if registro['nome'] == nome})
    return cpf

def diff (ano1, ano2, ordem, dados):
    campos = ['nirf', 'nome', 'area', 'isento', 'motivo', 'impostoDevido', 'valorTotalImovel']
    registros_ano1 = [
        {k: d[k] for k in campos if k in d}
        for d in dados if d['ano'] == ano1 and d['transmitido'] == True
    ]
    registros_ano2 = [
        {k: d[k] for k in campos if k in d}
        for d in dados if d['ano'] == ano2
    ]
 
    nirfsNomeAno2 = {d['nirf'] for d in registros_ano2}
    
    diferenca = [d for d in registros_ano1 if d['nirf'] not in nirfsNomeAno2]
    
    if (ordem == 'alf'):
        ordenado = sorted(diferenca, key=lambda x: x['nome'])
    elif (ordem == 'isent'):
        ordenado = sorted(diferenca, key=lambda x: (x['isento'] == '1', x['nome']))
    return ordenado
    
def importa_para_sqlite(dados, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    colunas = dados[0].keys()
    campos_sql = ", ".join([f"{col} TEXT" for col in colunas])
    cur.execute(f"CREATE TABLE IF NOT EXISTS itr ({campos_sql});")

    for registro in dados:
        valores = tuple(str(registro[col]) for col in colunas)
        placeholders = ", ".join(["?"] * len(colunas))
        cur.execute(f"INSERT INTO itr VALUES ({placeholders})", valores)

    conn.commit()
    conn.close()
    print(f"Importação finalizada para {db_path}")
    print(dados[0])
    
def estatAno (ano, dados):
    itrsAno = [d for d in dados if d['ano'] == ano and d['transmitido'] == True]
    qtde = len(itrsAno)
    com_incra = [d for d in itrsAno if d['incra'].strip() != '']
    isento = [d for d in itrsAno if d['isento'] == '1']
    pctg_incra = round(len(com_incra)/qtde * 100, 2)
    pctg_isento = round(len(isento)/qtde * 100, 2)
    
    stats = {
        'qtde': qtde,
        'pctg_incra': pctg_incra,
        'pctg_isento': pctg_isento
    }
    
    return stats
    
def aband (ano, dados):
    itrsAno = [
        (item['nome'], item['cpf']) 
        for item in dados 
        if not item['transmitido'] and item['ano'] == ano
    ]
    pessoas = list(set(itrsAno))
    
    pessoas_ordenadas = sorted(pessoas, key=lambda x: x[0])
    
    return pessoas_ordenadas
    

    
# views

if args.comando == 'diff':
    ano1 = args.ano1
    ano2 = args.ano2
    ordem = args.ordem
    saida = args.saida
    stats1 = estatAno(ano1, dados)
    stats2 = estatAno(ano2, dados)
    stats1['ano'] = ano1
    stats2['ano'] = ano2
    print(stats1)
    itrList = diff(ano1, ano2, ordem, dados)
    campos = ['nirf', 'nome', 'area']
    itrListTxt = [
        {k: d[k] for k in campos if k in d}
        for d in itrList
    ]
    headers = {
        "nirf": "nirf", 
        "nome": "nome", 
        "area": "area", 
        "isento": "isento", 
        "motivo": "motivo", 
        "impostoDevido": "imposto", 
        "valorImovel": "valor Imovel"
    }
    headersTxt = {
        "nirf": "nirf", 
        "nome": "nome"
    }
    headersStats = {
        "ano": "ano",
        "qtde": "Quantidade",
        "pctg_incra": "% incra",
        "pctg_isento": "% isento"
    }
    stats = tabulate([stats1, stats2], headers=headersStats, tablefmt="simple")
    tabelaConsole = tabulate(itrList, headers=headers, tablefmt="simple")
    tabelaTxt = tabulate(itrListTxt, headers=headersTxt, tablefmt="simple")
    with open(saida, 'w') as saida:
        saida.write(stats)
        saida.write('\n\n')
        saida.write(tabelaTxt)
    print(tabelaConsole)

elif args.comando == 'procura':
    if args.nirf:
        nirf = args.nirf
        anosList = anosNirf(nirf, dados)
        tabela = [[valor] for valor in anosList]
        print(tabulate(tabela, headers=["Ano"], tablefmt="simple"))
    elif args.cpf:
        cpf = args.cpf
        anosList = anosCpf(cpf, dados)
        tabela = [[valor] for valor in anosList]
        print(tabulate(tabela, headers=["Ano"], tablefmt="simple"))
       
elif args.comando == 'info-cpf':
    ano = args.ano
    cpf = args.cpf
    itrList = infoCpf(cpf, ano, dados)
    for itr in itrList:
        geral = extrair_parte(itr, 'ano', 'logradouroCont')
        print(tabulate(geral.items(), headers=['Geral', 'Valor'], tablefmt="grid"))
        if (itr['isento'] != '1'):
            utilizacao = extrair_parte(itr, 'areaPreservacaoPermanente', 'areaUtilizadaPelaAR')
            imposto = extrair_parte(itr, 'valorTotalImovel', 'impostoDevido')

            print(tabulate(utilizacao.items(), headers=['Utilizacao', 'Valor'], tablefmt="grid"))
            print(tabulate(imposto.items(), headers=['Imposto', 'Valor'], tablefmt="simple"))
        print('-'*100)

elif args.comando == 'nome-cpf':
    nome = args.nome
    cpfList = nomeCpf(nome, dados)
    tabela = [[valor] for valor in cpfList]
    print(tabulate(tabela, headers=["CPF"], tablefmt="simple"))
        
elif args.comando == 'importa':
    importa_para_sqlite(dados, args.db)
    
elif args.comando == 'estat-ano':
    ano = args.ano
    stats = estatAno(ano, dados)
    headers = {
        "qtde": "Quantidade",
        "pctg_incra": "% incra",
        "pctg_isento": "% isento"
    }
    print(tabulate([stats], headers=headers, tablefmt="simple"))
    
elif args.comando == 'abandonados':
    ano = args.ano
    listaPessoas = aband(ano, dados)
    print(tabulate(listaPessoas, headers=['nome', 'cpf'], tablefmt="simple"))
