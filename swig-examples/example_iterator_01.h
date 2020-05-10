#include <vector>

class Element
{
public:
  Element();
  ~Element();

  int get() const;
  void set(const int var);

private:
  int variable_;
};

class Collection
{
public:
  Collection();
  ~Collection();

  void add(const Element& element);

  typedef std::vector<Element> tElements;

  // iterators
  typedef tElements::iterator iterator;
  typedef tElements::const_iterator const_iterator;
  iterator begin();
  const_iterator begin() const;
  iterator end();
  const_iterator end() const;

private:
  tElements          elements_;
};
