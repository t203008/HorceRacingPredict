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
st.sidebar.markdown("2023年宝塚記念　データ")
sample2=pd.read_csv("Takaraduka Kinen 2023.csv")
sample2=sample2.to_csv(index=False) 
b64 = base64.b64encode(sample2.encode('utf-8-sig')).decode()
href = f'<a href="data:application/octet-stream;base64,{b64}" download="Takaraduka Kinen 2023.csv">Takaraduka Kinen 2023</a>'
st.sidebar.markdown(f"{href}", unsafe_allow_html=True)

horse_all=pd.read_csv("Horse_Race.csv")
horse_all=horse_all.fillna(0)
horse_all["rank_and_class"]=horse_all["P_rank"]*horse_all["P_class_Class"]
horse_all["pop_and_class"]=horse_all["P_popular"]*horse_all["P_class_Class"]
horse_all["pop_and_rank"]=horse_all["P_rank"]+horse_all["P_popular"]
#horse_all["pop_rank_class"]=horse_all["P_popular"]*horse_all["P_class_Class"]*horse_all["P_rank"]


st.write("どのデータから結果を予測しますか")
course=st.radio(label="どの馬場から選びますか",options=("芝","ダート"),index=0,horizontal=True,)
if course=="ダート":
  horse_all=horse_all[(horse_all["Dirt"]==1)]
elif course=="芝":
  horse_all=horse_all[(horse_all["Dirt"]==0)]
year=st.radio(label="年齢限定レースに絞りますか",options=("2歳馬限定","3歳馬限定","全年齢","絞り込まない"),index=0,horizontal=True,)
if year=="2歳馬限定":
  horse_all=horse_all[(horse_all["Restrict"]==2)]
elif year=="3歳馬限定":
  horse_all=horse_all[(horse_all["Restrict"]==3)]
elif year=="全年齢":
  horse_all=horse_all[(horse_all["Restrict"]==0)]

waku=st.radio(label="枠順を予想に入れますか",options=("入れる","入れない"),index=0,horizontal=True)
  
a=st.radio("データ選択", ("全レース", "レース賞別", "該当レース")) 


if a=="全レース":
  Y1=horse_all["Win"]
  Y2=horse_all["Quinella"]
  Y3=horse_all["Show"]
  Z=pd.get_dummies(horse_all,columns=['Frame'])
  X=Z.drop(["Race","Restrict","Mare Limited","Race_Grade","Dirt","Distance","Course","Win","Quinella","Show"],axis=1)
elif a=="該当レース":
  y=st.selectbox("レース選択",("フェブラリーステークス","高松宮記念","大阪杯","桜花賞","皐月賞","天皇賞（春）","NHKマイルカップ","ヴィクトリアマイル","優駿牝馬（オークス）","東京優駿（日本ダービー）","安田記念","宝塚記念","スプリンターズステークス","秋華賞","天皇賞（秋）","エリザベス女王杯","マイルチャンピオンシップ","ジャパンカップ","チャンピオンズカップ","阪神ジュベナイルフィリーズ","朝日杯フューチュリティステークス","有馬記念"))
  if y=="エリザベス女王杯":
    b="Queen Elizabeth II Cup"
  elif y=="マイルチャンピオンシップ":
    b="Mile Championship"
  elif y=="ジャパンカップ":
    b="Japan Cup"
  elif y=="チャンピオンズカップ":
    b="Champions Cup"
  elif y=="阪神ジュベナイルフィリーズ":
    b="Hanshin Juvenile Fillies"
  elif y=="朝日杯フューチュリティステークス":
    b="Asahi Hai Futurity Stakes"
  elif y=="有馬記念":
    b="Arima Kinen"
  elif y=="フェブラリーステークス":
    b="F"
  elif y=="高松宮記念":
    b="Takamatsunomiya"
  elif y=="大阪杯":
    b="Osaka Hai"
  elif y=="桜花賞":
    b="Oka Sho"
  elif y=="皐月賞":
    b="Satsuki Sho"
  elif y=="天皇賞（春）":
    b="Tenno Sho Spring"
  elif y=="NHKマイルカップ":
    b="NHK Mile Cup"
  elif y=="ヴィクトリアマイル":
    b="Victoria Mile"
  elif y=="優駿牝馬（オークス）":
    b="Yushun Himba"
  elif y=="東京優駿（日本ダービー）":
    b="Tokyo　Yushun"
  elif y=="安田記念":
    b="Yasuda Kinen"
  elif y=="宝塚記念":
    b="Takaraduka Kinen"
  elif y=="スプリンターズステークス":
    b="Sprinters Stakes"
  elif y=="秋華賞":
    b="Shuka Sho"
  elif y=="天皇賞（秋）":
    b="Tenno Sho (Autumn)"
  this=horse_all[horse_all["Race"].str.contains(b)]
  Y1=this["Win"]
  Y2=this["Quinella"]
  Y3=this["Show"]
  Z=pd.get_dummies(this,columns=['Frame'])
  X=Z.drop(["Race","Restrict","Mare Limited","Race_Grade","Dirt","Distance","Course","Win","Quinella","Show"],axis=1)
