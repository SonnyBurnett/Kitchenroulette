import voorbereiding
import toon_output
import random
from datetime import datetime
from operator import attrgetter
import pandas as pd



#####################################################
# De lijst met kokers en eters wordt in een willekeurige volgorde gezet.
# Zodat er automatisch een ander schema uit gaat komen.
#

def maak_een_indeling(huidige_gang, huizen):
    kook_ploeg = [huis for huis in huizen if huis.get_gang() == huidige_gang]
    eet_ploeg = [huis for huis in huizen if huis.get_gang() != huidige_gang]
    random.shuffle(kook_ploeg)
    random.shuffle(eet_ploeg)
    print("[INFO] Kokers en eters voor gang", huidige_gang,"in een willekeurige volgorde gezet.")
    print("Kokers:", [kook.get_adres() for kook in kook_ploeg])
    print("Eters:", [eet.get_adres() for eet in eet_ploeg])
    return kook_ploeg, eet_ploeg

#####################################################
# Uitgangspunt is dat al bepaald is welke eter bij welke koker komt.
# En welke gang het betreft.
# Hier wordt het adres van de koker toegevoegd aan de eter.
# Afhankelijk van welke gang het betreft.


def wijs_eter_aan_koker_toe(koker, eter1, gang):
    if gang == "voorgerecht":
        eter1.set_voorgerecht(koker.get_adres())
    if gang == "hoofdgerecht":
        eter1.set_hoofdgerecht(koker.get_adres())
    if gang == "nagerecht":
        eter1.set_nagerecht(koker.get_adres())
    return koker, eter1

#####################################################################################
# Input:  Een eter (object) en een koker (adres)
# Output: Hebben ze elkaar al eerder gezien ja of nee

def al_eerder_gezien(koker_adres, eter):
    if koker_adres not in eter.get_lijst_eters():
        return False
    else: return True


#####################################################################################
# Input:  Een eter (object) en een koker (adres)
# Output: Hebben ze elkaar al eerder gezien ja of nee

def andere_eters_al_eerder_gezien(koker_adres, lijst_eters, gang, eter):
    lijst_eters_bij_koker = [eter for eter in lijst_eters if getattr(eter, gang) == koker_adres]
    wie_hebben_de_eters_al_gezien = [eter.lijst_eters for eter in lijst_eters_bij_koker]
    platte_lijst_alle_eters = [item for sublijst in wie_hebben_de_eters_al_gezien for item in sublijst]
    if eter.get_adres() not in platte_lijst_alle_eters:
        return False
    else:
        return True


def andere_eters_bij_koker(koker_adres, lijst_eters, gang):
    lijst_eters_bij_koker = [eter for eter in lijst_eters if getattr(eter, gang) == koker_adres]
    return lijst_eters_bij_koker

#####################################################################################
# Input:  Een huis (eter) die nog aan een koker moet worden toegewezen.
#         De lijst met kokers, de lijst met eters en de gang die gekookt moet worden
# output: Een koker voor de eter die nog niet was toegewezen.
#
# Checks: De eter mag de koker niet eerder gezien hebben bij een vorige gang
#         De eter mag de andere eters bij deze koker (en deze gang) niet eerder gezien hebben
#

def vind_een_koker_nieuw(lijst_kokers, lijst_eters, eter_toe_te_wijzen, gang):
    geschikte_koker = ""
    gelukt = True
    for koker in lijst_kokers:
        koker_adres = koker.get_adres()
        if not al_eerder_gezien(koker_adres, eter_toe_te_wijzen):
            if not andere_eters_al_eerder_gezien(koker_adres, lijst_eters, gang, eter_toe_te_wijzen):
                geschikte_koker = koker
                break
    if geschikte_koker == "":
        gelukt = False
    return geschikte_koker, gelukt


def vind_een_koker_nieuwst(lijst_kokers, lijst_eters, eter_toe_te_wijzen, gang):
    geschikte_koker = ""
    gelukt = True
    lijst_kokers = sorted(lijst_kokers, key=attrgetter("aantal_huizen"))

    for koker in lijst_kokers:
        koker_adres = koker.adres
        if not al_eerder_gezien(koker_adres, eter_toe_te_wijzen):
            if not andere_eters_al_eerder_gezien(koker_adres, lijst_eters, gang, eter_toe_te_wijzen):
                if not koker.aantal_huizen > 2:
                    if not koker.aantal_personen + eter_toe_te_wijzen.aantal_personen > koker.max_personen:
                        geschikte_koker = koker
                        break
    if geschikte_koker == "":
        gelukt = False
    return geschikte_koker, gelukt


def registreer_gezien(huis1, huis2):
    huis1.add_eter(huis2.adres)
    huis2.add_eter(huis1.adres)
    return huis1, huis2


