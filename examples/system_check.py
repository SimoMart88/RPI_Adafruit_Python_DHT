#!/usr/bin/env python3
"""
System diagnostic script for Raspberry Pi GPIO issues.
Checks system configuration and suggests fixes.
"""

import os
import subprocess
import sys

def check_system_info():
    """Check basic system information."""
    print("System Information Check")
    print("=" * 40)
    
    try:
        # Check OS
        with open('/etc/os-release', 'r') as f:
            os_info = f.read()
        print("OS Information:")
        for line in os_info.split('\n'):
            if line.startswith(('PRETTY_NAME', 'VERSION')):
                print(f"  {line}")
        
        # Check kernel
        kernel = subprocess.check_output(['uname', '-r'], text=True).strip()
        print(f"\nKernel: {kernel}")
        
        # Check architecture
        arch = subprocess.check_output(['uname', '-m'], text=True).strip()
        print(f"Architecture: {arch}")
        
        return True
    except Exception as e:
        print(f"Error checking system info: {e}")
        return False

def check_gpio_devices():
    """Check GPIO device files and permissions."""
    print("\nGPIO Device Check")
    print("=" * 40)
    
    devices = ['/dev/gpiomem', '/dev/mem', '/dev/gpiochip0', '/dev/gpiochip1']
    found_devices = []
    
    for device in devices:
        if os.path.exists(device):
            try:
                stat = os.stat(device)
                perms = oct(stat.st_mode)[-3:]
                print(f"✓ {device} exists (permissions: {perms})")
                found_devices.append(device)
            except Exception as e:
                print(f"⚠ {device} exists but cannot stat: {e}")
        else:
            print(f"❌ {device} does not exist")
    
    return found_devices

def check_gpio_group():
    """Check if user is in gpio group."""
    print("\nGPIO Group Check")
    print("=" * 40)
    
    try:
        import pwd
        import grp
        
        # Get current user
        current_user = pwd.getpwuid(os.getuid()).pw_name
        print(f"Current user: {current_user}")
        
        # Check if gpio group exists
        try:
            gpio_group = grp.getgrnam('gpio')
            print(f"✓ gpio group exists (GID: {gpio_group.gr_gid})")
            
            # Check if user is in gpio group
            user_groups = [g.gr_name for g in grp.getgrall() if current_user in g.gr_mem]
            if 'gpio' in user_groups:
                print(f"✓ {current_user} is in gpio group")
                return True
            else:
                print(f"❌ {current_user} is NOT in gpio group")
                print(f"💡 Run: sudo usermod -a -G gpio {current_user}")
                print("   Then log out and log back in")
                return False
        except KeyError:
            print("❌ gpio group does not exist")
            return False
            
    except Exception as e:
        print(f"Error checking groups: {e}")
        return False

def check_gpio_modules():
    """Check if GPIO kernel modules are loaded."""
    print("\nGPIO Kernel Modules Check")
    print("=" * 40)
    
    try:
        with open('/proc/modules', 'r') as f:
            modules = f.read()
        
        gpio_modules = ['gpio_dev', 'bcm2835_gpiomem', 'gpiomem']
        found_modules = []
        
        for module in gpio_modules:
            if module in modules:
                print(f"✓ {module} module loaded")
                found_modules.append(module)
            else:
                print(f"❌ {module} module not loaded")
        
        return found_modules
        
    except Exception as e:
        print(f"Error checking modules: {e}")
        return []

def suggest_fixes(gpio_devices, in_gpio_group, gpio_modules):
    """Suggest fixes based on what was found."""
    print("\nSuggested Fixes")
    print("=" * 40)
    
    if not gpio_devices:
        print("🔧 No GPIO devices found. Try these steps:")
        print("1. Update your system:")
        print("   sudo apt update && sudo apt upgrade")
        print("2. Enable GPIO interface:")
        print("   sudo raspi-config")
        print("   → Interface Options → GPIO → Enable")
        print("3. Reboot the system:")
        print("   sudo reboot")
        
    elif '/dev/gpiomem' not in gpio_devices:
        print("🔧 /dev/gpiomem missing. Try loading GPIO modules:")
        print("For newer Raspberry Pi OS (2024+):")
        print("   sudo modprobe raspberrypi-gpiomem")
        print("For older systems:")
        print("   sudo modprobe bcm2835-gpiomem")
        print("Alternative:")
        print("   sudo modprobe gpiomem")
        print("To make permanent, add to /boot/config.txt:")
        print("   echo 'dtparam=gpio=on' | sudo tee -a /boot/config.txt")
        
    if not in_gpio_group:
        print("🔧 User not in gpio group:")
        current_user = os.getenv('USER', 'pi')
        print(f"   sudo usermod -a -G gpio {current_user}")
        print("   Then log out and log back in")
        
    if not gpio_modules:
        print("🔧 GPIO modules not loaded. Try:")
        print("   sudo modprobe raspberrypi-gpiomem  # For newer systems")
        print("   sudo modprobe bcm2835-gpiomem      # For older systems")
        print("   sudo modprobe gpio-dev             # Alternative")

def test_alternative_gpio():
    """Test if we can access GPIO through alternative methods."""
    print("\nAlternative GPIO Access Test")
    print("=" * 40)
    
    # Test sysfs GPIO
    try:
        if os.path.exists('/sys/class/gpio'):
            print("✓ /sys/class/gpio exists (sysfs GPIO available)")
            
            # Try to export a GPIO pin
            try:
                with open('/sys/class/gpio/export', 'w') as f:
                    f.write('18')
                print("✓ Can export GPIO pin via sysfs")
                
                # Clean up
                if os.path.exists('/sys/class/gpio/gpio18'):
                    with open('/sys/class/gpio/unexport', 'w') as f:
                        f.write('18')
                
                return True
            except Exception as e:
                print(f"❌ Cannot export GPIO via sysfs: {e}")
                return False
        else:
            print("❌ /sys/class/gpio does not exist")
            return False
            
    except Exception as e:
        print(f"Error testing sysfs GPIO: {e}")
        return False

def main():
    """Run all diagnostic checks."""
    print("Raspberry Pi GPIO System Diagnostic")
    print("=" * 50)
    
    # Run all checks
    system_ok = check_system_info()
    gpio_devices = check_gpio_devices()
    in_gpio_group = check_gpio_group()
    gpio_modules = check_gpio_modules()
    sysfs_works = test_alternative_gpio()
    
    # Provide suggestions
    suggest_fixes(gpio_devices, in_gpio_group, gpio_modules)
    
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"System info:      {'✓' if system_ok else '❌'}")
    print(f"GPIO devices:     {'✓' if gpio_devices else '❌'}")
    print(f"GPIO group:       {'✓' if in_gpio_group else '❌'}")
    print(f"GPIO modules:     {'✓' if gpio_modules else '❌'}")
    print(f"Sysfs GPIO:       {'✓' if sysfs_works else '❌'}")
    
    if gpio_devices and (in_gpio_group or sysfs_works):
        print("\n🎉 GPIO should work! Try the DHT sensor again.")
        return 0
    else:
        print("\n❌ GPIO issues found. Follow the suggested fixes above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

# TODO: include "sudo modprobe raspberrypi-gpiomem"
