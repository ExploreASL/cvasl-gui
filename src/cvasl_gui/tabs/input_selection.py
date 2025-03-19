from dash import html
from cvasl_gui.components.directory_input import create_directory_input
from cvasl_gui.components.job_list import create_job_list

def create_tab_input_selection():
    return html.Div([
        html.H2("Previous runs"),
        create_job_list(),
        html.H2("Selection"),
        html.Div("This will contain some more info on the run + download/remove"),
        html.H2("Select new input data"),
        create_directory_input(),
    ])
