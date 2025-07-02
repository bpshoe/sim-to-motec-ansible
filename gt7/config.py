
import yaml

class Config:
    def __init__(self, filename="config.yml"):
        self.filename = filename
        self.data = {}
        self.load()

    def load(self):
        try:
            with open(self.filename, "r") as f:
                self.data = yaml.safe_load(f)
        except FileNotFoundError:
            self.data = {
                "ps_ip": "",
                "ports": {
                    "heartbeat": 33739,
                    "telemetry": 33740
                },
                "schema_version": 3,
                "salsa20_key": "Simulator Interface Packet GT7 ver 0.0",
                "heartbeat_interval": 1.5,
                "output": {
                    "csv": True,
                    "motec": True
                }
            }
            self.save()

    def save(self):
        with open(self.filename, "w") as f:
            yaml.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()
