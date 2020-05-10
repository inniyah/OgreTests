CC= gcc
CXX= g++
RM= rm -f
SWIG=swig

SWIG_LIBS= \
	-I/usr/include/OGRE \
	-I/usr/include/OGRE/Bites \
	-I/usr/include/OGRE/Overlay \
	-I/usr/include/OGRE/RTShaderSystem \
	-I/usr/include/OGRE/Terrain

CFLAGS= $(OPT_CFLAGS) -fPIC -Wall -Wno-unused-variable -Wno-unused-value -Wno-unused-but-set-variable
LDFLAGS= -Wl,--as-needed -Wl,--no-undefined -Wl,--no-allow-shlib-undefined
LIBS= 
OPTS= -O2 -g
DEFS= 
INCS= 

CSTD=-std=c11
CPPSTD=-std=c++11

PKG_CONFIG= python3 OGRE OGRE-Bites OGRE-Overlay OGRE-RTShaderSystem OGRE-Terrain

ifndef PKG_CONFIG
PKG_CONFIG_CFLAGS=
PKG_CONFIG_LDFLAGS=
PKG_CONFIG_LIBS=
else
PKG_CONFIG_CFLAGS=`pkg-config --cflags $(PKG_CONFIG)`
PKG_CONFIG_LDFLAGS=`pkg-config --libs-only-L $(PKG_CONFIG)`
PKG_CONFIG_LIBS=`pkg-config --libs-only-l $(PKG_CONFIG)`
endif

all: \
	example_iterator_01.py _example_iterator_01.so \
	example_iterator_02.py _example_iterator_02.so \
	example_iterator_03.py _example_iterator_03.so

%_wrap.cxx %.py: %.i
	$(SWIG) -c++ -python $(SWIG_LIBS) $<

_example_iterator_01.so: example_iterator_01.o
_example_iterator_02.so: example_iterator_02.o
_example_iterator_03.so: example_iterator_03.o

_%.so: %_wrap.o
	$(CXX) -shared $+ -o $@ `pkg-config --libs OGRE`

%.o: %.cxx
	$(CXX) $(CPPSTD) $(OPTS) -o $@ -c $< $(DEFS) $(INCS) $(CFLAGS) $(PKG_CONFIG_CFLAGS)

%.o: %.cpp
	$(CXX) $(CPPSTD) $(OPTS) -o $@ -c $< $(DEFS) $(INCS) $(CFLAGS) $(PKG_CONFIG_CFLAGS)

%.o: %.c
	$(CC) $(CSTD) $(OPTS) -o $@ -c $< $(DEFS) $(INCS) $(CFLAGS) $(PKG_CONFIG_CFLAGS)

test_01: example_iterator_01.py _example_iterator_01.so
	python3 test_example_iterator_01.py

test_02: example_iterator_02.py _example_iterator_02.so
	python3 test_example_iterator_02.py

test_03: example_iterator_03.py _example_iterator_03.so
	python3 test_example_iterator_03.py

test: test_01 test_02 test_03

clean:
	$(RM) *_wrap.cxx Ogre*.py *_wrap.o _*.so *.o example_iterator_01.py
