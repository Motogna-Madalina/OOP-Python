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

    # Implementation of the abstract Product contract.

    @property
    def category(self):
        return "Clothing"

    def short_detail(self):
        return f"size {self.size}, {self.color}"

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
    # ==================================================================

    @staticmethod
    def load(storage, clothing_id):

        return storage.execute_query(
            """
            SELECT *
            FROM clothing
            WHERE id_clothing=%s
            """,
            (clothing_id,)
        ).fetchone()

    @staticmethod
    def load_all(storage):

        return storage.execute_query(
            "SELECT * FROM clothing"
        ).fetchall()
