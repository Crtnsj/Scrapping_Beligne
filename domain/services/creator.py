from domain.models.Article import Article
from infrastructure.prestashopAPI import PrestaShopAPI
import polars as pl
import requests


def createArticles(articles: pl.DataFrame, api: PrestaShopAPI):
    for row in articles.iter_rows(named=True):
        brand_search = api.searchBrandByName(row["brand"]).findall(".//manufacturer")
        if not len(brand_search):
            id_brand = int(
                api.createBrand(row["brand"])
                .findall(".//manufacturer")[0]
                .find("id")
                .text
            )
        else:
            id_brand = int(brand_search[0].find("id").text)
        id_taxe = api.searchIDTaxByPercentage(20)
        try:
            article = Article(
                ref=row["ref"],
                name=row["title"],
                price=2,
                description=row["desc"],
                recap="",
                IDTax=id_taxe,
                IDShop=1,
                defaultCat=2,
                manufacturer=id_brand,
                ean="",
                weight=1.0,
                chars="",
                pics="",
                active=1,
                state=1,
            )
        except Exception as e:
            print(e)
        article.generateGenericEAN()
        product_id = api.createArticle(article)
        # print(product_id)
        # api.addPicFromURL(
        #     product_id,
        #     "https://st3.depositphotos.com/29384342/34039/i/450/depositphotos_340396576-stock-photo-yellow-spring-dandelion-inflorescence-which.jpg",
        # )
