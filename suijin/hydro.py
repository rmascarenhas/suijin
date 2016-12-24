"""hydro: this module implements the hydrological analysis algorithms.

The hydro module exposes two different classes:

    hydro.Direction
    hydro.Accumulation

Each implementing the algorithm described by their names. In all cases, a TIF
file with elevation data is received as input, and the result is stored as
an output ASCII Grid file.

Usage

    elevation_data = "/path/to/elevation.tiff"
    flow_direction = "/path/to/output.tiff"

    hydro.Direction(elevation_data).run(flow_direction)

The output can then be analysed with tools such as QGIS.
"""

import elevation
import numpy as np

class Cell(object):
    """A cell in a data grid.

    A cell is defined by its position in the matrix (row and column), as well as the
    value relative another reference cell (see hydro.Direction.)

    A cell is considered to be valid (in terms of flow direction calculation)
    if it is within bounds and if its elevation datapoint is different from the
    NODATA_value for the given input data.

    Usage

        cell = hydro.Cell(x, y, 128, elevation)
        cell.is_valid() # => True
    """

    def __init__(self, x, y, value, elevation):
        self.x         = x
        self.y         = y
        self.value     = value
        self.elevation = elevation

    def is_valid(self):
        """Indicates whether the cell is valid or not.

        A cell must be within bounds and not be equal to the NODATA_value.
        """

        return (
            self.x >= 0               and
            self.y >= 0                   and
            self.x < self.elevation.nrows and
            self.y < self.elevation.ncols and
            self.elevation.data[self.x][self.y] != self.elevation.nodata_value
        )

class Grid(object):
    """Wrapper for a data grid.

    The data grid could represent data with multiple contexts: it could have
    elevation data, or it could be a flow direction grid.

    It keeps track of a 2 dimensional array and is able to serialize itself to
    ASCII Grid for later analysis.

    Usage

        grid = hydro.Grid(elevation)
        grid.add_row(array)
        grid.render("/path/to/file.asc") # => renders the data in a file
    """

    def __init__(self, elevation):
        self.elevation = elevation
        self.data      = np.array([[]], ndmin=2)

    def nodata(self):
        """Returns the value used for the NODATA_value field.

        Uses the default of `-9999` for that.
        """
        return -9999

    def add_row(self, row):
        """adds a row of data to the grid.

        This method ensures that every row of data has the exact same size.
        Callers passing arrays with different sizes when adding rows will draw
        an error when invoking this method.
        """

        # if there is data previously in the `data` field, make sure new rows
        # respect the size by passing `axis=0` to `append`. If we are inserting
        # the first row of data, there is nothing to be enforced and the first
        # row will determine the size to be expected in subsequent insertions.
        if self.data.any():
            self.data = np.append(self.data, [row], axis=0)
        else:
            self.data = np.append(self.data, [row], axis=1)

    def render(self, path):
        """Generates an file in the ASCII Grid format with the data provided.

        The `path` argument passed to this method needs to point to the location
        of the file where the data will be persisted.
        """

        header =  'ncols       {}\n'.format(int(self.elevation.ncols))
        header += 'nrows       {}\n'.format(int(self.elevation.nrows))
        header += 'xllcorner   {}\n'.format(self.elevation.xllcorner)
        header += 'yllcorner   {}\n'.format(self.elevation.yllcorner)
        header += 'cellsize   {}\n'.format(self.elevation.cellsize)
        header += 'NODATA_value   {}\n'.format(self.nodata())

        with open(path, 'wb') as f:
            f.write(header)
            for row in self.data:
                f.write(' '.join(str(n) for n in row))
                f.write('\n')

class Direction(object):
    """Implements the flow direction algorithm.

    For a longer description of the algorithm, check:

        http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/flow-direction.htm

    Usage

        # generating the flow direction for an elevation data file
        hydro.Direction("/path/to/elevation.tiff").run("output.asc")
    """

    def __init__(self, input):
        self.input_data = elevation.read(input)

    def run(self, output):
        grid = Grid(self.input_data)

        for row in range(int(self.input_data.nrows)):
            direction_row = np.array([])

            for col in range(int(self.input_data.ncols)):
                # create the list of 8 neighbours of a cell using the values
                # described in the algorithm specification
                neighbours = [
                    Cell(row-1, col-1, 32,  self.input_data),
                    Cell(row-1, col,   64,  self.input_data),
                    Cell(row-1, col+1, 128, self.input_data),
                    Cell(row,   col-1, 16,  self.input_data),
                    Cell(row,   col+1, 1,   self.input_data),
                    Cell(row+1, col-1, 8,   self.input_data),
                    Cell(row+1, col,   4,   self.input_data),
                    Cell(row+1, col+1, 2,   self.input_data)
                ]

                # only "valid" neighbours (see definition on the `Cell` class)
                # are considered when calculating the flow direction.
                valid = [n for n in neighbours if n.is_valid()]

                # if there is at least one valid neighbour, process the list
                # to find the flow direction. Otherwise, there is not enough
                # data to find out the direction, and a nodata data point is
                # inserted.
                if valid:
                    value = self._process_element(valid)
                else:
                    value = grid.nodata()

                direction_row = np.append(direction_row, value)

            grid.add_row(direction_row)

        grid.render(output)

    def _process_element(self, neighbours):
        # sorts the neighbours according to their elevation data. The first element
        # is that with the lowest elevation
        collection = sorted(neighbours, key=self._cell_elevation)

        # the direction is defined to be to the lowest elevation neighbour
        # Remove it from the list and get the its 1..128 value
        min   = collection.pop(0)
        total = min.value

        # the specification defines that when the same change in z-value
        # happens in multiple directions, the value of the output flow
        # direction raster is the sum of such directions.
        for n in collection:
            if self._cell_elevation(n) == self._cell_elevation(min):
                total += n.value
            else:
                # since the list is sorted, if an element with elevation
                # different from that of `min` is found, it means all others
                # are also different (larger) than that.
                break

        return total

    def _cell_elevation(self, cell):
        return cell.elevation.data[cell.x][cell.y]
