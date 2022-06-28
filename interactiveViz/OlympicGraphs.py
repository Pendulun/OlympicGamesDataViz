import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import numpy as np
import math

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

    def graph_pequenos_multiplos_col(self, app):
        dfAtt = self._athletesWithMedals.copy()
        dfAtt['Categoria'] = ""
        
        for index in dfAtt.index:
            if dfAtt.loc[index, 'Sport'] == 'Football' or dfAtt.loc[index, 'Sport'] == 'Basketball' or dfAtt.loc[index, 'Sport'] == 'Beach Voleyball' or dfAtt.loc[index, 'Sport'] == 'Rowing' or dfAtt.loc[index, 'Sport'] == 'Handball' or dfAtt.loc[index, 'Sport'] == 'Hockey' or dfAtt.loc[index, 'Sport'] == 'Ice Hockey' or dfAtt.loc[index, 'Sport'] == 'Lacrosse' or dfAtt.loc[index, 'Sport'] == 'Rugby' or dfAtt.loc[index, 'Sport'] == 'Voleyball' or dfAtt.loc[index, 'Sport'] == 'Softball' or dfAtt.loc[index, 'Sport'] == 'Badminton' or dfAtt.loc[index, 'Sport'] == 'Bobsleigh' or dfAtt.loc[index, 'Sport'] == 'Cricket' or dfAtt.loc[index, 'Sport'] == 'Curling' or dfAtt.loc[index, 'Sport'] == 'Sailing' or dfAtt.loc[index, 'Sport'] == 'Water Polo':
                dfAtt.loc[index,'Categoria'] = 'Coletivo'
            elif dfAtt.loc[index, 'Sport'] == 'Alpine Skiing' or dfAtt.loc[index, 'Sport'] == 'Alpinism' or dfAtt.loc[index, 'Sport'] == 'Archery' or dfAtt.loc[index, 'Sport'] == 'Athletics' or dfAtt.loc[index, 'Sport'] == 'Biathlon' or dfAtt.loc[index, 'Sport'] == 'Boxing' or dfAtt.loc[index, 'Sport'] == 'Canoeing' or dfAtt.loc[index, 'Sport'] == 'Cross Country Skiing' or dfAtt.loc[index, 'Sport'] == 'Cycling' or dfAtt.loc[index, 'Sport'] == 'Diving' or dfAtt.loc[index, 'Sport'] == 'Equestrianism' or dfAtt.loc[index, 'Sport'] == 'Fencing' or dfAtt.loc[index, 'Sport'] == 'Figure Skating' or dfAtt.loc[index, 'Sport'] == 'Golf' or dfAtt.loc[index, 'Sport'] == 'Gymnastics' or dfAtt.loc[index, 'Sport'] == 'Judo' or dfAtt.loc[index, 'Sport'] == 'Modern Pentathlon' or dfAtt.loc[index, 'Sport'] == 'Rhythmic Gymnastics' or dfAtt.loc[index, 'Sport'] == 'Shooting' or dfAtt.loc[index, 'Sport'] == 'Ski Jumping' or dfAtt.loc[index, 'Sport'] == 'Snowboarding' or dfAtt.loc[index, 'Sport'] == 'Speed Skating' or dfAtt.loc[index, 'Sport'] == 'Swimming' or dfAtt.loc[index, 'Sport'] == 'Synchronized Swimming' or dfAtt.loc[index, 'Sport'] == 'Table Tennis' or dfAtt.loc[index, 'Sport'] == 'Taekwondo' or dfAtt.loc[index, 'Sport'] == 'Tennis' or dfAtt.loc[index, 'Sport'] == 'Trampolining' or dfAtt.loc[index, 'Sport'] == 'Triathlon' or dfAtt.loc[index, 'Sport'] == 'Weightlifting' or dfAtt.loc[index, 'Sport'] == 'Wrestling':       
                dfAtt.loc[index, 'Categoria'] = 'Individual'
            else:
                dfAtt.loc[index, 'Categoria'] = ''

        for index in dfAtt.index:
            if dfAtt.loc[index,'Categoria'] != 'Coletivo':
                dfAtt.drop(index, axis=0, inplace = True)

        fig = px.density_heatmap(dfAtt, x="Height", y="Weight", facet_row = 'Categoria')
        #fig = px.density_heatmap(dfAtt, x="Height", y="Weight", histnorm = 'probability density')


        graficoMult = dcc.Graph(
            id='graphMultCol',
            figure=fig
        )

        myGraphDiv = html.Div(children=[
            graficoMult
        ])

        return myGraphDiv

    def graph_pequenos_multiplos_ind(self, app):
        dfAtt = self._athletesWithMedals.copy()
        dfAtt['Categoria'] = ""
        
        for index in dfAtt.index:
            if dfAtt.loc[index, 'Sport'] == 'Football' or dfAtt.loc[index, 'Sport'] == 'Basketball' or dfAtt.loc[index, 'Sport'] == 'Beach Voleyball' or dfAtt.loc[index, 'Sport'] == 'Rowing' or dfAtt.loc[index, 'Sport'] == 'Handball' or dfAtt.loc[index, 'Sport'] == 'Hockey' or dfAtt.loc[index, 'Sport'] == 'Ice Hockey' or dfAtt.loc[index, 'Sport'] == 'Lacrosse' or dfAtt.loc[index, 'Sport'] == 'Rugby' or dfAtt.loc[index, 'Sport'] == 'Voleyball' or dfAtt.loc[index, 'Sport'] == 'Softball' or dfAtt.loc[index, 'Sport'] == 'Badminton' or dfAtt.loc[index, 'Sport'] == 'Bobsleigh' or dfAtt.loc[index, 'Sport'] == 'Cricket' or dfAtt.loc[index, 'Sport'] == 'Curling' or dfAtt.loc[index, 'Sport'] == 'Sailing' or dfAtt.loc[index, 'Sport'] == 'Water Polo':
                dfAtt.loc[index,'Categoria'] = 'Coletivo'
            elif dfAtt.loc[index, 'Sport'] == 'Alpine Skiing' or dfAtt.loc[index, 'Sport'] == 'Alpinism' or dfAtt.loc[index, 'Sport'] == 'Archery' or dfAtt.loc[index, 'Sport'] == 'Athletics' or dfAtt.loc[index, 'Sport'] == 'Biathlon' or dfAtt.loc[index, 'Sport'] == 'Boxing' or dfAtt.loc[index, 'Sport'] == 'Canoeing' or dfAtt.loc[index, 'Sport'] == 'Cross Country Skiing' or dfAtt.loc[index, 'Sport'] == 'Cycling' or dfAtt.loc[index, 'Sport'] == 'Diving' or dfAtt.loc[index, 'Sport'] == 'Equestrianism' or dfAtt.loc[index, 'Sport'] == 'Fencing' or dfAtt.loc[index, 'Sport'] == 'Figure Skating' or dfAtt.loc[index, 'Sport'] == 'Golf' or dfAtt.loc[index, 'Sport'] == 'Gymnastics' or dfAtt.loc[index, 'Sport'] == 'Judo' or dfAtt.loc[index, 'Sport'] == 'Modern Pentathlon' or dfAtt.loc[index, 'Sport'] == 'Rhythmic Gymnastics' or dfAtt.loc[index, 'Sport'] == 'Shooting' or dfAtt.loc[index, 'Sport'] == 'Ski Jumping' or dfAtt.loc[index, 'Sport'] == 'Snowboarding' or dfAtt.loc[index, 'Sport'] == 'Speed Skating' or dfAtt.loc[index, 'Sport'] == 'Swimming' or dfAtt.loc[index, 'Sport'] == 'Synchronized Swimming' or dfAtt.loc[index, 'Sport'] == 'Table Tennis' or dfAtt.loc[index, 'Sport'] == 'Taekwondo' or dfAtt.loc[index, 'Sport'] == 'Tennis' or dfAtt.loc[index, 'Sport'] == 'Trampolining' or dfAtt.loc[index, 'Sport'] == 'Triathlon' or dfAtt.loc[index, 'Sport'] == 'Weightlifting' or dfAtt.loc[index, 'Sport'] == 'Wrestling':       
                dfAtt.loc[index, 'Categoria'] = 'Individual'
            else:
                dfAtt.loc[index, 'Categoria'] = ''

        for index in dfAtt.index:
            if dfAtt.loc[index,'Categoria'] != 'Individual':
                dfAtt.drop(index, axis=0, inplace = True)

        fig = px.density_heatmap(dfAtt, x="Height", y="Weight", facet_row = 'Categoria')
        #fig = px.density_heatmap(dfAtt, x="Height", y="Weight", histnorm = 'probability density')


        graficoMult = dcc.Graph(
            id='graphMultInd',
            figure=fig
        )

        myGraphDiv = html.Div(children=[
            graficoMult
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
            showlegend=True
            )

            fig.update_traces()
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
                    ]),
                    html.Br(),
                    grafico,
                ])
                
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
            showlegend=True
            )

            fig.update_traces()
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
                        "Altura:",
                        dcc.Input(id='Altura',value='190',type='text'),
                        "Idade:",
                        dcc.Input(id='Idade',value='22',type='text'),
                        "Peso",
                        dcc.Input(id='Peso',value='90',type='text')
                    ]),
                    html.Br(),
                    grafico,
                ])
                
        return myGraphDiv