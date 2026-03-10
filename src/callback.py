from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import os
import pandas as pd
import plotly.graph_objects as go
import openai
from dash import html
from dash.exceptions import PreventUpdate
import json
import datetime
import time
import re

from app import app

# API-KEY
openai.api_key = ''

# data, file_name
file_path = "../data/output_data_monja1.csv"
if os.path.isfile(file_path):
    data = pd.read_csv(file_path, index_col=0)
else:
    data = pd.DataFrame(columns=["時刻", "料理名", "材料", "作り方", "プロンプト", "独創性", "おいしさ", "食感", "プロンプトに対する一致度","塩味", "甘味", "酸味", "苦味", "旨味", "辛味"])
    # data = pd.DataFrame(columns=["時刻", "商品名", "材料", "プロンプト", "さわやかな", "やさしい", "ナチュラルな","パワフルな",
    #                              "デリケートな","シンプルな","若々しい","個性的な","エレガントな","セクシーな",
    #                              "シックな","リフレッシュする","リラックスする","クリーンな","ダーティな","女性的な","男性的な",
    #                              "チープな","リッチな","ダイナミックな","静かな","プロンプトに対する一致度"])
    data.to_csv(file_path)
    
# table-header
col_name = ["時刻", "料理名","独創性","おいしさ", "食感","プロンプトに対する一致度","塩味", "甘味", "酸味", "苦味", "旨味", "辛味"]
# col_name = ["時刻", "商品名",  "さわやかな", "やさしい", "ナチュラルな","パワフルな",
#              "デリケートな","シンプルな","若々しい","個性的な","エレガントな","セクシーな",
#              "シックな","リフレッシュする","リラックスする","クリーンな","ダーティな","女性的な","男性的な",
#              "チープな","リッチな","ダイナミックな","静かな","プロンプトに対する一致度"]
th = [html.Th(i) for i in col_name]
header = [ html.Thead( html.Tr( th ) ) ]

# key
dic = {"originality": "独創性", "deliciousness": "おいしさ","texture": "食感", "score":"プロンプトに対する一致度","salty": "塩味", "sweet": "甘味", "sour": "酸味", "bitter": "苦味", "umami": "旨味", "spicy": "辛味"}
# dic = {"fresh": "さわやかな",
#        "kind": "やさしい",
#        "natural": "ナチュラルな",
#        "powerful": "パワフルな",
#        "delicate": "デリケートな",
#        "simple": "シンプルな",
#        "youthful": "若々しい",
#        "unique": "個性的な",
#        "elegant": "エレガントな",
#        "sexy": "セクシーな",
#        "chic": "シックな",
#        "refresh": "リフレッシュする",
#        "relax": "リラックスする",
#        "clean": "クリーンな",
#        "dirty": "ダーティな",
#        "women": "女性的な",
#        "men": "男性的な",
#        "cheap": "チープな", 
#        "rich": "リッチな", 
#        "dynamic": "ダイナミックな",
#        "silent": "静かな",
#        "score": "プロンプトに対する一致度"}
modebar_setting = ['toImage', 'zoom2d', 'pan2d', 'select2d',  'lasso2d',  'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']


# constraints
constraints_path = "../data/constraints_monja.csv"
constraints = pd.read_csv(constraints_path, index_col=0)

#fig2のためのリスト
use_list=["独創性","おいしさ", "食感","プロンプトに対する一致度","塩味", "甘味", "酸味", "苦味", "旨味", "辛味"]
#use_list=['さわやかな','やさしい','ナチュラルな','パワフルな','デリケートな','シンプルな','若々しい','個性的な','エレガントな','セクシーな','シックな','リフレッシュする','リラックスする','クリーンな','ダーティな','女性的な','男性的な','チープな','リッチな','ダイナミックな','静かな','プロンプトに対する一致度']

# figure(base)
def initial_fig():
    layout = go.Layout(
        xaxis={'title': {'text': 'X', 'font': {'size': 15}}},
        yaxis={'title': {'text': 'Y', 'font': {'size': 15}}},
    )
    no_data_fig = go.Figure(layout=layout)
    no_data_fig.update_layout(
        annotations=[
            go.layout.Annotation(
                xref='paper',
                yref='paper',
                x=0.5,
                y=0.5,
                showarrow=False,
                text='No Figure',
                font={'size': 20}
            ),
        ],
        modebar_remove=modebar_setting,
        margin=dict(l=75, r=50, t=50, b=75),
        paper_bgcolor='rgb(236,240,241)',
        plot_bgcolor='rgb(236,240,241)',
    ),
    return no_data_fig

# figure
def make_figure(axis_x, axis_y, flag, idx):
    global data
    layout = go.Layout(
        xaxis={'title': {'text': axis_x, 'font': {'size': 15}}},
        yaxis={'title': {'text': axis_y, 'font': {'size': 15}}},
    )

    x = data[axis_x].to_list()[1:]
    y = data[axis_y].to_list()[1:]
    # print(x, y)
    trace = go.Scatter(x=x, y=y, mode="markers", showlegend=False)
    trace_latest = go.Scatter(x=[data.loc[0, axis_x]], y=[data.loc[0, axis_y]], mode="markers",
                            marker={"size": 10, "color": "red"}, showlegend=False)
    fig = go.Figure([trace, trace_latest], layout=layout)
    fig.update_layout(
        modebar_remove=modebar_setting,
        margin=dict(l=75, r=50, t=50, b=75),
        paper_bgcolor='rgb(236,240,241)',
        plot_bgcolor='rgb(236,240,241)',
    ),
    if flag:
        fig.add_trace(
            go.Scatter(
                x = [data.loc[idx+1, axis_x], data.loc[0, axis_x]],
                y = [data.loc[idx+1, axis_y], data.loc[0, axis_y]],
                mode = 'lines',
                showlegend=False
            )
        )
    return fig

def make_figure2(categories):
    categories = [*categories, categories[0]]  # レーダーチャートを閉じるために最初のカテゴリを最後に追加します

    # 空のデータトレースを作成
    trace_empty = go.Scatterpolar(
        r=[0] * len(categories),  # 各軸のデータポイント（空なので全て0）
        theta=categories,  # カテゴリー名
        fill='toself',
        showlegend=False
    )

    # レイアウト設定
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]  # デフォルトのレンジ設定
            )),
        showlegend=False
    )

    # 空のレーダーチャートを作成
    fig = go.Figure(data=[trace_empty], layout=layout)
    fig.update_layout(
        margin=dict(l=75, r=50, t=50, b=75),
        paper_bgcolor='rgb(236,240,241)',
        plot_bgcolor='rgb(236,240,241)',
    )

    return fig

# chatgpt-callback(1)
@app.callback(Output('tab1-fig1', 'figure', allow_duplicate=True),
              Output("tab1-fig2", "figure", allow_duplicate=True),
              Output("aroma_name", "children", allow_duplicate=True),
              Output("aroma_materials", "children", allow_duplicate=True),
              Output("aroma_recipe", "children", allow_duplicate=True),
              Output("aroma_score", "children", allow_duplicate=True),
              Output("notification", "children", allow_duplicate=True),
              Input('chatgpt-btn', 'n_clicks'),
              State('chatgpt-input', 'value'),
              State("chatgpt-constraints", "value"),
              State("fig1_x_axis", "value"),
              State("fig1_y_axis", "value"),
              #State("fig2_x_axis", "value"),
              #State("fig2_y_axis", "value"),
              prevent_initialcall=True
              )
