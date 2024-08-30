import json

def load_parameters(file_name):
    with open(file=file_name, mode="r") as file:
        data = json.load(file)
    return data

def save_parameters(data, file_name):
    with open(file=file_name, mode="w") as file:
        json.dump(data, file)
