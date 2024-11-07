/* SPDX-License-Identifier: GPL-2.0-only */

#include <cstdlib>
#include <stdio.h>

int main() {
  int data;
  FILE * file = fopen("/sys/class/power_supply/BAT0/capacity", "r");
  fscanf(file, "%i", &data);
  fclose(file);
  if (data <= 5) {
    system("echo '0 blink' > /proc/acpi/ibm/led");
  }
  else if (data <= 50) {
    system("echo '0 on' > /proc/acpi/ibm/led");
  }
  else {
    system("echo '0 off' > /proc/acpi/ibm/led");
  }
  return 0;
}
