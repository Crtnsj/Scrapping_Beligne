import requests
import xml.etree.ElementTree as ET
from domain.models.Article import Article
from interfaces.xml_builder import build_xml_article
from io import BytesIO
import tempfile


class PrestaShopAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def getArticleScheme(self, route):
        """
        Get the article (product) schema from PrestaShop API.

        Returns:
            ET.Element: XML element of the blank product schema, or None on failure.
        """

        headers = {"Content-Type": "application/xml"}

        response = requests.get(
            f"{self.base_url}/{route}?schema=blank",
            headers=headers,
            auth=(self.api_key, ""),
        )

        if response.status_code == 200:
            product_xml = ET.fromstring(response.content)
            return product_xml
        else:
            print(
                f"Echec de la recuperation du schema : {response.status_code} - {response.text}"
            )
            return None

    def getRequest(self, route, displayFull=False):
        """
        Get a request from PrestaShop API.

        Args:
            route (str): The API route to get.

        Returns:
            ET.Element: XML element of the response, or None on failure.
        """

        headers = {"Content-Type": "application/xml"}

        response = requests.get(
            f"{self.base_url}/{route}?{'&display=full' if displayFull else ''}",
            headers=headers,
            auth=(self.api_key, ""),
        )

        if response.status_code == 200:
            return ET.fromstring(response.content)
        else:
            print(
                f"Echec de la recuperation : {response.status_code} - {response.text}"
            )
            return None

    def postRequest(self, route, data):
        headers = {"Content-Type": "application/xml"}

        response = requests.post(
            f"{self.base_url}/{route}",
            headers=headers,
            auth=(self.api_key, ""),
            data=data,
        )

    def createArticle(self, article: Article):
        xml_data = build_xml_article(article)
        headers = {"Content-Type": "application/xml"}

        response = requests.post(
            f"{self.base_url}/products",
            headers=headers,
            auth=(self.api_key, ""),
            data=xml_data,
        )
        if response.status_code == 201:
            product_id = ET.fromstring(response.content).find("product").find("id").text
            return product_id

    def addPicFromPath(self, product_id, path_file):
        with open(path_file, "rb") as image_file:
            files = {"image": image_file}
            image_res = requests.post(
                f"{self.base_url}/images/products/{product_id}",
                files=files,
                auth=(self.api_key, ""),
            )

            if image_res.status_code == 201:
                print("✅ Image ajoutée au produit")
            else:
                print("❌ Erreur lors de l’ajout de l’image :", image_res.content)

    def addPicFromURL(self, product_id, url):
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "").lower()

            if "jpeg" in content_type or "jpg" in content_type:
                file_ext = "jpg"
                mime_type = "image/jpeg"
            elif "png" in content_type:
                file_ext = "png"
                mime_type = "image/png"
            elif "gif" in content_type:
                file_ext = "gif"
                mime_type = "image/gif"
            else:
                print(f"Format d'image non supporté: {content_type}")
                return

            # Écrire l’image sur un fichier temporaire
            with tempfile.NamedTemporaryFile(suffix=f".{file_ext}") as tmp_file:
                tmp_file.write(response.content)
                tmp_file.flush()  # S’assurer que tout est écrit

                with open(tmp_file.name, "rb") as img_file:
                    files = {"image": (f"image.{file_ext}", img_file, mime_type)}

                    headers = {"Accept": "application/xml"}

                    upload_response = requests.post(
                        f"{self.base_url}/images/products/{product_id}",
                        files=files,
                        headers=headers,
                        auth=(self.api_key, ""),
                    )

            if upload_response.status_code in [200, 201]:
                print("Image ajoutée avec succès !")
            else:
                print(
                    f"Erreur upload image: {upload_response.status_code} - {upload_response.text}"
                )
        else:
            print(f"Erreur téléchargement image: {response.status_code}")

    def searchBrandByName(self, brand_name):
        response = requests.get(
            f"{self.base_url}/manufacturers?display=full&filter[name]=[{brand_name.title()}]",
            auth=(self.api_key, ""),
        )
        xml = ET.fromstring(response.text)
        return xml

    def createBrand(self, brand_name):
        data = f"""<?xml version="1.0" encoding="UTF-8"?>
                        <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
                            <manufacturer>
                                <name>{brand_name.title()}</name>
                            </manufacturer>
                        </prestashop>
                """
        response = requests.post(
            f"{self.base_url}/manufacturers",
            data=data,
            auth=(self.api_key, ""),
        )
        xml = ET.fromstring(response.text)
        return xml

    def searchFeatureByName(self, feature_name):
        response = self.getRequest("product_features", True)
        available_features = response.findall(".//product_feature")
        for feature in available_features:
            texte = feature.find(".//language").text
            if feature_name == texte:
                return True
        return False

    def searchIDTaxByPercentage(self, percentage):
        response = self.getRequest("taxes", True)
        available_taxes = response.findall(".//tax")
        for tax in available_taxes:
            rate = float(tax.find(".//rate").text)
            if rate == percentage:
                tax_id = tax.find(".//id").text
                return tax_id
        raise ValueError(f"Aucune taxe trouvée avec un taux de {percentage}%")