def update_chatgpt_txt(n_clicks, prompt, constraints, fig1_x, fig1_y):#, fig2_x, fig2_y):
    global data
    if n_clicks:
        response = openai.ChatCompletion.create(
                        model = "gpt-4o",
                        messages = [
                            {"role": "system", "content": "あなたはもんじゃ焼き専門家です。"},
                            {"role": "system", "content": constraints},
                            {"role": "user", "content": prompt+"""
                            以下は条件です。また、料理名は個性的なものが望ましいです。材料は「辞書型」で出力、作り方は1から手順ごとにキーを振り、「辞書型」で出力してください。材料は小麦粉:20g、水:250g、ウスターソース:大さじ1.5、白だし:大さじ1の生地とキャベツ:180gを必須とし総重量は750g程度になるように調整してください。「独創性」「おいしさ」「食感」「プロンプトに対する一致度」「塩味」「甘味」「酸味」「苦味」「旨味」「辛味」は0～100数値が入るように点数をつけ、必ず「json形式」で出力してください。点数の小数点第1位は0以外も含まれることが望ましいです。
                            以下は各評価指標の評価基準です。評価基準に基づいて採点してください。
                            1.「独創性」：具材の組合せが新規性を持っているか
                             - 90～100: 他にはないユニークな具材やアイデアが取り入れられている。
                             - 70～89: 新規性があり魅力的だが完全に独自とは言えない。
                             - 50～69: 一般的な具材の組み合わせだが、少し工夫が感じられる。
                             - 30～49: 新規性が少なく、ありふれた具材の組み合わせ。
                             - 0～29: 極めて一般的で独創性が全く感じられない。
                            2.「おいしさ」：味の満足感があるか
                             - 90～100: 非常においしいと感じられ、バランスが完璧。
                             - 70～89: 十分においしく、バランスも良いが、改善の余地がある。
                             - 50～69: 可もなく不可もない味わい。
                             - 30～49: 味が単調またはバランスが悪い。
                             - 0～29: 味の満足感が非常に低い。
                            3.「食感」：食感が豊かであるか
                            - 90～100: 非常に多様な食感があり、バランスも良い。
                             - 70～89: 食感が豊かで、満足感が高い。
                             - 50～69: 食感に多少のバリエーションがあるが平凡。
                             - 30～49: 食感に乏しく、単調。
                             - 0～29: 食感がほとんどなく、満足感に欠ける。
                            4.「プロンプトに対する一致度」：条件以外のプロンプトの要求を満たしているか
                             - 90～100: プロンプト要求を完全に満たしており、期待以上の成果。
                             - 70～89: ほとんどの要求を満たしているが、細部に不足がある。
                             - 50～69: 基本的な要求は満たしているが、重要な要素が不足。
                             - 30～49: 多くの要求を満たしていないが、最低限の要素は含まれる。
                             - 0～29: プロンプトの要求をほとんど満たしていない。
                            5.「塩味」「甘味」「酸味」「苦味」「旨味」「辛味」：それぞれの強さ
                             - 90～100: 味が際立ちつつ、全体に調和している。
                             - 70～89: 味の特徴が十分に感じられる。
                             - 50～69: 味の特徴があるが、強さや調和が平凡。
                             - 30～49: 味の特徴が弱く、印象に残らない。
                             - 0～29: 味の特徴がほとんど感じられない。
                            以下の2点に違反すると罰則が課せられるので気を付けてください。
                            1、指定したフォーマットで出力すること。2、余計な文章を加えないこと。
                            """}
                        ],
                        temperature=1.0
                    )
        # response
        #print(response) #トークン数を出力
        text = response['choices'][0]['message']['content']
        print(text)
        try:
            # 正規表現パターンを定義
            pattern = r"(\{.*\})"

            # パターンに一致する部分を検索
            matches = re.findall(pattern, text, re.DOTALL)

            # 一致した部分をリスト形式に戻す
            if matches:
                text = matches[0]
                print(text)
            else:
                print("辞書型の部分が見つかりませんでした。")

        except:
            print('error')

        try:
            text_json = json.loads(text)
            # print(text_json)
            # print(text_json["料理名"])
            concat_data = pd.DataFrame([[str(datetime.datetime.now()).split('.')[0],
                                         text_json["料理名"], text_json["材料"],text_json["作り方"], prompt, text_json["独創性"],text_json["おいしさ"], text_json["食感"], text_json["プロンプトに対する一致度"],text_json["塩味"],text_json["甘味"],text_json["酸味"],text_json["苦味"],text_json["旨味"],text_json["辛味"]
                                        #  text_json["さわやかな"], text_json["やさしい"], text_json["ナチュラルな"],
                                        #  text_json["パワフルな"], text_json["デリケートな"], text_json["シンプルな"],
                                        #  text_json["若々しい"], text_json["個性的な"], text_json["エレガントな"],
                                        #  text_json["セクシーな"], text_json["シックな"], text_json["リフレッシュする"],
                                        #  text_json["リラックスする"], text_json["クリーンな"], text_json["ダーティな"],
                                        #  text_json["女性的な"], text_json["男性的な"], text_json["チープな"],
                                        #  text_json["リッチな"], text_json["ダイナミックな"], text_json["静かな"],
                                        #  text_json["プロンプトに対する一致度"]
                                         ]], 
                                         columns=["時刻", "料理名", "材料","作り方" , "プロンプト","独創性","おいしさ","食感","プロンプトに対する一致度", "塩味", "甘味", "酸味", "苦味", "旨味", "辛味"])
                                                #    "さわやかな", "やさしい", "ナチュラルな",
                                                #    "パワフルな", "デリケートな", "シンプルな",
                                                #    "若々しい", "個性的な", "エレガントな",
                                                #    "セクシーな", "シックな", "リフレッシュする",
                                                #    "リラックスする", "クリーンな", "ダーティな",
                                                #    "女性的な", "男性的な", "チープな",
                                                #    "リッチな", "ダイナミックな", "静かな","プロンプトに対する一致度"])
            data = pd.concat([concat_data, data])
            data = data.reset_index(drop=True)
            # print(data)
            data.to_csv(file_path)
            aroma_name = text_json["料理名"]
            # 材料
            materials_p = []
            materials = text_json["材料"]
            for key, value in materials.items():
                materials_p.append(f'{key} : {value}')
                materials_p.append(html.Br())
            # # 作り方
            recipe_p = []
            recipe = text_json["作り方"]
            for key, value in recipe.items():
                recipe_p.append(f'{key} : {value}')
                recipe_p.append(html.Br())
            # スコア
            aroma_score = text_json["プロンプトに対する一致度"]
            note = dmc.Notification(
                    title="Success",
                    id="simple-notify",
                    action="show",
                    color="green",
                    message="Successfully obtained output.",
                    icon=DashIconify(icon="mdi:success-bold"),
            )
        except:
            # print("error")
            aroma_name = data.loc[0, "料理名"]
            # 材料
            materials_p = []
            materials= data.loc[0, ['材料']].values[0]
            materials = materials.replace("'", "\"")
            materials_obj = json.loads(materials)
            for key, value in materials_obj.items():
                materials_p.append(f'{key} : {value}')
                materials_p.append(html.Br())
            # # 作り方
            recipe_p = []
            recipe = data.loc[0, ['作り方']].values[0]
            recipe = recipe.replace("'", "\"")
            recipe_obj = json.loads(recipe)
            for key, value in recipe_obj.items():
                recipe_p.append(f'{key} : {value}')
                recipe_p.append(html.Br())
            aroma_score = data.loc[0, "プロンプトに対する一致度"]
            note = dmc.Notification(
                    title="Failed",
                    id="simple-notify",
                    action="show",
                    color="red",
                    message="We couldn't get the expected output",
                    icon=DashIconify(icon="material-symbols:error"),
            )


        fig = make_figure(dic[fig1_x], dic[fig1_y], False, 0)
        use_list=['独創性','おいしさ','食感','プロンプトに対する一致度', '塩味', '甘味', '酸味', '苦味', '旨味', '辛味']
        #use_list=['さわやかな','やさしい','ナチュラルな','パワフルな','デリケートな','シンプルな','若々しい','個性的な','エレガントな','セクシーな','シックな','リフレッシュする','リラックスする','クリーンな','ダーティな','女性的な','男性的な','チープな','リッチな','ダイナミックな','静かな','プロンプトに対する一致度']
        fig2 = make_figure2(use_list)

        return fig, fig2, aroma_name, materials_p, recipe_p, aroma_score, [note]
    
    else:
        if len(data)==0: fig1, fig2 = initial_fig(), initial_fig()
        else:
            fig1 = make_figure(dic[fig1_x], dic[fig1_y], False, 0)
            use_list=['独創性','おいしさ','食感','プロンプトに対する一致度','塩味', '甘味', '酸味', '苦味', '旨味', '辛味']
            #use_list=['さわやかな','やさしい','ナチュラルな','パワフルな','デリケートな','シンプルな','若々しい','個性的な','エレガントな','セクシーな','シックな','リフレッシュする','リラックスする','クリーンな','ダーティな','女性的な','男性的な','チープな','リッチな','ダイナミックな','静かな','プロンプトに対する一致度']
            fig2 = make_figure2(use_list)
        return fig1, fig2, "", "", "","", []
    
