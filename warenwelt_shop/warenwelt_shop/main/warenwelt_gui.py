"""
WarenWelt - Simple GUI (beginner level) with the green "GreenWorld" look.

==============================  LEGEND  ==============================
Every time the interface uses one of YOUR classes there is a marker:

        # <-- ⭐ ClassName

You can search (Ctrl+F) for "⭐ ShoppingCart", "⭐ Validator", etc.
to jump to every place where that class is used.

Classes used by this GUI:
  ⭐ Storage          (data_base/storage.py)      -> MySQL connection
  ⭐ Book / ⭐ Electronics / ⭐ Clothing            -> products
  ⭐ PrivateCustomer / ⭐ CompanyCustomer          -> customers
  ⭐ Customer                                      -> shared methods (get_email)
  ⭐ Validator                                     -> validate the form
  ⭐ ShoppingCart                                  -> shopping cart
  ⭐ Order                                         -> order + invoice

Products come from the MySQL database. There is no example data, so if
there is no database connection the product list will be empty.

Run it with:
    python main/warenwelt_gui.py
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox

# --- your classes (imported here; used below, marked with ⭐) ---
from shop_models.products.book import Book  # ⭐ Book
from shop_models.products.electronics import Electronics  # ⭐ Electronics
from shop_models.products.clothing import Clothing  # ⭐ Clothing
from shop_models.customers.private_customer import PrivateCustomer  # ⭐ PrivateCustomer
from shop_models.customers.company_customer import CompanyCustomer  # ⭐ CompanyCustomer
from orders.shopping_cart import ShoppingCart  # ⭐ ShoppingCart
from utils.validator import Validator  # ⭐ Validator

# ----------------------------------------------------------------------
# DATABASE LOGIN DATA
# Change these values to match your own MySQL server if needed.
# ----------------------------------------------------------------------
DB_HOST = "127.0.0.1"  # where MySQL is (this same computer)
DB_USER = "root"  # the MySQL user name
DB_PASSWORD = "Motogna6624."  # the MySQL password
DB_NAME = "warenwelt"  # the database name
DB_PORT = 3306  # the MySQL port

# ----------------------------------------------------------------------
# COLORS (the green "GreenWorld" palette)
# ----------------------------------------------------------------------
WHITE = "#FFFFFF"
SOFT = "#F1F1EE"
GREEN_LT = "#CFE0AC"
GREEN_DK = "#445033"
INK = "#1F2419"
GREY = "#8A8A82"

FONT = "Helvetica"


def button(parent, text, command, primary=True):
    # Create a button with the shared style (green if primary, soft if not).
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
# THE APP: one window. To change screen we delete what is there and draw
# the new screen.
# ----------------------------------------------------------------------
class ShopApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("WarenWelt")
        self.geometry("460x580")
        self.configure(bg=WHITE)

        # --- data the app remembers while running ---
        self.storage = self.connect_db()
        self.users = {}
        self.current_user = None
        self.cart = None
        self.catalog = self.load_catalog()
        self.active_category = "All"  # which category filter is selected
        self.shown_products = []  # the products currently in the list

        self.show_login()

    # ==================================================================
    #  DATA ACCESS  (this is what connects the GUI to the rest)
    # ==================================================================
    def connect_db(self):
        # Try to open MySQL using your Storage class. If anything fails
        # (no server, no library, wrong password) we return None and the
        # app simply runs offline.
        try:
            from data_base.storage import Storage  # <-- ⭐ Storage
            storage = Storage(host=DB_HOST, user=DB_USER,  # <-- ⭐ Storage
                              password=DB_PASSWORD,
                              database=DB_NAME, port=DB_PORT)
            storage.connect()  # <-- ⭐ Storage.connect()
            return storage
        except Exception:
            return None

    def load_catalog(self):
        # Products are read from MySQL using your load_all() methods.
        # The three product classes share the same column order
        # (id, name, price, field4, field5), so ONE loop covers all of them
        # instead of repeating almost the same code three times.
        # Without a database connection the catalog stays empty.
        if self.storage is None:
            return []
        try:
            products = []
            for product_class in (Book, Electronics, Clothing):  # <-- ⭐ Book / Electronics / Clothing
                for row in (product_class.load_all(self.storage) or []):  # <-- ⭐ .load_all()
                    products.append(
                        product_class(row[1], float(row[2]), row[3], row[4]))
            return products
        except Exception:
            return []

    def save_customer(self, customer, password):
        # Offline -> keep the customer in memory.
        if self.storage is None:
            # get_email() comes from the base class Customer.
            self.users[customer.get_email()] = {  # <-- ⭐ Customer.get_email()
                "password": password, "customer": customer}
            return
        # Online -> write to MySQL using your save() method.
        if isinstance(customer, PrivateCustomer):  # <-- ⭐ PrivateCustomer
            # The birthdate is stored as DD.MM.YYYY in the object but the
            # DATE column needs YYYY-MM-DD, so we convert it only to save.
            original_birthdate = customer.birthdate
            customer.birthdate = datetime.strptime(
                original_birthdate, "%d.%m.%Y").strftime("%Y-%m-%d")
            customer.save(self.storage)  # <-- ⭐ PrivateCustomer.save()
            customer.birthdate = original_birthdate
        else:
            customer.save(self.storage)  # <-- ⭐ CompanyCustomer.save()

    def find_customer(self, email, password):
        # Offline -> look in the in-memory dictionary.
        if self.storage is None:
            record = self.users.get(email)
            if record and record["password"] == password:
                return record["customer"]
            return None
        # Online -> use your load() methods to read the row by email.
        private_row = PrivateCustomer.load(self.storage, email)  # <-- ⭐ PrivateCustomer.load()
        if private_row and private_row[5] == password:
            birthdate_value = private_row[6]
            if hasattr(birthdate_value, "strftime"):
                birthdate_text = birthdate_value.strftime("%d.%m.%Y")
            else:
                birthdate_text = str(birthdate_value)
            return PrivateCustomer(private_row[1], private_row[2],  # <-- ⭐ PrivateCustomer
                                   private_row[3], private_row[4],
                                   private_row[5], birthdate_text)
        company_row = CompanyCustomer.load(self.storage, email)  # <-- ⭐ CompanyCustomer.load()
        if company_row and company_row[5] == password:
            return CompanyCustomer(company_row[1], company_row[2],  # <-- ⭐ CompanyCustomer
                                   company_row[3], company_row[4],
                                   company_row[5], str(company_row[6]))
        return None

    def email_exists(self, email):
        # True if some customer already uses this email.
        # Offline -> look in the in-memory dictionary.
        if self.storage is None:
            return email in self.users
        # Online -> check both customer tables with your load() methods.
        if PrivateCustomer.load(self.storage, email):  # <-- ⭐ PrivateCustomer.load()
            return True
        if CompanyCustomer.load(self.storage, email):  # <-- ⭐ CompanyCustomer.load()
            return True
        return False

    # ==================================================================
    #  Helpers to build widgets
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

        self.label("Password:").pack(pady=(8, 0))
        password_entry = self.entry(hide="*")
        password_entry.pack(pady=3, ipady=4)

        def do_login():
            user = self.find_customer(email_entry.get().strip(),
                                      password_entry.get())
            if user is not None:
                self.current_user = user
                self.cart = ShoppingCart(user)  # <-- ⭐ ShoppingCart
                self.show_shop()
            else:
                messagebox.showerror("Login failed", "Wrong email or password.")

        button(self, "Log in", do_login).pack(pady=(16, 6))
        button(self, "Create account", self.show_register, primary=False).pack()

        # Show whether we are connected to the database or not.
        if self.storage is None:
            status = "Offline mode (no database)"
        else:
            status = "Connected to database"
        self.label(status, GREY, 9).pack(pady=(18, 0))

    # ==================================================================
    #  SCREEN 2: REGISTER
    # ==================================================================
    def show_register(self):
        self.clear()

        title(self, "Create account", 18).pack(pady=(20, 10))

        customer_type = tk.StringVar(value="private")
        # We keep a reference to each radio button so we can set its command
        # AFTER the update_extra_label() function is defined further down.
        radio_private = tk.Radiobutton(self, text="Private customer",
                       variable=customer_type, value="private",
                       bg=WHITE, fg=INK, font=(FONT, 10),
                       selectcolor=GREEN_LT, activebackground=WHITE)
        radio_private.pack()
        radio_company = tk.Radiobutton(self, text="Company customer",
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
        entry_address = field("Address:")
        entry_email = field("Email:")
        entry_phone = field("Phone (8-20 digits):")
        entry_password = field("Password:", hide="*")

        # The last field changes its meaning with the customer type, so we
        # keep its label in a variable and update the text when the type
        # changes: private -> birthdate, company -> company number.
        extra_label = self.label("Birthdate (DD.MM.YYYY):")
        extra_label.pack(pady=(6, 0))
        entry_extra = self.entry()
        entry_extra.pack(pady=2, ipady=3)

        def update_extra_label():
            if customer_type.get() == "private":
                extra_label.config(text="Birthdate (DD.MM.YYYY):")
            else:
                extra_label.config(text="Company number (5-15 digits):")

        # Now that the function exists, run it whenever a radio is clicked,
        # and once at the start so the label is correct from the beginning.
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

            # Step 1: check the basics with your Validator.
            if not Validator.validate_name(name):  # <-- ⭐ Validator
                messagebox.showerror("Error", "Invalid name (letters only).")
                return
            if not Validator.validate_address(address):  # <-- ⭐ Validator
                messagebox.showerror("Error", "Invalid address.")
                return
            if not Validator.validate_email(email):  # <-- ⭐ Validator
                messagebox.showerror("Error", "Invalid email.")
                return
            if not Validator.validate_phone(phone):  # <-- ⭐ Validator
                messagebox.showerror("Error", "Invalid phone (8-20 digits).")
                return

            # Step 1b: the email must not be used by another account.
            if self.email_exists(email):
                messagebox.showerror(
                    "Error", "An account with this email already exists.")
                return

            # Step 2: build the right customer (your class).
            try:
                if customer_type.get() == "private":
                    customer = PrivateCustomer(name, address, email,  # <-- ⭐ PrivateCustomer
                                               phone, password, extra)
                else:
                    customer = CompanyCustomer(name, address, email,  # <-- ⭐ CompanyCustomer
                                               phone, password, extra)
            except ValueError as error:
                messagebox.showerror("Error", str(error))
                return

            # Step 3: save it (to MySQL if online, else in memory).
            try:
                self.save_customer(customer, password)
            except Exception as error:
                messagebox.showerror("Error", f"Could not save account: {error}")
                return

            messagebox.showinfo("Done", "Account created. You can log in now.")
            self.show_login()

        button(self, "Register", do_register).pack(pady=(12, 6))
        button(self, "Back", self.show_login, primary=False).pack()

    # ==================================================================
    #  SCREEN 3: SHOP
    # ==================================================================
    def show_shop(self):
        self.clear()

        title(self, "Products", 18).pack(pady=(20, 10))

        # If there are no products (no database), show a message instead.
        if not self.catalog:
            self.label("No products to show (no database connection).",
                       GREY, 11).pack(pady=20)
            button(self, "Log out", self.logout, primary=False).pack()
            return

        # --- category filter buttons (All / Electronics / Books / Clothing) ---
        filter_row = tk.Frame(self, bg=WHITE)
        filter_row.pack(pady=(0, 8))
        for category_name in ("All", "Electronics", "Books", "Clothing"):
            # The selected category is highlighted in light green.
            if category_name == self.active_category:
                color = GREEN_LT
            else:
                color = SOFT
            # 'c=category_name' makes each button remember its own category.
            tk.Button(filter_row, text=category_name,
                      command=lambda c=category_name: self.filter_by(c),
                      bg=color, fg=INK, font=(FONT, 9, "bold"), relief="flat",
                      activebackground=GREEN_LT, padx=10, pady=4,
                      cursor="hand2").pack(side="left", padx=3)

        # Keep only the products of the selected category (or all of them).
        # product.category comes from your product classes.
        self.shown_products = []
        for product in self.catalog:
            if self.active_category == "All" or product.category == self.active_category:  # <-- ⭐ Product.category
                self.shown_products.append(product)

        self.listbox = tk.Listbox(self, width=52, height=11, font=(FONT, 10),
                                  bg=SOFT, fg=INK, relief="flat",
                                  selectbackground=GREEN_DK, selectforeground="white",
                                  highlightthickness=1, highlightbackground=GREEN_LT)
        self.listbox.pack(pady=5)

        # Fill the list in the SAME order as self.shown_products.
        for product in self.shown_products:
            self.listbox.insert(
                tk.END,
                f"{product.name}  ({product.category})  -  {product.price:.2f} EUR")
            #                       ^⭐ Product.category

        def add_to_cart():
            selection = self.listbox.curselection()
            if not selection:
                messagebox.showinfo("Info", "Please select a product first.")
                return
            product = self.shown_products[selection[0]]
            self.cart.add_product(product)  # <-- ⭐ ShoppingCart.add_product()
            messagebox.showinfo("Added", f"'{product.name}' added to your cart.")

        button(self, "Add to cart", add_to_cart).pack(pady=(8, 4))
        button(self, "View cart", self.show_cart, primary=False).pack(pady=2)
        button(self, "Log out", self.logout, primary=False).pack(pady=2)

    def filter_by(self, category):
        # Remember the chosen category and redraw the shop screen.
        self.active_category = category
        self.show_shop()

    # ==================================================================
    #  SCREEN 4: CART
    # ==================================================================
    def show_cart(self):
        self.clear()

        title(self, "Your cart", 18).pack(pady=(20, 10))

        if not self.cart.products:  # <-- ⭐ ShoppingCart.products
            self.label("Your cart is empty.", GREY, 11).pack(pady=10)
            button(self, "Back to shop", self.show_shop, primary=False).pack()
            return

        cart_list = tk.Listbox(self, width=52, height=9, font=(FONT, 10),
                               bg=SOFT, fg=INK, relief="flat",
                               highlightthickness=1, highlightbackground=GREEN_LT)
        cart_list.pack(pady=5)
        for product in self.cart.products:  # <-- ⭐ ShoppingCart.products
            cart_list.insert(tk.END, f"{product.name}  -  {product.price:.2f} EUR")

        total = self.cart.calculate_total()  # <-- ⭐ ShoppingCart.calculate_total()
        tk.Label(self, text=f"Total: {total:.2f} EUR", bg=WHITE, fg=GREEN_DK,
                 font=(FONT, 13, "bold")).pack(pady=8)

        def place_order():
            order = self.cart.checkout()  # <-- ⭐ ShoppingCart.checkout() -> ⭐ Order
            try:
                order.create_invoice()  # <-- ⭐ Order.create_invoice()
            except Exception:
                pass
            messagebox.showinfo(
                "Order confirmed",
                f"Thank you for your order!\n"
                f"Total paid: {order.total_amount:.2f} EUR\n"  # <-- ⭐ Order.total_amount
                f"Invoice saved to invoice.txt")
            self.cart.clear_cart()  # <-- ⭐ ShoppingCart.clear_cart()
            self.show_shop()

        button(self, "Place order", place_order).pack(pady=(8, 4))
        button(self, "Keep shopping", self.show_shop, primary=False).pack(pady=2)

    # ==================================================================
    def logout(self):
        self.current_user = None
        self.cart = None
        self.show_login()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = ShopApp()
    app.mainloop()
    if app.storage is not None:
        app.storage.disconnect()  # <-- ⭐ Storage.disconnect()