all: build-models build-floors build-ceilings build-stairs

TinyRenderer/TinyRenderer: TinyRenderer/Makefile
	$(MAKE) -C TinyRenderer

OgreAssimp/OgreAssimpConverter: OgreAssimp/Makefile
	$(MAKE) -C OgreAssimp

build-models: TinyRenderer/TinyRenderer OgreAssimp/OgreAssimpConverter
	$(MAKE) -C models

build-floors: TinyRenderer/TinyRenderer OgreAssimp/OgreAssimpConverter
	$(MAKE) -C floors

build-ceilings: TinyRenderer/TinyRenderer OgreAssimp/OgreAssimpConverter
	$(MAKE) -C ceilings

build-stairs: TinyRenderer/TinyRenderer OgreAssimp/OgreAssimpConverter
	$(MAKE) -C stairs

clean:
	@rm -rf tmp/
	@rm -rf *.log
	@rm -fv `find . -name "*.bak"`
	@rm -fv `find . -name "*~"`
	@rm -fv `find tiled -name "*.tsx"`

	$(MAKE) -C models clean
	$(MAKE) -C floors clean
	$(MAKE) -C ceilings clean
	$(MAKE) -C stairs clean

cleanall: clean
	$(MAKE) -C OgreAssimp cleanall
	$(MAKE) -C TinyRenderer cleanall

.PHONY: all build-models build-floors build-ceilings build-stairs clean cleanall
