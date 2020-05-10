#include "example_iterator_03.h"

// https://github.com/ikalnytskyi/termcolor
#include "termcolor.hpp"

#include <cstdint>

// http://burtleburtle.net/bob/hash/integer.html
inline uint32_t hash( uint32_t a) {
	a = a ^ (a>>4);
	a = (a^0xdeadbeef) + (a<<5);
	a = a ^ (a>>11);
	return a;
}

std::ostream& (*getColor(const void * ptr))(std::ostream& stream) {
	std::ostream& (*color)(std::ostream& stream) = nullptr;
	switch( hash((uintptr_t)ptr) % 16 ) {
		case 0: color = termcolor::grey; break;
		case 1: color = termcolor::red; break;
		case 2: color = termcolor::green; break;
		case 3: color = termcolor::yellow; break;
		case 4: color = termcolor::blue; break;
		case 5: color = termcolor::magenta; break;
		case 6: color = termcolor::cyan; break;
		case 7: color = termcolor::white; break;

		case 8: color = termcolor::on_grey; break;
		case 9: color = termcolor::on_red; break;
		case 10: color = termcolor::on_green; break;
		case 11: color = termcolor::on_yellow; break;
		case 12: color = termcolor::on_blue; break;
		case 13: color = termcolor::on_magenta; break;
		case 14: color = termcolor::on_cyan; break;
		default: color = termcolor::on_white; break;
	}
	return color;
}

std::ostream & operator<<(std::ostream & os, const Element * ptr) {
	auto color = getColor(ptr);
	std::cout << "[E#" << color << (const void *)ptr << termcolor::reset << "]";
	return os;
}

std::ostream & operator<<(std::ostream & os, const Collection * ptr) {
	auto color = getColor(ptr);
	std::cout << "[C#" << color << (const void *)ptr << termcolor::reset << "]";
	return os;
}

Element::Element() {
	//~ std::cout << this << ": " << "Element()" << std::endl;
}

Element::Element(const Element &e) : m_variable(e.m_variable) {
	//~ std::cout << this << ": " << "Element(&)" << " [v=" << m_variable << "]" << std::endl;
}

Element::~Element() {
	//~ std::cout << this << ": " << "~Element()" << " [v=" << m_variable << "]" << std::endl;
}

int Element::get() const {
	return m_variable;
}

void Element::set(const int var)
{
	//~ std::cout << this << ": " << "Element::set()" << " [v=" << var << "]" << std::endl;
	m_variable = var;
}

Collection::Collection() : m_elements() {
	//~ std::cout << this << ": " << "Collection()" << std::endl;
}

Collection::~Collection() {
	//~ std::cout << this << ": " << "~Collection()" << std::endl;
}

void Collection::add(const Element& element)
{
	//~ std::cout << this << ": " << "Collection::add()" << &element << " [" << element.get() << "]" << std::endl;
	m_elements.push_back(element);
}

Collection::Iterator Collection::begin()
{
	return m_elements.begin();
}

Collection::ConstIterator Collection::begin() const
{
	return m_elements.begin();
}

Collection::Iterator Collection::end()
{
	return m_elements.end();
}

Collection::ConstIterator Collection::end() const
{
	return m_elements.end();
}
