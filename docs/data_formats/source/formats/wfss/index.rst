.. _data-wfss:

Wide Field Slitless Spectroscopy
================================

Modes used by this definition: :ref:`NIRCAM WFS <nircam-wfss>`, :ref:`NIRISS WFS <niriss-wfss>`.


:ref:`Level 1 <level1>` and :ref:`Level 2a <level2a>` datasets are the same for all imaging and spectroscopic modes.


.. Level 2b Information

Level 2b Description
--------------------

.. FITS File Description

The IFU dataset is a 2D dataset with axes of spatial and wavelength dimensions.  There will
be N SCI, DQ and ERR HDU tuples in a FITS file.  There will be multiple FITS files, one for
each exposure.


Level 2C Description
--------------------

.. TL;DR

TL;DR
^^^^^
* 2D dataset: spatial, wavelength
* Multiple [SCI, WHT, CTX] tuples in a single FITS file
* Each exposure will be in a separate FITS file


.. FITS File Description

FITS File Description
^^^^^^^^^^^^^^^^^^^^^

The WFSS dataset is a 2D dataset with axes of spatial and wavelength dimensions.  There will
be a SCI, WHT, CTX HDU.

There will be a FITS file for *each* exposure.

Level 3 Description
-------------------

The Level 3 WFSS dataset will be the same data format as in the Level 2c. Each will be 2D and the data
will be ordered by spatial dimension first and then by wavelength.

