


import time
import logging
import curses
import threading
from gt7.sampler import GT7Sampler
from gt7.telemetry import GT7Logger
from gt7.display import Display
from gt7.config import Config

def display_thread(display, logger):
    display.run(logger.get_latest_data)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Load configuration
    config = Config()

    # Create a sampler to receive telemetry data
    sampler = GT7Sampler(addr=config.get("ps_ip"), port=config.get("port"))

    # Create a logger to process and save the data
    logger = GT7Logger(sampler=sampler, imperial=config.get("imperial"))

    # Set the logger as the callback for the sampler
    sampler.callback = lambda timestamp, sample: logger.process_sample(timestamp, sample)

    # Start the sampler
    sampler.start()

    print("GT7 Telemetry Logger started. Press Ctrl+C to stop.")

    # Initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    try:
        display = Display(stdscr)
        # Run display in a separate thread
        display_thread = threading.Thread(target=display_thread, args=(display, logger))
        display_thread.start()

        while display_thread.is_alive():
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping GT7 Telemetry Logger...")
    finally:
        # Clean up curses
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

        sampler.stop()
        sampler.join()
        logger.save_log()
        print("GT7 Telemetry Logger stopped.")


