#!/usr/bin/env python3
"""
Install the library properly and test DHT sensor.
This script handles the installation and testing in the correct directory.
"""

import os
import sys
import subprocess
import time

def install_library():
    """Install the library in development mode."""
    print("Installing Adafruit DHT Library")
    print("=" * 40)
    
    # Get the parent directory (where setup.py is located)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    print(f"Library directory: {parent_dir}")
    
    try:
        # Change to the library directory
        os.chdir(parent_dir)
        
        # Install in development mode
        print("Installing library...")
        result = subprocess.run([
            sys.executable, 'setup.py', 'develop', '--user'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Library installed successfully")
            return True
        else:
            print("❌ Installation failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def test_import():
    """Test if the library can be imported."""
    print("\nTesting Library Import")
    print("=" * 40)
    
    try:
        import Adafruit_DHT
        print("✓ Adafruit_DHT imported successfully")
        
        # Check platform detection
        version = Adafruit_DHT.platform_detect.pi_version()
        print(f"✓ Detected Pi version: {version}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during import test: {e}")
        return False

def test_dht_sensor():
    """Test DHT sensor reading."""
    print("\nTesting DHT Sensor")
    print("=" * 40)
    
    try:
        import Adafruit_DHT
        
        sensor = Adafruit_DHT.DHT22
        pins_to_test = [4, 17, 18, 27]
        
        print("Testing DHT22 on multiple pins...")
        
        for pin in pins_to_test:
            print(f"\nTesting pin {pin}:")
            
            for attempt in range(3):
                print(f"  Attempt {attempt + 1}: ", end="", flush=True)
                
                humidity, temperature = Adafruit_DHT.read(sensor, pin)
                
                if humidity is not None and temperature is not None:
                    print(f"SUCCESS - Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
                    return True
                else:
                    print("FAILED")
                
                if attempt < 2:
                    time.sleep(2)
        
        print("\n❌ All sensor tests failed")
        return False
        
    except Exception as e:
        print(f"❌ Sensor test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main installation and test procedure."""
    print("Adafruit DHT Installation and Test")
    print("=" * 50)
    
    # Step 1: Install the library
    if not install_library():
        print("\n❌ Installation failed. Cannot proceed.")
        return 1
    
    # Step 2: Test import
    if not test_import():
        print("\n❌ Library import failed. Check installation.")
        return 1
    
    # Step 3: Test sensor
    if test_dht_sensor():
        print("\n🎉 DHT sensor is working!")
        return 0
    else:
        print("\n❌ DHT sensor failed. Check:")
        print("1. Hardware connections")
        print("2. GPIO permissions (run system_check.py)")
        print("3. Try with sudo if needed")
        return 1

if __name__ == '__main__':
    sys.exit(main())