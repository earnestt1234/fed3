# -*- coding: utf-8 -*-

#imports for package namespace

import os
import sys
import warnings

from fed3.core.fedfuncs import load

# public function for accessing data

def load_examples(key):

    try:
        return DATA[key]
    except KeyError:
        raise KeyError(f"No matching key '{key}'; options are: "
                       f"{list(DATA.keys())}")

# find the data directory
DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
DATA = {}

if not os.path.isdir(DATADIR):
    warnings.warn("Unable to find fed3 example data directory; unable "
                  "to load example data.", RuntimeWarning)
    sys.exit()

# main loop for loading data
for folder in os.listdir(DATADIR):

    fullfolder = os.path.join(DATADIR, folder)
    if not os.path.isdir(fullfolder): continue;
    l = []

    for file in os.listdir(fullfolder):

        name, ext = os.path.splitext(file)
        if ext not in ['.csv', '.xlsx']: continue;
        fullfile = os.path.join(fullfolder, file)
        l.append(load(fullfile, deduplicate_index='keep_first'))

    DATA[folder] = l



