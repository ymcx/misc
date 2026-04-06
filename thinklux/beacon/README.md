# Installation

In order to build and use Beacon, you'll need to have the following installed:

- D-Bus
- GCC/Clang
- Meson
- systemd

We're using systemd-logind's D-Bus interface for controlling the leds so that no additional setup/permissions are needed. If not for systemd-logind, you would either need to [run the program as root or define additional udev rules and add your user to a group](https://github.com/Hummer12007/brightnessctl#permissions).

```
meson setup build
meson compile -C build
sudo cp tlbeacon.* /etc/systemd/user/
sudo ln -s $PWD/build/tlbeacon /usr/local/bin/
systemctl enable --now --user tlbeacon.timer
```
