import terminatorlib.plugin as plugin
from terminatorlib.terminator import Terminator
from gi.repository import Gtk, Gdk
import tempfile

AVAILABLE = ['OpenScrollback']

class OpenScrollback(plugin.Plugin):
    def __init__(self):
        self.current_window = Terminator().windows[0]
        self.current_window.connect('key-press-event', self.onKeyPress)

    def onKeyPress(self, widget, event):
        if (event.state & Gdk.ModifierType.MOD1_MASK == Gdk.ModifierType.MOD1_MASK) and (event.keyval == 32): # Alt+Space
            current_terminal = self.current_window.get_focussed_terminal()
            vte = current_terminal.get_vte()
            col, row = vte.get_cursor_position()
            content, _ = vte.get_text_range(0, 0, row, col, lambda *a: True)
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            with open(temp_file.name, 'w') as f:
                f.write(content)
            tab = self.current_window.tab_new()
            new_terminal = self.current_window.get_focussed_terminal()
            command = "vim " + temp_file.name + '\n'
            new_terminal.vte.feed_child(str(command).encode("utf-8"))
