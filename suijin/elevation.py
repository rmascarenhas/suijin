"""elevation: reads elevation data from TIF files to produce a matrix of data.

Elevation data is commonly provided using the GeoTIFF format, where each element
in the matrix represents an elevation data point.

For easier manipulation of such data, this module reads the TIF file provided
(using GDAL), converts that data to an ASCII Grid and then loads that up using
built-in methods available in the numpy package.

Usage

    import elevation

    elevation.read("/path/to/data.tiff")
    # => elevation.Elevation

The `read` function returns a named tuple called `Elevation`. It contains the
information from the parsed TIF file (such as number of rows and columns of data)
as well as the matrix of data itself.
"""

from osgeo import gdal
from collections import namedtuple
import numpy
import tempfile
import linecache

Elevation = namedtuple('Elevation', 'ncols nrows xllcorner yllcorner cellsize nodata_value data')

# number of header fields in the ASCII Grid intermediary format. These lines provide
# metadata that needs to be skipped when reading data with numpy.
header_size = 6

def read(path):
    """Reads a TIF file located at `path`, and returns parsed data.
    """

    dataset = gdal.Open(path, gdal.GA_ReadOnly)
    ascii_file = _to_ascii_grid(dataset)

    data = numpy.loadtxt(ascii_file.name, skiprows=header_size)
    ncols, nrows, xllcorner, yllcorner, cellsize, nodata_value = _parse_headers(ascii_file.name)

    return Elevation(ncols, nrows, xllcorner, yllcorner, cellsize, nodata_value, data)

    # when this method returns, `ascii_file` (a temporary file containing the
    # ASCII grid) goes out of scope. In the next GC run, the file will be
    # implicitly closed and therefore deleted from the system.

def _to_ascii_grid(dataset):
    tmpfile = tempfile.NamedTemporaryFile()
    ascii_driver = gdal.GetDriverByName('AAIGrid')

    ascii_driver.CreateCopy(tmpfile.name, dataset)
    return tmpfile

def _parse_headers(path):
    lines = [linecache.getline(path, n) for n in range(1, header_size+1)]

    # extracts the value for each header. Typically, these headers are in the
    # format:
    #
    #   ncols   983
    #
    # To extract that `983`, it is necessary to get the last field, remove
    # any leading/trailing white spaces from it and transform it to an actual
    # number
    clean = lambda header: float(header.split(' ')[-1].strip())

    return [clean(header) for header in lines]
