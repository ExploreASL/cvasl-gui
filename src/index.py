from dash import html, dcc, Input, Output

from app import app
from components.data_table import create_data_table
from components.graph import create_graph
from components.date_picker import date_picker
from tab_input_selection import create_tab_input_selection


app.layout = html.Div([
    dcc.Tabs(
        id='tabs',
        value='1',
        children=[
            dcc.Tab(label='Select input', value='1'),
            dcc.Tab(label='Inspect', value='2'),
            dcc.Tab(label='Compare', value='3'),
            dcc.Tab(label='Harmonize', value='4'),
            dcc.Tab(label='Estimate', value='5'),
        ],
        vertical=False
    ),
    html.Div(id='tab-output')
], style={'width': '80%', 'fontFamily': 'Sans-Serif', 'margin-left': 'auto', 'margin-right': 'auto'})

tabs = {
    '1': create_tab_input_selection(),
    '2': create_data_table(),
    '3': None,
    '4': None,
    '5': None
}

# Callback to switch between tabs and update content
@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    return tabs[value]


if __name__ == '__main__':
    app.run_server(debug=True)