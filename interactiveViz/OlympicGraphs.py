import pandas as pd
import plotly.express as px
from dash import dcc

class OlympicGRaphs():
    def __init__(self, athletesFilePath:str, regionsFilePath:str):
        self._athletesFilePath = athletesFilePath
        self._athletesDf = pd.read_csv(self._athletesFilePath)

        self._regionsFilePath = regionsFilePath
        self._regionsDf = pd.read_csv(self._regionsFilePath)
    
    #Pode receber parâmetros como coisas para serem usadas em filtros
    def getGraficoExemplo(self):
        """
        Esse é um exemplo de função que será chamada pelo app Dash e que deve retornar um objeto dcc.Graph.
        Basicamente, realizamos quaisquer agrupamentos e filtragens sejam necessários, usamos o plotly.express para gerar o gráfico
        e retornamos um objeto dcc.Graph irá conter o gráfico de fato e será exibido no HTML.
        Ver o exemplo https://dash.plotly.com/layout#more-about-visualization.
        Se quiser estilizar mais o gráfico, talvez seja necessário construí-lo por partes e "do zero".
        Ver exemplo: https://plotly.com/python/line-and-scatter/#style-scatter-plots
        """

        fig = px.scatter(self._athletesDf, x="Height", y="Weight", color="Medal", 
                        color_discrete_map={ #Para cada valor diferente na coluna Medal, eu defino um valor para a bolinha
                                "None":'#a3a0a0',
                                'Bronze':'#96642f',
                                'Gold':'#f5dd05',
                                #'Silver':'#ededeb'
                                'Silver':'#98c5f5'
                                }, 
                        hover_name="Name")
            
        grafico = dcc.Graph(
            id='Peso x Altura e Medalha',
            figure=fig
        )

        return grafico
