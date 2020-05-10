#include <vector>

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

