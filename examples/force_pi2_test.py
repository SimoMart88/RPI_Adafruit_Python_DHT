#!/usr/bin/env python3
"""
Force Pi 2 driver test for ARM64 systems.
Sometimes the Pi 2 driver works better on ARM64 than the specialized ARM64 driver.
"""

import Adafruit_DHT
import time

def test_with_pi2_driver():
    """Test DHT sensor using Pi 2 driver on ARM64 system."""
    print("Force Pi 2 Driver Test on ARM64")
    print("=" * 40)
    
    # Override platform detection to force Pi 2 driver
    import Adafruit_DHT.Raspberry_Pi_2 as pi2_platform
    
    sensor = Adafruit_DHT.DHT22
    pin = 17
    
    print(f"Testing DHT22 on pin {pin} using Pi 2 driver...")
    print("Attempting 5 reads...")
    
    success_count = 0
    
    for i in range(5):
        print(f"Attempt {i+1}: ", end="", flush=True)
        
        # Use Pi 2 platform directly
        humidity, temperature = pi2_platform.read(sensor, pin)
        
        if humidity is not None and temperature is not None:
            print(f"SUCCESS - Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
            success_count += 1
        else:
            print("FAILED")
        
        if i < 4:
            time.sleep(2)
    
    print(f"\nResults: {success_count}/5 successful reads")
    
    if success_count > 0:
        print("✅ Pi 2 driver works on this ARM64 system!")
        print("💡 Consider using Pi 2 driver as workaround.")
        return True
    else:
        print("❌ Pi 2 driver also fails.")
        return False

def main():
    return test_with_pi2_driver()

if __name__ == '__main__':
    main()