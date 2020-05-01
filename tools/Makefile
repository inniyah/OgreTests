OBJ_SOURCES = $(shell find 3d_models -name "*.obj")
ISO_TILES = $(OBJ_SOURCES:.obj=_1.iso.png) $(OBJ_SOURCES:.obj=_2.iso.png) $(OBJ_SOURCES:.obj=_3.iso.png) $(OBJ_SOURCES:.obj=_4.iso.png) $(OBJ_SOURCES:.obj=.mesh)

all: $(ISO_TILES) tiled/tiles.tsx

TinyRenderer/TinyRenderer:
	$(MAKE) -C TinyRenderer

OgreAssimp/OgreAssimpConverter:
	$(MAKE) -C OgreAssimp

%_1.iso.png: %.obj TinyRenderer/TinyRenderer
	TinyRenderer/TinyRenderer -w $< $@
	optipng $@
	scripts/add_metadata.py $< -d 3d_models/info.json -t tile -D IsoTile1 $@

%_2.iso.png: %.obj TinyRenderer/TinyRenderer
	TinyRenderer/TinyRenderer -w $< $@ -a 90
	optipng $@
	scripts/add_metadata.py $< -d 3d_models/info.json -t tile -D IsoTile2 $@

%_3.iso.png: %.obj TinyRenderer/TinyRenderer
	TinyRenderer/TinyRenderer -w $< $@ -a 180
	optipng $@
	scripts/add_metadata.py $< -d 3d_models/info.json -t tile -D IsoTile3 $@

%_4.iso.png: %.obj TinyRenderer/TinyRenderer
	TinyRenderer/TinyRenderer -w $< $@ -a 270
	optipng $@
	scripts/add_metadata.py $< -d 3d_models/info.json -t tile -D IsoTile4 $@

%.mesh: %.obj OgreAssimp/OgreAssimpConverter
	OgreAssimp/OgreAssimpConverter $<
	scripts/add_metadata.py $< -d 3d_models/info.json -t tile -D 3DModel $< -D 3DMesh $@

%.iso.png: %_1.iso.png %_2.iso.png %_3.iso.png %_4.iso.png
	mkdir -p tmp
	@echo DIR: "'$(dir $@)'", FILE: "'$(basename $(basename $(notdir $@)))'", EXT: "'$(suffix $@)'"
	convert +append $+ $@
	optipng $@

tiled/tiles.tsx: 3d_models/info.json $(ISO_TILES)
	scripts/tsx_generator.py -d 3d_models/info.json -o $@

clean:
	@rm -rf tmp/
	@rm -fv `find 3d_models -name "*.iso.png"`
	@rm -fv `find 3d_models -name "*.mesh"`
	@rm -fv `find 3d_models -name "*.mesh.xml"`
	@rm -fv `find 3d_models -name "*.material"`
	@rm -fv `find 3d_models -name "*.skeleton"`
	@rm -fv `find 3d_models -name "*.skeleton.xml"`
	@rm -fv `find tiled -name "*.tsx"`
	@rm -rf *.log
