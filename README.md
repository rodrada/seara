
<h1 align="center">
  Anki Dark Mode Fix
</h1>

![Showcase GIF](examples/clip.gif)

# What's this for?

On Linux, Anki does not immediately detect modifications in the system's theme polarity (light/dark mode).
Instead, it polls for the new value every 5 minutes.

This add-on allows Anki to instantly react to those changes by suscribing to updates to the
`org.freedesktop.appearance.color-scheme` property on D-Bus.
