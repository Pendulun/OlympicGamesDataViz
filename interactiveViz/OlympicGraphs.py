import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import numpy as np
import math

class OlympicGraphs():

    DEFAULT_SPORT_FOR_DROPDOWN_FILTER = "All"
    DEFAULT_MIN_YEAR_LIMIT = 1896
    DEFAULT_MAX_YEAR_LIMIT = 2016

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

        # Criando tabela com médias das características por evento
        eventosUnicos = sorted(self._athletesDf ["Event"].unique())
        data = []
        for evento in eventosUnicos:
            goldAthlete = self._goldMedalAthletes[self._goldMedalAthletes["Event"].isin([evento])]
            avgWeight = goldAthlete["Weight"].mean()
            avgHeight = goldAthlete["Height"].mean()
            avgAge = goldAthlete["Age"].mean()
            if math.isnan(avgWeight) or math.isnan(avgHeight):
                pass
            else:
                data.append([evento,avgHeight,avgWeight,avgAge])
        self._avgPerEvent = pd.DataFrame(data, columns=['Event', 'Height', 'Weight', 'Age'])
    
    def myDropdownAndSlider(self, app):

        def getMinMaxValueForSport(sportType):
            athletesOfSportWithMedal = self._athletesWithMedals[self._athletesWithMedals['Sport']==sportType]
            yearsOfMedalists = np.sort(athletesOfSportWithMedal['Year'].unique())
            if len(yearsOfMedalists) > 0:
                minYear = np.min(yearsOfMedalists)
                maxYear = np.max(yearsOfMedalists)
            else:
                minYear = OlympicGraphs.DEFAULT_MIN_YEAR_LIMIT
                maxYear = OlympicGraphs.DEFAULT_MAX_YEAR_LIMIT
            
            value = [minYear, maxYear]

            return minYear, maxYear, value

        @app.callback(
                Output('TimeSlider','min'),
                Output('TimeSlider','max'),
                Output('TimeSlider','value'),
                Input('SportsDropdown','value')
        )
        def updateTimeSlider(sportType):
            return getMinMaxValueForSport(sportType)
        

        minYear, maxYear, dropDownCurrValue = getMinMaxValueForSport(OlympicGraphs.DEFAULT_SPORT_FOR_DROPDOWN_FILTER)

        sportsTypeDropdown = dcc.Dropdown(np.append(['All'], np.sort(self._athletesDf['Sport'].unique())), 
                                            OlympicGraphs.DEFAULT_SPORT_FOR_DROPDOWN_FILTER, id='SportsDropdown'
                                        )
        
        yearsSlider = dcc.RangeSlider(minYear, maxYear, value=dropDownCurrValue,
                                        marks=None,
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        allowCross=False,
                                        id='TimeSlider'
                                    )

        return html.Div(children=[
            sportsTypeDropdown,
            html.Br(),  
            yearsSlider
        ],
        style = {'width':'70vw','margin':'auto'})
    
    def graphMedalsByPhisicalAttribute(self, app):
        
        def getDataOfSport(sportType:str, atributo, limInfTempo, limMaxTempo):
            dfOfSport = 0

            if sportType == 'All':
                dfOfSport = self._athletesWithMedals
            else:
                dfOfSport = self._athletesWithMedals[self._athletesWithMedals['Sport'] == sportType]
            
            dfOfSport = dfOfSport[(dfOfSport['Year'] >= limInfTempo) & (dfOfSport['Year'] <= limMaxTempo)]
            
            atletasPorAtributoMedalha = dfOfSport.groupby(["Sex", atributo, "Medal"])

            numVencedoresAgrupados = atletasPorAtributoMedalha.size().reset_index()
            numVencedoresAgrupados.rename(columns={0:'qtMedals'}, inplace=True)
            numVencedoresAgrupados['medalhasPorSexo'] = numVencedoresAgrupados['Sex'] + numVencedoresAgrupados['Medal']

            return numVencedoresAgrupados
        
        def getGraphPhisicalAttributeFigure(data, atributo, title_axis_x):
            x_range = ()
            if atributo == "Age":
                x_range = (10, 75)
            elif atributo == 'Height':
                x_range = (127, 230)
            else:
                x_range = (25, 190)

            fig = px.line(data, x=atributo, y="qtMedals", color="medalhasPorSexo", 
                        color_discrete_map={ #Para cada valor diferente na coluna medalhasPorSexo, eu defino um valor para a linha
                                "FSilver":'#eb1c1c',
                                'FBronze':'#fa9191',
                                'FGold':'#910101',
                                'MSilver':'#5967eb',
                                'MBronze': '#a5adf0',
                                'MGold': '#030d63'
                                },
                                range_x = x_range
                        ).update_layout(xaxis={"title": title_axis_x}, yaxis={"title": "Medalhas"}, title_x=0.5,
                            title_font_size=15)
            return fig

        
        @app.callback(
            Output('graph4','figure'),
            Output('graph5','figure'),
            Output('graph6','figure'),
            Input('SportsDropdown','value'),
            Input('TimeSlider','value')
        )
        def attGraph4(sportType, timeRange):
            numVencedoresAgrupadosIdade = getDataOfSport(sportType, "Age", timeRange[0], timeRange[1])
            numVencedoresAgrupadosAltura = getDataOfSport(sportType, "Height", timeRange[0], timeRange[1])
            numVencedoresAgrupadosPeso = getDataOfSport(sportType, "Weight", timeRange[0], timeRange[1])
            figAge = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosIdade, "Age", "Idade (ano)")
            figHeight = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosAltura, "Height", "Altura (cm)")
            figWeight = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosPeso, "Weight", "Peso (Kg)")
            return figAge, figHeight, figWeight

        #Visualizaão padrão
        default_sport = OlympicGraphs.DEFAULT_SPORT_FOR_DROPDOWN_FILTER
        default_min_year = OlympicGraphs.DEFAULT_MIN_YEAR_LIMIT
        default_max_year = OlympicGraphs.DEFAULT_MAX_YEAR_LIMIT
        numVencedoresAgrupadosIdade = getDataOfSport(default_sport, "Age", default_min_year, default_max_year)
        numVencedoresAgrupadosAltura = getDataOfSport(default_sport, "Height", default_min_year, default_max_year)
        numVencedoresAgrupadosPeso = getDataOfSport(default_sport, "Weight", default_min_year, default_max_year)
        figAge = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosIdade, "Age", "Idade (ano)")
        figHeight = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosAltura, "Height", "Altura (cm)")
        figWeight = getGraphPhisicalAttributeFigure(numVencedoresAgrupadosPeso, "Weight", "Peso (Kg)")
            
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

        myGraphDiv = html.Div(children=[
                                graficoAltura,
                                graficoPeso,
                                graficoIdade
                            ],
                            style = {'width':'80vw','margin':'auto'}
                        )
        return myGraphDiv

    def medalsPerWeightAndHeight(self, app):
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

            if sportType == "All":
                athletesOfSportWithMedal = self._athletesWithMedals
            else:
                athletesOfSportWithMedal = self._athletesWithMedals[self._athletesWithMedals['Sport']==sportType]

            athletesWithMedalOnTimeRange = athletesOfSportWithMedal[
                    (athletesOfSportWithMedal['Year'] >= minTime) & (athletesOfSportWithMedal['Year'] <= maxTime)
                ]

            fig = px.scatter(athletesWithMedalOnTimeRange, x="Height", y="Weight",
                                range_x = (127, 230), range_y = (25, 190), hover_name="Name",
                                color='Medal',
                                #Para cada valor diferente na coluna Medal, eu defino uma cor hex para a bolinha
                                color_discrete_map={ 
                                    'Bronze':'#96642f',
                                    'Gold':'#f5dd05',
                                    'Silver':'#98c5f5'
                                    })
            fig.update_layout(xaxis={"title": 'Altura (cm)'}, yaxis={"title": "Peso (Kg)"},
                                title={
                                    'text': 'Altura x Peso por medalha e esporte', 'xanchor': 'center', 'x':0.5}
                            )
            
            return fig
        
        def getMinMaxValueForSport(sportType):
            athletesOfSportWithMedal = self._athletesWithMedals[self._athletesWithMedals['Sport']==sportType]
            yearsOfMedalists = np.sort(athletesOfSportWithMedal['Year'].unique())
            if len(yearsOfMedalists) > 0:
                minYear = np.min(yearsOfMedalists)
                maxYear = np.max(yearsOfMedalists)
            else:
                minYear = 1896
                maxYear = 2016
            
            value = [minYear, maxYear]

            return minYear, maxYear, value

        #Como recebi o app criado em app.py por parâmetro, posso adicionar callbacks a ele

        @app.callback(
            Output('graph1','figure'),
            Input('SportsDropdown','value'),
            Input('TimeSlider','value')
        )
        def updateGraph1(sportType, timeRange):

            fig = getGraphFigWith(sportType, timeRange[0], timeRange[1])

            return fig

        #Aqui começa o display default do gráfico. Ele será alterado de acordo com os callbacks definidos acima    
            
        defaultSportType = OlympicGraphs.DEFAULT_SPORT_FOR_DROPDOWN_FILTER
        minYear, maxYear, dropDownCurrValue = getMinMaxValueForSport(defaultSportType)
        
        fig = getGraphFigWith(defaultSportType, minYear, maxYear)
        grafico = dcc.Graph(
            id='graph1',
            figure=fig
        )

        myGraphDiv = html.Div(children=[
            grafico
        ])

        return myGraphDiv

    def weightAndHeightDist(self, app):
        """
        Esse é um gráfico com as seguintes características:
        Eixo x: Altura
        Eixo y: Peso
        Filtros:
            Dropdown: Tipo de Esporte
            RangeSlider: Faixa de tempo
        """

        def getGraphFigWith(sportType, minTime, maxTime):
            if sportType == "All":
                athletesOfSportWithMedal = self._athletesWithMedals
            else:
                athletesOfSportWithMedal = self._athletesWithMedals[self._athletesWithMedals['Sport']==sportType]

            athletesWithMedalOnTimeRange = athletesOfSportWithMedal[
                    (athletesOfSportWithMedal['Year'] >= minTime) & (athletesOfSportWithMedal['Year'] <= maxTime)
                ]

            fig = px.density_heatmap(athletesWithMedalOnTimeRange, x="Height", y="Weight", marginal_x = "histogram", marginal_y = "histogram",
                                        range_x = (127, 230), range_y = (25, 214))
            
            fig.update_layout(xaxis={"title": "Altura (cm)"}, yaxis={"title": "Peso (kg)"}, 
                                        title={'text': 'Altura x Peso por esporte', 'xanchor': 'center', 'x':0.5})
            
            return fig
        
        def getMinMaxValueForSport(sportType):
            athletesOfSportWithMedal = self._athletesWithMedals[self._athletesWithMedals['Sport']==sportType]
            yearsOfMedalists = np.sort(athletesOfSportWithMedal['Year'].unique())
            if len(yearsOfMedalists) > 0:
                minYear = np.min(yearsOfMedalists)
                maxYear = np.max(yearsOfMedalists)
            else:
                minYear = 1896
                maxYear = 2016
            
            value = [minYear, maxYear]

            return minYear, maxYear, value

        #Como recebi o app criado em app.py por parâmetro, posso adicionar callbacks a ele

        @app.callback(
            Output('graph2','figure'),
            Input('SportsDropdown','value'),
            Input('TimeSlider','value')
        )
        def updateGraph2(sportType, timeRange):

            fig = getGraphFigWith(sportType, timeRange[0], timeRange[1])

            return fig
            
        defaultSportType = OlympicGraphs.DEFAULT_SPORT_FOR_DROPDOWN_FILTER
        minYear, maxYear, dropDownCurrValue = getMinMaxValueForSport(defaultSportType)
        
        fig = getGraphFigWith(defaultSportType, minYear, maxYear)
        grafico = dcc.Graph(
            id='graph2',
            figure=fig
        )

        myGraphDiv = html.Div(children=[
            grafico,
        ])

        return myGraphDiv
    
    def graph_pequenos_multiplos(self, app):
        
        collectiveSports = [
            'Football', 'Basketball', 'Beach Voleyball', 'Rowing', 'Handball', 'Hockey',
            'Ice Hockey', 'Lacrosse', 'Rugby', 'Voleyball', 'Softball', 'Badminton',
            'Bobsleigh', 'Cricket', 'Curling', 'Sailing', 'Water Polo'
        ]

        individualSports = [
            'Alpine Skiing', 'Alpinism', 'Archery', 'Athletics', 'Biathlon', 'Boxing',
            'Canoeing', 'Cross Country Skiing', 'Cycling', 'Diving', 'Equestrianism',
            'Fencing', 'Figure Skating', 'Golf', 'Gymnastics', 'Judo', 'Modern Pentathlon',
            'Rhythmic Gymnastics', 'Shooting', 'Ski Jumping', 'Snowboarding', 'Speed Skating',
            'Swimming', 'Synchronized Swimming', 'Table Tennis', 'Taekwondo', 'Tennis',
            'Trampolining', 'Triathlon', 'Weightlifting', 'Wrestling'
        ]

        collectiveData = self._athletesWithMedals[self._athletesWithMedals['Sport'].isin(collectiveSports)]
        individualData = self._athletesWithMedals[self._athletesWithMedals['Sport'].isin(individualSports)]

        figCollective = px.density_heatmap(collectiveData, x="Height", y="Weight", range_x = (127, 230), range_y = (25, 214))
        figIndividual = px.density_heatmap(individualData, x="Height", y="Weight", range_x = (127, 230), range_y = (25, 214))

        figCollective.update_layout(xaxis={"title": "Altura (cm)"}, yaxis={"title": "Peso (kg)"})
        figIndividual.update_layout(xaxis={"title": "Altura (cm)"}, yaxis={"title": "Peso (kg)"})

        graficoMultCol = dcc.Graph(
            id='graphMultCol',
            figure=figCollective
        )
        
        graficoMultInd = dcc.Graph(
            id='graphMultInd',
            figure=figIndividual
        )

        myGraphDiv = html.Div(
                        [
                            html.Div(
                                [
                                    html.H4('Esportes Coletivos', style={'textAlign':'center'}),
                                    graficoMultCol
                                ],
                                style = {"width":'50vw'}
                            ),
                            html.Div(
                                [
                                    html.H4('Esportes Individuais', style={'textAlign':'center'}),
                                    graficoMultInd
                                ],
                                style = {"width":'50vw'}
                            )   
                        ],
                        style = {'display':'flex', "width": '95vw', 'margin': 'auto'}
                    )

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
            categories = ['Idade','Altura','Peso','Idade']            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[round(bestAthleteAge,2), round(bestAthleteHeight,2), round(bestAthleteWeight,2),round(bestAthleteAge,2)],
                theta=categories,
                text = [round(bestAthleteAge,2), round(bestAthleteHeight,2), round(bestAthleteWeight,2),round(bestAthleteAge,2)],
                hoverinfo = "r+theta",
                mode = "lines+markers+text",
                textfont=dict(
                    family="Balto, sans-serif",
                    size=13,
                    color="RoyalBlue"
                ),
                textposition= ["top right", "top right", "bottom right","top right"],
                name='Melhor Atleta'
            ))
            fig.add_trace(go.Scatterpolar(
                r=[round(meanAges,2),round(meanHeights,2),round(meanWeights,2),round(meanAges,2)],
                theta=categories,
                hoverinfo = "r+theta",
                text = [round(meanAges,2),round(meanHeights,2),round(meanWeights,2),round(meanAges,2)],
                mode = "lines+markers+text",
                textposition= ["bottom right", "top left", "bottom left","bottom right"],
                textfont=dict(
                    family="Balto, sans-serif",
                    size=13,
                    color="IndianRed"
                ),
                name='Média de medalhistas de ouro'
            ))
            
            # Adicionando anotação do melhor atleta
            fig.add_annotation(text="Melhor atleta: " + bestAthlete,
                                xref="paper", yref="paper",
                                x=0.5, y=1.2, showarrow=False)

            fig.update_layout(
            polar=dict(
                radialaxis_angle = -45,
                radialaxis=dict(
                visible=True,
                range=[0, 250],
                tickfont = dict(size = 10),
                )),
            showlegend=True,
            #paper_bgcolor = "#E8E9EB"
            )

            fig.update_polars(bgcolor='#CCCDC6')            
            return fig

        defaultEvent = "Alpine Skiing Men's Combined"
        defaultSport = "Alpine Skiing"
        dfSportEvent = self._athletesDf[['Sport', 'Event']].copy()
        
        # Sports dropdown
        @app.callback(
            Output(component_id='dropdownEvent', component_property='options'),
            Input(component_id='dropdownSport', component_property='value'),
        )
        def updateSports(sportsDropdown):
            EventAux = dfSportEvent[dfSportEvent["Sport"].isin([sportsDropdown])]
            return [{'label': i, 'value': i} for i in sorted(EventAux.Event.unique())]

        # Event dropdown
        @app.callback(
            Output('dropdownEvent','value'),
            Input('dropdownEvent', 'options')
        )
        def set_eventDropdown_value(options):
            #print(options)
            return options[0]['value']

        # Update graph
        @app.callback(
            Output(component_id='output_event', component_property='figure'),
            Input(component_id='dropdownEvent', component_property='value'),
        )
        def updateGraph1(eventDropdown):
            fig = getRadarGraph(eventDropdown)
            return fig

        fig = getRadarGraph(defaultEvent)

        grafico = dcc.Graph(
            id='output_event',
            figure=fig
        )

        myGraphDiv = html.Div([
                    html.Div([
                        "Selecione o esporte:",
                        dcc.Dropdown(self._athletesDf['Sport'].sort_values().unique(), value=defaultSport, id = "dropdownSport"),
                        "Selecione o evento:",
                        dcc.Dropdown(id = "dropdownEvent", options=[],multi=False)
                    ],
                    style = {'width':'70vw', 'margin':'auto'}),
                    html.Br(),
                    grafico,
                ],
                style = {'width':'80vw', 'margin':'auto'})
                
        return myGraphDiv

    # Voce tem porte de atleta?
    def graphAreYouAthlete(self, app):

        """
        Esse é um gráfico de radar.
        Mostra as caracteristicas da média dos medalhistas de ouro por evento e
        as caracteristicas do medalhista com mais medalhas de ouro (melhor atleta)
        Filtros:
            Dropdown: Tipo de evento
            RangeSlider: Faixa de tempo
        """
        
        def getGraphAreYouAthlete(idade,altura,peso):
            avgPerEventAux = self._avgPerEvent.copy()
            eventoAtual = self._avgPerEvent.copy()
            idade = float(idade)
            altura = float(altura)
            peso = float(peso)
            for i in range(100,10,-1):
                x = i/10
                # Dropando por altura
                indexNames = avgPerEventAux[ (avgPerEventAux['Height'] >= altura+x) | (avgPerEventAux['Height'] <= altura - x) ].index
                avgPerEventAux.drop(indexNames , inplace=True)

                # Dropando por peso
                indexNames = avgPerEventAux[ (avgPerEventAux['Weight'] >= peso+x) | (avgPerEventAux['Weight'] <= peso - x) ].index
                avgPerEventAux.drop(indexNames , inplace=True)

                # Dropando por idade
                indexNames = avgPerEventAux[ (avgPerEventAux['Age'] >= idade+5) | (avgPerEventAux['Age'] <= idade - 5) ].index
                avgPerEventAux.drop(indexNames , inplace=True)

                if len(avgPerEventAux) == 0:
                    break
                else:
                    eventoAtual = avgPerEventAux.copy()

            row = eventoAtual.iloc[0]
            evento = row.Event
            meanAges = row.Age
            meanHeights = row.Height
            meanWeights = row.Weight

            # Criando figura
            categories = ['Idade','Altura','Peso','Idade']            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[round(idade,2), round(altura,2), round(peso,2),round(idade,2)],
                theta=categories,
                text = [round(idade,2), round(altura,2), round(peso,2),round(idade,2)],
                hoverinfo = "r+theta",
                mode = "lines+markers+text",
                textfont=dict(
                    family="Balto, sans-serif",
                    size=13,
                    color="RoyalBlue"
                ),
                textposition= ["top right", "top right", "bottom right","top right"],
                name='Seus dados'
            ))
            fig.add_trace(go.Scatterpolar(
                r=[round(meanAges,2),round(meanHeights,2),round(meanWeights,2),round(meanAges,2)],
                theta=categories,
                hoverinfo = "r+theta",
                text = [round(meanAges,2),round(meanHeights,2),round(meanWeights,2),round(meanAges,2)],
                mode = "lines+markers+text",
                textposition= ["bottom right", "top left", "bottom left","bottom right"],
                textfont=dict(
                    family="Balto, sans-serif",
                    size=13,
                    color="IndianRed"
                ),
                name='Média de medalhistas de ouro'
            ))
            
            # Adicionando anotação do melhor atleta
            fig.add_annotation(text="Evento: " + evento,
                                xref="paper", yref="paper",
                                x=0.5, y=1.2, showarrow=False)

            fig.update_layout(
            polar=dict(
                radialaxis_angle = -45,
                radialaxis=dict(
                visible=True,
                range=[0, 250],
                tickfont = dict(size = 10),
                )),
            #paper_bgcolor = "#E8E9EB",
            showlegend=True
            )

            fig.update_polars(bgcolor='#CCCDC6')
            return fig

        defaultEvent = "Alpine Skiing Men's Combined"
        defaultSport = "Alpine Skiing"
        dfSportEvent = self._athletesDf[['Sport', 'Event']].copy()
        
        # Sports dropdown
        @app.callback(
            Output(component_id='output_AreYouAthlete', component_property='figure'),
            Input(component_id='Altura', component_property='value'),
            Input(component_id='Idade', component_property='value'),
            Input(component_id='Peso', component_property='value'),
        )
        def updateGraph(altura,idade,peso):
            fig = getGraphAreYouAthlete(idade,altura,peso)
            return fig       

        fig = getGraphAreYouAthlete(22,190,90)

        grafico = dcc.Graph(
            id='output_AreYouAthlete',
            figure=fig
        )

        myGraphDiv = html.Div([
                    html.Div([
                        "Altura (cm): ",
                        dcc.Input(id='Altura',value='190',type='text'),
                        " Idade (anos): ",
                        dcc.Input(id='Idade',value='22',type='text'),
                        " Peso (kg): ",
                        dcc.Input(id='Peso',value='90',type='text')
                    ],
                    style={'width':'70vw', 'margin':'auto', 'text-align':'center'}),
                    html.Br(),
                    grafico,
                ],
                style = {'width':'80vw', 'margin':'auto'})
                
        return myGraphDiv