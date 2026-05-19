.. _fb_sinewave:

FB_SineWave (Function Block)
============================

Generates a sine wave signal.

The output follows:

.. math::

   y(t) = A \sin\left(\frac{2\pi}{T} t + \phi\right) + B

where :math:`A` is :attr:`Amplitude`, :math:`T` is :attr:`Period` in seconds,
:math:`\phi` is :attr:`Phase` in radians, and :math:`B` is :attr:`Bias`.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`tPeriod`, :attr:`fAmplitude`, :attr:`fBias`,
   and :attr:`fPhase` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_SineWave EXTENDS FB_PeriodicSignal
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_tTime : LTIME;
   END_VAR

Methods
-------

.. _fb_sinewave.fb_init:

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


.. _fb_sinewave.reset:

Reset
~~~~~

Restarts the wave from the beginning by resetting the accumulated time to zero. The phase, amplitude, and bias are unaffected.

.. _fb_sinewave.run:

Run
~~~

Advances the sine wave by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If the measured cycle
   time is zero or :attr:`Period` is zero, the method returns early without
   updating the output.
