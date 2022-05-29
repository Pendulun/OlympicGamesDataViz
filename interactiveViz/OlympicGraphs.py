import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import numpy as np

class OlympicGraphs():

    def __init__(self, athletesFilePath:str, regionsFilePath:str, nocCountryContinentFilePath:str, yearCountryHostFilePath:str):
        self._athletesFilePath = athletesFilePath
        self._athletesDf = pd.read_csv(self._athletesFilePath)

        # Para regular o range dos anos
        self._athletesDf = self._athletesDf[self._athletesDf['Year'].isin(range(0,2040))]

        #Commom filters
        self._athletesWithMedals = self._athletesDf[self._athletesDf['Medal'] != 'None']

        self._regionsFilePath = regionsFilePath
        self._regionsDf = pd.read_csv(self._regionsFilePath)

        self._nocCountryContinent = nocCountryContinentFilePath
        self._nocCountryContinentDf = pd.read_csv(self._nocCountryContinent)

        self._yearCountryHost = yearCountryHostFilePath
        self._yearCountryHostDf = pd.read_csv(self._yearCountryHost)

        #Graph3 stuff so dont make them everytime
        self.meanMedalsRegion = 0
        self.summerComparison = 0

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
            athletesOfSportWithMedal = self._athletesWithMedals[self._athletesWithMedals['Sport']==sportType]

            athletesWithMedalOnTimeRange = athletesOfSportWithMedal[
                    (athletesOfSportWithMedal['Year'] >= minTime) & (athletesOfSportWithMedal['Year'] <= maxTime)
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

            athletesOfSportWithMedal = self._athletesWithMedals[self._athletesWithMedals['Sport']==sportType]
            yearsOfMedalists = np.sort(athletesOfSportWithMedal['Year'].unique())
            minYear = np.min(yearsOfMedalists)
            maxYear = np.max(yearsOfMedalists)
            value = [minYear, maxYear]

            return minYear, maxYear, value 

        #Aqui começa o display default do gráfico. Ele será alterado de acordo com os callbacks definidos acima    
            
        defaultSportType ='Football'
        athletesOfSportWithMedal = self._athletesWithMedals[self._athletesWithMedals['Sport']==defaultSportType]
        yearsOfMedalists = np.sort(athletesOfSportWithMedal['Year'].unique())
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


    def graph2(self, app):
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
            athletesOfSportWithMedal = self._athletesWithMedals[self._athletesWithMedals['Sport']==sportType]

            athletesWithMedalOnTimeRange = athletesOfSportWithMedal[
                    (athletesOfSportWithMedal['Year'] >= minTime) & (athletesOfSportWithMedal['Year'] <= maxTime)
                ]

            fig = px.density_heatmap(athletesWithMedalOnTimeRange, x="Height", y="Weight", marginal_x = "histogram", marginal_y = "histogram", range_x = (140, 230), range_y = (40, 150))
            
            return fig

        #Como recebi o app criado em app.py por parâmetro, posso adicionar callbacks a ele

        @app.callback(
            Output('graph2','figure'),
            Input('graph2SportsDropdown','value'),
            Input('graph2Slider','value')
        )
        def updateGraph2(sportType, timeRange):

            fig = getGraphFigWith(sportType, timeRange[0], timeRange[1])

            return fig
        
        @app.callback(
                Output('graph2Slider','min'),
                Output('graph2Slider','max'),
                Output('graph2Slider','value'),
                Input('graph2SportsDropdown','value')
        )
        def updateGraph2Slider(sportType):
            athletesOfSportWithMedal = self._athletesWithMedals[self._athletesWithMedals['Sport']==sportType]

            yearsOfMedalists = np.sort(athletesOfSportWithMedal['Year'].unique())
            minYear = np.min(yearsOfMedalists)
            maxYear = np.max(yearsOfMedalists)
            value = [minYear, maxYear]
            return minYear, maxYear, value 

        #Aqui começa o display default do gráfico. Ele será alterado de acordo com os callbacks definidos acima    
            
        defaultSportType ='Football'
        athletesOfSportWithMedal = self._athletesWithMedals[self._athletesWithMedals['Sport']==defaultSportType]

        yearsOfMedalists = np.sort(athletesOfSportWithMedal['Year'].unique())
        minYear = np.min(yearsOfMedalists)
        maxYear = np.max(yearsOfMedalists)
        
        fig = getGraphFigWith(defaultSportType, minYear, maxYear)
        grafico = dcc.Graph(
            id='graph2',
            figure=fig
        )

        sportsTypeDropdown = dcc.Dropdown(np.sort(self._athletesDf['Sport'].unique()), 
                                            'Football', id='graph2SportsDropdown'
                                        )
        
        yearsSlider = dcc.RangeSlider(minYear, maxYear, value=[minYear, maxYear],
                                        marks=None,
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        allowCross=False,
                                        id='graph2Slider'
                                    )

        myGraphDiv = html.Div(children=[
            sportsTypeDropdown,
            grafico,
            html.Label('Faixa de tempo'),
            yearsSlider
        ])

        return myGraphDiv


    def graph3Aggregations(self):
        #Separando os anos em verão em inverno, importante para não dar conflito de datas depois.
        summerYearCountry = self._yearCountryHostDf[~self._yearCountryHostDf['Summer'].isna()]
        winterYearCountry = self._yearCountryHostDf[~self._yearCountryHostDf['Winter'].isna()]
        
        # Separando atletas em verão e inverno
        summerAthletes = self._athletesDf[self._athletesDf['Season'].isin(['Summer'])]
        winterAthletes = self._athletesDf[self._athletesDf['Season'].isin(['Winter'])]

        #TODO Acredito que pode criar uma tabela nova
        # Criando nova tabela, a dos atletas + o país hosteador do evento + continente do atleta + sub região do atleta
        summerOlimpWithHostCountry = pd.merge(summerAthletes, summerYearCountry[["Year","Country"]], how = "left", on = ["Year"])
        winterOlimpWithHostCountry = pd.merge(winterAthletes, winterYearCountry[["Year","Country"]], how = "left", on = ["Year"])
        summerOlimpWithHostCountry.rename(columns = {'Country':'HostCountry'}, inplace = True)
        winterOlimpWithHostCountry.rename(columns = {'Country':'HostCountry'}, inplace = True)
        summerAthletesCompleteRegions = pd.merge(summerOlimpWithHostCountry, self._nocCountryContinentDf[["NOC", "continent", "sub_region"]], how = "left",on = ["NOC"])
        winterAthletesCompleteRegions = pd.merge(winterOlimpWithHostCountry, self._nocCountryContinentDf[["NOC", "continent", "sub_region"]], how = "left",on = ["NOC"])
        
        # Selecionando apenas os medalhistas
        summerAthletesWithMedals = summerAthletesCompleteRegions[~summerAthletesCompleteRegions['Medal'].isna()]
        winterAthletesWithMedals = winterAthletesCompleteRegions[~winterAthletesCompleteRegions['Medal'].isna()]

        #TODO ESTÁ APENAS COM VERÃO, TEM AINDA DE FAZER INVERNO
        # Pegando apenas 1 medalhista por evento (pois em esportes com times, todos levam medalhas)
        # Exceto esportes individuais que distribuem mais medalhas bronze
        summerBoxJudoTaekwondoWrestling = summerAthletesWithMedals[summerAthletesWithMedals['Sport'].isin(['Judo', 'Taekwondo', 'Boxing', 'Wrestling'])]
        summerAthletesWithMedals = summerAthletesWithMedals[~summerAthletesWithMedals['Sport'].isin(['Judo', 'Taekwondo', 'Boxing', 'Wrestling'])]
        dfSummerMedalsAndRegions = summerAthletesWithMedals.drop_duplicates(subset = ["Event","Medal"],keep = "first")
        dfSummerMedalsAndRegions = pd.concat([dfSummerMedalsAndRegions, summerBoxJudoTaekwondoWrestling], axis=0)

        # Agrupando por ano e subregião
        summerCount = dfSummerMedalsAndRegions.groupby(['Year', 'continent']).agg('count').reset_index()
        self.meanMedalsRegion = summerCount.groupby(['continent'])['Medal'].agg('mean').reset_index()

        # Calculate Percentage
        self.meanMedalsRegion['Porcentagem da média geral de todos jogos'] = (self.meanMedalsRegion['Medal'] / 
                            self.meanMedalsRegion['Medal'].sum()) * 100

        self.summerComparison = dfSummerMedalsAndRegions.groupby(['Year'])

    #Pode receber parâmetros como coisas para serem usadas em filtros
    #graph3
    def graphMedalsByContinent(self, app):

        """
        Esse é um gráfico com as seguintes características:
        Eixo x: Continentes
        Eixo y: % de medalhas
        Filtros:
            Dropdown: Tipo de Esporte
            RangeSlider: Faixa de tempo
        """
        
        def getGraph(comparison_year):
            comparison_year = int(comparison_year)
            
            currSummerComparison = self.summerComparison.get_group(comparison_year).groupby(['continent']).agg('count').reset_index()
            currSummerComparison.rename(columns = {'Medal':'MedalComparison'}, inplace = True)
            
            currSummerComparison['Porcentagem do ano escolhido para comparação'] = (currSummerComparison['MedalComparison'] / 
                        currSummerComparison['MedalComparison'].sum()) * 100
            
            comparisonGraph = pd.merge(self.meanMedalsRegion, currSummerComparison[["continent","Porcentagem do ano escolhido para comparação"]], how = "left", on = ["continent"])

            # Criando a figura
            fig = px.bar(comparisonGraph, x=["Porcentagem da média geral de todos jogos", "Porcentagem do ano escolhido para comparação"], y="continent", orientation='h', barmode = 'group', labels={
                     "value": "Porcentagem de medalhas (%)",
                     "continent": "Continente",
                     "variable": "Variáveis"
                 },)
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            
            return fig

        @app.callback(
            Output('graphMedalsByContinent','figure'),
            Input('yearOlympDropdown','value'),
        )
        def updateGraph1(year):
            fig = getGraph(year)

            return fig
    
        #Aqui começa o display default do gráfico. Ele será alterado de acordo com os callbacks definidos acima
        self.graph3Aggregations()   
    
        defaultComparisonYear = 2016        
        fig = getGraph(defaultComparisonYear)

        grafico = dcc.Graph(
            id='graphMedalsByContinent',
            figure=fig
        )

        summerYearCountry = self._yearCountryHostDf[~self._yearCountryHostDf['Summer'].isna()]
        summerYears = summerYearCountry['Year'].astype(str)
        yearOlympDropdown = dcc.Dropdown(summerYears, 
                                            '2016', id='yearOlympDropdown'
                                        )

        myGraphDiv = html.Div(children=[
            yearOlympDropdown,
            grafico
        ])

        return myGraphDiv

    def graphMedalsByAge(self, app):
        
        def getDataOfSport(sportType:str):
            dfOfSport = 0

            if sportType == 'All':
                dfOfSport = self._athletesWithMedals
            else:
                dfOfSport = self._athletesWithMedals[self._athletesWithMedals['Sport'] == sportType]
            
            atletasPorIdadeMedalha = dfOfSport.groupby(["Sex", "Age", "Medal"])

            numVencedoresAgrupados = atletasPorIdadeMedalha.size().reset_index()
            numVencedoresAgrupados.rename(columns={0:'qtMedals'}, inplace=True)
            numVencedoresAgrupados['SexMedal'] = numVencedoresAgrupados['Sex'] + numVencedoresAgrupados['Medal']

            return numVencedoresAgrupados
        
        def getGraph4Figure(data):
            fig = px.line(data, x="Age", y="qtMedals", color="SexMedal", 
                        color_discrete_map={ #Para cada valor diferente na coluna SexMedal, eu defino um valor para a linha
                                "FSilver":'#eb1c1c',
                                'FBronze':'#fa9191',
                                'FGold':'#910101',
                                'MSilver':'#5967eb',
                                'MBronze': '#a5adf0',
                                'MGold': '#030d63'
                                },
                        )
            return fig
        
        @app.callback(
            Output('graph4','figure'),
            Input('graph4SportsDropdown','value'),
        )
        def attGraph4(sportType):
            numVencedoresAgrupados = getDataOfSport(sportType)
            fig = getGraph4Figure(numVencedoresAgrupados)
            return fig

        #Visualizaão padrão
        numVencedoresAgrupados = getDataOfSport('All')
        fig = getGraph4Figure(numVencedoresAgrupados)
            
        grafico = dcc.Graph(
            id='graph4',
            figure=fig
        )

        sportsTypeDropdown = dcc.Dropdown(np.append(['All'], np.sort(self._athletesDf['Sport'].unique())), 
                                            'Football', id='graph4SportsDropdown'
                                        )

        myGraphDiv = html.Div(children=[
            sportsTypeDropdown,
            grafico
        ])
        return myGraphDiv