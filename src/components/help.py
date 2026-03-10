# Help Tab
import dash_bootstrap_components as dbc
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

help = html.Div([
    dbc.Card(
        dbc.CardBody(
            [
                html.P("ヘルプ", className="text-white fs-4 fw-bolder mb-0"),
                html.Hr(className='text-white mt-0'),
                
                # html.H4('Caution (Unavailable components)', className='text-white fw-bold mt-4 mb-0'),
                # html.Hr(className='m-0 p-0 text-white mb-2'),
                # html.P('・追加ボタン', className='text-white mb-1 fs-6 text-indent'),
                # html.P('・改善ボタン', className='text-white mb-1 fs-6 text-indent'),
                # html.P('・縦軸・横軸選択', className='text-white mb-1 fs-6 text-indent'),
                # html.P('・縦軸・横軸選択を変えたときに上の値表示は変わらない', className='text-white fs-6 text-indent'),
                
                html.H4('概要', className='text-white fw-bold mt-4 mb-0'),
                html.Hr(className='m-0 p-0 text-white mb-2'),
                html.P('・ChatGPTのAPIを使用し、料理レシピの考案、評価、比較ができるツールです。', className='text-white mb-1 fs-6 text-indent'),
                html.P('・プロンプトを入力すると、ChatGPTからの応答が反映されます。', className='text-white fs-6 text-indent'),
                
                html.H4('使用ツール', className='text-white fw-bold mt-4 mb-0'),
                html.Hr(className='m-0 p-0 text-white mb-2'),
                html.Span(
                    [
                        dbc.Badge("Python", color="success", className="me-1 mb-2"),
                        dbc.Badge("ChatGPT API", color="danger", className="me-1 mb-2"),
                        dbc.Badge("Visual Studio Code", color="secondary", className="me-1 mb-2"),
                        dbc.Badge("plotly dash", color="info", className="me-1 mb-2"),
                    ]
                ),
                
                html.Br(),
                
                html.H4('使い方', className='text-white fw-bold mt-4 mb-0'),
                html.Hr(className='m-0 p-0 text-white mb-3'),
                html.H5('サイドバー', className='text-white mb-0'),
                html.Hr(className='m-0 p-0 text-white mb-2'),
                html.Div([
                    html.Img(src='assets/img/setting_aroma.png', style={'width': '250px'}, className='my-2'),
                    html.Div([
                        html.P('・プロンプトを入力し、「新規」ボタンを押すと、ChatGPTからの応答が3つ得られます。', className='text-white fs-6 text-indent ms-2 my-2 mt-4'),
                        html.P('・プロンプトを入力し、「追加」ボタンを押すと、ChatGPTからの応答が1つ得られます。', className='text-white fs-6 text-indent ms-2 my-2 mt-4'),
                    ], className='help-subsection'),
                ], className='d-flex help-section mb-2'),
                
                html.Br(),
                
                html.H5('パフォーマンス', className='text-white mb-0'),
                html.Hr(className='m-0 p-0 text-white mb-2'),
                html.Div([
                    html.Div([
                        html.Img(src='assets/img/tab1-1_aroma.png', style={'width': '500px'}, className='my-2'),
                        html.Img(src='assets/img/tab1-2_aroma.png', style={'width': '500px'}, className='my-2'),
                    ], className='', style={'width': '500px'}),
                    html.Div([
                        dmc.Alert(
                            "Axis select components are not available(under construction).",
                            title="Note",
                            color='green',
                            icon=DashIconify(icon='mingcute:warning-line'),
                            className='ms-2 mb-2'
                        ),
                        html.P('・各評価項目を軸としたグラフが表示されます。', className='text-white fs-6 text-indent ms-2 my-2 mt-4'),
                        html.P('・クリックした点の調合、または、最新の調合が表示されます。', className='text-white fs-6 text-indent ms-2 my-2 mt-4'),
                        html.P('・最新の応答は赤い点で表されます。', className='text-white fs-6 text-indent ms-2 my-2 mt-4'),
                    ], className='help-subsection m-0 p-0'),
                ], className='d-flex help-section mb-2'),
                
                html.Br(),
                
                html.H5('履歴', className='text-white mb-0'),
                html.Hr(className='m-0 p-0 text-white mb-2'),
                html.Div([
                    html.Div([
                        html.Img(src='assets/img/tab2_aroma.png', style={'width': '500px'}, className='my-2'),
                    ], style={'width': '500px'}),
                    html.Div([
                        html.P('・履歴が表示されます。', className='text-white fs-6 text-indent ms-2 my-2 mt-4'),
                        html.P('・ドロップダウンから選択するとソートして表示します。', className='text-white fs-6 text-indent ms-2 my-2'),
                    ], className='help-subsection'),
                ], className='d-flex help-section mb-2'),
                
                html.Br(),

                html.H5('設定',className='text-white mb-0'),
                html.Hr(className='m-0 p-0 text-white mb-2'),
                html.Div([
                    html.Div([
                        html.Img(src='assets/img/tab3_aroma.png', style={'width': '500px'}, className='my-2'),
                    ],style={'width': '500px'}),
                    html.Div([
                        html.P('・プロンプトに追加する文章を設定します。',className='text-white fs-6 text-indent ms-2 my-2 mt-4'),
                        html.P('・制約条件はすべてのプロンプトに追加される文章です。',className='text-white fs-6 text-indent ms-2 my-2 mt-4'),
                        html.P('・改善文はサイドバーの「改善」を押した際に追加される文章です。',className='text-white fs-6 text-indent ms-2 my-2 mt-4'),
                        html.P('※制約条件の出力形式は変更しないでください。',className='text-white fs-6 text-indent ms-2 my-2 mt-4'),
                    ],className='help-subsection'),
                ],className='d-flex help-section mb-2'),

                html.Br(),
                
                html.H4('連絡先', className='text-white fw-bold text-decoration-underline'),
                html.Hr(className='m-0 p-0 text-white mb-2'),
                html.P('E-mail: taisei.arisaka@outlook.com', className='text-white'),
                html.Br(),
                
                # html.H4('References', className='text-white fw-bold text-decoration-underline'),
                # html.Hr(className='m-0 p-0 text-white mb-2'),
                # html.Div([
                # html.P('Coming soon', className='text-white'),]),
                # html.Br(),
            ]
        ),
        className="mt-3 bg-primary",
    ),
], className='mb-4'
)
