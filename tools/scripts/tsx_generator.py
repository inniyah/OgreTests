#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

from data_db import get_obj_info, update_obj_info, get_all_info
from obj_loader import ObjLoader

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process obj 3d models")
    parser.add_argument("-d", "--db", help="path to the json db", default=None)
    parser.add_argument("-o", "--output", help="output file", default=None)
    args = parser.parse_args()

    if not args.db or not args.output:
        print("Wrong arguments")
        sys.exit(-1)

    with open(args.output, 'w') as file_output:

        all_info = get_all_info(args.db)
        tiles_list = all_info[":type_lists"]["tile"]

        tiles_per_object = 4
        tile_id_multiplier = 5
        tile_id_base = 1

        num_of_objects = len(tiles_list)

        print(f'<?xml version="1.0" encoding="UTF-8"?>', file=file_output)
        print(f'<tileset version="1.2" tiledversion="1.3.3" name="tiles" tilewidth="128" tileheight="224" tilecount="{num_of_objects}" columns="0">', file=file_output)
        print(f' <grid orientation="orthogonal" width="1" height="1"/>', file=file_output)

        for tile_id in sorted(tiles_list.keys()):
            obj_filename = tiles_list[tile_id]
            tile_id_num = int(tile_id)
            tile_info = all_info[obj_filename]

            for (tile_id_inc, json_label, rot_angle) in [
                (0, "@IsoTile1", 0),
                (1, "@IsoTile2", 90),
                (2, "@IsoTile3", 180),
                (3, "@IsoTile4", 270),
            ]:

                print(f' <tile id="{tile_id_base + tile_id_multiplier * tile_id_num + tile_id_inc}">', file=file_output)
                print(f'  <properties>', file=file_output)
                print(f'   <property name="3DModel" value="{tile_info["@3DModel"]}"/>', file=file_output)
                print(f'   <property name="3DMesh" value="{tile_info["@3DMesh"]}"/>', file=file_output)
                print(f'   <property name="RotAngle" value="{rot_angle}"/>', file=file_output)
                print(f'  </properties>', file=file_output)
                print(f'  <image source="../{tile_info[json_label]}" width="128" height="224"/>', file=file_output)
                print(f' </tile>', file=file_output)

        print(f'</tileset>', file=file_output)
