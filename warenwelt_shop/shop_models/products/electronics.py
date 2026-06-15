"""
This class represents electronic products.
"""

from shop_models.products.product import Product


class Electronics(Product):

    def __init__(
            self,
            name,
            price,
            brand,
            warranty_years
    ):

        super().__init__(name, price)

        self.brand = brand
        self.warranty_years = warranty_years

    def get_brand(self):
        return self.brand

    def get_warranty_years(self):
        return self.warranty_years

    def set_brand(self, brand):
        self.brand = brand

    def set_warranty_years(self, warranty_years):
        self.warranty_years = warranty_years

    # ==================================================================
    # >>> DATABASE METHODS (READ ELECTRONICS FROM MYSQL) <<<
    # These methods ASK the database for electronics (SELECT).
    # load()      -> get ONE item by its id  (returns one row)
    # load_all()  -> get ALL items           (returns a list of rows)
    # ==================================================================

    @staticmethod
    def load(storage, electronic_id):

        return storage.execute_query(
            """
            SELECT *
            FROM electronics
            WHERE id_electronic=%s   -- only the item with this id
            """,
            (electronic_id,)         # value for %s (safe)
        ).fetchone()                 # one row only

    @staticmethod
    def load_all(storage):

        return storage.execute_query(
            "SELECT * FROM electronics"  # every electronic item
        ).fetchall()                     # a list of rows