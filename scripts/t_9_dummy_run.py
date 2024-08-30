import sys
import json

def load_parameters(file_name):
    with open(file=file_name, mode="r") as file:
        data = json.load(file)
    return data

def run(*args, **kwargs):
    print("Hello World!")

    for i, a in enumerate(args):
        print(f"arg {i} :{a}")

    for k, v in kwargs.items():
        print(f"key: {k} and value: {v}")

if __name__ == "__main__":
  file_name = sys.argv[1]
  
  payload = load_parameters(file_name)

  run(**payload)