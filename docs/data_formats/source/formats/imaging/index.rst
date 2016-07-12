.. _data-imaging:

Imaging
=======

Modes used by this imaging definition: :ref:`FGS Imaging <fgs-imaging>`, :ref:`MIRI Imaging <miri-imaging>`,
:ref:`NIRCAM Imaging <nircam-imaging>`, and :ref:`NIRISS Imaging <niriss-imaging>`.


:ref:`Level 1 <level1>` and :ref:`Level 2a <level2a>` datasets are the same for all imaging and spectroscopic modes.


.. _imaging-level2b

Level 2b Description
--------------------

.. FITS File Format

The imaging FITS file will contain an SCI, DQ and ERR set of HDUs. Each will be 2D and with axes that represent
spatial dimensions.


.. _imaging-level2c

Level 2c Description
--------------------

The imaginge FITS file will contain an SCI, WHT and CTX set of HDUs. Each will be 2D with axes that represent the
spatial dimensions and they will have the same as the FITS file in :ref:`Imaging Level 2b <imaging-level2b>`.