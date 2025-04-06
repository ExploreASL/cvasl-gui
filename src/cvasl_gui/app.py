from dash import Dash
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

external_stylesheets = [dbc.themes.BOOTSTRAP, "assets/custom.css"]

pathname_prefix = os.getenv("CVASL_PATHNAME_PREFIX", "/")
print(f"Using pathname prefix: {pathname_prefix}")

app = Dash(
    __name__,
    requests_pathname_prefix=pathname_prefix,
    routes_pathname_prefix=pathname_prefix,
    external_stylesheets=external_stylesheets)
