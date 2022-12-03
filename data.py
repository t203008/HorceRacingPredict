import streamlit as st
import numpy as np 
import pandas as pd
import base64
import statsmodels.formula.api as smf
import statsmodels.api as sm
from PIL import Image
import matplotlib.pyplot as plt
import japanize_matplotlib

st.title("競馬")
st.write("前走から今回のレースの勝率などを計算します")

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
st.sidebar.markdown("2022年チャンピオンズカップ　データ")
sample2=pd.read_csv("Champions Cup 2022.csv")
sample2=sample2.to_csv(index=False)  
b64 = base64.b64encode(sample2.encode('utf-8-sig')).decode()
href = f'<a href="data:application/octet-stream;base64,{b64}" download="Champions Cup 2022.csv">Chanmpions Cup 2022</a>'
st.sidebar.markdown(f"{href}", unsafe_allow_html=True)

st.write("どのデータから結果を予測しますか")
a=st.radio("データ選択", ("全レース", "芝ダート別","レース賞別", "該当レース")) 

horse_all=pd.read_csv("Horse_Race.csv")
horse_all=horse_all.fillna(0)
horse_all["rank_and_class"]=horse_all["P_rank"]*horse_all["P_class_Class"]
horse_all["pop_and_class"]=horse_all["P_popular"]*horse_all["P_class_Class"]

if a=="全レース":
  X=horse_all.drop(["Race","Race_Grade","Win","Quinella","Show"],axis=1)
  Y1=horse_all["Win"]
  Y2=horse_all["Quinella"]
  Y3=horse_all["Show"]
  Z=horse_all
elif a=="該当レース":
  y=st.selectbox("レース選択",("エリザベス女王杯","マイルチャンピオンシップ","ジャパンカップ","チャンピオンズカップ"))
  if y=="エリザベス女王杯":
    b="Queen Elizabeth II Cup"
  if y=="マイルチャンピオンシップ":
    b="Mile Championship"
  if y=="ジャパンカップ":
    b="Japan Cup"
  if y=="チャンピオンズカップ":
    b=="Champions Cup"
  this=horse_all[horse_all["Race"].str.contains(b)]
  X=this.drop(["Race","Race_Grade","Dirt","Distance","Win","Quinella","Show"],axis=1)
  Y1=this["Win"]
  Y2=this["Quinella"]
  Y3=this["Show"]
  Z=this
elif a=="芝ダート別":
  y=st.select.box("選択",("芝","ダート"))
  if y=="ダート":
    course=horse_all[(horse_all["Dirt"]==1)]
  X=course.drop(["Race","Race_Grade","Dirt","Distance","Win","Quinella","Show"],axis=1)
  Y1=course["Win"]
  Y2=course["Quinella"]
  Y3=course["Show"]
  Z=course
elif a=="レース賞別":
  y=st.selectbox("レース賞選択",("G1","G2","G3"))
  y=int(y.replace("G",""))
  grade=horse_all[(horse_all["Race_Grade"]==y)]
  X=grade.drop(["Race","Race_Grade","Dirt","Distance","Win","Quinella","Show"],axis=1)
  Y1=grade["Win"]
  Y2=grade["Quinella"]
  Y3=grade["Show"]
  Z=grade
st.write("次に画面左上からサイドバーを開いてください")
#st.write("未実装です")
#st.write(Z)

st.sidebar.markdown("")
st.sidebar.markdown("### 2. ファイルアップロード")
st.sidebar.markdown("1で作成したcsvファイルをドラッグ&ドロップしてください")
pred=st.sidebar.file_uploader("CSVファイルをドラッグ&ドロップ", type='csv', key='train')

sub=list(horse_all.columns.values)
dellist=["Race_Grade","Win","Quinella","Show","rank_and_class","pop_and_class"]
for i in dellist:
  sub.remove(i)
sub.insert(0,"Horse")

if pred is not None:
  pred1=pred
  predic=pd.read_csv(pred,names=sub)
  predic=predic.drop(index=predic.index[[0]])
  predic=predic.fillna(0)
  #st.dataframe(predic)
  for i in sub:
    if i not in ["Horse","Race"]:
      predic[i]=predic[i].astype(float,errors="raise")
  predic["rank_and_class"]=predic["P_rank"]*predic["P_class_Class"]
  predic["pop_and_class"]=predic["P_popular"]*predic["P_class_Class"]
  #st.dataframe(predic) 
  st.header("予測される確率") 
  logistic1 = smf.glm(formula = "Win ~ 1+Age+Mare+Stallion+P_rank+P_popular+Jockey_change+Change_from_P_Grass+Change_from_P_Dirt+Change_from_P_Hurdle+P_class_Class+Weight_P_Weight+Distance_P_distance+Week_distance+P_overseas+P_rank*P_popular*P_class_Class",
                   data = Z ,
                   family = sm.families.Binomial()).fit()
  logistic2 = smf.glm(formula = "Quinella ~ 1+Age+Mare+Stallion+P_rank+P_popular+Jockey_change+Change_from_P_Grass+Change_from_P_Dirt+Change_from_P_Hurdle+P_class_Class+Weight_P_Weight+Distance_P_distance+Week_distance+P_overseas+P_rank*P_popular*P_class_Class",
                   data = Z ,
                   family = sm.families.Binomial()).fit()
  logistic3 = smf.glm(formula = "Show ~ 1+Age+Mare+Stallion+P_rank+P_popular+Jockey_change+Change_from_P_Grass+Change_from_P_Dirt+Change_from_P_Hurdle+P_class_Class+Weight_P_Weight+Distance_P_distance+Week_distance+P_overseas+P_rank*P_popular*P_class_Class",
                   data = Z ,
                   family = sm.families.Binomial()).fit()
  
  predic1=logistic1.predict(predic)
  predic2=logistic2.predict(predic)
  predic3=logistic3.predict(predic)
  pre=pd.concat([predic["Horse"],predic1,predic2,predic3],axis=1)
  pred=pre.rename(columns={"Horse":"馬名",0:"単勝率",1:"連対率",2:"複勝率"})
  L=["単勝率","連対率","複勝率"]
  K=1
  for i in L:
    pred[i]=pred[i]/pred[i].sum()*int(K)
    K+=1
  st.write(pred)
  
  st.write("注意点")
  st.markdown("1.前走のデータからの予測ゆえ、前走不利があった馬などは確率が下がっています")
  st.markdown("2.前走海外馬のデータが少なく、確率はかなり低くでると考えられます")
  st.markdown("3.3歳馬限定レースがあるため、3歳が評価されやすくなっています")
  st.markdown("4.該当レースから求めた確率はサンプル数が少なく、信ぴょう性に欠けます")

  pred1=pred.drop(["馬名"],axis=1)
  pred=pred.T
  
  win_list=pred["単勝率"].to_list()
  quinella_list=pred["連対率"].to_list()
  show_list=pred["複勝率"].to_list()
  names=pred["馬名"].to_list()
  predicrt_list=[win_list,quinella_list,show_list]
  graph1=pd.DataFrame(data=predict_list,index=["単勝率","連対率","複勝率"],cplumns=names)
  
  st.write(graph1)