# click plot and show recipe
@app.callback(
    Output('aroma_name', 'children', allow_duplicate=True),
    Output('aroma_materials', 'children', allow_duplicate=True),
    Output('aroma_recipe', 'children', allow_duplicate=True),
    Output("aroma_score", "children", allow_duplicate=True),
    Output("chatgpt-input", "value", allow_duplicate=True),
    Output("fig1_x_text", "children", allow_duplicate=True),
    Output("fig1_y_text", "children", allow_duplicate=True),
    # どこをclickしたのかを表示する
    Output('tab1-fig1', 'figure', allow_duplicate=True),
    Output("tab1-fig2", "figure", allow_duplicate=True),
    Input('tab1-fig1', 'clickData'),
    State("fig1_x_axis", "value"),
    State("fig1_y_axis", "value"),
    #State("fig2_x_axis", "value"),
    #State("fig2_y_axis", "value"),
)
def show_clickData(fig1_clickData, fig1_x_axis, fig1_y_axis):#, fig2_x_axis, fig2_y_axis):
    global index
    if fig1_clickData is None:
        raise PreventUpdate
    else:
        df = pd.read_csv(file_path, index_col=0)
        #print(fig1_clickData)
        index = fig1_clickData['points'][0]['pointIndex']
        #print(index)
        x_value = fig1_clickData['points'][0]['x']
        y_value = fig1_clickData['points'][0]['y']
        if index!=0: index+=1
        else:
            if not(df.loc[index, dic[fig1_x_axis]]==x_value and df.loc[index, dic[fig1_y_axis]]==y_value):
                index += 1
        # 料理名
        aroma_name = df.loc[index, ['料理名']].values[0]
        # 材料
        materials_p = []
        materials = df.loc[index, ['材料']].values[0]
        materials = materials.replace("'", "\"")
        materials_obj = json.loads(materials)
        for key, value in materials_obj.items():
            materials_p.append(f'{key} : {value}')
            materials_p.append(html.Br())
        # 作り方
        recipe_p = []
        recipe = data.loc[index, ['作り方']].values[0]
        #print(recipe, type(recipe))
        recipe = str(recipe).replace("'", "\"")
        recipe_obj = json.loads(recipe)
        for key, value in recipe_obj.items():
            recipe_p.append(f'{key} : {value}')
            recipe_p.append(html.Br())
        aroma_score = df.loc[index, ['プロンプトに対する一致度']].values[0]
        prompt = df.loc[index, ["プロンプト"]].values[0]

        output_text1 = f"{dic[fig1_x_axis]}: {df.loc[index, dic[fig1_x_axis]]}"
        output_text2 = f"{dic[fig1_y_axis]}: {df.loc[index, dic[fig1_y_axis]]}"

        fig1 = make_figure(dic[fig1_x_axis], dic[fig1_y_axis], False, 0)
        fig1.add_trace(
            go.Scatter(
                x = [df.loc[index, dic[fig1_x_axis]]],
                y = [df.loc[index, dic[fig1_y_axis]]],
                showlegend=False,
                mode = 'markers',
                marker= {'size': 8, 'color': 'orange'}
            )
        )
        use_list=['独創性','おいしさ','食感','プロンプトに対する一致度','塩味', '甘味', '酸味', '苦味', '旨味', '辛味']
        #use_list=['さわやかな','やさしい','ナチュラルな','パワフルな','デリケートな','シンプルな','若々しい','個性的な','エレガントな','セクシーな','シックな','リフレッシュする','リラックスする','クリーンな','ダーティな','女性的な','男性的な','チープな','リッチな','ダイナミックな','静かな','プロンプトに対する一致度']
        fig2 = fig2 = make_figure2(use_list)
        chartlist=[]
        for i in range(len(use_list)):
            chartlist.append(df.loc[index, use_list[i]])
        chartlist.append(df.loc[index, use_list[0]])
        use_list2=['独創性','おいしさ','食感','プロンプトに対する一致度','塩味', '甘味', '酸味', '苦味', '旨味', '辛味']
        #use_list2=['さわやかな','やさしい','ナチュラルな','パワフルな','デリケートな','シンプルな','若々しい','個性的な','エレガントな','セクシーな','シックな','リフレッシュする','リラックスする','クリーンな','ダーティな','女性的な','男性的な','チープな','リッチな','ダイナミックな','静かな','プロンプトに対する一致度','さわやかな']
        fig2.add_trace(
            go.Scatterpolar(
                r = chartlist,
                theta = use_list2,
                fill = 'toself'
            )
        )
        fig2.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]  # 必要に応じて範囲を設定
                )
            ),
            showlegend=False
        )
       #print(chartlist)
        #print(0)
        return aroma_name, materials_p,recipe_p, aroma_score, prompt, output_text1, output_text2, fig1, fig2
    
