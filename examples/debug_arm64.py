#!/usr/bin/env python3
"""
Debug script for ARM64 DHT sensor issues.
This script provides detailed error information to help diagnose segmentation faults.
"""

import sys
import traceback
import Adafruit_DHT

def test_platform_detection():
    """Test platform detection in detail."""
    print("=== Platform Detection Test ===")
    try:
        from Adafruit_DHT import platform_detect
        version = platform_detect.pi_version()
        print(f"Detected Pi version: {version}")
        
        # Read /proc/cpuinfo to see what we're working with
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            
            # Look for key fields
            import re
            hardware_match = re.search(r'^Hardware\s*:\s*(.+)$', cpuinfo, re.MULTILINE)
            model_match = re.search(r'^Model\s*:\s*(.+)$', cpuinfo, re.MULTILINE)
            arch_match = re.search(r'^Architecture\s*:\s*(.+)$', cpuinfo, re.MULTILINE)
            
            if hardware_match:
                print(f"Hardware: {hardware_match.group(1)}")
            if model_match:
                print(f"Model: {model_match.group(1)}")
            if arch_match:
                print(f"Architecture: {arch_match.group(1)}")
                
        except Exception as e:
            print(f"Error reading /proc/cpuinfo: {e}")
            
        return True
    except Exception as e:
        print(f"Platform detection failed: {e}")
        traceback.print_exc()
        return False

def test_platform_loading():
    """Test loading the platform module."""
    print("\n=== Platform Loading Test ===")
    try:
        import Adafruit_DHT.common as common
        platform = common.get_platform()
        print(f"Loaded platform: {platform}")
        print(f"Platform module: {platform.__name__}")
        return True
    except Exception as e:
        print(f"Platform loading failed: {e}")
        traceback.print_exc()
        return False

def test_driver_import():
    """Test importing the ARM64 driver directly."""
    print("\n=== Driver Import Test ===")
    try:
        from Adafruit_DHT import platform_detect
        version = platform_detect.pi_version()
        
        if version in [4, 5]:
            print("Attempting to import ARM64 driver...")
            from Adafruit_DHT import Raspberry_Pi_ARM64_Driver as driver
            print(f"ARM64 driver imported successfully: {driver}")
            return True
        else:
            print(f"Not ARM64 system (version {version}), skipping driver test")
            return True
    except Exception as e:
        print(f"Driver import failed: {e}")
        traceback.print_exc()
        return False

def test_simple_read():
    """Test a simple sensor read."""
    print("\n=== Simple Read Test ===")
    try:
        print("Attempting simple DHT22 read on pin 4...")
        
        # Use the high-level interface
        humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT22, 4)
        
        if humidity is not None and temperature is not None:
            print(f"Success! Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
        else:
            print("Read returned None values (this is normal and just means retry is needed)")
        
        return True
    except Exception as e:
        print(f"Simple read failed: {e}")
        traceback.print_exc()
        return False

def main():
    print("ARM64 DHT Debug Script")
    print("=" * 50)
    
    tests = [
        test_platform_detection,
        test_platform_loading,
        test_driver_import,
        test_simple_read
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\nRunning test {i}/{len(tests)}: {test.__name__}")
        try:
            success = test()
            if not success:
                print("❌ Test failed, stopping here for safety")
                return 1
            else:
                print("✅ Test passed")
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            traceback.print_exc()
            return 1
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed successfully!")
    return 0

if __name__ == '__main__':
    sys.exit(main())