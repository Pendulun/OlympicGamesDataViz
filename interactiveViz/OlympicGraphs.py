import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
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
        self._goldMedalAthletes = self._athletesDf[self._athletesDf["Medal"].isin(["Gold"])]

        self._regionsFilePath = regionsFilePath
        self._regionsDf = pd.read_csv(self._regionsFilePath)

        self._nocCountryContinent = nocCountryContinentFilePath
        self._nocCountryContinentDf = pd.read_csv(self._nocCountryContinent)

        self._yearCountryHost = yearCountryHostFilePath
        self._yearCountryHostDf = pd.read_csv(self._yearCountryHost)

        #Graph3 stuff so dont make them everytime
        self.meanMedalsRegion = 0
        self.summerComparison = 0

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

    def graphMedalsByPhisicalAttribute(self, app):
        
        def getDataOfSport(sportType:str, atributo):
            dfOfSport = 0

            if sportType == 'All':
                dfOfSport = self._athletesWithMedals
            else:
                dfOfSport = self._athletesWithMedals[self._athletesWithMedals['Sport'] == sportType]
            
            atletasPorAtributoMedalha = dfOfSport.groupby(["Sex", atributo, "Medal"])

            numVencedoresAgrupados = atletasPorAtributoMedalha.size().reset_index()
            numVencedoresAgrupados.rename(columns={0:'qtMedals'}, inplace=True)
            numVencedoresAgrupados['medalhasPorSexo'] = numVencedoresAgrupados['Sex'] + numVencedoresAgrupados['Medal']

            return numVencedoresAgrupados
        
        def getGraphPhisicalAttributeFigure(data, atributo, title_axis_x, titulo):
            fig = px.line(data, x=atributo, y="qtMedals", color="medalhasPorSexo", 
                        color_discrete_map={ #Para cada valor diferente na coluna medalhasPorSexo, eu defino um valor para a linha
                                "FSilver":'#eb1c1c',
                                'FBronze':'#fa9191',
                                'FGold':'#910101',
                                'MSilver':'#5967eb',
                                'MBronze': '#a5adf0',
                                'MGold': '#030d63'
                                },
                        ).update_layout(xaxis={"title": title_axis_x}, yaxis={"title": "Quantidade de medalhas"}, title_text=titulo, title_x=0.5,
                  title_font_size=15)
            return fig

        
        @app.callback(
            Output('graph4','figure'),
            Output('graph5','figure'),
            Output('graph6','figure'),
            Input('graphsPhiAttrportsDropdown','value'),
        )
        def attGraph4(sportType):
            numVencedoresAgrupadosIdade = getDataOfSport(sportType, "Age")
            numVencedoresAgrupadosAltura = getDataOfSport(sportType, "Height")
            numVencedoresAgrupadosPeso = getDataOfSport(sportType, "Weight")
            figAge = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosIdade, "Age", "Idade em anos", "Qtde de medalhas por idade")
            figHeight = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosAltura, "Height", "Altura em cm", "Qtde de medalhas por altura")
            figWeight = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosPeso, "Weight", "Peso em kg", "Qtde de medalhas por peso")
            return figAge, figHeight, figWeight

        #Visualizaão padrão
        numVencedoresAgrupadosIdade = getDataOfSport('All', "Age")
        numVencedoresAgrupadosAltura = getDataOfSport('All', "Height")
        numVencedoresAgrupadosPeso = getDataOfSport('All', "Weight")
        figAge = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosIdade, "Age", "Idade em anos", "Qtde de medalhas por idade")
        figHeight = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosAltura, "Height", "Altura em cm", "Qtde de medalhas por altura")
        figWeight = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosPeso, "Weight", "Peso em kg", "Qtde de medalhas por peso")
            
        graficoIdade = dcc.Graph(
            id='graph4',
            figure=figAge
        )
        graficoAltura = dcc.Graph(
            id='graph5',
            figure=figHeight
        )
        graficoPeso = dcc.Graph(
            id='graph6',
            figure=figWeight
        )

        sportsTypeDropdown = dcc.Dropdown(np.append(['All'], np.sort(self._athletesDf['Sport'].unique())), 
                                            'Football', id='graphsPhiAttrportsDropdown'
                                        )

        myGraphDiv = html.Div(children=[
            sportsTypeDropdown,
            graficoIdade,
            graficoAltura, 
            graficoPeso
        ])
        return myGraphDiv


    #Pode receber parâmetros como coisas para serem usadas em filtros
    # Graph média de medalhas ganhas por continente
    def graphRadar(self, app):

        """
        Esse é um gráfico de radar.
        Mostra as caracteristicas da média dos medalhistas de ouro por evento e
        as caracteristicas do medalhista com mais medalhas de ouro (melhor atleta)
        Filtros:
            Dropdown: Tipo de evento
            RangeSlider: Faixa de tempo
        """
        
        def getRadarGraph(eventType):
            goldMedalistsByEvent = self._goldMedalAthletes[self._athletesWithMedals['Event']==eventType]

            # Pegando medias de todos medalhistas de ouro
            meanWeights = goldMedalistsByEvent["Weight"].mean()
            meanHeights = goldMedalistsByEvent["Height"].mean()
            meanAges = goldMedalistsByEvent["Age"].mean()

            # Pegando o atleta com mais medalhas de ouro
            bestAthlete = goldMedalistsByEvent["Name"].value_counts().idxmax()
            bestAthleteWeight = goldMedalistsByEvent[goldMedalistsByEvent["Name"].isin([bestAthlete])]["Weight"].iloc[0]
            bestAthleteHeight = goldMedalistsByEvent[goldMedalistsByEvent["Name"].isin([bestAthlete])]["Height"].iloc[0]
            bestAthleteAge = goldMedalistsByEvent[goldMedalistsByEvent["Name"].isin([bestAthlete])]["Age"].mean()

            # Criando figura
            categories = ['Idade','Altura','Peso','Idade',]            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[round(bestAthleteAge,2), round(bestAthleteHeight,2), round(bestAthleteWeight,2),round(bestAthleteAge,2)],
                theta=categories,
                text = [round(bestAthleteAge,2), round(bestAthleteHeight,2), round(bestAthleteWeight,2)],
                hoverinfo = "r+theta",
                mode = "lines+markers+text",
                textfont=dict(
                    family="sans serif",
                    size=12,
                    color="RoyalBlue"
                ),
                textposition= ["top right", "top right", "bottom right"],
                name='Melhor Atleta'
            ))
            fig.add_trace(go.Scatterpolar(
                r=[round(meanAges,2),round(meanHeights,2),round(meanWeights,2),round(meanAges,2)],
                theta=categories,
                hoverinfo = "r+theta",
                text = [round(meanAges,2),round(meanHeights,2),round(meanWeights,2)],
                mode = "lines+markers+text",
                textposition= ["bottom right", "top left", "bottom left"],
                textfont=dict(
                    family="Balto, sans-serif",
                    size=12,
                    color="IndianRed"
                ),
                name='Média de medalhistas de ouro'
            ))
            fig.update_layout(
            polar=dict(
                radialaxis_angle = -45,
                radialaxis=dict(
                visible=True,
                range=[0, 250]
                )),
            showlegend=True
            )

            return fig

        defaultEvent = "Alpine Skiing Men's Combined"
        @app.callback(
            Output(component_id='output_event', component_property='figure'),
            Input(component_id='input_event', component_property='value')
        )
        def updateGraph1(event):
            fig = getRadarGraph(event)
            return fig

        fig = getRadarGraph(defaultEvent)

        grafico = dcc.Graph(
            id='output_event',
            figure=fig
        )

        myGraphDiv = html.Div([
                    html.H6("Escolha o nome do evento"),
                    html.Div([
                        "Input: ",
                        dcc.Input(id='input_event', value=defaultEvent, type="text")
                    ]),
                    html.Br(),
                    grafico,
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
    # Graph média de medalhas ganhas por continente
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