from dash import Dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP, "assets/custom.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)
