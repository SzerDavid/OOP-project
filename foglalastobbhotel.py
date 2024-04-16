from abc import ABC, abstractmethod
from datetime import date, timedelta

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 5000)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 8000)

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []
    
    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)
    
    def foglalas(self, szobaszam, datum):
        if datum <= date.today():
            return "A dátum érvénytelen. Kérjük, jövőbeli dátumot adjon meg!"
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                if any(f.szobaszam == szobaszam and f.datum == datum for f in self.foglalasok):
                    return "Ez a szoba már foglalt ezen a napon!"
                self.foglalasok.append(Foglalas(szobaszam, datum))
                return f"Foglalás létrehozva! Ár: {szoba.ar} Ft"
        return "Nem található ilyen szobaszám!"
    
    def foglalas_lemondas(self, szobaszam, datum):
        for f in self.foglalasok:
            if f.szobaszam == szobaszam and f.datum == datum:
                self.foglalasok.remove(f)
                return "Foglalás lemondva!"
    
    def foglalasok_listazasa(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return "\n".join(f"Foglalás: Szobaszám: {f.szobaszam}, Dátum: {f.datum}" for f in self.foglalasok)

class Foglalas:
    def __init__(self, szobaszam, datum):
        self.szobaszam = szobaszam
        self.datum = datum

class SzallodaMenedzser:
    def __init__(self):
        self.szallodak = []

    def szalloda_hozzaadas(self, szalloda):
        self.szallodak.append(szalloda)

    def szalloda_kivalasztas(self):
        while True:
            print("\nElérhető szállodák:")
            for index, szalloda in enumerate(self.szallodak):
                print(f"{index + 1}. {szalloda.nev}")
            print(f"{len(self.szallodak) + 1}. Kilépés")
            valasztas = int(input("Válasszon szállodát vagy lépjen ki (szám): "))
            if valasztas == len(self.szallodak) + 1:
                print("Kilépés...")
                return None  # Kilépés
            elif 1 <= valasztas <= len(self.szallodak):
                return self.szallodak[valasztas - 1]
            else:
                print("Érvénytelen választás. Próbálja újra.")

def kezdo_adatok_feltoltese(szalloda, szobak, foglalasok):
    for szoba in szobak:
        if szoba[1] == 'egyagyas':
            szalloda.szoba_hozzaadas(EgyagyasSzoba(szoba[0]))
        elif szoba[1] == 'ketagyas':
            szalloda.szoba_hozzaadas(KetagyasSzoba(szoba[0]))

    ma = date.today()
    for foglalas in foglalasok:
        szalloda.foglalas(foglalas[0], ma + timedelta(days=foglalas[1]))

def felhasznaloi_interfesz():
    menedzser = SzallodaMenedzser()
    szalloda1 = Szalloda("Szentesi Agrár Üdülőcske")
    szalloda2 = Szalloda("Budapesti Kényelem Szálloda")

    # Kezdeti adatok különbözőek minden szállodához
    kezdo_adatok_feltoltese(szalloda1, [(101, 'egyagyas'), (102, 'egyagyas'), (103, 'ketagyas')],
                           [(101, 2), (102, 3), (103, 5), (102, 8), (103, 9)])
    kezdo_adatok_feltoltese(szalloda2, [(201, 'egyagyas'), (202, 'ketagyas'), (203, 'ketagyas')],
                           [(201, 1), (202, 2), (203, 3), (202, 4), (201, 6)])

    menedzser.szalloda_hozzaadas(szalloda1)
    menedzser.szalloda_hozzaadas(szalloda2)

    while True:
        szalloda = menedzser.szalloda_kivalasztas()
        if szalloda is None:
            break  # Kilépés a programból

        while True:
            print(f"\nÜdvözöljük a {szalloda.nev} szobafoglaló rendszerében!")
            print("\nVálasszon az alábbi műveletek közül:")
            print("1. Szoba foglalása")
            print("2. Foglalás lemondása")
            print("3. Foglalások listázása")
            print("4. Vissza a szálloda választóhoz")
            valasztas = input("Adja meg a választott művelet számát: ")

            if valasztas == "4":
                break  # Vissza a szállodaválasztóhoz
            elif valasztas == "1":
                szoba_tipus = input("Válassza ki a szobatípust (1: Egyágyas, 2: Kétagyas): ")
                szobak_listaja = [szoba for szoba in szalloda.szobak if (szoba_tipus == "1" and isinstance(szoba, EgyagyasSzoba)) or (szoba_tipus == "2" and isinstance(szoba, KetagyasSzoba))]
                if not szobak_listaja:
                    print("Nincs elérhető szoba ebben a kategóriában.")
                else:
                    print("Elérhető szobák:")
                    for szoba in szobak_listaja:
                        print(f"Szobaszám: {szoba.szobaszam}, Ár: {szoba.ar} Ft/éj")
                    szobaszam = int(input("Adja meg a kiválasztott szobaszámot: "))
                    datum = input("Adja meg a foglalás dátumát (éééé-hh-nn formátumban): ")
                    try:
                        datum = date.fromisoformat(datum)
                        print(szalloda.foglalas(szobaszam, datum))
                    except ValueError:
                        print("Érvénytelen dátumformátum!")
            elif valasztas == "2":
                szobaszam = int(input("Adja meg a szobaszámot: "))
                datum = input("Adja meg a foglalás dátumát (éééé-hh-nn formátumban): ")
                try:
                    datum = date.fromisoformat(datum)
                    print(szalloda.foglalas_lemondas(szobaszam, datum))
                except ValueError:
                    print("Érvénytelen dátumformátum!")
            elif valasztas == "3":
                print(szalloda.foglalasok_listazasa())
            else:
                print("Érvénytelen választás. Próbálja újra.")

felhasznaloi_interfesz()