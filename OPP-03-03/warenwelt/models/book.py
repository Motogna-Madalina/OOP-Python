from warenwelt.models.product import Product


class Book(Product):

    def __init__(
        self,
        name,
        price,
        weight,
        author,
        page_count
    ):

        super().__init__(
            name,
            price,
            weight
        )

        self.author = author
        self.page_count = page_count

    def __str__(self):

        return (
            f"Book: {self.name} | "
            f"Author: {self.author} | "
            f"Pages: {self.page_count}"
        )

    # =====================================
    # BOOK DATABASE METHODS
    # =====================================

    @staticmethod
    def save(storage, book):

        sql = """
        INSERT INTO Book
        (name, price, weight, author, page_count)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            book.name,
            book.price,
            book.weight,
            book.author,
            book.page_count
        )

        storage.query(sql, values)

    @staticmethod
    def load_all(storage):

        cursor = storage.query(
            "SELECT * FROM Book"
        )

        return cursor.fetchall()

    @staticmethod
    def load(storage, book_id):

        cursor = storage.query(
            """
            SELECT *
            FROM Book
            WHERE id_book = %s
            """,
            (book_id,)
        )

        return cursor.fetchone()