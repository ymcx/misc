# ThinkLed

A tool that simply switches the power led of your Thinkpad on/off depending on the current battery capacity. Additionally, a systemd service and a timer are provided so that the tool can be automatically run in order to have the led react to the capacity in real time.

This is mostly useful for people who are not using any kind of statusbar on their Thinkpad, since doing that makes it quite hard to keep track of the remaining battery capacity.

# Installation

For compiling ThinkLed, you will need Meson, a C compiler such as GCC, systemd and D-Bus. We're using systemd-logind's D-Bus interface for controlling the led so that you are not required to set any additional udev rules or give this program higher privileges. [source](https://github.com/Hummer12007/brightnessctl#permissions)

You'll need superuser permissions for copying the systemd service and the timer to the correct directory. After that ThinkLed will work just fine without superuser permissions.

```
meson setup build
meson compile -C build
sudo cp thinkled.service /etc/systemd/user/
sudo cp thinkled.timer /etc/systemd/user/
systemctl enable --now --user thinkled.timer
```
