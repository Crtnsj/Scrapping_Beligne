import requests
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()

url = os.getenv("PRESTASHOP_API_URL")
api_key = os.getenv("PRESTASHOP_API_KEY")


def getArticleScheme(route):
    """
    Get the article (product) schema from PrestaShop API.

    Returns:
        ET.Element: XML element of the blank product schema, or None on failure.
    """

    headers = {"Content-Type": "application/xml"}

    response = requests.get(
        f"{url}/{route}?schema=blank",
        headers=headers,
        auth=(api_key, ""),
    )

    if response.status_code == 200:
        product_xml = ET.fromstring(response.content)
        return product_xml
    else:
        print(
            f"Echec de la recuperation du schema : {response.status_code} - {response.text}"
        )
        return None


def getRequest(route, displayFull=False):
    """
    Get a request from PrestaShop API.

    Args:
        route (str): The API route to get.

    Returns:
        ET.Element: XML element of the response, or None on failure.
    """

    headers = {"Content-Type": "application/xml"}

    response = requests.get(
        f"{url}/{route}?{'&display=full' if displayFull else ''}",
        headers=headers,
        auth=(api_key, ""),
    )

    if response.status_code == 200:
        return ET.fromstring(response.content)
    else:
        print(f"Echec de la recuperation : {response.status_code} - {response.text}")
        return None


def postRequest(route, data):
    headers = {"Content-Type": "application/xml"}

    response = requests.post(
        f"{url}/{route}",
        headers=headers,
        auth=(api_key, ""),
        data=data,
    )
