# Alpha Shape Toolbox

[![PyPI version](https://img.shields.io/pypi/v/alphashape.svg)](https://pypi.python.org/pypi/alphashape/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/alphashape.svg)](https://pypi.python.org/pypi/alphashape/)
[![Travis](https://api.travis-ci.org/bellockk/alphashape.svg?branch=master)](https://travis-ci.org/bellockk/alphashape/)
[![CodeCov](https://codecov.io/gh/bellockk/alphashape/branch/master/graph/badge.svg)](https://codecov.io/gh/bellockk/alphashape)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/bellockk/alphashape/master)
[![Documentation Status](https://readthedocs.org/projects/alphashape/badge/?version=latest)](http://alphashape.readthedocs.io/?badge=latest)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

[![Anaconda install](https://anaconda.org/conda-forge/alphashape/badges/installer/conda.svg)](https://anaconda.org/conda-forge/alphashape)
[![Anaconda version](https://anaconda.org/conda-forge/alphashape/badges/version.svg)](https://anaconda.org/conda-forge/alphashape)
[![Anaconda downloads](https://anaconda.org/conda-forge/alphashape/badges/downloads.svg)](https://anaconda.org/conda-forge/alphashape)
[![Anaconda platforms](https://anaconda.org/conda-forge/alphashape/badges/platforms.svg)](https://anaconda.org/conda-forge/alphashape)
[![Anaconda lastupdated](https://anaconda.org/conda-forge/alphashape/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/alphashape)

Toolbox for generating alpha shapes.

Alpha shapes are often used to generalize bounding polygons containing sets of points.  The alpha parameter is defined as the value `a`, such that an edge of a  disk of radius 1/`a` can be drawn between any two edge members of a set of points and still contain all the points. The convex hull, a shape resembling what you would see if you wrapped a rubber band around pegs at all the data points, is an alpha shape where the alpha parameter is equal to zero.  In this toolbox we will be generating alpha complexes, which are closely related to alpha shapes, but which consist of straight lines between the edge points instead of arcs of circles.

https://en.wikipedia.org/wiki/Alpha_shape

https://en.wikipedia.org/wiki/Convex_hull

Creating alpha shapes around sets of points usually requires a visually interactive step where the alpha parameter for a concave hull is determined by iterating over or bisecting values to approach a best fit.  The alpha shape toolbox will provide workflows to shorten the development loop on this manual process, or to bypass it completely by solving for an alpha shape with particular characteristics.  A python API will be provided to aid in the scripted generation of alpha shapes.  A console application will also be provided as an example usage of the alpha shape toolbox, and to facilitate generation of alpha shapes from the command line.  In addition to the utility of being able to quickly iterate on alpha parameters to generate concave hulls, the framework of this tool set will provide a template for generating GIS tool sets accessible from python, the console, or graphical user interfaces without the licensing restrictions of proprietary tool sets and without having a python installation for the console and user interface.

* Free software: MIT license
* Documentation: https://alphashape.readthedocs.io.

## Features

### Import Dependencies


```python
import sys
from descartes import PolygonPatch
import matplotlib.pyplot as plt
import alphashape
```

### Define a set of points


```python
points = [(0., 0.), (0., 1.), (1., 1.), (1., 0.),
          (0.5, 0.25), (0.5, 0.75), (0.25, 0.5), (0.75, 0.5)]
```

### Plotting the input points


```python
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_5_0.png)


### Generate an Alpha Shape (Alpha=0.0) (Convex Hull)
Every convex hull is an alpha shape, but not every alpha shape is a convex hull.  When the `alphashape` function is called with an alpha parameter of 0, a convex hull will always be returned.

#### Create the alpha shape


```python
alpha_shape = alphashape.alphashape(points, 0.)
```

#### Plotting the alpha shape over the input data


```python
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_10_0.png)


### Generate an Alpha Shape (Alpha=2.0) (Concave Hull)
As we increase the alpha parameter value, the bounding shape will begin to fit the sample data with a more tightly fitting bounding box.

#### Create the alpha shape


```python
alpha_shape = alphashape.alphashape(points, 2.0)
```

#### Plotting the alpha shape over the input data


```python
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_15_0.png)


### Generate an Alpha Shape (Alpha=3.5)
If you go too high on the alpha parameter, you will start to lose points from the original data set.

#### Create the alpha shape


```python
alpha_shape = alphashape.alphashape(points, 3.5)
```

#### Plotting the alpha shape over the input data


```python
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_20_0.png)


### Generate an Alpha Shape (Alpha=5.0)
If you go too far, you will lose everything.


```python
alpha_shape = alphashape.alphashape(points, 5.0)
print(alpha_shape)
```

    GEOMETRYCOLLECTION EMPTY
    

### Generate an Alpha Shape by Solving for an Optimal Alpha Value
The alpha parameter can be solved for if it is not provided as an argument, but with large datasets this can take a long time to calculate.

#### Create the alpha shape


```python
alpha_shape = alphashape.alphashape(points)
```

#### Plotting the alpha shape over the input data


```python
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
plt.show()
```


![png](https://raw.github.com/bellockk/alphashape/master/media/output_27_0.png)

### Alpha Shapes with GeoPandas

#### Sample Data

The data used in this notebook can be obtained from the Alaska Department of Transportation and Public Facilities website at the link below.  It consists of a point collection for each of the public airports in Alaska.

[http://www.dot.alaska.gov/stwdplng/mapping/shapefiles.shtml](http://www.dot.alaska.gov/stwdplng/mapping/shapefiles.shtml)

#### Load the Shapefile


```python
import os
import geopandas
data = os.path.join(os.getcwd(), 'data', 'Public_Airports_March2018.shp')
gdf = geopandas.read_file(data)
```


```python
%matplotlib inline
gdf.plot()
```

![png](https://raw.github.com/bellockk/alphashape/master/media/output_4_1.png)



```python
gdf.crs
```




    {'init': 'epsg:4269'}



#### Generate Alpha Shape
The alpha shape will be generated in the coordinate frame the geodataframe is in.  In this example, we will project into an Albers Equal Area projection, construct our alpha shape in that coordinate system, and then convert back to the source projection.

#### Project to Albers Equal Area Spatial Reference


```python
import cartopy.crs as ccrs
gdf_proj = gdf.to_crs(ccrs.AlbersEqualArea().proj4_init)
gdf_proj.plot()
```

![png](https://raw.github.com/bellockk/alphashape/master/media/output_8_1.png)


#### Determine the Alpha Shape


```python
import alphashape
alpha_shape = alphashape.alphashape(gdf_proj)
alpha_shape.plot()
```

![png](https://raw.github.com/bellockk/alphashape/master/media/output_10_1.png)


#### Plotting the Alpha Shape over the Data Points
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
