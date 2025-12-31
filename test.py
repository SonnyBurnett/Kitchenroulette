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