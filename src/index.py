from dash import html, dcc, Input, Output

from app import app
from components.data_table import create_data_table
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
    # Load all tab contents here but control visibility through a callback
    html.Div(
        [
            html.Div(create_tab_input_selection(), id='tab-1-content', style={'display': 'block'}),
            html.Div(create_data_table(), id='tab-2-content', style={'display': 'none'}),
            html.Div("asdf", id='tab-3-content', style={'display': 'none'}),
            html.Div("asdf", id='tab-4-content', style={'display': 'none'}),
            html.Div("Estimate content goes here", id='tab-5-content', style={'display': 'none'}),
        ],
        id='tab-content-container'
    )
], style={'width': '80%', 'fontFamily': 'Sans-Serif', 'margin-left': 'auto', 'margin-right': 'auto'})


# Callback to toggle visibility based on selected tab
@app.callback(
    [Output(f'tab-{i}-content', 'style') for i in range(1, 6)],
    [Input('tabs', 'value')]
)
def display_content(selected_tab):
    # Set 'display' to 'block' for the selected tab and 'none' for others
    return [{'display': 'block' if selected_tab == str(i) else 'none'} for i in range(1, 6)]


if __name__ == '__main__':
    app.run_server(debug=True)
