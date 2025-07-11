#!/usr/bin/env python3
"""
GPIO Test for ARM64 DHT debugging.
This script tests basic GPIO functionality to isolate the issue.
"""

import time
import sys

def test_gpio_basic():
    """Test basic GPIO access using the ARM64 driver."""
    print("GPIO Basic Test for ARM64")
    print("=" * 40)
    
    try:
        # Import the ARM64 driver directly
        import Adafruit_DHT.Raspberry_Pi_ARM64_Driver as driver
        print("✓ ARM64 driver imported successfully")
        
        pin = 17  # Use pin 17 for testing
        print(f"Testing GPIO pin {pin}")
        
        # Test basic read operation with different sensor types
        print("\nTesting DHT22 read...")
        result, humidity, temp = driver.read(22, pin)  # DHT22
        print(f"Result code: {result}")
        
        if result == 0:
            print(f"✓ SUCCESS - Temp: {temp:.1f}°C, Humidity: {humidity:.1f}%")
        elif result == -1:
            print("❌ TIMEOUT - Sensor not responding")
        elif result == -2:
            print("⚠️ CHECKSUM ERROR - Sensor responding but data corrupted")
        elif result == -4:
            print("❌ GPIO ERROR - Cannot access GPIO")
        else:
            print(f"❌ UNKNOWN ERROR - Code: {result}")
            
        return result == 0
        
    except ImportError as e:
        print(f"❌ Cannot import ARM64 driver: {e}")
        print("This system may not be detected as ARM64")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_compatibility():
    """Test if the Pi 2 driver works on this ARM64 system."""
    print("\n" + "=" * 40)
    print("Testing Pi 2 Driver Compatibility")
    print("=" * 40)
    
    try:
        # Force use of Pi 2 driver
        import Adafruit_DHT.Raspberry_Pi_2_Driver as pi2_driver
        print("✓ Pi 2 driver imported successfully")
        
        pin = 17
        print(f"Testing DHT22 on pin {pin} with Pi 2 driver...")
        
        result, humidity, temp = pi2_driver.read(22, pin)
        print(f"Result code: {result}")
        
        if result == 0:
            print(f"✓ SUCCESS with Pi 2 driver - Temp: {temp:.1f}°C, Humidity: {humidity:.1f}%")
            return True
        elif result == -1:
            print("❌ TIMEOUT with Pi 2 driver")
        elif result == -2:
            print("⚠️ CHECKSUM ERROR with Pi 2 driver")
        elif result == -4:
            print("❌ GPIO ERROR with Pi 2 driver")
        else:
            print(f"❌ UNKNOWN ERROR with Pi 2 driver - Code: {result}")
            
        return False
        
    except ImportError as e:
        print(f"❌ Cannot import Pi 2 driver: {e}")
        return False
    except Exception as e:
        print(f"❌ Pi 2 driver error: {e}")
        return False

def main():
    print("ARM64 DHT GPIO Diagnostic Tool")
    print("=" * 50)
    
    # Test ARM64 driver
    arm64_works = test_gpio_basic()
    
    # Test Pi 2 driver as fallback
    pi2_works = test_fallback_compatibility()
    
    print("\n" + "=" * 50)
    print("Diagnostic Results:")
    print(f"ARM64 driver works: {'✓ YES' if arm64_works else '❌ NO'}")
    print(f"Pi 2 driver works:  {'✓ YES' if pi2_works else '❌ NO'}")
    
    if arm64_works:
        print("\n🎉 ARM64 driver is working correctly!")
    elif pi2_works:
        print("\n💡 ARM64 driver has issues, but Pi 2 driver works.")
        print("   Consider using Pi 2 driver as a temporary workaround.")
    else:
        print("\n❌ Neither driver works. Possible issues:")
        print("   1. Hardware connection problem")
        print("   2. GPIO permissions issue")
        print("   3. Sensor malfunction")
        print("   4. Power supply issue")
        
        print("\nTroubleshooting steps:")
        print("   1. Check wiring: VCC to 3.3V or 5V, GND to GND, DATA to GPIO pin")
        print("   2. Try running with sudo: sudo python3 examples/gpio_test.py")
        print("   3. Try a different GPIO pin")
        print("   4. Test the sensor on a different system")
    
    return 0 if (arm64_works or pi2_works) else 1

if __name__ == '__main__':
    sys.exit(main())