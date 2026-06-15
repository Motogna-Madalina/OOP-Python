"""
WarenWelt - Tkinter GUI (Part 4 of the project)

This is the user interface for the sustainable WarenWelt online shop.
It integrates the components built in the previous parts:
  - customer management (PrivateCustomer / CompanyCustomer + Validator)
  - product management (Book / Electronics / Clothing)
  - shopping cart and order system (ShoppingCart / Order)

The whole app lives in ONE window. Screens are swapped inside a content
area (welcome -> login / register -> shop -> cart -> confirmation).

Registered users are kept in memory (a simple dict) so the app ns
standalone, without a MySQL connection. The database layer (Storage)
can be plugged in later using the existing save()/load() methods.

Run it from the project root:

    python warenwelt_gui.py
"""

# ______________________________________________________________________
#  IMPORTS
# ______________________________________________________________________

import os
import sys

# --- make the project root importable, no matter where we start from ---
# This file lives in <root>/main/, so the project root is one level up.
# Adding it to sys.path lets the absolute imports below work even when the
# script is launched directly (python main/warenwelt_gui.py) without setting
# PYTHONPATH first.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk

# --- existing project classes (absolute imports from project root) ---
from shop_models.customers.private_customer import PrivateCustomer
from shop_models.customers.company_customer import CompanyCustomer
from shop_models.products.book import Book
from shop_models.products.electronics import Electronics
from shop_models.products.clothing import Clothing
from orders.shopping_cart import ShoppingCart
from utils.validator import Validator


# ______________________________________________________________________
#  STYLE  (the green "GreenWorld" look from the mockups)
# ______________________________________________________________________

BG       = "#FFFFFF"   # main background
SOFT     = "#F1F1EE"   # neutral product card
GREEN_LT = "#CFE0AC"   # highlight / active pill
GREEN_DK = "#445033"   # primary buttons + brand text
INK      = "#1F2419"   # main text
MUTED    = "#8A8A82"   # secondary text
LINE     = "#E4E4E0"   # separators
DANGER   = "#9A4A3A"   # remove / error

FAMILY = "Helvetica"   # safe cross-platform family (Tk substitutes if missing)


# ______________________________________________________________________
def font(size, weight="normal"):
    # Build a font tuple the way Tk expects it: (family, size, weight).
    return (FAMILY, size, weight)


# ______________________________________________________________________
#  DATABASE CONFIG
# ______________________________________________________________________
# >>> MYSQL LOGIN DATA <<<
# These 5 lines tell the app HOW to enter the MySQL database.
# It is like a username and password to open the database "warenwelt".
DB_HOST = "127.0.0.1"          # where MySQL is (this same computer)
DB_USER = "root"               # the MySQL user name
DB_PASSWORD = "Motogna6624."   # the MySQL password
DB_NAME = "warenwelt"          # the name of MY database
DB_PORT = 3306                 # the door (port) MySQL uses


# ______________________________________________________________________
#  PURE LOGIC  (no Tk -> easy to unit-test, see tests_package)
# ______________________________________________________________________

# Categories map to the product classes
CATEGORIES = ("All", "Electronics", "Clothing", "Books")

# Eco-themed delivery options: (label -> surcharge in EUR)
DELIVERY = {
    "Eco shipping (5-7 days)": 0.00,
    "Standard (3-5 days)":     2.90,
    "Express (1-2 days)":      6.90,
}


# ______________________________________________________________________
def category_of(product):
    """Return the category name for a product instance."""
    if isinstance(product, Electronics):
        return "Electronics"
    if isinstance(product, Clothing):
        return "Clothing"
    if isinstance(product, Book):
        return "Books"
    return "Other"


# ______________________________________________________________________
def filter_products(products, category):
    """Keep only products of a category. 'All' returns everything."""
    if category == "All":
        return list(products)

    # Go through every product and keep the ones that match.
    result = []
    for product in products:
        if category_of(product) == category:
            result.append(product)
    return result


# ______________________________________________________________________
def sort_products(products, key):
    """Sort a product list. key is one of the SORT_KEYS labels."""
    if key == "Name (A-Z)":
        return sorted(products, key=lambda p: p.name.lower())
    if key == "Price (low to high)":
        return sorted(products, key=lambda p: p.price)
    if key == "Price (high to low)":
        return sorted(products, key=lambda p: p.price, reverse=True)
    return list(products)


SORT_KEYS = ("Name (A-Z)", "Price (low to high)", "Price (high to low)")


# ______________________________________________________________________
def delivery_fee(method):
    """Surcharge for a delivery method (0.0 if unknown)."""
    return DELIVERY.get(method, 0.0)


