import pandas as pd
import matplotlib.pyplot as plt
import warnings
from pprint import pprint
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
AIRPORTS_JSON = {}
for index in AIRPORTS.index:
    AIRPORTS_JSON[AIRPORTS.faa[index]] = AIRPORTS.name[index]

# Combien y-a-t-il d’aéroports aux Etats-Unis
# où on ne passe pas à l’heure d’été (indice : colonne dst : 23) ?
# de fuseaux horaires (10 voir colone tzone dont une  « /N »)


def exo1():
    print("nb unique starting airport:", len(
        FLIGHTS.origin.drop_duplicates()))  # 3
    print("nb starts:", FLIGHTS.origin.value_counts())
    print("nb unique ending airports:", len(
        FLIGHTS.dest.drop_duplicates()), "\n")  # 103
    count = 0
    res = []
    for index in AIRPORTS.index:
        if ((str(AIRPORTS.tzone[index]).startswith("America"))
                and (AIRPORTS.dst[index] == "N")):
            res.append(AIRPORTS.tzone[index])
            count += 1
        elif ((str(AIRPORTS.tzone[index]).startswith("America"))
              and (AIRPORTS.dst[index] == "U")):
            if AIRPORTS.tzone[index] in res:
                count += 1
    print("number of airports in US where there's no DST:", count)
    df = AIRPORTS.tzone.drop(AIRPORTS.tzone[AIRPORTS.tzone == "\\N"].index)
    print("number of unique timezone", len(df.value_counts()))
    return {
        "number of airports in US where there's no DST:": count,
        "number of unique timezone": len(df.value_counts())
    }





# exo1()


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
    plt.show()

def exo3_carrier_nb_origin() -> None:
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

def exo5() -> None:
    """Trouver le nombre de vols par destination ?
    Trier les vols suivant la destination, l’aéroport d’origine,
    la compagnie dans un ordre alphabétique croissant
    (en réalisant les jointures nécessaires pour obtenir
    les noms des explicites des aéroports) ?
    """
    print("nb vol par destination:")
    for dest, value in FLIGHTS.groupby(["dest"]):
        try:
            print(AIRPORTS_JSON[dest], len(value))
        except Exception:
            print(dest, len(value))
    print("\n================================")
    df = FLIGHTS
    df['origin'] = df['origin'].map(
        AIRPORTS.set_index('faa')['name'])
    df['dest'] = df['dest'].map(AIRPORTS.set_index('faa')['name'])
    df['carrier'] = df['carrier'].map(
        AIRLINES.set_index('carrier')['name'])
    result = df.sort_values(["dest", "origin", "carrier"]).groupby("dest").head().set_index('dest')
    return result


# exo5()

def exo6():
    """Quelles sont les compagnies qui n'opèrent pas
    sur tous les aéroports d’origine ?
    Quelles sont les compagnies qui desservent l’ensemble de destinations ?
    Faire un tableau où l’on récupère l’ensemble des origines
    et des destinations pour l’ensemble des compagnies.
    """
    starting_airport = FLIGHTS.origin.drop_duplicates().to_list()
    arrival_airports = FLIGHTS.dest.drop_duplicates().to_list()
    compagnies = FLIGHTS.set_index("carrier").groupby("carrier")
    print("\n", "carrier that start from all origin:")
    for compagnie in compagnies:
        if len(
                compagnie[1].drop_duplicates("origin")) == len(
                    starting_airport):
            print(AIRLINES_JSON[compagnie[0]])
    print("\n", "carrier that go to all dest:")
    for compagnie in compagnies:
        if len(compagnie[1].drop_duplicates("dest")) == len(arrival_airports):
            print(AIRLINES_JSON[compagnie[0]])
    return
    {
        "Nombre de vols par destination" : AIRLINES_JSON[compagnie[0]]
    }

#exo6()

def flight_cancelled():
    print(
        len(FLIGHTS.loc[FLIGHTS["dep_time"] == " "]
            .loc[FLIGHTS["arr_time"] == " "]
            .loc[FLIGHTS["air_time"] == " "]
            ))


# flight_cancelled()
