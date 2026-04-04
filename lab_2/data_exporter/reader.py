import json


class JSONDataReader:
    @staticmethod
    def read(file_path) -> list:
        try:
           with open(file_path, "r") as file:
               return json.load(file)
        except FileNotFoundError:
            print(f"No file found at {file_path}.")
            return []