# ______________________________________________________________________
def build_catalog():
    """Create the in-memory product catalog using the existing classes."""
    return [
        Book("Python Basics", 29.99, "John Author", 350),
        Book("Clean Code", 39.99, "Robert Martin", 464),
        Book("The Green Garden", 19.99, "Maria Flora", 210),
        Electronics("Dell Laptop", 1200.99, "Dell", 2),
        Electronics("Solar Power Bank", 49.99, "EcoTech", 3),
        Electronics("Wireless Headphones", 89.99, "Sony", 2),
        Clothing("Organic T-Shirt", 24.99, "M", "Green"),
        Clothing("Hemp Jacket", 89.99, "XL", "Beige"),
        Clothing("Recycled Sneakers", 64.99, "42", "White"),
    ]


# ______________________________________________________________________
class UserStore:
    """In-memory user accounts: email -> {"password": ..., "customer": obj}."""

    def __init__(self):
        self._users = {}

    def register(self, customer, password):
        email = customer.get_email()
        if email in self._users:
            raise ValueError("An account with this email already exists.")
        self._users[email] = {"password": password, "customer": customer}

    def authenticate(self, email, password):
        record = self._users.get(email)
        if record and record["password"] == password:
            return record["customer"]
        return None


# ______________________________________________________________________
class ShopRepository:
    """Data access with a graceful fallback.

    If MySQL is reachable, products are loaded from the database and
    customers are saved/authenticated against it. Otherwise everything
    runs in memory so the app still works.
    """

    def __init__(self):
        self.storage = None
        self._mem = UserStore()          # in-memory fallback for users
        self._connect()

    @property
    def online(self):
        return self.storage is not None

    def _connect(self):
        # ==============================================================
        # >>> THIS IS WHERE THE APP CONNECTS TO MYSQL <<<
        # We try to open the database. If it works, we save the
        # connection and use the real database. If it fails (MySQL is
        # off or wrong password), we use memory so the app still opens.
        # ==============================================================
        try:
            from data_base.storage import Storage          # bring the database tool
            storage = Storage(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                              database=DB_NAME, port=DB_PORT)  # use the login data
            storage.connect()                              # <-- OPEN THE CONNECTION
            self.storage = storage                         # success: now we are ONLINE
        except Exception:
            self.storage = None                            # failed: use memory instead

    # ==================================================================
    # >>> READ PRODUCTS FROM MYSQL <<<
    # This reads all books, electronics and clothing FROM the database
    # and turns each row into a product object the app can show.
    # ==================================================================
    def load_catalog(self):
        if not self.online:                 # no database? use example products
            return build_catalog()
        try:
            products = []
            for row in (Book.load_all(self.storage) or []):   # GET books from MySQL
                p = Book(row[1], float(row[2]), row[3], row[4])
                p.id = row[0]
                products.append(p)
            for row in (Electronics.load_all(self.storage) or []):
                p = Electronics(row[1], float(row[2]), row[3], row[4])
                p.id = row[0]
                products.append(p)
            for row in (Clothing.load_all(self.storage) or []):
                p = Clothing(row[1], float(row[2]), row[3], row[4])
                p.id = row[0]
                products.append(p)
        except Exception:
            return build_catalog()
        # If the tables are empty, fall back to the seed catalog so the
        # shop is never blank.
        return products or build_catalog()

    # ==================================================================
    # >>> SAVE A NEW CUSTOMER INTO MYSQL <<<
    # This runs when a user clicks "Register". It writes the new
    # customer INTO the database (an INSERT). This is the part that
    # really saves data in MySQL.
    # ==================================================================
    def register(self, customer, password):
        if not self.online:                 # no database? save in memory
            self._mem.register(customer, password)
            return
        if self._email_exists(customer.get_email()):   # email already used?
            raise ValueError("An account with this email already exists.")
        try:
            if isinstance(customer, PrivateCustomer):
                # Convert DD.MM.YYYY -> YYYY-MM-DD for the DATE column, then
                # restore the original value (we do not modify the class).
                from datetime import datetime
                original = customer.birthdate
                try:
                    customer.birthdate = datetime.strptime(
                        original, "%d.%m.%Y").strftime("%Y-%m-%d")
                    customer.save(self.storage)
                finally:
                    customer.birthdate = original
            else:
                customer.save(self.storage)
        except ValueError:
            raise                            # already a clear message
        except Exception as error:
            # A failed INSERT now raises (see Storage.execute_query) instead
            # of pretending to succeed. Turn it into a clear message for the
            # GUI, which shows ValueError text in a "Registration failed" box.
            raise ValueError(
                f"Could not save your account to the database: {error}")

    # ==================================================================
    # >>> LOGIN: CHECK THE CUSTOMER IN MYSQL <<<
    # This runs when a user clicks "Login". It asks the database for a
    # customer with this email AND password (a SELECT). If it finds one,
    # the login is correct.
    # ==================================================================
    def authenticate(self, email, password):
        if not self.online:                 # no database? check memory
            return self._mem.authenticate(email, password)

        row = self._query(                  # ASK MySQL for a private customer
            "SELECT * FROM private_customers WHERE email=%s AND password=%s",
            (email, password))
        if row:
            bd = row[6]
            bd_str = bd.strftime("%d.%m.%Y") if hasattr(bd, "strftime") else str(bd)
            try:
                return PrivateCustomer(row[1], row[2], row[3], row[4],
                                       row[5], bd_str)
            except Exception:
                pass

        row = self._query(
            "SELECT * FROM company_customers WHERE email=%s AND password=%s",
            (email, password))
        if row:
            return CompanyCustomer(row[1], row[2], row[3], row[4],
                                   row[5], str(row[6]))
        return None

    def _email_exists(self, email):
        for table in ("private_customers", "company_customers"):
            if self._query(f"SELECT 1 FROM {table} WHERE email=%s", (email,)):
                return True
        return False

    # ==================================================================
    # >>> THE LITTLE HELPER THAT TALKS TO MYSQL <<<
    # All the SELECT questions above use this. It sends the SQL to the
    # database and gives back the first row, or None if something fails.
    # ==================================================================
    def _query(self, sql, params):
        """Run a SELECT and return the first row, or None on any problem."""
        try:
            cursor = self.storage.execute_query(sql, params)  # send SQL to MySQL
            return cursor.fetchone() if cursor else None      # take the first row
        except Exception:
            return None


