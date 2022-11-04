import streamlit as st
import numpy as np
from main import *

st.title('Statistiques')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

st.subheader('Nombre de destination par compagnie aérienne')
st.pyplot(exo3_carrier_nb_dest())

st.subheader('Nombre de destination par compagnie par aéroprt')
st.pyplot(exo3_carrier_nb_origin())


