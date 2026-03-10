# modules
import os
import sys
import pandas as pd
import numpy as np
import time
from datetime import date

import dash
from dash import html
from dash import dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px

VALID_USERNAME_PASSWORD_PAIRS = {
    'username': 'P@ssw0rd'
}
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY], prevent_initial_callbacks='initial_duplicate')
app.title = '料理レシピ作成システム'
app.config.suppress_callback_exceptions=True