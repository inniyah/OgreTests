MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MKFILE_DIR := $(dir $(MKFILE_PATH))

TILES_ID := $(lastword $(subst /, ,$(MKFILE_DIR)))

OBJ_SOURCES = $(shell find . -maxdepth 1 -name "*.obj")

ISO_TILES = \
	$(OBJ_SOURCES:.obj=_1.iso.png) \
	$(OBJ_SOURCES:.obj=_2.iso.png) \
	$(OBJ_SOURCES:.obj=_3.iso.png) \
	$(OBJ_SOURCES:.obj=_4.iso.png) \
	$(OBJ_SOURCES:.obj=.mesh)

all: $(ISO_TILES)

test:
	echo $(MKFILE_PATH) "->" $(MKFILE_DIR)  "->" $(TILES_ID)

../TinyRenderer/TinyRenderer:
	$(MAKE) -C ../TinyRenderer

../OgreAssimp/OgreAssimpConverter:
	$(MAKE) -C ../OgreAssimp

%_1.iso.png: %.obj ../TinyRenderer/TinyRenderer
	../TinyRenderer/TinyRenderer -w $< $@
	optipng $@
	../scripts/add_metadata.py $< -d metadata.json -t $(TILES_ID) -D IsoTile1 $@

%_2.iso.png: %.obj ../TinyRenderer/TinyRenderer
	../TinyRenderer/TinyRenderer -w $< $@ -a 90
	optipng $@
	../scripts/add_metadata.py $< -d metadata.json -t $(TILES_ID) -D IsoTile2 $@

%_3.iso.png: %.obj ../TinyRenderer/TinyRenderer
	../TinyRenderer/TinyRenderer -w $< $@ -a 180
	optipng $@
	../scripts/add_metadata.py $< -d metadata.json -t $(TILES_ID) -D IsoTile3 $@

%_4.iso.png: %.obj ../TinyRenderer/TinyRenderer
	../TinyRenderer/TinyRenderer -w $< $@ -a 270
	optipng $@
	../scripts/add_metadata.py $< -d metadata.json -t $(TILES_ID) -D IsoTile4 $@

%.mesh: %.obj ../OgreAssimp/OgreAssimpConverter
	../OgreAssimp/OgreAssimpConverter -uuid `echo '$<' | sha1sum | head -n1 | awk '{print $$1;}'` $<
	../scripts/add_metadata.py $< -d metadata.json -t $(TILES_ID) \
		-J $(dir $<)attributes.json -D 3DModel $< -D 3DMesh $@
	../scripts/add_metadata.py $< -d metadata.json -t $(TILES_ID) -D Material \
		`cat "$(dir $@)$(basename $(notdir $@)).material" | \
			grep '^material[[:space:]]*' | \
			sed -e 's|material[[:space:]]*||'`

%.iso.png: %_1.iso.png %_2.iso.png %_3.iso.png %_4.iso.png
	mkdir -p tmp
	@echo DIR: "'$(dir $@)'", FILE: "'$(basename $(basename $(notdir $@)))'", EXT: "'$(suffix $@)'"
	convert +append $+ $@
	optipng $@

$(TILES_ID).tsx: $(ISO_TILES) metadata.json
	../scripts/generate_simple_tsx.py -d metadata.json -i . -o . -n "$(TILES_ID)"

clean:
	@rm -fv `find . -maxdepth 1 -name "*.iso.png"`
	@rm -fv `find . -maxdepth 1 -name "*.mesh"`
	@rm -fv `find . -maxdepth 1 -name "*.mesh.xml"`
	@rm -fv `find . -maxdepth 1 -name "*.material"`
	@rm -fv `find . -maxdepth 1 -name "*.skeleton"`
	@rm -fv `find . -maxdepth 1 -name "*.skeleton.xml"`
	@rm -fv `find . -maxdepth 1 -name "*.tsx"`
