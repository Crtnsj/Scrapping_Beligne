import random


class Article:
    def __init__(
        self,
        ref: str,
        name: str,
        price: float,
        description: str,
        recap: str,
        IDTax: int,
        IDShop: int,
        defaultCat: int,
        manufacturer: int,
        ean: str,
        weight: float,
        chars: str,
        pics: str,
        active: bool,
        state: int,
    ):
        self.ref = ref
        self.name = name
        self.price = price
        self.description = description
        self.recap = recap
        self.IDTax = IDTax
        self.IDShop = IDShop
        self.defaultCat = defaultCat
        self.manufacturer = manufacturer
        self.ean = ean
        self.weight = weight
        self.chars = chars
        self.pics = pics
        self.active = active
        self.state = state

    def validate(self) -> bool:
        """
        Validate the article's attributes.
        Returns:
            bool: True if all attributes are valid, False otherwise.
        """
        if not self.ref or not isinstance(self.ref, str):
            return False
        if not self.name or not isinstance(self.name, str):
            return False
        if self.price <= 0 or not isinstance(self.price, (int, float)):
            return False
        if not isinstance(self.active, bool):
            return False
        # Add more validation rules as needed
        return True

    def generateGenericEAN(self) -> bool:
        code = str(random.randint(100000000000, 999999999999))
        prefix = "00000"
        code = prefix + code
        code = code[: -len(prefix)]

        code_partials = list(map(int, code))
        checkdigit = None
        even_numbers = 0
        odd_numbers = 0

        for key, value in enumerate(code_partials):
            if (key + 1) % 2 == 0:
                even_numbers += value
            else:
                odd_numbers += value

        even_numbers = even_numbers * 3
        total = even_numbers + odd_numbers

        if total % 10 == 0:
            checkdigit = 0
        else:
            next_multiple = total + (10 - total % 10)
            checkdigit = next_multiple - total

        code += str(checkdigit)
        self.ean = code
