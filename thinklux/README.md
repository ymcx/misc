# This repository contains two tools: ThinkLed and ThinkBright, both of which can be found from their own subdirectories.

# ThinkLed

A tool that simply switches the power led of your Thinkpad on/off depending on the current battery capacity. Additionally, a systemd service and a timer are provided so that the tool can be automatically run in order to have the led react to the capacity in real time.

This is mostly useful for people who are not using any kind of statusbar on their Thinkpad, since doing that makes it quite hard to keep track of the remaining battery capacity.

# ThinkBright

A tool you can use to set the screen brightness via systemd-logind's D-Bus interface.
