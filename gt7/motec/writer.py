

import csv
import logging
from datetime import datetime

l = logging.getLogger(__name__)

class MoTeCWriter:
    def __init__(self, filetemplate=None, imperial=False):
        self.filetemplate = filetemplate if filetemplate else "motec_log_{datetime}.csv"
        self.imperial = imperial
        self.log_file = None
        self.writer = None

    def new_log(self, channels, event):
        filename = self.filetemplate.format(datetime=datetime.now().strftime("%Y%m%d_%H%M%S"))
        l.info(f"Creating new MoTeC log file: {filename}")
        self.log_file = open(filename, "w", newline="")
        self.writer = csv.writer(self.log_file)

        # Write MoTeC headers
        self.writer.writerow(["MoTeC i2 Data"])
        self.writer.writerow(["Venue", event.get("venue", "")])
        self.writer.writerow(["Vehicle", event.get("vehicle", "")])
        self.writer.writerow(["Driver", event.get("driver", "")])
        self.writer.writerow(["Date", datetime.now().strftime("%Y/%m/%d")])
        self.writer.writerow(["Time", datetime.now().strftime("%H:%M:%S")])
        self.writer.writerow([]) # Blank line

        # Write channel units
        self.writer.writerow([c.get("name", c) for c in channels])
        self.writer.writerow([c.get("units", "") for c in channels])

    def add_samples(self, samples):
        if self.writer:
            self.writer.writerow(samples)

    def add_lap(self, laptime, lap):
        if self.writer:
            l.info(f"Adding new lap to MoTeC log: {lap} with time: {laptime}")
            # MoTeC uses a beacon channel to mark laps
            # We can add a beacon sample here
            pass

    def save_log(self):
        if self.log_file:
            l.info(f"Saving MoTeC log file")
            self.log_file.close()
            self.log_file = None
            self.writer = None

    def update_event(self, event):
        # This is more complex in a CSV file as the headers are already written
        # For now, we will not support updating the event after the log has started
        pass

