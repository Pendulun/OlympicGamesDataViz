# OlympicGamesDataViz

Create an virtual-environment and install the libs at the requirements.txt

## Análises Consideradas

POSSÍVEIS PERGUNTAS PARA RESPONDERMOS E RELAÇÕES INTERESSANTES PARA VISUALIZAR no [docs](https://docs.google.com/document/d/1SVtw_nfh-OvmWbxfb1T4aiiRh3xMCr-zcz467Rlmwpc/edit)

Análises estruturadas por dificuldade e explicações no [docs](https://docs.google.com/document/d/1SVtw_nfh-OvmWbxfb1T4aiiRh3xMCr-zcz467Rlmwpc/edit?usp=sharing)

# Dash Tutorial

O tutorial oficial de Dash pode ser encontrado no [site oficial](https://dash.plotly.com/installation)

# Plotly Tutorial

O tutorial oficial de Plotly pode ser encontrado no [site oficial](https://plotly.com/python/plotly-express/)

# Sobre o repositório

O repositório foi pensado para poder ser reproduzível, já que realizamos tratamentos e análises de dados a partir do [dataset original](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results).

## Configurações globais

O arquivo Config.py possui algumas constantes relativas a caminhos dos dados tanto antes quanto depois do seu tratamento.


## Datasets

Existem duas pastas com os datasets. O primeiro deles (originalDataset/) possui o dataset original. O segundo (cleanedDataSet/), possui o dataset após realizarmos eventuais tratamentos. Esse tratamento dos dados é realizado no arquivo cleanDataset.py.

## Análises dos dados

A pasta initialAnalisys/ possui, atualmente, um jupyter-notebook sobre a qualidade dos dados. Ainda falta realizar uma análise exploratória de fato.

## Visualização Interativa

A pasta interactiveViz/ deve conter os arquivos necessários para executar o servidor Dash que possui as visualizações interativas com o Plotly.
