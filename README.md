# Alpha Shape Toolbox

[![PyPI version](https://img.shields.io/pypi/v/alphashape.svg)](https://pypi.python.org/pypi/alphashape/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/alphashape.svg)](https://pypi.python.org/pypi/alphashape/)
[![Travis](https://api.travis-ci.org/bellockk/alphashape.svg?branch=master)](https://travis-ci.org/bellockk/alphashape/)
[![CodeCov](https://codecov.io/gh/bellockk/alphashape/branch/master/graph/badge.svg)](https://codecov.io/gh/bellockk/alphashape)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/bellockk/alphashape/master)
[![Documentation Status](https://readthedocs.org/projects/alphashape/badge/?version=latest)](http://alphashape.readthedocs.io/?badge=latest)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

Toolbox for generating alpha shapes.

Alpha shapes are often used to generalize bounding polygons containing sets of points.  The alpha parameter is defined as the value `a`, such that an edge of a  disk of radius 1/`a` can be drawn between any two edge members of a set of points and still contain all the points. The convex hull, a shape resembling what you would see if you wrapped a rubber band around pegs at all the data points, is an alpha shape where the alpha parameter is equal to zero.  In this toolbox we will be generating alpha complexes, which are closely related to alpha shapes, but which consist of straight lines between the edge points instead of arcs of circles.

https://en.wikipedia.org/wiki/Alpha_shape

https://en.wikipedia.org/wiki/Convex_hull

Creating alpha shapes around sets of points usually requires a visually interactive step where the alpha parameter for a concave hull is determined by iterating over or bisecting values to approach a best fit.  The alpha shape toolbox will provide workflows to shorten the development loop on this manual process, or to bypass it completely by solving for an alpha shape with particular characteristics.  A python API will be provided to aid in the scripted generation of alpha shapes.  A console application will also be provided as an example usage of the alpha shape toolbox, and to facilitate generation of alpha shapes from the command line.  In addition to the utility of being able to quickly iterate on alpha parameters to generate concave hulls, the framework of this tool set will provide a template for generating GIS tool sets accessible from python, the console, or graphical user interfaces without the licensing restrictions of proprietary tool sets and without having a python installation for the console and user interface.

* Free software: MIT license
* Documentation: https://alphashape.readthedocs.io.

## Features

## Import Dependencies


```python
import sys
from descartes import PolygonPatch
import matplotlib.pyplot as plt
sys.path.insert(0, r'C:\local\bellockk\alphashape')
import alphashape
```

## Define a set of points


```python
points = [(0., 0.), (0., 1.), (1., 1.), (1., 0.),
          (0.5, 0.25), (0.5, 0.75), (0.25, 0.5), (0.75, 0.5)]
```

## Plotting the input points


```python
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_5_0.png)


## Generate an Alpha Shape ($\alpha=0.$) (Convex Hull)
Every convex hull is an alpha shape, but not every alpha shape is a convex hull.  When the `alphashape` function is called with an alpha parameter of 0, a convex hull will always be returned.

### Create the alpha shape


```python
alpha_shape = alphashape.alphashape(points, 0.)
```

### Plotting the alpha shape over the input data


```python
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_10_0.png)


## Generate an Alpha Shape ($\alpha=2.0$) (Concave Hull)
As we increase the alpha parameter value, the bounding shape will begin to fit the sample data with a more tightly fitting bounding box.

### Create the alpha shape


```python
alpha_shape = alphashape.alphashape(points, 2.0)
```

### Plotting the alpha shape over the input data


```python
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_15_0.png)


## Generate an Alpha Shape ($\alpha=3.5$)
If you go too high on the alpha parameter, you will start to lose points from the original data set.

### Create the alpha shape


```python
alpha_shape = alphashape.alphashape(points, 3.5)
```

### Plotting the alpha shape over the input data


```python
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_20_0.png)


## Generate an Alpha Shape ($\alpha=5.0$)
If you go too far, you will lose everything.


```python
alpha_shape = alphashape.alphashape(points, 5.0)
print(alpha_shape)
```

    GEOMETRYCOLLECTION EMPTY
    

## Generate an Alpha Shape by Solving for an Optimal Alpha Value
The alpha parameter can be solved for if it is not provided as an argument, but with large datasets this can take a long time to calculate.

### Create the alpha shape


```python
alpha_shape = alphashape.alphashape(points)
```

### Plotting the alpha shape over the input data


```python
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_27_0.png)

# Alpha Shapes with GeoPandas

## Sample Data

The data used in this notebook can be obtained from the Alaska Department of Transportation and Public Facilities website at the link below.  It consists of a point collection for each of the public airports in Alaska.

[http://www.dot.alaska.gov/stwdplng/mapping/shapefiles.shtml](http://www.dot.alaska.gov/stwdplng/mapping/shapefiles.shtml)

## Load the Shapefile


```python
import geopandas
SCRIPT_PATH = os.getcwd()
data = os.path.join(SCRIPT_PATH, 'airports.shp')
gdf = geopandas.read_file(data)
gdf
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AREA</th>
      <th>PERIMETER</th>
      <th>AIRPRTX020</th>
      <th>LOCID</th>
      <th>FEATURE</th>
      <th>NAME</th>
      <th>TOT_ENP</th>
      <th>STATE</th>
      <th>COUNTY</th>
      <th>FIPS</th>
      <th>STATE_FIPS</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>5</td>
      <td>4Z7</td>
      <td>Seaplane Base</td>
      <td>Hyder</td>
      <td>319</td>
      <td>None</td>
      <td>Prince of Wales-Outer Ketchikan Census Area</td>
      <td>02201</td>
      <td>02</td>
      <td>POINT (-130.0125274658203 55.90433883666992)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>6</td>
      <td>KCL</td>
      <td>Airport</td>
      <td>Chignik Lagoon</td>
      <td>2697</td>
      <td>AK</td>
      <td>Lake and Peninsula Borough</td>
      <td>02164</td>
      <td>02</td>
      <td>POINT (-158.5325622558594 56.30786895751953)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>7</td>
      <td>KKA</td>
      <td>Airport</td>
      <td>Koyuk</td>
      <td>2346</td>
      <td>AK</td>
      <td>Nome Census Area</td>
      <td>02180</td>
      <td>02</td>
      <td>POINT (-161.1510772705078 64.93807220458984)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>8</td>
      <td>KVL</td>
      <td>Airport</td>
      <td>Kivalina</td>
      <td>3313</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-164.5255889892578 67.74520874023438)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>10</td>
      <td>5KE</td>
      <td>Seaplane Base</td>
      <td>Ketchikan Harbor</td>
      <td>46644</td>
      <td>AK</td>
      <td>Ketchikan Gateway Borough</td>
      <td>02130</td>
      <td>02</td>
      <td>POINT (-131.6851043701172 55.34780883789063)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>666</td>
      <td>MTM</td>
      <td>Seaplane Base</td>
      <td>Metlakatla</td>
      <td>15387</td>
      <td>AK</td>
      <td>Prince of Wales-Outer Ketchikan Census Area</td>
      <td>02201</td>
      <td>02</td>
      <td>POINT (-131.5780639648438 55.13104629516602)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>667</td>
      <td>KWF</td>
      <td>Seaplane Base</td>
      <td>Waterfall</td>
      <td>2018</td>
      <td>AK</td>
      <td>Prince of Wales-Outer Ketchikan Census Area</td>
      <td>02201</td>
      <td>02</td>
      <td>POINT (-133.2433319091797 55.29632186889648)</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>668</td>
      <td>KTN</td>
      <td>Airport</td>
      <td>Ketchikan</td>
      <td>132451</td>
      <td>AK</td>
      <td>Ketchikan Gateway Borough</td>
      <td>02130</td>
      <td>02</td>
      <td>POINT (-131.7137451171875 55.35556793212891)</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>669</td>
      <td>KXA</td>
      <td>Seaplane Base</td>
      <td>Kasaan</td>
      <td>455</td>
      <td>None</td>
      <td>Prince of Wales-Outer Ketchikan Census Area</td>
      <td>02201</td>
      <td>02</td>
      <td>POINT (-132.3975219726563 55.53741455078125)</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>670</td>
      <td>HYL</td>
      <td>Seaplane Base</td>
      <td>Hollis</td>
      <td>4170</td>
      <td>AK</td>
      <td>Prince of Wales-Outer Ketchikan Census Area</td>
      <td>02201</td>
      <td>02</td>
      <td>POINT (-132.6460876464844 55.48158645629883)</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>671</td>
      <td>CGA</td>
      <td>Seaplane Base</td>
      <td>Craig</td>
      <td>5898</td>
      <td>None</td>
      <td>Prince of Wales-Outer Ketchikan Census Area</td>
      <td>02201</td>
      <td>02</td>
      <td>POINT (-133.1477966308594 55.47883224487305)</td>
    </tr>
    <tr>
      <th>11</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>672</td>
      <td>KTB</td>
      <td>Seaplane Base</td>
      <td>Thorne Bay</td>
      <td>5210</td>
      <td>AK</td>
      <td>Prince of Wales-Outer Ketchikan Census Area</td>
      <td>02201</td>
      <td>02</td>
      <td>POINT (-132.5366821289063 55.68796157836914)</td>
    </tr>
    <tr>
      <th>12</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>673</td>
      <td>KCC</td>
      <td>Seaplane Base</td>
      <td>Coffman Cove</td>
      <td>705</td>
      <td>AK</td>
      <td>Prince of Wales-Outer Ketchikan Census Area</td>
      <td>02201</td>
      <td>02</td>
      <td>POINT (-132.8419647216797 56.00324249267578)</td>
    </tr>
    <tr>
      <th>13</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>674</td>
      <td>84K</td>
      <td>Seaplane Base</td>
      <td>Meyers Chuck</td>
      <td>341</td>
      <td>AK</td>
      <td>Prince of Wales-Outer Ketchikan Census Area</td>
      <td>02201</td>
      <td>02</td>
      <td>POINT (-132.2550201416016 55.7396354675293)</td>
    </tr>
    <tr>
      <th>14</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>675</td>
      <td>AKW</td>
      <td>Airport</td>
      <td>Klawock</td>
      <td>3900</td>
      <td>AK</td>
      <td>Prince of Wales-Outer Ketchikan Census Area</td>
      <td>02201</td>
      <td>02</td>
      <td>POINT (-133.0760040283203 55.5792350769043)</td>
    </tr>
    <tr>
      <th>15</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>676</td>
      <td>78K</td>
      <td>Seaplane Base</td>
      <td>Yes Bay Lodge</td>
      <td>941</td>
      <td>AK</td>
      <td>Prince of Wales-Outer Ketchikan Census Area</td>
      <td>02201</td>
      <td>02</td>
      <td>POINT (-131.8011322021484 55.91630172729492)</td>
    </tr>
    <tr>
      <th>16</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>677</td>
      <td>WRG</td>
      <td>Airport</td>
      <td>Wrangell</td>
      <td>13895</td>
      <td>AK</td>
      <td>Wrangell-Petersburg Census Area</td>
      <td>02280</td>
      <td>02</td>
      <td>POINT (-132.3698272705078 56.48432540893555)</td>
    </tr>
    <tr>
      <th>17</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>678</td>
      <td>PSG</td>
      <td>Airport</td>
      <td>Petersburg James A. Johnson</td>
      <td>21047</td>
      <td>AK</td>
      <td>Wrangell-Petersburg Census Area</td>
      <td>02280</td>
      <td>02</td>
      <td>POINT (-132.9452819824219 56.80165100097656)</td>
    </tr>
    <tr>
      <th>18</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>679</td>
      <td>KAE</td>
      <td>Seaplane Base</td>
      <td>Kake</td>
      <td>3466</td>
      <td>AK</td>
      <td>Wrangell-Petersburg Census Area</td>
      <td>02280</td>
      <td>02</td>
      <td>POINT (-133.9456176757813 56.97299575805664)</td>
    </tr>
    <tr>
      <th>19</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>680</td>
      <td>SIT</td>
      <td>Airport</td>
      <td>Sitka Rocky Gutierrez</td>
      <td>68659</td>
      <td>AK</td>
      <td>Sitka Borough</td>
      <td>02220</td>
      <td>02</td>
      <td>POINT (-135.3616027832031 57.04713821411133)</td>
    </tr>
    <tr>
      <th>20</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>681</td>
      <td>AGN</td>
      <td>Seaplane Base</td>
      <td>Angoon</td>
      <td>2865</td>
      <td>AK</td>
      <td>Skagway-Hoonah-Angoon Census Area</td>
      <td>02232</td>
      <td>02</td>
      <td>POINT (-134.5850982666016 57.50355529785156)</td>
    </tr>
    <tr>
      <th>21</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>682</td>
      <td>FNR</td>
      <td>Seaplane Base</td>
      <td>Funter Bay</td>
      <td>303</td>
      <td>AK</td>
      <td>Skagway-Hoonah-Angoon Census Area</td>
      <td>02232</td>
      <td>02</td>
      <td>POINT (-134.8979034423828 58.25438690185547)</td>
    </tr>
    <tr>
      <th>22</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>683</td>
      <td>TKE</td>
      <td>Seaplane Base</td>
      <td>Tenakee</td>
      <td>1072</td>
      <td>AK</td>
      <td>Skagway-Hoonah-Angoon Census Area</td>
      <td>02232</td>
      <td>02</td>
      <td>POINT (-135.2184448242188 57.77965927124023)</td>
    </tr>
    <tr>
      <th>23</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>684</td>
      <td>HWI</td>
      <td>Seaplane Base</td>
      <td>Hawk Inlet</td>
      <td>1073</td>
      <td>AK</td>
      <td>Skagway-Hoonah-Angoon Census Area</td>
      <td>02232</td>
      <td>02</td>
      <td>POINT (-134.7559509277344 58.12744140625)</td>
    </tr>
    <tr>
      <th>24</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>685</td>
      <td>HNH</td>
      <td>Airport</td>
      <td>Hoonah</td>
      <td>9126</td>
      <td>AK</td>
      <td>Skagway-Hoonah-Angoon Census Area</td>
      <td>02232</td>
      <td>02</td>
      <td>POINT (-135.4096984863281 58.09609222412109)</td>
    </tr>
    <tr>
      <th>25</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>686</td>
      <td>JNU</td>
      <td>Airport</td>
      <td>Juneau International</td>
      <td>377559</td>
      <td>AK</td>
      <td>Juneau Borough</td>
      <td>02110</td>
      <td>02</td>
      <td>POINT (-134.5762786865234 58.35496139526367)</td>
    </tr>
    <tr>
      <th>26</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>687</td>
      <td>PEC</td>
      <td>Seaplane Base</td>
      <td>Pelican</td>
      <td>1022</td>
      <td>AK</td>
      <td>Skagway-Hoonah-Angoon Census Area</td>
      <td>02232</td>
      <td>02</td>
      <td>POINT (-136.2362670898438 57.95517349243164)</td>
    </tr>
    <tr>
      <th>27</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>688</td>
      <td>ELV</td>
      <td>Seaplane Base</td>
      <td>Elfin Cove</td>
      <td>1325</td>
      <td>AK</td>
      <td>Skagway-Hoonah-Angoon Census Area</td>
      <td>02232</td>
      <td>02</td>
      <td>POINT (-136.3473968505859 58.19518280029297)</td>
    </tr>
    <tr>
      <th>28</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>689</td>
      <td>EXI</td>
      <td>Seaplane Base</td>
      <td>Excursion Inlet</td>
      <td>1972</td>
      <td>AK</td>
      <td>Skagway-Hoonah-Angoon Census Area</td>
      <td>02232</td>
      <td>02</td>
      <td>POINT (-135.4490356445313 58.42049789428711)</td>
    </tr>
    <tr>
      <th>29</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>690</td>
      <td>GST</td>
      <td>Airport</td>
      <td>Gustavus</td>
      <td>11570</td>
      <td>AK</td>
      <td>Skagway-Hoonah-Angoon Census Area</td>
      <td>02232</td>
      <td>02</td>
      <td>POINT (-135.7073822021484 58.42438125610352)</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>191</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>852</td>
      <td>WMO</td>
      <td>Airport</td>
      <td>White Mountain</td>
      <td>1790</td>
      <td>AK</td>
      <td>Nome Census Area</td>
      <td>02180</td>
      <td>02</td>
      <td>POINT (-163.4125518798828 64.68919372558594)</td>
    </tr>
    <tr>
      <th>192</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>853</td>
      <td>BVK</td>
      <td>Airport</td>
      <td>Buckland</td>
      <td>3153</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-161.1519775390625 65.98228454589844)</td>
    </tr>
    <tr>
      <th>193</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>854</td>
      <td>WLK</td>
      <td>Airport</td>
      <td>Selawik</td>
      <td>5176</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-159.9861907958984 66.60002899169922)</td>
    </tr>
    <tr>
      <th>194</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>855</td>
      <td>OBU</td>
      <td>Airport</td>
      <td>Kobuk</td>
      <td>992</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-156.8610534667969 66.90917205810547)</td>
    </tr>
    <tr>
      <th>195</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>856</td>
      <td>SHG</td>
      <td>Airport</td>
      <td>Shungnak</td>
      <td>2309</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-157.1505126953125 66.88916778564453)</td>
    </tr>
    <tr>
      <th>196</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>857</td>
      <td>AFM</td>
      <td>Airport</td>
      <td>Ambler</td>
      <td>2423</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-157.8536224365234 67.10610198974609)</td>
    </tr>
    <tr>
      <th>197</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>858</td>
      <td>SCC</td>
      <td>Airport</td>
      <td>Deadhorse</td>
      <td>12479</td>
      <td>AK</td>
      <td>North Slope Borough</td>
      <td>02185</td>
      <td>02</td>
      <td>POINT (-148.4651641845703 70.19475555419922)</td>
    </tr>
    <tr>
      <th>198</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>859</td>
      <td>OME</td>
      <td>Airport</td>
      <td>Nome</td>
      <td>56911</td>
      <td>AK</td>
      <td>Nome Census Area</td>
      <td>02180</td>
      <td>02</td>
      <td>POINT (-165.4452514648438 64.51219940185547)</td>
    </tr>
    <tr>
      <th>199</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>860</td>
      <td>DEE</td>
      <td>Airport</td>
      <td>Deering</td>
      <td>1473</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-162.7666015625 66.06820678710938)</td>
    </tr>
    <tr>
      <th>200</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>861</td>
      <td>IAN</td>
      <td>Airport</td>
      <td>Bob Baker Memorial</td>
      <td>3899</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-160.4358673095703 66.97937774658203)</td>
    </tr>
    <tr>
      <th>201</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>862</td>
      <td>ORV</td>
      <td>Airport</td>
      <td>Robert (Bob) Curtis Memorial</td>
      <td>5266</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-161.0277862548828 66.82852935791016)</td>
    </tr>
    <tr>
      <th>202</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>863</td>
      <td>OTZ</td>
      <td>Airport</td>
      <td>Ralph Wien Memorial</td>
      <td>59351</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-162.5985565185547 66.88467407226563)</td>
    </tr>
    <tr>
      <th>203</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>864</td>
      <td>AQT</td>
      <td>Airport</td>
      <td>Nuiqsut</td>
      <td>1018</td>
      <td>AK</td>
      <td>North Slope Borough</td>
      <td>02185</td>
      <td>02</td>
      <td>POINT (-151.0055541992188 70.20995330810547)</td>
    </tr>
    <tr>
      <th>204</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>865</td>
      <td>SVA</td>
      <td>Airport</td>
      <td>Savoonga</td>
      <td>4271</td>
      <td>AK</td>
      <td>Nome Census Area</td>
      <td>02180</td>
      <td>02</td>
      <td>POINT (-170.4926300048828 63.68639373779297)</td>
    </tr>
    <tr>
      <th>205</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>866</td>
      <td>K54</td>
      <td>Airport</td>
      <td>Teller</td>
      <td>983</td>
      <td>AK</td>
      <td>Nome Census Area</td>
      <td>02180</td>
      <td>02</td>
      <td>POINT (-166.3360137939453 65.24089813232422)</td>
    </tr>
    <tr>
      <th>206</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>867</td>
      <td>KTS</td>
      <td>Airport</td>
      <td>Brevig Mission</td>
      <td>1463</td>
      <td>AK</td>
      <td>Nome Census Area</td>
      <td>02180</td>
      <td>02</td>
      <td>POINT (-166.4631652832031 65.33135986328125)</td>
    </tr>
    <tr>
      <th>207</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>868</td>
      <td>SHH</td>
      <td>Airport</td>
      <td>Shishmaref</td>
      <td>3866</td>
      <td>AK</td>
      <td>Nome Census Area</td>
      <td>02180</td>
      <td>02</td>
      <td>POINT (-166.0895538330078 66.24956512451172)</td>
    </tr>
    <tr>
      <th>208</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>869</td>
      <td>IWK</td>
      <td>Airport</td>
      <td>Wales</td>
      <td>1542</td>
      <td>AK</td>
      <td>Nome Census Area</td>
      <td>02180</td>
      <td>02</td>
      <td>POINT (-168.0991668701172 65.62393951416016)</td>
    </tr>
    <tr>
      <th>209</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>870</td>
      <td>WTK</td>
      <td>Airport</td>
      <td>Noatak</td>
      <td>4124</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-162.9752807617188 67.56208038330078)</td>
    </tr>
    <tr>
      <th>210</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>871</td>
      <td>AED</td>
      <td>Airport</td>
      <td>Red Dog</td>
      <td>9316</td>
      <td>AK</td>
      <td>Northwest Arctic Borough</td>
      <td>02188</td>
      <td>02</td>
      <td>POINT (-162.9029541015625 68.03128814697266)</td>
    </tr>
    <tr>
      <th>211</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>872</td>
      <td>ATK</td>
      <td>Airport</td>
      <td>Atqasuk Edward Burnell Sr. Memorial</td>
      <td>2686</td>
      <td>AK</td>
      <td>North Slope Borough</td>
      <td>02185</td>
      <td>02</td>
      <td>POINT (-157.4357299804688 70.46727752685547)</td>
    </tr>
    <tr>
      <th>212</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>874</td>
      <td>GAM</td>
      <td>Airport</td>
      <td>Gambell</td>
      <td>4098</td>
      <td>AK</td>
      <td>Nome Census Area</td>
      <td>02180</td>
      <td>02</td>
      <td>POINT (-171.7328186035156 63.76676559448242)</td>
    </tr>
    <tr>
      <th>213</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>875</td>
      <td>PHO</td>
      <td>Airport</td>
      <td>Point Hope</td>
      <td>5533</td>
      <td>AK</td>
      <td>North Slope Borough</td>
      <td>02185</td>
      <td>02</td>
      <td>POINT (-166.7993011474609 68.34877777099609)</td>
    </tr>
    <tr>
      <th>214</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>876</td>
      <td>PIZ</td>
      <td>Airport</td>
      <td>Point Lay LRRS</td>
      <td>1962</td>
      <td>AK</td>
      <td>North Slope Borough</td>
      <td>02185</td>
      <td>02</td>
      <td>POINT (-163.0053405761719 69.73287200927734)</td>
    </tr>
    <tr>
      <th>215</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>877</td>
      <td>AWI</td>
      <td>Airport</td>
      <td>Wainwright</td>
      <td>3783</td>
      <td>AK</td>
      <td>North Slope Borough</td>
      <td>02185</td>
      <td>02</td>
      <td>POINT (-159.9947509765625 70.63800048828125)</td>
    </tr>
    <tr>
      <th>216</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>878</td>
      <td>BRW</td>
      <td>Airport</td>
      <td>Wiley Post-Will Rogers Memorial</td>
      <td>40751</td>
      <td>AK</td>
      <td>North Slope Borough</td>
      <td>02185</td>
      <td>02</td>
      <td>POINT (-156.7660064697266 71.28544616699219)</td>
    </tr>
    <tr>
      <th>217</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>880</td>
      <td>KNW</td>
      <td>Airport</td>
      <td>New Stuyahok</td>
      <td>2217</td>
      <td>AK</td>
      <td>Dillingham Census Area</td>
      <td>02070</td>
      <td>02</td>
      <td>POINT (-157.3271942138672 59.44955444335938)</td>
    </tr>
    <tr>
      <th>218</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>881</td>
      <td>ANC</td>
      <td>Airport</td>
      <td>Ted Stevens Anchorage International</td>
      <td>2536319</td>
      <td>AK</td>
      <td>Anchorage Borough</td>
      <td>02020</td>
      <td>02</td>
      <td>POINT (-149.9961853027344 61.17432022094727)</td>
    </tr>
    <tr>
      <th>219</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>900</td>
      <td>ILI</td>
      <td>Airport</td>
      <td>Iliamna</td>
      <td>13806</td>
      <td>AK</td>
      <td>Lake and Peninsula Borough</td>
      <td>02164</td>
      <td>02</td>
      <td>POINT (-154.9109649658203 59.75379943847656)</td>
    </tr>
    <tr>
      <th>220</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>901</td>
      <td>KYU</td>
      <td>Airport</td>
      <td>Koyukuk</td>
      <td>994</td>
      <td>AK</td>
      <td>Yukon-Koyukuk Census Area</td>
      <td>02290</td>
      <td>02</td>
      <td>POINT (-157.7158355712891 64.87714385986328)</td>
    </tr>
  </tbody>
