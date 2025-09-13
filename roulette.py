import huis
import csv
from itertools import combinations
from itertools import permutations
import random
import collections


def get_deelnemers():
    deelnemers = list(csv.reader(open("deelnemers.txt")))
    aantal_deelnemers = sum([int(x[2]) for x in deelnemers])
    aantal_huizen = len(deelnemers)
    print("[INFO]",aantal_deelnemers, "deelnemers uit file deelnemers.txt gelezen")
    print("[INFO]",aantal_huizen, "huizen doen mee")
    return deelnemers, aantal_huizen, aantal_deelnemers


def get_list_of_houses(deelnemers):
    huizen = []
    for deelnemer in deelnemers:
        huizen.append(huis.huis(deelnemer[0], int(deelnemer[2]), "", deelnemer[1], "", "", ""))
    print("[INFO]",len(huizen), "huizen in een lijst gezet.")
    return huizen


def unieke_combinaties(items, r):
    print("[INFO]  lijst met unieke combinaties gemaakt.")
    return set(combinations(items, r))


def verdeel_in_zo_gelijk_mogelijke_groepen(aantal_huizen):
    x = divmod(aantal_huizen, 3)
    aantal_voorgerecht = x[0]
    aantal_hoofdgerecht = x[0]
    aantal_nagerecht = x[0]
    if x[1] == 1:
        aantal_voorgerecht+=1
    elif x[1] == 2:
        aantal_voorgerecht += 1
        aantal_hoofdgerecht+=1
    else:
        print("good to go")
    print("[INFO] de lijst verdeeld in ", aantal_voorgerecht, "voorgerechten", aantal_hoofdgerecht, "hoofdgerechten", aantal_nagerecht, "nagerechten")
    return [aantal_voorgerecht, aantal_hoofdgerecht, aantal_nagerecht]


def assign_gang(aantallen, huizen):
    eerste_groep = aantallen[0]
    tweede_groep = aantallen[1]
    derde_groep = aantallen[2]
    for a in range(0, eerste_groep):
        huizen[a].set_gang("voorgerecht")
        huizen[a].set_voorgerecht(huizen[a].get_adres())
    for b in range(eerste_groep, eerste_groep + tweede_groep):
        huizen[b].set_gang("hoofdgerecht")
        huizen[b].set_hoofdgerecht(huizen[b].get_adres())
    for c in range(eerste_groep + tweede_groep, eerste_groep + tweede_groep + derde_groep):
        huizen[c].set_gang("nagerecht")
        huizen[c].set_nagerecht(huizen[c].get_adres())
    print("[INFO] Ieder huis heeft een gang om te koken toegewezen gekregen")
    return huizen


def set_gang_eters(gang, huis, adres):
    if gang == "voorgerecht":
        huis.set_voorgerecht(adres)
    elif gang == "hoofdgerecht":
        huis.set_hoofdgerecht(adres)
    elif gang == "nagerecht":
        huis.set_nagerecht(adres)
    else:
        print("error")
    return


#####################################################


def maak_een_indeling(huidige_gang, huizen):
    kook_ploeg = [huis for huis in huizen if huis.get_gang() == huidige_gang]
    eet_ploeg = [huis for huis in huizen if huis.get_gang() != huidige_gang]
    alle_mogelijkheden_eters = list(permutations(eet_ploeg))
    lijst_eters = list(random.choice(alle_mogelijkheden_eters))
    alle_mogelijkheden_kokers = list(permutations(kook_ploeg))
    lijst_kokers = list(random.choice(alle_mogelijkheden_kokers))
    print("[INFO] Kokers en eters voor gang", huidige_gang,"in een willekeurige volgorde gezet.")
    return lijst_kokers, lijst_eters


def geef_de_dubbele(a):
    return [item for item, count in collections.Counter(a).items() if count > 1]


def met_wie_heb_ik_al_gegeten(ik, huizen):
    success = False
    lijst_gasten = []
    voorgerecht = ik.get_voorgerecht()
    hoofdgerecht = ik.get_hoofdgerecht()
    nagerecht = ik.get_nagerecht()
    for huis in huizen:
        if huis.get_adres() != ik.get_adres():
            if huis.get_voorgerecht() == voorgerecht:
                lijst_gasten.append(huis.get_adres())
                #print("voorgerecht gevonden", huis.get_adres())
            if huis.get_hoofdgerecht() == hoofdgerecht:
                lijst_gasten.append(huis.get_adres())
                #print("hoofdgerecht gevonden", huis.get_adres())
            if huis.get_nagerecht() == nagerecht:
                lijst_gasten.append(huis.get_adres())
                #print("nagerecht gevonden", huis.get_adres())
    if len(lijst_gasten) == len(set(lijst_gasten)):
        success = True

    return success, geef_de_dubbele(lijst_gasten)


