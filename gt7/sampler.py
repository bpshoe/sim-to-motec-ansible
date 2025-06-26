
import socket
import threading
import logging

l = logging.getLogger(__name__)

class GT7Sampler(threading.Thread):
    def __init__(self, addr="0.0.0.0", port=33740, freq=60):
        super().__init__()
        self.addr = addr
        self.port = port
        self.freq = freq
        self.socket = None
        self.running = False
        self.callback = None

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.addr, self.port))
        self.socket.settimeout(1)
        self.running = True

        l.info(f"Listening for GT7 telemetry on {self.addr}:{self.port}")

        while self.running:
            try:
                data, addr = self.socket.recvfrom(4096)
                if self.callback:
                    self.callback(data)
            except socket.timeout:
                continue
            except Exception as e:
                l.error(f"Error receiving telemetry data: {e}")

        self.socket.close()
        l.info("GT7 telemetry listener stopped")

    def stop(self):
        self.running = False