# history-table
pre_nc = 0
@app.callback(Output("history-table", "children", allow_duplicate=True),
              Input('chatgpt-btn', 'n_clicks',),
              Input('sort-col', 'value'),
              )
def update_table(nc, v):
    global pre_nc
    if nc!=pre_nc:
        time.sleep(10)
        pre_nc = nc
    data = pd.read_csv("../data/output_data_monja.csv", index_col=0)
    if v=="timescale":
        idx = list(data.index)
        #print(idx)
    # elif v=="fresh":
    #     idx = data.sort_values("さわやかな", ascending=False).index.to_list()
    # elif v=="kind":
    #     idx = data.sort_values("やさしい", ascending=False).index.to_list()
    # elif v=="natural":
    #     idx = data.sort_values("ナチュラルな", ascending=False).index.to_list()
    # elif v=="powerful":
    #     idx = data.sort_values("パワフルな", ascending=False).index.to_list()
    # elif v=="delicate":
    #     idx = data.sort_values("デリケートな", ascending=False).index.to_list()
    # elif v=="simple":
    #     idx = data.sort_values("シンプルな", ascending=False).index.to_list()
    # elif v=="youthful":
    #     idx = data.sort_values("若々しい", ascending=False).index.to_list()
    # elif v=="unique":
    #     idx = data.sort_values("個性的な", ascending=False).index.to_list()
    # elif v=="elegant":
    #     idx = data.sort_values("エレガントな", ascending=False).index.to_list()
    # elif v=="sexy":
    #     idx = data.sort_values("セクシーな", ascending=False).index.to_list()
    # elif v=="chic":
    #     idx = data.sort_values("シックな", ascending=False).index.to_list()
    # elif v=="refresh":
    #     idx = data.sort_values("リフレッシュする", ascending=False).index.to_list()
    # elif v=="relax":
    #     idx = data.sort_values("リラックスする", ascending=False).index.to_list()
    # elif v=="clean":
    #     idx = data.sort_values("クリーンな", ascending=False).index.to_list()
    # elif v=="dirty":
    #     idx = data.sort_values("ダーティな", ascending=False).index.to_list()
    # elif v=="women":
    #     idx = data.sort_values("女性的な", ascending=False).index.to_list()
    # elif v=="men":
    #     idx = data.sort_values("男性的な", ascending=False).index.to_list()
    # elif v=="cheap":
    #     idx = data.sort_values("チープな", ascending=False).index.to_list()
    # elif v=="rich":
    #     idx = data.sort_values("リッチな", ascending=False).index.to_list()
    # elif v=="dynamic":
    #     idx = data.sort_values("ダイナミックな", ascending=False).index.to_list()
    # elif v=="silent":
    #     idx = data.sort_values("静かな", ascending=False).index.to_list()
    elif v=="originality":
        idx = data.sort_values("独創性", ascending=False).index.to_list()
    elif v=="deliciousness":
        idx = data.sort_values("おいしさ", ascending=False).index.to_list()
    elif v=="texture":
        idx = data.sort_values("食感", ascending=False).index.to_list()
    elif v=="score":
        idx = data.sort_values("プロンプトに対する一致度", ascending=False).index.to_list()
    elif v == "salty":
        idx = data.sort_values("塩味", ascending=False).index.to_list()
    elif v == "sweet":
        idx = data.sort_values("甘味", ascending=False).index.to_list()
    elif v == "sour":
        idx = data.sort_values("酸味", ascending=False).index.to_list()
    elif v == "bitter":
        idx = data.sort_values("苦味", ascending=False).index.to_list()
    elif v == "umami":
        idx = data.sort_values("旨味", ascending=False).index.to_list()
    elif v == "spicy":
        idx = data.sort_values("辛味", ascending=False).index.to_list()

    body = []
    for i in idx:
        el = [html.Td(data.loc[i, col]) for col in col_name]
        body.append(html.Tr(el))

    return header+[html.Tbody(body)]

# update figure
@app.callback(Output("tab1-fig1", "figure"),
              Input('fig1_x_axis', 'value'),
              Input('fig1_y_axis', 'value'),
              )
def update_fig1(v1, v2):
    fig = make_figure(dic[v1], dic[v2], False, 0)
    return fig

# update constraints
@app.callback(Output("update-constraints-notification", "children"),
              Output("chatgpt-constraints", "value"),
              Input('update-constraints-btn', 'n_clicks'),
              State("chatgpt-constraints", "value")
              )
def update_constraints(n_clicks, const_text):
    if n_clicks==0: return [], constraints.iloc[0, 0]
    else:
        constraints.iloc[0, 0] = const_text
        constraints.to_csv(constraints_path)
        note = dmc.Notification(
                title="Saved",
                id="simple-notify",
                action="show",
                color="green",
                message="Saved new constraints",
                icon=DashIconify(icon="mdi:success-bold"),
        )
        return [note], const_text

@app.callback(Output("notification", "children", allow_duplicate=True),
              Output('tab1-fig1', 'figure', allow_duplicate=True),
              Output("tab1-fig2", "figure", allow_duplicate=True),
              Output("aroma_name", "children", allow_duplicate=True),
              Output("aroma_materials", "children", allow_duplicate=True),
              Output("aroma_recipe", "children", allow_duplicate=True),
              Output("aroma_score", "children", allow_duplicate=True),
              State('eval-list', 'value'),
              State('chatgpt-input', 'value'),
              State('chatgpt-improvement', 'value'),
              State("fig1_x_axis", "value"),
              State("fig1_y_axis", "value"),
              Input('improve-button', 'n_clicks'),
              State("aroma_name", "children"),
              State("aroma_materials", "children"),
              State("aroma_recipe", "children"),
              prevent_initial_call=True,
              )
