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

    def save(self, storage):

        storage.execute_query(
            """
            INSERT INTO clothing
            (
                name,
                price,
                size,
                color
            )
            VALUES (%s,%s,%s,%s)
            """,
            (
                self.name,
                self.price,
                self.size,
                self.color
            )
        )

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

    def update(self, storage, clothing_id):

        storage.execute_query(
            """
            UPDATE clothing
            SET
                name=%s,
                price=%s,
                size=%s,
                color=%s
            WHERE id_clothing=%s
            """,
            (
                self.name,
                self.price,
                self.size,
                self.color,
                clothing_id
            )
        )

    def delete(self, storage, clothing_id):

        storage.execute_query(
            """
            DELETE FROM clothing
            WHERE id_clothing=%s
            """,
            (clothing_id,)
        )