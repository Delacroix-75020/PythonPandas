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
    def lowercase(x): return str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


st.subheader('Exercice 1')
st.write(exo1())

st.subheader('Exercice 2 : ')
st.text(busiest_departure_airport())
st.text("--------------------------")
st.text(most_frequent_destinations())
st.text("--------------------------")
# st.text(less_frequent_destinations())
st.text("--------------------------")
st.text(planes_taken_off_the_least())
st.text("--------------------------")
st.text(planes_taken_off_the_most())
st.text("--------------------------")


# Exercice 3

st.subheader('Nombre de destination par compagnie aérienne')
st.pyplot(exo3_carrier_nb_dest())

st.subheader('Nombre de destination par compagnie par aéroprt')
st.pyplot(exo3_carrier_nb_origin())

# Exercice4

st.subheader('Exercice 4')
st.text(landed_in_Houston())
st.text("--------------------------")
st.text(NYC_to_Seattle())
st.text("--------------------------")
st.text(carrier_NYC_to_Seattle())
st.text("--------------------------")
st.text(plane_NYC_to_Seattle())
st.text("--------------------------")

st.subheader('Exercice 5')
st.text(exo5())

st.subheader('Exercice 6')
st.text(exo6())

st.subheader('Exercice 7')
st.write(destinations_exclusive())

st.subheader('Exercice 8')
st.write(flights_UAD())
