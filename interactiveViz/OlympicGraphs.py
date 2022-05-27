import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import numpy as np

class OlympicGraphs():

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

    def graph1(self, app):
        """
        Esse é um gráfico com as seguintes características:
        Eixo x: Altura
        Eixo y: Peso
        Filtros:
            Dropdown: Tipo de Esporte
            RangeSlider: Faixa de tempo
        """

        #Essas são funções aninhadas dentro da função graph1. São funções de utilidade ou de callback

        def getGraphFigWith(sportType, minTime, maxTime):
            athletesOfSport = self._athletesDf[self._athletesDf['Sport']==sportType]
            athletesWithNoMedal = athletesOfSport['Medal'] == 'None'
            athletesWithMedal = athletesOfSport[~athletesWithNoMedal]

            athletesWithMedalOnTimeRange = athletesWithMedal[
                    (athletesWithMedal['Year'] >= minTime) & (athletesWithMedal['Year'] <= maxTime)
                ]

            fig = px.scatter(athletesWithMedalOnTimeRange, x="Height", y="Weight", hover_name="Name",
                                color='Medal',
                                #Para cada valor diferente na coluna Medal, eu defino uma cor hex para a bolinha
                                color_discrete_map={ 
                                    'Bronze':'#96642f',
                                    'Gold':'#f5dd05',
                                    'Silver':'#98c5f5'
                                    })
            
            return fig

        #Como recebi o app criado em app.py por parâmetro, posso adicionar callbacks a ele

        @app.callback(
            Output('graph1','figure'),
            Input('graph1SportsDropdown','value'),
            Input('graph1Slider','value')
        )
        def updateGraph1(sportType, timeRange):

            fig = getGraphFigWith(sportType, timeRange[0], timeRange[1])

            return fig
        
        @app.callback(
                Output('graph1Slider','min'),
                Output('graph1Slider','max'),
                Output('graph1Slider','value'),
                Input('graph1SportsDropdown','value')
        )
        def updateGraph1Slider(sportType):
            athletesOfSport = self._athletesDf[self._athletesDf['Sport']==sportType]
            athletesWithNoMedal = athletesOfSport['Medal'] == 'None'
            athletesWithMedal = athletesOfSport[~athletesWithNoMedal]

            yearsOfMedalists = np.sort(athletesWithMedal['Year'].unique())
            minYear = np.min(yearsOfMedalists)
            maxYear = np.max(yearsOfMedalists)
            value = [minYear, maxYear]
            return minYear, maxYear, value 

        #Aqui começa o display default do gráfico. Ele será alterado de acordo com os callbacks definidos acima    
            
        defaultSportType ='Football'
        athletesOfSport = self._athletesDf[self._athletesDf['Sport']==defaultSportType]
        athletesWithNoMedal = athletesOfSport['Medal'] == 'None'
        athletesWithMedal = athletesOfSport[~athletesWithNoMedal]

        yearsOfMedalists = np.sort(athletesWithMedal['Year'].unique())
        minYear = np.min(yearsOfMedalists)
        maxYear = np.max(yearsOfMedalists)
        
        fig = getGraphFigWith(defaultSportType, minYear, maxYear)
        grafico = dcc.Graph(
            id='graph1',
            figure=fig
        )

        sportsTypeDropdown = dcc.Dropdown(np.sort(self._athletesDf['Sport'].unique()), 
                                            'Football', id='graph1SportsDropdown'
                                        )
        
        yearsSlider = dcc.RangeSlider(minYear, maxYear, value=[minYear, maxYear],
                                        marks=None,
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        allowCross=False,
                                        id='graph1Slider'
                                    )

        myGraphDiv = html.Div(children=[
            sportsTypeDropdown,
            grafico,
            html.Label('Faixa de tempo'),
            yearsSlider
        ])

        return myGraphDiv