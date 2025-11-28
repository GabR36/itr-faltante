# Aviso
Este programa nao possui garantia nenhuma, use por sua conta e risco.

# Descrição
Script Python que busca nos dados de declarações de Imposto
Territorial Rural (ITR) feitas no seu computador e gera relatórios
úteis, como relação de quem falta fazer a declaração com base em quem
fez em algum outro ano; procura de declarações feitas com base no nirf
ou cpf, quantidade de declarações feitas, porcentagem de isentos, etc.

Esse programa foi testado com python 3.8.6 no windows 7, talvez o
código tenha que ser mudado para atender ao seu caso de uso.

# Funcionalidades
```
> python.exe .\itr-util2.py --help
usage: itr-util2.py [-h]
{diff,procura,importa,info-cpf,nome-cpf,estat-ano,abandonados} ...

Ferramenta para análise de ITR.

positional arguments:
  {diff,procura,importa,info-cpf,nome-cpf,estat-ano,abandonados}
    diff                Mostra quem falta fazer a declaração do ITR.
    procura             Mostra anos do ITR em que se tem informações
    importa             Importa os dados para um banco SQLite
    info-cpf            Mostra as informações relevantes de todos os
ITRs de um ano a partir de CPF
    nome-cpf            Procura CPF na base de dados por meio do nome
    estat-ano           Mostra estatisticas do ITR sobre um ano
    abandonados         Mostra quem teve algum ITR que não foram
transmitidos

optional arguments:
  -h, --help            show this help message and exit
```

# Dependências
- Python 3.8.6+
- Tabulate (Python package)