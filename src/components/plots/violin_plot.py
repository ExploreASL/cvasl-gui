from dash import html, dcc, Input, Output
from app import app
import plotly.express as px
import data_store


layout = html.Div([
    html.Div([
        html.Label("Column to plot"),
        dcc.Dropdown(
            id='violin-y-axis',
            placeholder="Select a column"
        ),
        html.Label("Group by"),
        dcc.Dropdown(
            id='violin-group-by',
            placeholder="Select a column"
        )
    ], style={'flex': '1', 'padding': '10px'}),

    html.Div([
        dcc.Graph(id='violin-plot')
    ], style={'flex': '2', 'padding': '10px'})
], style={'display': 'flex', 'width': '100%'})


@app.callback(
    Output('violin-y-axis', 'options'),
    Output('violin-group-by', 'options'),
    Input('btn-violin', 'n_clicks')
)
def update_violin_dropdowns(n_clicks):
    if not hasattr(data_store, 'all_data') or data_store.all_data is None:
        return [], []
    columns = [{'label': col, 'value': col} for col in data_store.all_data.columns]
    return columns, columns


@app.callback(
    Output('violin-plot', 'figure'),
    Input('violin-y-axis', 'value'),
    Input('violin-group-by', 'value')
)
def update_violin_plot(y_axis, group_by):
    if not y_axis:
        return {}
    data = data_store.all_data
    fig = px.violin(data, y=y_axis, color=group_by,
                    box=True, points='outliers') # points can be 'all', 'outliers', or False
    return fig
