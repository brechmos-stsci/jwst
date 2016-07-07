.. _data-soss:

Single Object Slitless Spectroscopy
===================================

Modes used by this definition: :ref:`MIRI Low Resolution Slitless Spectroscopy <miri-lrs-slitless-standard>` and
:ref:`NIRISS Single Object Slitless Specroscopy <niriss-soss-standard>`.


.. Level 1 Information

.. include:: /levels/level1/index.rst


.. Level 2a Information

.. include:: /levels/level2a/index.rst


.. Level 2b Information

Level 2b Description
--------------------

.. FITS File Description

The IFU dataset is a 2D dataset with axes of spatial and wavelength dimensions.  There will
be a SCI, DQ and ERR HDU in a FITS file.  There will be multiple FITS files, one for each exposure. (??)


Level 2C Description
--------------------

.. TL;DR

TL;DR
^^^^^
* 2D dataset, spatial, wavelength
* Single SCI, DQ, ERR tuple
* Each exposure will be in a separate FITS file (??)


.. FITS File Description

FITS File Description
^^^^^^^^^^^^^^^^^^^^^

The IFU dataset is a 2D dataset with axes of spatial and wavelength dimensions.  There will
be a SCI, DQ, ERR HDU.

There will be a FITS file for *each* exposure.

Level 3 Description
-------------------

The Level 3 IFU dataset will be the same data format as in the Level 2c. Each will be 2D and the data
will be ordered by spatial dimension first and then by wavelength.