elif a=="レース賞別":
  y=st.selectbox("レース賞選択",("G1","G2","G3"))
  y=int(y.replace("G",""))
  grade=horse_all[(horse_all["Race_Grade"]==y)]
  Y1=grade["Win"]
  Y2=grade["Quinella"]
  Y3=grade["Show"]
  Z=pd.get_dummies(grade,columns=['Frame'])
  X=Z.drop(["Race","Restrict","Mare Limited","Race_Grade","Dirt","Distance","Course","Win","Quinella","Show"],axis=1)
st.write("次に画面左上からサイドバーを開いてください")
#st.write("未実装です")
#st.write(Z)

st.sidebar.markdown("")
st.sidebar.markdown("### 2. ファイルアップロード")
st.sidebar.markdown("1で作成したcsvファイルをドラッグ&ドロップしてください")
pred=st.sidebar.file_uploader("CSVファイルをドラッグ&ドロップ", type='csv', key='train')

sub=list(horse_all.columns.values)
dellist=["Race_Grade","Mare Limited","Restrict","Dirt","Distance","Course","Win","Quinella","Show","rank_and_class","pop_and_class"]
for i in dellist:
  sub.remove(i)
sub.insert(0,"No.")
sub.insert(1,"Horse")

if pred is not None:
  pred1=pred
  predic=pd.read_csv(pred,names=sub)
  predic=predic.drop(index=predic.index[[0]])
  predic=predic.fillna(0)
  #st.dataframe(predic)
  for i in sub:
    if i not in ["Horse","Race","Frame"]:
      predic[i]=predic[i].astype(float,errors="raise")
  predic=pd.get_dummies(predic,columns=['Frame'])
  #st.dataframe(predic)
  #st.dataframe(Z)
  predic["rank_and_class"]=predic["P_rank"]*predic["P_class_Class"]
  predic["pop_and_class"]=predic["P_popular"]*predic["P_class_Class"]
  #predic["pop_rank_class"]=predic["P_popular"]*predic["P_class_Class"]*predic["P_rank"]
  
  #st.dataframe(predic)
  #st.dataframe(Z)
  st.header("予測される確率")
 
  if waku=="入れる":
    
    logistic1 = smf.glm(formula = "Win ~ 1+Age+Frame_one+Frame_two+Frame_three+Frame_four+Frame_five+Frame_six+Frame_seven+Frame_eight+Mare+Stallion+P_rank+P_popular+Jockey_change+Change_from_P_Grass+Change_from_P_Dirt+Change_from_P_Hurdle+P_class_Class+Weight_P_Weight+Distance_P_distance+Week_distance+P_overseas+P_rank*P_popular*P_class_Class",
                   data = Z ,
                   family = sm.families.Binomial()).fit()
    logistic2 = smf.glm(formula = "Quinella ~ 1+Age+Frame_one+Frame_two+Frame_three+Frame_four+Frame_five+Frame_six+Frame_seven+Frame_eight+Mare+Stallion+P_rank+P_popular+Jockey_change+Change_from_P_Grass+Change_from_P_Dirt+Change_from_P_Hurdle+P_class_Class+Weight_P_Weight+Distance_P_distance+Week_distance+P_overseas+P_rank*P_popular*P_class_Class",
                   data = Z ,
                   family = sm.families.Binomial()).fit()
    logistic3 = smf.glm(formula = "Show ~ 1+Age+Frame_one+Frame_two+Frame_three+Frame_four+Frame_five+Frame_six+Frame_seven+Frame_eight+Mare+Stallion+P_rank+P_popular+Jockey_change+Change_from_P_Grass+Change_from_P_Dirt+Change_from_P_Hurdle+P_class_Class+Weight_P_Weight+Distance_P_distance+Week_distance+P_overseas+P_rank*P_popular*P_class_Class",
                   data = Z ,
                   family = sm.families.Binomial()).fit()
  elif waku=="入れない":

    st.write(Z)
    
    logistic1 = smf.glm(formula = "Win ~ 1+Age+Mare+Stallion+P_rank+P_popular*P_popular+Jockey_change+Change_from_P_Grass+Change_from_P_Dirt+Change_from_P_Hurdle+P_class_Class+Weight_P_Weight+Distance_P_distance+Week_distance+P_overseas",
                   data = Z ,
                   family = sm.families.Binomial()).fit()
    logistic2 = smf.glm(formula = "Quinella ~ 1+Age+Mare+Stallion+P_rank+P_popular*P_popular+P_popular+Jockey_change+Change_from_P_Grass+Change_from_P_Dirt+Change_from_P_Hurdle+P_class_Class+Weight_P_Weight+Distance_P_distance+Week_distance+P_overseas",
                   data = Z ,
                   family = sm.families.Binomial()).fit()
    logistic3 = smf.glm(formula = "Show ~ 1+Age+Mare+Stallion+P_rank+P_popular*P_popular+P_popular+Jockey_change+Change_from_P_Grass+Change_from_P_Dirt+Change_from_P_Hurdle+P_class_Class+Weight_P_Weight+Distance_P_distance+Week_distance+P_overseas",
                   data=Z,
                   family = sm.families.Binomial()).fit() 
  predic1=logistic1.predict(predic)
  predic2=logistic2.predict(predic)
  predic3=logistic3.predict(predic)

  st.write(predic3)
  pre=pd.concat([predic["Horse"],predic1,predic2,predic3],axis=1)
  pred=pre.rename(columns={"Horse":"馬名",0:"単勝率",1:"連対率",2:"複勝率"})
  L=["単勝率","連対率","複勝率"]
  K=1
  changedata=st.radio("調整しますか",("する","しない"))
  if changedata=="する":
    for i in L:
      pred[i]=pred[i]/pred[i].sum()*int(K)
      K+=1
    st.write(pred)
  else:
    st.write(pred)

  pred1=pred.drop(["馬名"],axis=1)
  
  win_list=pred["単勝率"].to_list()
  quinella_list=pred["連対率"].to_list()
  show_list=pred["複勝率"].to_list()
  names=pred["馬名"].to_list()
  predict_list=[win_list,quinella_list,show_list]
  graph1=pd.DataFrame(data=predict_list,index=["1.単勝率","2.連対率","3.複勝率"],columns=names)
  st.line_chart(graph1)

  st.write("注意点")
  st.markdown("1.前走のデータからの予測ゆえ、前走不利があった馬などは確率が下がっています")
  st.markdown("2.前走海外馬のデータが少なく、確率はかなり低くでると考えられます")
  st.markdown("3.3歳馬限定レースがあるため、3歳が評価されやすくなっています")
  st.markdown("4.該当レースから求めた確率はサンプル数が少なく、信ぴょう性に欠けます")
