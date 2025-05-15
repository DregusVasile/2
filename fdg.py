import json
import random

# Încarcă datele din fișierul JSON
with open("date.json", "r") as f:
    data = json.load(f)  # <- asta trebuie indentat cu 4 spații/tab
    bancnote = sorted(data["bancnote"], key=lambda x: -x["valoare"])  # Sortate descrescător


bancnote = sorted(data["bancnote"], key=lambda x: -x["valoare"])  # Sortate descrescător
produse = data["produse"]

# Convertim lista de bancnote într-un dicționar pentru acces rapid
stoc = {b["valoare"]: b["stoc"] for b in bancnote}
valori = list(stoc.keys())

def rest_optim(sum_rest):
    """
    Returnează o combinație optimă de bancnote pentru o sumă dată,
    folosind programare dinamică și ținând cont de stocul disponibil.
    """
    dp = [None] * (sum_rest + 1)
    dp[0] = {}

    for s in range(1, sum_rest + 1):
        for val in valori:
            if val <= s and dp[s - val] is not None:
                prev_combo = dp[s - val].copy()
                prev_combo[val] = prev_combo.get(val, 0) + 1
                if prev_combo[val] <= stoc[val]:
                    if dp[s] is None or sum(prev_combo.values()) < sum(dp[s].values()):
                        dp[s] = prev_combo
    return dp[sum_rest]

clienti_serviti = 0

while True:
    produs = random.choice(produse)
    pret = produs["pret"]
    suma_platita = pret + random.randint(1, 20)
    rest = suma_platita - pret

    print(f"\nClientul {clienti_serviti + 1}:")
    print(f"  Produs: {produs['nume']}, Preț: {pret} lei")
    print(f"  Suma plătită: {suma_platita} lei")
    print(f"  Rest de oferit: {rest} lei")

    solutie = rest_optim(rest)

    if solutie is None:
        print("\n  Nu se poate oferi restul cu bancnotele disponibile. Simularea se oprește.")
        print("  Stoc rămas:")
        for v in valori:
            print(f"    {v} lei: {stoc[v]} bucăți")
        break

    print("  Rest oferit cu următoarele bancnote:")
    for val in sorted(solutie.keys(), reverse=True):
        print(f"    {val} lei x {solutie[val]}")
        stoc[val] -= solutie[val]

    clienti_serviti += 1
