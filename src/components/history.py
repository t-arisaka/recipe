import dash_bootstrap_components as dbc
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

table = dbc.Spinner(dmc.Table(id="history-table"), color="primary")

tab2_content = html.Div([
    dbc.Card(
        dbc.CardBody([
            html.Div([
                html.Div([
                    html.P("プロンプト履歴", className="card-text fs-4 fw-bolder me-2"),
                    DashIconify(
                        icon="ph:note-light",
                        width=31,
                        className='mt-1' ,
                        color=""
                        ),
                    dmc.Button(
                        "更新", 
                        id = 'refresh-button',
                        variant='filled',
                        n_clicks=0,
                        size= 'md',
                        className = 'ms-3'
                    ),
                ], className="d-flex ms-0 ps-0"),
                dmc.Select(
                    label="",
                    placeholder="並び替え",
                    id="sort-col",
                    value="timescale",
                    data=[
                        {"value": "timescale", "label": "時刻"},
                        # {"value": "fresh", "label": "さわやかな順"},
                        # {"value": "kind", "label": "やさしい順"},
                        # {"value": "natural", "label": "ナチュラルな順"},
                        # {"value": "powerful", "label": "パワフルな順"},
                        # {"value": "delicate", "label": "デリケートな順"},
                        # {"value": "simple", "label": "シンプルな順"},
                        # {"value": "youthful", "label": "若々しい順"},
                        # {"value": "unique", "label": "個性的な順"},
                        # {"value": "elegant", "label": "エレガントな順"},
                        # {"value": "sexy", "label": "セクシーな順"},
                        # {"value": "chic", "label": "シックな順"},
                        # {"value": "refresh", "label": "リフレッシュする順"},
                        # {"value": "relax", "label": "リラックスする順"},
                        # {"value": "clean", "label": "クリーンな順"},
                        # {"value": "dirty", "label": "ダーティな順"},
                        # {"value": "women", "label": "女性的な順"},
                        # {"value": "men", "label": "男性的な順"},
                        # {"value": "cheap", "label": "チープな順"},
                        # {"value": "rich", "label": "リッチな順"},
                        # {"value": "dynamic", "label": "ダイナミックな順"},
                        # {"value": "silent", "label": "静かな順"},
                        {"value": "originality", "label": "独創性"},
                        {"value": "deliciousness", "label": "おいしさ"},
                        {"value": "texture", "label": "食感"},
                        {"value": "score", "label": "プロンプトに対する一致度"},
                        {"value": "salty", "label": "塩味"},
                        {"value": "sweet", "label": "甘味"},
                        {"value": "sour", "label": "酸味"},
                        {"value": "bitter", "label": "苦味"},
                        {"value": "umami", "label": "旨味"},
                        {"value": "spicy", "label": "辛味"}
                    ],
                    style={"width": 200, "marginBottom": 10},
                    className="ms-3 az"
                ),
            ], className="d-flex ms-3 justify-content-between"),
            table
        ]),
        className="mt-3 bg-light",
    ),
], className='')