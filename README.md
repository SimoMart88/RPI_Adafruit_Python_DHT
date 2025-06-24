Adafruit Python DHT Sensor Library for RaspberryPI
=======================

**This library has been deprecated by the original authors!**
See https://github.com/adafruit/Adafruit_Python_DHT

Since the proposed solution, CircuitPython libraries, doesn't work for me on 'RaspberryPi 1b', 
I decided to "resume" it but with a reduced scope.

**Reason why alternative solution does not work for me:** https://github.com/adafruit/Adafruit_Blinka/issues/210

**Scope update:** Library will work ONLY for RaspberryPI (no more compatibility with Beaglebone Black) 
and it will properly support the installation with Uv.

---------------------------------------

Python library to read the DHT series of humidity and temperature sensors on a Raspberry Pi.

Designed specifically to work with the Adafruit DHT series sensors ---->
https://www.adafruit.com/products/385

Currently the library is tested with Python 2.6, 2.7, 3.3, 3.4 and 3.9.
It should work with Python greater than 3.9, too.

Installing
----------

### Dependencies

For all platforms (Raspberry Pi) make sure your system is
able to compile and download Python extensions with **pip**:

On Raspbian you can ensure your
system is ready by running one or two of the following sets of commands:

Python 2:

````sh
sudo apt-get update
sudo apt-get install python-pip
sudo python -m pip install --upgrade pip setuptools wheel
````

Python 3:

````sh
sudo apt-get update
sudo apt-get install python3-pip
sudo python3 -m pip install --upgrade pip setuptools wheel
````

### Install with pip

Use `pip` to install from PyPI.

Python 2:

```sh
sudo pip install Adafruit_DHT
```

Python 3:

```sh
sudo pip3 install Adafruit_DHT
```

### Compile and install from the repository

First download the library source code from the [GitHub releases
page](https://github.com/adafruit/Adafruit_Python_DHT/releases), unzipping the
archive, and execute:

Python 2:

```sh
cd Adafruit_Python_DHT
sudo python setup.py install
```

Python 3:

```sh
cd Adafruit_Python_DHT
sudo python3 setup.py install
```

You may also git clone the repository if you want to test an unreleased
version:

```sh
git clone https://github.com/SimoMart88/RPI_Adafruit_Python_DHT
```

Usage
-----

See example of usage in the examples folder.

Author
------

Adafruit invests time and resources providing this open source code, please
support Adafruit and open-source hardware by purchasing products from Adafruit!

Originally written by Tony DiCola for Adafruit Industries.

MIT license, all text above must be included in any redistribution
