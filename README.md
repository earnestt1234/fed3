# fed3

fed3 is a Python package for working with [FED3](https://github.com/KravitzLabDevices/FED3) data.  fed3 aims to lower the barrier for producing analyses and visualizations of behavioral data produced from FED3 devices.  Data manipulation is largely based on [pandas](https://pandas.pydata.org/), while plotting is managed through [matplotlib](https://matplotlib.org/stable/index.html) (and a little bit of [seaborn](https://seaborn.pydata.org/)).

## Development

fed3 does not have a working full release yet.  These are the immediate goals for fed3 development:

1. Documentation.  Currently there are no function docstrings or examples showing fed3 usage.

2. Test cases.  Make a test suite to help make fed3 more shareable.

3. Finishing FED3Viz porting.  There are still several plots from FED3Viz that have not been ported to fed3.  Namely:

   - Daynight bar plots
   - Daynight interpellet interval plots
   - Heatmap chronograms
   - Meal size histograms
   - Breakpoint plots
   - Poke bias plots
   - Poke time plots

   The "Summary Stats" feature from FED3Viz has also not been added.

4. Expanding functionality, pending community input.

## Installation

If you would like to test fed3 in its current state, you can install it from the command line:
```
git clone https://github.com/earnestt1234/fed3
cd fed3
pip install .
```

