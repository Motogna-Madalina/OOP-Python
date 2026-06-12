"""
This class represents books.
"""

from shop_models.products.product import Product


class Book(Product):

    def __init__(
            self,
            name,
            price,
            author,
            page_count
    ):

        super().__init__(name, price)

        self.author = author
        self.page_count = page_count

    def get_author(self):
        return self.author

    def get_page_count(self):
        return self.page_count

    def set_author(self, author):
        self.author = author

    def set_page_count(self, page_count):
        self.page_count = page_count

    def save(self, storage):

        storage.execute_query(
            """
            INSERT INTO books
            (
                name,
                price,
                author,
                page_count
            )
            VALUES (%s,%s,%s,%s)
            """,
            (
                self.name,
                self.price,
                self.author,
                self.page_count
            )
        )

    @staticmethod
    def load(storage, book_id):

        return storage.execute_query(
            """
            SELECT *
            FROM books
            WHERE id_book=%s
            """,
            (book_id,)
        ).fetchone()

    @staticmethod
    def load_all(storage):

        return storage.execute_query(
            "SELECT * FROM books"
        ).fetchall()

    def update(self, storage, book_id):

        storage.execute_query(
            """
            UPDATE books
            SET
                name=%s,
                price=%s,
                author=%s,
                page_count=%s
            WHERE id_book=%s
            """,
            (
                self.name,
                self.price,
                self.author,
                self.page_count,
                book_id
            )
        )

    def delete(self, storage, book_id):

        storage.execute_query(
            """
            DELETE FROM books
            WHERE id_book=%s
            """,
            (book_id,)
        )