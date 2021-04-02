=====
Usage
=====

To use the Alpha Shape Toolbox in a project::

    import alphashape

Reference the examples gallery for further demonstration of using the Python API.

To use the Alpha Shape Toolbox from the command line::

    Usage: alphashape [OPTIONS] SOURCE TARGET
    
      Example console appication using the alphashape toolbox.
    
      Given an input shapefile or GeoJSON INPUT with point geometry, write out a
      new OUTPUT that contains the geometries resulting from execting the alpha
      shape toolbox.
    
      The alpha parameter is optional.  If provided it will return the alpha
      shape for the given value, if one is not provided, the tightest fitting
      alpha shape that contains all input points will be solved for.
    
      The EPSG code of a coordinate system can also be given to conduct the
      alpha shape analysis in.  If one is not given the coordinate system of the
      input data will be used.
    
      The output file will always have the same coordinate system as the source
      file.
    
      The output file format will be determined by the extension of the provided
      target filename and can be written out in shapefile format or GeoJSON.
    
    Options:
      -a, --alpha FLOAT    Alpha parameter
      -e, --epsg INTEGER   EPSG code to create alpha shape in
      -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
      --help               Show this message and exit.
