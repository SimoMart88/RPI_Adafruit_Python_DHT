// Copyright (c) 2014 Adafruit Industries
// Author: Tony DiCola
// ARM64 compatibility implementation

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
#include <Python.h>

#include "Raspberry_Pi_ARM64/pi_arm64_dht_read.h"

static PyObject *pi_arm64_dht_read_wrapper(PyObject *self, PyObject *args) {
  int type, pin;
  float humidity, temperature;
  if (!PyArg_ParseTuple(args, "ii", &type, &pin)) {
    return NULL;
  }
  int result = pi_arm64_dht_read(type, pin, &humidity, &temperature);
  return Py_BuildValue("iff", result, humidity, temperature);
}

static PyMethodDef module_methods[] = {
  {"read", pi_arm64_dht_read_wrapper, METH_VARARGS, "Read DHT sensor value"},
  {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef module_definition = {
  PyModuleDef_HEAD_INIT,
  "Raspberry_Pi_ARM64_Driver",
  "ARM64 Raspberry Pi DHT sensor driver",
  -1,
  module_methods
};

PyMODINIT_FUNC PyInit_Raspberry_Pi_ARM64_Driver(void) {
  return PyModule_Create(&module_definition);
}
#else
PyMODINIT_FUNC initRaspberry_Pi_ARM64_Driver(void) {
  Py_InitModule("Raspberry_Pi_ARM64_Driver", module_methods);
}
#endif