def verdeel_eters_voor_gang(gang, lijst_eters, lijst_kokers):
    te_verdelen_eters = []
    for eters in lijst_eters:
        te_verdelen_eters.append(eters)
    while len(te_verdelen_eters) > 0:
        eter_toe_te_wijzen = random.choice(te_verdelen_eters)
        te_verdelen_eters.remove(eter_toe_te_wijzen)
        koker, gevonden = vind_een_koker_nieuwst(lijst_kokers, lijst_eters, eter_toe_te_wijzen, gang)
        if gevonden:
            koker.aantal_eters += eter_toe_te_wijzen.aantal_personen
            koker.aantal_huizen += 1
            koker, eter_toe_te_wijzen = wijs_eter_aan_koker_toe(koker, eter_toe_te_wijzen, gang)
            koker, eter_toe_te_wijzen = registreer_gezien(koker, eter_toe_te_wijzen)
            andere_eters = andere_eters_bij_koker(koker.adres, lijst_eters, gang)
            for andere_eter in andere_eters:
                eter_toe_te_wijzen, andere_eter = registreer_gezien(eter_toe_te_wijzen, andere_eter)
        else:
            return lijst_kokers + lijst_eters, False
    return lijst_kokers + lijst_eters, True


#####################################################################################
# Doel:        Alle eters verdelen over de kokers
# Input:       Lijst met eters, lijst met kokers, de gang die het betreft
# output:      Een complete lijst met alle deelnemers, aangepast aan wie waar gaat eten bij deze gang
#              Een indicatie of het gelukt is om alle eters aan een koker toe te wijzen.
#
# Controles:   Elke eter (huis) mag maar 1 keer toegewezen worden aan een koker
#              Een eter mag de koker nog niet eerder gezien hebben bij een vorige gang
#              Een eter mag de andere eters (bij deze koker) nog niet eerder gezien hebben
#              Elke eter moet toegewezen worden.
#              Een koker moet minimaal 1 en mag maximaal 3 eters toegewezen krijgen.
#              [NIEUW] Het aantal personen dat komt eten bij een koker, mag niet meer dan X zijn.
#

def verdeel_eters_over_kokers(gang, lijst_eters, lijst_kokers):
    alles_toegewezen = True
    originele_lijst = lijst_eters+lijst_kokers
    aantal_kokers_beschikbaar = len(lijst_kokers)
    aantal_eters_niet_ingedeeld = len(lijst_eters)
    eters_al_toegewezen = []

    for koker in lijst_kokers:
        eter1_toegewezen = False
        eter2_toegewezen = False
        eter3_toegewezen = False
        eter2_toewijzen = True
        eter3_toewijzen = False
        aantal_personen = koker.aantal_personen
        print("[CHECK] koker", koker.adres, "max_personen koker: ", koker.max_personen)
        aantal1 = aantal2 = aantal3 = 0

        if aantal_kokers_beschikbaar == aantal_eters_niet_ingedeeld:
            eter2_toewijzen = eter3_toewijzen = False
        if aantal_kokers_beschikbaar*3 == aantal_eters_niet_ingedeeld:
            eter2_toewijzen = eter3_toewijzen = True

        for eter1 in lijst_eters:
            if eter1.adres not in eters_al_toegewezen:
                if eter1.adres not in koker.get_lijst_eters():
                    koker, eter1 = wijs_eter_aan_koker_toe(koker, eter1, gang)
                    koker, eter1 = registreer_gezien(koker, eter1)
                    eters_al_toegewezen.append(eter1.adres)
                    aantal_eters_niet_ingedeeld, aantal_kokers_beschikbaar = aantal_eters_niet_ingedeeld - 1, aantal_kokers_beschikbaar - 1
                    aantal_personen += eter1.aantal_personen
                    aantal1 = eter1.aantal_personen
                    eter1_toegewezen = True

                    if eter2_toewijzen:
                        for eter2 in lijst_eters:
                            if eter2.adres not in eters_al_toegewezen:
                                if eter2.adres not in koker.get_lijst_eters() and eter2.adres not in eter1.get_lijst_eters():
                                    if not aantal_personen+eter2.aantal_personen > koker.max_personen:
                                        koker, eter2 = wijs_eter_aan_koker_toe(koker, eter2, gang)
                                        koker, eter2 = registreer_gezien(koker, eter2)
                                        eter1, eter2 = registreer_gezien(eter1, eter2)
                                        eters_al_toegewezen.append(eter2.adres)
                                        aantal_eters_niet_ingedeeld -= 1
                                        aantal_personen += eter2.aantal_personen
                                        aantal2 = eter2.aantal_personen
                                        eter2_toegewezen = True

                                    if eter3_toewijzen:
                                        for eter3 in lijst_eters:
                                            if eter3.adres not in eters_al_toegewezen:
                                                if not aantal_personen + eter3.aantal_personen > koker.max_personen:
                                                    koker_nieuw, gevonden = vind_een_koker_nieuw(lijst_kokers,
                                                                                                 lijst_eters, eter3,
                                                                                                 gang)
                                                    if not gevonden:
                                                        koker_nieuw = koker
                                                    else:
                                                        print("[VALIDATE] nieuwe koker", koker_nieuw.adres,
                                                              "aantal personen deze koker", koker_nieuw.aantal_personen)

                                                    koker_nieuw, eter3 = wijs_eter_aan_koker_toe(koker_nieuw, eter3,
                                                                                                 gang)
                                                    koker_nieuw, eter3 = registreer_gezien(koker_nieuw, eter3)
                                                    eter1, eter3 = registreer_gezien(eter1, eter3)
                                                    eter2, eter3 = registreer_gezien(eter2, eter3)
                                                    eters_al_toegewezen.append(eter3.adres)
                                                    aantal_eters_niet_ingedeeld -= 1
                                                    aantal_personen += eter3.aantal_personen
                                                    aantal3 = eter3.aantal_personen
                                                    eter3_toegewezen = True
                                            if eter3_toegewezen:
                                                break
                            if eter2_toegewezen:
                                break
            if eter1_toegewezen:
                break
        print("[VALIDATE] koker", koker.adres, "aantal personen", aantal_personen, "eters: ", aantal1, aantal2, aantal3)


    if aantal_eters_niet_ingedeeld > 0:
        print("[ERROR] we hebben nog", aantal_eters_niet_ingedeeld, "eters over")
        for loser in lijst_eters:
            if loser.get_adres() not in eters_al_toegewezen:
                print("[ERROR] we hebben nog", loser.get_adres())
                #koker_nieuw, gevonden = vind_een_koker_nieuw(lijst_kokers, lijst_eters, loser, gang)
                #print("[NIEUWE POGING]", koker_nieuw.adres, gevonden)
        alles_toegewezen = False
        return originele_lijst, alles_toegewezen

    if aantal_kokers_beschikbaar > 0:
        print("[ERROR] we hebben nog kokers beschikbaar", aantal_kokers_beschikbaar)
        alles_toegewezen = False
        return originele_lijst, alles_toegewezen

    if alles_toegewezen:
        print("[INFO] indeling van", gang, "succesvol!")
        aangepaste_lijst = lijst_kokers + lijst_eters
        return aangepaste_lijst, alles_toegewezen




