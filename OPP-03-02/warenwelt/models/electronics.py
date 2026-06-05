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