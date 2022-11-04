import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Adrien DELACROIX
# Claudia TIMOCI

AIRLINES = pd.read_csv("airlines.csv")  # 16
AIRPORTS = pd.read_csv("airports.csv")  # 1458
FLIGHTS = pd.read_csv("flights.csv")  # 252704
PLANES = pd.read_csv("planes.csv")  # 3322
WEATHER = pd.read_csv("weather.csv")  # 26130
WEATHER_WITH_3_DOUBLONS = pd.read_csv("weather_with_3_doublons.csv")  # 26115

AIRLINES_JSON = {}
for index in AIRLINES.index:
    AIRLINES_JSON[AIRLINES.carrier[index]] = AIRLINES.name[index]


# Combien y-a-t-il d’aéroports aux Etats-Unis
# où on ne passe pas à l’heure d’été (indice : colonne dst : 23) ?
# de fuseaux horaires (10 voir colone tzone dont une  « /N ») 

def exo1():
    print(len(FLIGHTS.origin.drop_duplicates()))  # 3
    print(FLIGHTS.origin.value_counts())
    print(len(FLIGHTS.dest.drop_duplicates()), "\n")  # 103


def exo3_carrier_nb_dest() -> None:
    res1 = {}
    for carrier, value in FLIGHTS.groupby(["carrier"]):
        res1[AIRLINES_JSON[carrier]] = {
            "dest": len(value.groupby("dest").size())}
    df = pd.DataFrame.from_dict(res1)
    df = df.fillna(0)
    df.plot(kind="bar",
            figsize=(8, 8),
            title="nombre de destination par compagnie aérienne")
    res = {}
    for carrier1, value1 in FLIGHTS.groupby(["carrier"]):
        res[AIRLINES_JSON[carrier1]] = {}
        for origin, value2 in value1.groupby(["origin"]):
            res[AIRLINES_JSON[carrier1]][origin] = len(
                value2.groupby("dest").size())
    df2 = pd.DataFrame.from_dict(res)
    df2 = df2.fillna(0)
    df2.plot(kind="bar",
             figsize=(8, 8),
             title="nombre de destination par compagnie par aéroprt d'origine")
    plt.show()


# exo3_carrier_nb_dest()
