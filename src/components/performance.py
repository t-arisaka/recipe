import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# card1
card_1_1 = dbc.Spinner(dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.Div([
                        html.H6("独創性: ??点", className="fw-bold text-center", id="fig1_x_text"),
                        dmc.Select(
                            label="横軸",
                            placeholder="Select one",
                            id="fig1_x_axis",
                            value="originality",
                            data=[
                                # {"value": "fresh", "label": "さわやかな"},
                                # {"value": "kind", "label": "やさしい"},
                                # {"value": "natural", "label": "ナチュラルな"},
                                # {"value": "powerful", "label": "パワフルな"},
                                # {"value": "delicate", "label": "デリケートな"},
                                # {"value": "simple", "label": "シンプルな"},
                                # {"value": "youthful", "label": "若々しい"},
                                # {"value": "unique", "label": "個性的な"},
                                # {"value": "elegant", "label": "エレガントな"},
                                # {"value": "sexy", "label": "セクシーな"},
                                # {"value": "chic", "label": "シックな"},
                                # {"value": "refresh", "label": "リフレッシュする"},
                                # {"value": "relax", "label": "リラックスする"},
                                # {"value": "clean", "label": "クリーンな"},
                                # {"value": "dirty", "label": "ダーティな"},
                                # {"value": "women", "label": "女性的な"},
                                # {"value": "men", "label": "男性的な"},
                                # {"value": "cheap", "label": "チープな"},
                                # {"value": "rich", "label": "リッチな"},
                                # {"value": "dynamic", "label": "ダイナミックな"},
                                # {"value": "silent", "label": "静かな"},
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
                        ),
                    ]),
                    html.Div([
                        html.H6("おいしさ： ??点", className="fw-bold text-center", id="fig1_y_text"),
                        dmc.Select(
                            label="縦軸",
                            placeholder="Select one",
                            id="fig1_y_axis",
                            value="deliciousness",
                            data=[
                                # {"value": "fresh", "label": "さわやかな"},
                                # {"value": "kind", "label": "やさしい"},
                                # {"value": "natural", "label": "ナチュラルな"},
                                # {"value": "powerful", "label": "パワフルな"},
                                # {"value": "delicate", "label": "デリケートな"},
                                # {"value": "simple", "label": "シンプルな"},
                                # {"value": "youthful", "label": "若々しい"},
                                # {"value": "unique", "label": "個性的な"},
                                # {"value": "elegant", "label": "エレガントな"},
                                # {"value": "sexy", "label": "セクシーな"},
                                # {"value": "chic", "label": "シックな"},
                                # {"value": "refresh", "label": "リフレッシュする"},
                                # {"value": "relax", "label": "リラックスする"},
                                # {"value": "clean", "label": "クリーンな"},
                                # {"value": "dirty", "label": "ダーティな"},
                                # {"value": "women", "label": "女性的な"},
                                # {"value": "men", "label": "男性的な"},
                                # {"value": "cheap", "label": "チープな"},
                                # {"value": "rich", "label": "リッチな"},
                                # {"value": "dynamic", "label": "ダイナミックな"},
                                # {"value": "silent", "label": "静かな"},
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
                        ),
                    ]),
                    ], className='card-contena')])
           ), color='primary')

card_contena1 = dbc.Row(
    [
        dbc.Col(card_1_1, width=6),
        #dbc.Col(card_1_2, width=6),
    ], className='mt-3',
)

graph_1_1 = dbc.Spinner(dcc.Graph(className='tab1-fig', id='tab1-fig1', config={'displaylogo': False}), color='light')
graph_1_2 = dbc.Spinner(dcc.Graph(className='tab1-fig', id='tab1-fig2', config={'displaylogo': False}), color='light')
# ↓Mobile version
graph_1_1_sub = dbc.Spinner(dcc.Graph(className='tab1-fig', id='tab1-fig1-sub', config={'displaylogo': False}), color='light')
graph_1_2_sub = dbc.Spinner(dcc.Graph(className='tab1-fig', id='tab1-fig2-sub', config={'displaylogo': False}), color='light')

graph_contena1 = dbc.Row(
    [
        dbc.Col(graph_1_1, width=6),
        dbc.Col(graph_1_2, width=6),
    ], className='mt-3 graph-contena1'
)

# max-width: 1200px
graph_contena1_sub = dbc.Row(
    [
        dbc.Row([
            dbc.Col(
                graph_1_1_sub, width=12
            ) 
        ], className='mb-3'),
        dbc.Row([
            dbc.Col(
                graph_1_2_sub, width=12
            )
        ])
    ], className='mt-3 graph-contena1-sub'
)

# card2
graph_2_1 = dmc.Paper(
                children = [
                    dmc.Highlight(
                        '料理名',
                        highlight='料理名',
                        highlightColor='yellow'
                    ),
                    html.P(id = 'aroma_name'),
                    dmc.Highlight(
                        '材料',
                        highlight='材料',
                        highlightColor='yellow'
                    ),
                    html.P(id = 'aroma_materials'),
                    dmc.Highlight(
                        '作り方',
                        highlight='作り方',
                        highlightColor='yellow'
                    ),
                    html.P(id = 'aroma_recipe'),
                    dmc.Highlight(
                        'プロンプトに対する一致度',
                        highlight='プロンプトに対する一致度',
                        highlightColor='yellow'
                    ),
                    html.P(id = 'aroma_score'),
                ],
                radius='md',
                p= 'xl',
                shadow='sm',
                withBorder=True,
            )
graph_contena2 = dbc.Row(
    [
        dbc.Col(graph_2_1, width=12)
    ], className='mt-3'
)

tab1_content = html.Div([
    dbc.Card(
        dbc.CardBody(
            [
                html.Div([
                    html.P("グラフ", className="card-text text-white fs-4 fw-bolder me-2"),
                    DashIconify(
                        icon="mdi:graph-line",
                        width=31,
                        className='mt-1' ,
                        color="white"
                    ),
                ], className="d-flex"),
                graph_contena1,
                graph_contena1_sub,
                card_contena1,
                html.Div(id="notification")
                #graph_contena1_2,
            ]
        ),
        className="mt-3 bg-primary",
    ),
    dbc.Card(
        dbc.CardBody(
            [
                html.Div([
                    html.P("作り方", className="text-black fs-4 fw-bolder me-2"),
                    DashIconify(
                        icon="game-icons:cooking-pot",
                        width=38,
                        className='' 
                    ),
                ], className="d-flex"),
                graph_contena2,
            ],
        ),
        className="mt-3 bg-light",
    ),
], className='mb-3'
)