def improve_chatgpt_txt(eval_list, chatgpt_prompt, chatgpt_improvement_prompt, fig1_x, fig1_y, n_clicks, input_name, input_materials, input_recipe):
    global data, index
    if n_clicks:
        if chatgpt_prompt == '':
            note = dmc.Notification(
                title="Error",
                id="simple-notify",
                action="show",
                color="red",
                message="グラフのプロットをクリックしてから改善ボタンを押してください",
                icon=DashIconify(icon="material-symbols:error"),
            )
            return '', [note]
        
        else:
            note = dmc.Notification(
                title="Success",
                id="simple-notify",
                action="show",
                color="blue",
                message="改善しました",
                icon=DashIconify(icon="mdi:success-bold"),
            )
            if "[料理名]" in chatgpt_prompt:
                # prompt
                chatgpt_improvement_prompt = chatgpt_improvement_prompt.replace('〇〇', dic[eval_list])
                #prompt = f'{chatgpt_prompt}\n' + f'{chatgpt_improvement_prompt}'
                # 材料
                cnt=int(len(input_materials)/2)
                for i in range(1,cnt+1):
                    input_materials.pop(i)
                    #print(input_materials)
                
                # レシピ
                cnt=int(len(input_recipe)/2)
                for i in range(1,cnt+1):
                    input_recipe.pop(i)
                    
                # 正規表現パターンを定義
                pattern = r"\[プロンプト\]\n(.*?)\n\["

                # パターンに一致する部分を検索
                match = re.search(pattern, chatgpt_prompt, re.DOTALL)

                # 一致部分が見つかった場合はそのテキストを取得
                if match:
                    chatgpt_prompt_loop = match.group(1)
                    #print(chatgpt_prompt_loop)
                else:
                    print("プロンプトの項目が見つかりませんでした。")

                prompt = f'[プロンプト]\n{chatgpt_prompt_loop}\n'+f'[料理名]\n{input_name}\n'+f'[材料]\n{input_materials}\n'+f'[作り方]\n{input_recipe}\n'+f'{chatgpt_improvement_prompt}'

                response = openai.ChatCompletion.create(
                                model = "gpt-4o",
                                messages = [
                                    {"role": "system", "content": "あなたはもんじゃ焼き専門家です。"},
                                    {"role": "system", "content": constraints.iloc[0, 0]},
                                    {"role": "user", "content": prompt+"""
                                    以下は条件です。また、料理名は個性的なものが望ましいです。材料は「辞書型」で出力、作り方は1から手順ごとにキーを振り、「辞書型」で出力してください。材料は小麦粉:20g、水:250g、ウスターソース:大さじ1.5、白だし:大さじ1の生地とキャベツ:180gを必須とし総重量は750g程度になるように調整してください。「独創性」「おいしさ」「食感」「プロンプトに対する一致度」「塩味」「甘味」「酸味」「苦味」「旨味」「辛味」は0～100数値が入るように点数をつけ、必ず「json形式」で出力してください。点数の小数点第1位は0以外も含まれることが望ましいです。
                                    以下は各評価指標の評価基準です。評価基準に基づいて採点してください。
                                    1.「独創性」：具材の組合せが新規性を持っているか
                                     - 90～100: 他にはないユニークな具材やアイデアが取り入れられている。
                                     - 70～89: 新規性があり魅力的だが完全に独自とは言えない。
                                     - 50～69: 一般的な具材の組み合わせだが、少し工夫が感じられる。
                                     - 30～49: 新規性が少なく、ありふれた具材の組み合わせ。
                                     - 0～29: 極めて一般的で独創性が全く感じられない。
                                    2.「おいしさ」：味の満足感があるか
                                     - 90～100: 非常においしいと感じられ、バランスが完璧。
                                     - 70～89: 十分においしく、バランスも良いが、改善の余地がある。
                                     - 50～69: 可もなく不可もない味わい。
                                     - 30～49: 味が単調またはバランスが悪い。
                                     - 0～29: 味の満足感が非常に低い。
                                    3.「食感」：食感が豊かであるか
                                    - 90～100: 非常に多様な食感があり、バランスも良い。
                                     - 70～89: 食感が豊かで、満足感が高い。
                                     - 50～69: 食感に多少のバリエーションがあるが平凡。
                                     - 30～49: 食感に乏しく、単調。
                                     - 0～29: 食感がほとんどなく、満足感に欠ける。
                                    4.「プロンプトに対する一致度」：条件以外のプロンプトの要求を満たしているか
                                     - 90～100: プロンプト要求を完全に満たしており、期待以上の成果。
                                     - 70～89: ほとんどの要求を満たしているが、細部に不足がある。
                                     - 50～69: 基本的な要求は満たしているが、重要な要素が不足。
                                     - 30～49: 多くの要求を満たしていないが、最低限の要素は含まれる。
                                     - 0～29: プロンプトの要求をほとんど満たしていない。
                                    5.「塩味」「甘味」「酸味」「苦味」「旨味」「辛味」：それぞれの強さ
                                     - 90～100: 味が際立ちつつ、全体に調和している。
                                     - 70～89: 味の特徴が十分に感じられる。
                                     - 50～69: 味の特徴があるが、強さや調和が平凡。
                                     - 30～49: 味の特徴が弱く、印象に残らない。
                                     - 0～29: 味の特徴がほとんど感じられない。
                                    以下の2点に違反すると罰則が課せられるので気を付けてください。
                                    1、指定したフォーマットで出力すること。2、余計な文章を加えないこと。
                                    """}
                                ],
                                temperature=1.0
                            )
                # response
                text = response['choices'][0]['message']['content']
                print(text)

            else:
                # prompt
                chatgpt_improvement_prompt = chatgpt_improvement_prompt.replace('〇〇', dic[eval_list])
                #prompt = f'{chatgpt_prompt}\n' + f'{chatgpt_improvement_prompt}'
                # 材料
                cnt=int(len(input_materials)/2)
                for i in range(1,cnt+1):
                    input_materials.pop(i)
                    #print(input_materials)
                # レシピ
                cnt=int(len(input_recipe)/2)
                for i in range(1,cnt+1):
                    input_recipe.pop(i)

                #input_recipe = input_recipe.replace("', {'props': {'children': None}, 'type': 'Br', 'namespace': 'dash_html_components'}","")
                
                prompt = f'[プロンプト]\n{chatgpt_prompt}\n'+f'[料理名]\n{input_name}\n'+f'[材料]\n{input_materials}\n'+f'[作り方]\n{input_recipe}\n'+f'{chatgpt_improvement_prompt}'

                #print(prompt)
                response = openai.ChatCompletion.create(
                                model = "gpt-4o",
                                messages = [
                                    {"role": "system", "content": "あなたはもんじゃ焼き専門家です。"},
                                    {"role": "system", "content": constraints.iloc[0, 0]},
                                    {"role": "user", "content": prompt+"""
                                    以下は条件です。また、料理名は個性的なものが望ましいです。材料は「辞書型」で出力、作り方は1から手順ごとにキーを振り、「辞書型」で出力してください。材料は小麦粉:20g、水:250g、ウスターソース:大さじ1.5、白だし:大さじ1の生地とキャベツ:180gを必須とし総重量は750g程度になるように調整してください。「独創性」「おいしさ」「食感」「プロンプトに対する一致度」「塩味」「甘味」「酸味」「苦味」「旨味」「辛味」は0～100数値が入るように点数をつけ、必ず「json形式」で出力してください。点数の小数点第1位は0以外も含まれることが望ましいです。
                                    以下は各評価指標の評価基準です。評価基準に基づいて採点してください。
                                    1.「独創性」：具材の組合せが新規性を持っているか
                                     - 90～100: 他にはないユニークな具材やアイデアが取り入れられている。
                                     - 70～89: 新規性があり魅力的だが完全に独自とは言えない。
                                     - 50～69: 一般的な具材の組み合わせだが、少し工夫が感じられる。
                                     - 30～49: 新規性が少なく、ありふれた具材の組み合わせ。
                                     - 0～29: 極めて一般的で独創性が全く感じられない。
                                    2.「おいしさ」：味の満足感があるか
                                     - 90～100: 非常においしいと感じられ、バランスが完璧。
                                     - 70～89: 十分においしく、バランスも良いが、改善の余地がある。
                                     - 50～69: 可もなく不可もない味わい。
                                     - 30～49: 味が単調またはバランスが悪い。
                                     - 0～29: 味の満足感が非常に低い。
                                    3.「食感」：食感が豊かであるか
                                    - 90～100: 非常に多様な食感があり、バランスも良い。
                                     - 70～89: 食感が豊かで、満足感が高い。
                                     - 50～69: 食感に多少のバリエーションがあるが平凡。
                                     - 30～49: 食感に乏しく、単調。
                                     - 0～29: 食感がほとんどなく、満足感に欠ける。
                                    4.「プロンプトに対する一致度」：条件以外のプロンプトの要求を満たしているか
                                     - 90～100: プロンプト要求を完全に満たしており、期待以上の成果。
                                     - 70～89: ほとんどの要求を満たしているが、細部に不足がある。
                                     - 50～69: 基本的な要求は満たしているが、重要な要素が不足。
                                     - 30～49: 多くの要求を満たしていないが、最低限の要素は含まれる。
                                     - 0～29: プロンプトの要求をほとんど満たしていない。
                                    5.「塩味」「甘味」「酸味」「苦味」「旨味」「辛味」：それぞれの強さ
                                     - 90～100: 味が際立ちつつ、全体に調和している。
                                     - 70～89: 味の特徴が十分に感じられる。
                                     - 50～69: 味の特徴があるが、強さや調和が平凡。
                                     - 30～49: 味の特徴が弱く、印象に残らない。
                                     - 0～29: 味の特徴がほとんど感じられない。
                                    以下の2点に違反すると罰則が課せられるので気を付けてください。
                                    1、指定したフォーマットで出力すること。2、余計な文章を加えないこと。
                                    """}
                                ],
                                temperature=1.0
                            )
                # response
                text = response['choices'][0]['message']['content']
                print(text)
                # chatgpt_prompt_loop=chatgpt_prompt
            try:
                # 正規表現パターンを定義
                pattern = r"(\{.*\})"

                # パターンに一致する部分を検索
                matches = re.findall(pattern, text, re.DOTALL)

                # 一致した部分をリスト形式に戻す
                if matches:
                    text = matches[0]
                    print(text)
                else:
                    print("辞書型の部分が見つかりませんでした。")

            except:
                print('error')
            
            try:
                text_json = json.loads(text)
                # print(text_json)
                # print(text_json["料理名"])
                concat_data = pd.DataFrame([[str(datetime.datetime.now()).split('.')[0],
                                         text_json["料理名"], text_json["材料"],text_json["作り方"], prompt, text_json["独創性"],text_json["おいしさ"],text_json["食感"],text_json["プロンプトに対する一致度"],text_json["塩味"],text_json["甘味"],text_json["酸味"],text_json["苦味"],text_json["旨味"],text_json["辛味"]
                                        #  text_json["さわやかな"], text_json["やさしい"], text_json["ナチュラルな"],
                                        #  text_json["パワフルな"], text_json["デリケートな"], text_json["シンプルな"],
                                        #  text_json["若々しい"], text_json["個性的な"], text_json["エレガントな"],
                                        #  text_json["セクシーな"], text_json["シックな"], text_json["リフレッシュする"],
                                        #  text_json["リラックスする"], text_json["クリーンな"], text_json["ダーティな"],
                                        #  text_json["女性的な"], text_json["男性的な"], text_json["チープな"],
                                        #  text_json["リッチな"], text_json["ダイナミックな"], text_json["静かな"],
                                        #  text_json["プロンプトに対する一致度"]
                                         ]], 
                                         columns=["時刻", "料理名", "材料","作り方" , "プロンプト","独創性","おいしさ","食感", "プロンプトに対する一致度","塩味", "甘味", "酸味", "苦味", "旨味", "辛味"])
                                                #    "さわやかな", "やさしい", "ナチュラルな",
                                                #    "パワフルな", "デリケートな", "シンプルな",
                                                #    "若々しい", "個性的な", "エレガントな",
                                                #    "セクシーな", "シックな", "リフレッシュする",
                                                #    "リラックスする", "クリーンな", "ダーティな",
                                                #    "女性的な", "男性的な", "チープな",
                                                #    "リッチな", "ダイナミックな", "静かな","プロンプトに対する一致度"])
                data = pd.concat([concat_data, data])
                data = data.reset_index(drop=True)
                # print(data)
                data.to_csv(file_path)
                aroma_name = text_json["料理名"]
                # 材料
                materials_p = []
                materials = text_json["材料"]
                for key, value in materials.items():
                    materials_p.append(f'{key} : {value}')
                    materials_p.append(html.Br())
                # 作り方
                recipe_p = []
                recipe = text_json["作り方"]
                for key, value in recipe.items():
                    recipe_p.append(f'{key} : {value}')
                    recipe_p.append(html.Br())
                # スコア
                aroma_score = text_json["プロンプトに対する一致度"]
                note = dmc.Notification(
                        title="Success",
                        id="simple-notify",
                        action="show",
                        color="green",
                        message="Successfully obtained output.",
                        icon=DashIconify(icon="mdi:success-bold"),
                )
            except:
                # print("error")
                aroma_name = data.loc[0, "料理名"]
                # 材料
                materials_p = []
                materials= data.loc[0, ['材料']].values[0]
                materials = materials.replace("'", "\"")
                materials_obj = json.loads(materials)
                for key, value in materials_obj.items():
                    materials_p.append(f'{key} : {value}')
                    materials_p.append(html.Br())
                # 作り方
                recipe_p = []
                recipe = data.loc[0, ['作り方']].values[0]
                recipe = recipe.replace("'", "\"")
                recipe_obj = json.loads(recipe)
                for key, value in recipe_obj.items():
                    recipe_p.append(f'{key} : {value}')
                    recipe_p.append(html.Br())
                aroma_score = data.loc[0, "プロンプトに対する一致度"]
                note = dmc.Notification(
                        title="Failed",
                        id="simple-notify",
                        action="show",
                        color="red",
                        message="We couldn't get the expected output",
                        icon=DashIconify(icon="material-symbols:error"),
                )


            fig = make_figure(dic[fig1_x], dic[fig1_y], False, 0)
            use_list=['独創性','おいしさ','食感','プロンプトに対する一致度','塩味', '甘味', '酸味', '苦味', '旨味', '辛味']
            #use_list=['さわやかな','やさしい','ナチュラルな','パワフルな','デリケートな','シンプルな','若々しい','個性的な','エレガントな','セクシーな','シックな','リフレッシュする','リラックスする','クリーンな','ダーティな','女性的な','男性的な','チープな','リッチな','ダイナミックな','静かな','プロンプトに対する一致度']
            fig2 = make_figure2(use_list)

            return [note], fig, fig2, aroma_name, materials_p, recipe_p, aroma_score
        
    else:
        if len(data)==0: fig1, fig2 = initial_fig(), initial_fig()
        else:
            fig1 = make_figure(dic[fig1_x], dic[fig1_y], False, 0)
            use_list=['独創性','おいしさ','食感','プロンプトに対する一致度','塩味', '甘味', '酸味', '苦味', '旨味', '辛味']
            #use_list=['さわやかな','やさしい','ナチュラルな','パワフルな','デリケートな','シンプルな','若々しい','個性的な','エレガントな','セクシーな','シックな','リフレッシュする','リラックスする','クリーンな','ダーティな','女性的な','男性的な','チープな','リッチな','ダイナミックな','静かな','プロンプトに対する一致度']
            fig2 = make_figure2(use_list)
        return [], fig1, fig2, "", "", "",""


