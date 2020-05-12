OBJ_SOURCES = $(shell find . -maxdepth 1 -name "*.obj")

ISO_TILES = \
	$(OBJ_SOURCES:.obj=_1.iso.png) \
	$(OBJ_SOURCES:.obj=_2.iso.png) \
	$(OBJ_SOURCES:.obj=_3.iso.png) \
	$(OBJ_SOURCES:.obj=_4.iso.png) \
	$(OBJ_SOURCES:.obj=.mesh)

all: $(ISO_TILES)

../TinyRenderer/TinyRenderer:
	$(MAKE) -C ../TinyRenderer

../OgreAssimp/OgreAssimpConverter:
	$(MAKE) -C ../OgreAssimp

%_1.iso.png: %.obj ../TinyRenderer/TinyRenderer
	../TinyRenderer/TinyRenderer -w $< $@
	optipng $@

%_2.iso.png: %.obj ../TinyRenderer/TinyRenderer
	../TinyRenderer/TinyRenderer -w $< $@ -a 90
	optipng $@

%_3.iso.png: %.obj ../TinyRenderer/TinyRenderer
	../TinyRenderer/TinyRenderer -w $< $@ -a 180
	optipng $@

%_4.iso.png: %.obj ../TinyRenderer/TinyRenderer
	../TinyRenderer/TinyRenderer -w $< $@ -a 270
	optipng $@

%.mesh: %.obj ../OgreAssimp/OgreAssimpConverter
	../OgreAssimp/OgreAssimpConverter -uuid `echo '$<' | sha1sum | head -n1 | awk '{print $$1;}'` $<

%.iso.png: %_1.iso.png %_2.iso.png %_3.iso.png %_4.iso.png
	mkdir -p tmp
	@echo DIR: "'$(dir $@)'", FILE: "'$(basename $(basename $(notdir $@)))'", EXT: "'$(suffix $@)'"
	convert +append $+ $@
	optipng $@

clean:
	@rm -fv `find . -maxdepth 1 -name "*.iso.png"`
	@rm -fv `find . -maxdepth 1 -name "*.mesh"`
	@rm -fv `find . -maxdepth 1 -name "*.mesh.xml"`
	@rm -fv `find . -maxdepth 1 -name "*.material"`
	@rm -fv `find . -maxdepth 1 -name "*.skeleton"`
	@rm -fv `find . -maxdepth 1 -name "*.skeleton.xml"`
