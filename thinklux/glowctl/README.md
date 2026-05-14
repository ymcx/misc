# Installation

In order to build and use Glowctl, you'll need to have the following installed:

- D-Bus
- GCC/Clang
- Meson
- systemd

Before building Glowctl, you will need to modify the source code by setting your own brightness levels, since your laptop most likely doesn't have the same brightness curve nor the same maximum brightness.

You can check your screen's maximum brightness from /sys/class/backlight/\[NAME\]/max_brightness, where \[NAME\] needs to be replaced with the actual value. In my case, it is 'intel_backlight', but [it might also be 'acpi_video0' or something else altogether](https://wiki.archlinux.org/title/Backlight#ACPI).

We're using systemd-logind's D-Bus interface for controlling the leds so that no additional setup/permissions are needed. If not for systemd-logind, you would either need to [run the program as root or define additional udev rules and add your user to a group](https://github.com/Hummer12007/brightnessctl#permissions).

```
$EDITOR main.c # define your own brightness levels (mandatory)
meson setup build
meson compile -C build
sudo ln -s $PWD/build/tlglowctl /usr/local/bin/
```

# Usage

You can increase the brightness by passing '+' to the program and likewise decrease the brightness by passing '-':

```
tlglowctl + # increase the brightness
tlglowctl - # decrease the brightness
```
