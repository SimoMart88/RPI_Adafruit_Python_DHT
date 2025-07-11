#!/usr/bin/env python3
"""
Basic GPIO test that bypasses the DHT library entirely.
Tests raw GPIO access to isolate hardware vs software issues.
"""

import os
import sys
import time

def test_sysfs_gpio():
    """Test GPIO using sysfs interface (doesn't require special drivers)."""
    print("Basic sysfs GPIO Test")
    print("=" * 30)
    
    test_pin = 18  # Use a safe pin
    
    try:
        # Export the pin
        print(f"Exporting GPIO pin {test_pin}...")
        with open('/sys/class/gpio/export', 'w') as f:
            f.write(str(test_pin))
        
        time.sleep(0.5)
        
        pin_dir = f'/sys/class/gpio/gpio{test_pin}'
        if not os.path.exists(pin_dir):
            print(f"❌ Pin directory {pin_dir} not created")
            return False
        
        print(f"✓ Pin {test_pin} exported successfully")
        
        # Set as output
        with open(f'{pin_dir}/direction', 'w') as f:
            f.write('out')
        print("✓ Set pin as output")
        
        # Toggle the pin a few times
        for i in range(3):
            # Set high
            with open(f'{pin_dir}/value', 'w') as f:
                f.write('1')
            print(f"  Set pin HIGH (iteration {i+1})")
            time.sleep(0.5)
            
            # Set low
            with open(f'{pin_dir}/value', 'w') as f:
                f.write('0')
            print(f"  Set pin LOW (iteration {i+1})")
            time.sleep(0.5)
        
        # Set as input and read
        with open(f'{pin_dir}/direction', 'w') as f:
            f.write('in')
        
        with open(f'{pin_dir}/value', 'r') as f:
            value = f.read().strip()
        print(f"✓ Read pin value: {value}")
        
        # Clean up
        with open('/sys/class/gpio/unexport', 'w') as f:
            f.write(str(test_pin))
        print(f"✓ Unexported pin {test_pin}")
        
        return True
        
    except PermissionError:
        print("❌ Permission denied - try with sudo")
        return False
    except Exception as e:
        print(f"❌ sysfs GPIO test failed: {e}")
        return False

def test_dev_mem_access():
    """Test direct /dev/mem access."""
    print("\nDirect /dev/mem Access Test")
    print("=" * 30)
    
    try:
        # Try to open /dev/mem
        with open('/dev/mem', 'r+b') as f:
            print("✓ Can open /dev/mem")
            return True
    except PermissionError:
        print("❌ Permission denied accessing /dev/mem - try with sudo")
        return False
    except Exception as e:
        print(f"❌ Cannot access /dev/mem: {e}")
        return False

def test_gpiomem_access():
    """Test /dev/gpiomem access."""
    print("\nGPIO Memory Access Test") 
    print("=" * 30)
    
    if not os.path.exists('/dev/gpiomem'):
        print("❌ /dev/gpiomem does not exist")
        return False
    
    try:
        with open('/dev/gpiomem', 'r+b') as f:
            print("✓ Can open /dev/gpiomem")
            return True
    except PermissionError:
        print("❌ Permission denied accessing /dev/gpiomem")
        return False
    except Exception as e:
        print(f"❌ Cannot access /dev/gpiomem: {e}")
        return False

def check_hardware_info():
    """Display hardware information for context."""
    print("\nHardware Information")
    print("=" * 30)
    
    try:
        # Check Pi model
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
        
        import re
        model_match = re.search(r'^Model\s*:\s*(.+)$', cpuinfo, re.MULTILINE)
        hardware_match = re.search(r'^Hardware\s*:\s*(.+)$', cpuinfo, re.MULTILINE)
        
        if model_match:
            print(f"Model: {model_match.group(1)}")
        if hardware_match:
            print(f"Hardware: {hardware_match.group(1)}")
        
        # Check kernel version
        with open('/proc/version', 'r') as f:
            version = f.read().strip()
        print(f"Kernel: {version.split()[2]}")
        
    except Exception as e:
        print(f"Error reading hardware info: {e}")

def suggest_fixes(sysfs_ok, gpiomem_ok, devmem_ok):
    """Suggest fixes based on test results."""
    print("\nSuggested Actions")
    print("=" * 30)
    
    if not (sysfs_ok or gpiomem_ok or devmem_ok):
        print("❌ No GPIO access methods work")
        print("1. Run with sudo:")
        print("   sudo python3 examples/basic_gpio_test.py")
        print("2. Run the GPIO system fix:")
        print("   sudo python3 examples/gpio_system_fix.py")
        print("3. Enable GPIO in raspi-config:")
        print("   sudo raspi-config → Interface Options → GPIO")
        print("4. Check if this is actually a Raspberry Pi")
    elif sysfs_ok and not (gpiomem_ok or devmem_ok):
        print("⚠️ Only sysfs GPIO works")
        print("This suggests permission or driver issues with /dev/gpiomem")
        print("1. Run GPIO system fix with sudo")
        print("2. The DHT library may need to be modified to use sysfs")
    elif gpiomem_ok or devmem_ok:
        print("✓ GPIO memory access works")
        print("The DHT library should work. If it doesn't:")
        print("1. Check hardware connections")
        print("2. Try different GPIO pins")
        print("3. Verify DHT sensor is working")
    else:
        print("Mixed results - run with sudo for full diagnosis")

def main():
    """Run basic GPIO tests."""
    print("Basic GPIO Hardware Test")
    print("=" * 40)
    print("This test checks if GPIO works at all, independent of the DHT library.")
    
    # Show hardware info
    check_hardware_info()
    
    # Run tests
    sysfs_ok = test_sysfs_gpio()
    gpiomem_ok = test_gpiomem_access()
    devmem_ok = test_dev_mem_access()
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"sysfs GPIO:      {'✓' if sysfs_ok else '❌'}")
    print(f"/dev/gpiomem:    {'✓' if gpiomem_ok else '❌'}")
    print(f"/dev/mem:        {'✓' if devmem_ok else '❌'}")
    
    # Provide suggestions
    suggest_fixes(sysfs_ok, gpiomem_ok, devmem_ok)
    
    if sysfs_ok or gpiomem_ok or devmem_ok:
        print("\n✅ At least one GPIO method works")
        return 0
    else:
        print("\n❌ No GPIO methods work")
        return 1

if __name__ == '__main__':
    sys.exit(main())