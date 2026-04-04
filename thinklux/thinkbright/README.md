# Installation

For compiling ThinkBright, you will need Meson, a C compiler such as GCC, systemd and D-Bus. We're using systemd-logind's D-Bus interface for controlling the led so that you are not required to set any additional udev rules or give this program higher privileges. [source](https://github.com/Hummer12007/brightnessctl#permissions)

```
meson setup build
meson compile -C build
./build/thinkbright +
./build/thinkbright -
```
