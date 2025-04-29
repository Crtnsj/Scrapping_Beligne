from models.Article import Article

import tools.prestashopAPI as prestashop


def createArticles(articles):
    return ""


def createArticle(df):
    article = Article(
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

    article.sendToPrestashop()
