#include "example_iterator_01.h"

Element::Element() {}

Element::~Element() {}

int Element::get() const
{
  return variable_;
}

void Element::set(const int var)
{
  variable_ = var;
}

Collection::Collection() : elements_() {}

Collection::~Collection() {}

void Collection::add(const Element& element)
{
  elements_.push_back(element);
}

Collection::iterator Collection::begin()
{
  return elements_.begin();
}

Collection::const_iterator Collection::begin() const
{
  return elements_.begin();
}

Collection::iterator Collection::end()
{
  return elements_.end();
}

Collection::const_iterator Collection::end() const
{
  return elements_.end();
}
