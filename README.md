Suijin: hydrological analysis tool
==================================

Suijin (水神) is the god of water, in Japanese mythology.

This is a tool to run hydrological analysis, given elevation data as input. Namely,
this tool implements both [flow direction](http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/flow-direction.htm)
and [flow accumulation](https://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/how-flow-accumulation-works.htm)
natively.

### Usage

To invoke the tool, it will be necessary to have a copy of the elevation data, in TIF format.

```console
$ ./bin/suijin ele.tiff direction.tiff --algo direction
```

See `bin/suijin -h` for usage instructions and available options.


### Set up

Suijin requires Python 2.7. Apart from that, GDAL bindings for Python are also required.
To install GDAL and Python support on a Linux box, it is sufficient to run:

```console
$ sudo apt-get build-dep gdal
$ curl -O 'http://download.osgeo.org/gdal/2.1.0/gdal-2.1.0.tar.gz'
$ tar zxf gdal-2.1.0.tar.gz
$ cd gdal-2.1.0
$ make
$ sudo make install
$ cd swig/python
$ sudo python setup.py install
```

Requirements for this project can be installed using `pip`:

```console
$ pip install -r requirements.txt
```
