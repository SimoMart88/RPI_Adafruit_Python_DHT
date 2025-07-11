#!/usr/bin/env python3
"""
Example usage of the ARM64-compatible DHT library.
This demonstrates how to use the library on ARM64 Raspberry Pi systems.
"""

import Adafruit_DHT

# Sensor should be set to Adafruit_DHT.DHT22,
# Adafruit_DHT.DHT11, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22

# Example using pin 4 (you can use any available GPIO pin)
pin = 4

def main():
    print("ARM64 Raspberry Pi DHT Sensor Example")
    print("=====================================")
    print(f"Sensor type: DHT22")
    print(f"GPIO pin: {pin}")
    print()
    
    # Detect the platform
    from Adafruit_DHT import platform_detect
    pi_version = platform_detect.pi_version()
    
    if pi_version == 4:
        print("✓ Detected ARM64 Raspberry Pi (Pi 4/5)")
        print("  Using optimized ARM64 driver with:")
        print("  - Enhanced peripheral base address detection")
        print("  - ARM64-optimized timing loops")
        print("  - Increased timeout values for faster processors")
    elif pi_version is None:
        print("ℹ Not running on Raspberry Pi - using test driver")
    else:
        print(f"ℹ Detected Raspberry Pi version {pi_version}")
    
    print()
    
    # Try to grab a sensor reading. Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not None and temperature is not None:
        print(f'Temperature: {temperature:.1f}°C')
        print(f'Humidity: {humidity:.1f}%')
    else:
        print('Failed to get reading. Try again!')

if __name__ == '__main__':
    main()