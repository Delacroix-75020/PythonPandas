import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Adrien DELACROIX
# Claudia TIMOCI

AIRLINES=pd.read_csv("airlines.csv") # 16
AIRPORTS=pd.read_csv("airports.csv") # 1458
FLIGHTS=pd.read_csv("flights.csv") # 252704
PLANES=pd.read_csv("planes.csv") # 3322
WEATHER=pd.read_csv("weather.csv") # 26130
WEATHER_WITH_3_DOUBLONS=pd.read_csv("weather_with_3_doublons.csv") # 26115

def exo1():
    print(len(FLIGHTS.origin.drop_duplicates())) # 3
    print(FLIGHTS.origin.value_counts())
    print(len(FLIGHTS.dest.drop_duplicates()),"\n") # 103


def exo3_carrier_nb_dest(): 
    for x,y in FLIGHTS.groupby(["carrier"]):
        print("carrier:",x)
        print(len(y.groupby("dest").size()),"\n")

def exo3_carrier_nb_dest_origin():
    res={}
    for carrier,value1 in FLIGHTS.groupby(["carrier"]):
            res[carrier]={}
            for origin,value2 in value1.groupby(["origin"]):
                res[carrier][origin]=len(value2.groupby("dest").size())
    return res  

df = pd.DataFrame.from_dict(exo3_carrier_nb_dest_origin())
df=df.fillna(0)
df.plot(kind="bar")
plt.show()