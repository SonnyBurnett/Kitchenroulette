import huis
import csv
from itertools import combinations
from itertools import permutations
import random
import collections
from tabulate import tabulate


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


def print_eters_en_kokers(lijst_kokers, lijst_eters, gang):
    print("Dit zijn de kokers voor gang", gang)
    for k in lijst_kokers:
        print(k.get_adres())
    print("Dit zijn de eters voor gang", gang)
    for e in lijst_eters:
        print(e.get_adres())
    print("aantal kokers:", len(lijst_kokers), "aantal eters:", len(lijst_eters))


def wijs_eter_aan_koker_toe(koker, eter1, gang):
    if gang == "voorgerecht":
        eter1.set_voorgerecht(koker.get_adres())
    if gang == "hoofdgerecht":
        eter1.set_hoofdgerecht(koker.get_adres())
    if gang == "nagerecht":
        eter1.set_nagerecht(koker.get_adres())
    return koker, eter1


def vind_een_koker(lijst_kokers, lijst_eters, eter_remie, gang):
    geschikte_koker = ""
    gelukt = True
    for koker in lijst_kokers:
        koker_adres = koker.get_adres()
        if koker_adres not in eter_remie.get_lijst_eters():
            if gang == "voorgerecht":
                lijst_voorgerecht = [veter for veter in lijst_eters if veter.voorgerecht == koker_adres]
                if eter_remie.get_adres() not in lijst_voorgerecht:
                    geschikte_koker = koker
                    break
            if gang == "hoofdgerecht":
                lijst_hoofdgerecht = [heter for heter in lijst_eters if heter.hoofdgerecht == koker_adres]
                if eter_remie.get_adres() not in lijst_hoofdgerecht:
                    geschikte_koker = koker
                    break
            if gang == "nagerecht":
                lijst_nagerecht = [neter for neter in lijst_eters if neter.nagerecht == koker_adres]
                if eter_remie.get_adres() not in lijst_nagerecht:
                    geschikte_koker = koker
                    break
    if geschikte_koker == "":
        gelukt = False
    return geschikte_koker, gelukt



def verdeel_eters_over_kokers(gang, lijst_eters, lijst_kokers):
    #print_eters_en_kokers(lijst_kokers, lijst_eters, gang)
    aantal_kokers_beschikbaar = len(lijst_kokers)+1
    aantal_eters_niet_ingedeeld = len(lijst_eters)
    eters_al_toegewezen = []
    alle_eters = []
    for e in lijst_eters:
        alle_eters.append(e.get_adres())


    for koker in lijst_kokers:
        #zoek eter1
        aantal_kokers_beschikbaar -= 1
        print("[KOKER]", koker.get_adres(), "kokers", aantal_kokers_beschikbaar, "eters", aantal_eters_niet_ingedeeld)
        vlag_eter1 = False
        vlag_eter2 = False
        vlag_eter3 = True
        if aantal_kokers_beschikbaar == 2 and aantal_eters_niet_ingedeeld == 2:
            vlag_eter2 = True
            print("nu minder eters toekennen")
        if aantal_kokers_beschikbaar ==1 and aantal_eters_niet_ingedeeld == 3:
            vlag_eter3 = False
            print("nu meer eters toekennen")


        for eter1 in lijst_eters:
            if eter1.get_adres() not in eters_al_toegewezen:
                if eter1.get_adres() not in koker.get_lijst_eters():
                    koker, eter1 = wijs_eter_aan_koker_toe(koker, eter1, gang)
                    eters_al_toegewezen.append(eter1.get_adres())
                    koker.add_eter(eter1.get_adres())
                    eter1.add_eter(koker.get_adres())
                    aantal_eters_niet_ingedeeld-=1
                    vlag_eter1 = True

                    if not vlag_eter2:
                        for eter2 in lijst_eters:
                            if eter2.get_adres() not in eters_al_toegewezen:
                                if eter2.get_adres() not in koker.get_lijst_eters() and eter2.get_adres() not in eter1.get_lijst_eters():
                                    koker, eter2 = wijs_eter_aan_koker_toe(koker, eter2, gang)
                                    koker.add_eter(eter2.get_adres())
                                    eter2.add_eter(koker.get_adres())
                                    eter1.add_eter(eter2.get_adres())
                                    eter2.add_eter(eter1.get_adres())
                                    eters_al_toegewezen.append(eter2.get_adres())
                                    aantal_eters_niet_ingedeeld -= 1
                                    vlag_eter2 = True

                                    if not vlag_eter3:
                                        for eter3 in lijst_eters:
                                            if eter3.get_adres() not in eters_al_toegewezen:
                                                koker_nieuw, gevonden = vind_een_koker(lijst_kokers, lijst_eters, eter3, gang)
                                                if not gevonden:
                                                    print("eter 3:", eter3.get_adres(), "geen koker kunnen vinden")
                                                    koker_nieuw = koker

                                                koker_nieuw, eter3 = wijs_eter_aan_koker_toe(koker_nieuw, eter3, gang)
                                                koker_nieuw.add_eter(eter3.get_adres())
                                                eter3.add_eter(koker_nieuw.get_adres())
                                                eter1.add_eter(eter3.get_adres())
                                                eter3.add_eter(eter1.get_adres())
                                                eter2.add_eter(eter3.get_adres())
                                                eter3.add_eter(eter2.get_adres())
                                                eters_al_toegewezen.append(eter3.get_adres())
                                                aantal_eters_niet_ingedeeld -= 1
                                                vlag_eter3 = True
                                            if vlag_eter3:
                                                break
                            if vlag_eter2:
                                break
            if vlag_eter1:
                break




    if aantal_eters_niet_ingedeeld > 0:
        print("[ERROR] we hebben nog", aantal_eters_niet_ingedeeld, "eters over")
        print(list(set(alle_eters) - set(eters_al_toegewezen)))

    aangepaste_lijst = lijst_kokers+lijst_eters
    return aangepaste_lijst


