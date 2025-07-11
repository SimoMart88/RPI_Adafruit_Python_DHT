#!/usr/bin/env python3
"""
Simple GPIO test for ARM64 DHT debugging.
Tests only the ARM64 driver without requiring other drivers.
"""

import sys
import time

def test_arm64_driver_only():
    """Test only the ARM64 driver."""
    print("ARM64 Driver Test")
    print("=" * 30)
    
    try:
        # Check platform detection
        from Adafruit_DHT import platform_detect
        version = platform_detect.pi_version()
        print(f"Detected Pi version: {version}")
        
        if version not in [4, 5]:
            print("❌ System not detected as ARM64 Pi 4/5")
            return False
        
        # Import ARM64 driver
        import Adafruit_DHT.Raspberry_Pi_ARM64_Driver as driver
        print("✓ ARM64 driver imported successfully")
        
        # Test different pins
        pins_to_test = [4, 17, 18, 27]
        sensor = 22  # DHT22
        
        print(f"\nTesting DHT22 on multiple pins...")
        
        for pin in pins_to_test:
            print(f"\nTesting pin {pin}:")
            
            for attempt in range(3):
                print(f"  Attempt {attempt + 1}: ", end="", flush=True)
                
                result, humidity, temp = driver.read(sensor, pin)
                
                if result == 0:
                    print(f"SUCCESS - Temp: {temp:.1f}°C, Humidity: {humidity:.1f}%")
                    return True
                elif result == -1:
                    print("TIMEOUT")
                elif result == -2:
                    print("CHECKSUM ERROR")
                elif result == -4:
                    print("GPIO ERROR")
                else:
                    print(f"ERROR {result}")
                
                if attempt < 2:
                    time.sleep(1)
        
        print("\n❌ All pins and attempts failed")
        return False
        
    except ImportError as e:
        print(f"❌ Cannot import ARM64 driver: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_sudo_suggestion():
    """Test and provide sudo suggestion if needed."""
    print("\n" + "=" * 40)
    print("Testing GPIO Access Permissions")
    print("=" * 40)
    
    try:
        # Check if /dev/gpiomem is accessible
        import os
        if os.path.exists("/dev/gpiomem"):
            stat = os.stat("/dev/gpiomem")
            print(f"✓ /dev/gpiomem exists")
            print(f"  Owner: {stat.st_uid}, Group: {stat.st_gid}")
            print(f"  Permissions: {oct(stat.st_mode)[-3:]}")
            
            # Check if current user can access it
            if os.access("/dev/gpiomem", os.R_OK | os.W_OK):
                print("✓ Current user can access /dev/gpiomem")
            else:
                print("❌ Current user cannot access /dev/gpiomem")
                print("💡 Try running with sudo: sudo python3 examples/simple_gpio_test.py")
                return False
        else:
            print("❌ /dev/gpiomem does not exist")
            print("💡 Try running with sudo to use /dev/mem instead")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Permission check failed: {e}")
        return False

def main():
    print("Simple ARM64 DHT GPIO Test")
    print("=" * 50)
    
    # Test permissions first
    perm_ok = test_with_sudo_suggestion()
    
    if not perm_ok:
        print("\n🔧 Permission issues detected. Try with sudo:")
        print("   sudo python3 examples/simple_gpio_test.py")
        return 1
    
    # Test ARM64 driver
    success = test_arm64_driver_only()
    
    if success:
        print("\n🎉 ARM64 driver is working!")
    else:
        print("\n❌ ARM64 driver failed on all tests")
        print("\nPossible solutions:")
        print("1. Check hardware connections:")
        print("   - VCC to 3.3V or 5V")
        print("   - GND to GND") 
        print("   - DATA to GPIO pin")
        print("2. Try with sudo (may need root for GPIO access)")
        print("3. Try a different DHT22 sensor (hardware may be faulty)")
        print("4. Use a logic analyzer to check signal timing")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())