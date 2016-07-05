.. JWST Data Document documentation master file, created by
   sphinx-quickstart on Tue Jul  5 11:31:55 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to JWST Data Document's documentation!
==============================================

Contents:

.. toctree::
   :maxdepth: 3
   :numbered:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



Instruments and Modes
=====================


Fine Guidance System
--------------------


.. _fgs-imaging:

Imaging / Science
+++++++++++++++++
Corresponding data format: :ref:`Imaging Data <data-imaging>`


.. _fgs-guiding:

Guiding
+++++++
Corresponding data format: :ref:`Guiding Data <data-guiding>`



MIRI
----


.. _miri-imaging:

Imaging
+++++++
Corresponding data format: :ref:`Imaging Data <data-imaging>`


.. _miri-lrs:

Low Resolution Spectroscopy (LRS)
+++++++++++++++++++++++++++++++++

.. _miri-lrs-fixed-slit:

* Fixed Slit

Corresponding data format: :ref:`Fixed Slit Data <data-fss>`

.. _miri-lrs-slitless:

* Slitless

.. _miri-lrs-slitless-standard:

** Standard

Corresponding data format: :ref:`SOSS Data <data-soss>`


.. _miri-lrs-slitless-timeseries:

** Time Series

Corresponding data format: :ref:`SOSS Timeseries Data <data-soss-ts>`


.. _miri-mrs:

Medium Resolution Spectroscopy (MRS, IFU)
+++++++++++++++++++++++++++++++++++++++++

Corresponding data format: :ref:`IFU Data <data-ifu>`


.. _miri-coronagraphy:

Coronagraphy
++++++++++++
Corresponding data format: :ref:`Coronagraphy Data <data-coronagraphy>`


NIRCAM
------

.. _nircam-imaging:

Imaging
+++++++
Corresponding data format: :ref:`Imaging Data <data-imaging>`


.. _nircam-wfss:

Wide Field Slitless Spectroscopy (WFSS)
+++++++++++++++++++++++++++++++++++++++
Corresponding data format: :ref:`WFSS Data <data-wfss>`


.. _nircam-coronagraphy:

Coronagraphy
++++++++++++
Corresponding data format: :ref:`Coronagraphy Data <data-coronagraphy>`


NIRISS
------


.. _niriss-imaging:

Imaging
+++++++
Corresponding data format: :ref:`Imaging Data <data-imaging>`


.. _niriss-soss:

Single Object Slitless Spectroscopy (SOSS)
++++++++++++++++++++++++++++++++++++++++++

.. _niriss-soss-standard:

* Standard

Corresponding data format: :ref:`SOSS Data <data-soss>`


.. _niriss-soss-timeseries:

* Time Series

Corresponding data format: :ref:`SOSS Timeseries Data <data-soss-ts>`


.. _niriss-wfss:

Wide Field Slitless (WFSS)
++++++++++++++++++++++++++
Corresponding data format: :ref:`WFSS Data <data-wfss>`


.. _niriss-ami:

Aperture Masking Interferometry (AMI)
+++++++++++++++++++++++++++++++++++++
Corresponding data format: :ref:`AMI Data <data-ami>`


NIRSPEC
-------

.. _nirspec-fs:

Fixed Slit Spectroscopy (FS)
++++++++++++++++++++++++++++
Corresponding data format: :ref:`Fixed Slit Data <data-fss>`


.. _nirspec-mos:

Multi-Object Spectroscopy (MOS)
+++++++++++++++++++++++++++++++
Corresponding data format: :ref:`Fixed Slit Data <data-fss>`


.. _nirspec-ifu:

Interferometer Field Unit
+++++++++++++++++++++++++
Corresponding data format: :ref:`IFU Data <data-ifu>`



Levels
======

Level 1
-------

Level 2a
--------

Level 2b
--------


.. _data-imaging:

Imaging
+++++++

Modes used by this imaging definition: :ref:`FGS Imaging <fgs-imaging>`, :ref:`MIRI Imaging <miri-imaging>`,
:ref:`MIRI Imaging <nircam-imaging>`, and :ref:`NIRISS Imaging <niriss-imaging>`.

.. _data-ifu:

Interferometer Field Unit
+++++++++++++++++++++++++

Modes used by this definition: :ref:`NIRSPEC IFU <nirspec-ifu>`, :ref:`MIRI Medium Resolution Spectroscopy <miri-mrs>`.


.. _data-coronagraphy:

Coronagraphy
++++++++++++

Modes used by this definition: :ref:`MIRI Coronagraphy <miri-coronagraphy>`, :ref:`NIRSPEC Coronagraphy <nircam-coronagraphy>`.

.. _data-wfss:

Wide Field Slitless Spectroscopy
++++++++++++++++++++++++++++++++

Modes used by this definition: :ref:`NIRCAM WFS <nircam-wfss>`, :ref:`NIRISS WFS <niriss-wfss>`.

.. _data-soss:

Single Object Slitless Spectroscopy
+++++++++++++++++++++++++++++++++++

Modes used by this definition: :ref:`MIRI Low Resolution Slitless Spectroscopy <miri-lrs-slitless-standard>` and
:ref:`NIRISS Single Object Slitless Specroscopy <niriss-soss-standard>`.

.. _data-soss-ts:

Single Object Slitless Spectroscopy Time Series
+++++++++++++++++++++++++++++++++++++++++++++++

Modes used by this definition: :ref:`MIRI Low Resolution Slitless Spectroscopy Time Series <miri-lrs-slitless-timeseries>` and
:ref:`NIRISS Single Object Slitless Specroscopy Time Series <niriss-soss-timeseries>`.


.. _data-guiding:

FGS Guiding
+++++++++++

Modes used by this imaging definition: :ref:`FGS Guiding <fgs-guiding>`

.. _data-ami:

Aperature Masking Interferometry
++++++++++++++++++++++++++++++++

Modes used by this imaging definition: :ref:`NIRISS AMI <niriss-ami>`.

.. _data-fss:

Fixed Slit Spectroscopy
+++++++++++++++++++++++

Modes used by this imaging definition: :ref:`MIRI Fixed Slit Low Resolution Spectroscopy <miri-lrs-fixed-slit>`,
:ref:`NIRSPEC Fixed Slit Spectroscopy <nirspec-fs>`, and :ref:`NIRSPEC Multi-Object Spectroscopy <nirspec-mos>`
