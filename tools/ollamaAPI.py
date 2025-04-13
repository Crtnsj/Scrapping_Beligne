import requests
import json

base_url = "http://localhost:11434/api/"


def createModelFromJson(file_path):
    with open(file_path, "r") as file:
        json_data = json.load(file)
    response = requests.post(base_url + "create", json=json_data)
    if response.status_code == 200:
        print("Model created successfully.")
        return True
    else:
        print(f"Failed to create model: {response.status_code} - {response.text}")
        return False


def chatToModel(model_name, prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7,
    }
    response = requests.post(base_url + "generate", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to chat with model: {response.status_code} - {response.text}")
        return None
