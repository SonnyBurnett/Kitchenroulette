
from tabulate import tabulate
from datetime import datetime
import voorbereiding
from operator import attrgetter



def print_eters_en_kokers(lijst_kokers, lijst_eters, gang):
    print("Dit zijn de kokers voor gang", gang)
    for k in lijst_kokers:
        print(k.get_adres())
    print("Dit zijn de eters voor gang", gang)
    for e in lijst_eters:
        print(e.get_adres())
    print("aantal kokers:", len(lijst_kokers), "aantal eters:", len(lijst_eters))


def print_eters(huizen):
    teller = 1
    gelukt = True
    huizen = sorted(huizen, key=attrgetter("gang"))
    tabel_schema = []
    tabel_schema.append(["naam", "adres", "kookt gang", "eet voorgerecht bij", "eet voorgerecht met",
                    "eet hoofdgerecht bij", "eet hoofdgerecht met", "eet nagerecht bij", "eet nagerecht met", "aantal huizen", "aantal eters"])
    for huis in huizen:
        voor_eters = wie_eet_nog_meer_mee("voorgerecht", huis, huizen )
        hoofd_eters = wie_eet_nog_meer_mee("hoofdgerecht", huis, huizen )
        na_eters = wie_eet_nog_meer_mee("nagerecht", huis, huizen )
        if len(hoofd_eters) > 3 :
            gelukt = False
            #print("[ERREUR]", hoofd_eters)
        # print("nummer:            ", teller)
        # print("naam:             ", huis.get_naam())
        # print("adres:             ", huis.get_adres())
        # print("Je kookt het:      ", huis.get_gang())
        # print("Voorgerecht:       ", huis.get_voorgerecht(), "samen met", voor_eters)
        # print("Hoofdgerecht:      ", huis.get_hoofdgerecht(), "samen met", hoofd_eters)
        # print("Nagerecht:         ", huis.get_nagerecht(), "samen met", na_eters)
        # print("personen:          ", huis.get_aantal_personen())
        # print()
        #print("#",huis.get_naam(), "#", huis.get_adres(), "#",huis.get_gang(), "#",huis.get_voorgerecht(), "#",voor_eters,
        #                      "#", huis.get_hoofdgerecht(), "#", hoofd_eters, "#", huis.get_nagerecht(), "#", na_eters, "#", huis.get_aantal_personen(),"#",huis.get_opmerkingen())
        tabel_schema.append([huis.get_naam(), huis.get_adres(), huis.get_gang(), huis.get_voorgerecht(),voor_eters,
                             huis.get_hoofdgerecht(), hoofd_eters, huis.get_nagerecht(), na_eters, huis.aantal_huizen, huis.aantal_eters])
        teller += 1
    return tabel_schema, gelukt


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




def check_vorige_keer(lijst_huizen, lijst_vorige):
    for huis in lijst_huizen:
        dit_adres = huis.get_adres()
        deze_gang = huis.get_gang()
        #print("[KOKER]", huis.get_adres(), huis.get_gang())
        for h in lijst_huizen:
            lijstje_etertjes = []
            if deze_gang == "voorgerecht":
                if h.get_voorgerecht() == dit_adres and h.get_adres() != dit_adres:
                    #print("[ETER VOOR]", h.get_adres())
                    lijstje_etertjes.append(h.get_adres())
            if deze_gang == "hoofdgerecht" and h.get_adres() != dit_adres:
                if h.get_hoofdgerecht() == dit_adres:
                    #print("[ETER HOOFD]", h.get_adres())
                    lijstje_etertjes.append(h.get_adres())
            if deze_gang == "nagerecht" and h.get_adres() != dit_adres:
                if h.get_nagerecht() == dit_adres:
                    #print("[ETER NA]", h.get_adres())
                    lijstje_etertjes.append(h.get_adres())
        for v in lijst_vorige:
            if v[0] == dit_adres:
                #print("[VORIGE]", v)
                for e in lijstje_etertjes:
                    if e in v:
                        print("[ERROR] koker",dit_adres,"heeft vorige keer ook voor eter",e," gekookt")


def afronden(lijst_na_nagerecht):
    schema_tabel, gelukt_hoofdgerecht = print_eters(lijst_na_nagerecht)
    vorig_bestand = "deel.txt"
    vorige_keer = voorbereiding.get_vorige_keer(vorig_bestand)
    check_vorige_keer(lijst_na_nagerecht, vorige_keer)
    print(tabulate(schema_tabel, headers="firstrow", tablefmt="grid"))
    with open('kitchenroulette_schema.txt', 'w') as f:
        f.write(tabulate(schema_tabel, headers="firstrow", tablefmt="grid"))