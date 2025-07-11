#!/usr/bin/env python3
"""
Workaround: Use Pi 2 driver on ARM64 systems.
This often works better than the ARM64 driver on Pi 4/5 systems.
"""

import os
import sys
import time

def setup_workaround():
    """Set up the library to use Pi 2 driver for ARM64."""
    print("Pi 2 Driver Workaround Setup")
    print("=" * 40)
    
    # Add parent directory to path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    sys.path.insert(0, parent_dir)
    
    try:
        # Test if we can import the Pi 2 driver
        import Adafruit_DHT.Raspberry_Pi_2_Driver as pi2_driver
        print("✓ Pi 2 driver available")
        
        # Test if we can import the Pi 2 platform
        import Adafruit_DHT.Raspberry_Pi_2 as pi2_platform
        print("✓ Pi 2 platform available")
        
        return True
        
    except ImportError as e:
        print(f"❌ Pi 2 driver not available: {e}")
        return False

def test_pi2_driver_direct():
    """Test Pi 2 driver directly without going through platform detection."""
    print("\nDirect Pi 2 Driver Test")
    print("=" * 40)
    
    try:
        import Adafruit_DHT.Raspberry_Pi_2_Driver as pi2_driver
        
        sensor = 22  # DHT22
        pins_to_test = [4, 17, 18, 27]
        
        for pin in pins_to_test:
            print(f"\nTesting pin {pin} with Pi 2 driver:")
            
            for attempt in range(3):
                print(f"  Attempt {attempt + 1}: ", end="", flush=True)
                
                result, humidity, temp = pi2_driver.read(sensor, pin)
                
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
                    time.sleep(2)
        
        print("❌ All tests failed")
        return False
        
    except Exception as e:
        print(f"❌ Pi 2 driver test failed: {e}")
        return False

def test_pi2_platform():
    """Test Pi 2 platform interface."""
    print("\nPi 2 Platform Test")
    print("=" * 40)
    
    try:
        import Adafruit_DHT.Raspberry_Pi_2 as pi2_platform
        
        sensor = 22  # DHT22
        pins_to_test = [4, 17, 18, 27]
        
        for pin in pins_to_test:
            print(f"\nTesting pin {pin} with Pi 2 platform:")
            
            for attempt in range(3):
                print(f"  Attempt {attempt + 1}: ", end="", flush=True)
                
                humidity, temperature = pi2_platform.read(sensor, pin)
                
                if humidity is not None and temperature is not None:
                    print(f"SUCCESS - Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
                    return True
                else:
                    print("FAILED")
                
                if attempt < 2:
                    time.sleep(2)
        
        print("❌ All tests failed")
        return False
        
    except Exception as e:
        print(f"❌ Pi 2 platform test failed: {e}")
        return False

def create_permanent_workaround():
    """Create a permanent fix by modifying the platform detection."""
    print("\nCreating Permanent Workaround")
    print("=" * 40)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    common_file = os.path.join(parent_dir, 'Adafruit_DHT', 'common.py')
    
    if not os.path.exists(common_file):
        print(f"❌ Cannot find {common_file}")
        return False
    
    try:
        # Read the current file
        with open(common_file, 'r') as f:
            content = f.read()
        
        # Check if already patched
        if 'ARM64 Pi 2 workaround' in content:
            print("✓ Workaround already applied")
            return True
        
        # Apply the patch
        old_pattern = '''    elif version == 4:
        """ARM64 Raspberry Pi 4 support"""
        from . import Raspberry_Pi_ARM64
        return Raspberry_Pi_ARM64
    elif version == 5:
        """ARM64 Raspberry Pi 5 support"""
        from . import Raspberry_Pi_ARM64
        return Raspberry_Pi_ARM64'''
        
        new_pattern = '''    elif version == 4:
        """ARM64 Pi 2 workaround - use Pi 2 driver for better compatibility"""
        from . import Raspberry_Pi_2
        return Raspberry_Pi_2
    elif version == 5:
        """ARM64 Pi 2 workaround - use Pi 2 driver for better compatibility"""
        from . import Raspberry_Pi_2
        return Raspberry_Pi_2'''
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            
            # Backup original
            backup_file = common_file + '.backup'
            with open(backup_file, 'w') as f:
                f.write(content.replace(new_pattern, old_pattern))
            print(f"✓ Backup created: {backup_file}")
            
            # Write patched version
            with open(common_file, 'w') as f:
                f.write(content)
            print("✓ Applied Pi 2 driver workaround to common.py")
            return True
        else:
            print("❌ Could not find pattern to patch")
            return False
            
    except Exception as e:
        print(f"❌ Failed to apply workaround: {e}")
        return False

def main():
    """Run Pi 2 workaround tests."""
    print("Pi 2 Driver Workaround for ARM64")
    print("=" * 50)
    
    # Test if Pi 2 driver is available
    if not setup_workaround():
        print("\n❌ Pi 2 driver not available. Cannot proceed with workaround.")
        return 1
    
    # Test Pi 2 driver directly
    direct_works = test_pi2_driver_direct()
    
    # Test Pi 2 platform
    platform_works = test_pi2_platform()
    
    if direct_works or platform_works:
        print("\n🎉 Pi 2 driver works on this ARM64 system!")
        
        # Offer to make it permanent
        response = input("\nWould you like to permanently use Pi 2 driver? (y/n): ")
        if response.lower() == 'y':
            if create_permanent_workaround():
                print("\n✅ Permanent workaround applied!")
                print("The library will now use Pi 2 driver for ARM64 systems.")
                print("You can restore original by copying common.py.backup back to common.py")
            else:
                print("\n❌ Failed to apply permanent workaround")
        
        return 0
    else:
        print("\n❌ Pi 2 driver also doesn't work")
        print("This suggests a hardware or system configuration issue")
        return 1

if __name__ == '__main__':
    sys.exit(main())