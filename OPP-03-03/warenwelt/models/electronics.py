from warenwelt.models.product import Product


class Electronics(Product):

    def __init__(
        self,
        name,
        price,
        weight,
        brand,
        warranty_years
    ):

        super().__init__(
            name,
            price,
            weight
        )

        self.brand = brand
        self.warranty_years = warranty_years

    def __str__(self):

        return (
            f"Electronics: {self.name} | "
            f"Brand: {self.brand}"
        )

    # =====================================
    # ELECTRONICS DATABASE METHODS
    # =====================================

    @staticmethod
    def save(storage, electronics):

        sql = """
        INSERT INTO Electronics
        (name, price, weight, brand, warranty_years)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            electronics.name,
            electronics.price,
            electronics.weight,
            electronics.brand,
            electronics.warranty_years
        )

        storage.query(sql, values)

    @staticmethod
    def load_all(storage):

        cursor = storage.query(
            "SELECT * FROM Electronics"
        )

        return cursor.fetchall()

    @staticmethod
    def load(storage, electronic_id):

        cursor = storage.query(
            """
            SELECT *
            FROM Electronics
            WHERE id_electronic = %s
            """,
            (electronic_id,)
        )

        return cursor.fetchone()