#################################################

def main():
    start_time = datetime.now()
    gelukt_hoofdgerecht = False
    gelukt_nagerecht = False
    indeling_gelukt = False
    teller = 0
    max_aantal_pogingen = 50


# Note: maak een indeling hernoemen, naar: zet de lijsten in willekeurige volgorde

    while not indeling_gelukt and teller < max_aantal_pogingen:
        huizen = voorbereiding.maak_lijst_huizen_met_gang()
        lijst_kokers, lijst_eters = maak_een_indeling("voorgerecht", huizen)
        lijst_na_voorgerecht, gelukt_voorgerecht = verdeel_eters_voor_gang("voorgerecht", lijst_eters, lijst_kokers)

        #lijst_na_voorgerecht, gelukt_voorgerecht = verdeel_eters_over_kokers("voorgerecht", lijst_eters, lijst_kokers)
        if gelukt_voorgerecht:
            lijst_kokers2, lijst_eters2 = maak_een_indeling("hoofdgerecht", lijst_na_voorgerecht)
            #lijst_na_hoofdgerecht, gelukt_hoofdgerecht = verdeel_eters_over_kokers("hoofdgerecht", lijst_eters2, lijst_kokers2)
            lijst_na_hoofdgerecht, gelukt_hoofdgerecht = verdeel_eters_voor_gang("hoofdgerecht", lijst_eters2, lijst_kokers2)


            if gelukt_hoofdgerecht:
                lijst_kokers3, lijst_eters3 = maak_een_indeling("nagerecht", lijst_na_hoofdgerecht)
                #lijst_na_nagerecht, gelukt_nagerecht = verdeel_eters_over_kokers("nagerecht", lijst_eters3, lijst_kokers3)
                lijst_na_nagerecht, gelukt_nagerecht = verdeel_eters_voor_gang("nagerecht", lijst_eters3, lijst_kokers3)



                schema_tabel, gelukt_hoofdgerecht = toon_output.print_eters(lijst_na_nagerecht)
        if gelukt_voorgerecht and gelukt_hoofdgerecht and gelukt_nagerecht:
            indeling_gelukt = True
            toon_output.afronden(start_time, lijst_na_nagerecht, schema_tabel)
        else:
            print("[ERROR] Indeling niet gelukt. Start nieuwe poging.")
        teller += 1


        df = voorbereiding.open_excel("roulette2025.xlsx")
        print(type(df))
        voorbereiding.tel_voorkeuren(df)
        huizen = voorbereiding.zet_pandas_in_objecten(df)



if __name__ == '__main__':
    main()