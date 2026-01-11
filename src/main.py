import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from hrac import Hrac_Repository
from klub import Klub_Repository
from liga import LigaRepository
from majitel import Majitel_Repository
from prestup import Prestup_Repository


class FotbalovyTrhAplikace:
    def __init__(self, koren):
        self.koren = koren
        self.koren.title("Fotbalový trh - Administrace")
        self.koren.geometry("900x700")

        self.repo_hrac = Hrac_Repository()
        self.repo_klub = Klub_Repository()
        self.repo_liga = LigaRepository()
        self.repo_majitel = Majitel_Repository()
        self.repo_prestup = Prestup_Repository()

        self.zapisnik = ttk.Notebook(koren)
        self.zapisnik.pack(expand=True, fill="both")

        self.nastavit_zalozku_prestupu()
        self.nastavit_zalozku_hracu()
        self.nastavit_zalozku_klubu()
        self.nastavit_zalozku_ligy()
        self.nastavit_zalozku_majitelu()
        self.nastavit_zalozku_importu()

    def vytvorit_vystupni_okno(self, rodic):
        textova_oblast = tk.Text(rodic, height=15, state='disabled', bg="#f0f0f0")
        textova_oblast.pack(padx=10, pady=10, fill="both", expand=True)
        return textova_oblast

    def zapsat_do_vystupu(self, textova_oblast, data):
        textova_oblast.config(state='normal')
        textova_oblast.delete("1.0", tk.END)
        if data:
            for radek in data:
                textova_oblast.insert(tk.END, str(radek) + "\n")
        else:
            textova_oblast.insert(tk.END, "Žádná data k zobrazení.")
        textova_oblast.config(state='disabled')

    def bezpecne_spusteni(self, funkce, *args):
        try:
            funkce(*args)
        except Exception as e:
            messagebox.showinfo("Chyba", f"{e}")

    def nastavit_zalozku_prestupu(self):
        zalozka = ttk.Frame(self.zapisnik)
        self.zapisnik.add(zalozka, text="Přestupy")

        ramecek = ttk.Frame(zalozka)
        ramecek.pack(pady=10)

        ttk.Label(ramecek, text="Hráč ID:").grid(row=0, column=0)
        vstup_hrac = ttk.Entry(ramecek)
        vstup_hrac.grid(row=0, column=1, padx=5)

        ttk.Label(ramecek, text="Kupující Klub ID:").grid(row=0, column=2)
        vstup_klub = ttk.Entry(ramecek)
        vstup_klub.grid(row=0, column=3, padx=5)

        ttk.Label(ramecek, text="Cena:").grid(row=0, column=4)
        vstup_cena = ttk.Entry(ramecek)
        vstup_cena.grid(row=0, column=5, padx=5)

        vystup = self.vytvorit_vystupni_okno(zalozka)

        def pridat():
            try:
                self.repo_prestup.pridat(vstup_hrac.get(), vstup_klub.get(), vstup_cena.get())
                self.zapsat_do_vystupu(vystup, self.repo_prestup.seznam_prestupu())
                messagebox.showinfo("Úspěch", "Přestup přidán")
            except Exception as e:
                messagebox.showerror("Chyba", f"Nastala chyba: {e}")

        ttk.Button(ramecek, text="Provést přestup", command= lambda: self.bezpecne_spusteni(pridat)).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(ramecek, text="Seznam přestupů",command=lambda: self.bezpecne_spusteni(lambda: self.zapsat_do_vystupu(vystup, self.repo_prestup.seznam_prestupu()))).grid(row=1,column=2,columnspan=2)

    def nastavit_zalozku_hracu(self):
        zalozka = ttk.Frame(self.zapisnik)
        self.zapisnik.add(zalozka, text="Hráči")

        f = ttk.Frame(zalozka)
        f.pack(pady=10)
        popisky = ["Jméno", "Příjmení", "Číslo dresu", "Pozice", "Klub ID"]
        vstupy = []
        for i, text in enumerate(popisky):
            ttk.Label(f, text=text).grid(row=0, column=i)
            e = ttk.Entry(f, width=12)
            e.grid(row=1, column=i, padx=2)
            vstupy.append(e)

        vystup = self.vytvorit_vystupni_okno(zalozka)

        def nacti(): self.zapsat_do_vystupu(vystup, self.repo_hrac.seznam_hracu())

        ttk.Button(f, text="Přidat", command=lambda: self.bezpecne_spusteni(lambda: [self.repo_hrac.pridat(vstupy[0].get(), vstupy[1].get(), vstupy[2].get(), vstupy[3].get(), vstupy[4].get()),nacti()])).grid(row=2, column=0)
        ttk.Button(f, text="Smazat",command=lambda: self.bezpecne_spusteni(lambda: [self.repo_hrac.smazat(vstupy[0].get(), vstupy[1].get()), nacti()])).grid(row=2,column=1)
        ttk.Button(f, text="Seznam hráčů", command=lambda: self.bezpecne_spusteni(nacti)).grid(row=2, column=2)

    def nastavit_zalozku_klubu(self):
        zalozka = ttk.Frame(self.zapisnik)
        self.zapisnik.add(zalozka, text="Kluby")
        f = ttk.Frame(zalozka)
        f.pack(pady=10)

        ttk.Label(f, text="Název:").grid(row=0, column=0)
        vstup_nazev = ttk.Entry(f)
        vstup_nazev.grid(row=0, column=1)
        ttk.Label(f, text="Liga ID:").grid(row=0, column=2)
        vstup_liga = ttk.Entry(f)
        vstup_liga.grid(row=0, column=3)
        ttk.Label(f, text="Majitel ID:").grid(row=0, column=4)
        vstup_majitel = ttk.Entry(f)
        vstup_majitel.grid(row=0, column=5)

        vystup = self.vytvorit_vystupni_okno(zalozka)

        def nacti(): self.zapsat_do_vystupu(vystup, self.repo_klub.seznam_klubu())

        ttk.Button(f, text="Přidat",command=lambda: self.bezpecne_spusteni(lambda: [self.repo_klub.pridat(vstup_nazev.get(), vstup_liga.get(), vstup_majitel.get()),nacti()])).grid(row=1, column=0)
        ttk.Button(f, text="Smazat", command=lambda: self.bezpecne_spusteni(lambda: [self.repo_klub.smazat(vstup_nazev.get()), nacti()])).grid(row=1,column=1)
        ttk.Button(f, text="Seznam klubů", command=lambda: self.bezpecne_spusteni(nacti)).grid(row=1, column=2)

    def nastavit_zalozku_ligy(self):
        zalozka = ttk.Frame(self.zapisnik)
        self.zapisnik.add(zalozka, text="Ligy")
        f = ttk.Frame(zalozka)
        f.pack(pady=10)

        ttk.Label(f, text="Název:").grid(row=0, column=0)
        vstup_nazev = ttk.Entry(f)
        vstup_nazev.grid(row=0, column=1)
        ttk.Label(f, text="Země:").grid(row=0, column=2)
        vstup_zeme = ttk.Entry(f)
        vstup_zeme.grid(row=0, column=3)
        ttk.Label(f, text="Úroveň:").grid(row=0, column=4)
        vstup_uroven = ttk.Entry(f)
        vstup_uroven.grid(row=0, column=5)

        vystup = self.vytvorit_vystupni_okno(zalozka)

        def nacti(): self.zapsat_do_vystupu(vystup, self.repo_liga.seznam_lig())

        ttk.Button(f, text="Přidat",command=lambda: self.bezpecne_spusteni(lambda: [self.repo_liga.pridat(vstup_nazev.get(), vstup_zeme.get(), vstup_uroven.get()),nacti()])).grid(row=1, column=0)
        ttk.Button(f, text="Smazat", command=lambda: self.bezpecne_spusteni(lambda: [self.repo_liga.smazat(vstup_nazev.get()), nacti()])).grid(row=1,column=1)
        ttk.Button(f, text="Seznam lig", command=lambda: self.bezpecne_spusteni(nacti)).grid(row=1, column=2)

    def nastavit_zalozku_majitelu(self):
        zalozka = ttk.Frame(self.zapisnik)
        self.zapisnik.add(zalozka, text="Majitelé")
        f = ttk.Frame(zalozka)
        f.pack(pady=10)

        popisky = ["Jméno", "Příjmení", "Email", "Rozpočet", "Aktivní(1/0)"]
        vstupy = []
        for i, text in enumerate(popisky):
            ttk.Label(f, text=text).grid(row=0, column=i)
            e = ttk.Entry(f, width=12)
            e.grid(row=1, column=i)
            vstupy.append(e)

        vystup = self.vytvorit_vystupni_okno(zalozka)

        def nacti(): self.zapsat_do_vystupu(vystup, self.repo_majitel.aktivni_majitele())

        ttk.Button(f, text="Přidat", command=lambda: self.bezpecne_spusteni(lambda: [self.repo_majitel.pridat(vstupy[0].get(), vstupy[1].get(), vstupy[2].get(), vstupy[3].get(),vstupy[4].get()), nacti()])).grid(row=2, column=0)
        ttk.Button(f, text="Smazat",command=lambda: self.bezpecne_spusteni(lambda: [self.repo_majitel.smazat(vstupy[0].get(), vstupy[1].get()), nacti()])).grid(row=2,column=1)
        ttk.Button(f, text="Sezna aktivních majitelů", command=lambda: self.bezpecne_spusteni(nacti)).grid(row=2, column=2)

    def nastavit_zalozku_importu(self):
        zalozka = ttk.Frame(self.zapisnik)
        self.zapisnik.add(zalozka, text="Import")

        f = ttk.Frame(zalozka)
        f.pack(pady=50)
        self.popisek_cesty = ttk.Label(f, text="Soubor nevybrán", foreground="red")
        self.popisek_cesty.pack(pady=10)

        def vybrat_soubor():
            nazev_souboru = filedialog.askopenfilename(filetypes=[("CSV soubory", "*.csv")])
            if nazev_souboru:
                self.vybrana_cesta = nazev_souboru
                self.popisek_cesty.config(text=nazev_souboru, foreground="green")

        ttk.Button(f, text="Vybrat CSV soubor", command=lambda: self.bezpecne_spusteni(vybrat_soubor)).pack(pady=5)

        ttk.Label(f, text="Vyberte typ importu:").pack(pady=10)
        vyber = ttk.Combobox(f, values=["Hráči", "Kluby", "Ligy", "Majitelé"], state="readonly")
        vyber.pack(pady=5)

        def spustit():
            cesta = getattr(self, 'vybrana_cesta', None)
            if not cesta:
                messagebox.showwarning("Chyba", "Nejdříve vyberte soubor!")
                return

            typ = vyber.get()
            try:
                if typ == "Hráči":
                    self.repo_hrac.import_z_csv(cesta)
                elif typ == "Kluby":
                    self.repo_klub.import_z_csv(cesta)
                elif typ == "Ligy":
                    self.repo_liga.import_z_csv(cesta)
                elif typ == "Majitelé":
                    self.repo_majitel.import_z_csv(cesta)
                messagebox.showinfo("Hotovo", f"Import {typ} proběhl úspěšně.")
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodařilo se importovat: {e}")

        ttk.Button(f, text="Spustit import", command=lambda: self.bezpecne_spusteni(spustit)).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    aplikace = FotbalovyTrhAplikace(root)
    root.mainloop()