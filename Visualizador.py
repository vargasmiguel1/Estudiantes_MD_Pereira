import pandas as pd
import plotly.express as px
import streamlit as st
from sodapy import Socrata

st.set_page_config(layout="wide", page_title="Maria Dolorosa")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

##DATOS
client = Socrata("www.datos.gov.co", None)

results = client.get("gi8c-bbik",
                     where="INSTITUCION = 'I.E MARIA DOLOROSA'",
                     limit=2000)

df = pd.DataFrame.from_records(results)

cols = df.columns.tolist()
###


def titulo(num, tit):
  st.markdown(f'<h{num} style="text-align: center;">{tit}</h{num}>',
              unsafe_allow_html=True)

def encab(tit):
  st.markdown(f'<p style="text-align: center;"><strong>{tit}</strong></p>', unsafe_allow_html = True)


titulo(1, "Visualizador de Datos")

titulo(3, "I.E María Dolorosa - Pereira")

st.markdown(
    "Created by: [Angela Rodas](https://www.linkedin.com/in/angela-mar%C3%ADa-rodas-86795611b/) & [MAVV](https://mavvsmart.com/)"
)

st.write(f"Hay un total de **{len(df)} estudiantes reportados**")

pregx=None
pregy=None
pregc=None
pregs=None

st.divider()
ex=st.columns(4)
###
###EJE X
###
with ex[0]:
    encab("Eje X")
    pregx=st.selectbox("Variable", options=cols, index=None, key="pregx")

###
###EJE Y
###
with ex[1]:
    encab("Eje Y")
    pregy=st.selectbox("Variable", options=cols, index=None, key="pregy")



###
### CLASIFICAR
###
with ex[2]:
    encab("Clasificar")
    pregc=st.selectbox("Variable", options=cols, index=None, key="pregc")     

###
### SOMBREAR
###
with ex[3]:
    encab("Sombrear")
    pregs=st.selectbox("Variable", options=cols, index=None, key="pregs")



st.divider()
fun={"Contar": "count", "Sumar":"sum", "Promedio":"avg", "Minímo":"min", "Máximo":"max"}
autot={"Ninguno":False,"Enteros":'.0f',"Una cifra decimal":'.1f', "Dos cifras decimales":".2f"}

encab("Parámetros")
p=st.columns(3)
funcion=p[0].selectbox("Función de agregación", ["Contar", "Sumar", "Promedio", "Minímo", "Máximo"], index=0, key="func")
bins=p[1].number_input("Bins", value=None, step=1, key="bins")
autotexto=p[2].selectbox("Tipo de texto", ["Ninguno","Enteros","Una cifra decimal", "Dos cifras decimales"], index=0, key="autotexto")

encab("GRÁFICO")
if pregx is not None:
    fig = px.histogram(df, x=pregx, y=pregy, color=pregc, pattern_shape=pregs, histfunc=fun[funcion], nbins=bins, text_auto=autot[autotexto])
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
