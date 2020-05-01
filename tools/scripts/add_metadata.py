#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

from data_db import get_obj_info, update_obj_info

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process obj 3d models")
    parser.add_argument("objfile", help="path to an .obj")
    parser.add_argument("-d", "--db", help="path to the json db", default=None)
    parser.add_argument("-t", "--type", help="type of file", default=None)
    parser.add_argument("-D", nargs=2, action='append')
    args = parser.parse_args()

    if not args.db or not args.objfile:
        print("Wrong arguments")
        sys.exit(-1)

    obj_info = get_obj_info(args.db, args.objfile, args.type)

    if args.D:
        for (key, value) in args.D:
            obj_info[f"@{key}"] = value

    update_obj_info(args.db, args.objfile, obj_info)
