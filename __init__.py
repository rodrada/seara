
import os
import sys
import asyncio
from aqt import mw
from aqt.operations import QueryOp
from aqt.theme import theme_manager

# Add vendor dir to path so that dbus_fast is importable.
vendor_dir = os.path.join(os.path.dirname(__file__), "vendor")
sys.path.insert(0, vendor_dir)

from dbus_fast.aio import MessageBus

async def bus_listener():

    bus = await MessageBus().connect()
    introspection = await bus.introspect(
        "org.freedesktop.portal.Desktop",
        "/org/freedesktop/portal/desktop"
    )

    obj = bus.get_proxy_object(
        "org.freedesktop.portal.Desktop",
        "/org/freedesktop/portal/desktop",
        introspection
    )
    settings = obj.get_interface("org.freedesktop.portal.Settings")

    def callback(path, setting, value):
        # Reload theme if the light/dark mode property has changed value.
        if path == "org.freedesktop.appearance" and setting == "color-scheme":
            aqt.mw.taskman.run_on_main(
                lambda: theme_manager.apply_style()
            )

    settings.on_setting_changed(callback)

    await asyncio.Event().wait()

dbus_op = QueryOp(
    parent=mw,
    op=lambda _: asyncio.run(bus_listener()),
    success=lambda: pass    # Don't do anything on listener exit.
)

dbus_op.run_in_background()

