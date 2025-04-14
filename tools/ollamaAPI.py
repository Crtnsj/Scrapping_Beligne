import requests
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()


def createModelFromJson(file_path):
    """
    Create a model from a JSON file.
    Args:
        file_path (str): Path to the JSON file containing model data.
    Returns:
        bool: True if the model was created successfully, False otherwise.
    """
    with open(file_path, "r") as file:
        json_data = json.load(file)
    response = requests.post(os.getenv("OLLAMA_BASE_URL") + "create", json=json_data)
    if response.status_code == 200:
        print("Model created successfully.")
        return True
    else:
        print(f"Failed to create model: {response.status_code} - {response.text}")
        return False


def chatToModel(model_name, prompt):
    """
    Send a prompt to the model and get the response.
    Args:
        model_name (str): The name of the model to chat with.
        prompt (str): The prompt to send to the model.
    Returns:
        dict: The response from the model.
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7,
    }
    response = requests.post(
        os.getenv("base_url") + "generate", headers=headers, json=data
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to chat with model: {response.status_code} - {response.text}")
        return None


def removeThinkingPart(text):
    """
    Remove the <think> part from the response text.
    Args:
        text (str): The response text from the model.
    Returns:
        str: The cleaned text without the <think> part.
    """

    try:
        clean_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        clean_text = clean_text.replace("\n", "")
        return clean_text
    except Exception as e:
        print(f"Error cleaning response: {e}")
        return text


def parseResult(response):
    """
    Parse the response from the model to extract categories.
    Args:
        response (str): The response text from the model.
    Returns:
        list: A list of dictionaries containing category IDs and names.
    """

    matches = re.findall(r"id\s*:\s*(\d+),\s*nom\s*:\s*([^\]]+)", response)

    result = [{"id": int(id_), "nom": nom.strip()} for id_, nom in matches]

    return result
