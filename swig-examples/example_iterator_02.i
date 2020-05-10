%module example_iterator_02
%{
#include "example_iterator_02.h"
%}

%include "example_iterator_02.h"

%include "exception.i"
%include "iterators_02.i"

iterator(Collection, CollectionIterator, Element)
