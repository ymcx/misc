#include <math.h>
#include <stdio.h>
#include <systemd/sd-bus.h>

// I found the exponent by trial & error along with using my smartphone as a
// poor man's calibration tool.
static const double EXPONENT = 4.0;
static const double MAX = 24242.0;

// Pre-calculated list of brightness values calculated using
// x ^ EXPONENT * MAX, where x ∈ [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0].
// The change from 0.0 to 0.3 is unnoticable so we don't include it.
static const int BRIGHTNESS_LEVELS[8] = {
    196, 621, 1515, 3142, 5821, 9930, 15905, 24242,
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
  return round(scaled * 10.0) - 3.0;
}

// Reads the argument and increments/decrements it accordingly.
// The value is additionally clamped to [0, 10].
int updateLevel(const int level, const char arg) {
  switch (arg) {
  case '-':
    return max(level - 1, 0);
  case '+':
    return min(level + 1, 7);
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
