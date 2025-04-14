import tools.ollamaAPI as ollama
import polars as pl
import tools.dataFormatter as dataFormatter


def categorize(df):
    for row in df.iter_rows(named=True):
        title = row["title"]
        desc = row["desc"]

        categories = ""

        ps_category = dataFormatter.getRootCategories(
            "data/ps_category.csv", "data/ps_category_lang.csv"
        )

        categories = ", ".join(
            [
                f"{row['name']} (id:{row['id_category']})"
                for row in ps_category.iter_rows(named=True)
            ]
        )

        response = categorizeArticle(title, desc, categories)

        if response:
            print(response)
            response = ollama.parseResult(response)
            dftest = pl.DataFrame(response)
            print(dftest)
        else:
            print("Failed to get response from model")


def categorizeArticle(title, desc, categories):
    prompt = f"{title} - {desc}. Les categories disponibles sont: {categories}"

    response = ollama.chatToModel("Classifier", prompt)

    if response:
        cleaned_response = ollama.removeThinkingPart(response["response"])
        return cleaned_response
    else:
        return None
