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