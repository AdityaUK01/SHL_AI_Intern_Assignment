import json


class SHLCatalog:
    def __init__(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            self.assessments = json.load(f)

    def get_all(self):
        return self.assessments

    def count(self):
        return len(self.assessments)