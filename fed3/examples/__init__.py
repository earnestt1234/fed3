# -*- coding: utf-8 -*-
'''This package provides example data for fed3.  The package comes
bundled with some CSV files of FED3 data.  These can be loaded via
fed3, returning FEDFrames.

fed3 uses this package to create reproducible examples for the documentation.

[Most data & descriptions are taken directly from the FED3 GitHub repo](https://github.com/KravitzLabDevices/FED3/tree/main/ExampleData).

Data included in the package are all intended to be taken from real fed3
experiments.  If you have data you would like to contribute as an example,
please raise an issue on GitHub.

Datasets
-----

### Closed Economy, Progressive Ratio 1 (`closed_economy_pr1`)
These are example FED3 data files collected from mice performing an PR1 task in
which the number of required pokes increments each time they earn a pellet.
For instance, the first pellet requires 1 poke, the second 2 pokes, etc.
The trick is that if a mouse does not earn a pellet for 30 minutes the
requirement resets.  This allows mice to run on this task for days,
without the requirement becoming too challenging for them to obtain their
daily food requirements.

### Justin's Data (`justin`)
Seven FEDs with data collected over a long-term experiment (10 days).
These data represent FED3 data from multiple recordings, already concatenated.
Data were collected in "ProRat2" mode.  The data show pellet
retrieval in response to an active left poke.

### Fixed Ratio 1 (`fr1`)
These are example FED3 data files collected from mice performing an FR1 task for 12-24 hours

### Fixed Ratio 1 With Delay (`fr1_4s_delay`)
These are example FED3 data files collected from mice performing an FR1 task
with a 4s delay between nosepoke and pellet delivery.  This task is useful for
synchronizing with brain recordings, to separate the nosepoke from the pellet
retrievals to analyze brain activity around each.

### Dual Fixed Ratio 1 (`fr1_dual`)
These are example FED3 data files collected from mice performing an FR1 task in
which both right or left pokes are rewarded with a pellet.

### Optogenetic Self Stim (`optogenetic_self_stim`)
These are example FED3 data files collected from mice performing an FR1 task
for optogenetic stimulation. Trials were 1-2 hours in length, this is all from
the same mouse trained across 6 sessions.  The mouse acquires a preference for
stimulation on the 4th session.

### Reversal Task (`reversal_task`)
These are example FED3 data files collected from mice performing a reversal
learning task.  The rewarded nosepoke switches each time the mice earn 40
pellets.  For instance, the program starts with the Left poke delivering a
pellet, but after the mouse earns 40 pellets it switches to the Right poke,
after 80 pellets back to the Left poke, etc. Task was run for 4-5 days,
resulting in several hundred earned pellets

### Punished Reversal Task (`reversal_task_punished`)
These are example FED3 data files collected from mice performing a reversal
learning task with a punishment.  The punishment is that if an incorrect poke
is made, the FED3 will enter a timeout for 30 seconds. The rewarded nosepoke
switches each time the mice earn 40 pellets.  For instance, the program starts
with the Left poke delivering a pellet, but after the mouse earns 40 pellets it
switches to the Right poke, after 80 pellets back to the Left poke, etc. Task
was run for 4-5 days, resulting in several hundred earned pellets

'''


__all__ = ['list_examples', 'load_examples']

import os
import sys
import warnings

from fed3.core.fedfuncs import load

# module variables
DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
DATA = {}

def list_examples():
    '''
    List all the available example data sets - specifically the string
    keys which can be provided to `load_examples()`.

    Returns
    -------
    list
        All avaiable keys.
    '''

    examples = []
    for folder in sorted(os.listdir(DATADIR)):
        fullfolder = os.path.join(DATADIR, folder)
        if not os.path.isdir(fullfolder): continue;
        examples.append(folder)

    return examples


def load_examples(key, verbose=False):
    '''
    Load the example data linked to a given key.

    Parameters
    ----------
    key : str
        Example to load.
    verbose : bool
        Print status while loading

    Raises
    ------
    KeyError
        Unrecognized key.

    Returns
    -------
    list
        FED3 example data, as a list of FEDFrame objects.

    '''
    vprint = print if verbose else lambda *args, **kwargs: None


    example_path = os.path.join(DATADIR, key)
    examples = []
    vprint()
    vprint(f'Loading from data directory: {DATADIR}')
    vprint()
    vprint(f'Example folder: {example_path}')

    vprint()
    for file in sorted(os.listdir(example_path)):
        name, ext = os.path.splitext(file)
        if ext.lower() not in ['.csv', '.xlsx']: continue;
        vprint(f' - {file}...')
        fullfile = os.path.join(example_path, file)
        examples.append(load(fullfile, deduplicate_index='keep_first'))

    return examples

# def _build_examples():
#     '''Load all the FED3 example data.  To be called on start up.'''
#     if not os.path.isdir(DATADIR):
#         warnings.warn("Unable to find fed3 example data directory; unable "
#                       "to load example data.", RuntimeWarning)
#         sys.exit()

#     # main loop for loading data
#     for folder in sorted(os.listdir(DATADIR)):

#         fullfolder = os.path.join(DATADIR, folder)
#         if not os.path.isdir(fullfolder): continue;
#         l = []

#         for file in sorted(os.listdir(fullfolder)):

#             name, ext = os.path.splitext(file)
#             if ext not in ['.csv', '.xlsx']: continue;
#             fullfile = os.path.join(fullfolder, file)
#             l.append(load(fullfile, deduplicate_index='keep_first'))

#         DATA[folder] = l

# _build_examples()