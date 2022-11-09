import streamlit as st
import pandas as pd
import base64
from sklearn.linear_model import LogisticRegression
from PIL import Image

st.title("競馬")
sample=pd.read_csv("Sample.csv")
sample=sample.to_csv(index=False)  
b64 = base64.b64encode(sample.encode('utf-8-sig')).decode()
href = f'<a href="data:application/octet-stream;base64,{b64}" download="sample.csv">download</a>'
st.sidebar.markdown("### 1. データ入力")
st.sidebar.markdown("下のdownloadをクリックしてSampleデータを入力してください")
st.sidebar.markdown(f"{href}", unsafe_allow_html=True)
st.sidebar.markdown("入力例")
image=Image.open("スクリーンショット (506).png")
st.sidebar.image(image,caption="サイレンススズカの天皇賞(秋)に出る際の確率を調べたいとき",use_column_width=True)

st.sidebar.markdown("")
st.sidebar.markdown("### 2. ファイルアップロード")
st.sidebar.markdown("1で作成したcsvファイルをドラッグ&ドロップしてください")
pred=st.sidebar.file_uploader("CSVファイルをドラッグ&ドロップ", type='csv', key='train')

if pred is not None:
  predict=pd.read_csv(pred)
  st.markdown("入力データの確認")
  st.dataframe(predict)

a=st.radio("データ選択", ("全レース", "レース賞別", "該当レース")) #第一引数：リスト名（選択肢群の上に表示）、第二引数：選択肢

horse_all=pd.read_csv("Horse_Race.csv")
horse_all=horse_all.fillna(0)
horse_all["rank*class"]=horse_all["P_rank"]*horse_all["P_class-Class"]
horse_all["pop*class"]=horse_all["P_popular"]*horse_all["P_class-Class"]

if a=="全レース":
  X=horse_all.drop(["Race","Race_Grade","Win","Quinella","Show"],axis=1)
  Y1=horse_all["Win"]
  Y2=horse_all["Quinella"]
  Y3=horse_all["Show"]
elif a=="該当レース":
  y=st.selectbox("レース選択(現在はエリザベス女王杯のみ)",("天皇賞(秋)","エリザベス女王杯"))
  if y=="エリザベス女王杯":
    b="Queen Elizabeth"
  this=horse_all[horse_all["Race"].str.contains(b)]
  X=this.drop(["Race","Race_Grade","Win","Quinella","Show"],axis=1)
  Y1=this["Win"]
  Y2=this["Quinella"]
  Y3=this["Show"]
  
elif a=="レース賞別":
  y=st.selectbox("レース賞選択",("G1","G2","G3"))
  y=int(y.replace("G",""))
  grade=horse_all[(horse_all["Race_Grade"]==y)]
  X=grade.drop(["Race","Race_Grade","Win","Quinella","Show"],axis=1)
  Y1=grade["Win"]
  Y2=grade["Quinella"]
  Y3=grade["Show"]

st.write("未実装です")

LR1=LogisticRegression()
LR2=LogisticRegression()
LR3=LogisticRegression()
LR1.fit(X,Y1)
LR2.fit(X,Y2)
LR3.fit(X,Y3)
#st.write(LR1,LR2,LR3)
