# -*- coding: utf-8 -*-

"""Console script for alphashape."""
import os
import sys
import click
import click_log
import logging
import shapely
import geopandas
import alphashape


# Setup Logging
LOGGER = logging.getLogger(__name__)
click_log.basic_config(LOGGER)


@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('target', type=click.Path())
@click.option('--alpha', '-a', type=float, help='Alpha parameter')
@click.option('--epsg', '-e', type=int,
              help='EPSG code to create alpha shape in')
@click_log.simple_verbosity_option()
def main(source, target, alpha, epsg):
    """
    Example console appication using the alphashape toolbox.

    Given an input shapefile or GeoJSON INPUT with point geometry, write out a
    new OUTPUT that contains the geometries resulting from execting the alpha
    shape toolbox.

    The alpha parameter is optional.  If provided it will return the alpha
    shape for the given value, if one is not provided, the tightest fitting
    alpha shape that contains all input points will be solved for.

    The EPSG code of a coordinate system can also be given to conduct the alpha
    shape analysis in.  If one is not given the coordinate system of the input
    data will be used.

    The output file will always have the same coordinate system as the
    source file.

    The output file format will be determined by the extension of the provided
    target filename and can be written out in shapefile format or GeoJSON.
    """
    # Read in source data
    source_filename = click.format_filename(source)
    target_filename = click.format_filename(target)
    LOGGER.info('Reading source file: %s', source_filename)
    try:
        gdf = geopandas.read_file(source_filename)
    except:  # noqa: E722
        LOGGER.error('Could not read source file')
        return 10

    # Source data type checking
    if not any([isinstance(
            p, shapely.geometry.Point) for p in gdf['geometry']]):
        LOGGER.error('Source file does not contain multipiont features')
        return 20

    # Project data if given an EPSG code
    if epsg:
        LOGGER.info('Projecting source data to EPSG=%s', epsg)
        try:
            gdf_input = gdf.to_crs({'init': 'epsg:%s' % epsg})
        except:  # noqa: E722
            LOGGER.error('Could not project source data')
            return 30
    else:
        gdf_input = gdf

    # Generate the alpha shape
    LOGGER.info('Createing alpha shape')
    try:
        alpha_shape = alphashape.alphashape(gdf_input, alpha)
    except:  # noqa: E722
        LOGGER.error('Could not generate alpha shape')
        return 40

    # Project back to the input coordinate system if an EPSG code was given
    if epsg:
        LOGGER.info('Projecting alpha shape data to source projection')
        try:
            alpha_shape = alpha_shape.to_crs(gdf.crs)
        except:  # noqa: E722
            LOGGER.error('Could not project alpha shape')
            return 50

    # Write out the target file
    LOGGER.info('Writing target file: %s', target_filename)
    try:
        if os.path.splitext(target)[1].lower() == '.geojson':
            alpha_shape.to_file(target, driver='GeoJSON')
        else:
            alpha_shape.to_file(target)
    except:  # noqa: E722
        LOGGER.error('Could not write target file')
        return 60
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
