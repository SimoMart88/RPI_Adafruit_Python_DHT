#!/usr/bin/env python3
"""
Debug the build process and check what drivers were actually compiled.
"""

import os
import sys
import subprocess
import glob

def check_platform_detection():
    """Check what platform is detected during build."""
    print("Platform Detection Test")
    print("=" * 40)
    
    try:
        # Add current directory to path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        sys.path.insert(0, parent_dir)
        
        import Adafruit_DHT.platform_detect as platform_detect
        version = platform_detect.pi_version()
        print(f"Detected Pi version: {version}")
        
        # Check /proc/cpuinfo details
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
        
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
        
        return version
        
    except Exception as e:
        print(f"Platform detection failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def check_compiled_modules():
    """Check what Python extension modules were actually compiled."""
    print("\nCompiled Modules Check")
    print("=" * 40)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Look for .so files (compiled extensions)
    adafruit_dir = os.path.join(parent_dir, 'Adafruit_DHT')
    so_files = glob.glob(os.path.join(adafruit_dir, '*.so'))
    
    print(f"Looking in: {adafruit_dir}")
    print("Found compiled modules:")
    
    if so_files:
        for so_file in so_files:
            basename = os.path.basename(so_file)
            print(f"  ✓ {basename}")
    else:
        print("  ❌ No .so files found")
    
    # Also check build directory
    build_dir = os.path.join(parent_dir, 'build')
    if os.path.exists(build_dir):
        build_so_files = glob.glob(os.path.join(build_dir, '**', '*.so'), recursive=True)
        if build_so_files:
            print("Found in build directory:")
            for so_file in build_so_files:
                rel_path = os.path.relpath(so_file, parent_dir)
                print(f"  ✓ {rel_path}")
    
    return so_files

def test_manual_import():
    """Test importing each possible driver manually."""
    print("\nManual Import Test")
    print("=" * 40)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    sys.path.insert(0, parent_dir)
    
    drivers_to_test = [
        'Raspberry_Pi_Driver',
        'Raspberry_Pi_2_Driver', 
        'Raspberry_Pi_ARM64_Driver',
        'Test_Driver'
    ]
    
    working_drivers = []
    
    for driver in drivers_to_test:
        try:
            module = __import__(f'Adafruit_DHT.{driver}', fromlist=[driver])
            print(f"✓ {driver} - imports successfully")
            working_drivers.append(driver)
        except ImportError as e:
            print(f"❌ {driver} - {e}")
        except Exception as e:
            print(f"⚠ {driver} - unexpected error: {e}")
    
    return working_drivers

def force_rebuild():
    """Force a complete rebuild of the extensions."""
    print("\nForce Rebuild")
    print("=" * 40)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    try:
        os.chdir(parent_dir)
        
        # Clean previous build
        print("Cleaning previous build...")
        subprocess.run(['rm', '-rf', 'build/'], check=False)
        subprocess.run(['find', '.', '-name', '*.so', '-delete'], check=False)
        
        # Force rebuild
        print("Building extensions...")
        result = subprocess.run([
            sys.executable, 'setup.py', 'build_ext', '--force', '--inplace'
        ], capture_output=True, text=True)
        
        print("Build output:")
        print(result.stdout)
        if result.stderr:
            print("Build errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Rebuild failed: {e}")
        return False

def suggest_workaround():
    """Suggest using a working driver as workaround."""
    print("\nWorkaround Suggestions")
    print("=" * 40)
    
    print("Since ARM64 driver failed to compile, try these workarounds:")
    print()
    print("1. Use Pi 2 driver (often works on Pi 4/5):")
    print("   Edit Adafruit_DHT/common.py")
    print("   Change version 4/5 detection to use Raspberry_Pi_2")
    print()
    print("2. Force Pi 2 driver in your code:")
    print("   import Adafruit_DHT.Raspberry_Pi_2 as platform")
    print("   humidity, temp = platform.read(sensor, pin)")
    print()
    print("3. Install original Adafruit library:")
    print("   pip install Adafruit-DHT")

def main():
    """Run build diagnostics."""
    print("Adafruit DHT Build Diagnostic")
    print("=" * 50)
    
    # Check platform detection
    pi_version = check_platform_detection()
    
    # Check compiled modules
    compiled_modules = check_compiled_modules()
    
    # Test imports
    working_drivers = test_manual_import()
    
    # Try rebuild if ARM64 driver missing
    if pi_version in [4, 5] and 'Raspberry_Pi_ARM64_Driver' not in [os.path.basename(m).split('.')[0] for m in compiled_modules]:
        print("\nARM64 driver not found, attempting rebuild...")
        rebuild_success = force_rebuild()
        
        if rebuild_success:
            print("Rebuild completed, rechecking...")
            compiled_modules = check_compiled_modules()
            working_drivers = test_manual_import()
    
    # Summary and suggestions
    print("\n" + "=" * 50)
    print("Diagnostic Summary:")
    print(f"Pi version: {pi_version}")
    print(f"Compiled modules: {len(compiled_modules)}")
    print(f"Working drivers: {working_drivers}")
    
    if pi_version in [4, 5] and 'Raspberry_Pi_ARM64_Driver' not in working_drivers:
        print("\n❌ ARM64 driver compilation failed")
        suggest_workaround()
        return 1
    elif working_drivers:
        print(f"\n✓ At least one driver works: {working_drivers[0]}")
        return 0
    else:
        print("\n❌ No drivers compiled successfully")
        suggest_workaround()
        return 1

if __name__ == '__main__':
    sys.exit(main())