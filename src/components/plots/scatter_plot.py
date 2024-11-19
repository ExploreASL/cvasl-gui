from dash import html, dcc, Input, Output
from app import app
import plotly.express as px
import data_store


layout = html.Div([
    html.Div([
        html.Label("X-axis"),
        dcc.Dropdown(
            id='scatter-x-axis',
            placeholder="Select a column"
        ),
        html.Label("Y-axis"),
        dcc.Dropdown(
            id='scatter-y-axis',
            placeholder="Select a column"
        ),
        html.Label("Group by"),
        dcc.Dropdown(
            id='scatter-group-by',
            placeholder="Select a column"
        )
    ], style={'flex': '1', 'padding': '10px'}),
    
    html.Div([
      dcc.Graph(id='scatter-plot')
    ], style={'flex': '2', 'padding': '10px'})
], style={'display': 'flex', 'width': '100%'})


@app.callback(
    Output('scatter-x-axis', 'options'),
    Output('scatter-y-axis', 'options'),
    Output('scatter-group-by', 'options'),
    Input('btn-scatter', 'n_clicks')
)
def update_scatter_dropdowns(n_clicks):
    if not hasattr(data_store, 'all_data') or data_store.all_data is None:
        return [], [], []
    columns = [{'label': col, 'value': col} for col in data_store.all_data.columns]
    return columns, columns, columns


@app.callback(
    Output('scatter-plot', 'figure'),
    Input('scatter-x-axis', 'value'),
    Input('scatter-y-axis', 'value'),
    Input('scatter-group-by', 'value')
)
def update_scatter_plot(x_axis, y_axis, group_by):
    if not x_axis or not y_axis:
        return {}
    data = data_store.all_data
    fig = px.scatter(data, x=x_axis, y=y_axis, color=group_by)
    return fig
