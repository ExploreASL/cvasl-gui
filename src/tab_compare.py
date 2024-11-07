import plotly.express as px
import pandas as pd
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
import data_store


def create_tab_compare():
    return html.Div([
        create_violin_plot_component()
    ])

def create_violin_plot_component():
    return html.Div([
        html.Div([
            html.Div([
                html.Label("Column to plot"),
                dcc.Dropdown(
                    id='column-dropdown',
                    placeholder="Select a column",
                    style={'width': '100%'}
                )
            ], style={'flex': '1', 'margin-right': '10px'}),  # Adjust width and add spacing

            html.Div([
                html.Label("Group by"),
                dcc.Dropdown(
                    id='group-by-dropdown',
                    placeholder="Select a column",
                    style={'width': '100%'}
                )
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'width': '80%', 'gap': '10px', 'padding': '10px 0'}),

        dcc.Graph(id='violin-plot')
    ])


@app.callback(
    Output('column-dropdown', 'options'),
    Output('group-by-dropdown', 'options'),
    Input('data-table', 'data'), # This feels a bit hacky, using it as a trigger
    State('file-list', 'value')
)
def update_dropdown_options(n_clicks, selected_file):
    if n_clicks == 0 or selected_file is None:
        raise PreventUpdate

    # Check if data is loaded and get column names
    if isinstance(data_store.all_data, pd.DataFrame):
        columns = [{'label': col, 'value': col} for col in data_store.all_data.columns]
        return columns, columns

    return [], []


@app.callback(
    Output('violin-plot', 'figure'),
    Input('column-dropdown', 'value'),
    Input('group-by-dropdown', 'value')
)
def update_violin_plot(selected_column, group_by_column):
    if not selected_column:
        raise PreventUpdate

    # Ensure data is loaded
    if hasattr(data_store, 'all_data') and isinstance(data_store.all_data, pd.DataFrame):
        data = data_store.all_data

        # Check if the selected column is valid
        if selected_column in data.columns:
            # If group_by_column is selected, use it for grouping
            if group_by_column and group_by_column in data.columns:
                fig = px.violin(data, y=selected_column, color=group_by_column, box=True, points="all")
                fig.update_layout(
                    title=f"Violin Plot of {selected_column} grouped by {group_by_column}",
                    yaxis_title=selected_column
                )
            else:
                fig = px.violin(data, y=selected_column, box=True, points="all")
                fig.update_layout(
                    title=f"Violin Plot of {selected_column}",
                    yaxis_title=selected_column
                )
            return fig

    return px.Figure()  # Return an empty figure if no data is available