%module test

%{
#define SWIG_FILE_WITH_INIT
#include "test.h"
%}

int fact(int n);