
import json

class Config:
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.data = {}
        self.load()

    def load(self):
        try:
            with open(self.filename, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {
                "ps_ip": "",
                "port": 33740,
                "imperial": False,
                "log_dir": "logs"
            }
            self.save()

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()
