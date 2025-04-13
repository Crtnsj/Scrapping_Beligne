import tools.ollamaAPI as ollama
import re


def categorize(df, categories):
    return ""


def removeThinkingPart(text):
    try:
        clean_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        return clean_text
    except Exception as e:
        print(f"Error cleaning response: {e}")
        return text


def categorizeArticle(title, desc, categories):
    prompt = f"{title} - {desc}. Les categories disponibles sont: {categories}"

    response = ollama.chatToModel("Classifier", prompt)

    if response:
        cleaned_response = removeThinkingPart(response["response"])
        print(cleaned_response)
    else:
        return None


# response = ollama.chatToModel(
#     "Classifier",
#     "Couteau à bout rond en plastique, jouet. Les categories disponibles sont: Couteau de table(id:32), Couteau pliant(id:1), couteau de randonnée(id:2), couteau pour enfant(id:4)",
# )


# if response:
#     cleaned_response = removeThinkingPart(response["response"])
#     print(cleaned_response)
# else:
#     print("Failed to get response from model")
