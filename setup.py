from setuptools import setup, find_packages, Extension
import os
import sys

import Adafruit_DHT.platform_detect as platform_detect


BINARY_COMMANDS = [
    'build_ext',
    'build_clib',
    'bdist',
    'bdist_dumb',
    'bdist_rpm',
    'bdist_wininst',
    'bdist_wheel',
    'install'
]


def is_binary_install():
    do_binary = [command for command in BINARY_COMMANDS if command in sys.argv]
    return len(do_binary) > 0


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()



# Pick the right extension to compile based on the platform.
extensions = []
if not is_binary_install():
    print('Skipped loading platform-specific extensions for Adafruit_DHT (we are generating a cross-platform source distribution).')
else:
    # Get the Pi version (1, 2, 3, 4 or 5 for ARM64)
    pi_version = platform_detect.pi_version()

    # Build the right extension depending on the Pi version.
    if pi_version == 1:
        extensions.append(Extension("Adafruit_DHT.Raspberry_Pi_Driver",
                                    ["source/_Raspberry_Pi_Driver.c", "source/common_dht_read.c", "source/Raspberry_Pi/pi_dht_read.c", "source/Raspberry_Pi/pi_mmio.c"],
                                    libraries=['rt'],
                                    extra_compile_args=['-std=gnu99']))
    elif pi_version == 2:
        extensions.append(Extension("Adafruit_DHT.Raspberry_Pi_2_Driver",
                                    ["source/_Raspberry_Pi_2_Driver.c", "source/common_dht_read.c", "source/Raspberry_Pi_2/pi_2_dht_read.c", "source/Raspberry_Pi_2/pi_2_mmio.c"],
                                    libraries=['rt'],
                                    extra_compile_args=['-std=gnu99']))
    elif pi_version == 3:
        extensions.append(Extension("Adafruit_DHT.Raspberry_Pi_2_Driver",
                                    ["source/_Raspberry_Pi_2_Driver.c", "source/common_dht_read.c", "source/Raspberry_Pi_2/pi_2_dht_read.c", "source/Raspberry_Pi_2/pi_2_mmio.c"],
                                    libraries=['rt'],
                                    extra_compile_args=['-std=gnu99']))
    elif pi_version == 4:
        extensions.append(Extension("Adafruit_DHT.Raspberry_Pi_ARM64_Driver",
                                    ["source/_Raspberry_Pi_ARM64_Driver.c", "source/common_dht_read.c", "source/Raspberry_Pi_ARM64/pi_arm64_dht_read.c", "source/Raspberry_Pi_ARM64/pi_arm64_mmio.c"],
                                    libraries=['rt'],
                                    extra_compile_args=['-std=gnu99']))
    elif pi_version == 5:
        extensions.append(Extension("Adafruit_DHT.Raspberry_Pi_ARM64_Driver",
                                    ["source/_Raspberry_Pi_ARM64_Driver.c", "source/common_dht_read.c", "source/Raspberry_Pi_ARM64/pi_arm64_dht_read.c", "source/Raspberry_Pi_ARM64/pi_arm64_mmio.c"],
                                    libraries=['rt'],
                                    extra_compile_args=['-std=gnu99']))
    else:
        print('Could not detect if running on the Raspberry Pi. Test driver will be used')
        extensions.append(Extension("Adafruit_DHT.Test_Driver",
                                    ["source/_Test_Driver.c", "source/Test/test_dht_read.c"],
                                    extra_compile_args=['-std=gnu99']))

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

# Call setuptools setup function to install package.
setup(name              = 'RPI_Adafruit_Python_DHT',
      version           = '2.0.0',
      author            = 'Tony DiCola',
      author_email      = 'tdicola@adafruit.com',
      description       = 'Library to get readings from the DHT11, DHT22, and AM2302 humidity and temperature sensors on a Raspberry Pi.',
      long_description  = read('README.md'),
      license           = 'MIT',
      classifiers       = classifiers,
      url               = 'https://github.com/SimoMart88/RPI_Adafruit_Python_DHT',
      packages          = find_packages(),
      ext_modules       = extensions)
