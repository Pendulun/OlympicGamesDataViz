from dash import Dash, html, dcc
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
            style=  {
                    'backgroundColor': olympicsPalette['bege']
                    }
            )

app.layout = html.Div(
    children=[
        headerDiv,
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)