</table>
<p>221 rows × 12 columns</p>
</div>




```python
%matplotlib inline
gdf.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1e89bf8ddd8>




![png](https://raw.github.com/bellockk/alphashape/master/media/output_4_1.png)



```python
gdf.crs
```




    {'init': 'epsg:4269'}



## Generate Alpha Shape
The alpha shape will be generated in the coordinate frame the geodataframe is in.  In this example, we will project into an Albers Equal Area projection, construct our alpha shape in that coordinate system, and then convert back to the source projection.

### Project to Albers Equal Area Spatial Reference


```python
import cartopy.crs as ccrs
gdf_proj = gdf.to_crs(ccrs.AlbersEqualArea().proj4_init)
gdf_proj.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1e89c123b38>




![png](https://raw.github.com/bellockk/alphashape/master/media/output_8_1.png)


### Determine the Alpha Shape


```python
import alphashape
alpha_shape = alphashape.alphashape(gdf_proj)
alpha_shape.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1e89c48b048>




![png](https://raw.github.com/bellockk/alphashape/master/media/output_10_1.png)


### Plotting the Alpha Shape over the Data Points
#### Plate Carree Projection


```python
import matplotlib.pyplot as plt
ax = plt.axes(projection=ccrs.PlateCarree())
ax.scatter([p.x for p in gdf_proj['geometry']],
           [p.y for p in gdf_proj['geometry']],
           transform=ccrs.AlbersEqualArea())
ax.add_geometries(
    alpha_shape['geometry'],
    crs=ccrs.AlbersEqualArea(), alpha=.2)
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_12_0.png)


#### Robinson Projection


```python
import matplotlib.pyplot as plt
ax = plt.axes(projection=ccrs.Robinson())
ax.scatter([p.x for p in gdf_proj['geometry']],
           [p.y for p in gdf_proj['geometry']],
           transform=ccrs.AlbersEqualArea())
ax.add_geometries(
    alpha_shape['geometry'],
    crs=ccrs.AlbersEqualArea(), alpha=.2)
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_14_0.png)


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
