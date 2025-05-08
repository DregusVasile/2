import hashlib

# Hash-ul parolei reale
TARGET_HASH = "0e000d61c1735636f56154f30046be93b3d71f1abbac3cd9e3f80093fdb357ad"


# Funcția care calculează hash-ul unei parole
def get_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Seturile de caractere disponibile
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
specials = "!@#$"
lowercase = "abcdefghijklmnopqrstuvwxyz"

# Contorizare apeluri recursive
recursive_calls = 0
found = False


def backtrack(password, count_upper, count_digit, count_special, count_lower):
    global recursive_calls, found

    if found:
        return  # Oprire dacă parola a fost deja găsită

    if len(password) == 6:
        if count_upper == 1 and count_digit == 1 and count_special == 1 and count_lower == 3:
            recursive_calls += 1
            if get_hash(password) == TARGET_HASH:
                print(f"Parola găsită: {password}")
                print(f"Număr apeluri recursive: {recursive_calls}")
                found = True
        return

    recursive_calls += 1

    # Adăugăm fiecare tip de caracter menținând constrângerile
    if count_upper < 1:
        for ch in uppercase:
            backtrack(password + ch, count_upper + 1, count_digit, count_special, count_lower)
    if count_digit < 1:
        for ch in digits:
            backtrack(password + ch, count_upper, count_digit + 1, count_special, count_lower)
    if count_special < 1:
        for ch in specials:
            backtrack(password + ch, count_upper, count_digit, count_special + 1, count_lower)
    if count_lower < 3:
        for ch in lowercase:
            backtrack(password + ch, count_upper, count_digit, count_special, count_lower + 1)


# Inițierea procesului de backtracking
backtrack("", 0, 0, 0, 0)