# ______________________________________________________________________
#  REUSABLE WIDGETS
# ______________________________________________________________________

class RoundedButton(tk.Canvas):
    """A flat pill-shaped button drawn on a Canvas (rounded corners)."""

    # __________________________________________________________________
    def __init__(self, parent, text, command=None, bg=GREEN_DK, fg="white",
                 hover=None, size=11, weight="bold", padx=22, pady=11,
                 radius=18, **kw):
        # Remember the colors and the action for later.
        self._bg = bg
        self._hover = hover or self._shade(bg)
        self._fg = fg
        self._command = command
        self._font = tkfont.Font(family=FAMILY, size=size, weight=weight)

        # Make the canvas big enough for the text plus padding.
        w = self._font.measure(text) + 2 * padx
        h = self._font.metrics("linespace") + 2 * pady
        super().__init__(parent, width=w, height=h, bg=parent["bg"],
                         highlightthickness=0, **kw)

        # Draw the rounded rectangle and the text on top of it.
        self._rect = self._round_rect(1, 1, w - 1, h - 1, radius, fill=bg)
        self._text = self.create_text(w / 2, h / 2, text=text,
                                       fill=fg, font=self._font)

        # React to clicks and to the mouse entering / leaving.
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", lambda e: self.itemconfig(self._rect, fill=self._hover))
        self.bind("<Leave>", lambda e: self.itemconfig(self._rect, fill=self._bg))
        self.configure(cursor="hand2")

    # __________________________________________________________________
    def _on_click(self, _event):
        # Run the button's action if there is one.
        if self._command:
            self._command()

    # __________________________________________________________________
    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        # Corner points of a rounded rectangle; smooth=True bends them.
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kw)

    # __________________________________________________________________
    @staticmethod
    def _shade(hex_color, factor=0.88):
        # Make a color a bit darker (used for the hover color).
        hex_color = hex_color.lstrip("#")

        # Read the red / green / blue parts from the hex string.
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # Multiply each part to darken it.
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)

        return f"#{r:02x}{g:02x}{b:02x}"


# ______________________________________________________________________
class ScrollFrame(tk.Frame):
    """A vertically scrollable frame. Add widgets to self.inner."""

    # __________________________________________________________________
    def __init__(self, parent, bg=BG):
        super().__init__(parent, bg=bg)

        # A canvas does the scrolling; the scrollbar controls the canvas.
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        bar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        # 'inner' is the frame where the real content goes.
        self.inner = tk.Frame(self.canvaLs, bg=bg)

        # When the inner content changes size, update the scroll area.
        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Put the inner frame inside the canvas and keep it as wide as the canvas.
        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self._win, width=e.width),
        )
        self.canvas.configure(yscrollcommand=bar.set)

        # Place the canvas on the left and the scrollbar on the right.
        self.canvas.pack(side="left", fill="both", expand=True)
        bar.pack(side="right", fill="y")

        # Mouse wheel scrolling.
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-e.delta / 120), "units"),
        )


