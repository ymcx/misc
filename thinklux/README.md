# ThinkLux

This repository contains two tools: ThinkLux Beacon and ThinkLux Glowctl, both of which can be found from their own subdirectories.

As a sidenote, the names for these programs were generated using GPT-5.3, since I'm not creative enough to come up with my own names.

# ThinkLux Beacon

Beacon is a program that simply fetches the remaining battery capacity and turns on the power led of your Thinkpad if the capacity is below a given threshold.

A systemd timer is provided for making the program run periodically so that it doesn't have to be manually executed each time to be of any use.

Beacon is mostly useful for people who are not using any kind of statusbar on their laptop and as such can't really keep track of their remaining battery life.

# ThinkLux Glowctl

Glowctl is a tool that controls your screen's brightness using the exact same method as brightnessctl. The difference is that the brightness levels are hardcoded and that they are set via systemd-logind only, since most people are running systemd anyway.

The motivation for creating this tool was that, since we're creating a tool for controlling the brightness of a led via systemd-logind, why not do the same for the screen brightness which is done using the same interface?

Moreover, by hardcoding the brightness values we can simply not worry about the wonkiness that brightnessctl has to deal with when trying to set a brightness while having an exponent set.
