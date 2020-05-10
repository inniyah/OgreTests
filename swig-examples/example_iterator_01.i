%module example_iterator_01
%{
#include "example_iterator_01.h"
%}

%inline %{
class StopIterator {};
class Iterator {
  public:
    Iterator(Collection::iterator _cur, Collection::iterator _end) : cur(_cur), end(_end) {}
    Iterator* __iter__()
    {
      return this;
    }
    Collection::iterator cur;
    Collection::iterator end;
  };
%}

%include "example_iterator_01.h"

%include "exception.i"
%exception Iterator::__next__ {
  try
  {
    $action // calls %extend function next() below
  }
  catch (StopIterator)
  {
    PyErr_SetString(PyExc_StopIteration, "End of iterator");
    return NULL;
  }
}

%extend Iterator
{
  Element& __next__()
  {
    if ($self->cur != $self->end)
    {
      // dereference the iterator and return reference to the object,
      // after that it increments the iterator
      return *$self->cur++;
    }
    throw StopIterator();
  }
}

%extend Collection {
  Iterator __iter__()
  {
    // return a constructed Iterator object
    return Iterator($self->begin(), $self->end());
  }
};
