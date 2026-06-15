# WarenWelt – How to Run the Program

A short guide for opening and running the **WarenWelt** sustainable online shop.

---

## 1. What you need

- **Python 3.10 or newer** (developed and tested with Python 3.14).
  Check with:
  ```
  python --version
  ```
- **Tkinter** – the graphical interface library.
  It comes bundled with the standard Python installer on Windows, so
  normally there is nothing to install. Check with:
  ```
  python -c "import tkinter; print('tkinter OK')"
  ```

> **MySQL is optional.** The app tries to connect to a MySQL database on
> start. If MySQL is not running (or not installed), it automatically
> falls back to built-in example data and **runs anyway**. You do not
> need a database to test the program.

---

## 2. How to run it

The main program is:

```
main/warenwelt_gui.py
```

You can start it in **any** of these ways — they all open the same window.

### Option A — Double-click / Run button (easiest)
Open the project in **VS Code** (or IDLE), open the file
`main/warenwelt_gui.py`, and press the **Run ▶** button (or `F5`).

### Option B — From a terminal
Open a terminal (PowerShell or CMD) and run:

```powershell
python "main\warenwelt_gui.py"
```

It does not matter from which folder you start it — the program adds the
project root to its path automatically, so the imports always work.

---

## 3. What you should see

1. A window titled **WarenWelt** opens.
2. The **Welcome** screen shows a *"Get started"* button.
   - At the bottom it says either *"Connected to database"* (MySQL found)
     or *"Offline mode (in-memory data)"* (no MySQL — this is normal and fine).
3. Click **Get started → Create one** to register a customer
   (private or company), then **Log in**.
4. Browse the **Shop**, filter by category, sort by price/name, and
   **Add to cart** products.
5. Open the **Cart**, choose a delivery option, and **Place order**.
6. An **Order confirmed** screen appears and an `invoice.txt` file is
   written to the project folder.

To close the program, just close the window.

---

## 4. Optional: using a real MySQL database

Only needed if you want products and customers stored in MySQL instead of
in memory.

1. Install the MySQL connector:
   ```
   pip install mysql-connector-python
   ```
2. Have a MySQL server running and import the schema:
   ```
   data_base/warenwelt.sql
   ```
3. Check the login data near the top of `main/warenwelt_gui.py`
   (section **DATABASE CONFIG**) — `DB_HOST`, `DB_USER`, `DB_PASSWORD`,
   `DB_NAME`, `DB_PORT` — and adjust them to your server if needed.

When MySQL is reachable, the welcome screen shows *"Connected to database"*.

---

## 5. Project structure (overview)

```
warenwelt_shop/
├─ main/
│  └─ warenwelt_gui.py        # ← START HERE (the Tkinter GUI + data access)
├─ shop_models/
│  ├─ customers/              # PrivateCustomer, CompanyCustomer
│  └─ products/               # Book, Electronics, Clothing
├─ orders/                    # ShoppingCart, Order
├─ utils/                     # Validator (input checks)
├─ data_base/
│  ├─ storage.py              # MySQL connection helper
│  └─ warenwelt.sql           # database schema
└─ tests_package/             # unit tests
```

---

### Troubleshooting

| Problem | Fix |
|---|---|
| `python` not found | Install Python from python.org and tick *"Add to PATH"*. |
| `No module named tkinter` | Reinstall Python with the *tcl/tk* option enabled. |
| Window says *"Offline mode"* | Normal if MySQL is off — the app still works with example data. |
| `ModuleNotFoundError` for project modules | Run `main/warenwelt_gui.py` directly; it fixes its own import path. |