from dash import Dash, html, dcc
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

from Config import Config
from OlympicGraphs import OlympicGraphs
import plotly.express as px
import pandas as pd

app = Dash(__name__)

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
myGraphs = OlympicGraphs(cleanedAthletesFilePath, cleanedRegionsFilePath)

mainBodyDiv = html.Div(children=[
                            html.Div(
                                [
                                    html.H4('Altura x Peso',
                                        style={
                                        'textAlign': 'center'}
                                    ),
                                    myGraphs.getGraficoExemplo(),
                                    html.P(
                                        """
                                            Esse gráfico tem alguns problemas ainda. O principal é que, se um mesmo atleta ganhou várias medalhas, 
                                            os seus pontos ficarão um em cima do outro e, ao passar o mouse, pode não fazer muito sentido o que é 
                                            mostrado como informação do ponto. Entretanto, já serve de base de fluxo de desenvolvimento do gráfico no código.
                                            Além disso, pode ser interessante plotar em partes, por exemplo, primeiro apenas só aqueles que não ganharam medalhas.
                                            Depois, apenas aqueles que ganharam bronze. Depois prata e, por fim, ouro. Dessa forma, poderíamos ver melhor o que importa.
                                        """
                                    )
                                ]
                            ),
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