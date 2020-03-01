import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from timer import Timer
from threading import Thread
from scramble import Scramble3x3, Scramble4x4, Scramble2x2, Scramble
from times import TimeList

# Box orientation
HORIZONTAL = 0
VERTICAL = 1

class TimerWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.connect("destroy", Gtk.main_quit)
        self.set_title("Speedcubing timer")
        self.set_size_request(800, 600)

        self.content = Gtk.Box(orientation = Gtk.Orientation(VERTICAL), spacing = 0)
        self.add(self.content)
        self.timer = Timer()
        self.scramble = Scramble3x3()
        self.scramble.reset()
        event_list = ["2x2", "3x3", "4x4"]

        self.events = Gtk.ListStore(str)

        for event in event_list:
            self.events.append([event])

        choice_box = Gtk.Box()

        self.event_choice = Gtk.ComboBox.new_with_model(self.events)
        self.modify_sensitive = True
        self.event_choice.set_size_request(100,20)
        self.event_choice.connect("changed", self.change_event)
        renderer_text = Gtk.CellRendererText()
        self.event_choice.pack_start(renderer_text, True)
        self.event_choice.add_attribute(renderer_text, "text", 0)

        choice_box.pack_start(child = Gtk.Label(), expand = True,
                                fill = True, padding = 0)

        choice_box.pack_start(child = self.event_choice, expand = True,
                                fill = True, padding = 0)

        choice_box.pack_start(child = Gtk.Label(), expand = True,
                                fill = True, padding = 0)

        self.content.pack_start(child = choice_box,expand = False,
                                fill = False, padding = 0)
        self.content.pack_start(child = self.scramble.label,expand = False,
                                fill = False, padding = 0)

        self.time_list = TimeList()
        self.hor_box = Gtk.Box()

        self.hor_box.pack_start(child = self.time_list.content ,expand = False,
                                fill = False, padding = 0)

        self.hor_box.pack_start(child = self.timer.label,expand = True,
                                fill = False, padding = 0)

        self.content.pack_start(child = self.hor_box,expand = True,
                                fill = False, padding = 0)

        footer_box = Gtk.Box()

        self.content.pack_start(child = footer_box,expand = False,
                                fill = False, padding = 0)

        for _ in range(3):
           footer_box.pack_start(child = Gtk.Label(""), expand = True,
                                fill = True, padding = 0)

        footer_box.pack_start(child = self.scramble.cube.draw, expand = True,
                                fill = True, padding = 0)

        self.connect("key-press-event", self.key_pressed)
        self.connect("key-release-event", self.key_released)

        self.show_all()


    def key_pressed(self, widget, event):
        if event.keyval == Gdk.KEY_space:
            self.hide_show()
            self.modify_sensitive = False
            result = self.timer.space_pressed(self.scramble)
            if result:
                (time, scramble) = result
                self.time_list.add_time(time, scramble)
                scramble.reset()
            #self.show_all()

    def key_released(self, widget, event):
        if event.keyval == Gdk.KEY_space:
            self.modify_sensitive = True
            self.timer.space_released()

    def hide_show(self, widget = None):
        if self.modify_sensitive:
            sensitive = self.event_choice.get_sensitive()
            self.event_choice.set_sensitive(not sensitive)
            self.event_choice.props.visible = not self.event_choice.props.visible
            self.scramble.switch_visible()
            

    def change_event(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            event = model[tree_iter][0]
            label = self.scramble.label
            if event == "2x2":
                self.scramble = Scramble2x2(label)
            elif event == "3x3":
                self.scramble = Scramble3x3(label)
            elif event == "4x4":
                self.scramble = Scramble4x4(label)