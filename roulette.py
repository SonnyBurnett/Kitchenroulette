import voorbereiding
import toon_output
import random
from operator import attrgetter


#####################################################
# De lijst met kokers en eters wordt in een willekeurige volgorde gezet.
# Zodat er automatisch een ander schema uit gaat komen.
#

def maak_willekeurige_volgorde(huidige_gang, huizen):
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
# Output: heeft de eter de andere eters bij deze koker en deze gang al gezien: ja of nee

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


def verdeel_eters_voor_gang(gang, huizen):
    te_verdelen_eters = []
    lijst_kokers, lijst_eters = maak_willekeurige_volgorde(gang, huizen)

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




#################################################

def main():
    gelukt_hoofdgerecht = gelukt_nagerecht = indeling_gelukt = False
    lijst_na_nagerecht = []
    teller = 0
    max_aantal_pogingen = 50

    while not indeling_gelukt and teller < max_aantal_pogingen:
        huizen = voorbereiding.maak_lijst_huizen_met_gang_nieuw()
        lijst_na_voorgerecht, gelukt_voorgerecht = verdeel_eters_voor_gang("voorgerecht", huizen)
        if gelukt_voorgerecht:
            lijst_na_hoofdgerecht, gelukt_hoofdgerecht = verdeel_eters_voor_gang("hoofdgerecht", huizen)
            if gelukt_hoofdgerecht:
                lijst_na_nagerecht, gelukt_nagerecht = verdeel_eters_voor_gang("nagerecht", huizen)
        if gelukt_voorgerecht and gelukt_hoofdgerecht and gelukt_nagerecht:
            indeling_gelukt = True
            toon_output.afronden(lijst_na_nagerecht)
        else:
            print("[ERROR] Indeling niet gelukt. Start nieuwe poging.")
        teller += 1


if __name__ == '__main__':
    main()