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

    def save(self, storage):

        storage.execute_query(
            """
            INSERT INTO electronics
            (
                name,
                price,
                brand,
                warranty_years
            )
            VALUES (%s,%s,%s,%s)
            """,
            (
                self.name,
                self.price,
                self.brand,
                self.warranty_years
            )
        )

    @staticmethod
    def load(storage, electronic_id):

        return storage.execute_query(
            """
            SELECT *
            FROM electronics
            WHERE id_electronic=%s
            """,
            (electronic_id,)
        ).fetchone()

    @staticmethod
    def load_all(storage):

        return storage.execute_query(
            "SELECT * FROM electronics"
        ).fetchall()

    def update(self, storage, electronic_id):

        storage.execute_query(
            """
            UPDATE electronics
            SET
                name=%s,
                price=%s,
                brand=%s,
                warranty_years=%s
            WHERE id_electronic=%s
            """,
            (
                self.name,
                self.price,
                self.brand,
                self.warranty_years,
                electronic_id
            )
        )

    def delete(self, storage, electronic_id):

        storage.execute_query(
            """
            DELETE FROM electronics
            WHERE id_electronic=%s
            """,
            (electronic_id,)
        )