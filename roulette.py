import huis
import voorbereiding
import toon_output
import random
from datetime import datetime


#####################################################


def maak_een_indeling(huidige_gang, huizen):
    kook_ploeg = [huis for huis in huizen if huis.get_gang() == huidige_gang]
    eet_ploeg = [huis for huis in huizen if huis.get_gang() != huidige_gang]
    random.shuffle(kook_ploeg)
    random.shuffle(eet_ploeg)
    print("[INFO] Kokers en eters voor gang", huidige_gang,"in een willekeurige volgorde gezet.")
    print("Kokers:", [kook.get_adres() for kook in kook_ploeg])
    print("Eters:", [eet.get_adres() for eet in eet_ploeg])
    return kook_ploeg, eet_ploeg


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
    alles_toegewezen = True
    originele_lijst = lijst_eters+lijst_kokers
    aantal_kokers_beschikbaar = len(lijst_kokers)
    aantal_eters_niet_ingedeeld = len(lijst_eters)
    eters_al_toegewezen = []
    alle_eters = []
    for e in lijst_eters:
        alle_eters.append(e.get_adres())


    for koker in lijst_kokers:
        vlag_eter1 = False
        vlag_eter2 = False
        vlag_eter3 = True
        if aantal_kokers_beschikbaar == 2 and aantal_eters_niet_ingedeeld == 2:
            vlag_eter2 = True
        if aantal_kokers_beschikbaar ==1 and aantal_eters_niet_ingedeeld == 3:
            vlag_eter3 = False
        if aantal_kokers_beschikbaar == 2 and aantal_eters_niet_ingedeeld == 6:
            vlag_eter3 = False

        for eter1 in lijst_eters:
            if eter1.get_adres() not in eters_al_toegewezen:
                if eter1.get_adres() not in koker.get_lijst_eters():
                    koker, eter1 = wijs_eter_aan_koker_toe(koker, eter1, gang)
                    eters_al_toegewezen.append(eter1.get_adres())
                    koker.add_eter(eter1.get_adres())
                    eter1.add_eter(koker.get_adres())
                    aantal_eters_niet_ingedeeld-=1
                    vlag_eter1 = True
                    aantal_kokers_beschikbaar -= 1

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
        for losers in lijst_eters:
            if losers.get_adres() not in eters_al_toegewezen:
                print("[ERROR] we hebben nog", losers.get_adres())
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
    max_aantal_pogingen = 15

    while not indeling_gelukt and teller < max_aantal_pogingen:
        huizen = voorbereiding.maak_lijst_huizen_met_gang()
        lijst_kokers, lijst_eters = maak_een_indeling("voorgerecht", huizen)
        lijst_na_voorgerecht, gelukt_voorgerecht = verdeel_eters_over_kokers("voorgerecht", lijst_eters, lijst_kokers)
        if gelukt_voorgerecht:
            lijst_kokers2, lijst_eters2 = maak_een_indeling("hoofdgerecht", lijst_na_voorgerecht)
            lijst_na_hoofdgerecht, gelukt_hoofdgerecht = verdeel_eters_over_kokers("hoofdgerecht", lijst_eters2, lijst_kokers2)
            if gelukt_hoofdgerecht:
                lijst_kokers3, lijst_eters3 = maak_een_indeling("nagerecht", lijst_na_hoofdgerecht)
                lijst_na_nagerecht, gelukt_nagerecht = verdeel_eters_over_kokers("nagerecht", lijst_eters3, lijst_kokers3)
                schema_tabel, gelukt_hoofdgerecht = toon_output.print_eters(lijst_na_nagerecht)
        if gelukt_voorgerecht and gelukt_hoofdgerecht and gelukt_nagerecht:
            indeling_gelukt = True
            toon_output.afronden(start_time, lijst_na_nagerecht, schema_tabel)
        else:
            print("[ERROR] Indeling niet gelukt. Start nieuwe poging.")
        teller += 1



if __name__ == '__main__':
    main()