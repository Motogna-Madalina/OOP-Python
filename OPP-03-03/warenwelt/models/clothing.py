from warenwelt.models.product import Product


class Clothing(Product):

    def __init__(
        self,
        name,
        price,
        weight,
        size,
        color
    ):

        super().__init__(
            name,
            price,
            weight
        )

        self.size = size
        self.color = color

    def __str__(self):

        return (
            f"Clothing: {self.name} | "
            f"Size: {self.size} | "
            f"Color: {self.color}"
        )

    # =====================================
    # CLOTHING DATABASE METHODS
    # =====================================

    @staticmethod
    def save(storage, clothing):

        sql = """
        INSERT INTO Clothing
        (name, price, weight, size, color)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            clothing.name,
            clothing.price,
            clothing.weight,
            clothing.size,
            clothing.color
        )

        storage.query(sql, values)

    @staticmethod
    def load_all(storage):

        cursor = storage.query(
            "SELECT * FROM Clothing"
        )

        return cursor.fetchall()

    @staticmethod
    def load(storage, cloth_id):

        cursor = storage.query(
            """
            SELECT *
            FROM Clothing
            WHERE id_cloth = %s
            """,
            (cloth_id,)
        )

        return cursor.fetchone()