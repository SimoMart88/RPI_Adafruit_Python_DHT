#!/usr/bin/env python3
"""
Comprehensive GPIO system fix for Raspberry Pi.
Attempts to resolve all common GPIO access issues.
"""

import os
import sys
import subprocess
import time

def run_command(cmd, description="", ignore_errors=False):
    """Run a system command and report results."""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} - Success")
            if result.stdout.strip():
                print(f"  Output: {result.stdout.strip()}")
            return True
        else:
            if ignore_errors:
                print(f"⚠ {description} - Failed (ignored)")
                if result.stderr.strip():
                    print(f"  Error: {result.stderr.strip()}")
                return False
            else:
                print(f"❌ {description} - Failed")
                if result.stderr.strip():
                    print(f"  Error: {result.stderr.strip()}")
                return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def check_root():
    """Check if running as root."""
    if os.getuid() == 0:
        print("✓ Running as root")
        return True
    else:
        print("❌ Not running as root")
        print("💡 Many GPIO fixes require root privileges")
        print("   Try: sudo python3 examples/gpio_system_fix.py")
        return False

def fix_gpio_permissions():
    """Fix GPIO permissions and group membership."""
    print("\nFixing GPIO Permissions")
    print("=" * 40)
    
    success = True
    
    # Create gpio group if it doesn't exist
    success &= run_command("groupadd -f gpio", "Create gpio group", ignore_errors=True)
    
    # Add current user to gpio group
    current_user = os.getenv('SUDO_USER', os.getenv('USER', 'pi'))
    success &= run_command(f"usermod -a -G gpio {current_user}", f"Add {current_user} to gpio group")
    
    # Fix /dev/gpiomem permissions if it exists
    if os.path.exists('/dev/gpiomem'):
        success &= run_command("chmod 666 /dev/gpiomem", "Fix /dev/gpiomem permissions")
        success &= run_command("chgrp gpio /dev/gpiomem", "Set /dev/gpiomem group to gpio")
    
    # Fix /dev/mem permissions as fallback
    if os.path.exists('/dev/mem'):
        success &= run_command("chmod 644 /dev/mem", "Fix /dev/mem permissions")
    
    return success

def load_gpio_modules():
    """Load GPIO kernel modules."""
    print("\nLoading GPIO Modules")
    print("=" * 40)
    
    modules_to_try = [
        "raspberrypi-gpiomem",
        "bcm2835-gpiomem", 
        "gpiomem",
        "gpio-dev"
    ]
    
    loaded_any = False
    
    for module in modules_to_try:
        if run_command(f"modprobe {module}", f"Load {module} module", ignore_errors=True):
            loaded_any = True
    
    # Check what's actually loaded
    run_command("lsmod | grep gpio", "Check loaded GPIO modules", ignore_errors=True)
    
    return loaded_any

def enable_gpio_interface():
    """Enable GPIO interface through raspi-config."""
    print("\nEnabling GPIO Interface")
    print("=" * 40)
    
    # Method 1: Direct config.txt modification
    config_txt = "/boot/config.txt"
    firmware_config = "/boot/firmware/config.txt"
    
    # Check which config file exists
    config_file = None
    if os.path.exists(config_txt):
        config_file = config_txt
    elif os.path.exists(firmware_config):
        config_file = firmware_config
    
    if config_file:
        print(f"Found config file: {config_file}")
        
        # Read current config
        try:
            with open(config_file, 'r') as f:
                content = f.read()
            
            # Add GPIO settings if not present
            settings_to_add = [
                "dtparam=gpio=on",
                "enable_uart=1",
                "dtoverlay=gpio-poweroff,gpiopin=3"
            ]
            
            modified = False
            for setting in settings_to_add:
                if setting not in content:
                    content += f"\n{setting}\n"
                    modified = True
                    print(f"  Added: {setting}")
            
            if modified:
                # Backup original
                run_command(f"cp {config_file} {config_file}.backup", "Backup config file")
                
                # Write modified config
                with open(config_file, 'w') as f:
                    f.write(content)
                print("✓ Updated config file")
                return True
            else:
                print("✓ Config file already has GPIO settings")
                return True
                
        except Exception as e:
            print(f"❌ Failed to modify config file: {e}")
    
    # Method 2: raspi-config non-interactive
    return run_command("raspi-config nonint do_gpio 0", "Enable GPIO via raspi-config", ignore_errors=True)

