import dash_bootstrap_components as dbc
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify


tab3_content = html.Div([
    dbc.Card(
        dbc.CardBody([
            html.Div([
                html.P("制約条件", className="card-text fs-5 fw-bolder me-1"),
                DashIconify(
                    icon="gridicons:add-outline",
                    width=26,
                    className='mt-1' ,
                    color=""
                    ),
            ], className="d-flex ms-0 ps-0"),
            dmc.Textarea(
                id = 'chatgpt-constraints',
                placeholder="テキストを入力してください",
                autosize=True,
                minRows=3,
                size='sm',
                value="出力は「料理名」「材料」「作り方」「独創性」「おいしさ」「食感」「プロンプトに対する一致度」「塩味」「甘味」「酸味」「苦味」「旨味」「辛味」です。"),
            dmc.Button(
                "更新", 
                id = 'update-constraints-btn',
                variant='filled',
                n_clicks=0,
                color = 'blue',
                size= 'sm',
                className = 'mt-3'
            ),
            html.Div([
                html.P("改善文", className="card-text fs-5 fw-bolder me-1 mt-4"),
                DashIconify(
                    icon="iconamoon:trend-up-bold",
                    width=26,
                    className='mt-4' ,
                    color=""
                    ),
            ], className="d-flex ms-0 ps-0"),
            dmc.Textarea(
                id = 'chatgpt-improvement',
                placeholder="テキストを入力してください",
                autosize=True,
                minRows=3,
                size='sm',
                value="上記のレシピを参考に「〇〇」がさらに高まるよう、改良してください。",
            ),
            dmc.Button(
                "更新", 
                id = 'update-improvement-btn',
                variant='filled',
                n_clicks=0,
                color = 'blue',
                size= 'sm',
                className = 'mt-3'
            ),
            html.Div(id="update-constraints-notification"),
        ]),
        className="mt-3 bg-light",
    ),
], className='')