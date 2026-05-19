.. _fb_ramp:

FB_Ramp (Function Block)
========================

Generates a ramp signal that rises or falls at a fixed rate indefinitely.

The output starts at :attr:`StartValue` and advances at :attr:`Rate` units per second.
A positive rate produces a rising ramp, a negative rate a falling ramp.
Changing :attr:`Rate` mid-run takes effect immediately.

Calling :meth:`Reset` returns the output to :attr:`StartValue`.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fStartValue` and :attr:`fRate` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_Ramp EXTENDS FB_SoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_fStartValue : LREAL; // Initial output value. Restored on Reset.
   	_fRate       : LREAL; // Rate of change in units per second. Negative values produce a falling ramp.
   END_VAR

Properties
----------

.. _fb_ramp.rate:

Rate
~~~~

Type: ``LREAL``

Gets or sets the rate of change in units per second.

A positive value produces a rising ramp, a negative value a falling ramp.
Changes take effect immediately.

.. _fb_ramp.startvalue:

StartValue
~~~~~~~~~~

Type: ``LREAL``

Gets or sets the start value.

This is the output value the ramp returns to after a :meth:`Reset`.

Methods
-------

.. _fb_ramp.fb_init:

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
   * - ``fStartValue``
     - ``LREAL;``
     - Initial output value.
   * - ``fRate``
     - ``LREAL;``
     - Rate of change in units per second. Negative values produce a falling ramp.


.. _fb_ramp.reset:

Reset
~~~~~

Resets the output to the start value set in ``FB_init``. The rate is unaffected.

.. _fb_ramp.run:

Run
~~~

Advances the ramp by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If the measured cycle
   time is zero the method returns early without updating the output.
