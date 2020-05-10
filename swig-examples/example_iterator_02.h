#include <vector>
#include <iostream>

std::ostream& (*getColor(const void * ptr))(std::ostream& stream);

class Element
{
public:
	Element();
	Element(const Element &e);
	~Element();

	int get() const;
	void set(const int var);

private:
	int m_variable;
};

class Collection
{
public:
	Collection();
	~Collection();

	void add(const Element& element);

	typedef std::vector<Element> tElements;

	typedef tElements::iterator Iterator;
	typedef tElements::const_iterator ConstIterator;

	Iterator begin();
	ConstIterator begin() const;
	Iterator end();
	ConstIterator end() const;

private:
	tElements m_elements;
};

class CollectionIterator;
std::ostream & operator<<(std::ostream & os, const CollectionIterator * ptr);

class CollectionIterator {
public:
	inline CollectionIterator(Collection * col) : itr(col->begin()), end(col->end()) {
		std::cout << this << ": " << "CollectionIterator()" << std::endl;
	}
	inline ~CollectionIterator() {
		std::cout << this << ": " << "~CollectionIterator()" << std::endl;
	}
	inline bool hasMoreElements() {
		if (itr != end )
			std::cout << this << ": " << "hasMoreElements()" << " [" << itr->get() << "]" << " [" << (itr != end ? "true" : "false") << "]" << std::endl;
		else
			std::cout << this << ": " << "hasMoreElements()" << " [" << (itr != end ? "true" : "false") << "]" << std::endl;
		return (itr != end);
	}
	inline Element next() {
		std::cout << this << ": " << "next()" << std::endl;
		Element & value = *itr;
		itr++;
		return value;
	}
	inline Element peekNext() {
		std::cout << this << ": " << "peekNext()" << std::endl;
		Element & value = *itr;
		return value;
	}
private:
	Collection::Iterator itr;
	Collection::Iterator end;
};
