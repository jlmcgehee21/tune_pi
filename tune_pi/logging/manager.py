import time
import json

class LogManager:
    def __init__(self, readers):
        self.readers = readers

        self.log = []

    def run(self, run_time):
        start = time.time()
        curr_time = start
        while curr_time - start < run_time:

            for reader in self.readers:
                for chan in reader.channels:
                    curr_time = time.time()
                    reading = reader.read(chan)
                    parsed = reader.parser_callback(reading)
                    parsed['time'] = curr_time - start
                    self.log.append(parsed)

    def save(self, fname):
        with open(fname, 'w') as out_file:
            out_string = json.dumps(self.log)
            out_file.write(out_string)


