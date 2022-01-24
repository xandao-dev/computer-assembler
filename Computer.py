from DatabaseManager import Database

product_types = {
    "Keyboard": "Keyboard",
    "Mouse": "Mouse",
    "Headphone": "Headphone",
    "Monitor": "Monitor",
    "CPU": "CPU",
    "GPU": "GPU",
    "PSU": "PSU",
    "Storage": "Storage",
    "RAM": "RAM",
    "Motherboard": "Motherboard",
    "Cooler": "Cooler",
    "Case": "Case",
    "Operating System": "Operating System"}
currency_symbols = {"real": "R$"}
db = Database()


class AddProduct():
    def __init__(
            self,
            product_type: str,
            model: str,
            brand: str,
            currency_symbol: str,
            price: float,
            description: str = '',
            link: str = ''):
        self.product_type = product_type
        self.model = model
        self.brand = brand
        self.currency_symbol = currency_symbol
        self.price = price
        self.description = description
        self.link = link
        self.__validate_data()
        db.insert_product(self.get_tuple())

    def __validate_data(self):
        if not self.product_type in product_types.values():
            raise ValueError(
                'Wrong part_type, see product_type dict in Computer.py')
        if not self.currency_symbol in currency_symbols.values():
            raise ValueError(
                'Wrong currency symbol, see currency_symbols dict in Computer.py')
        # Converting money to cents
        self.price = int(self.price*100)

    # To add in database
    def get_tuple(self):
        return (
            self.product_type,
            self.model,
            self.brand,
            self.currency_symbol,
            self.price,
            self.description,
            self.link)

    """
    # To print
    def get_dict(self):
        return {
            "Product": self.product_type,
            "Model": self.model,
            "Brand": self.brand,
            "Price": self.price,
            "Currency Symbol": self.currency_symbol,
            "Description": self.description,
            "Link": self.link
        }

    def print_data(self):
        data = self.get_dict()
        data.pop('Currency Symbol')
        for key in data:
            if data[key] == '':
                continue
            if key == 'Price':
                print(f' \t\t{key} -> {self.currency_symbol} {data[key]}')
            elif key == 'Product':
                print(f' \t{key} -> {data[key]}')
            else:
                print(f' \t\t{key} -> {data[key]}')
    """


class AssembleComputer():
    def __init__(self, name: str, currency_symbol: str, description: str = '', parts: tuple = tuple()):
        self.name = name
        self.currency_symbol = currency_symbol
        self.description = description
        self.parts = parts
        self.__validate_data()
        self.__calculate_price_total()
        db.insert_computer(self.get_tuple())

    def __validate_data(self):
        if not self.currency_symbol in currency_symbols.values():
            raise ValueError(
                'Wrong currency symbol, see currency_symbols dict in Computer.py')

    def __calculate_price_total(self):
        self.price_total = 0

    def get_tuple(self):
        return (
            self.name,
            self.currency_symbol,
            self.price_total,
            self.description)

    """
    def get_computer_price(self):
        price = 0
        for part in self.parts:
            price += part.price
        return price

    def print_data(self):
        print(f'\nComputer ID: 0')
        for part in self.parts:
            part.print_data()
        print(
            f'Final Price: {part.currency_symbol} {self.get_computer_price()}\n')
    """
