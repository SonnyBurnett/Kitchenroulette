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
        huizen.append(huis.huis(deelnemer[0], int(deelnemer[2]), "", deelnemer[1], "", "", "",
                                0, []))
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
    print("ik ben", ik.get_adres())
    print("voorgerecht: ", voorgerecht)
    print("hoofdgerecht: ", hoofdgerecht)
    print("nagerecht: ", nagerecht)
    for huis in huizen:
        if huis.get_adres() != ik.get_adres():
            print("huis is", huis.get_adres())
            print("Dit huis eet voorgerecht bij", huis.get_voorgerecht())
            print("Dit huis eet hoofdgerecht bij", huis.get_hoofdgerecht())
            print("Dit huis eet nagerecht bij", huis.get_nagerecht())
            if huis.get_voorgerecht() == voorgerecht and huis.get_voorgerecht() != "" and voorgerecht != "":
                lijst_gasten.append(huis.get_adres())
                print("voorgerecht match gevonden", huis.get_adres())
            if huis.get_hoofdgerecht() == hoofdgerecht and huis.get_hoofdgerecht() != "" and hoofdgerecht != "":
                lijst_gasten.append(huis.get_adres())
                print("hoofdgerecht match gevonden", huis.get_adres())
            if huis.get_nagerecht() == nagerecht and huis.get_nagerecht() != "" and nagerecht != "":
                lijst_gasten.append(huis.get_adres())
                print("nagerecht match gevonden", huis.get_adres())
        print()
    if len(lijst_gasten) == len(set(lijst_gasten)):
        success = True

    return lijst_gasten


def verdeel_eters_over_kokers(gang, lijst_eters, lijst_kokers):

    print("Dit zijn de kokers voor gang", gang)
    for k in lijst_kokers:
        print(k.get_adres())
    print("Dit zijn de eters voor gang", gang)
    for e in lijst_eters:
        print(e.get_adres())

    eters_al_toegewezen = []
    for koker in lijst_kokers:
        #zoek eter1
        print("[KOKER]", koker.get_adres())
        for eter1 in lijst_eters:
            #print("[ETER1] probeer:", eter1.get_adres())
            if eter1.get_adres() not in eters_al_toegewezen:
                if eter1.get_adres() not in koker.get_lijst_eters():
                    if gang == "voorgerecht":
                        eter1.set_voorgerecht(koker.get_adres())
                        print("[ETER1 OK", eter1.get_adres(), "eet het voorgerecht bij", koker.get_adres(), "want niet in al gezien", koker.get_lijst_eters())
                    if gang == "hoofdgerecht":
                        eter1.set_hoofdgerecht(koker.get_adres())
                        print("[ETER1 OK", eter1.get_adres(), "eet het hoofdgerecht bij", koker.get_adres(), "want niet in al gezien", koker.get_lijst_eters())
                    if gang == "nagerecht":
                        eter1.set_nagerecht(koker.get_adres())
                        print("[ETER1 OK", eter1.get_adres(), "eet het nagerecht bij", koker.get_adres(), "want niet in al gezien", koker.get_lijst_eters())
                    koker.add_eter(eter1.get_adres())
                    eter1.add_eter(koker.get_adres())
                    eters_al_toegewezen.append(eter1.get_adres())
                    #zoek eter2
                    for eter2 in lijst_eters:
                        #print("[al gedaan", eters_al_toegewezen)
                        #print("[ETER2] probeer:", eter2.get_adres())
                        if eter2.get_adres() not in eters_al_toegewezen:
                            if eter2.get_adres() not in koker.get_lijst_eters() and eter2.get_adres() not in eter1.get_lijst_eters():
                                if gang == "voorgerecht":
                                    eter2.set_voorgerecht(koker.get_adres())
                                    print("[ETER2 OK", eter2.get_adres(), "eet het voorgerecht bij", koker.get_adres(),
                                          "al gezien", koker.get_lijst_eters(), "en niet in eter1", eter1.get_lijst_eters())
                                if gang == "hoofdgerecht":
                                    eter2.set_hoofdgerecht(koker.get_adres())
                                    print("[ETER2 OK", eter2.get_adres(), "eet het hoofdgerecht bij", koker.get_adres(),
                                          "al gezien", koker.get_lijst_eters(), "en niet in eter1", eter1.get_lijst_eters())
                                if gang == "nagerecht":
                                    eter2.set_nagerecht(koker.get_adres())
                                    print("[ETER2 OK", eter2.get_adres(), "eet het nagerecht bij", koker.get_adres(),
                                          "al gezien", koker.get_lijst_eters(), "en niet in eter1", eter1.get_lijst_eters())
                                koker.add_eter(eter2.get_adres())
                                eter2.add_eter(koker.get_adres())
                                eter1.add_eter(eter2.get_adres())
                                eter2.add_eter(eter1.get_adres())
                                eters_al_toegewezen.append(eter2.get_adres())
                                break
                    break

    aangepaste_lijst = lijst_kokers+lijst_eters
    return aangepaste_lijst


