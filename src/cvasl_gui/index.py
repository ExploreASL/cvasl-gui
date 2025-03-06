import os
import webbrowser
from threading import Timer
from dotenv import load_dotenv
from waitress import serve

from dash import html, dcc, Input, Output

from cvasl_gui import data_store
from cvasl_gui.app import app
from cvasl_gui.tabs.data_inspection import create_tab_data_inspection
from cvasl_gui.tabs.input_selection import create_tab_input_selection
from cvasl_gui.tabs.compare import create_tab_compare
from cvasl_gui.tabs.harmonization import create_tab_harmonization

data_store.all_data = None
data_store.selected_directory = None

app.layout = html.Div(
    id='root',
    children=[html.Div([
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
                html.Div(create_tab_data_inspection(), id='tab-2-content', style={'display': 'none'}),
                html.Div(create_tab_compare(), id='tab-3-content', style={'display': 'none'}),
                html.Div(create_tab_harmonization(), id='tab-4-content', style={'display': 'none'}),
                html.Div("Estimate content goes here", id='tab-5-content', style={'display': 'none'}),
            ],
            id='tab-content-container'
        )
    ], id='main-container')])


# Callback to toggle visibility based on selected tab
@app.callback(
    [Output(f'tab-{i}-content', 'style') for i in range(1, 6)],
    [Input('tabs', 'value')]
)
def display_content(selected_tab):
    # Set 'display' to 'block' for the selected tab and 'none' for others
    return [{'display': 'block' if selected_tab == str(i) else 'none'} for i in range(1, 6)]


def main():
    # Load environment variables
    load_dotenv()
    port = int(os.getenv('CVASL_PORT', 8767))
    debug_mode = os.getenv('CVASL_DEBUG_MODE', 'False') == 'True'
    host = '127.0.0.1'

    # Start the server and open the browser
    if debug_mode:
        app.run_server(port=port, debug=True)
    else:
        # Schedule a timer to open the browser
        url = f"http://{host}:{port}/"
        Timer(1, lambda: webbrowser.open(url)).start()
        
        # Start the server using waitress
        print(f"Starting server at {url}")
        serve(app.server, host=host, port=port, threads=8) 


if __name__ == '__main__':
    main()
