

import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox


from storage.storage import Storage
from models_shop.products.product import Product
from models_shop.customers.customer import Customer
from models_shop.customers.private_customer import PrivateCustomer
from models_shop.customers.company_customer import CompanyCustomer
from models_shop.orders.cart import Cart
from models_shop.orders.order import Order
from utils.validator import Validator
from exceptions.shop_error import ShopError


# ----------------------------------------------------------------------
# FARBEN (die grüne "GreenWorld"-Palette)
# ----------------------------------------------------------------------
WHITE = "#FFFFFF"
SOFT = "#F1F1EE"
GREEN_LT = "#CFE0AC"
GREEN_DK = "#445033"
INK = "#1F2419"
GREY = "#8A8A82"

FONT = "Helvetica"

# kategorie kommt from Produktklassen: get_category() liefert
# genau diese Texte ("Electronic" / "Clothing" / "Book").
CATEGORIES = ("All", "Electronic", "Clothing", "Book")


def button(parent, text, command, primary=True):
    # Ein Button im gemeinsamen Stil (grün, wenn primary, sonst hell).
    if primary:
        fill_color = GREEN_DK
        text_color = "white"
    else:
        fill_color = SOFT
        text_color = INK
    return tk.Button(parent, text=text, command=command,
                     bg=fill_color, fg=text_color,
                     font=(FONT, 11, "bold"), relief="flat",
                     activebackground=GREEN_LT, width=22, pady=8, cursor="hand2")


def title(parent, text, size=18):
    return tk.Label(parent, text=text, bg=WHITE, fg=GREEN_DK,
                    font=(FONT, size, "bold"))


