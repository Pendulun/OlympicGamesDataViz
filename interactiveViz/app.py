from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

if __name__ == "__main__":
    app.run_server(debug=True)