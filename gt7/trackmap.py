
import csv
import matplotlib.pyplot as plt

class TrackMap:
    def __init__(self, filename):
        self.filename = filename
        self.lats = []
        self.longs = []

    def read_data(self):
        with open(self.filename, "r") as f:
            reader = csv.reader(f)
            # Skip headers
            for _ in range(8):
                next(reader)
            
            lat_index = -1
            long_index = -1

            header = next(reader)
            for i, channel in enumerate(header):
                if channel == '"lat"':
                    lat_index = i
                elif channel == '"long"':
                    long_index = i

            if lat_index == -1 or long_index == -1:
                raise ValueError("Could not find lat and long channels in the log file")

            for row in reader:
                self.lats.append(float(row[lat_index]))
                self.longs.append(float(row[long_index]))

    def generate_map(self, output_filename="track_map.png"):
        plt.figure(figsize=(10, 10))
        plt.plot(self.longs, self.lats)
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Track Map")
        plt.savefig(output_filename)
        plt.close()

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m gt7.trackmap <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]
    track_map = TrackMap(log_file)
    track_map.read_data()
    track_map.generate_map()