# ----------------------------------------------------------------------
# DIE APP: ein Fenster. Um den Bildschirm zu wechseln, löschen wir alles
# und zeichnen den neuen Bildschirm neu.
# ----------------------------------------------------------------------
class ShopApp(tk.Tk):

    def __init__(self, storage=None):
        super().__init__()

        self.title("WarenWelt")
        self.geometry("470x620")
        self.configure(bg=WHITE)

        # --- Daten, die sich die App während der Laufzeit merkt ---
        self.storage = storage
        self.users = {}
        self.current_user = None
        self.cart = None                # HERE IS CART
        self.catalog = self.load_catalog()
        self.active_category = "All"
        self.sort_mode = "none"
        self.shown_products = []

        self.show_login()

    # ==================================================================
    '''DATEN LADEN- FROM MYSQL GELESESN; Product.load all() take automatic Electronic + Clothing + Book '
    without DB connection it will be just empty'''

    def load_catalog(self):

        if self.storage is None:
            return []
        try:
            return Product.load_all(self.storage)  #LOAD ALL
        except Exception:
            return []

    def save_customer(self, customer):
        # Offline-----Kunde nur im Speicher merken.
        if self.storage is None:
            self.users[customer.get_email()] = customer  #Customer.get_email()
            return

        customer.save(self.storage)  # PrivateCustomer.save() / CompanyCustomer.save()

    def find_customer(self, email, password):
        # Login: alle Kunden laden und nach E-Mail + Passwort suchen.
        # (Deine load()-Methode sucht über die id; eine Suche per E-Mail
        #  gibt es nicht, also laden wir alle und vergleichen.)
        if self.storage is None:
            customer = self.users.get(email)
            if customer and customer.get_password() == password:  # Customer.get_password()
                return customer
            return None

        for customer in Customer.load_all(self.storage):  #Customer.load_all()
            if customer.get_email() == email and customer.get_password() == password:  #Customer
                return customer
        return None

    def email_exists(self, email):
        # True, wenn schon ein Kunde diese E-Mail benutzt.
        # Genau das verhindert, dass dieselbe E-Mail zweimal angelegt wird.
        if self.storage is None:
            return email in self.users

        for customer in Customer.load_all(self.storage):  #Customer.load_all()
            if customer.get_email() == email:  # Customer.get_email()
                return True
        return False

    # ==================================================================
    #  Kleine Helfer zum Bauen von Widgets
    # ==================================================================
    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def label(self, text, color=INK, size=10):
        return tk.Label(self, text=text, bg=WHITE, fg=color, font=(FONT, size))

    def entry(self, hide=None):
        return tk.Entry(self, width=30, font=(FONT, 11), bg="white", relief="flat",
                        show=hide or "", highlightthickness=1,
                        highlightbackground=GREEN_LT, highlightcolor=GREEN_DK)

    # ==================================================================
    #  SCREEN 1: LOGIN
    # ==================================================================
    def show_login(self):
        self.clear()

        title(self, "WarenWelt", 24).pack(pady=(28, 2))
        self.label("Shop greener, live better.", GREEN_DK, 11).pack(pady=(0, 18))

        self.label("Email:").pack()
        email_entry = self.entry()
        email_entry.pack(pady=3, ipady=4)

        self.label("Passwort:").pack(pady=(8, 0))
        password_entry = self.entry(hide="*")
        password_entry.pack(pady=3, ipady=4)

        def do_login():
            user = self.find_customer(email_entry.get().strip(),
                                      password_entry.get())
            if user is not None:
                self.current_user = user
                self.cart = Cart(user)  # CART - neuer Warenkorb für den Kunden)
                self.show_shop()
            else:
                messagebox.showerror("Login fehlgeschlagen", "Falsche E-Mail oder falsches Passwort.")

        button(self, "Einloggen", do_login).pack(pady=(16, 6))
        button(self, "Konto erstellen", self.show_register, primary=False).pack()

        # Zeigt an, ob wir mit der Datenbank verbunden sind oder nicht.
        if self.storage is None:
            status = "Offline-Modus (keine Datenbank)"
        else:
            status = "Mit Datenbank verbunden"
        self.label(status, GREY, 9).pack(pady=(18, 0))

    # ==================================================================
    #  SCREEN 2: REGISTRIERUNG
    # ==================================================================
    def show_register(self):
        self.clear()

        title(self, "Konto erstellen", 18).pack(pady=(20, 10))

        customer_type = tk.StringVar(value="private")
        radio_private = tk.Radiobutton(self, text="Privatkunde",
                       variable=customer_type, value="private",
                       bg=WHITE, fg=INK, font=(FONT, 10),
                       selectcolor=GREEN_LT, activebackground=WHITE)
        radio_private.pack()
        radio_company = tk.Radiobutton(self, text="Firmenkunde",
                       variable=customer_type, value="company",
                       bg=WHITE, fg=INK, font=(FONT, 10),
                       selectcolor=GREEN_LT, activebackground=WHITE)
        radio_company.pack()

        def field(text, hide=None):
            self.label(text).pack(pady=(6, 0))
            entry_widget = self.entry(hide=hide)
            entry_widget.pack(pady=2, ipady=3)
            return entry_widget

        entry_name = field("Name:")
        entry_address = field("Adresse:")
        entry_email = field("Email:")
        entry_phone = field("Telefon (8-20 Ziffern):")
        entry_password = field("Passwort (min. 8 Zeichen):", hide="*")

        # Das letzte Feld ändert seine Bedeutung je nach Kundentyp:
        # privat -> Geburtsdatum, Firma -> Firmennummer.
        extra_label = self.label("Geburtsdatum (TT.MM.JJJJ):")
        extra_label.pack(pady=(6, 0))
        entry_extra = self.entry()
        entry_extra.pack(pady=2, ipady=3)

        def update_extra_label():
            if customer_type.get() == "private":
                extra_label.config(text="Geburtsdatum (TT.MM.JJJJ):")
            else:
                extra_label.config(text="Firmennummer (5-15 Ziffern):")

        radio_private.config(command=update_extra_label)
        radio_company.config(command=update_extra_label)
        update_extra_label()

        def do_register():
            name = entry_name.get().strip()
            address = entry_address.get().strip()
            email = entry_email.get().strip()
            phone = entry_phone.get().strip()
            password = entry_password.get()
            extra = entry_extra.get().strip()

            # Schritt 1: E-Mail darf noch nicht vergeben sein.
            if self.email_exists(email):  #Customer.load_all()
                messagebox.showerror("Fehler", "Diese E-Mail wird bereits verwendet.")
                return

            # Schritt 2: das richtige Kunden-Objekt bauen (deine Klassen).
            # Die Validierung passiert AUTOMATISCH in deinen Settern: bei
            # ungültigen Daten wirft die Klasse ein ShopError, das wir hier fangen.
            try:
                if customer_type.get() == "private":
                    customer = PrivateCustomer(name, address, email,  # PrivateCustomer
                                               phone, password, extra)
                else:
                    customer = CompanyCustomer(name, address, email,  # <CompanyCustomer
                                               phone, password, extra)
            except ShopError as error:  #  ShopError (deine Validierungsfehler)
                messagebox.showerror("Fehler", str(error))
                return

            # Schritt 3: speichern (in MySQL, wenn online; sonst im Speicher).
            try:
                self.save_customer(customer)
            except Exception as error:
                messagebox.showerror("Fehler", f"Konto konnte nicht gespeichert werden: {error}")
                return

            messagebox.showinfo("Fertig", "Konto erstellt. Du kannst dich jetzt einloggen.")
            self.show_login()

        button(self, "Registrieren", do_register).pack(pady=(12, 6))
        button(self, "Zurück", self.show_login, primary=False).pack()

    # ==================================================================
    #  SCREEN 3: SHOP (Produkte)
    # ==================================================================
    def show_shop(self):
        self.clear()

        title(self, "Produkte", 18).pack(pady=(16, 8))

        # Keine Produkte (keine DB) -> Hinweis anzeigen.
        if not self.catalog:
            self.label("Keine Produkte (keine Datenbankverbindung).",
                       GREY, 11).pack(pady=20)
            button(self, "Logout", self.logout, primary=False).pack()
            return

        # --- Kategorie-Filter (All / Electronic / Clothing / Book) ---
        filter_row = tk.Frame(self, bg=WHITE)
        filter_row.pack(pady=(0, 6))
        for category_name in CATEGORIES:
            color = GREEN_LT if category_name == self.active_category else SOFT
            tk.Button(filter_row, text=category_name,
                      command=lambda c=category_name: self.filter_by(c),
                      bg=color, fg=INK, font=(FONT, 9, "bold"), relief="flat",
                      activebackground=GREEN_LT, padx=8, pady=4,
                      cursor="hand2").pack(side="left", padx=2)

        # --- Sortier-Buttons (optionaler Teil der Aufgabe) ---
        sort_row = tk.Frame(self, bg=WHITE)
        sort_row.pack(pady=(0, 6))
        self.label("Sortieren:").pack_forget()
        tk.Label(sort_row, text="Sortieren:", bg=WHITE, fg=GREY,
                 font=(FONT, 9)).pack(side="left", padx=(0, 4))
        for sort_name, sort_key in (("Name", "name"), ("Preis", "price")):
            color = GREEN_LT if self.sort_mode == sort_key else SOFT
            tk.Button(sort_row, text=sort_name,
                      command=lambda k=sort_key: self.sort_by(k),
                      bg=color, fg=INK, font=(FONT, 9, "bold"), relief="flat",
                      activebackground=GREEN_LT, padx=8, pady=3,
                      cursor="hand2").pack(side="left", padx=2)

        # Nur die Produkte der gewählten Kategorie behalten.
        # get_category() kommt aus deinen Produktklassen.
        self.shown_products = []
        for product in self.catalog:
            if self.active_category == "All" or product.get_category() == self.active_category:  #  Product.get_category()
                self.shown_products.append(product)

        # Sortieren (optional) nach Name oder Preis -> deine Getter.
        if self.sort_mode == "name":
            self.shown_products.sort(key=lambda p: p.get_name().lower())  #  Product.get_name()
        elif self.sort_mode == "price":
            self.shown_products.sort(key=lambda p: float(p.get_price()))  #  Product.get_price()

        # --- scrollbare Produktliste (Listbox + Scrollbar) ---
        list_frame = tk.Frame(self, bg=WHITE)
        list_frame.pack(pady=5)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        self.listbox = tk.Listbox(list_frame, width=50, height=11, font=(FONT, 10),
                                  bg=SOFT, fg=INK, relief="flat",
                                  selectbackground=GREEN_DK, selectforeground="white",
                                  highlightthickness=1, highlightbackground=GREEN_LT,
                                  yscrollcommand=scrollbar.set)
        self.listbox.pack(side="left")
        scrollbar.config(command=self.listbox.yview)

        # Liste in derselben Reihenfolge wie self.shown_products füllen.
        for product in self.shown_products:
            self.listbox.insert(
                tk.END,
                f"{product.get_name()}  ({product.get_category()})  -  {float(product.get_price()):.2f} EUR")
            #     ^ get_name()        ^ get_category()                ^get_price()

        def add_to_cart():
            selection = self.listbox.curselection()
            if not selection:
                messagebox.showinfo("Info", "Bitte zuerst ein Produkt auswählen.")
                return
            product = self.shown_products[selection[0]]
            self.cart.add_product(product)  # <Cart.add_product()
            messagebox.showinfo("Hinzugefügt", f"'{product.get_name()}' im Warenkorb.")

        button(self, "In den Warenkorb", add_to_cart).pack(pady=(8, 4))
        button(self, "Warenkorb ansehen", self.show_cart, primary=False).pack(pady=2)
        button(self, "Logout", self.logout, primary=False).pack(pady=2)

    def filter_by(self, category):
        self.active_category = category
        self.show_shop()

    def sort_by(self, key):
        # Klick auf denselben Sortier-Button schaltet ihn wieder aus.
        self.sort_mode = "none" if self.sort_mode == key else key
        self.show_shop()

    # ==================================================================
    #  SCREEN 4: WARENKORB
    # ==================================================================
    def show_cart(self):
        self.clear()

        title(self, "Dein Warenkorb", 18).pack(pady=(20, 10))

        products = self.cart.get_products()  # < Cart.get_products()
        if not products:
            self.label("Dein Warenkorb ist leer.", GREY, 11).pack(pady=10)
            button(self, "Zurück zum Shop", self.show_shop, primary=False).pack()
            return

        cart_list = tk.Listbox(self, width=50, height=8, font=(FONT, 10),
                               bg=SOFT, fg=INK, relief="flat",
                               highlightthickness=1, highlightbackground=GREEN_LT)
        cart_list.pack(pady=5)
        for product in products:
            cart_list.insert(tk.END, f"{product.get_name()}  -  {float(product.get_price()):.2f} EUR")
            #                            ^get_name()             ^ get_price()

        # Ausgewählte Position aus dem Warenkorb entfernen (Bearbeitung).
        def remove_selected():
            selection = cart_list.curselection()
            if not selection:
                messagebox.showinfo("Info", "Bitte eine Position auswählen.")
                return
            product = products[selection[0]]
            self.cart.remove_product(product)  # <- Cart.remove_product()
            self.show_cart()

        # Zwischensumme (ohne Rabatt) -> deine Methode get_total().
        total = self.cart.get_total()  # <-Cart.get_total()
        tk.Label(self, text=f"Zwischensumme: {total:.2f} EUR", bg=WHITE, fg=GREEN_DK,
                 font=(FONT, 13, "bold")).pack(pady=8)

        # --- Liefermethode wählen (Bestellprozess-Schritt) ---
        delivery = tk.StringVar(value="Standard")
        deliver_row = tk.Frame(self, bg=WHITE)
        deliver_row.pack(pady=(0, 6))
        tk.Label(deliver_row, text="Lieferung:", bg=WHITE, fg=GREY,
                 font=(FONT, 9)).pack(side="left", padx=(0, 4))
        for method in ("Standard", "Express"):
            tk.Radiobutton(deliver_row, text=method, variable=delivery, value=method,
                           bg=WHITE, fg=INK, font=(FONT, 9),
                           selectcolor=GREEN_LT, activebackground=WHITE).pack(side="left")

        def place_order():
            # Eine Bestellung wird aus dem Warenkorb gebaut.
            # Der 5%-Firmenrabatt steckt schon in Order.calculate_total().
            order = Order(self.cart)  #  Order (übernimmt Kunde + Produkte aus dem Cart)
            try:
                order.create_invoice()  # Order.create_invoice()  (schreibt rechnung.txt)
            except Exception:
                pass

            messagebox.showinfo(
                "Bestellung bestätigt",
                f"Danke für deine Bestellung!\n"
                f"Lieferung: {delivery.get()}\n"
                f"Gesamtbetrag: {order.get_total():.2f} EUR\n"  # < Order.get_total()
                f"Rechnung gespeichert in rechnung.txt")

            self.cart.clear()  # < Cart.clear()
            self.show_shop()

        button(self, "Bestellung abschließen", place_order).pack(pady=(8, 4))
        button(self, "Position entfernen", remove_selected, primary=False).pack(pady=2)
        button(self, "Weiter einkaufen", self.show_shop, primary=False).pack(pady=2)

    # ==================================================================
    def logout(self):
        self.current_user = None
        self.cart = None
        self.show_login()


# ----------------------------------------------------------------------
# Verbindung herstellen (oder offline weitermachen) und App starten.
# ----------------------------------------------------------------------
def connect_storage():
    # Versucht, deine Storage-Klasse zu verbinden. Klappt das nicht
    # has du eine falsche password gegeben oder so etwas dann läuft die App offline weiter.
    try:
        storage = Storage()
        storage.connect()
        return storage
    except Exception:
        return None


if __name__ == "__main__":
    storage_obj = connect_storage()
    app = ShopApp(storage_obj)
    app.mainloop()
    if app.storage is not None:
        app.storage.disconnect()