def gang_indelen(gang, lijst_eters, lijst_kokers):
    nieuwe_lijst = []
    for eter in lijst_eters:
        for koker in lijst_kokers:
            if gang == "voorgerecht":
                eter.set_voorgerecht(koker.get_adres())
            if gang == "hoofdgerecht":
                eter.set_hoofdgerecht(koker.get_adres())
            if gang == "nagerecht":
                eter.set_nagerecht(koker.get_adres())
            gelukt, lijst_dubbele = met_wie_heb_ik_al_gegeten(eter, lijst_eters)
            print("eter", eter.get_adres(), "koker", koker.get_adres(), gelukt, lijst_dubbele)
        nieuwe_lijst.append(eter)
    return nieuwe_lijst


def indeling_gang(gang, lijst_eters, lijst_kokers):
    gelukt = True
    teller = 0
    nieuwe_lijst = []
    for eter in lijst_eters:
        if teller >= len(lijst_kokers):
            teller = 0
        adres = lijst_kokers[teller].get_adres()
        if gang == "voorgerecht":
            eter.set_voorgerecht(adres)
        elif gang == "hoofdgerecht":
            eter.set_hoofdgerecht(adres)
        elif gang == "nagerecht":
            eter.set_nagerecht(adres)
        else:
            print("error")
        teller += 1
        nieuwe_lijst.append(eter)
    if gelukt:
        print("[INFO] lijst met eters aangepast voor gang", gang, gelukt)
    else:
        print("[ERROR] geen unieke combinatie kunnen vinden, gelukt")
    return nieuwe_lijst, gelukt


def print_lijstje(huizen):
    for huis in huizen:
        print(huis.get_adres())




#################################################



def print_eters(huizen):
    teller = 1
    for huis in huizen:
        print("nummer:            ", teller)
        print("naam:             ", huis.get_naam())
        print("adres:             ", huis.get_adres())
        print("Je kookt het:      ", huis.get_gang())
        print("Voorgerecht:       ", huis.get_voorgerecht())
        print("Hoofdgerecht:      ", huis.get_hoofdgerecht())
        print("Nagerecht:         ", huis.get_nagerecht())
        print("personen:          ", huis.get_aantal_personen())
        print()
        teller += 1

def maak_paren(lijstje):
    paren_lijst = []
    for x in range(3):
        for y in range(3):
            if len(lijstje[x]) > 0 and len(lijstje[y]) > 0 and x != y:
                    paren_lijst.append((lijstje[x], lijstje[y]))
    return paren_lijst


def print_combinaties(huizen):
    combinaties = []
    for huis in huizen:
        combinaties.append([huis.get_voorgerecht(), huis.get_hoofdgerecht(), huis.get_nagerecht()])
    return combinaties


def dubbele_items(lijst):
    return [item for item, count in collections.Counter(lijst).items() if count > 1]


def he_die_heb_ik_al_gezien(lijst_huizen):
    lijst_met_alle_paren = []
    success = True
    huis_gasten = print_combinaties(lijst_huizen)
    for huis in huis_gasten:
        combinaties_gasten = []
        combinaties_gasten = maak_paren(huis)
        for gast in combinaties_gasten:
            lijst_met_alle_paren.append(gast)

    dubbele = dubbele_items(lijst_met_alle_paren)
    if len(lijst_met_alle_paren) != len(set(lijst_met_alle_paren)):
        success = False
        print("[ERROR]", dubbele)
    else:
        print("[OK]")

    return success



#################################################

def main():
    deelnemers, aantal_huizen, aantal_deelnemers = get_deelnemers()
    aantallen = verdeel_in_zo_gelijk_mogelijke_groepen(aantal_huizen)
    huizen = get_list_of_houses(deelnemers)
    huizen = assign_gang(aantallen, huizen)
    lijst_kokers, lijst_eters = maak_een_indeling("voorgerecht", huizen)
    nieuwe_lijst_eters, gelukt = indeling_gang("voorgerecht", lijst_eters, lijst_kokers)
    lijst_na_voorgerecht = lijst_kokers+lijst_eters

    success = False
    teller = 1
    while not success:
        lijst_kokers2, lijst_eters2 = maak_een_indeling("hoofdgerecht", lijst_na_voorgerecht)
        #nog_nieuwe_lijst_eters, gelukt = indeling_gang("hoofdgerecht", lijst_eters2, lijst_kokers2)
        nog_nieuwe_lijst_eters = gang_indelen("hoofdgerecht", lijst_eters2, lijst_kokers2)
        lijst_na_hoofdgerecht = lijst_kokers2 + lijst_eters2
        success = he_die_heb_ik_al_gezien(lijst_na_hoofdgerecht)
        teller += 1
        if teller > 1:
            break

    lijst_kokers3, lijst_eters3 = maak_een_indeling("nagerecht", lijst_na_hoofdgerecht)
    nog_nieuwe_lijst_eters, gelukt = indeling_gang("nagerecht", lijst_eters3, lijst_kokers3)
    lijst_na_nagerecht = lijst_kokers3 + lijst_eters3
    success = he_die_heb_ik_al_gezien(lijst_na_nagerecht)
    print_eters(lijst_na_nagerecht)









if __name__ == '__main__':
    main()