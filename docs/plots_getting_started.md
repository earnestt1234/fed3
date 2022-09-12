# Plotting with fed3

## Import `fed3.plot`

The plotting package within fed3, `fed3.plot` is not imported by default.  Make an explicit call to import it:


```python
import fed3
import fed3.plot as fplot
```

For the purposes of this documentation, matplotlib will be used to set the default figure size.


```python
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [7, 5]
plt.rcParams['figure.dpi'] = 100
```

## Example data

The following sections will make use of some example data, provided by the [`fed3.examples`](https://earnestt1234.github.io/fed3/fed3/examples/index.html) package:


```python
feds = fed3.load_examples('justin')
f = feds[0]
```

## Basic plotting

The following section will intoduce the basics of plotting with fed3.  

### The "Hello World" plot

The simplest plot is the [line plot](https://earnestt1234.github.io/fed3/fed3/plot/simple.html#fed3.plot.simple.line), which plots a variable of interest over time.  This demonstrates the syntax that applies to almost all plotting functions: pass the data to be plotted as the first argument (the FEDFrame(s)) followed by any options.  In this case, the `y` parameter specifies the variable to be plotted: 


```python
fplot.line(f, y='pellets')

plt.show()
```


    
![png](https://raw.githubusercontent.com/earnestt1234/fed3/main/img/plots_getting_started/plots_getting_started_9_0.png)
    


Many other `y` values can be specified - they link to the functions defined within [`fed3.metrics`](https://earnestt1234.github.io/fed3/fed3/metrics/index.html).  Call [`fed3.list_metrics()`](https://earnestt1234.github.io/fed3/fed3/index.html#fed3.list_metrics) to see all available options.

### Plotting multiple FEDs

Most plots are able to plot data from multiple FEDs, either as separate or aggregated curves.  The structure of the passed data determines this behavior:

- A single FEDFrame ([`fed3.core.fedframe.FEDFrame`](https://earnestt1234.github.io/fed3/fed3/core/fedframe.html#fed3.core.fedframe.FEDFrame)) specifies a single line to be plotted (as shown above)
- A `list` (or other 1D collection) of FEDFrames will plot each as separate curves
- A `dict` is used to aggregate data.  Within each dictionary, the key is the group label, and the value is the collection of FEDFrames belonging to that group.

#### List of FEDs

The following is an example of the second option - data for each FED are plotted as individual lines.


```python
fplot.line(feds, y='pellets')
plt.show()
```


    
![png](https://raw.githubusercontent.com/earnestt1234/fed3/main/img/plots_getting_started/plots_getting_started_12_0.png)
    


#### Grouping

To create a group average, pass a dictionary indicating group membership:


```python
groups = {'A' : feds[0:3], 'B' : feds[3:]}

fplot.line(groups, y='pellets')
plt.show()
```


    
![png](https://raw.githubusercontent.com/earnestt1234/fed3/main/img/plots_getting_started/plots_getting_started_14_0.png)
    


A few things have changed in the above plot:

- **There are two curves plotted only**; one for each member of the dictionary passed.  The curves correspond to the average pellet retrieval, and the shaded error bar correspond to the standard deviation.
- **The measure of pellet retrieval has changed from cumulative to absolute**.  I.e., the y-axis corresponds to the number of pellets retrieved (on average) within each temporal bin (by default, 1 hour).  This is the default behavior of the `y='pellets'` metric ([see here](https://earnestt1234.github.io/fed3/fed3/metrics/core.html#fed3.metrics.core.pellets)).

There are options to tweak the behavior for grouping.  `agg` sets the aggregation method for the grouped data, and `var` sets the measure of error.  Furthermore, the `bins` parameter sets the resolution of temporal averaging:


```python
fplot.line(groups, y='pellets', bins='4H', agg='median')
plt.show()
```


    
![png](https://raw.githubusercontent.com/earnestt1234/fed3/main/img/plots_getting_started/plots_getting_started_16_0.png)
    


## Integrating with matplotlib

Plotting with fed3 is all implemented through calls to [matplotlib](https://matplotlib.org/).  Thus, you can make use of typical matplotlib routines to customize your plots:


```python
import matplotlib.pyplot as plt

fplot.scatter(f, y='rt')

plt.title('Retrieval Time for FED1')
plt.xlabel('Custom X')
plt.ylabel('Custom Y')
plt.axhline(20, color='red', linestyle='dashed')

plt.show()
```


    
![png](https://raw.githubusercontent.com/earnestt1234/fed3/main/img/plots_getting_started/plots_getting_started_18_0.png)
    


Most plots can also be directed to a given [matplotlib axis](https://matplotlib.org/stable/api/axes_api.html), using the `ax` argument:


```python
# create layout
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

# plot
fplot.line(f, y='pellets', ax=ax1)
fplot.ipi(f, ax=ax2)
plt.show()
```


    
![png](https://raw.githubusercontent.com/earnestt1234/fed3/main/img/plots_getting_started/plots_getting_started_20_0.png)
    


This can also be used to plot different metrics from one FED on the same axis.  Note that the `shadedark` option will be specified for both calls if not otherwise specified:


```python
# create figure and axis
fig = plt.figure()
ax = plt.subplot()

fplot.line(f, y='left_pokes', ax=ax, shadedark=False, label='Left')
fplot.line(f, y='right_pokes', ax=ax, label='Right')
plt.ylabel('Pokes')
plt.show()
```


    
![png](https://raw.githubusercontent.com/earnestt1234/fed3/main/img/plots_getting_started/plots_getting_started_22_0.png)
    

