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


# Exercice 1 :

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

# Exercice 2 :

def busiest_departure_airport():
    aeroport = FLIGHTS["origin"].mode()
    return aeroport

def most_frequent_destinations():
    merged_tables = FLIGHTS.merge(AIRPORTS,how ='left', left_on ='dest', right_on ='faa')
    frequent_destinations = merged_tables['name'].value_counts(normalize=True).head(10)
    return frequent_destinations

def less_frequent_destinations():
    destinations_moins_prisées = merged_tables['name'].value_counts(normalize=True).tail(10)
    return destinations_moins_prisées

def planes_taken_off_the_most():
    planes_most  = FLIGHTS['tailnum'].value_counts().head(10)
    return planes_most

def planes_taken_off_the_least():
    les_10_avions_moins = FLIGHTS['tailnum'].value_counts().tail(10)
    return les_10_avions_moins


#Exercice 3 :

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

#Exercice 4 :
def landed_in_Houston():
    landed_Houston = FLIGHTS.loc[FLIGHTS['dest'].isin(['IAH','HOU'])]
    return landed_Houston
def NYC_to_Seattle():
    NYC_to_Seattle_table = FLIGHTS.loc[FLIGHTS['dest'].isin(["SEA"])]
    NYC_Seattle = NYC_to_Seattle_table['dest'].value_counts()
    return NYC_Seattle
def carrier_NYC_to_Seattle():
    NYC_Seattle_carrier = NYC_to_Seattle_table['carrier'].drop_duplicates(keep='first').count()
    return NYC_Seattle_carrier

def plane_NYC_to_Seattle():
    flights_sea = FLIGHTS[FLIGHTS['dest']=='SEA']
    return flights_sea['tailnum'].nunique()


#Exercice 5 :

def exo5() -> None:
    """Trouver le nombre de vols par destination ?
    Trier les vols suivant la destination, l’aéroport d’origine,
    la compagnie dans un ordre alphabétique croissant
    (en réalisant les jointures nécessaires pour obtenir
    les noms des explicites des aéroports) ?
    """
    flights = pd.read_csv("flights.csv")
    print("nb vol par destination:")
    for dest, value in flights.groupby(["dest"]):
        try:
            print(AIRPORTS_JSON[dest], len(value))
        except Exception:
            print(dest, len(value))
    print("\n================================")
    df = flights
    df['origin'] = df['origin'].map(
        AIRPORTS.set_index('faa')['name'])
    df['dest'] = df['dest'].map(AIRPORTS.set_index('faa')['name'])
    df['carrier'] = df['carrier'].map(
        AIRLINES.set_index('carrier')['name'])
    result = df.sort_values(["dest", "origin", "carrier"]).groupby("dest").head().set_index('dest')
    return result

#Exercice 6 :

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
    origins = {}
    for compagnie in compagnies:
        if len(
                compagnie[1].drop_duplicates("origin")) == len(
                    starting_airport):
            print(AIRLINES_JSON[compagnie[0]])
        origins[AIRLINES_JSON[compagnie[0]]] = (
            compagnie[1].drop_duplicates("origin").origin.to_list())
    print("\n", "carrier that go to all dest:")
    for compagnie in compagnies:
        if len(compagnie[1].drop_duplicates("dest")) == len(arrival_airports):
            print(AIRLINES_JSON[compagnie[0]])


#Exercice 7 :

def destinations_exclusive():
    groupby_destination_table = FLIGHTS.groupby(by="dest").nunique()
    exclusive  = groupby_destination_table[groupby_destination_table['carrier'] == 1 ]
    return list(exclusive.index.values)


#Exercice 8 :

def flights_UAD():
    United_American_Delta_table  = FLIGHTS.loc[FLIGHTS['carrier'].isin(["UA", "AA", "DL"])]
    return United_American_Delta_table

flights_UAD()

def flight_cancelled():
    print(
        len(FLIGHTS.loc[FLIGHTS["dep_time"] == " "]
            .loc[FLIGHTS["arr_time"] == " "]
            .loc[FLIGHTS["air_time"] == " "]
            ))

