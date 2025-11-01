import os
import sys
import asyncio
import threading
from aqt import mw, gui_hooks
from aqt.theme import theme_manager

# Add vendor dir to path so that dbus_fast is importable.
vendor_dir = os.path.join(os.path.dirname(__file__), "vendor")
sys.path.insert(0, vendor_dir)

from dbus_fast.aio import MessageBus

# --- Globals to manage the background thread and event loop ---
dbus_thread = None
dbus_loop = None
profile_close_event = None


async def bus_listener():
    """The main coroutine that listens for DBus signals."""
    global profile_close_event

    try:
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
                # mw.taskman is thread-safe and designed for this
                mw.taskman.run_on_main(
                    lambda: theme_manager.apply_style()
                )

        settings.on_setting_changed(callback)

        # Wait until the profile is closed
        await profile_close_event.wait()

    except Exception as e:
        # It's good practice to log errors in background tasks
        print(f"Anki DBus listener error: {e}")
    finally:
        # Disconnect from the bus if possible
        if 'bus' in locals() and bus.connected:
            bus.disconnect()
        if dbus_loop and dbus_loop.is_running():
            dbus_loop.stop()


def run_dbus_loop():
    """This function is the target for our background thread."""
    global dbus_loop, profile_close_event

    # Create and set a new event loop for this thread
    dbus_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(dbus_loop)

    # Create the event that will be used for signaling
    profile_close_event = asyncio.Event()

    # Schedule our main coroutine to run
    dbus_loop.create_task(bus_listener())
    
    # Run the event loop until it's stopped from the main thread
    dbus_loop.run_forever()

    # Clean up after the loop is stopped
    dbus_loop.close()
    dbus_loop = None


def on_profile_open():
    """Starts the background thread when a profile is opened."""
    global dbus_thread
    # Ensure no previous thread is running
    if dbus_thread is None:
        dbus_thread = threading.Thread(target=run_dbus_loop, daemon=True)
        dbus_thread.start()


def on_profile_close():
    """Stops the background thread and event loop when the profile closes."""
    global dbus_thread, dbus_loop, profile_close_event

    if dbus_loop and dbus_loop.is_running():
        # Set the event to allow bus_listener() to finish
        dbus_loop.call_soon_threadsafe(profile_close_event.set)

    if dbus_thread:
        # Wait for the thread to fully terminate
        dbus_thread.join()
        dbus_thread = None


gui_hooks.profile_did_open.append(on_profile_open)
gui_hooks.profile_will_close.append(on_profile_close)
