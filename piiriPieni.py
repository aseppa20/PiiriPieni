import math
import cmath
import ikkunasto as ikn
import piiristo
import sim

# Käyttöliittymän elementit ja muut globaalit arvot
KLIITTYMÄ = {
    "syote": [None, None, None],
    "piirikuva": None,
    "muutokset": None,
    "tulokset": None,
    "logi": None,
    "laskentatulokset": None,
    "komplistaus": None,
    "jannite": 0,
    "taajuus": 0,
    "komponentit": [[]],
    "wizAk": None,
    "kompAk": None
}


# Jännitteiden ja taajuuksien asetus
def asetaJannite():
    """
    Lukee syötekenttää ja koettaa asettaa jännitteen.
    """
    janniteTulokas = ikn.lue_kentan_sisalto(KLIITTYMÄ["syote"[0]]).strip()
    # Muunnos SI yksikköön. Tarkistaa myös syötteen kelvollisuuden. Jos ei kelvollinen,
    # palauttaa "None" arvon.
    janniteTulokas = sim.muunnaSi(janniteTulokas)

    if janniteTulokas:
        KLIITTYMÄ["jannite"] = janniteTulokas
        tulostus = sim.Si_ksi(janniteTulokas)
        ikn.kirjoita_tekstilaatikkoon(
            KLIITTYMÄ["logi"], "Jännite: {}{} V".format(tulostus[0], tulostus[1]))
    else:
        ikn.avaa_viesti_ikkuna("Virhe!", "Syöte ei ollut kelvollinen.", True)

    ikn.tyhjaa_kentan_sisalto(KLIITTYMÄ["syote"[0]])


def asetaTaajuus():
    """
    Lukee syötekenttää ja koettaa asettaa taajuuden.
    """
    taajuusTulokas = ikn.lue_kentan_sisalto(KLIITTYMÄ["syote"[1]]).strip()
    # Muunnos SI yksikköön. Tarkistaa myös syötteen kelvollisuuden. Jos ei kelvollinen,
    # palauttaa "None" arvon.
    taajuusTulokas = sim.muunnaSi(taajuusTulokas)

    if taajuusTulokas:
        KLIITTYMÄ["taajuus"] = taajuusTulokas
        tulostus = sim.Si_ksi(taajuusTulokas)
        ikn.kirjoita_tekstilaatikkoon(
            KLIITTYMÄ["logi"], "Taajuus: {}{} Hz".format(tulostus[0], tulostus[1]))
    else:
        ikn.avaa_viesti_ikkuna("Virhe!", "Syöte ei ollut kelvollinen.", True)

    ikn.tyhjaa_kentan_sisalto(KLIITTYMÄ["syote"[1]])


# Komponenttien lisäämiseen tarkoitetut funktiot
def tarkistaID(id):
    """
    Tekee tarkistuksen komponentin haaran ID:stä. Jos tyhjä tai negatiivinen, palauttaa 0.
    """
    try:
        if id == "":
            return 0
        luku = int(id)
    except ValueError:
        luku = len(KLIITTYMÄ["komponentit"])

    # Jos ensimmäinen lista (haara) on tyhjä, palautetaan ensimmäinen haaran ID
    if not KLIITTYMÄ["komponentit"][0]:
        return 0

    # Palautetaan komponenttien haarojen ID. Negatiivinen palauttaa 0.
    if luku < 0:
        ikn.avaa_viesti_ikkuna(
            "Huom!", "Antamasi ID oli negatiivinen luku. Komponentti lisätty haaraan ID: 0")
        return 0
    elif luku <= len(KLIITTYMÄ["komponentit"]) - 1:
        return luku
    elif luku == len(KLIITTYMÄ["komponentit"]):
        KLIITTYMÄ["komponentit"].append([])
        return luku

    ikn.avaa_viesti_ikkuna(
        "Huom!", "Antamasi ID ei ollut kelvollinen. Komponentti lisätään uuteen haaraan. Uuden haaran ID: {}".format(luku))
    KLIITTYMÄ["komponentit"].append([])
    return len(KLIITTYMÄ["komponentit"])


