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

    # ==================================================================
    # >>> DATABASE METHODS (READ BOOKS FROM MYSQL) <<<
    # These methods ASK the database for books (SELECT).
    # load()      -> get ONE book by its id  (returns one row)
    # load_all()  -> get ALL books           (returns a list of rows)
    # ==================================================================

    @staticmethod
    def load(storage, book_id):

        return storage.execute_query(
            """
            SELECT *
            FROM books
            WHERE id_book=%s         -- only the book with this id
            """,
            (book_id,)               # value for %s (safe)
        ).fetchone()                 # one row only

    @staticmethod
    def load_all(storage):

        return storage.execute_query(
            "SELECT * FROM books"    # every book
        ).fetchall()                 # a list of rows