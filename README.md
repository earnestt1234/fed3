# fed3

fed3 is a Python package for working with [FED3](https://github.com/KravitzLabDevices/FED3) data.  fed3 aims to simplify the creation of analyses and visualizations of behavioral data produced from FED3 devices.  Data manipulation is largely based on [pandas](https://pandas.pydata.org/), while plotting is managed through [matplotlib](https://matplotlib.org/stable/index.html) (and a little bit of [seaborn](https://seaborn.pydata.org/)).

## Development

fed3 is somewhat functional, but requires some more development.  These are the immediate goals:

### Documentation

There is a partially complete [API documentation here](https://earnestt1234.github.io/fed3/fed3/index.html).  Many functions are still missing docstrings.  Additionally, I want to add more getting started/example code (for basics of plotting, [see here](https://earnestt1234.github.io/fed3/fed3/plot/index.html) for some basics).

### Testing

There currently is not a test suite for fed3, and should be added.

### Porting FED3Viz

There are still several plots from FED3Viz that have not been ported to fed3.  Namely:

- Daynight bar plots
- Daynight interpellet interval plots
- Heatmap chronograms
- Meal size histograms
- Breakpoint plots
- Poke bias plots
- Poke time plots

The "Summary Stats" feature from FED3Viz has also not been added.

### New Features

I hope to add more things which were not possible in FED3VIZ - especially new types of graphs.  This somewhat pending on usage and feature requests.

## Installation

If you would like to test fed3 in its current state, you can install it from the command line:
```
git clone https://github.com/earnestt1234/fed3
cd fed3
pip install .
```

## fed3 vs FED3VIZ

Many of the functions and visualizations in fed3 are taken from [FED3VIZ](https://github.com/earnestt1234/FED3_Viz), a previously-developed GUI for working with FED3 data.  There is currently incomplete overlap between these two softwares; i.e. some stuff from FED3VIZ can't be done with fed3, and some new things in fed3 can't be done with FED3VIZ.  An immediate goal of the fed3 package is to address the first point by porting all the remaining FED3VIZ functions to fed3 (see the Development section above).

I would like to also have FED3VIZ be expanded to include new operations being developed in this repository.  However, the implementation of FED3VIZ is somewhat of a mess, due to a lot of learn-on-the-job software code :sweat_smile:.  And unfortunately, updating that program requires far more effort than updating this package.

Instead, I hope to reimplement FED3VIZ using the fed3 package (and some better coding practices).  Ideally, some of the interface will be automatically generated based on functions available in fed3.  This will most likely require a rewrite of FED3Viz, rather than an update.  Plus, the fed3 package is still very immature, and needs much more development and testing.  Therefore, this reimplementation of FED3VIZ is probably a long way off.
