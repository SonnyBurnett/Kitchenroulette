import huis
import csv

def get_deelnemers(input_bestand):
    deelnemers = list(csv.reader(open(input_bestand)))
    aantal_deelnemers = sum([int(x[2]) for x in deelnemers])
    aantal_huizen = len(deelnemers)
    print("[INFO]",aantal_deelnemers, "deelnemers uit file", input_bestand ,"gelezen")
    print("[INFO]",aantal_huizen, "huizen doen mee")
    return deelnemers, aantal_huizen, aantal_deelnemers


def get_vorige_keer(vorig_bestand):
    vorige_keer = list(csv.reader(open(vorig_bestand)))
    return vorige_keer


def get_list_of_houses(deelnemers):
    huizen = []
    for deelnemer in deelnemers:
        nummer = 0
        #print("[MAIN]", deelnemer[1], deelnemer)
        # for x in deelnemer:
        #     print("[TEST]", nummer, x)
        #     nummer += 1
        #huizen.append(deelnemer[1]) ???????
        huizen.append(huis.huis(deelnemer[0], int(deelnemer[2]), "", deelnemer[1], "", "", "",
                                0, [],deelnemer[3],deelnemer[4],deelnemer[5],deelnemer[7],int(deelnemer[6]),0))
    print("[INFO]",len(huizen), "huizen in een lijst gezet.")
    return huizen


def tel_voorkeur(huizen):
    aantal_voor = 0
    aantal_hoofd = 0
    aantal_na = 0
    for huis in huizen:
        if huis.get_voorkeur1() == "J":
            aantal_voor += 1
        if huis.get_voorkeur2() == "J":
            aantal_hoofd += 1
        if huis.get_voorkeur3() == "J":
            aantal_na += 1
    print("[INFO] voorkeur voor voorgerecht", aantal_voor,"voorkeur voor hoofdgerecht", aantal_hoofd,"voorkeur voor nagerecht", aantal_na)
    return aantal_voor, aantal_hoofd, aantal_na


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
        # if huis.get_adres() == "IJsselmeerdijk 9":
        #     print("[WARN] dit is", huis.get_adres())
        #     print("[WARN] aantal1",aantal1,"eerste groep",eerste_groep)
        if huis.get_voorkeur1() == "J" and aantal1 < eerste_groep:
            aantal1 += 1
            huis.set_gang("voorgerecht")
            huis.set_voorgerecht(huis.get_adres())
            #print("[INFO]", huis.get_adres(), "kookt het voorgerecht")
        elif huis.get_voorkeur2() == "J" and aantal2 < tweede_groep:
            aantal2 += 1
            huis.set_gang("hoofdgerecht")
            huis.set_hoofdgerecht(huis.get_adres())
            #print("[INFO]", huis.get_adres(), "kookt het hoofdgerecht")
        elif huis.get_voorkeur3() == "J" and aantal3 < derde_groep:
            aantal3 += 1
            huis.set_gang("nagerecht")
            huis.set_nagerecht(huis.get_adres())
            #print("[INFO]", huis.get_adres(), "kookt het nagerecht")
        else:
            print("[ERROR] major problem, stop everything and start over please!")
            gelukt = False

    # for a in range(0, eerste_groep):
    #     huizen[a].set_gang("voorgerecht")
    #     huizen[a].set_voorgerecht(huizen[a].get_adres())
    # for b in range(eerste_groep, eerste_groep + tweede_groep):
    #     huizen[b].set_gang("hoofdgerecht")
    #     huizen[b].set_hoofdgerecht(huizen[b].get_adres())
    # for c in range(eerste_groep + tweede_groep, eerste_groep + tweede_groep + derde_groep):
    #     huizen[c].set_gang("nagerecht")
    #     huizen[c].set_nagerecht(huizen[c].get_adres())
    print("[INFO] aantal voorgerecht",aantal1, "aantal hoofdgerecht", aantal2, "aantal nagerecht", aantal3)
    print("[INFO] Ieder huis heeft een gang om te koken toegewezen gekregen")
    return huizen


def maak_lijst_huizen_met_gang():
    input_bestand = "deelnemers2025.txt"
    deelnemers, aantal_huizen, aantal_deelnemers = get_deelnemers(input_bestand)
    aantallen = verdeel_in_zo_gelijk_mogelijke_groepen(aantal_huizen)
    huizen = get_list_of_houses(deelnemers)
    huizen = assign_gang(aantallen, huizen)
    tel_voorkeur(huizen)
    return huizen