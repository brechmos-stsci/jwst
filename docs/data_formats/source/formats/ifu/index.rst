.. _data-ifu:

Integral Field Unit
===================

Modes used by this definition: :ref:`0n0NIRSPEC IFU <nirspec-ifu>`, :ref:`MIRI Medium Resolution Spectroscopy <miri-mrs>`.

:ref:`Level 1 <level1>` and :ref:`Level 2a <level2a>` datasets are the same for all imaging modes.


.. Level 2b Information

Level 2b Description
--------------------

.. FITS File Description

The IFU dataset is a 3D dataset with axes of spatial, spatial and wavelength dimensions.  There will
be a SCI, DQ and ERR HDU in a FITS file.  There will be multiple FITS files, one for each exposure.


Level 2C Description
--------------------

.. TL;DR

TL;DR
^^^^^
* 3D dataset, spatial, spatial, wavelength
* Each exposure will be in a separate FITS file


.. FITS File Description

FITS File Description
^^^^^^^^^^^^^^^^^^^^^

The IFU dataset is a 3D dataset with axes of spatial, spatial and wavelength dimensions.  There will
be a SCI, DQ, ERR HDU.  Each will be 3D and the data will be ordered by spatial, spatial dimension first
and then by wavelength. So the first m x n set of data will be an image at the first wavelength.

There will be a FITS file for *each* exposure.

Level 3 Description
-------------------

The Level 3 IFU dataset will be the same data format as in the Level 2c. Each will be 3D and the data
will be ordered by spatial, spatial dimension first and then by wavelength. So the first m x n set of data will be
an image at the first wavelength.