def lisaaKomponentti():
    """
    Lisää komponentin haaraan.
    """
    komp = ikn.lue_kentan_sisalto(KLIITTYMÄ["syote"[0]]).strip().lower()
    arvo = ikn.lue_kentan_sisalto(KLIITTYMÄ["syote"[1]]).strip()
    id = ikn.lue_kentan_sisalto(KLIITTYMÄ["syote"[2]]).strip()
    sallitut = ("v", "r", "k", "l", "c")

    if not komp in sallitut:
        ikn.avaa_viesti_ikkuna(
            "Virhe!", "Komponentti ei ollut kelvollinen.", True)
        ikn.tyhjaa_kentan_sisalto(KLIITTYMÄ["syote"[0]])
        return

    if komp == "v":
        komp = "r"
    elif komp == "k":
        komp = "l"

    arvo = sim.muunnaSi(arvo)
    if not arvo:
        ikn.avaa_viesti_ikkuna("Virhe!", "Arvo ei ollut kelvollinen.", True)
        ikn.tyhjaa_kentan_sisalto(KLIITTYMÄ["syote"[1]])
        return

    komp = (komp, arvo)
    id = tarkistaID(id)

    KLIITTYMÄ["komponentit"][id].append(komp)
    komponenttilistaus()
    piirtaja()


def komponenttilistaus():
    """
    Komponenttien tekstiesikatselu Wizardissa.
    """
    ikn.kirjoita_tekstilaatikkoon(KLIITTYMÄ["komplistaus"], "", True)
    for i in range(len(KLIITTYMÄ["komponentit"])):
        ikn.kirjoita_tekstilaatikkoon(
            KLIITTYMÄ["komplistaus"], "Haara {}:".format(i))
        for u in KLIITTYMÄ["komponentit"][i]:
            tulostus = sim.Si_ksi(u[1])
            ikn.kirjoita_tekstilaatikkoon(
                KLIITTYMÄ["komplistaus"], "Komponentti: {}, Arvo: {}{}".format(u[0], tulostus[0], tulostus[1]))


def piirtaja():
    """
    Komponenttien piirtäjä piirtoalueille
    """
    piiristo.tyhjaa_piiri(KLIITTYMÄ["piirikuva"])
    h_asettelu = natistaja()
    piiristo.piirra_jannitelahde(
        KLIITTYMÄ["piirikuva"], KLIITTYMÄ["jannite"], KLIITTYMÄ["taajuus"])
    for i in range(len(KLIITTYMÄ["komponentit"])):
        if i < len(KLIITTYMÄ["komponentit"]) - 1:
            piiristo.piirra_haara(
                KLIITTYMÄ["piirikuva"], KLIITTYMÄ["komponentit"][i], h_asetteluvali=h_asettelu)
        else:
            piiristo.piirra_haara(
                KLIITTYMÄ["piirikuva"], KLIITTYMÄ["komponentit"][i], h_asetteluvali=h_asettelu, viimeinen=True)

    piiristo.piirra_piiri(KLIITTYMÄ["piirikuva"])

    # Laitetaan laskuri pyörimään samalla
    ikn.kirjoita_tekstilaatikkoon(
        KLIITTYMÄ["laskentatulokset"], "", tyhjaa=True)
    laskuri()


def natistaja():
    """
    Laskee komponenteille h_asetteluvälin. Poistaa hieman sumppuja ja hidastaa kuvan rikkoutumista.
    """
    luku = 7
    for i in KLIITTYMÄ["komponentit"]:
        if len(i) + 2 > luku:
            luku = len(i) + 2
    return luku


