// This header allows to share *clientInterp and *serverInterp between main.cpp and realms.cpp.

#pragma once

#include <Python.h>

extern PyThreadState *clientInterp, *serverInterp;