#################################################



def print_eters(huizen):
    teller = 1
    for huis in huizen:
        print("nummer:            ", teller)
        print("naam:             ", huis.get_naam())
        print("adres:             ", huis.get_adres())
        print("Je kookt het:      ", huis.get_gang())
        print("Voorgerecht:       ", huis.get_voorgerecht(), "samen met", wie_eet_nog_meer_mee("voorgerecht", huis, huizen ))
        print("Hoofdgerecht:      ", huis.get_hoofdgerecht(), "samen met", wie_eet_nog_meer_mee("hoofdgerecht", huis, huizen ))
        print("Nagerecht:         ", huis.get_nagerecht(), "samen met", wie_eet_nog_meer_mee("nagerecht", huis, huizen ))
        print("personen:          ", huis.get_aantal_personen())
        print()
        teller += 1

def wie_eet_nog_meer_mee(gang, ik, lijst_huizen):
    andere_eters = []

    if gang == "voorgerecht":
        ik_voor = ik.get_voorgerecht()
    if gang == "hoofdgerecht":
        ik_hoofd = ik.get_hoofdgerecht()
    if gang == "nagerecht":
        ik_na = ik.get_nagerecht()

    for huis in lijst_huizen:
        if huis.get_adres() != ik.get_adres():
            if gang == "voorgerecht":
                if ik_voor == huis.get_voorgerecht():
                    andere_eters.append(huis.get_adres())
            if gang == "hoofdgerecht":
                if ik_hoofd == huis.get_hoofdgerecht():
                    andere_eters.append(huis.get_adres())
            if gang == "nagerecht":
                if ik_na == huis.get_nagerecht():
                    andere_eters.append(huis.get_adres())

    return andere_eters




#################################################

def main():
    deelnemers, aantal_huizen, aantal_deelnemers = get_deelnemers()
    aantallen = verdeel_in_zo_gelijk_mogelijke_groepen(aantal_huizen)
    huizen = get_list_of_houses(deelnemers)
    huizen = assign_gang(aantallen, huizen)

    print(huizen[0].get_adres())
    lijst_kokers, lijst_eters = maak_een_indeling("voorgerecht", huizen)
    lijst_na_voorgerecht = verdeel_eters_over_kokers("voorgerecht", lijst_eters, lijst_kokers)
    print_eters(lijst_na_voorgerecht)
    print("[INFO] nu starten we met het hoofdgerecht")

    lijst_kokers2, lijst_eters2 = maak_een_indeling("hoofdgerecht", lijst_na_voorgerecht)
    lijst_na_hoofdgerecht = verdeel_eters_over_kokers("hoofdgerecht", lijst_eters2, lijst_kokers2)

    lijst_kokers3, lijst_eters3 = maak_een_indeling("nagerecht", lijst_na_hoofdgerecht)
    lijst_na_nagerecht = verdeel_eters_over_kokers("nagerecht", lijst_eters3, lijst_kokers3)

    print_eters(lijst_na_nagerecht)




if __name__ == '__main__':
    main()