.. _fb_squarewave:

FB_SquareWave (Function Block)
==============================

Generates a square wave signal.

The raw wave alternates between ``+1`` and ``-1`` over one period. :attr:`Amplitude`
scales the wave and :attr:`Bias` shifts it vertically, giving an output that swings
between ``Bias + Amplitude`` and ``Bias - Amplitude``.

:attr:`Phase` shifts the wave horizontally in radians. A phase of π starts the
wave in its low half-cycle, a phase of -π has the same effect.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`tPeriod`, :attr:`fAmplitude`, :attr:`fBias`,
   and :attr:`fPhase` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_SquareWave EXTENDS FB_PeriodicSignal
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_tTime : LTIME; // Accumulated time.
   END_VAR

Methods
-------

.. _fb_squarewave.fb_init:

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
   * - ``tPeriod``
     - ``LTIME;``
     - Duration of one full cycle.
   * - ``fAmplitude``
     - ``LREAL;``
     - Scales the ±1 wave. Output swings between Bias ± Amplitude.
   * - ``fBias``
     - ``LREAL;``
     - Shifts the output up or down by a fixed value.
   * - ``fPhase``
     - ``LREAL;``
     - Phase offset in radians. Shifts the wave horizontally. Negative values shift in the opposite direction.


.. _fb_squarewave.reset:

Reset
~~~~~

Restarts the wave from the beginning by resetting the accumulated time to zero. The phase, amplitude, and bias are unaffected.

.. _fb_squarewave.run:

Run
~~~

Advances the square wave by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If the measured cycle
   time is zero or :attr:`Period` is zero, the method returns early without
   updating the output.
