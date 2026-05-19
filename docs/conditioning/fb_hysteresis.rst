.. _fb_hysteresis:

FB_Hysteresis (Function Block)
==============================

Implements a hysteresis controller with two thresholds and latching behaviour.

The output switches low when the input rises above :attr:`UpperThreshold` and
switches high when the input falls below :attr:`LowerThreshold`. Between the
two thresholds the output latches at its current state.

This convention suits heating applications, the output drives a heater that
turns on when the process falls below the lower threshold and off when it
exceeds the upper threshold.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fUpperThreshold` and :attr:`fLowerThreshold`
   at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_Hysteresis EXTENDS FB_SiComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_fUpperThreshold : LREAL; // Input level above which the output switches low.
   	_fLowerThreshold : LREAL; // Input level below which the output switches high.
   	_bOutput         : BOOL;  // Current output state.
   END_VAR

Properties
----------

.. _fb_hysteresis.lowerthreshold:

LowerThreshold
~~~~~~~~~~~~~~

Type: ``LREAL``

Gets or sets the lower threshold.

When the input falls below this value the output switches high. Must be less
than :attr:`UpperThreshold` for correct operation.

.. _fb_hysteresis.output:

Output
~~~~~~

Type: ``BOOL``

Gets the current output state. 

TRUE when the process is below :attr:`LowerThreshold`.
FALSE when above :attr:`UpperThreshold`.

.. _fb_hysteresis.upperthreshold:

UpperThreshold
~~~~~~~~~~~~~~

Type: ``LREAL``

Gets or sets the upper threshold.

When the input rises above this value the output switches low. Must be greater
than :attr:`LowerThreshold` for correct operation.

Methods
-------

.. _fb_hysteresis.fb_init:

Initialisation
~~~~~~~~~~~~~~

**Parameters**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Name
     - Type
     - Description
   * - ``bInitRetains``
     - ``BOOL;``
     - if TRUE, the retain variables are initialized (warm start / cold start)
   * - ``bInCopyCode``
     - ``BOOL;``
     - if TRUE, the instance afterwards gets moved into the copy code (online change)
   * - ``fUpperThreshold``
     - ``LREAL;``
     - Input level above which the output switches low.
   * - ``fLowerThreshold``
     - ``LREAL;``
     - Input level below which the output switches high.


.. _fb_hysteresis.reset:

Reset
~~~~~

Evaluates the current input against the thresholds and sets the output immediately,
rather than waiting for the input to cross a threshold.

If the input is above :attr:`UpperThreshold` the output is set low. If below
:attr:`LowerThreshold` the output is set high. If between the two thresholds
the output defaults to low as a safe state.

.. _fb_hysteresis.run:

Run
~~~

Evaluates the input against the thresholds and updates the output.
