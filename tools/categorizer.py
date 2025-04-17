import tools.ollamaAPI as ollama
import polars as pl
import tools.dataFormatter as dataFormatter


def categorize(df):
    for i in range(0, 30, 1):
        for row in df.iter_rows(named=True):
            title = row["title"]
            desc = row["desc"]

            categories = ""

            ps_category = dataFormatter.getRootCategories(
                "data/ps_category.csv", "data/ps_category_lang.csv"
            )

            categories = (
                ps_category.select("id_category", "name")
                .to_pandas()
                .to_markdown(index=False)
            )

            response = categorizeArticle(title, desc, categories)

            if response:
                print(f"Response: {response}")
                response = ollama.parseResult(response)
                # response to dataframe
                df_stats = pl.read_csv("data/stats.csv")
                df_response = pl.DataFrame(response)

                pl.concat([df_stats, df_response]).write_csv("data/stats.csv")

                first_category = response[1]["nom"]
                if response:
                    print(f"Article: {title} | Categorie: {first_category}")
                    relevance = evaluateRelevance(title, desc, first_category)
                    if relevance:
                        print(f"Relevance: {relevance}")
                    else:
                        print("Failed to evaluate relevance")
                else:
                    print("Failed to parse response")

            else:
                print("Failed to get response from model")


def categorizeArticle(title, desc, categories):
    prompt = f"""{title} - {desc}. 
    
Les categories disponibles sont: 
    
{categories}"""

    print(prompt)
    response = ollama.chatToModel("Classifier", prompt)

    if response:
        cleaned_response = ollama.removeThinkingPart(response["response"])
        return cleaned_response
    else:
        return None


def evaluateRelevance(title, desc, categorie):
    """
    Evaluate the relevance of the categories to the article.
    Args:
        title (str): The title of the article.
        desc (str): The description of the article.
        categories (list): The list of categories to evaluate.
    Returns:
        str: The evaluated relevance.
    """
    prompt = f"Titre de l'article : {title} | Description : {desc}. La categorie proposée est : {categorie}"
    response = ollama.chatToModel("Evaluator", prompt)
    if response:
        cleaned_response = ollama.removeThinkingPart(response["response"])
        return cleaned_response
    else:
        return None
