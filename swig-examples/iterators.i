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

// Macro to construct iterable objects.
%define ogre_iterator(TYPE, PREFIX, VALUE_TYPE)

#if !SWIGRUBY

#if SWIGJAVA
%typemap(javainterfaces) TYPE##Iterator "java.util.Iterator<"#VALUE_TYPE">"
%typemap(javacode) TYPE##Iterator %{
  @Override
  public void remove() {
    throw new UnsupportedOperationException();
  }
%}
#endif

#if SWIGCSHARP
%typemap(csinterfaces) TYPE##Iterator "global::System.Collections.IEnumerator"
%typemap(cscode) TYPE##Iterator %{
  public object Current 
  {
     get
     {
       return GetCurrent();
     }
  }
%}
#endif

// Structure
%begin %{
typedef struct {
  PREFIX##_t *ptr;
  bool hasMoreElements() {
    return bool(!arg1->ptr);
  }
  VALUE_TYPE getNext() {
    VALUE_TYPE *value = ##VALUE_TYPE##_fromIter($self->ptr);
    $self->ptr = ##PREFIX##_next($self->ptr);
    return value;
  }
} TYPE##Iterator;
%}
typedef struct {} TYPE##Iterator;

// Exception to end iteration

#if SWIGJAVA
%exception TYPE##Iterator##::next() {
  if (!arg1->ptr) {
    jclass cls = (*jenv)->FindClass(jenv, "java/util/NoSuchElementException");
    (*jenv)->ThrowNew(jenv, cls, NULL);
    return $null;
  }
  $action;
}
#elif SWIGPYTHON
%exception TYPE##Iterator##::next() {
  if (!arg1->ptr) {
    SWIG_SetErrorObj(PyExc_StopIteration, SWIG_Py_Void());
    SWIG_fail;
  }
  $action;
}
%exception TYPE##Iterator##::__next__() {
  if (!arg1->ptr) {
    SWIG_SetErrorObj(PyExc_StopIteration, SWIG_Py_Void());
    SWIG_fail;
  }
  $action;
}
#endif

// Implementation of the iterator itself

%extend TYPE##Iterator {

  TYPE##Iterator(void *ptr) {
    TYPE##Iterator *iter = (TYPE##Iterator *)ckd_malloc(sizeof *iter);
    iter->ptr = (PREFIX##_t *)ptr;
    return iter;
  }

  ~TYPE##Iterator() {
    if ($self->ptr)
    PREFIX##_free($self->ptr);
    ckd_free($self);
  }

#if SWIGJAVA
  %newobject next;
  VALUE_TYPE * next() {
    if ($self->ptr) {
      VALUE_TYPE *value = ##VALUE_TYPE##_fromIter($self->ptr);
      $self->ptr = ##PREFIX##_next($self->ptr);
      return value;
    }

    return NULL;
  }
  bool hasNext() {
    return $self->ptr != NULL;
  }
#elif SWIGJAVASCRIPT
  %newobject next;
  VALUE_TYPE * next() {
    if ($self->ptr) {
      VALUE_TYPE *value = ##VALUE_TYPE##_fromIter($self->ptr);
      $self->ptr = ##PREFIX##_next($self->ptr);
      return value;
    }

    return NULL;
  }
#elif SWIGPYTHON
  // Python2
  %newobject next;
  VALUE_TYPE * next() {
    if ($self->ptr) {
      VALUE_TYPE *value = ##VALUE_TYPE##_fromIter($self->ptr);
      $self->ptr = ##PREFIX##_next($self->ptr);
      return value;
    }
    return NULL;
  }

  // Python3
  %newobject __next__;
  VALUE_TYPE * __next__() {
    if ($self->ptr) {
      VALUE_TYPE *value = ##VALUE_TYPE##_fromIter($self->ptr);
      $self->ptr = ##PREFIX##_next($self->ptr);
      return value;
    }
    return NULL;
  }
#elif SWIGCSHARP
  bool MoveNext() {
    if(!$self || !$self->ptr)
        return false;
    $self->ptr = ##PREFIX##_next($self->ptr);
    if ($self->ptr) {
    return true;
    }
    return false;
  }
  
  void Reset() {
    return;
  }

  VALUE_TYPE *GetCurrent() {
    VALUE_TYPE *value = ##VALUE_TYPE##_fromIter($self->ptr);
    return value;
  }
#endif


}

#endif // SWIGRUBY

%enddef


%define ogre_iterable(TYPE, ITER_TYPE, PREFIX, INIT_PREFIX, VALUE_TYPE)

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
    ##PREFIX##_t *iter = INIT_PREFIX##($self);
    while (iter) {
      VALUE_TYPE *value = ##VALUE_TYPE##_fromIter(iter);
      rb_yield(SWIG_NewPointerObj(SWIG_as_voidptr(value), SWIGTYPE_p_##VALUE_TYPE##, 0 |  0 ));
      iter = PREFIX##_next(iter);
    }
    return;
  }

  void each(int count) {
    ##PREFIX##_t *iter = INIT_PREFIX##($self);
    int cnt = 0;
    while (iter && cnt < count) {
      VALUE_TYPE *value = ##VALUE_TYPE##_fromIter(iter);
      rb_yield(SWIG_NewPointerObj(SWIG_as_voidptr(value), SWIGTYPE_p_##VALUE_TYPE##, 0 |  0 ));
      iter = PREFIX##_next(iter);
      cnt++;
    }
    if (iter)
    PREFIX##_free(iter);
    return;
  }

#elif SWIGJAVA
  %newobject iterator;
  ITER_TYPE##Iterator * iterator() {
    return new_##ITER_TYPE##Iterator(INIT_PREFIX##($self));
  }
#elif SWIGCSHARP
  %newobject get_enumerator;
  ITER_TYPE##Iterator *get_enumerator() {
    return new_##ITER_TYPE##Iterator(INIT_PREFIX##($self));
  } 

#else  /* PYTHON, JS */
  %newobject __iter__;
  ITER_TYPE##Iterator * __iter__() {
    return new_##ITER_TYPE##Iterator(INIT_PREFIX##($self));
  }  
#endif 

}

%enddef
