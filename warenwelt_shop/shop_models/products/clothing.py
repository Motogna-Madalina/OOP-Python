"""
This class represents clothing products.
"""

from shop_models.products.product import Product


class Clothing(Product):

    def __init__(
            self,
            name,
            price,
            size,
            color
    ):

        super().__init__(name, price)

        self.size = size
        self.color = color

    def get_size(self):
        return self.size

    def get_color(self):
        return self.color

    def set_size(self, size):
        self.size = size

    def set_color(self, color):
        self.color = color

    # ==================================================================
    # >>> DATABASE METHODS (READ CLOTHING FROM MYSQL) <<<
    # These methods ASK the database for clothing (SELECT).
    # load()      -> get ONE item by its id  (returns one row)
    # load_all()  -> get ALL items           (returns a list of rows)
    # ==================================================================

    @staticmethod
    def load(storage, clothing_id):

        return storage.execute_query(
            """
            SELECT *
            FROM clothing
            WHERE id_clothing=%s     -- only the item with this id
            """,
            (clothing_id,)           # value for %s (safe)
        ).fetchone()                 # one row only

    @staticmethod
    def load_all(storage):

        return storage.execute_query(
            "SELECT * FROM clothing"  # every clothing item
        ).fetchall()                  # a list of rows