# chatgpt-callback(3 times)
@app.callback(Output('tab1-fig1', 'figure', allow_duplicate=True),
              Output("tab1-fig2", "figure", allow_duplicate=True),
              Output("aroma_name", "children", allow_duplicate=True),
              Output("aroma_materials", "children", allow_duplicate=True),
              Output("aroma_score", "children", allow_duplicate=True),
              Output("aroma_recipe", "children", allow_duplicate=True),
              Output("notification", "children", allow_duplicate=True),
              Input('chatgpt-btn-5times', 'n_clicks'),
              State('chatgpt-input', 'value'),
              State("chatgpt-constraints", "value"),
              State("fig1_x_axis", "value"),
              State("fig1_y_axis", "value"),
              #State("fig2_x_axis", "value"),
              #State("fig2_y_axis", "value"),
              )
def update_chatgpt_txt(n_clicks, prompt, constraints, fig1_x, fig1_y):#, fig2_x, fig2_y):
    global data
    if n_clicks:
        #for i in range(5):
        #time.sleep(2)
        response = openai.ChatCompletion.create(
                        model = "gpt-4o",
                        messages = [
                            {"role": "system", "content": "あなたはもんじゃ焼き専門家です。"},
                            {"role": "system", "content": constraints},
                            {"role": "user", "content": prompt+"""
                            以下は条件です。3種類考え、全体を「リスト型」、それぞれを「辞書型」にして出力してください。また、料理名は個性的なものが望ましいです。材料は「辞書型」で出力、作り方は1から手順ごとにキーを振り、「辞書型」で出力してください。材料は小麦粉:20g、水:250g、ウスターソース:大さじ1.5、白だし:大さじ1の生地とキャベツ:180gを必須とし総重量は750g程度になるように調整してください。「独創性」「おいしさ」「食感」「プロンプトに対する一致度」「塩味」「甘味」「酸味」「苦味」「旨味」「辛味」は0～100数値が入るように点数をつけ、必ず「json形式」で出力してください。点数の小数点第1位は0以外も含まれることが望ましいです。
                            以下は各評価指標の評価基準です。評価基準に基づいて採点してください。
                            1.「独創性」：具材の組合せが新規性を持っているか
                             - 90～100: 他にはないユニークな具材やアイデアが取り入れられている。
                             - 70～89: 新規性があり魅力的だが完全に独自とは言えない。
                             - 50～69: 一般的な具材の組み合わせだが、少し工夫が感じられる。
                             - 30～49: 新規性が少なく、ありふれた具材の組み合わせ。
                             - 0～29: 極めて一般的で独創性が全く感じられない。
                            2.「おいしさ」：味の満足感があるか
                             - 90～100: 非常においしいと感じられ、バランスが完璧。
                             - 70～89: 十分においしく、バランスも良いが、改善の余地がある。
                             - 50～69: 可もなく不可もない味わい。
                             - 30～49: 味が単調またはバランスが悪い。
                             - 0～29: 味の満足感が非常に低い。
                            3.「食感」：食感が豊かであるか
                            - 90～100: 非常に多様な食感があり、バランスも良い。
                             - 70～89: 食感が豊かで、満足感が高い。
                             - 50～69: 食感に多少のバリエーションがあるが平凡。
                             - 30～49: 食感に乏しく、単調。
                             - 0～29: 食感がほとんどなく、満足感に欠ける。
                            4.「プロンプトに対する一致度」：条件以外のプロンプトの要求を満たしているか
                             - 90～100: プロンプト要求を完全に満たしており、期待以上の成果。
                             - 70～89: ほとんどの要求を満たしているが、細部に不足がある。
                             - 50～69: 基本的な要求は満たしているが、重要な要素が不足。
                             - 30～49: 多くの要求を満たしていないが、最低限の要素は含まれる。
                             - 0～29: プロンプトの要求をほとんど満たしていない。
                            5.「塩味」「甘味」「酸味」「苦味」「旨味」「辛味」：それぞれの強さ
                             - 90～100: 味が際立ちつつ、全体に調和している。
                             - 70～89: 味の特徴が十分に感じられる。
                             - 50～69: 味の特徴があるが、強さや調和が平凡。
                             - 30～49: 味の特徴が弱く、印象に残らない。
                             - 0～29: 味の特徴がほとんど感じられない。
                            以下の2点に違反すると罰則が課せられるので気を付けてください。
                            1、指定したフォーマットで出力すること。2、余計な文章を加えないこと。
                            """}
                        ],
                        temperature=1.0
                    )
        # response
        text = response['choices'][0]['message']['content']
        print(text)
        # print(text[0])
        # text_json = json.loads(text)
        # print(text_json)
        try:
            # 正規表現パターンを定義
            pattern = r"\[(.*?)\]"

            # パターンに一致する部分を検索
            matches = re.findall(pattern, text, re.DOTALL)

            # 一致した部分をリスト形式に戻す
            if matches:
                text = "[" + matches[0] + "]"
                print(text)
            else:
                print("リスト型の部分が見つかりませんでした。")

        except:
            print('error')
        try:
            text_jsons = json.loads(text)
            for i in range(len(text_jsons)):
                text_json = text_jsons[i]
                concat_data = pd.DataFrame([[str(datetime.datetime.now()).split('.')[0],
                                         text_json["料理名"], text_json["材料"],text_json["作り方"], prompt, text_json["独創性"],text_json["おいしさ"],text_json["食感"],text_json["プロンプトに対する一致度"],text_json["塩味"],text_json["甘味"],text_json["酸味"],text_json["苦味"],text_json["旨味"],text_json["辛味"]
                                        #  text_json["さわやかな"], text_json["やさしい"], text_json["ナチュラルな"],
                                        #  text_json["パワフルな"], text_json["デリケートな"], text_json["シンプルな"],
                                        #  text_json["若々しい"], text_json["個性的な"], text_json["エレガントな"],
                                        #  text_json["セクシーな"], text_json["シックな"], text_json["リフレッシュする"],
                                        #  text_json["リラックスする"], text_json["クリーンな"], text_json["ダーティな"],
                                        #  text_json["女性的な"], text_json["男性的な"], text_json["チープな"],
                                        #  text_json["リッチな"], text_json["ダイナミックな"], text_json["静かな"],
                                        #  text_json["プロンプトに対する一致度"]
                                         ]], 
                                         columns=["時刻", "料理名", "材料","作り方" , "プロンプト","独創性","おいしさ","食感", "プロンプトに対する一致度","塩味", "甘味", "酸味", "苦味", "旨味", "辛味"])
                                                #    "さわやかな", "やさしい", "ナチュラルな",
                                                #    "パワフルな", "デリケートな", "シンプルな",
                                                #    "若々しい", "個性的な", "エレガントな",
                                                #    "セクシーな", "シックな", "リフレッシュする",
                                                #    "リラックスする", "クリーンな", "ダーティな",
                                                #    "女性的な", "男性的な", "チープな",
                                                #    "リッチな", "ダイナミックな", "静かな","プロンプトに対する一致度"])
                data = pd.concat([concat_data, data])
                data = data.reset_index(drop=True)
                data.to_csv(file_path)
                aroma_name = text_json["料理名"]
                # 材料
                materials_p = []
                materials = text_json["材料"]
                for key, value in materials.items():
                    materials_p.append(f'{key} : {value}')
                    materials_p.append(html.Br())
                # 作り方
                recipe_p = []
                recipe = text_json["作り方"]
                try:
                    for key, value in recipe.items():
                        recipe_p.append(f'{key} : {value}')
                        recipe_p.append(html.Br())
                except:
                    recipe_p.append(recipe)
                aroma_score = text_json['プロンプトに対する一致度']
                note = dmc.Notification(
                        title="Success",
                        id="simple-notify",
                        action="show",
                        color="green",
                        message="Successfully obtained output.",
                        icon=DashIconify(icon="mdi:success-bold"),
                )
        except:
            print("error")
            aroma_name = data.loc[0, "料理名"]
            # 材料
            materials_p = []
            materials = data.loc[0, ['材料']].values[0]
            materials = materials.replace("'", "\"")
            materials_obj = json.loads(materials)
            for key, value in materials_obj.items():
                materials_p.append(f'{key} : {value}')
                materials_p.append(html.Br())
            # 作り方
            recipe_p = []
            recipe = data.loc[0, ['作り方']].values[0]
            recipe = recipe.replace("'", "\"")
            recipe_obj = json.loads(recipe)
            for key, value in recipe_obj.items():
                recipe_p.append(f'{key} : {value}')
                recipe_p.append(html.Br())
            aroma_score = data.loc[0, "プロンプトに対する一致度"]
            note = dmc.Notification(
                    title="Failed",
                    id="simple-notify",
                    action="show",
                    color="red",
                    message="We couldn't get the expected output",
                    icon=DashIconify(icon="material-symbols:error"),
            )


        fig = make_figure(dic[fig1_x], dic[fig1_y], False, 0)
        use_list=['独創性','おいしさ','食感','プロンプトに対する一致度','塩味', '甘味', '酸味', '苦味', '旨味', '辛味']
        #use_list=['さわやかな','やさしい','ナチュラルな','パワフルな','デリケートな','シンプルな','若々しい','個性的な','エレガントな','セクシーな','シックな','リフレッシュする','リラックスする','クリーンな','ダーティな','女性的な','男性的な','チープな','リッチな','ダイナミックな','静かな','プロンプトに対する一致度']
        fig2 = make_figure2(use_list)

        return fig, fig2, aroma_name, materials_p, recipe_p,aroma_score, [note]
        
    else:
        if len(data)==0: fig1, fig2 = initial_fig(), initial_fig()
        else:
            fig1 = make_figure(dic[fig1_x], dic[fig1_y], False, 0)
            use_list=['独創性','おいしさ','食感','プロンプトに対する一致度','塩味', '甘味', '酸味', '苦味', '旨味', '辛味']
            #use_list=['さわやかな','やさしい','ナチュラルな','パワフルな','デリケートな','シンプルな','若々しい','個性的な','エレガントな','セクシーな','シックな','リフレッシュする','リラックスする','クリーンな','ダーティな','女性的な','男性的な','チープな','リッチな','ダイナミックな','静かな','プロンプトに対する一致度']
            fig2 = make_figure2(use_list)
        return fig1, fig2, "", "", "","", []

