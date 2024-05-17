/* SPDX-License-Identifier: GPL-2.0-only */

#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/io.h>

void send_ec_data(uint8_t data) {
  int timeout = 0x7ff;
  while ((inb(0x66) & 2) && --timeout) {
    usleep(10);
  }
  outb(data, 0x62);
}

void ec_write(uint8_t data) {
  outb(0x81, 0x66);
  send_ec_data(12);
  send_ec_data(data);
}

int main() {
  iopl(3);
  FILE * file = fopen("/sys/class/power_supply/BAT0/capacity", "r");
  int battery = 0;
  while (1) {
    fscanf(file, "%i", &battery);
    if (battery <= 10) {
      ec_write(192);
    } else if (battery <= 50) {
      ec_write(160);
      if (battery <= 15) {
        sleep(60);
        continue;
      }
    } else {
      ec_write(128);
    }
    sleep(900);
  }
  fclose(file);
  return 0;
}
