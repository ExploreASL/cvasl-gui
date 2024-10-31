import pandas as pd
from dash import Input, Output, dash_table
from app import app

# Sample data
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'Age': [24, 19, 22, 32, 29],
    'Salary': [70000, 50000, 60000, 120000, 90000],
    'Department': ['HR', 'Finance', 'IT', 'Management', 'HR']
}
df = pd.DataFrame(data)

def create_data_table():
    return dash_table.DataTable(
        id='table',
        columns=[
            {'name': 'Name', 'id': 'Name', 'type': 'text'},
            {'name': 'Age', 'id': 'Age', 'type': 'numeric'},
            {'name': 'Salary', 'id': 'Salary', 'type': 'numeric'},
            {'name': 'Department', 'id': 'Department', 'type': 'text'},
        ],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        page_action='none'
    )

# # Callback to update table based on age and salary filters
# @app.callback(
#     Output('table', 'data'),
#     [Input('age-range-slider', 'value'), Input('salary-range-slider', 'value')]
# )
# def update_table(age_range, salary_range):
#     filtered_df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1]) &
#                      (df['Salary'] >= salary_range[0]) & (df['Salary'] <= salary_range[1])]
#     return filtered_df.to_dict('records')
