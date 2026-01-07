import huis
import csv
import pandas as pd


def open_excel(filename):
    df = pd.read_excel(filename, sheet_name="Blad1")
    aantal_deelnemers = df.aantalpersonen.sum()
    aantal_huizen = len(df)
    print("[INFO]", aantal_deelnemers, "deelnemers uit file", filename, "gelezen")
    print("[INFO]", aantal_huizen, "huizen doen mee")
    return df


def tel_voorkeuren(df):
    aantal_voor = (df.voorgerecht == "J").sum()
    aantal_hoofd = (df.hoofdgerecht == "J").sum()
    aantal_na = (df.nagerecht == "J").sum()
    print("[INFO] voorkeur voorgerecht:",aantal_voor, "voorkeur hoofdgerecht:", aantal_hoofd, "voorkeur nagerecht:", aantal_na)


def lees_alle_huizen(df):
    huizen = []
    for row in df.itertuples(index=True):
        aantal_eters = 0
        aantal_huizen = 0
        gang = voorgerecht = hoofdgerecht = nagerecht = ""
        lijst_eters = []
        huizen.append(huis.huis(row.adres,
                                row.aantalpersonen,
                                gang,
                                row.naam,
                                voorgerecht,
                                hoofdgerecht,
                                nagerecht,
                                aantal_eters,
                                lijst_eters,
                                row.voorgerecht,
                                row.hoofdgerecht,
                                row.nagerecht,
                                row.dieetwensen,
                                row.maxaantaleters,
                                aantal_huizen,
                                row.kids,
                                row.kids_mee,))
    print("[INFO]", len(huizen), "huizen in een lijst gezet.")
    return huizen


def get_vorige_keer(vorig_bestand):
    vorige_keer = list(csv.reader(open(vorig_bestand)))
    return vorige_keer


def verdeel_in_zo_gelijk_mogelijke_groepen(aantal_huizen):
    x = divmod(aantal_huizen, 3)
    aantal_voorgerecht = x[0]
    aantal_hoofdgerecht = x[0]
    aantal_nagerecht = x[0]
    if x[1] == 1:
        aantal_nagerecht+=1
    elif x[1] == 2:
        aantal_voorgerecht += 1
        aantal_nagerecht+=1
    print("[INFO] de lijst verdeeld in ", aantal_voorgerecht, "voorgerechten", aantal_hoofdgerecht, "hoofdgerechten", aantal_nagerecht, "nagerechten")
    return [aantal_voorgerecht, aantal_hoofdgerecht, aantal_nagerecht]


def assign_gang(aantallen, huizen):
    eerste_groep = int(aantallen[0])
    tweede_groep = int(aantallen[1])
    derde_groep = int(aantallen[2])
    aantal1 = 0
    aantal2 = 0
    aantal3 = 0
    gelukt = True

    for huis in huizen:
        if huis.get_voorkeur1() == "J" and aantal1 < eerste_groep:
            aantal1 += 1
            huis.set_gang("voorgerecht")
            huis.set_voorgerecht(huis.get_adres())
        elif huis.get_voorkeur2() == "J" and aantal2 < tweede_groep:
            aantal2 += 1
            huis.set_gang("hoofdgerecht")
            huis.set_hoofdgerecht(huis.get_adres())
        elif huis.get_voorkeur3() == "J" and aantal3 < derde_groep:
            aantal3 += 1
            huis.set_gang("nagerecht")
            huis.set_nagerecht(huis.get_adres())
        else:
            print("[ERROR] major problem, stop everything and start over please!")
            gelukt = False

    print("[INFO] aantal voorgerecht",aantal1, "aantal hoofdgerecht", aantal2, "aantal nagerecht", aantal3)
    print("[INFO] Ieder huis heeft een gang om te koken toegewezen gekregen")
    return huizen


def maak_lijst_huizen_met_gang_nieuw():
    input_bestand = "roulette2025.xlsx"
    df = open_excel(input_bestand)
    tel_voorkeuren(df)
    aantal_huizen = len(df)
    huizen = lees_alle_huizen(df)
    aantallen = verdeel_in_zo_gelijk_mogelijke_groepen(aantal_huizen)
    huizen = assign_gang(aantallen, huizen)
    return huizen
