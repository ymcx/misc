/* SPDX-License-Identifier: GPL-2.0-only */

#include <iostream>
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

int main(int argc, char * argv[]) {
  iopl(3);
  int data;
  if (argv[1] == NULL) {
    FILE * file = fopen("/sys/class/power_supply/BAT0/capacity", "r");
    fscanf(file, "%i", &data);
    fclose(file);
    data = 192 - (data + 34) / 45 * 32;
  } else {
    data = atoi(argv[1]);
  }
  ec_write(data);
  return 0;
}
