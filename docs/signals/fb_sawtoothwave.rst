.. _fb_sawtoothwave:

FB_SawtoothWave (Function Block)
================================

Generates a sawtooth wave signal.

The output rises linearly from ``-Amplitude`` to ``+Amplitude`` over one full
cycle then resets instantly, or falls from ``+Amplitude`` to ``-Amplitude``
depending on :attr:`Direction`. :attr:`Bias` shifts the output vertically.

:attr:`Phase` shifts the wave horizontally in radians. Negative values shift
in the opposite direction.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`tPeriod`, :attr:`fAmplitude`, :attr:`fBias` and
   :attr:`fPhase` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_SawtoothWave EXTENDS FB_PeriodicSignal
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_eDirection : E_RampDirection; // Direction of the sawtooth. Rising goes from -Amplitude to +Amplitude, Falling goes from +Amplitude to -Amplitude.
   	_tTime      : LTIME;
   END_VAR

Properties
----------

.. _fb_sawtoothwave.direction:

Direction
~~~~~~~~~

Type: ``E_RampDirection``

Gets or sets the direction of the sawtooth.

:attr:`~E_RampDirection.Rising` ramps from ``-Amplitude`` to ``+Amplitude``
before resetting. :attr:`~E_RampDirection.Falling` is the inverse.
Changes take effect immediately.

Methods
-------

.. _fb_sawtoothwave.fb_init:

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
     - Scales the wave. Output swings between Bias ± Amplitude.
   * - ``fBias``
     - ``LREAL;``
     - Shifts the output vertically.
   * - ``fPhase``
     - ``LREAL;``
     - Phase offset in radians. Shifts the wave horizontally.


.. _fb_sawtoothwave.reset:

Reset
~~~~~

Restarts the wave from the beginning by resetting the accumulated time to zero. The phase, amplitude, and bias are unaffected.

.. _fb_sawtoothwave.run:

Run
~~~

Advances the sawtooth wave by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If the measured cycle
   time is zero or :attr:`Period` is zero, the method returns early without
   updating the output.