# update history-table
@app.callback(Output("history-table", "children", allow_duplicate=True),
              Input('refresh-button', 'n_clicks'),
              Input('sort-col', 'value')
)
def refresh_table(n_click, v):
    ddd = pd.read_csv(file_path, index_col=0)
    if v=="timescale":
        idx = list(ddd.index)
        #print(idx)
    # elif v=="fresh":
    #     idx = data.sort_values("さわやかな", ascending=False).index.to_list()
    # elif v=="kind":
    #     idx = data.sort_values("やさしい", ascending=False).index.to_list()
    # elif v=="natural":
    #     idx = data.sort_values("ナチュラルな", ascending=False).index.to_list()
    # elif v=="powerful":
    #     idx = data.sort_values("パワフルな", ascending=False).index.to_list()
    # elif v=="delicate":
    #     idx = data.sort_values("デリケートな", ascending=False).index.to_list()
    # elif v=="simple":
    #     idx = data.sort_values("シンプルな", ascending=False).index.to_list()
    # elif v=="youthful":
    #     idx = data.sort_values("若々しい", ascending=False).index.to_list()
    # elif v=="unique":
    #     idx = data.sort_values("個性的な", ascending=False).index.to_list()
    # elif v=="elegant":
    #     idx = data.sort_values("エレガントな", ascending=False).index.to_list()
    # elif v=="sexy":
    #     idx = data.sort_values("セクシーな", ascending=False).index.to_list()
    # elif v=="chic":
    #     idx = data.sort_values("シックな", ascending=False).index.to_list()
    # elif v=="refresh":
    #     idx = data.sort_values("リフレッシュする", ascending=False).index.to_list()
    # elif v=="relax":
    #     idx = data.sort_values("リラックスする", ascending=False).index.to_list()
    # elif v=="clean":
    #     idx = data.sort_values("クリーンな", ascending=False).index.to_list()
    # elif v=="dirty":
    #     idx = data.sort_values("ダーティな", ascending=False).index.to_list()
    # elif v=="women":
    #     idx = data.sort_values("女性的な", ascending=False).index.to_list()
    # elif v=="men":
    #     idx = data.sort_values("男性的な", ascending=False).index.to_list()
    # elif v=="cheap":
    #     idx = data.sort_values("チープな", ascending=False).index.to_list()
    # elif v=="rich":
    #     idx = data.sort_values("リッチな", ascending=False).index.to_list()
    # elif v=="dynamic":
    #     idx = data.sort_values("ダイナミックな", ascending=False).index.to_list()
    # elif v=="silent":
    #     idx = data.sort_values("静かな", ascending=False).index.to_list()
    elif v=="originality":
        idx = data.sort_values("独創性", ascending=False).index.to_list()
    elif v=="deliciousness":
        idx = data.sort_values("おいしさ", ascending=False).index.to_list()
    elif v=="texture":
        idx = data.sort_values("食感", ascending=False).index.to_list()
    elif v=="score":
        idx = data.sort_values("プロンプトに対する一致度", ascending=False).index.to_list()
    elif v == "salty":
        idx = data.sort_values("塩味", ascending=False).index.to_list()
    elif v == "sweet":
        idx = data.sort_values("甘味", ascending=False).index.to_list()
    elif v == "sour":
        idx = data.sort_values("酸味", ascending=False).index.to_list()
    elif v == "bitter":
        idx = data.sort_values("苦味", ascending=False).index.to_list()
    elif v == "umami":
        idx = data.sort_values("旨味", ascending=False).index.to_list()
    elif v == "spicy":
        idx = data.sort_values("辛味", ascending=False).index.to_list()
    body = []
    for i in idx:
        el = [html.Td(ddd.loc[i, col]) for col in col_name]
        body.append(html.Tr(el))

    return header+[html.Tbody(body)]
