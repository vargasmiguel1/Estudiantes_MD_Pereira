import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
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


def titulo(num, tit):
  st.markdown(f'<h{num} style="text-align: center;">{tit}</h{num}>',
              unsafe_allow_html=True)


titulo(1, "Explorador de Datos")

titulo(3, "I.E María Dolorosa - Pereira")

st.markdown(
    "Created by: [Angela María Rodas Panesso](https://www.linkedin.com/in/angela-mar%C3%ADa-rodas-86795611b/) & [MAVV Smart Optimization Consulting](https://mavvsmart.com/)"
)

st.write(
    "Este recurso se basa en los datos Abiertos reportados por la Scretaría de Educación de Pereira. Más información en el siguiente botón."
)

st.link_button(
    "ℹ️  Info Datos Abiertos",
    "https://www.datos.gov.co/Educaci-n/Estudiantes-matriculados-en-las-instituciones-educ/gi8c-bbik/about_data",
    type="primary",
    disabled=False,
    use_container_width=False)

st.divider()

init_streamlit_comm()


@st.cache_resource
def get_pyg_renderer() -> "StreamlitRenderer":
  ##DATOS
  client = Socrata("www.datos.gov.co", None)

  results = client.get("gi8c-bbik",
                     where="INSTITUCION = 'I.E MARIA DOLOROSA'",
                     limit=2000)

  df = pd.DataFrame.from_records(results)
###
  return StreamlitRenderer(df, spec="./gw_config.json", debug=False)


renderer = get_pyg_renderer()

renderer.render_explore()

