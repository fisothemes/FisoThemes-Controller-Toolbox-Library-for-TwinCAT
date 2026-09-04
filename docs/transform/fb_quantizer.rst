.. _fb_quantizer:

FB_Quantizer (Function Block)
=============================

Rounds the input signal to the nearest multiple of :attr:`StepSize`.

Useful for simulating ADC resolution, modelling actuators with discrete
positions, or testing controller behaviour under quantisation.

A :attr:`StepSize` of zero passes the input through unchanged.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fStepSize` at declaration time.

**Extends:** :ref:`FB_SisoComponent <fb_sisocomponent>`

Properties
----------

.. _fb_quantizer.stepsize:

StepSize
~~~~~~~~

Type: ``LREAL``

Gets or sets the quantisation step size.

The output is rounded to the nearest multiple of this value. For example,
a step size of 0.5 rounds the input to the nearest 0.5. A value of zero
passes the input through unchanged.

Methods
-------

.. _fb_quantizer.fb_init:

FB_init
~~~~~~~

**Inputs**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Name
     - Type
     - Description
   * - ``bInitRetains``
     - ``BOOL``
     - if TRUE, the retain variables are initialized (warm start / cold start)
   * - ``bInCopyCode``
     - ``BOOL``
     - if TRUE, the instance afterwards gets moved into the copy code (online change)
   * - ``fStepSize``
     - ``LREAL``
     - Quantisation step size. Zero passes the input through unchanged.


.. _fb_quantizer.run:

Run
~~~

Applies quantisation to the current input.
