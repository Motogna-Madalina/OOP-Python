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

    # Implementation of the abstract Product contract.

    @property
    def category(self):
        return "Books"

    def short_detail(self):
        return f"by {self.author}, {self.page_count} pages"

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
    # load()      -> get ONE book by its id  (returns one row)
    # load_all()  -> get ALL books           (returns a list of rows)
    # ==================================================================

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
