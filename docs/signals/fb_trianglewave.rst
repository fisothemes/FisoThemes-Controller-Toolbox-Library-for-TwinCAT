.. _fb_trianglewave:

FB_TriangleWave (Function Block)
================================

Generates a triangle wave signal.

The output rises linearly from ``-Amplitude`` to ``+Amplitude`` over the first
half-cycle, then falls back to ``-Amplitude`` over the second half. :attr:`Bias`
shifts the output vertically.

:attr:`Phase` shifts the wave horizontally in radians. A phase of π starts the
wave at its peak rather than its trough.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`tPeriod`, :attr:`fAmplitude`, :attr:`fBias`,
   and :attr:`fPhase` at declaration time.

**Extends:** :ref:`FB_PeriodicSignal <fb_periodicsignal>`

Methods
-------

.. _fb_trianglewave.fb_init:

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
   * - ``tPeriod``
     - ``LTIME``
     - Duration of one full cycle.
   * - ``fAmplitude``
     - ``LREAL``
     - Scales the wave. Output swings between Bias ± Amplitude.
   * - ``fBias``
     - ``LREAL``
     - Shifts the output vertically.
   * - ``fPhase``
     - ``LREAL``
     - Phase offset in radians. Shifts the wave horizontally.


.. _fb_trianglewave.reset:

Reset
~~~~~

Restarts the wave from the beginning by resetting the accumulated time to zero. The phase, amplitude, and bias are unaffected.

.. _fb_trianglewave.run:

Run
~~~

Advances the triangle wave by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If the measured cycle
   time is zero or :attr:`Period` is zero, the method returns early without
   updating the output.
