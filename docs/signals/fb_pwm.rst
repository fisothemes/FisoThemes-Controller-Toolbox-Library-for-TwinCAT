.. _fb_pwm:

FB_PWM (Function Block)
=======================

Generates a pulse-width modulated (PWM) signal.

The output switches between ``Amplitude`` and ``0`` at a fixed :attr:`Period`.
:attr:`DutyCycle` controls the proportion of the period the output is high,
as a value between -1 and 1.

For example, a duty cycle of 0.3 produces a high output for 30% of the period
and a low output for the remaining 70%. A duty cycle of -0.3 inverts this,
producing a low output for 30% and a high output for 70%.

A duty cycle of 0 keeps the output permanently low. A duty cycle of ±1 keeps
it permanently high.

:attr:`Phase` shifts the wave horizontally in radians. Negative values shift
in the opposite direction.
:attr:`Bias` shifts the output vertically.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`tPeriod`, :attr:`fAmplitude`, :attr:`fBias`,
   and :attr:`fDutyCycle` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_PWM EXTENDS FB_PeriodicSignal
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_fDutyCycle : LREAL; // Proportion of the period the output is high. Clamped to -1..1. Negative values invert the wave.
   	_bIsHigh    : BOOL;  // TRUE when the output is in its high state, regardless of amplitude, bias, or phase.
   	_tTime      : LTIME;
   END_VAR

Properties
----------

.. _fb_pwm.dutycycle:

DutyCycle
~~~~~~~~~

Type: ``LREAL``

Gets or sets the duty cycle as a value between -1 and 1.

This controls the proportion of the period the output is high. A value of 0.3
keeps the output high for 30% of the period. A negative value inverts the wave —
-0.3 keeps the output low for 30% and high for the remaining 70%. Values outside
-1..1 are clamped. Changes take effect immediately.

.. _fb_pwm.ishigh:

IsHigh
~~~~~~

Type: ``BOOL``

Gets whether the output is currently in its high state.

TRUE regardless of the values of :attr:`Amplitude`, :attr:`Bias`, or :attr:`Phase`.

Methods
-------

.. _fb_pwm.fb_init:

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
     - High-state output level. Low state is always 0.
   * - ``fBias``
     - ``LREAL;``
     - Shifts the output vertically.
   * - ``fDutyCycle``
     - ``LREAL;``
     - Proportion of the period the output is high. Clamped to -1..1.


.. _fb_pwm.reset:

Reset
~~~~~

Restarts the wave from the beginning by resetting the accumulated time to zero.
The duty cycle, phase, amplitude, and bias are unaffected.

.. _fb_pwm.run:

Run
~~~

Advances the PWM signal by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If the measured cycle
   time is zero or :attr:`Period` is zero, the method returns early without
   updating the output.
