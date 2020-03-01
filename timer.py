import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from enum import Enum
from threading import Thread
from math import modf

from time import perf_counter, sleep
from scramble import Scramble3x3, Scramble4x4

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = perf_counter()
        self.end_time = None

    def stop(self):
        self.end_time = perf_counter()

    def elapsed(self, numbers):
        now = perf_counter()
        return round(now-self.start_time, numbers)

    def time(self):
        return round(self.end_time-self.start_time,2)

class State(Enum):
    STOPPED = 0,
    READY = 1,
    RUNNING = 2

class Timer:
    def __init__(self):
        self.label = Gtk.Label("0.00")
        self.show_time(0.00, 2)
        self.state = State.STOPPED
        self.stopwatch = Stopwatch()

    def space_pressed(self, scramble):
        if self.state == State.RUNNING:
            self.stop()
            time = self.stopwatch.time()
            #scramble = scramble.copy()
            #scramble.reset()
            return (time, scramble)
            
        elif self.state == State.STOPPED:
            self.set_ready()
            return None

    def space_released(self):
        if self.state == State.READY:
            self.stopwatch.start()
            self.state = State.RUNNING
            self.t1 = Thread(target = self.run)
            self.t1.start()

    def run(self):
        while (self.state == State.RUNNING):
            now = self.stopwatch.elapsed(1)
            self.show_time(now, 1)
            self.timelaps = now
            sleep(0.1)

    def show_time(self, time, numbers):
        if time >= 60.0:
            text = "{}:{}{}".format(int(time/60), "0" if time%60<10 else "",round(time%60, numbers))
        else:
            text = str(round(time,numbers))

        self.label.set_markup("<span font_desc='Ubuntu 150'>{}</span>".format(text))

    def set_ready(self):
        self.label.set_markup("<span color='green' font_desc='Ubuntu 150'>0.0</span>")
        self.state = State.READY

    def stop(self):
        self.state = State.STOPPED
        self.stopwatch.stop()
        self.show_time(self.stopwatch.time(), 2)

    def time(self):
        return self.stopwatch.time()