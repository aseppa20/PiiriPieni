"""
SI-järjestelmän muunnokset by. Aleksanteri Seppä
"""

# SI järjestelmän kerrannaisyksiköt
SIK = {
    "Y": 24,
    "Z": 21,
    "E": 18,
    "P": 15,
    "T": 12,
    "G": 9,
    "M": 6,
    "k": 3,
    "m": -3,
    "u": -6,
    "μ": -6,
    "n": -9,
    "p": -12,
    "f": -15,
    "z": -21,
    "y": -24
}


def muunnaSi(muunnettava):
    """
    Muuttaa annetun luvun ja mahdollisen kerrannaisyksikön vastaavaksi liukuluvuksi.
    Palauttaa arvon None jos luku ei ole kelvollinen.
    """
    # Otetaan muunnettavan viimeinen merkki ja katsotaan onko se numero vai mikä
    muunnettava = muunnettava.strip()
    yksikko = muunnettava[-1]
    try:
        int(yksikko)
    except ValueError:
        try:
            kasittelija = float(muunnettava[:-1])
        except ValueError:
            return None
        if yksikko in SIK:
            return float(kasittelija) * 10 ** SIK[yksikko]
        return None

    return float(muunnettava)


def Si_ksi(muunnettava):
    """
    Muuttaa annetun luvun SI kerrannaisyksikön muotoon. Jos ei luku,
    palauttaa annetus tekstin takaisin.

    Palauttaa arvot tuplana (arvo, yksikkö)
    """
    sik_ker = 0
    
    #Seuraava pätkä saatu täältä (kirjaston kääntö):
    #https://therenegadecoder.com/code/how-to-invert-a-dictionary-in-python/
    sikkaan = dict(map(reversed, SIK.items()))

    try:
        float(muunnettava)    
        while muunnettava < 1 or muunnettava > 1000:
            if muunnettava < 1:
                muunnettava = muunnettava * 1000
                sik_ker -= 3
            elif muunnettava > 1000:
                muunnettava = muunnettava / 1000
                sik_ker += 3
        
        if sik_ker == 0:
            return (muunnettava, "")
        else:
            palautus = (muunnettava, sikkaan[sik_ker][0])
            return palautus

    except ValueError:
        raise Exception("Annettu arvo ei ollut luku.")
        return (muunnettava, "")

if __name__ == "__main__":
    pass