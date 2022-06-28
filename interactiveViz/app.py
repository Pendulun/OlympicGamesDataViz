from dash import Dash, html
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

from Config import Config
from OlympicGraphs import OlympicGraphs

app = Dash(__name__)

server = app.server

#https://coolors.co/0085c7-f4c300-009f3d-f55d3e-ffffff
olympicsPalette = {
    'blue': '#0085C7',
    'yellow': '#F4C300',
    'green': '#009F3D',
    'orange': '#F55D3E',
    'white': '#FFFFFF',
    'black': '#000000',
    'bege': "#e9eef7"
}

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

#título e subtítulo
headerDiv = html.Div(
            [
                html.H1(
                    children='120 Anos dos Jogos Olímpicos',
                    style={
                        'textAlign': 'center',
                        'color': olympicsPalette['black']
                    }   
                ),
                html.P(
                    children="Uma análise dos físicos dos atletas (ou algo do tipo)",
                    style={
                        'textAlign': 'center',
                        'color': olympicsPalette['black']
                    }
                ),
            ], 
            style = {
                    'backgroundColor': olympicsPalette['bege']
                    }
            )

cleanedAthletesFilePath = '../'+Config.CLEANED_DATASET_DIR_NAME+"/"+Config.CLEANED_ATHLETES_FILE_NAME
cleanedRegionsFilePath = '../'+Config.CLEANED_DATASET_DIR_NAME+"/"+Config.CLEANED_REGIONS_FILE_NAME
cleanedNocCountryContinentFilePath = '../'+Config.CLEANED_DATASET_DIR_NAME+"/"+Config.CLEANED_NOC_COUNTRY_CONTINENT
yearCountryHostFilePath = '../'+Config.ORIGINAL_DATASET_DIR_NAME+"/"+Config.YEAR_COUNTRY_HOST
myGraphs = OlympicGraphs(cleanedAthletesFilePath, cleanedRegionsFilePath,cleanedNocCountryContinentFilePath,yearCountryHostFilePath)


mainBodyDiv = html.Div(children=[
                            html.Div(
                                [
                                    html.H4('Altura x Peso por medalha e esporte',
                                        style={
                                            'textAlign':'center'
                                        }
                                    ),
                                    myGraphs.graph1(app)
                                ]
                            ),
                            html.Div(
                                [
                                    html.H4('Altura x Peso por esporte',
                                        style={
                                            'textAlign':'center'
                                        }
                                    ),
                                    myGraphs.graph2(app)
                                ]
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H4('Esportes Coletivos e Individuais',
                                                style={
                                                    'textAlign':'center'
                                                }
                                            ),
                                            myGraphs.graph_pequenos_multiplos(app)
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                [
                                    html.H4('Melhores características por evento',
                                        style={
                                            'textAlign':'center'
                                        }
                                    ),
                                    myGraphs.graphRadar(app)
                                ]
                            ),
                            html.Div(
                                [
                                    html.H4('Você é atleta?',
                                        style={
                                            'textAlign':'center'
                                        }
                                    ),
                                    myGraphs.graphAreYouAthlete(app)
                                ]
                            ),
                            html.Div(
                                [
                                    html.H4('Medalhas por Atributo Físico',
                                        style={
                                            'textAlign':'center'
                                        }
                                    ),
                                    myGraphs.graphMedalsByPhisicalAttribute(app)
                                ]
                            )
                        ]
                    )

app.layout = html.Div(
    children=[
        headerDiv,
        mainBodyDiv
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)