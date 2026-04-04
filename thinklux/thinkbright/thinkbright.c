#include <math.h>
#include <stdio.h>
#include <systemd/sd-bus.h>

static const double EXPONENT = 2.2;
static const double MAX = 24242.0;
static const int BRIGHTNESS_LEVELS[11] = {
    // Pre-calculated list of brightness values calculated using x^EXPONENT.
    // The minimum brightness is set to 1, since 0 turns off the screen.
    1, 153, 703, 1715, 3229, 5276, 7880, 11061, 14838, 19227, 24242,
};

int min(const int a, const int b) { return a < b ? a : b; }

int max(const int a, const int b) { return a > b ? a : b; }

// Reads the current brightness value, transforms it using the given exponent
// and discretizes it.
int getLevel(void) {
  int brightness;
  FILE *file = fopen("/sys/class/backlight/intel_backlight/brightness", "rb");
  fscanf(file, "%d", &brightness);
  fclose(file);

  const double scaled = pow((double)brightness / MAX, 1.0 / EXPONENT);
  return round(scaled * 10.0);
}

// Reads the argument and increments/decrements it accordingly.
// The value is additionally clamped to [0, 10].
int updateLevel(const int level, const char arg) {
  switch (arg) {
  case '-':
    return max(level - 1, 0);
  case '+':
    return min(level + 1, 10);
  default:
    return level;
  }
}

// Sets the brightness from the given table.
// The brightness is set via D-Bus so that we don't need root permissions.
void setLevel(const int level) {
  sd_bus *bus;
  sd_bus_default_system(&bus);
  sd_bus_call_method(
      bus, "org.freedesktop.login1", "/org/freedesktop/login1/session/auto",
      "org.freedesktop.login1.Session", "SetBrightness", NULL, NULL, "ssu",
      "backlight", "intel_backlight", BRIGHTNESS_LEVELS[level]);
}

int main(const int argc, const char **argv) {
  // We need to know if we're incrementing or decrementing the brightness.
  if (argc < 2) {
    return 0;
  }

  int level = getLevel();
  level = updateLevel(level, argv[1][0]);
  setLevel(level);
}
