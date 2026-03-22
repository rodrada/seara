
<h1 align="center">
  Seară
  <div>
  <sub><sup>/ˈse̯arə/</sup></sub>
  </div>
</h1>

https://github.com/user-attachments/assets/f4e5ebf1-910f-4288-84ad-7fb0d3a31fad

# What's this for?

On Linux, Anki does not immediately detect modifications in the system's theme polarity (light/dark mode).
Instead, it polls for the new value every 5 minutes.

This add-on allows Anki to instantly react to those changes by subscribing to updates to the
`org.freedesktop.appearance.color-scheme` property on D-Bus.

# Installation

## NixOS (using Flakes and Home Manager)

Add the following to your flake inputs:

```nix
anki-seara.url = "github:rodrada/seara";
```

Then, in your Anki configuration:

```nix
programs.anki.addons = [
    inputs.anki-seara.packages."x86_64-linux".default
];
```

## Other distros

The easiest way to install the add-on is to download it from [AnkiWeb](https://ankiweb.net/shared/info/1080056423).

However, if you do not want to do so, you can simply get the .zip from the latest GitHub release and extract it in your Anki add-on directory.
