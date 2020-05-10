%module example_iterator_03
%{
#include "example_iterator_03.h"

#include <iostream>

class CollectionIterator {
public:
	CollectionIterator(Collection * col) : itr(col->begin()), end(col->end()) {
		std::cout << "CollectionIterator()" << std::endl;
	}
	~CollectionIterator() {
		std::cout << "~CollectionIterator()" << std::endl;
	}
	inline bool hasMoreElements() {
		if (itr != end )
			std::cout << "CollectionIterator::hasMoreElements()" << " [" << itr->get() << "]" << " [" << (itr != end ? "true" : "false") << "]" << std::endl;
		else
			std::cout << "CollectionIterator::hasMoreElements()" << " [" << (itr != end ? "true" : "false") << "]" << std::endl;
		return (itr != end);
	}
	inline Element next() {
		std::cout << "CollectionIterator::next()" << std::endl;
		Element & value = *itr;
		itr++;
		return value;
	}
	inline Element peekNext() {
		std::cout << "CollectionIterator::peekNext()" << std::endl;
		Element & value = *itr;
		return value;
	}
private:
	Collection::Iterator itr;
	Collection::Iterator end;
};
%}

%include "example_iterator_03.h"

%include "exception.i"
%include "iterators_03.i"

struct CollectionIterator { };

%extend CollectionIterator {
  CollectionIterator(void * col) {
    return new CollectionIterator((Collection *)col);
  }
  ~CollectionIterator() {
    delete $self;
  }
}

iterator(Collection, CollectionIterator, Element)
