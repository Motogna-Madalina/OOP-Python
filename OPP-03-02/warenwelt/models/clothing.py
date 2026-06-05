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