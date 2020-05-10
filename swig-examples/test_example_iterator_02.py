#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import example_iterator_02 as example
col = example.Collection()

print("Adding first element")

el = example.Element()
el.set(4)
col.add(el)
del el

print("Adding second element")
el = example.Element()
el.set(6)
col.add(el)
del el

print("Create iterator")
for e in col:
    print(e.get())

print("The end")
