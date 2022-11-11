import streamlit as st
import pandas as pd
import base64
import statsmodels.formula.api as smf
import statsmodels.api as sm
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
  Z=horse_all
elif a=="該当レース":
  y=st.selectbox("レース選択(現在はエリザベス女王杯のみ)",("天皇賞(秋)","エリザベス女王杯"))
  if y=="エリザベス女王杯":
    b="Queen Elizabeth"
  this=horse_all[horse_all["Race"].str.contains(b)]
  X=this.drop(["Race","Race_Grade","Win","Quinella","Show"],axis=1)
  Y1=this["Win"]
  Y2=this["Quinella"]
  Y3=this["Show"]
  Z=this
elif a=="レース賞別":
  y=st.selectbox("レース賞選択",("G1","G2","G3"))
  y=int(y.replace("G",""))
  grade=horse_all[(horse_all["Race_Grade"]==y)]
  X=grade.drop(["Race","Race_Grade","Win","Quinella","Show"],axis=1)
  Y1=grade["Win"]
  Y2=grade["Quinella"]
  Y3=grade["Show"]
  Z=grade
st.write("未実装です")

st.sidebar.markdown("")
st.sidebar.markdown("### 2. ファイルアップロード")
st.sidebar.markdown("1で作成したcsvファイルをドラッグ&ドロップしてください")
pred=st.sidebar.file_uploader("CSVファイルをドラッグ&ドロップ", type='csv', key='train')

sub=list(horse_all.columns.values)
dellist=["Race_Grade","Win","Quinella","Show","rank*class","pop*class"]
for i in dellist:
  sub.remove(i)
sub.insert(0,"Horse")

if pred is not None:
  pred1=pred
  predict=pd.read_csv(pred,names=sub)
  predict=predict.fillna(0)
  predict=predict.drop(index=predict.index[[0]])
  st.dataframe(predict)
  for i in sub:
    st.write(predict[i].dtype())
    predict[i]=predict[i].astype(float,errors="raise")
  predict["rank*class"]=predict["P_rank"]*predict["P_class-Class"]
  predict["pop*class"]=predict["P_popular"]*predict["P_class-Class"]
  st.markdown("入力データの確認")

  
  logistic1 = smf.glm(formula = "Y1 ~ X",
                   data = Z ,
                   family = sm.families.Binomial()).fit()
  
#  st.write(LR1.predict(predict))
