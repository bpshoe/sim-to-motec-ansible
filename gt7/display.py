
import curses

class Display:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.timeout(100)

    def update(self, data):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "GT7 Telemetry")

        row = 2
        for key, value in data.items():
            self.stdscr.addstr(row, 0, f"{key}: {value}")
            row += 1

        self.stdscr.refresh()

    def run(self, callback):
        while True:
            key = self.stdscr.getch()
            if key == ord('q'):
                break

            data = callback()
            if data:
                self.update(data)
