# modules
import os
import sys
import pandas as pd
import time
from datetime import date
import re

import dash
from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px

import components.performance as perf
import components.history as his
import components.sidebar as sidebar
import components.help as help_tab
import components.footer as footer
import components.settings as settings

sidebar = sidebar.sidebar
tab1_content = perf.tab1_content
tab2_content = his.tab2_content
tab3_content = settings.tab3_content
help_content = help_tab.help
footer = footer.footer

tabs = dmc.Tabs(
    [
        dmc.TabsList(
            [
                dmc.Tab(
                    "パフォーマンス",
                    icon=DashIconify(icon="streamline:money-graph-bar-increase-up-product-performance-increase-arrow-graph-business-chart"),
                    value="performance",
                    className='tab',
                ),
                dmc.Tab(
                    "履歴",
                    icon=DashIconify(icon="material-symbols:history", width=25),
                    value="history",
                    className='tab'
                ),
                dmc.Tab(
                    "設定",
                    icon=DashIconify(icon="uil:setting", width=25),
                    value="settings",
                    className='tab'
                ),
                dmc.Tab(
                    "ヘルプ",
                    icon=DashIconify(icon="material-symbols:help", width=25),
                    value="help",
                    className='tab'
                ),
            ]
        ),
        dmc.TabsPanel(tab1_content, value="performance"),
        dmc.TabsPanel(tab2_content, value="history"),
        dmc.TabsPanel(tab3_content, value="settings"),
        dmc.TabsPanel(help_content, value="help"),
    ],
    value="performance",
    className='tabs-contena',
)

layout = dmc.NotificationsProvider(
    dbc.Container([
        dbc.Row(
            [
                dbc.Col(sidebar, id='side' ,width=4, className='bg-light', style={}),
                dbc.Col(
                    dbc.Row([tabs], id='top'),
                    width=8,
                    id='content',
                    style={},
                    className=''
                ),
                dbc.Row(footer, style={}, className='')
            ]
        ),
    ],fluid=True
    )
)