#!/usr/bin/make -f

CC= gcc
CXX= g++
RM= rm -f

PKGCONFIG= pkg-config
PACKAGES= gl

CFLAGS= -O2 -g -Wall -std=c++17 \
	-fstack-protector-strong \
	-Wall \
	-Wformat \
	-Werror=format-security \
	-Wdate-time \
	-D_FORTIFY_SOURCE=2 \
	$(shell $(PKGCONFIG) --cflags $(PACKAGES))

LDFLAGS= \
	-Wl,--as-needed \
	-Wl,--no-undefined \
	-Wl,--no-allow-shlib-undefined

INCS= \
	-I.

LIBS= \
	-lm -lfltk -lfltk_gl \
	$(shell $(PKGCONFIG) --libs $(PACKAGES))

SRCS= DemoUI.cpp MyWindow.cpp defmesh.cpp processor.cpp motion.cpp filter.cpp \
	Pinocchio/attachment.cpp Pinocchio/discretization.cpp Pinocchio/indexer.cpp \
	Pinocchio/lsqSolver.cpp Pinocchio/mesh.cpp Pinocchio/graphutils.cpp \
	Pinocchio/intersector.cpp Pinocchio/matrix.cpp Pinocchio/skeleton.cpp \
	Pinocchio/embedding.cpp Pinocchio/pinocchioApi.cpp Pinocchio/PinnocchioCallback.cpp \
	Pinocchio/refinement.cpp Pinocchio/quatinterface.cpp Pinocchio/yaml.cpp

OBJS= $(subst .cpp,.o,$(SRCS))

BINARY= DemoUI

all: $(BINARY)

$(BINARY): $(OBJS)
	$(CXX) $(LDFLAGS) -o $@ $(OBJS) $(LIBS)

%.o: %.cpp
	$(CXX) -o $@ -c $< $(INCS) $(CFLAGS)

%.o: %.cc
	$(CXX) -o $@ -c $< $(INCS) $(CFLAGS)

%.o: %.c
	$(CC) -o $@ -c $< $(INCS) $(CFLAGS)

depend: .depend

.depend: $(SRCS)
	$(RM) ./.depend
	$(CXX) $(CFLAGS) -MM $^>>./.depend;

clean:
	$(RM) $(OBJS) $(BINARY)
	$(RM) -fv *~ .depend core *.out *.bak
	$(RM) -fv *.o *.a *~
	$(RM) -fv */*.o */*.a */*~

test: $(BINARY)
	./$(BINARY) data/test.obj -motion data/crossWalk.txt

include .depend

.PHONY: all depend clean distclean cleanall
