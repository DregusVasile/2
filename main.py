import tkinter as tk
from tkinter import messagebox, ttk
from book_form import BookForm
from book_manager import load_books, save_books, generate_id

# Clasa principală a aplicației
class BookCatalogApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Catalog de Cărți")
        self.geometry("600x400")
        self.books = load_books()  # Încărcăm datele din JSON
        self.create_widgets()
        self.populate_list()

    # Creează interfața principală: tabel și butoane
    def create_widgets(self):
        # Tabelul unde se afișează cărțile
        self.tree = ttk.Treeview(self, columns=("Titlu", "Autor", "An", "Gen"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Butoane CRUD
        btn_frame = tk.Frame(self)
        btn_frame.pack()

        tk.Button(btn_frame, text="Adaugă", command=self.add_book).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editează", command=self.edit_book).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Șterge", command=self.delete_book).grid(row=0, column=2, padx=5)

    # Populează lista de cărți în tabel
    def populate_list(self):
        self.tree.delete(*self.tree.get_children())  # Curățăm vechile rânduri
        for book in self.books:
            self.tree.insert("", tk.END, iid=book["id"], values=(book["titlu"], book["autor"], book["an"], book["gen"]))

    # Deschide formularul pentru adăugarea unei cărți
    def add_book(self):
        def save(new_book):
            new_book["id"] = generate_id(self.books)
            self.books.append(new_book)
            save_books(self.books)
            self.populate_list()

        BookForm(self, on_save=save)

    # Deschide formularul pentru editarea unei cărți existente
    def edit_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selectează", "Selectează o carte.")
            return
        book_id = int(selected[0])
        book = next((b for b in self.books if b["id"] == book_id), None)

        def save(updated_book):
            for i, b in enumerate(self.books):
                if b["id"] == updated_book["id"]:
                    self.books[i] = updated_book
                    break
            save_books(self.books)
            self.populate_list()

        BookForm(self, book=book, on_save=save)

    # Șterge o carte selectată
    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selectează", "Selectează o carte.")
            return
        book_id = int(selected[0])
        confirm = messagebox.askyesno("Confirmare", "Ești sigur că vrei să ștergi cartea?")
        if confirm:
            self.books = [b for b in self.books if b["id"] != book_id]
            save_books(self.books)
            self.populate_list()

# Rulează aplicația
if __name__ == "__main__":
    app = BookCatalogApp()
    app.mainloop()


















book_manager.py

import json
import os

# Calea către directorul și fișierul unde salvăm datele
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "books.json")

# Funcția încarcă toate cărțile din fișierul JSON
def load_books():
    if not os.path.exists(DATA_FILE):
        return []  # Dacă fișierul nu există, returnează o listă goală
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)  # Deserializare JSON → listă de dicționare

# Funcția salvează lista de cărți în fișierul JSON
def save_books(books):
    os.makedirs(DATA_DIR, exist_ok=True)  # Creează folderul dacă nu există
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)  # Scrie frumos în fișier

# Generează un ID unic pentru fiecare carte nouă
def generate_id(books):
    return max([book["id"] for book in books], default=0) + 1









book_form.py


import tkinter as tk
from tkinter import messagebox

class BookForm(tk.Toplevel):
    def __init__(self, master, book=None, on_save=None):
        super().__init__(master)
        self.title("Formular Carte")
        self.on_save = on_save
        self.book = book

        # Creăm label-urile și entry-urile pentru fiecare câmp
        tk.Label(self, text="Titlu:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_title = tk.Entry(self)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Autor:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_author = tk.Entry(self)
        self.entry_author.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="An:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        vcmd = (self.register(self.validate_year), '%P')
        self.entry_year = tk.Entry(self, validate="key", validatecommand=vcmd)
        self.entry_year.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Gen:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.entry_gen = tk.Entry(self)
        self.entry_gen.grid(row=3, column=1, padx=5, pady=5)

        # Dacă edităm o carte, completăm câmpurile
        if book:
            self.entry_title.insert(0, book["titlu"])
            self.entry_author.insert(0, book["autor"])
            self.entry_year.insert(0, str(book["an"]))
            self.entry_gen.insert(0, book["gen"])

        # Butonul de salvare
        btn_save = tk.Button(self, text="Salvează", command=self.save)
        btn_save.grid(row=4, column=0, columnspan=2, pady=10)

    def validate_year(self, new_value):
        if new_value == "":
            return True  # Permite gol pentru ștergere
        if new_value.isdigit():
            val = int(new_value)
            if 0 <= val <= 2025:  # Permite anul 0 până la 2025
                return True
        return False

    def save(self):
        # Verificăm validitatea anului și celelalte câmpuri
        try:
            an = int(self.entry_year.get())
            if an < 0 or an > 2025:
                messagebox.showerror("Eroare", "Anul trebuie să fie între 0 și 2025.")
                return
        except ValueError:
            messagebox.showerror("Eroare", "Anul trebuie să fie un număr întreg.")
            return

        titlu = self.entry_title.get().strip()
        autor = self.entry_author.get().strip()
        gen = self.entry_gen.get().strip()

        if not titlu or not autor or not gen:
            messagebox.showerror("Eroare", "Toate câmpurile trebuie completate.")
            return

        new_book = {
            "titlu": titlu,
            "autor": autor,
            "an": an,
            "gen": gen,
        }

        if self.book:  # Dacă edităm, păstrăm ID-ul
            new_book["id"] = self.book["id"]

        if self.on_save:
            self.on_save(new_book)

        self.destroy()



books.json

[]
