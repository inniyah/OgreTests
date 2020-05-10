/* ====================================================================
 * Copyright (c) 2013 Carnegie Mellon University.  All rights
 * reserved.
 *
 * Copyright (c) 2020 Miriam Ruiz <miriam@debian.org>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * This work was supported in part by funding from the Defense Advanced
 * Research Projects Agency and the National Science Foundation of the
 * United States of America, and the CMU Sphinx Speech Consortium.
 *
 * THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND
 * ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
 * NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * ====================================================================
 */

/////////////////////////////////////////////////////////////////////

%define ogre_iterator(TYPE, ITER_TYPE, VALUE_TYPE)

#if SWIGJAVA
%typemap(javainterfaces) ITER_TYPE "java.util.Iterator<"#VALUE_TYPE">"
%typemap(javacode) ITER_TYPE %{
  @Override
  public void remove() {
    throw new UnsupportedOperationException();
  }
%}
#endif

#if SWIGCSHARP
%typemap(csinterfaces) ITER_TYPE "global::System.Collections.IEnumerator"
%typemap(cscode) ITER_TYPE %{
  public object Current 
  {
     get
     {
       return GetCurrent();
     }
  }
%}
#endif


// Exception to end iteration

#if SWIGJAVA
%exception ITER_TYPE##::next() {
  if (!arg1->hasMoreElements()) {
    jclass cls = (*jenv)->FindClass(jenv, "java/util/NoSuchElementException");
    (*jenv)->ThrowNew(jenv, cls, NULL);
    return $null;
  }
  $action;
}
#elif SWIGPYTHON
%exception ITER_TYPE##::next() {
  if (!arg1->hasMoreElements()) {
    SWIG_SetErrorObj(PyExc_StopIteration, SWIG_Py_Void());
    SWIG_fail;
  }
  $action;
}
%exception ITER_TYPE##::__next__() {
  if (!arg1->hasMoreElements()) {
    SWIG_SetErrorObj(PyExc_StopIteration, SWIG_Py_Void());
    SWIG_fail;
  }
  $action;
}
#endif


// Implementation of the iterator itself

%extend ITER_TYPE {

#if SWIGJAVA
  %newobject next;
  VALUE_TYPE * next() {
    if ($self->hasMoreElements()) {
      return $self->next();
    }
    return NULL;
  }
  bool hasNext() {
    return $self->hasMoreElements();
  }
#elif SWIGJAVASCRIPT
  %newobject next;
  VALUE_TYPE * next() {
    if ($self->hasMoreElements()) {
      return $self->next();
    }
    return NULL;
  }
#elif SWIGPYTHON
  // Python2
  %newobject next;
  VALUE_TYPE * next() {
    if ($self->hasMoreElements()) {
      return $self->next();
    }
    return NULL;
  }

  // Python3
  %newobject __next__;
  VALUE_TYPE * __next__() {
    if ($self->hasMoreElements()) {
      return $self->next();
    }
    return NULL;
  }
#elif SWIGCSHARP
  bool MoveNext() {
    if(!$self || !$self->hasMoreElements())
        return false;
    $self->next();
    if ($self->hasMoreElements()) {
      return true;
    }
    return false;
  }
  
  void Reset() {
    return;
  }

  VALUE_TYPE *GetCurrent() {
    VALUE_TYPE *value = $self->peekNext();
    return value;
  }
#endif

}


// Methods to retrieve the iterator from the container

#if SWIGJAVA
%typemap(javainterfaces) TYPE "Iterable<"#VALUE_TYPE">"
#endif

#if SWIGCSHARP
%typemap(csinterfaces) TYPE "global::System.Collections.IEnumerable"
%typemap(cscode) TYPE %{
  global::System.Collections.IEnumerator global::System.Collections.IEnumerable.GetEnumerator() {
     return (global::System.Collections.IEnumerator) GetEnumerator();
  }
%}
#endif

%extend TYPE {

#if SWIGRUBY
  void each() {
    ITER_TYPE iter($self);
    while (iter.hasMoreElements()) {
      VALUE_TYPE * value = iter.next();
      rb_yield(SWIG_NewPointerObj(SWIG_as_voidptr(value), SWIGTYPE_p_##VALUE_TYPE##, 0 |  0 ));
    }
    return;
  }

  void each(int count) {
    ITER_TYPE iter($self);
    int cnt = 0;
    while (iter.hasMoreElements() && cnt < count) {
      VALUE_TYPE * value = iter.next();
      rb_yield(SWIG_NewPointerObj(SWIG_as_voidptr(value), SWIGTYPE_p_##VALUE_TYPE##, 0 |  0 ));
      cnt++;
    }
    return;
  }

#elif SWIGJAVA
  %newobject iterator;
  ITER_TYPE * iterator() {
    return new ITER_TYPE($self);
  }
#elif SWIGCSHARP
  %newobject get_enumerator;
  ITER_TYPE *get_enumerator() {
    return new ITER_TYPE($self);
  } 

#else  /* PYTHON, JS */
  %newobject __iter__;
  ITER_TYPE * __iter__() {
    return new ITER_TYPE($self);
  }  
#endif 

}

%enddef
