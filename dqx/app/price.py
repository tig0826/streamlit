import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time
from common.load_psql import load_psql



# def get_price_data(selected_item_tables):

# アイテムのメタデータを取得
sql_item_name = """SELECT * FROM metadata.item_name"""
df_item_name = load_psql(sql_item_name)
# アイテムの種類一覧を取得
df_item_type = df_item_name['種類'].unique()
# アイテムの種類を選択するボックス
selected_item_type = st.sidebar.multiselect('種類を選択', df_item_type)
# アイテムのカテゴリ一覧を取得。アイテムの種類を選択した場合は対応するカテゴリに絞る。
if len(selected_item_type) > 0:
    df_item_category = df_item_name[df_item_name['種類'].isin(selected_item_type)]['カテゴリ'].unique()
else:
    df_item_category = df_item_name['カテゴリ'].unique()
# アイテムのカテゴリを選択するボックス
selected_item_category = st.sidebar.multiselect('カテゴリを選択', df_item_category)
# アイテムの種類、カテゴリが選択された場合は
# アイテムのサブカテゴリ一覧を取得。アイテムの種類やカテゴリを選択した場合は対応するカテゴリに絞る。
if len(selected_item_category) > 0:
    df_item_subcategory = df_item_name[df_item_name['カテゴリ'].isin(selected_item_category)]['サブカテゴリ'].dropna().unique()
elif len(selected_item_type) > 0:
    df_item_subcategory = df_item_name[df_item_name['種類'].isin(selected_item_type)]['サブカテゴリ'].dropna().unique()
else:
    df_item_subcategory = df_item_name['サブカテゴリ'].dropna().unique()
# アイテムのサブカテゴリを選択するボックス
selected_item_subcategory = st.sidebar.multiselect('サブカテゴリを選択', df_item_subcategory)
if len(selected_item_type) > 0 or len(selected_item_category) > 0 or len(selected_item_subcategory) > 0:
    selected_item_type = df_item_type.tolist() if len(selected_item_type) == 0 else selected_item_type
    selected_item_category = df_item_category.tolist() if len(selected_item_category) == 0 else selected_item_category
    selected_item_subcategory = df_item_subcategory.tolist() if len(selected_item_subcategory) == 0 else selected_item_subcategory
    # df_item_tables = df_item_name[(df_item_name['カテゴリ'].isin(selected_item_category)
    #                                & df_item_name['種類'].isin(selected_item_type))]['アイテム名'].unique()
     # & df_item_name['サブカテゴリ'].isin(selected_item_subcategory)
    # フィルタリングの条件を動的に構築
    condition = (df_item_name['カテゴリ'].isin(selected_item_category)
                 & df_item_name['種類'].isin(selected_item_type))

    # '種類'が'武器'や'防具'でない場合のみ、サブカテゴリの条件を追加
    if selected_item_type in ['武器', '防具']:
        condition &= df_item_name['サブカテゴリ'].isin(selected_item_subcategory)

    # 条件に基づいてフィルタリングし、ユニークなアイテム名を取得
    df_item_tables = df_item_name[condition]['アイテム名'].unique()
else:
    df_item_tables = df_item_name['アイテム名'].unique()
item_name = st.sidebar.selectbox(label='アイテム名を選択', options=df_item_tables)
st.title(f'{item_name}')
sql_price = f"""SELECT * from price.{item_name}"""
df =  load_psql(sql_price)
# 取得した日付と時刻を合わせたカラムを作成
df['日時'] = df['取得日'] + ' ' + df['取得時刻']
# 単品の場合1つあたりの価格がNaNなので価格を埋める
df['1つあたりの価格'] = df['1つあたりの価格'].fillna(df['価格']).astype('int')
df_percentile = df.groupby('日時')['1つあたりの価格'].quantile([0.10,0.25,0.50]).unstack()
st.write("出品価格パーセンタイル")
st.line_chart(df_percentile)

st.write("出品数")
df_sum = df.groupby('日時')['個数'].sum()
st.line_chart(df_sum)


