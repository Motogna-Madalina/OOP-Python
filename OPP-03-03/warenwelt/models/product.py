from abc import ABC, abstractmethod


class Product(ABC):

    next_id = 1

    def __init__(self, name, price, weight):

        self.id_product = Product.next_id
        Product.next_id += 1

        self.name = name
        self.price = price
        self.weight = weight

    # Metodo abstracto: cada subclase DEBE definir su propio __str__.
    # Esto es lo que impide instanciar Product directamente.
    @abstractmethod
    def __str__(self):
        pass