# Laskelmat
def laskuri():
    """
    Aloittaa laskemalla kokonaisimpedanssit haaroille.
    """
    haarojenImp = []

    for i in range(len(KLIITTYMÄ["komponentit"])):
        haaranimp = 0  # Itseisarvo
        kompimp = []  # Itseisarvot jännitelaskuille
        ikn.kirjoita_tekstilaatikkoon(
            KLIITTYMÄ["laskentatulokset"], "\nhaara {}:".format(i))

        for komp, arvo in KLIITTYMÄ["komponentit"][i]:
            imp = 0
            if komp != "r":
                imp = 2 * math.pi * KLIITTYMÄ["taajuus"] * arvo * 1j
                if komp == "c" and imp != 0:
                    imp = 1/imp
            else:
                imp = arvo

            Z = cmath.polar(imp)
            tulostus = sim.Si_ksi(Z[0])
            ikn.kirjoita_tekstilaatikkoon(KLIITTYMÄ["laskentatulokset"], "Komp: {}, Arvo: {:.3f}{}Ω < {:.3f}°".format(
                komp, tulostus[0], tulostus[1], math.degrees(Z[1])))

            # Itseisarvojen laskutoimitukset jännite- ja virtalaskuihin
            imp = abs(imp)
            kompimp.append(imp)
            haaranimp = imp + haaranimp

        haarojenImp.append(haaranimp)
        jannitelaskuri(i, kompimp, haaranimp)

    piirinVirta(haarojenImp)


def jannitelaskuri(haara, kompZ, kokZ):
    """
    Komponenttien jännitteiden ja virran laskeminen.
    """
    ikn.kirjoita_tekstilaatikkoon(
        KLIITTYMÄ["laskentatulokset"], "\nhaaran {} komponenttien jännitteet:".format(haara))
    for i, Z in enumerate(kompZ):
        jannite = Z * (KLIITTYMÄ["jannite"] / kokZ)
        tulostus = sim.Si_ksi(jannite)
        ikn.kirjoita_tekstilaatikkoon(KLIITTYMÄ["laskentatulokset"], "Komponentti: {}, Jännite: {:.3f}{}V".format(
            KLIITTYMÄ["komponentit"][haara][i][0], tulostus[0], tulostus[1]))


def piirinVirta(imp):
    """
    Laskee piirin virran.
    """
    I = 0
    if len(imp) == 1 and imp[0] != 0:
        I = KLIITTYMÄ["jannite"] / imp[0]
    elif imp[0] == 0:
        I = "ääretön"
    else:
        for Z in imp:
            I = I + 1/Z
        I = I ** -1

    try:
        tulostus = sim.Si_ksi(I)
        ikn.kirjoita_tekstilaatikkoon(
            KLIITTYMÄ["laskentatulokset"], "\nVirtapiirin virta: {:.3f}{}A".format(tulostus[0], tulostus[1]))
    except:
        ikn.kirjoita_tekstilaatikkoon(
            KLIITTYMÄ["laskentatulokset"], "\nVirtaa ei voida laskea")


# Käyttöliittymät
def wizard():
    """
    Funktio, jolla lähdetään kysymään piirtämiseen tarvittavat arvot.
    Funktio jatkuu Komponenttien lisäämiseen uudella funktiolla.
    """
    KLIITTYMÄ["wizAk"] = ikn.luo_ali_ikkuna("Wizard")
    # Jännite:
    ikn.luo_tekstirivi(KLIITTYMÄ["wizAk"], "Anna jännite ilman yksikköä:")
    KLIITTYMÄ["syote"[0]] = ikn.luo_tekstikentta(KLIITTYMÄ["wizAk"])
    ikn.luo_nappi(KLIITTYMÄ["wizAk"], "Aseta jännite", asetaJannite)

    ikn.luo_vaakaerotin(KLIITTYMÄ["wizAk"])
    # Taajuus:
    ikn.luo_tekstirivi(KLIITTYMÄ["wizAk"], "Anna taajuus ilman yksikköä:")
    KLIITTYMÄ["syote"[1]] = ikn.luo_tekstikentta(KLIITTYMÄ["wizAk"])
    ikn.luo_nappi(KLIITTYMÄ["wizAk"], "Aseta taajuus", asetaTaajuus)

    ikn.luo_vaakaerotin(KLIITTYMÄ["wizAk"])
    ikn.luo_nappi(KLIITTYMÄ["wizAk"], "Seuraava", lisaaKomponenttiKL)


