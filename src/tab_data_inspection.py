from dash import html
from components.data_table import create_data_table

def create_tab_data_inspection():
    return html.Div([
        create_data_table(),
    ])