import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

st.title('Streamlit 入門')
st.write('DataFrameを表示')

df_dict = {"A": [1,2,3], "B": [4,5,6]}
df = pd.DataFrame(df_dict)
st.dataframe(df.style.highlight_max(axis=0))
st.write("静的に表示")
st.table(df)
st.write("文字列やコードを表示")
"""
# 章
## 節
### 項

```python
import streamlit as st
```
"""
st.write("グラフを表示")
df = pd.DataFrame(
    np.random.rand(20,3),
    columns = ['A','B','C']
    )
st.line_chart(df)

df = pd.DataFrame(
        np.random.rand(100, 2)/[50, 50] + [35.69, 139.70],
        columns = ['lat', 'lon']
        )
# st.dataframe(df)
# st.map(df)

st.write('画像を表示')
if st.checkbox('show image'):
    img = Image.open('/Users/takurokamahori/Pictures/wallpaperbetter.jpg')
    st.image(img, caption='wallpaper',use_column_width=True)

st.sidebar.text_input("あなたの名前は？")
selected_number = st.sidebar.selectbox('好きな数字を選んでください',list(range(0,10)))
st.text('sidebarから好きな数字を選んでください')
f'あなたの好きな数字は{selected_number}です'

st.slider('あなたの今の調子は?', 0, 100, 50)


left_column, right_column = st.columns(2)
left_column.text_input("test")
right_column.button("test",help="testのボタンです")

expander = st.expander("折りたたみ")
expander.text_input("文字を入力",help="折りたたみのテストです")
expander.button("ボタン")


latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    latest_iteration.text(f'iteration {i+1}')
    bar.progress(i+1)
    time.sleep(0.05)

'Done'
