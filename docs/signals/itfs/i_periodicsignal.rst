.. _i_periodicsignal:

I_PeriodicSignal (Interface)
============================

Base interface for periodic signal generators.

Implementors produce a cyclic output defined by :attr:`Period`, :attr:`Amplitude`,
:attr:`Bias`, and :attr:`Phase`.

.. code-block:: none

   INTERFACE I_PeriodicSignal EXTENDS I_SoComponent

Properties
----------

.. _i_periodicsignal.amplitude:

Amplitude
~~~~~~~~~

Type: ``LREAL``

Gets or sets the amplitude. 

The output swings between ``Bias + Amplitude`` and ``Bias - Amplitude``.

.. _i_periodicsignal.bias:

Bias
~~~~

Type: ``LREAL``

Gets or sets the bias.

This is a fixed offset added to the output, shifting the wave up or down.

.. _i_periodicsignal.period:

Period
~~~~~~

Type: ``LTIME``

Gets or sets the period. 

This is the time taken to complete one full cycle.

.. _i_periodicsignal.phase:

Phase
~~~~~

Type: ``LREAL``

Gets or sets the phase offset in radians.

This shifts the wave horizontally. Negative values shift in the opposite direction.
