
import os
import sys
from aqt import mw
from aqt.operations import QueryOp
from aqt.theme import theme_manager

# Add vendor dir to path so that dasbus is importable.
vendor_dir = os.path.join(os.path.dirname(__file__), "vendor")
sys.path.insert(0, vendor_dir)

try:
    # This import will fail if the user doesn't have PyGObject installed
    from gi.repository import GLib

    from dasbus.connection import SessionMessageBus
    from dasbus.loop import EventLoop

    def bus_listener_thread():

        bus = SessionMessageBus()
        loop = EventLoop()

        proxy = bus.get_proxy(
            "org.freedesktop.impl.portal.Settings",   # Bus name
            "/org/freedesktop/portal/desktop",        # Object path
        )

        def callback(path, setting, value):
            # Reload theme if the light/dark mode property has changed value.
            if path == "org.freedesktop.appearance" and setting == "color-scheme":
                theme_manager.apply_style()

        proxy.SettingChanged.connect(callback)

        loop.run()

    dbus_op = QueryOp(
        parent = mw,
        op=lambda _: bus_listener_thread()
    )

    dbus_op.run_in_background()

except ImportError:

    from aqt.utils import showWarning

    msg = """
        <b>Anki Dark Mode Fix failed to load</b><br><br>
        This add-on requires system libraries for D-Bus communication and will only work on Linux.
        <br><br>
        Please install the Python GI bindings using your system's package manager.
        <br><br>
        After installing, please restart Anki.
    """
    showWarning(msg, parent=mw, textFormat="rich")

