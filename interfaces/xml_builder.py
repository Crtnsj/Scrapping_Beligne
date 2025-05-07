from domain.models.Article import Article


def build_xml_article(article: Article) -> str:
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
        "reference": article.ref,
        "price": str(article.price),
        "id_tax_rules_group": str(article.IDTax),
        "id_shop_default": str(article.IDShop),
        "id_category_default": str(article.defaultCat),
        "id_manufacturer": str(article.manufacturer),
        "ean13": str(article.ean),
        "weight": str(article.weight),
        "active": str(int(article.active)),
        "state": str(article.state),
    }

    for tag, value in fields.items():
        xml_parts.append(f"<{tag}><![CDATA[{value}]]></{tag}>")

    # Add language fields
    xml_parts.append(
        f'<name><language id="1"><![CDATA[{article.name}]]></language></name>'
    )
    xml_parts.append(
        f'<description><language id="1"><![CDATA[{article.description}]]></language></description>'
    )
    xml_parts.append(
        f'<description_short><language id="1"><![CDATA[{article.recap}]]></language></description_short>'
    )

    xml_parts.append("</product>")
    xml_parts.append("</prestashop>")

    return "".join(xml_parts)
