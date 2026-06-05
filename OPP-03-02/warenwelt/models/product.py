from abc import ABC


class Product(ABC):

    _id_counter = 1

    def __init__(self, name, price, weight):

        self.id = Product._id_counter
        Product._id_counter += 1

        self.name = name
        self.price = price
        self.weight = weight

    def __str__(self):

        return (
            f"ID: {self.id} | "
            f"Name: {self.name} | "
            f"Price: {self.price}"
        )