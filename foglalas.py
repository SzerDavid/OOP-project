from abc import ABC, abstractmethod
from datetime import date, timedelta

# Absztrakt Szoba osztály
class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

# EgyágyasSzoba
class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 5000)  # például 5000 forint / éj

# KétagyasSzoba
class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 8000)  # például 8000 forint / éj

# Szálloda osztály
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
        return "Nem található ilyen foglalás!"
    
    def foglalasok_listazasa(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return "\n".join(f"Foglalás: Szobaszám: {f.szobaszam}, Dátum: {f.datum}" for f in self.foglalasok)

# Foglalás osztály
class Foglalas:
    def __init__(self, szobaszam, datum):
        self.szobaszam = szobaszam
        self.datum = datum

# Felhasználói interfész
def felhasznaloi_interfesz():
    szalloda = Szalloda("Szentesi Agrár Üdülőcske")
    # Hozzáadunk 3 szobát a szállodához (2 egyágyas és 1 kétagyas)
    szalloda.szoba_hozzaadas(EgyagyasSzoba(101))
    szalloda.szoba_hozzaadas(EgyagyasSzoba(102))
    szalloda.szoba_hozzaadas(KetagyasSzoba(103))
    
    # Automatikus foglalások hozzáadása
    ma = date.today()
    szalloda.foglalas(101, ma + timedelta(days=2))
    szalloda.foglalas(102, ma + timedelta(days=3))
    szalloda.foglalas(103, ma + timedelta(days=4))
    szalloda.foglalas(101, ma + timedelta(days=5))
    szalloda.foglalas(102, ma + timedelta(days=6))
    
    while True:
        print(f"\nÜdvözöljük a {szalloda.nev} szobafoglaló rendszerében!")
        print("\nVálasszon az alábbi műveletek közül:")
        print("1. Szoba foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasztas = input("Adja meg a választott művelet számát: ")
        
        if valasztas == "1":
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
        elif valasztas == "4":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen választás. Próbálja újra!")

felhasznaloi_interfesz()