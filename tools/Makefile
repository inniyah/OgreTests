OBJ_SOURCES = $(shell find 3d_models -name "*.obj")
ISO_TILES = \
	$(OBJ_SOURCES:.obj=_1.iso.png) \
	$(OBJ_SOURCES:.obj=_2.iso.png) \
	$(OBJ_SOURCES:.obj=_3.iso.png) \
	$(OBJ_SOURCES:.obj=_4.iso.png) \
	$(OBJ_SOURCES:.obj=.mesh)

FLOOR_PNG_SOURCES = $(shell find floors -name "*.png" | grep -v ".iso.png$$")
FLOOR_JPG_SOURCES = $(shell find floors -name "*.jpg")
FLOOR_ISO_OBJS = $(FLOOR_PNG_SOURCES:.png=.obj) $(FLOOR_JPG_SOURCES:.jpg=.obj)
FLOOR_ISO_TILES = \
	$(FLOOR_ISO_OBJS:.obj=_1.iso.png) \
	$(FLOOR_ISO_OBJS:.obj=_2.iso.png) \
	$(FLOOR_ISO_OBJS:.obj=_3.iso.png) \
	$(FLOOR_ISO_OBJS:.obj=_4.iso.png) \
	$(FLOOR_ISO_OBJS:.obj=.mesh)

CEILING_PNG_SOURCES = $(shell find ceilings -name "*.png" | grep -v ".iso.png$$")
CEILING_JPG_SOURCES = $(shell find ceilings -name "*.jpg")
CEILING_ISO_OBJS = $(CEILING_PNG_SOURCES:.png=.obj) $(CEILING_JPG_SOURCES:.jpg=.obj)
CEILING_ISO_TILES = \
	$(CEILING_ISO_OBJS:.obj=_1.iso.png) \
	$(CEILING_ISO_OBJS:.obj=_2.iso.png) \
	$(CEILING_ISO_OBJS:.obj=_3.iso.png) \
	$(CEILING_ISO_OBJS:.obj=_4.iso.png) \
	$(CEILING_ISO_OBJS:.obj=.mesh)

all: tiles floors ceilings tiled/models.tsx

tiles: $(ISO_TILES)

floors: $(FLOOR_ISO_OBJS) $(FLOOR_ISO_TILES)
	echo $(FLOOR_ISO_OBJS)

ceilings: $(CEILING_ISO_OBJS) $(CEILING_ISO_TILES)
	echo $(CEILING_ISO_OBJS)

floors/%.obj: floors/%.png
	cat floors/floor.mtl.in \
		| sed -e 's|$${MATERIAL_TEXTURE}|$(<:floors/%=%)|' \
		| sed -e 's|$${MATERIAL_NAME}|Material_$(shell echo "$<" | md5sum)|' \
		> $(basename $@).mtl
	cat floors/floor.obj.in \
		| sed -e 's|$${MATERIAL_FILE}|$(basename $(<:floors/%=%)).mtl|' \
		| sed -e 's|$${MATERIAL_NAME}|Material_$(shell echo "$<" | md5sum)|' \
		> $@
	scripts/add_metadata.py $@ -d metadata/info.json -t $(firstword $(subst /, ,$<)) -D Texture $<

floors/%.obj: floors/%.jpg
	cat floors/floor.mtl.in \
		| sed -e 's|$${MATERIAL_TEXTURE}|$(<:floors/%=%)|' \
		| sed -e 's|$${MATERIAL_NAME}|Material_$(shell echo "$<" | md5sum)|' \
		> $(basename $@).mtl
	cat floors/floor.obj.in \
		| sed -e 's|$${MATERIAL_FILE}|$(basename $(<:floors/%=%)).mtl|' \
		| sed -e 's|$${MATERIAL_NAME}|Material_$(shell echo "$<" | md5sum)|' \
		> $@
	scripts/add_metadata.py $@ -d metadata/info.json -t $(firstword $(subst /, ,$<)) -D Texture $<

ceilings/%.obj: ceilings/%.png
	cat ceilings/ceiling.mtl.in \
		| sed -e 's|$${MATERIAL_TEXTURE}|$(<:ceilings/%=%)|' \
		| sed -e 's|$${MATERIAL_NAME}|Material_$(shell echo "$<" | md5sum)|' \
		> $(basename $@).mtl
	cat ceilings/ceiling.obj.in \
		| sed -e 's|$${MATERIAL_FILE}|$(basename $(<:ceilings/%=%)).mtl|' \
		| sed -e 's|$${MATERIAL_NAME}|Material_$(shell echo "$<" | md5sum)|' \
		> $@
	scripts/add_metadata.py $@ -d metadata/info.json -t $(firstword $(subst /, ,$<)) -D Texture $<

