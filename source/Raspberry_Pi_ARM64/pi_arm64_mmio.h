// Copyright (c) 2014 Adafruit Industries
// Author: Tony DiCola
// ARM64 compatibility implementation

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
#ifndef PI_ARM64_MMIO_H
#define PI_ARM64_MMIO_H

#include <stdint.h>

#define MMIO_SUCCESS      0
#define MMIO_ERROR_DEVMEM 1
#define MMIO_ERROR_MMAP   2
#define MMIO_ERROR_OFFSET 3

extern volatile uint32_t* pi_arm64_mmio_gpio;

int pi_arm64_mmio_init(void);
static inline void pi_arm64_mmio_set_input(int pin) {
  // Set pin as input by clearing bits in function select register.
  if (pi_arm64_mmio_gpio != NULL && pin >= 0 && pin <= 31) {
    *(pi_arm64_mmio_gpio + ((pin)/10)) &= ~(7<<(((pin)%10)*3));
  }
}
static inline void pi_arm64_mmio_set_output(int pin) {
  // First set as input to clear any previous value, then set as output.
  if (pi_arm64_mmio_gpio != NULL && pin >= 0 && pin <= 31) {
    pi_arm64_mmio_set_input(pin);
    *(pi_arm64_mmio_gpio + ((pin)/10)) |=  (1<<(((pin)%10)*3));
  }
}
static inline void pi_arm64_mmio_set_high(int pin) {
  if (pi_arm64_mmio_gpio != NULL && pin >= 0 && pin <= 31) {
    *(pi_arm64_mmio_gpio + 7) = 1 << pin;
  }
}
static inline void pi_arm64_mmio_set_low(int pin) {
  if (pi_arm64_mmio_gpio != NULL && pin >= 0 && pin <= 31) {
    *(pi_arm64_mmio_gpio + 10) = 1 << pin;
  }
}
static inline uint32_t pi_arm64_mmio_input(int pin) {
  if (pi_arm64_mmio_gpio != NULL && pin >= 0 && pin <= 31) {
    return (*(pi_arm64_mmio_gpio + 13) & (1 << pin)) >> pin;
  }
  return 0;
}

#endif