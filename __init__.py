
import os
import sys
from aqt import mw
from aqt.operations import QueryOp
from aqt.theme import theme_manager

# Add vendor dir to path so that dasbus is importable.
vendor_dir = os.path.join(os.path.dirname(__file__), "vendor")
sys.path.insert(0, vendor_dir)

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