ceilings/%.obj: ceilings/%.jpg
	cat ceilings/ceiling.mtl.in \
		| sed -e 's|$${MATERIAL_TEXTURE}|$(<:ceilings/%=%)|' \
		| sed -e 's|$${MATERIAL_NAME}|Material_$(shell echo "$<" | md5sum)|' \
		> $(basename $@).mtl
	cat ceilings/ceiling.obj.in \
		| sed -e 's|$${MATERIAL_FILE}|$(basename $(<:ceilings/%=%)).mtl|' \
		| sed -e 's|$${MATERIAL_NAME}|Material_$(shell echo "$<" | md5sum)|' \
		> $@
	scripts/add_metadata.py $@ -d metadata/info.json -t $(firstword $(subst /, ,$<)) -D Texture $<

TinyRenderer/TinyRenderer:
	$(MAKE) -C TinyRenderer

OgreAssimp/OgreAssimpConverter:
	$(MAKE) -C OgreAssimp

%_1.iso.png: %.obj TinyRenderer/TinyRenderer
	TinyRenderer/TinyRenderer -w $< $@
	optipng $@
	scripts/add_metadata.py $< -d metadata/info.json -t $(firstword $(subst /, ,$<)) -D IsoTile1 $@

%_2.iso.png: %.obj TinyRenderer/TinyRenderer
	TinyRenderer/TinyRenderer -w $< $@ -a 90
	optipng $@
	scripts/add_metadata.py $< -d metadata/info.json -t $(firstword $(subst /, ,$<)) -D IsoTile2 $@

%_3.iso.png: %.obj TinyRenderer/TinyRenderer
	TinyRenderer/TinyRenderer -w $< $@ -a 180
	optipng $@
	scripts/add_metadata.py $< -d metadata/info.json -t $(firstword $(subst /, ,$<)) -D IsoTile3 $@

%_4.iso.png: %.obj TinyRenderer/TinyRenderer
	TinyRenderer/TinyRenderer -w $< $@ -a 270
	optipng $@
	scripts/add_metadata.py $< -d metadata/info.json -t $(firstword $(subst /, ,$<)) -D IsoTile4 $@

%.mesh: %.obj OgreAssimp/OgreAssimpConverter
	OgreAssimp/OgreAssimpConverter -uuid `echo '$<' | sha1sum | head -n1 | awk '{print $$1;}'` $<
	scripts/add_metadata.py $< -d metadata/info.json -t $(firstword $(subst /, ,$<)) \
		-J $(dir $<)attributes.json -D 3DModel $< -D 3DMesh $@
	scripts/add_metadata.py $< -d metadata/info.json -t $(firstword $(subst /, ,$<)) -D Material \
		`cat "$(dir $@)$(basename $(notdir $@)).material" | \
			grep '^material[[:space:]]*' | \
			sed -e 's|material[[:space:]]*||'`

%.iso.png: %_1.iso.png %_2.iso.png %_3.iso.png %_4.iso.png
	mkdir -p tmp
	@echo DIR: "'$(dir $@)'", FILE: "'$(basename $(basename $(notdir $@)))'", EXT: "'$(suffix $@)'"
	convert +append $+ $@
	optipng $@

tiled/models.tsx tiled/floors.tsx tiled/ceilings.tsx: metadata/info.json tiles floors ceilings
	scripts/tsx_generator.py -d metadata/info.json -o tiled/

clean:
	@rm -rf tmp/
	@rm -rf *.log
	@rm -fv `find . -name "*.bak"`
	@rm -fv `find . -name "*~"`

	@rm -fv `find 3d_models -name "*.iso.png"`
	@rm -fv `find 3d_models -name "*.mesh"`
	@rm -fv `find 3d_models -name "*.mesh.xml"`
	@rm -fv `find 3d_models -name "*.material"`
	@rm -fv `find 3d_models -name "*.skeleton"`
	@rm -fv `find 3d_models -name "*.skeleton.xml"`

	@rm -fv `find tiled -name "*.tsx"`

	@rm -fv `find floors -name "*.obj"`
	@rm -fv `find floors -name "*.mtl"`
	@rm -fv `find floors -name "*.iso.png"`
	@rm -fv `find floors -name "*.mesh"`
	@rm -fv `find floors -name "*.mesh.xml"`
	@rm -fv `find floors -name "*.material"`
	@rm -fv `find floors -name "*.skeleton"`
	@rm -fv `find floors -name "*.skeleton.xml"`

	@rm -fv `find ceilings -name "*.obj"`
	@rm -fv `find ceilings -name "*.mtl"`
	@rm -fv `find ceilings -name "*.iso.png"`
	@rm -fv `find ceilings -name "*.mesh"`
	@rm -fv `find ceilings -name "*.mesh.xml"`
	@rm -fv `find ceilings -name "*.material"`
	@rm -fv `find ceilings -name "*.skeleton"`
	@rm -fv `find ceilings -name "*.skeleton.xml"`

cleanall: clean
	$(MAKE) -C OgreAssimp cleanall
	$(MAKE) -C TinyRenderer cleanall
