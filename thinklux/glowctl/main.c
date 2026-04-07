#include <stdio.h>
#include <stdlib.h>
#include <systemd/sd-bus.h>

// A pre-calculated list of brightness values calculated using
// x ^ EXPONENT * MAX, where
//   x ∈ [0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
//     A brightness of 0 makes the screen go completely dark, set it to 1
//     0.1, 0.2 are skipped since they were too close to 0.0 and 0.3
//   EXPONENT = 4
//     I tried doing some poor man's calibration using a smartphone but mostly
//     eye-balled it
//   MAX = max(BRIGHTNESS_STATES)
static const int BRIGHTNESS_STATES[] = {
    1, 196, 621, 1515, 3142, 5821, 9930, 15905, 24242,
};

int min(const int a, const int b) { return a < b ? a : b; }

int max(const int a, const int b) { return a > b ? a : b; }

// Retrieve the directory where the saved state is located at
void getStateFile(char *stateFile) {
  const char *xdg_state_home = getenv("XDG_STATE_HOME");

  // https://wiki.archlinux.org/title/XDG_Base_Directory#User_directories
  if (xdg_state_home == NULL) {
    const char *home = getenv("HOME");
    snprintf(stateFile, 100, "%s/.local/state/tlglowctl", home);
  } else {
    snprintf(stateFile, 100, "%s/tlglowctl", xdg_state_home);
  }
}

// Reads the state value from the given file
int readState(const char *stateFile) {
  FILE *file = fopen(stateFile, "rb");
  if (file == NULL) {
    // File doesn't exist
    file = fopen(stateFile, "wb");
    if (file == NULL) {
      // Unable to create the file
      return -1;
    }
  }

  int stateValue = 0;
  fread(&stateValue, sizeof(int), 1, file);
  fclose(file);
  return stateValue;
}

// Updates the state value according to the given argument
int updateState(const int stateValue, const char argument) {
  int stateAmount;

  switch (argument) {
  case '-':
    return max(stateValue - 1, 0);
  case '+':
    stateAmount = sizeof(BRIGHTNESS_STATES) / sizeof(BRIGHTNESS_STATES[0]);
    return min(stateValue + 1, stateAmount - 1);
  default:
    return stateValue;
  }
}

// Write the new state back to the file
int writeState(const char *stateFile, const int stateValue) {
  FILE *file = fopen(stateFile, "wb");
  if (file == NULL) {
    return -1;
  }

  fwrite(&stateValue, sizeof(int), 1, file);
  fclose(file);
  return 0;
}

// Sets the brightness from the given table using the given state
int setBrightness(const int stateValue) {
  sd_bus *bus;
  sd_bus_default_system(&bus);
  return sd_bus_call_method(
      bus, "org.freedesktop.login1", "/org/freedesktop/login1/session/auto",
      "org.freedesktop.login1.Session", "SetBrightness", NULL, NULL, "ssu",
      "backlight", "intel_backlight", BRIGHTNESS_STATES[stateValue]);
}

int main(const int argc, const char **argv) {
  int success, state;
  char stateFile[100];

  // We need to know if we're incrementing or decrementing the brightness
  if (argc < 2) {
    fprintf(stderr, "No action provided");
    return 0;
  }

  // Read the statefile
  getStateFile(stateFile);
  state = readState(stateFile);
  if (state < 0) {
    fprintf(stderr, "Unable to create the statefile");
    return 0;
  }

  // Write the updated state
  state = updateState(state, argv[1][0]);
  success = writeState(stateFile, state);
  if (success < 0) {
    fprintf(stderr, "Unable to write to the statefile");
    return 0;
  }

  // Set the updated brightness
  success = setBrightness(state);
  if (success < 0) {
    fprintf(stderr, "Unable to set the brightness");
    return 0;
  }
}