# ______________________________________________________________________
#  APPLICATION
# ______________________________________________________________________

class WarenWeltApp(tk.Tk):

    # __________________________________________________________________
    def __init__(self):
        super().__init__()

        # --- window settings ---
        self.title("WarenWelt")
        self.geometry("900x680")
        self.minsize(760, 560)
        self.configure(bg=BG)

        # --- state (the data the app remembers while running) ---
        self.repo = ShopRepository()
        self.catalog = self.repo.load_catalog()
        self.current_user = None
        self.cart = None
        self.active_category = "All"
        self.active_sort = SORT_KEYS[0]

        # --- menu bar (required: "Menueleiste fuer Navigation") ---
        self._build_menubar()

        # --- content area where screens are swapped ---
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(fill="both", expand=True)

        # Show the first screen.
        self.show_welcome()

    # __________________________________________________________________
    #  Menu + helpers
    # __________________________________________________________________
    def _build_menubar(self):
        # Top menu with a "Navigation" dropdown: Shop / Cart / Log out.
        menubar = tk.Menu(self)
        nav = tk.Menu(menubar, tearoff=0)
        nav.add_command(label="Shop", command=self._goto_shop)
        nav.add_command(label="Cart", command=self._goto_cart)
        nav.add_separator()
        nav.add_command(label="Log out", command=self.logout)
        menubar.add_cascade(label="Navigation", menu=nav)
        self.config(menu=menubar)

    # __________________________________________________________________
    def _goto_shop(self):
        # Only allow the shop when someone is logged in.
        if self.current_user:
            self.show_shop()
        else:
            messagebox.showinfo("WarenWelt", "Please log in first.")

    # __________________________________________________________________
    def _goto_cart(self):
        # Only allow the cart when someone is logged in.
        if self.current_user:
            self.show_cart()
        else:
            messagebox.showinfo("WarenWelt", "Please log in first.")

    # __________________________________________________________________
    def _clear(self):
        # Remove everything currently shown in the content area.
        for child in self.content.winfo_children():
            child.destroy()

    # __________________________________________________________________
    def _make_command(self, action, value):
        # Build a function that runs "action(value)" when a button is clicked.
        # This replaces the harder-to-read "lambda x=value: ..." trick with a
        # small named helper that does exactly the same thing. We need it
        # because a button only stores the value at click time, so each button
        # must keep its own copy of "value".
        def run():
            action(value)
        return run

    # __________________________________________________________________
    def logout(self):
        # Forget the user and the cart, then go back to the start.
        self.current_user = None
        self.cart = None
        self.show_welcome()

    # __________________________________________________________________
    #  SCREEN 1: Welcome
    # __________________________________________________________________
    def show_welcome(self):
        self._clear()

        # A box centered in the middle of the window.
        wrap = tk.Frame(self.content, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        # Title and slogan texts.
        tk.Label(wrap, text="Welcome to WarenWelt",
                 bg=BG, fg=INK, font=font(34, "bold")).pack(pady=(0, 6))
        tk.Label(wrap, text="Shop greener, live better.",
                 bg=BG, fg=GREEN_DK, font=font(15, "normal")).pack(pady=(0, 4))
        tk.Label(wrap,
                 text="Your sustainable online shop for books, "
                      "electronics and clothing.",
                 bg=BG, fg=MUTED, font=font(11)).pack(pady=(0, 28))

        # Button that opens the login screen.
        RoundedButton(wrap, "Get started", command=self.show_login,
                      bg=GREEN_DK, size=12).pack()

        # Small line that says if we are connected to the database or not.
        if self.repo.online:
            status = "Connected to database"
        else:
            status = "Offline mode (in-memory data)"
        tk.Label(wrap, text=status, bg=BG, fg=MUTED,
                 font=font(9)).pack(pady=(22, 0))

    # __________________________________________________________________
    #  SCREEN 2: Login
    # __________________________________________________________________
    def show_login(self):
        self._clear()
        card = self._centered_card(width=380)

        tk.Label(card, text="Log in", bg=card["bg"], fg=INK,
                 font=font(22, "bold")).pack(anchor="w", pady=(0, 16))

        # Two input fields.
        email = self._field(card, "Email")
        password = self._field(card, "Password", show="*")

        def do_login():
            # Ask the repository to check email + password.
            user = self.repo.authenticate(email.get().strip(), password.get())
            if user is None:
                messagebox.showerror("Login failed",
                                     "Wrong email or password.")
                return
            # Login worked: remember the user and give them a cart.
            self.current_user = user
            self.cart = ShoppingCart(user)
            self.show_shop()

        RoundedButton(card, "Log in", command=do_login,
                      bg=GREEN_DK).pack(anchor="w", pady=(18, 8))

        # "No account yet? Create one" link row.
        row = tk.Frame(card, bg=card["bg"])
        row.pack(anchor="w")
        tk.Label(row, text="No account yet?", bg=card["bg"],
                 fg=MUTED, font=font(10)).pack(side="left")
        link = tk.Label(row, text="Create one", bg=card["bg"],
                        fg=GREEN_DK, font=font(10, "bold"), cursor="hand2")
        link.pack(side="left", padx=(6, 0))
        link.bind("<Button-1>", lambda e: self.show_register())

    # __________________________________________________________________
    #  SCREEN 3: Register
    # __________________________________________________________________
    def show_register(self):
        self._clear()

        # The form can be long, so put it inside a scrollable frame.
        outer = ScrollFrame(self.content, bg=BG)
        outer.pack(fill="both", expand=True)

        card = tk.Frame(outer.inner, bg=SOFT, padx=30, pady=26)
        card.pack(pady=28)

        tk.Label(card, text="Create your account", bg=SOFT, fg=INK,
                 font=font(22, "bold")).pack(anchor="w", pady=(0, 4))
        tk.Label(card, text="Join WarenWelt and shop sustainably.",
                 bg=SOFT, fg=MUTED, font=font(10)).pack(anchor="w", pady=(0, 16))

        # Choose customer type: private or company.
        ctype = tk.StringVar(value="private")
        type_row = tk.Frame(card, bg=SOFT)
        type_row.pack(anchor="w", pady=(0, 10))
        for label, val in (("Private customer", "private"),
                           ("Company customer", "company")):
            tk.Radiobutton(type_row, text=label, variable=ctype, value=val,
                           bg=SOFT, fg=INK, font=font(10),
                           activebackground=SOFT, selectcolor=GREEN_LT,
                           command=lambda: toggle_extra()).pack(side="left",
                                                                padx=(0, 16))

        # The normal input fields, same for both customer types.
        name = self._field(card, "Name", bg=SOFT)
        address = self._field(card, "Address", bg=SOFT)
        email = self._field(card, "Email", bg=SOFT)
        phone = self._field(card, "Phone (e.g. +431234567)", bg=SOFT)
        password = self._field(card, "Password", show="*", bg=SOFT)

        # One extra field whose meaning changes with the customer type.
        extra_label = tk.Label(card, bg=SOFT, fg=INK, font=font(10, "bold"))
        extra_label.pack(anchor="w", pady=(8, 2))
        extra = tk.Entry(card, font=font(11), bg="white", relief="flat",
                         highlightthickness=1, highlightbackground=LINE,
                         highlightcolor=GREEN_DK)
        extra.pack(fill="x", ipady=6)

        def toggle_extra():
            # Update the extra field's label depending on the chosen type.
            if ctype.get() == "private":
                extra_label.config(text="Birthdate (DD.MM.YYYY)")
            else:
                extra_label.config(text="Company number (5-15 digits)")

        toggle_extra()

        def do_register():
            # Step 1: try to build the right customer object.
            try:
                if ctype.get() == "private":
                    customer = PrivateCustomer(
                        name.get().strip(), address.get().strip(),
                        email.get().strip(), phone.get().strip(),
                        password.get(), extra.get().strip())
                else:
                    customer = CompanyCustomer(
                        name.get().strip(), address.get().strip(),
                        email.get().strip(), phone.get().strip(),
                        password.get(), extra.get().strip())
            except ValueError as err:
                messagebox.showerror("Invalid data", str(err))
                return

            # Step 2: the Customer setters silently ignore invalid values, so we
            # validate the basics explicitly to give clear error messages.
            problems = self._validate_basics(
                name.get().strip(), address.get().strip(),
                email.get().strip(), phone.get().strip(), password.get())
            if problems:
                messagebox.showerror("Invalid data", "\n".join(problems))
                return

            # Step 3: save the new customer.
            try:
                self.repo.register(customer, password.get())
            except ValueError as err:
                messagebox.showerror("Registration failed", str(err))
                return

            # Step 4: tell the user and go to the login screen.
            messagebox.showinfo("Welcome!",
                                "Account created. You can log in now.")
            self.show_login()

        RoundedButton(card, "Create account", command=do_register,
                      bg=GREEN_DK).pack(anchor="w", pady=(18, 8))

        # "Back to login" link.
        back = tk.Label(card, text="Back to login", bg=SOFT, fg=GREEN_DK,
                        font=font(10, "bold"), cursor="hand2")
        back.pack(anchor="w")
        back.bind("<Button-1>", lambda e: self.show_login())

    # __________________________________________________________________
    @staticmethod
    def _validate_basics(name, address, email, phone, password):
        # Collect a readable error message for every wrong field.
        problems = []
        if not Validator.validate_name(name):
            problems.append("- Name: letters only, must not be empty.")
        if not Validator.validate_address(address):
            problems.append("- Address: must not be empty.")
        if not Validator.validate_email(email):
            problems.append("- Email: invalid format.")
        if not Validator.validate_phone(phone):
            problems.append("- Phone: 8-20 digits, optional '+'.")
        if len(password) < 4:
            problems.append("- Password: at least 4 characters.")
        return problems

    # __________________________________________________________________
    #  SCREEN 4: Shop (products + filter + sort)
    # __________________________________________________________________
    def show_shop(self):
        self._clear()
        self._header("Shop")

        # filter + sort bar
        bar = tk.Frame(self.content, bg=BG)
        bar.pack(fill="x", padx=30, pady=(8, 4))

        # Left side: one pill button per category.
        pills = tk.Frame(bar, bg=BG)
        pills.pack(side="left")
        for cat in CATEGORIES:
            active = (cat == self.active_category)
            # The active category gets the green highlight color.
            if active:
                pill_bg = GREEN_LT
            else:
                pill_bg = SOFT
            RoundedButton(
                pills, cat,
                command=self._make_command(self._set_category, cat),
                bg=pill_bg,
                fg=INK, hover=GREEN_LT, size=10, weight="bold",
                padx=14, pady=7, radius=14,
            ).pack(side="left", padx=(0, 8))

        # Right side: a dropdown to choose the sort order.
        sort_box = tk.Frame(bar, bg=BG)
        sort_box.pack(side="right")
        tk.Label(sort_box, text="Sort:", bg=BG, fg=MUTED,
                 font=font(10)).pack(side="left", padx=(0, 6))
        sort_var = tk.StringVar(value=self.active_sort)
        combo = ttk.Combobox(sort_box, textvariable=sort_var, values=SORT_KEYS,
                             state="readonly", width=18, font=font(10))
        combo.pack(side="left")
        combo.bind("<<ComboboxSelected>>",
                   lambda e: self._set_sort(sort_var.get()))

        # product list (scrollable)
        listing = ScrollFrame(self.content, bg=BG)
        listing.pack(fill="both", expand=True, padx=22, pady=(8, 16))

        # First filter by category, then sort the result.
        products = filter_products(self.catalog, self.active_category)
        products = sort_products(products, self.active_sort)

        # Draw one card for each product.
        for product in products:
            self._product_card(listing.inner, product)

    # __________________________________________________________________
    def _product_card(self, parent, product):
        # One product row: name + details on the left, price + button on the right.
        card = tk.Frame(parent, bg=SOFT, padx=20, pady=16)
        card.pack(fill="x", padx=8, pady=6)

        left = tk.Frame(card, bg=SOFT)
        left.pack(side="left", fill="x", expand=True)

        tk.Label(left, text=product.name, bg=SOFT, fg=INK,
                 font=font(14, "bold")).pack(anchor="w")
        tk.Label(left, text=f"{category_of(product)}  -  {self._detail(product)}",
                 bg=SOFT, fg=MUTED, font=font(10)).pack(anchor="w", pady=(2, 0))

        right = tk.Frame(card, bg=SOFT)
        right.pack(side="right")
        tk.Label(right, text=f"{product.price:.2f} EUR", bg=SOFT, fg=GREEN_DK,
                 font=font(13, "bold")).pack(side="left", padx=(0, 14))
        RoundedButton(right, "Add to cart",
                      command=self._make_command(self._add_to_cart, product),
                      bg=GREEN_DK, size=10, padx=16, pady=8).pack(side="left")

    # __________________________________________________________________
    @staticmethod
    def _detail(product):
        # Build a short detail text that fits the product type.
        if isinstance(product, Book):
            return f"by {product.author}, {product.page_count} pages"
        if isinstance(product, Electronics):
            return f"{product.brand}, {product.warranty_years}y warranty"
        if isinstance(product, Clothing):
            return f"size {product.size}, {product.color}"
        return ""

    # __________________________________________________________________
    def _set_category(self, cat):
        # Remember the chosen category and redraw the shop.
        self.active_category = cat
        self.show_shop()

    # __________________________________________________________________
    def _set_sort(self, key):
        # Remember the chosen sort order and redraw the shop.
        self.active_sort = key
        self.show_shop()

    # __________________________________________________________________
    def _add_to_cart(self, product):
        # Put the product in the cart and confirm it.
        self.cart.add_product(product)
        messagebox.showinfo("Added", f"'{product.name}' added to your cart.")

    # __________________________________________________________________
    #  SCREEN 5: Cart + order process
    # __________________________________________________________________
    def show_cart(self):
        self._clear()
        self._header("Your cart")

        # If the cart is empty, show a message and a button back to the shop.
        if not self.cart.products:
            tk.Label(self.content, text="Your cart is empty.", bg=BG,
                     fg=MUTED, font=font(13)).pack(pady=40)
            RoundedButton(self.content, "Browse products",
                          command=self.show_shop, bg=GREEN_DK).pack()
            return

        body = ScrollFrame(self.content, bg=BG)
        body.pack(fill="both", expand=True, padx=22, pady=(8, 6))

        # Group identical products together -> {product id: [product, quantity]}.
        grouped = {}
        for p in self.cart.products:
            if p.id not in grouped:
                grouped[p.id] = [p, 0]
            grouped[p.id][1] += 1

        # Draw one row per distinct product.
        for product, qty in grouped.values():
            self._cart_row(body.inner, product, qty)

        # ---- summary + delivery + checkout ----
        summary = tk.Frame(self.content, bg=SOFT, padx=24, pady=18)
        summary.pack(fill="x", padx=22, pady=(4, 16))

        subtotal = self.cart.calculate_total()
        is_company = isinstance(self.current_user, CompanyCustomer)

        # Delivery method choices (radio buttons).
        tk.Label(summary, text="Delivery method", bg=SOFT, fg=INK,
                 font=font(12, "bold")).pack(anchor="w")
        delivery_var = tk.StringVar(value=list(DELIVERY.keys())[0])
        for label in DELIVERY:
            fee = DELIVERY[label]
            # Show the surcharge, or "(free)" when it is 0.
            if fee:
                txt = label + f"  (+{fee:.2f} EUR)"
            else:
                txt = label + "  (free)"
            tk.Radiobutton(summary, text=txt, variable=delivery_var,
                           value=label, bg=SOFT, fg=INK, font=font(10),
                           activebackground=SOFT, selectcolor=GREEN_LT,
                           command=lambda: refresh_total()).pack(anchor="w")

        tk.Frame(summary, bg=LINE, height=1).pack(fill="x", pady=12)

        total_lbl = tk.Label(summary, bg=SOFT, fg=INK, font=font(16, "bold"))
        total_lbl.pack(anchor="e")
        note_lbl = tk.Label(summary, bg=SOFT, fg=MUTED, font=font(9))
        note_lbl.pack(anchor="e")

        def refresh_total():
            # Recalculate the total when the delivery method changes.
            fee = delivery_fee(delivery_var.get())
            total = subtotal + fee
            note = f"Subtotal {subtotal:.2f} EUR + delivery {fee:.2f} EUR"
            # Company customers get a 5% discount.
            if is_company:
                discounted = subtotal * 0.95 + fee
                total = discounted
                note += "  (company -5% applied at checkout)"
            total_lbl.config(text=f"Total: {total:.2f} EUR")
            note_lbl.config(text=note)

        refresh_total()

        RoundedButton(summary, "Place order",
                      command=lambda: self._place_order(delivery_var.get()),
                      bg=GREEN_DK, size=12).pack(anchor="e", pady=(12, 0))

    # __________________________________________________________________
    def _cart_row(self, parent, product, qty):
        # One cart line: name + quantity, line price, and a Remove button.
        row = tk.Frame(parent, bg=SOFT, padx=18, pady=12)
        row.pack(fill="x", padx=8, pady=5)

        left = tk.Frame(row, bg=SOFT)
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text=f"{product.name}  x{qty}", bg=SOFT, fg=INK,
                 font=font(12, "bold")).pack(anchor="w")
        tk.Label(left, text=f"{product.price:.2f} EUR each", bg=SOFT,
                 fg=MUTED, font=font(10)).pack(anchor="w")

        right = tk.Frame(row, bg=SOFT)
        right.pack(side="right")
        tk.Label(right, text=f"{product.price * qty:.2f} EUR", bg=SOFT,
                 fg=GREEN_DK, font=font(12, "bold")).pack(side="left",
                                                          padx=(0, 12))
        RoundedButton(right, "Remove",
                      command=self._make_command(self._remove_one, product),
                      bg="#EAD9D4", fg=DANGER, hover="#E0C9C2",
                      size=10, padx=14, pady=7, radius=14).pack(side="left")

    # __________________________________________________________________
    def _remove_one(self, product):
        # Take one copy of this product out of the cart, then redraw.
        self.cart.remove_product(product)   # removes one occurrence
        self.show_cart()

    # __________________________________________________________________
    def _place_order(self, delivery_label):
        # Turn the cart into an order (this applies the company -5%).
        order = self.cart.checkout()        # -> Order (applies company -5%)
        fee = delivery_fee(delivery_label)
        grand_total = order.total_amount + fee

        # Try to write the invoice file; ignore errors so the app keeps going.
        try:
            order.create_invoice()          # writes invoice.txt
        except Exception:
            pass

        # Empty the cart and show the confirmation screen.
        self.cart.clear_cart()
        self.show_confirmation(order, delivery_label, fee, grand_total)

    # __________________________________________________________________
    #  SCREEN 6: Confirmation
    # __________________________________________________________________
    def show_confirmation(self, order, delivery_label, fee, grand_total):
        self._clear()
        self._header("Order confirmed")

        # A green summary card with the order details.
        card = tk.Frame(self.content, bg=GREEN_LT, padx=30, pady=26)
        card.pack(fill="x", padx=22, pady=20)

        tk.Label(card, text="Thank you for your order!", bg=GREEN_LT, fg=INK,
                 font=font(20, "bold")).pack(anchor="w", pady=(0, 4))
        tk.Label(card, text=f"Customer: {order.customer.name}", bg=GREEN_LT,
                 fg=INK, font=font(11)).pack(anchor="w")
        tk.Label(card, text=f"Items: {len(order.products)}", bg=GREEN_LT,
                 fg=INK, font=font(11)).pack(anchor="w")
        tk.Label(card, text=f"Delivery: {delivery_label} (+{fee:.2f} EUR)",
                 bg=GREEN_LT, fg=INK, font=font(11)).pack(anchor="w")
        tk.Label(card, text=f"Total paid: {grand_total:.2f} EUR", bg=GREEN_LT,
                 fg=GREEN_DK, font=font(15, "bold")).pack(anchor="w",
                                                          pady=(8, 0))
        tk.Label(card, text="An invoice has been saved to invoice.txt.",
                 bg=GREEN_LT, fg=MUTED, font=font(9)).pack(anchor="w",
                                                           pady=(6, 0))

        RoundedButton(self.content, "Continue shopping",
                      command=self.show_shop, bg=GREEN_DK).pack(pady=10)

    # __________________________________________________________________
    #  Shared UI helpers
    # __________________________________________________________________
    def _header(self, title):
        # The top bar shown on the shop / cart / confirmation screens.
        head = tk.Frame(self.content, bg=BG)
        head.pack(fill="x", padx=30, pady=(22, 4))

        # Brand name on the left.
        tk.Label(head, text="WarenWelt", bg=BG, fg=GREEN_DK,
                 font=font(18, "bold")).pack(side="left")

        # Navigation buttons on the right.
        nav = tk.Frame(head, bg=BG)
        nav.pack(side="right")
        if self.cart:
            cart_count = len(self.cart.products)
        else:
            cart_count = 0
        RoundedButton(nav, "Shop", command=self.show_shop, bg=SOFT, fg=INK,
                      hover=GREEN_LT, size=10, padx=14, pady=7,
                      radius=14).pack(side="left", padx=4)
        RoundedButton(nav, f"Cart ({cart_count})", command=self.show_cart,
                      bg=SOFT, fg=INK, hover=GREEN_LT, size=10, padx=14,
                      pady=7, radius=14).pack(side="left", padx=4)
        RoundedButton(nav, "Log out", command=self.logout, bg=SOFT, fg=INK,
                      hover=GREEN_LT, size=10, padx=14, pady=7,
                      radius=14).pack(side="left", padx=4)

        # The big page title under the bar.
        tk.Label(self.content, text=title, bg=BG, fg=INK,
                 font=font(24, "bold")).pack(anchor="w", padx=30, pady=(6, 0))

    # __________________________________________________________________
    def _centered_card(self, width=380):
        # A soft-colored card placed in the middle of the window.
        holder = tk.Frame(self.content, bg=BG)
        holder.place(relx=0.5, rely=0.5, anchor="center")
        card = tk.Frame(holder, bg=SOFT, padx=30, pady=28, width=width)
        card.pack()
        return card

    # __________________________________________________________________
    def _field(self, parent, label, show=None, bg=None):
        # A labeled text input. 'show="*"' hides the text (for passwords).
        if bg is None:
            bg = parent["bg"]
        tk.Label(parent, text=label, bg=bg, fg=INK,
                 font=font(10, "bold")).pack(anchor="w", pady=(8, 2))
        entry = tk.Entry(parent, font=font(11), bg="white", relief="flat",
                         show=show or "", highlightthickness=1,
                         highlightbackground=LINE, highlightcolor=GREEN_DK)
        entry.pack(fill="x", ipady=6)
        return entry


# ______________________________________________________________________
#  START THE APP
# ______________________________________________________________________

if __name__ == "__main__":
    # Start the app and keep the window open.
    WarenWeltApp().mainloop()