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
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "pi_arm64_mmio.h"

#define GPIO_BASE_OFFSET 0x200000
#define GPIO_LENGTH 4096

volatile uint32_t* pi_arm64_mmio_gpio = NULL;

int pi_arm64_mmio_init(void) {
  if (pi_arm64_mmio_gpio == NULL) {
    // Check for GPIO and peripheral addresses from device tree.
    // This approach works for ARM64 systems including Pi 4/5
    FILE *fp = fopen("/proc/device-tree/soc/ranges", "rb");
    uint32_t peri_base = 0;
    uint32_t gpio_base = 0;
    
    if (fp != NULL) {
      // Try to read peripheral base from device tree
      fseek(fp, 4, SEEK_SET);
      unsigned char buf[4];
      if (fread(buf, 1, sizeof(buf), fp) == sizeof(buf)) {
        peri_base = buf[0] << 24 | buf[1] << 16 | buf[2] << 8 | buf[3] << 0;
        gpio_base = peri_base + GPIO_BASE_OFFSET;
      }
      fclose(fp);
    }
    
    // Fallback addresses for different Pi models
    if (peri_base == 0) {
      // Try Pi 4/5 default address (ARM64)
      peri_base = 0xFE000000;  // Pi 4/5 peripheral base
      gpio_base = peri_base + GPIO_BASE_OFFSET;
    }

    int fd;
    
    // On newer systems, /dev/gpiomem should exist and be user-accessible
    if (access("/dev/gpiomem", F_OK) != -1) {
      fd = open("/dev/gpiomem", O_RDWR | O_SYNC);
      if (fd != -1) {
        // For /dev/gpiomem, offset should be 0 as it maps directly to GPIO
        pi_arm64_mmio_gpio = (uint32_t*)mmap(NULL, GPIO_LENGTH, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
      }
    } else {
      // Fallback to /dev/mem (requires root)
      fd = open("/dev/mem", O_RDWR | O_SYNC);
      if (fd != -1) {
        // For /dev/mem, use the calculated GPIO base address
        pi_arm64_mmio_gpio = (uint32_t*)mmap(NULL, GPIO_LENGTH, PROT_READ | PROT_WRITE, MAP_SHARED, fd, gpio_base);
      }
    }
    
    if (fd == -1) {
      // Error opening device file
      return MMIO_ERROR_DEVMEM;
    }
    
    close(fd);
    
    if (pi_arm64_mmio_gpio == MAP_FAILED) {
      // Don't save the result if the memory mapping failed.
      pi_arm64_mmio_gpio = NULL;
      return MMIO_ERROR_MMAP;
    }
  }
  return MMIO_SUCCESS;
}