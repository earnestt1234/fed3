# Plotting with fed3

## Importing

The plotting package within fed3, `fed3.plot` is not imported by default.  Make an explicit call to import it:


```python
import fed3
import fed3.plot as fplot
```

For the purposes of this documentation, matplotlib will be used to set the default figure size.


```python
import matplotlib
matplotlib.rcParams['figure.figsize'] = [7, 5]
matplotlib.rcParams['figure.dpi'] = 100
```

## Example data

The following sections will make use of some example data, provided by the [`fed3.examples`](https://earnestt1234.github.io/fed3/fed3/examples/index.html) package:


```python
fedlist = fed3.load_examples('justin')
f = fedlist[0]
```

## Basic plotting

### Line Plots

The following section will intoduce the basics of plotting with fed3.  The simplest plot is the [line plot](https://earnestt1234.github.io/fed3/fed3/plot/simple.html#fed3.plot.simple.line), which plots a variable of interest over time.  Pass the FEDFrame to be plotted, and the desired variable:


```python
fig = fplot.line(f, y='pellets')
```


    
![png](https://raw.githubusercontent.com/earnestt1234/fed3/plots_docs/img/plots_getting_started/plots_getting_started_8_0.png)
    


Many other `y` values can be specified - they link to the functions defined within [`fed3.metrics`](https://earnestt1234.github.io/fed3/fed3/metrics/index.html) (call [`fed3.list_metrics()`](https://earnestt1234.github.io/fed3/fed3/index.html#fed3.list_metrics) to see all available options).


```python
fig = fplot.line(f, y='left_pokes')
```


    
![png](https://raw.githubusercontent.com/earnestt1234/fed3/plots_docs/img/plots_getting_started/plots_getting_started_10_0.png)
    



```python
fig = fplot.line(f, y='battery')
```


    
![png](https://raw.githubusercontent.com/earnestt1234/fed3/plots_docs/img/plots_getting_started/plots_getting_started_11_0.png)
    



```python
fig = fplot.line(f, y='rt') # retrieval time
```


    
![png](https://raw.githubusercontent.com/earnestt1234/fed3/plots_docs/img/plots_getting_started/plots_getting_started_12_0.png)
    

