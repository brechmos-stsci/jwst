.. _data-fss:

Fixed Slit Spectroscopy
=======================

Modes used by this imaging definition: :ref:`MIRI Fixed Slit Low Resolution Spectroscopy <miri-lrs-fixed-slit>`,
:ref:`NIRSPEC Fixed Slit Spectroscopy <nirspec-fs>`, and :ref:`NIRSPEC Multi-Object Spectroscopy <nirspec-mos>`

:ref:`Level 1 <level1>` and :ref:`Level 2a <level2a>` datasets are the same for all imaging modes.


.. Level 2b Information

.. Level 2b Information

Level 2b Description
--------------------

.. TL;DR

TL;DR
^^^^^
* 2D dataset: spatial, wavelength
* Multiple [SCI, DQ, ERR] tuples in a single FITS file
* Each exposure will be in a separate FITS file

.. FITS File Description

FITS File Description
^^^^^^^^^^^^^^^^^^

The fixed slit spectroscopic dataset is a 2D dataset with axes of spatial and wavelength dimensions.  There will
be N [SCI, DQ and ERR] HDU tuples in a FITS file. Each [SCI, DQ, ERR] tuple represents a dataset from a slit.

There will be multiple FITS files, one for each exposure.


Level 2C Description
--------------------

.. TL;DR

TL;DR
^^^^^
* 2D dataset: spatial, wavelength
* Multiple [SCI, DQ, ERR] tuples in a single FITS file
* Each exposure will be in a separate FITS file


.. FITS File Description

FITS File Description
^^^^^^^^^^^^^^^^^^^^^

The IFU dataset is a 2D dataset with axes of spatial and wavelength dimensions.  There will
be a SCI, DQ, ERR HDU.

There will be a FITS file for *each* exposure.

Level 3 Description
-------------------

.. TL;DR

TL;DR
^^^^^
* 2D dataset: spatial, wavelength
* Multiple [SCI, DQ, ERR] tuples in a single FITS file
* Each exposure will be in a separate FITS file


.. FITS File Description

FITS File Description
^^^^^^^^^^^^^^^^^^^^^

The Level 3 IFU dataset will be the same data format as in the Level 2c. Each will be 2D and the data
will be ordered by spatial dimension first and then by wavelength.

