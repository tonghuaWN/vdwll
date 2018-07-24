import gi
import Pyro4
import time

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
from playbin_player import VideoPlayer as playbin_player


@Pyro4.expose
class RemoteCommander(object):
    """
    The Pyro object that interfaces with the GUI application.
    """

    def __init__(self, gui):
        self.gui = gui

    def message(self, messagetext):
        # Add the message to the screen.
        # Note that you can't do anything that requires gui interaction
        # (such as popping a dialog box asking for user input),
        # because the gui (tkinter) is busy processing this pyro call.
        # It can't do two things at the same time when embedded this way.
        # If you do something in this method call that takes a long time
        # to process, the GUI is frozen during that time (because no GUI update
        # events are handled while this callback is active).
        self.gui.add_message("from Pyro: " + messagetext)

    def sleep(self, duration):
        # Note that you can't perform blocking stuff at all because the method
        # call is running in the gui mainloop thread and will freeze the GUI.
        # Try it - you will see the first message but everything locks up until
        # the sleep returns and the method call ends
        self.gui.add_message("from Pyro: sleeping {0} seconds...".format(duration))
        time.sleep(duration)
        self.gui.add_message("from Pyro: woke up!")

    def add_image(self):
        self.gui.add_image()

    def move_widget(self, xpos, ypos, name):
        # self.gui.move_widget(xpos, ypos, name)
        fixed_widget = self.gui.mainWindow.get_child()
        children = fixed_widget.get_children()
        print(children)
        for child in children:
            print("name :", child.get_name())
            if child.get_name() == name:
                fixed_widget.move(child, xpos, ypos)

    def resize(self, width, height, name):
        fixed_widget = self.gui.mainWindow.get_child()
        children = fixed_widget.get_children()
        print(children)
        for child in children:
            print("name :", child.get_name())

            if child.get_name() == name:
                child.set_size_request(width, height)

    def remove_widget(self, name):
        fixed_widget = self.gui.mainWindow.get_child()
        children = fixed_widget.get_children()
        print(children)
        for child in children:
            print("name :", child.get_name())
            if child.get_name() == name:
                fixed_widget.remove(child)

    def add_source(self, uri, xpos, ypos, width, heigth, name):
        # self.gui.add_source(uri, xpos, ypos, width, heigth, name)
        container = self.gui.mainWindow.get_child()
        videowidget = Gtk.DrawingArea(name=name)
        videowidget.set_halign(Gtk.Align.START)
        videowidget.set_valign(Gtk.Align.START)
        videowidget.set_size_request(width, heigth)
        videowidget.show()
        playbin_player(uri=uri, moviewindow=videowidget)
        container.put(videowidget, xpos, ypos)
