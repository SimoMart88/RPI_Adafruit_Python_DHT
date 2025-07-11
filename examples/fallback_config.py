#!/usr/bin/env python3
"""
Temporary workaround: Configure library to use Pi 2 driver for ARM64.
This can be used if the ARM64 driver doesn't work properly.
"""

import os
import sys

# Add the parent directory to path to modify the library
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def apply_fallback_patch():
    """Temporarily patch the platform detection to use Pi 2 driver for ARM64."""
    import Adafruit_DHT.common as common
    
    # Store the original get_platform function
    original_get_platform = common.get_platform
    
    def patched_get_platform():
        """Modified get_platform that uses Pi 2 driver for ARM64 systems."""
        from Adafruit_DHT import platform_detect
        version = platform_detect.pi_version()
        
        if version == 1:
            from Adafruit_DHT import Raspberry_Pi
            return Raspberry_Pi
        elif version in [2, 3, 4, 5]:  # Use Pi 2 driver for versions 2, 3, 4, 5
            print("🔧 Using Pi 2 driver for ARM64 compatibility")
            from Adafruit_DHT import Raspberry_Pi_2
            return Raspberry_Pi_2
        else:
            import warnings
            warnings.warn("Could not detect Raspberry Pi version. Test driver will be used")
            from Adafruit_DHT import Test
            return Test
    
    # Apply the patch
    common.get_platform = patched_get_platform
    print("✅ Applied Pi 2 driver fallback for ARM64 systems")

def test_with_fallback():
    """Test DHT sensor with the Pi 2 driver fallback."""
    print("DHT Test with Pi 2 Driver Fallback")
    print("=" * 40)
    
    # Apply the fallback patch
    apply_fallback_patch()
    
    # Now test with the standard interface
    import Adafruit_DHT
    
    sensor = Adafruit_DHT.DHT22
    pin = 17
    
    print(f"Testing DHT22 on pin {pin}...")
    
    # Try a few reads
    for i in range(3):
        print(f"Attempt {i+1}: ", end="", flush=True)
        
        humidity, temperature = Adafruit_DHT.read(sensor, pin)
        
        if humidity is not None and temperature is not None:
            print(f"SUCCESS - Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
            return True
        else:
            print("FAILED")
        
        if i < 2:
            import time
            time.sleep(2)
    
    print("❌ All attempts failed")
    return False

def main():
    """Run the fallback test."""
    success = test_with_fallback()
    
    if success:
        print("\n🎉 Success with Pi 2 driver fallback!")
        print("\nTo permanently use this workaround:")
        print("1. Edit Adafruit_DHT/common.py")
        print("2. Modify get_platform() to return Raspberry_Pi_2 for version 4/5")
        print("3. This will use the Pi 2 driver instead of ARM64 driver")
    else:
        print("\n❌ Pi 2 driver fallback also failed")
        print("The issue may be hardware-related")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())