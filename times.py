import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from enum import Enum
from scramble import *

# Box orientation
HORIZONTAL = 0
VERTICAL = 1

class Penalty(Enum):
    OK = 0,
    PLUS2 = 1,
    DNF = 2

class OptionsWindow(Gtk.Window):
    def __init__(self, solve):
        super().__init__()
        self.connect("destroy", self.close)
        self.set_size_request(300, 200)
        self.set_title("Solve info")
        self.content = Gtk.Box(orientation = Gtk.Orientation(VERTICAL), spacing = 5)
        self.scramble_label = Gtk.Label(str(solve.scramble))
        self.time_label = Gtk.Label(solve.time_str())
        self.scramble_label.set_selectable(True)
        self.time_label.set_selectable(True)
        self.content.pack_start(child = self.scramble_label, expand = True,
                                fill = True, padding = 0)
        self.content.pack_start(child = self.time_label, expand = True,
                                fill = True, padding = 0)

        # self.button_box = Gtk.Box()
        # self.button_ok = Gtk.Button("OK")
        # self.button_ok.connect("clicked", self.set_ok)
        self.add(self.content)
        self.show_all()

    def close(self, window):
        self.destroy()

class SolveInfo:
    def __init__(self, time, scramble):
        self.time = time
        self.penalty = Penalty.OK
        self.scramble = scramble
        self.box = Gtk.Box()
        self.options = Gtk.Button("options")
        self.label = Gtk.Label("")
        self.show()
        self.box.pack_start(child = self.label, expand = True,
                                fill = True, padding = 0)

        self.box.pack_start(child = self.options, expand = False,
                                fill = False, padding = 0)
        
        self.options.connect("clicked", self.button_clicked)

        self.label.show_all()
        self.box.show_all()

    def hide_all(self):
        self.label.set_text("")
        #self.options.hide_all()

    def show_all(self):
        self.label.set_text(self.time_str())
        #self.options.show_all()

    def button_clicked(self, button):
        self.window = OptionsWindow(self)

    def show(self):
        text = self.time_str() 
        spaces = 15 - len(text)

        self.label.set_text(text+spaces*" "+"|")

    def time_str(self):
        time = self.time
        if self.penalty == Penalty.PLUS2:
            time+=2
        
        if self.penalty == Penalty.DNF:
            text = "DNF"
        elif time >= 60.0:
            text = "{}:{}{}".format(int(time/60), "0" if time%60<10 else "",round(time%60, numbers))
        else:
            text = str(round(time,2))

        if self.penalty == Penalty.PLUS2:
            text += "+"
        
        return text
        
class TimeList:
    def __init__(self):
        self.content = Gtk.Box(orientation= Gtk.Orientation(VERTICAL), spacing = 3)
        self.time_list = []
        self.visible = True

    def add_time(self, time, scramble):
        self.time_list.append(SolveInfo(time, scramble))
        self.content.pack_start(child = self.time_list[-1].box, expand = False,
                                fill = False, padding = 2)

    def hide(self):
        for time in self.time_list:
            time.hide_all()
        self.visible = False
    
    def show(self):
        for time in self.time_list:
            time.show_all()
        self.visible = True

    def switch_visible(self):
        if self.visible:
            self.hide()
        else:
            self.show()
    