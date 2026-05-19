.. _fb_periodicsignal:

FB_PeriodicSignal (Function Block)
==================================

Abstract base block for periodic signal generators.

Provides :attr:`Period`, :attr:`Amplitude`, :attr:`Bias`, and :attr:`Phase`
as shared properties for all periodic signal generators. Derived blocks can
implement :meth:`Run` and :meth:`Reset` to produce their specific waveform.

.. note::
   Direct calls to this function block are not permitted (``no_explicit_call``).
   Extend it and call the derived block instead.

.. code-block:: none

   FUNCTION_BLOCK ABSTRACT FB_PeriodicSignal EXTENDS FB_SoComponent
   IMPLEMENTS I_PeriodicSignal
   VAR
   	_tPeriod    : LTIME; // Duration of one full cycle. Must be greater than zero.
   	_fAmplitude : LREAL; // Scales the raw wave. Output swings between Bias ± Amplitude.
   	_fBias      : LREAL; // Shifts the output vertically.
   	_fPhase     : LREAL; // Phase offset in radians. Shifts the wave horizontally.
   END_VAR

Properties
----------

.. _fb_periodicsignal.amplitude:

Amplitude
~~~~~~~~~

Type: ``LREAL``

Gets or sets the amplitude. 

The output swings between ``Bias + Amplitude`` and ``Bias - Amplitude``.

.. _fb_periodicsignal.bias:

Bias
~~~~

Type: ``LREAL``

Gets or sets the bias.

This is a fixed offset added to the output, shifting the wave up or down.

.. _fb_periodicsignal.period:

Period
~~~~~~

Type: ``LTIME``

Gets or sets the period. 

This is the time taken to complete one full cycle.

.. _fb_periodicsignal.phase:

Phase
~~~~~

Type: ``LREAL``

Gets or sets the phase offset in radians.

This shifts the wave horizontally. Negative values shift in the opposite direction.
