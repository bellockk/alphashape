=====
Usage
=====

To use the Alpha Shape Toolbox in a project::

    import alphashape

Reference the examples gallery for further demonstration of using the Python API.

To use the Alpha Shape Toolbox from the command line::

    Usage: alphashape [OPTIONS] SOURCE TARGET
    
      Example console appication using the alphashape toolbox.
    
      Given an input shapefile INPUT with point geometry, write out a new
      shapefile OUTPUT that contains the geometries resulting from execting the
      alpha shape toolbox.
    
      The alpha parameter is optional.  If provided it will return the alpha
      shape for the given value, if one is not provided, the tightest fitting
      alpha shape that contains all input points will be solved for.
    
      The EPSG code of a coordinate system can also be given to conduct the
      alpha shape analysis in.  If one is not given the coordinate system of the
      input data will be used.
    
      The output shapefile will always have the same coordinate system as the
      source file.
    
    Options:
      -a, --alpha FLOAT    Alpha parameter
      -e, --epsg INTEGER   EPSG code to create alpha shape in
      -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
      --help               Show this message and exit.

