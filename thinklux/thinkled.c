#include <stdio.h>
#include <systemd/sd-bus.h>

#define THRESHOLD 10

int main(void) {
  // Read the battery capacity from a file
  // Assuming BAT0
  int capacity;
  FILE *file = fopen("/sys/class/power_supply/BAT0/capacity", "rb");
  fscanf(file, "%d", &capacity);
  fclose(file);

  // The power button led should be on if
  // the capacity is lower than the threshold
  const int led_on = capacity <= THRESHOLD;

  // Use the D-Bus interface provided by systemd-logind instead
  // of requiring superuser permissions or any additional udev rules
  sd_bus *bus;
  sd_bus_default_system(&bus);
  sd_bus_call_method(bus, "org.freedesktop.login1",
                     "/org/freedesktop/login1/session/auto",
                     "org.freedesktop.login1.Session", "SetBrightness", NULL,
                     NULL, "ssu", "leds", "tpacpi::power", led_on);
}
