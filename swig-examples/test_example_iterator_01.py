#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import example_iterator_01 as example
col = example.Collection()

el = example.Element()
el.set(5)
col.add(el)

el = example.Element()
el.set(6)
col.add(el)

for e in col:
    print(e.get())
