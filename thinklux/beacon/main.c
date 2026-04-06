#include <stdio.h>
#include <systemd/sd-bus.h>
#include <unistd.h>

static const int BLINK_REPEAT = 5;
static const int BLINK_SLEEP = 1;
static const int THRESHOLD = 15;

// Read the battery capacity from a file
int getCapacity(void) {
  int capacity;

  // Assuming BAT0
  FILE *file = fopen("/sys/class/power_supply/BAT0/capacity", "rb");
  fscanf(file, "%d", &capacity);
  fclose(file);

  return capacity;
}

// Set the power led on/off
void setLed(const int state) {
  // Use the D-Bus interface provided by systemd-logind instead
  // of requiring superuser permissions or any additional udev rules
  sd_bus *bus;
  sd_bus_default_system(&bus);
  sd_bus_call_method(bus, "org.freedesktop.login1",
                     "/org/freedesktop/login1/session/auto",
                     "org.freedesktop.login1.Session", "SetBrightness", NULL,
                     NULL, "ssu", "leds", "tpacpi::power", state);
}

// Turn the led on/off a couple of times to attract attention
void blinkLed(void) {
  for (int i = 0; i < BLINK_REPEAT; ++i) {
    setLed(1);
    sleep(BLINK_SLEEP);
    setLed(0);
    sleep(BLINK_SLEEP);
  }
}

int main(void) {
  const int capacity = getCapacity();
  const int state = capacity <= THRESHOLD;

  if (state) {
    blinkLed();
  }

  setLed(state);
}
