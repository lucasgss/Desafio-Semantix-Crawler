# Desafio-Semantix-Crawler
Repository with the resolution of the technical challenge of the company Semantix

# Challenge Description

O profissional deverá criar um código que realize o seguinte crawler
Visão Geral
Os dados iniciais a serem capturados são referentes a cotações de:
1. ações que compõem o iBovespa
(https://www.investing.com/equities/StocksFilter?index_id=17920)
com os seguintes campos: name, last_rs, high_rs, low_rs, chg, chg%, vol, time;
2. ações que compõem a Nasdaq
(https://www.investing.com/equities/StocksFilter?index_id=20) com os
seguintes campos: name, last_usd, high_usd, low_usd, chg, chg%, vol, time;
3. dólar (em relação ao Real) do link (https://m.investing.com/currencies/usd-brl) com
os seguintes campos: currency, value, change, perc, e timestamp.
Dados importantes:

• As capturas (1, 2, 3) devem ser independentes e ocorrer a cada 2 min.

• Os arquivos das capturas (2 e 3) devem ser processados para conversão dos
valores de Dólares(US$) para Reais (R$), resultando num arquivo, cujo nome
contém o timestamp e com os seguintes campos: name, last_rs, high_rs,
low_rs, last_usd, high_usd, low_usd, chg, chg_perc, vol, time.

• Os dados deverão ser inseridos em uma base de dados relacional, usando o
SQLite. No código deverá constar a criação das bases de dados e a criação das
tabelas.

• O código deverá estar encapsulado dentro de um Docker.

• O código deverá ser realizado em Python 3.
