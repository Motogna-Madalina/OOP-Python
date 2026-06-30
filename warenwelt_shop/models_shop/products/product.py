from abc import ABC, abstractmethod

from utils.validator import Validator
from exceptions.shop_error import ShopError



class Product(ABC):


    def __init__(self, name, price, weight):
        # The id is None - we will make it in MySql (AUTO_INCREMENT).
        self._id = None
        self._name = None
        self._price = None
        self._weight = None

        self.set_name(name)
        self.set_price(price)
        self.set_weight(weight)


    @abstractmethod
    def get_category(self):
        pass

    #id-----------------------------------------------------------------

    def get_id(self):
        return self._id

    #name----------------------------------------------------------------

    def get_name(self):
        return self._name

    def set_name(self, name):
        if not Validator.validate_text(name):
            raise ShopError(f"Ungültiger Produktname: {name}")
        self._name = name

    #--------------------------------------------------------------------

    def get_price(self):
        return self._price

    def set_price(self, price):
        if not Validator.validate_price(price):
            raise ShopError(f"Ungültiger Preis (muss >= 0 sein): {price}")
        self._price = price

    #weight-----------------------------------------------------------------

    def get_weight(self):
        return self._weight

    def set_weight(self, weight):
        if not Validator.validate_weight(weight):
            raise ShopError(f"Ungültiges Gewicht (muss > 0 sein): {weight}")
        self._weight = weight

    # ==========================================================================================

    # ----------------------------------------------------------------
    # LOAD ONE PRODUCT


    @staticmethod
    def load(storage, product_id):
        from models_shop.products.electronic import Electronic
        from models_shop.products.clothing import Clothing
        from models_shop.products.book import Book

        query = """
        SELECT *
        FROM product
        WHERE id = %s
        """

        result = storage.fetch_query(query, (product_id,))

        if not result:
            return None

        product = result[0]

        #----------------------------------------------------------------
        # ELECTRONIC


        query = """
        SELECT *
        FROM electronic
        WHERE product_id = %s
        """

        result = storage.fetch_query(query, (product_id,))

        if result:

            row = result[0]

            electronic = Electronic(
                product["name"],
                product["price"],
                product["weight"],
                row["brand"],
                row["warranty_years"]
            )

            electronic._id = product["id"]

            return electronic

        # ----------------------------------------------------------------
        # CLOTHING


        query = """
        SELECT *
        FROM clothing
        WHERE product_id = %s
        """

        result = storage.fetch_query(query, (product_id,))

        if result:

            row = result[0]

            clothing = Clothing(
                product["name"],
                product["price"],
                product["weight"],
                row["size"],
                row["color"]
            )

            clothing._id = product["id"]

            return clothing

        #----------------------------------------------------------------
        # BOOK


        query = """
        SELECT *
        FROM book
        WHERE product_id = %s
        """

        result = storage.fetch_query(query, (product_id,))

        if result:

            row = result[0]

            book = Book(
                product["name"],
                product["price"],
                product["weight"],
                row["author"],
                row["pages"]
            )

            book._id = product["id"]

            return book

        return None

    #----------------------------------------------------------------
    # LOAD ALL PRODUCTS
    

    @staticmethod
    def load_all(storage):

        query = """
        SELECT id
        FROM product
        ORDER BY id
        """

        results = storage.fetch_query(query)

        products = []

        for row in results:

            product = Product.load(storage, row["id"])

            if product:
                products.append(product)

        return products