def lisaaKomponenttiKL():
    """
    Komponentin lisäys listaan.
    """

    ikn.piilota_ali_ikkuna(KLIITTYMÄ["wizAk"])

    lisaaKompAkkuna = ikn.luo_ali_ikkuna("Lisää komponentti")
    ikn.luo_tekstirivi(
        lisaaKompAkkuna, "Lisää komponentti (v)astus = (r), (k)ela = (l) tai (c)ondensaattori.")
    KLIITTYMÄ["syote"[0]] = ikn.luo_tekstikentta(lisaaKompAkkuna)

    ikn.luo_vaakaerotin(lisaaKompAkkuna)
    ikn.luo_tekstirivi(
        lisaaKompAkkuna, "Anna komponentin arvo ilman yksikköä:")
    KLIITTYMÄ["syote"[1]] = ikn.luo_tekstikentta(lisaaKompAkkuna)

    ikn.luo_vaakaerotin(lisaaKompAkkuna)
    ikn.luo_tekstirivi(lisaaKompAkkuna, "Anna lisättävän haaran ID (numero):")
    KLIITTYMÄ["syote"[2]] = ikn.luo_tekstikentta(lisaaKompAkkuna)

    ikn.luo_nappi(lisaaKompAkkuna, "Lisää komponentti", lisaaKomponentti)

    ikn.luo_vaakaerotin(lisaaKompAkkuna)
    ikn.luo_tekstirivi(lisaaKompAkkuna, "Komponentit:")
    KLIITTYMÄ["komplistaus"] = ikn.luo_tekstilaatikko(
        lisaaKompAkkuna, leveys=40)

    if KLIITTYMÄ["komponentit"] != [[]]:
        komponenttilistaus()


# Pääohjelman nappifunktiot
def tyhjaaLogi():
    """
    Tyhjää logilaatikon.
    """
    ikn.kirjoita_tekstilaatikkoon(KLIITTYMÄ["logi"], "", True)


def tyhjaaLaskut():
    """
    Tyhjää laskut laatikon.
    """
    ikn.kirjoita_tekstilaatikkoon(KLIITTYMÄ["laskentatulokset"], "", True)


def nollaus():
    """
    Palauttaa arvot perusarvoihin.
    """
    KLIITTYMÄ["komponentit"] = [[]]
    KLIITTYMÄ["jannite"] = 0
    KLIITTYMÄ["taajuus"] = 0
    tyhjaaLaskut()
    tyhjaaLogi()
    piiristo.tyhjaa_piiri(KLIITTYMÄ["piirikuva"])


# Pääohjelma
if __name__ == "__main__":
    akkuna = ikn.luo_ikkuna("Piiri pieni pyörii")
    kehysK = ikn.luo_kehys(akkuna)
    kehysO = ikn.luo_kehys(akkuna)

    KLIITTYMÄ["piirikuva"] = piiristo.luo_piiri(kehysK)

    ikn.luo_nappi(kehysO, "Aloita piirtäminen", wizard)
    ikn.luo_tekstirivi(kehysO, "Jännite/Taajuuslogi:")
    KLIITTYMÄ["logi"] = ikn.luo_tekstilaatikko(kehysO, leveys=40, korkeus=4)
    ikn.luo_nappi(kehysO, "Tyhjää logi", tyhjaaLogi)
    ikn.luo_tekstirivi(kehysO, "Laskentatulokset:")
    KLIITTYMÄ["laskentatulokset"] = ikn.luo_tekstilaatikko(
        kehysO, leveys=40, korkeus=10)
    ikn.luo_nappi(kehysO, "Tyhjää laskelmat", tyhjaaLaskut)
    ikn.luo_nappi(kehysO, "Nollaa arvot", nollaus)
    ikn.luo_nappi(kehysO, "Lopeta", ikn.lopeta)

    wizard()  # Avataan Wizard automaattisesti
    ikn.kaynnista()