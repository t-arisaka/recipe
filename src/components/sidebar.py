import os
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# 画像生成ボタン
image_generate_button = dmc.Button("Generate Recipe Image", id="generate-image-btn")
# 画像表示エリア
image_display = html.Img(id="recipe-image", style={"max-width": "100%", "height": "auto"})

sidebar = html.Div([
    dbc.Row(
        [
            html.Div([
                html.Div([
                    html.H5('プロンプト', className="text-black fs-4 fw-bolder mt-3 mb-2 me-1 ms-1", style={'fontSize': '20px'}),
                    DashIconify(
                        icon="clarity:note-line",
                        width=30,
                        className='mt-3 mb-2' 
                        ),
                ], className="d-flex"),
                dmc.Textarea(
                    id = 'chatgpt-input',
                    placeholder="テキストを入力してください",
                    autosize=True,
                    minRows=15,
                    size='md'
                ),
                # ファイル選択エリアをコメントアウト
                # html.Div([
                #     html.H5('ファイル選択', className="text-black fs-4 fw-bolder mt-1 mb-1 me-7", style={'fontSize': '20px'}),
                #     DashIconify(
                #         icon="pepicons-pop:file",
                #         width=28,
                #         className='mt-1 mb-2 ms-2' 
                #     ),
                #     dmc.Select(
                #         #label="ファイル選択",
                #         placeholder="ファイルを選択してください", 
                #         className=" mt-1 mb-2 ms-3",
                #         id="file-select",
                #         data=[
                #             {"value": "1", "label": "monja1"},
                #             {"value": "2", "label": "monja2"},
                #             {"value": "3", "label": "monja3"},
                #             {"value": "4", "label": "monja4"},
                #             {"value": "5", "label": "monja5"},
                #             {"value": "6", "label": "monja6"},
                #             {"value": "7", "label": "monja7"},
                #             {"value": "8", "label": "monja8"},
                #             {"value": "9", "label": "monja9"},
                #         ],
                #         size="md",
                #         style={"width": "60%"}
                #     ),
                # ], className="d-flex justify-content-start mt-3"),
                dmc.Group(
                    [
                        dmc.Button(
                            "新規", 
                            id = 'chatgpt-btn-5times',
                            variant='filled',
                            n_clicks = 0,
                            size= 'sm',
                            className = 'mt-3',
                        ),
                        dmc.Button(
                            "追加", 
                            id = 'chatgpt-btn',
                            variant='filled',
                            n_clicks=0,
                            color = 'pink',
                            size= 'sm',
                            className = 'mt-3'
                        ),
                    ],
                    grow=True,
                ),
            ],className="mb-4")
        ]
    ),
    dbc.Row(
        [
            html.Div([

                html.Div([
                    html.H5('評価指標', className = "text-black fs-4 fw-bolder ", style={'fontSize': '20px'}),
                    DashIconify(
                        icon="file-icons:testcafe",
                        width=30,
                        className='ms-2'
                    ),
                    dmc.Select(
                        label="",
                        placeholder="選択してください",
                        id="eval-list",
                        value="fresh",
                        data=[
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
                        #style={"width": 200, "marginBottom": 10},
                        size="md",
                        style={"width": "60%"},
                        className='ms-2'
                    ),
                    dmc.Button(
                        "改善", 
                        id = 'improve-button',
                        variant='filled',
                        n_clicks=0,
                        color = 'green',
                        size= 'md',
                        className = 'ms-3'
                    ),
                ], className="d-flex align-items-center justify-content-start mt-3 mb-3"),     
            ])
        ])
    ], className='setting'
)