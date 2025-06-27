

import io
import logging
from datetime import datetime

from stm.motec.data_log import DataLog
from stm.motec.motec_log import MotecLog

l = logging.getLogger(__name__)

class MoTeCWriter:
    def __init__(self, filetemplate=None, imperial=False, frequency=60.0):
        self.filetemplate = filetemplate if filetemplate else "motec_log_{datetime}.ld"
        self.imperial = imperial
        self.frequency = frequency
        self.buffer = None
        self.channels = []
        self.event = {}
        self.last_sample = []

    def new_log(self, channels, event):
        self.channels = channels
        # add a beacon channel for lap markers
        self.channels.append({'name': 'Beacon', 'units': ''})
        self.event = event
        self.buffer = io.StringIO()
        # write the header
        self.buffer.write(','.join(['Time'] + [c.get('name', c) for c in self.channels]) + '\n')
        l.info("In-memory log buffer initialized")

    def add_samples(self, timestamp, samples):
        if self.buffer:
            # add a 0 for the beacon channel
            self.last_sample = [timestamp] + samples + [0]
            self.buffer.write(','.join(map(str, self.last_sample)) + '\n')

    def add_lap(self, laptime, lap):
        if self.buffer:
            l.info(f"Adding new lap to MoTeC log: {lap} with time: {laptime}")
            # MoTeC uses a beacon channel to mark laps
            # We write the last known sample again, but with the beacon channel set to 1
            lap_sample = self.last_sample[:]
            lap_sample[-1] = 1 # set beacon
            self.buffer.write(','.join(map(str, lap_sample)) + '\n')

    def save_log(self):
        if not self.buffer or not self.channels:
            l.warning("save_log called with no data to save.")
            return

        l.info("Starting MoTeC .ld file generation")
        
        # Get the CSV data from our in-memory buffer
        self.buffer.seek(0)
        csv_lines = self.buffer.getvalue().splitlines()

        if len(csv_lines) < 2:
            l.warning("No data samples to write to MoTeC log.")
            self.reset()
            return

        # Create our data log from the CSV data
        data_log = DataLog()
        l.info("Extracting data from buffer...")
        data_log.from_csv_log(csv_lines)

        if not data_log.channels:
            l.error("Failed to find any channels in log data")
            self.reset()
            return

        l.info(f"Parsed {data_log.duration():.1f}s log with {len(data_log.channels)} channels")
        
        # Resample all channels to a fixed frequency
        l.info(f"Resampling channels to {self.frequency}Hz")
        data_log.resample(self.frequency)

        # Create and populate the MoTeC log object
        motec_log = MotecLog()
        motec_log.driver = self.event.get("driver", "")
        motec_log.vehicle_id = self.event.get("vehicle", "")
        motec_log.venue_name = self.event.get("venue", "")
        motec_log.event_session = self.event.get("session", "")
        motec_log.short_comment = f"Track: {self.event.get('track', 'Unknown')}"
        
        # You can add more metadata here if needed
        # motec_log.vehicle_weight = 0
        # motec_log.vehicle_type = ""
        # motec_log.vehicle_comment = ""
        # motec_log.event_name = ""
        # motec_log.long_comment = ""

        motec_log.initialize()
        motec_log.add_all_channels(data_log)

        # Generate filename and write the file
        filename = self.filetemplate.format(datetime=datetime.now().strftime("%Y%m%d_%H%M%S"))
        l.info(f"Saving MoTeC log to {filename}")
        motec_log.write(filename)
        
        l.info("MoTeC log file saved successfully.")
        self.reset()

    def update_event(self, event):
        l.info(f"Updating event data: {event}")
        self.event.update(event)

    def reset(self):
        self.buffer = None
        self.channels = []
        self.event = {}
        self.last_sample = []
        l.info("MoTeCWriter state has been reset.")

