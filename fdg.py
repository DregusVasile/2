import json
import random

# Încarcă datele din fișierul JSON: bancnote și produse
with open("date.json", "r") as f:
    data = json.load(f)
    # Sortează bancnotele descrescător după valoare, pentru a încerca întâi cele mari
    bancnote = sorted(data["bancnote"], key=lambda x: -x["valoare"])

# Lista de produse disponibile
produse = data["produse"]

# Creează un dicționar cu stocul pentru fiecare bancnotă: {valoare: număr bucăți}
stoc = {b["valoare"]: b["stoc"] for b in bancnote}

# Lista valorilor bancnotelor, folosită pentru procesare
valori = list(stoc.keys())

def rest_optim(sum_rest):
    """
    Calculează o combinație optimă de bancnote pentru a oferi restul sum_rest,
    folosind programare dinamică și respectând stocul disponibil.
    Returnează un dicționar {valoare: număr} sau None dacă nu e posibil.
    """
    # dp[i] va reține combinația optimă de bancnote pentru suma i
    dp = [None] * (sum_rest + 1)
    dp[0] = {}  # Pentru suma 0 nu avem nevoie de nicio bancnotă

    # Iterăm pentru toate sumele de la 1 până la sum_rest
    for s in range(1, sum_rest + 1):
        for val in valori:
            if val <= s and dp[s - val] is not None:
                # Încercăm să formăm suma s din s - val + bancnota de val
                prev_combo = dp[s - val].copy()
                prev_combo[val] = prev_combo.get(val, 0) + 1

                # Verificăm dacă nu depășim stocul disponibil
                if prev_combo[val] <= stoc[val]:
                    # Alegem combinația cu cel mai mic număr total de bancnote
                    if dp[s] is None or sum(prev_combo.values()) < sum(dp[s].values()):
                        dp[s] = prev_combo
    return dp[sum_rest]

# Contor pentru câți clienți au fost serviți
clienti_serviti = 0

# Simulează clienții până când nu se mai poate oferi restul
while True:
    # Alege un produs aleator
    produs = random.choice(produse)
    pret = produs["pret"]

    # Clientul plătește cu o sumă între preț + 1 și preț + 20
    suma_platita = pret + random.randint(1, 20)
    rest = suma_platita - pret

    # Afișează detalii despre tranzacție
    print(f"\nClientul {clienti_serviti + 1}:")
    print(f"  Produs: {produs['nume']}, Preț: {pret} lei")
    print(f"  Suma plătită: {suma_platita} lei")
    print(f"  Rest de oferit: {rest} lei")

    # Calculează cea mai bună combinație de bancnote pentru rest
    solutie = rest_optim(rest)

    if solutie is None:
        # Nu se poate oferi restul cu bancnotele rămase -> simularea se oprește
        print("\n  Nu se poate oferi restul cu bancnotele disponibile. Simularea se oprește.")
        print("  Stoc rămas:")
        for v in valori:
            print(f"    {v} lei: {stoc[v]} bucăți")
        break

    # Afișează bancnotele oferite ca rest
    print("  Rest oferit cu următoarele bancnote:")
    for val in sorted(solutie.keys(), reverse=True):
        print(f"    {val} lei x {solutie[val]}")
        stoc[val] -= solutie[val]  # Actualizează stocul

    clienti_serviti += 1  # Trecem la următorul client













date_casa.json

{
  "bancnote": [
    { "valoare": 50, "stoc": 20 },
    { "valoare": 20, "stoc": 30 },
    { "valoare": 10, "stoc": 40 },
    { "valoare": 5, "stoc": 50 },
    { "valoare": 1, "stoc": 100 }
  ],
  "produse": [
    { "nume": "Lapte", "pret": 7 },
    { "nume": "Paine", "pret": 3 },
    { "nume": "Ciocolata", "pret": 5 },
    { "nume": "Apa", "pret": 2 },
    { "nume": "Cafea", "pret": 9 }
  ]
}
