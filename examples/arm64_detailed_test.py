#!/usr/bin/env python3
"""
Detailed ARM64 DHT test with error reporting.
This script provides more detailed information about read failures.
"""

import Adafruit_DHT
import time

# Sensor configuration
sensor = Adafruit_DHT.DHT22
pin = 4

def test_detailed_reads():
    """Test multiple reads with detailed error reporting."""
    print("ARM64 DHT22 Detailed Test")
    print("=" * 40)
    print(f"Sensor: DHT22")
    print(f"Pin: GPIO {pin}")
    
    # Check platform
    from Adafruit_DHT import platform_detect
    version = platform_detect.pi_version()
    print(f"Detected Pi version: {version}")
    
    if version in [4, 5]:
        print("✓ ARM64 Raspberry Pi detected - using optimized driver")
    else:
        print(f"ℹ Using standard driver for Pi version {version}")
    
    print("\nAttempting 10 sensor reads...")
    print("-" * 40)
    
    success_count = 0
    timeout_count = 0
    checksum_count = 0
    other_error_count = 0
    
    for attempt in range(10):
        print(f"Attempt {attempt + 1:2d}: ", end="", flush=True)
        
        try:
            # Get platform and try direct read to get error code
            platform = Adafruit_DHT.common.get_platform()
            
            # Try the read
            humidity, temperature = Adafruit_DHT.read(sensor, pin)
            
            if humidity is not None and temperature is not None:
                print(f"SUCCESS - Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
                success_count += 1
            else:
                # Try to get more specific error by using platform directly
                if hasattr(platform, 'read'):
                    # This should give us the actual error codes
                    try:
                        import Adafruit_DHT.Raspberry_Pi_ARM64_Driver as driver
                        result, h, t = driver.read(sensor, pin)
                        
                        if result == 0:  # DHT_SUCCESS
                            print(f"SUCCESS - Temp: {t:.1f}°C, Humidity: {h:.1f}%")
                            success_count += 1
                        elif result == -1:  # DHT_ERROR_TIMEOUT
                            print("TIMEOUT - Sensor not responding")
                            timeout_count += 1
                        elif result == -2:  # DHT_ERROR_CHECKSUM
                            print("CHECKSUM ERROR - Data corrupted")
                            checksum_count += 1
                        elif result == -3:  # DHT_ERROR_ARGUMENT
                            print("ARGUMENT ERROR - Invalid parameters")
                            other_error_count += 1
                        elif result == -4:  # DHT_ERROR_GPIO
                            print("GPIO ERROR - Cannot access GPIO")
                            other_error_count += 1
                        else:
                            print(f"UNKNOWN ERROR - Code: {result}")
                            other_error_count += 1
                    except ImportError:
                        print("FAILED - Cannot get detailed error (not ARM64?)")
                        other_error_count += 1
                else:
                    print("FAILED - No detailed error available")
                    other_error_count += 1
                    
        except Exception as e:
            print(f"EXCEPTION - {e}")
            other_error_count += 1
        
        # Wait between reads
        if attempt < 9:
            time.sleep(2)
    
    print("\n" + "=" * 40)
    print("Results Summary:")
    print(f"  Successful reads: {success_count}/10")
    print(f"  Timeout errors:   {timeout_count}/10")
    print(f"  Checksum errors:  {checksum_count}/10") 
    print(f"  Other errors:     {other_error_count}/10")
    
    if success_count > 0:
        print(f"\n✅ SUCCESS! {success_count} reads worked.")
        if success_count < 8:
            print("💡 Some reads failed - this is normal for DHT sensors.")
            print("   Try running the script a few times.")
    else:
        print("\n❌ All reads failed.")
        if timeout_count > 7:
            print("💡 Mostly timeout errors - possible timing issue.")
            print("   Check wiring and try a different GPIO pin.")
        elif checksum_count > 7:
            print("💡 Mostly checksum errors - sensor responding but data corrupted.")
            print("   Check power supply and wiring.")
        else:
            print("💡 Mixed errors - check hardware connections.")

def main():
    test_detailed_reads()

if __name__ == '__main__':
    main()