def create_gpio_devices():
    """Create GPIO device files if they don't exist."""
    print("\nCreating GPIO Device Files")
    print("=" * 40)
    
    success = True
    
    # Create /dev/gpiomem if it doesn't exist
    if not os.path.exists('/dev/gpiomem'):
        # Try to create it manually (this is a bit of a hack)
        success &= run_command("mknod /dev/gpiomem c 244 0", "Create /dev/gpiomem device", ignore_errors=True)
        success &= run_command("chmod 666 /dev/gpiomem", "Set /dev/gpiomem permissions", ignore_errors=True)
        success &= run_command("chgrp gpio /dev/gpiomem", "Set /dev/gpiomem group", ignore_errors=True)
    
    # List all GPIO-related devices
    run_command("ls -la /dev/gpio* /dev/gpiochip* 2>/dev/null || echo 'No GPIO devices found'", "List GPIO devices", ignore_errors=True)
    
    return success

def test_gpio_access():
    """Test GPIO access with a simple read/write."""
    print("\nTesting GPIO Access")
    print("=" * 40)
    
    # Test 1: Try to access /dev/gpiomem directly
    if os.path.exists('/dev/gpiomem'):
        try:
            with open('/dev/gpiomem', 'r+b') as f:
                print("✓ Can open /dev/gpiomem for read/write")
                return True
        except PermissionError:
            print("❌ Permission denied accessing /dev/gpiomem")
        except Exception as e:
            print(f"❌ Error accessing /dev/gpiomem: {e}")
    
    # Test 2: Try sysfs GPIO
    try:
        test_pin = 18
        
        # Export pin
        with open('/sys/class/gpio/export', 'w') as f:
            f.write(str(test_pin))
        
        time.sleep(0.1)
        
        # Check if pin directory was created
        pin_dir = f'/sys/class/gpio/gpio{test_pin}'
        if os.path.exists(pin_dir):
            print(f"✓ Can export GPIO pin {test_pin} via sysfs")
            
            # Clean up
            with open('/sys/class/gpio/unexport', 'w') as f:
                f.write(str(test_pin))
            
            return True
        else:
            print(f"❌ GPIO pin {test_pin} directory not created")
            
    except Exception as e:
        print(f"❌ sysfs GPIO test failed: {e}")
    
    return False

def reboot_prompt():
    """Prompt for reboot if needed."""
    print("\nReboot Required")
    print("=" * 40)
    print("Some changes require a reboot to take effect.")
    print("After reboot, run the DHT test again.")
    
    response = input("Reboot now? (y/n): ")
    if response.lower() == 'y':
        print("Rebooting in 5 seconds...")
        time.sleep(5)
        subprocess.run(['reboot'])

def main():
    """Run comprehensive GPIO system fix."""
    print("Comprehensive GPIO System Fix")
    print("=" * 50)
    
    # Check if running as root
    if not check_root():
        return 1
    
    print("\n🔧 Attempting to fix GPIO system issues...")
    
    # Step 1: Fix permissions
    perm_ok = fix_gpio_permissions()
    
    # Step 2: Load modules
    modules_ok = load_gpio_modules()
    
    # Step 3: Enable GPIO interface
    interface_ok = enable_gpio_interface()
    
    # Step 4: Create device files
    devices_ok = create_gpio_devices()
    
    # Step 5: Test access
    access_ok = test_gpio_access()
    
    # Summary
    print("\n" + "=" * 50)
    print("Fix Summary:")
    print(f"Permissions:     {'✓' if perm_ok else '❌'}")
    print(f"Modules:         {'✓' if modules_ok else '❌'}")
    print(f"Interface:       {'✓' if interface_ok else '❌'}")
    print(f"Device files:    {'✓' if devices_ok else '❌'}")
    print(f"GPIO access:     {'✓' if access_ok else '❌'}")
    
    if access_ok:
        print("\n🎉 GPIO access is working!")
        print("Try running your DHT sensor test again.")
        return 0
    else:
        print("\n⚠️ GPIO access still has issues.")
        print("A reboot may be required for changes to take effect.")
        
        if perm_ok or interface_ok:
            reboot_prompt()
        
        return 1

if __name__ == '__main__':
    sys.exit(main())