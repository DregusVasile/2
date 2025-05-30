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

# Clasa care definește o fereastră (Toplevel) pentru adăugarea sau editarea unei cărți
class BookForm(tk.Toplevel):
    def __init__(self, parent, book=None, on_save=None):
        super().__init__(parent)
        self.title("Formular Carte")
        self.geometry("300x250")
        self.book = book          # Dacă primim o carte, e o editare
        self.on_save = on_save    # Funcția de apelat când salvăm
        self.create_widgets()
        if book:
            self.fill_form()

    # Creează câmpurile formularului (Titlu, Autor, An, Gen)
    def create_widgets(self):
        self.entries = {}
        fields = ["Titlu", "Autor", "An", "Gen"]
        for i, field in enumerate(fields):
            tk.Label(self, text=field).grid(row=i, column=0, pady=5, sticky="w")
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, pady=5)
            self.entries[field.lower()] = entry  # Salvăm referința la Entry

        tk.Button(self, text="Salvează", command=self.save).grid(row=5, column=0, columnspan=2, pady=10)

    # Dacă edităm o carte, pre-umplem câmpurile
    def fill_form(self):
        self.entries["titlu"].insert(0, self.book["titlu"])
        self.entries["autor"].insert(0, self.book["autor"])
        self.entries["an"].insert(0, self.book["an"])
        self.entries["gen"].insert(0, self.book["gen"])

    # Salvează datele introduse în formular
    def save(self):
        try:
            new_data = {
                "titlu": self.entries["titlu"].get(),
                "autor": self.entries["autor"].get(),
                "an": int(self.entries["an"].get()),  # Anul trebuie să fie numeric
                "gen": self.entries["gen"].get()
            }

            if self.book:
                new_data["id"] = self.book["id"]  # Dacă e editare, păstrăm ID-ul

            if self.on_save:
                self.on_save(new_data)  # Apelăm funcția care actualizează lista principală
            self.destroy()  # Închidem formularul
        except ValueError:
            messagebox.showerror("Eroare", "Anul trebuie să fie un număr.")


books.json

[]
