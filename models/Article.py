import xml.etree.ElementTree as ET
import requests


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
        group: int,
        defaultCat: int,
        manufacturer: int,
        ean: str,
        weight: float,
        chars: dict,
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
        self.group = group
        self.defaultCat = defaultCat
        self.manufacturer = manufacturer
        self.ean = ean
        self.weight = weight
        self.chars = chars
        self.active = active
        self.state = state

    def transformToXML(self) -> str:
        """
        Transform the article to XML format.
        Returns:
            str: XML representation of the article.
        """
        # Build XML string manually to properly handle CDATA sections
        xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_parts.append('<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">')
        xml_parts.append("<product>")

        # Add simple fields with CDATA
        fields = {
            "reference": self.ref,
            "price": str(self.price),
            "id_tax_rules_group": str(self.IDTax),
            "id_shop_default": str(self.IDShop),
            "id_category_default": str(self.defaultCat),
            "id_manufacturer": str(self.manufacturer),
            "ean13": str(self.ean),
            "weight": str(self.weight),
            "active": str(int(self.active)),
            "state": str(self.state),
        }

        for tag, value in fields.items():
            xml_parts.append(f"<{tag}><![CDATA[{value}]]></{tag}>")

        # Add language fields
        xml_parts.append(
            f'<name><language id="1"><![CDATA[{self.name}]]></language></name>'
        )
        xml_parts.append(
            f'<description><language id="1"><![CDATA[{self.description}]]></language></description>'
        )
        xml_parts.append(
            f'<description_short><language id="1"><![CDATA[{self.recap}]]></language></description_short>'
        )

        xml_parts.append("</product>")
        xml_parts.append("</prestashop>")

        return "".join(xml_parts)

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

    def sendToPrestashop(self, url: str, api_key: str) -> bool:
        """
        Send the article to PrestaShop API.
        Args:
            url (str): The PrestaShop API URL.
            api_key (str): The PrestaShop API key.
        Returns:
            bool: True if the article was sent successfully, False otherwise.
        """
        headers = {"Content-Type": "application/xml"}
        data = self.transformToXML()

        response = requests.post(
            f"{url}/products",
            headers=headers,
            auth=(api_key, ""),
            data=data,
        )
        print(f"Response: {response.status_code} - {response.text}")
        return response.status_code == 201


# Example usage
test = Article(
    "test",
    "test",
    1.0,
    "test",
    "test",
    1,
    1,
    1,
    1,
    1,
    "1234567890123",
    1.0,
    {},
    True,
    1,
)
if test.validate():
    test2 = test.transformToXML()
    test3 = test.sendToPrestashop(
        "http://localhost:8080/api/", "8PUU9Z9QCUH3R73MSSRYPT4IDL65XLMB"
    )
    print(test2)
    print(test3)
else:
    print("Invalid article attributes")
