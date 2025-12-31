def vind_een_koker_nieuw(lijst_kokers, lijst_eters, eter_toe_te_wijzen, gang):
    geschikte_koker = ""
    gelukt = True
    for koker in lijst_kokers:
        koker_adres = koker.get_adres()
        if koker_adres not in eter_toe_te_wijzen.get_lijst_eters():
            lijst_eters_bij_koker = [eter for eter in lijst_eters if getattr(eter, gang) == koker_adres()]
            wie_hebben_de_eters_al_gezien = [eter.lijst_eters for eter in lijst_eters_bij_koker]
            platte_lijst_alle_eters = [item for sublijst in wie_hebben_de_eters_al_gezien for item in sublijst]
            if eter_toe_te_wijzen.get_adres() not in platte_lijst_alle_eters:
                geschikte_koker = koker
                break
    if geschikte_koker == "":
        gelukt = False
    return geschikte_koker, gelukt

#####################################################
# Soms is het lastig een eter te plaatsen bij een koker,
# met name als er al eters zijn toegewezen voor deze koker (en de betreffende gang).
# Doorloop alle kokers
# Check of de eter die nog niet is toegewezen, al eerder met deze koker heeft gegeten (bij een vorige gang).
# door de lijst met eters te checken van de toe te wijzen eter.
# Check dan of de andere eters bij deze gang, bij deze koker,
# deze te plaatsen eter nog niet gezien hebben.
#

def vind_een_koker(lijst_kokers, lijst_eters, eter_toe_te_wijzen, gang):
    print("[CHECK] vind een koker voor ", eter_toe_te_wijzen.adres)
    lijst_van_eters_van_eter = eter_toe_te_wijzen.get_lijst_eters()
    print("[CHECK] lijst met eters van eter is", lijst_van_eters_van_eter)
    geschikte_koker = ""
    gelukt = True
    for koker in lijst_kokers:
        koker_adres = koker.get_adres()
        if koker_adres not in eter_toe_te_wijzen.get_lijst_eters():
            if gang == "voorgerecht":
                print("[CHECK] voorgerecht, potentiele koker is", koker_adres)
                lijst_voorgerecht = [veter for veter in lijst_eters if veter.voorgerecht == koker_adres]
                print("[CHECK] !!!!", getattr(lijst_voorgerecht[0], gang))
                print("[CHECK] !!!!", [eter for eter in lijst_eters if getattr(eter, gang) == koker_adres])
                print("[CHECK] voorgerecht_lijst", [h.adres for h in lijst_voorgerecht])
                print("[CHECK], eter adres", eter_toe_te_wijzen.get_adres())
                lijsten = [e.lijst_eters for e in lijst_voorgerecht]
                alle_eters = [item for sublijst in lijsten for item in sublijst]
                print("[CHECK] alle_eters", alle_eters)
                if eter_toe_te_wijzen.get_adres() not in lijst_voorgerecht:
                    geschikte_koker = koker
                    print("[CHECK] eter niet in lijst, succes")
                    break
            if gang == "hoofdgerecht":
                print("[CHECK] hoofdgerecht, potentiele koker is", koker_adres)
                lijst_hoofdgerecht = [heter for heter in lijst_eters if heter.hoofdgerecht == koker_adres]
                print("[CHECK] lijst hoofdgerecht", [h.adres for h in lijst_hoofdgerecht])
                print("[CHECK], eter adres", eter_toe_te_wijzen.get_adres())
                lijsten = [e.lijst_eters for e in lijst_hoofdgerecht]
                alle_eters = [item for sublijst in lijsten for item in sublijst]
                print("[CHECK] alle_eters", alle_eters)
                if eter_toe_te_wijzen.get_adres() not in lijst_hoofdgerecht:
                    geschikte_koker = koker
                    print("[CHECK] eter niet in lijst, succes")
                    break
            if gang == "nagerecht":
                print("[CHECK] nagerecht , potentiele koker is", koker_adres)
                lijst_nagerecht = [neter for neter in lijst_eters if neter.nagerecht == koker_adres]
                print("[CHECK] lijst nagerecht", [h.adres for h in lijst_nagerecht])
                print("[CHECK], eter adres", eter_toe_te_wijzen.get_adres())
                lijsten = [e.lijst_eters for e in lijst_nagerecht]
                alle_eters = [item for sublijst in lijsten for item in sublijst]
                print("[CHECK] alle_eters", alle_eters)
                if eter_toe_te_wijzen.get_adres() not in lijst_nagerecht:
                    geschikte_koker = koker
                    print("[CHECK] eter niet in lijst, succes")
                    break
    if geschikte_koker == "":
        gelukt = False
        print("[CHECK] alles is Mislukt")
    return geschikte_koker, gelukt

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

#####################################################################################
# Input:  Een eter (object) en een koker (adres)
# Output: Hebben ze elkaar al eerder gezien ja of nee

def al_eerder_gezien(koker_adres, eter):
    if koker_adres not in eter.get_lijst_eters():
        return False
    else: return True

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
