# Aviso
Este programa nao possui garantia nenhuma, use por sua conta e risco.
# Descrição
Script para python que permite saber a relação nirf-nome de imoveis
declarados em um ano mas nao em outro. ainda outros dados uteis como
quantidade de declarações feitas nos anos comparados e total de
declarações feitas só num ano mas nao no outro.
Esse programa foi testado com python 3.8.6 no windows 7.
# Exemplo
Declarações feitas em 2022 mas nao em 2023. resultando em
arquivo de texto com os nomes dos contribuintes e os respectivos nirfs
que foram declarados com o programa itr 2022 mas ainda nao foram
feitos com o itr 2023, assim fica facil saber quem falta fazer quando
a quantidade de declarações feitas todo ano passa das centenas.
```
python itr-util --ano1 2022 --ano2 2023 --saida saida.txt
```
# Parâmetros
--ano1, --ano2 e --saida, para, respectivamente, o ano a ser usado como guia, o ano a ser comparado com o ano guia e ser vefificado quanto a declarações nao feitas e o caminho do arquivo de saida (use \\ para windows).
# Uso
Apos clonar, use python itr-util no diretorio.
