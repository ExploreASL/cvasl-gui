import pandas as pd
from dash import Input, Output, dash_table
from dash.exceptions import PreventUpdate
from app import app
import data_store


def create_data_table():
    return dash_table.DataTable(
        id='table',
        columns=[
            {'name': 'participant_id', 'id': 'participant_id', 'type': 'text'},
            {'name': 'ID', 'id': 'ID', 'type': 'text'},
            {'name': 'Age', 'id': 'Age', 'type': 'numeric'},
            {'name': 'Sex', 'id': 'Sex', 'type': 'text'},
            {'name': 'Site', 'id': 'Site', 'type': 'text'}
        ],
        data=[],
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        page_action='none'
    )

@app.callback(
    Output('table', 'data'),
    Input('file-contents-container', 'children')
)
def update_table(data):
    if data is None:
        raise PreventUpdate

    df = data_store.all_data
    return df.to_dict('records')
