#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import datetime
import argparse

from filelock import FileLock

def generate_obj_info(obj_filename):
    obj_info = {}
    return obj_info

def get_new_seq_id(obj_filename, obj_type, seq_info):
    try:
        curr_seq_id = seq_info[obj_type]
    except KeyError:
        curr_seq_id = 1
    seq_info[obj_type] = curr_seq_id + 1
    return curr_seq_id

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def get_obj_info(json_db_filename, obj_filename, obj_type):
    with FileLock(f"{json_db_filename}.lock"):
        touch(json_db_filename) # make sure that the file exists

        with open(json_db_filename, "r+") as opened_file:
            current_json = opened_file.read()
            if current_json == "":
                current_json = {}
            else:
                current_json = json.loads(current_json)

            try:
                seq_info = current_json[':sequences']
            except KeyError:
                seq_info = { }
                current_json[':sequences'] = seq_info

            try:
                db_entry = current_json[obj_filename]
            except KeyError:
                db_entry = generate_obj_info(obj_filename)
                db_entry[":change_id"] = 0
                db_entry[":seq_id"] = get_new_seq_id(obj_filename, obj_type, seq_info)
                current_json[obj_filename] = db_entry

            now = datetime.datetime.utcnow()
            current_json[':timestamp'] = f"{now.strftime('%Y-%m-%d (%H:%M:%S) UTC')}"

            opened_file.seek(0)
            opened_file.truncate(0)
            json.dump(current_json, opened_file, indent=2, sort_keys=True)

    return db_entry

def update_obj_info(json_db_filename, obj_filename, db_entry):
    with FileLock(f"{json_db_filename}.lock"):
        touch(json_db_filename) # make sure that the file exists

        with open(json_db_filename, "r+") as opened_file:
            current_json = opened_file.read()
            if current_json == "":
                current_json = {}
            else:
                current_json = json.loads(current_json)

            try:
                old_db_entry = current_json[obj_filename]
                if (old_db_entry[":change_id"] == db_entry[":change_id"]):
                    db_entry[":change_id"] += 1
                else:
                    print(f"Error, data mismatch for {obj_filename} in {json_db_filename}")
                    return False
            except KeyError:
                pass

            now = datetime.datetime.utcnow()
            db_entry[':timestamp'] = f"{now.strftime('%Y-%m-%d (%H:%M:%S) UTC')}"
            current_json[':timestamp'] = f"{now.strftime('%Y-%m-%d (%H:%M:%S) UTC')}"

            current_json[obj_filename] = db_entry

            opened_file.seek(0)
            opened_file.truncate(0)
            json.dump(current_json, opened_file, indent=2, sort_keys=True)

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process obj 3d models")
    parser.add_argument("objfile", help="path to an .obj")
    parser.add_argument("-d", "--db", help="path to the jason db", default=None)
    parser.add_argument("-t", "--type", help="type of file", default=None)
    parser.add_argument("-D", nargs=2, action='append')
    args = parser.parse_args()

    if not args.db or not args.objfile or not args.type:
        print("Wrong arguments")
        sys.exit(-1)

    obj_info = get_obj_info(args.db, args.objfile, args.type)

    if args.D:
        for (key, value) in args.D:
            obj_info[f"@{key}"] = value

    update_obj_info(args.db, args.objfile, obj_info)
