import os
import json
import csv

RAPPORT_TXT = "treff_rapport.txt"
RAPPORT_CSV = "treff_rapport.csv"


def finn_fil(filnavn):
    # 1. Sjekk direkte (full sti)
    if os.path.exists(filnavn):
        return filnavn

    # 2. Sjekk i samme mappe som scriptet
    script_mappe = os.path.dirname(os.path.abspath(__file__))
    kandidat = os.path.join(script_mappe, filnavn)

    if os.path.exists(kandidat):
        return kandidat

    return None


def les_sokeord(filnavn):
    sti = finn_fil(filnavn)

    if not sti:
        print("Finner ikke søkeordfil:", filnavn)
        return []

    with open(sti, "r", encoding="utf-8") as fil:
        return [
            linje.strip().lower()
            for linje in fil
            if linje.strip() and not linje.strip().startswith("#")
        ]


def les_json(filsti):
    try:
        with open(filsti, "r", encoding="utf-8") as f:
            return json.load(f)
    except UnicodeDecodeError:
        with open(filsti, "r", encoding="latin-1") as f:
            return json.load(f)
    except Exception as e:
        print("Kunne ikke lese:", filsti, e)
        return None


def finn_json_filer(mappe):
    return [
        os.path.join(mappe, f)
        for f in os.listdir(mappe)
        if f.lower().endswith(".json")
    ]


def finn_treff(data, filsti, sokeord):
    treff = []

    tekst = json.dumps(data, ensure_ascii=False).lower()

    for ordet in sokeord:
        if ordet in tekst:
            treff.append({
                "fil": filsti,
                "ord": ordet,
                "utdrag": tekst[:3000]
            })

    return treff


def skriv_txt(treff):
    with open(RAPPORT_TXT, "w", encoding="utf-8") as f:
        for t in treff:
            f.write("=" * 80 + "\n")
            f.write(f"Fil: {t['fil']}\n")
            f.write(f"Treff på ord: {t['ord']}\n")
            f.write("Utdrag:\n")
            f.write(t["utdrag"] + "\n\n")


def skriv_csv(treff):
    with open(RAPPORT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        felter = ["fil", "ord", "utdrag"]
        writer = csv.DictWriter(f, fieldnames=felter, delimiter=";")
        writer.writeheader()
        writer.writerows(treff)


def main():
    print("Messenger tekstsøk\n")

    mappe = input("Mappe med JSON-filer: ").strip().strip('"')
    sokefil = input("Fil med søkeord (Enter = sokeord.txt): ").strip().strip('"')

    if sokefil == "":
        sokefil = "sokeord.txt"

    if not os.path.exists(mappe):
        print("Finner ikke mappen:", mappe)
        return

    sokeord = les_sokeord(sokefil)

    if not sokeord:
        print("Ingen søkeord funnet.")
        return

    json_filer = finn_json_filer(mappe)

    print("\nStarter søk...")
    print("Antall søkeord:", len(sokeord))
    print("Antall JSON-filer:", len(json_filer), "\n")

    alle_treff = []

    for nr, filsti in enumerate(json_filer, 1):
        print(f"Sjekker {nr}/{len(json_filer)}: {os.path.basename(filsti)}")

        data = les_json(filsti)
        if data is None:
            continue

        treff = finn_treff(data, filsti, sokeord)
        alle_treff.extend(treff)

    if not alle_treff:
        print("\nIngen treff funnet.")
        return

    skriv_txt(alle_treff)
    skriv_csv(alle_treff)

    print("\nFerdig")
    print("Treff:", len(alle_treff))
    print("TXT:", RAPPORT_TXT)
    print("CSV:", RAPPORT_CSV)


if __name__ == "__main__":
    main()