from dash import dcc
from datetime import datetime as dt

date_picker = dcc.DatePickerSingle(
    id='my-date-picker-single',
    min_date_allowed=dt(1995, 8, 5),
    max_date_allowed=dt(2017, 9, 19),
    initial_visible_month=dt(2017, 8, 5),
    date=dt(2017, 8, 25)
)