#################################################



def print_eters(huizen):
    teller = 1
    tabel_schema = []
    tabel_schema.append(["naam", "adres", "kookt gang", "eet voorgerecht bij", "eet voorgerecht met",
                    "eet hoofdgerecht bij", "eet hoofdgerecht met", "eet nagerecht bij", "eet nagerecht met", "aantal personen"])
    for huis in huizen:
        voor_eters = wie_eet_nog_meer_mee("voorgerecht", huis, huizen )
        hoofd_eters = wie_eet_nog_meer_mee("hoofdgerecht", huis, huizen )
        na_eters = wie_eet_nog_meer_mee("nagerecht", huis, huizen )
        # print("nummer:            ", teller)
        # print("naam:             ", huis.get_naam())
        # print("adres:             ", huis.get_adres())
        # print("Je kookt het:      ", huis.get_gang())
        # print("Voorgerecht:       ", huis.get_voorgerecht(), "samen met", voor_eters)
        # print("Hoofdgerecht:      ", huis.get_hoofdgerecht(), "samen met", hoofd_eters)
        # print("Nagerecht:         ", huis.get_nagerecht(), "samen met", na_eters)
        # print("personen:          ", huis.get_aantal_personen())
        # print()
        tabel_schema.append([huis.get_naam(), huis.get_adres(), huis.get_gang(), huis.get_voorgerecht(),voor_eters,
                             huis.get_hoofdgerecht(), hoofd_eters, huis.get_nagerecht(), na_eters, huis.get_aantal_personen()])
        teller += 1
    return tabel_schema


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


def maak_een_dictionairy(schema_lijst):
    return {index: value for index, value in enumerate(schema_lijst)}


def maak_csv_file(schema_tabel):
    with open('kitchenroulette_schema.csv', 'w', newline='') as csvfile:
        fieldnames = ['naam', 'adres', 'kookt gang', 'eet voorgerecht bij','eet voorgerecht met','eet hoofdgerecht bij',
                      'eet hoofdgerecht met', 'eet nagerecht bij', 'eet nagerecht met', 'aantal personen']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        #writer.writerows(schema_tabel)



#################################################

def main():
    deelnemers, aantal_huizen, aantal_deelnemers = get_deelnemers()
    aantallen = verdeel_in_zo_gelijk_mogelijke_groepen(aantal_huizen)
    huizen = get_list_of_houses(deelnemers)
    huizen = assign_gang(aantallen, huizen)


    lijst_kokers, lijst_eters = maak_een_indeling("voorgerecht", huizen)
    lijst_na_voorgerecht = verdeel_eters_over_kokers("voorgerecht", lijst_eters, lijst_kokers)

    lijst_kokers2, lijst_eters2 = maak_een_indeling("hoofdgerecht", lijst_na_voorgerecht)
    lijst_na_hoofdgerecht = verdeel_eters_over_kokers("hoofdgerecht", lijst_eters2, lijst_kokers2)

    lijst_kokers3, lijst_eters3 = maak_een_indeling("nagerecht", lijst_na_hoofdgerecht)
    lijst_na_nagerecht = verdeel_eters_over_kokers("nagerecht", lijst_eters3, lijst_kokers3)

    schema_tabel = print_eters(lijst_na_nagerecht)
    schema_dict = maak_een_dictionairy(schema_tabel)
    maak_csv_file(schema_dict)
    print(tabulate(schema_tabel, headers="firstrow", tablefmt="grid"))



if __name__ == '__main__':
    main()