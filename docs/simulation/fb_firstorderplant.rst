.. _fb_firstorderplant:

FB_FirstOrderPlant (Function Block)
===================================

Simulates a first-order linear plant using Euler's backward (implicit) discretisation.

The continuous-time transfer function is:

.. math::

   G(s) = \frac{K}{\tau s + 1}

which discretises to:

.. math::

   y[k] = \frac{\tau \cdot y[k-1] + K \cdot \Delta t \cdot u[k]}{\tau + \Delta t}

where :math:`K` is :attr:`Gain`, :math:`\tau` is :attr:`Tau` in seconds, and
:math:`\Delta t` is the task cycle time, measured automatically on the first call.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fGain` and :attr:`fTau` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_FirstOrderPlant EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_fGain 	: LREAL; // Steady-state gain (K). Ratio of output to input once the plant has fully settled.
   	_tTau 	: LTIME; // Time constant (τ). Time for the step response to reach 63.2% of its final value.
   END_VAR

Properties
----------

.. _fb_firstorderplant.gain:

Gain
~~~~

Type: ``LREAL``

Gets or sets the steady-state gain.

This is the factor by which a constant input is scaled to produce the output once
the plant has fully settled. For example, a gain of 2 with a constant input of 5
will eventually produce an output of 10.

.. _fb_firstorderplant.tau:

Tau
~~~

Type: ``LTIME``

Gets or sets the time constant (τ).

This controls how quickly the plant responds to a change in input. 
A larger value means a slower response. It is the time taken for the 
output to reach 63.2% of its final value after a step change in input.

Methods
-------

.. _fb_firstorderplant.fb_init:

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
   * - ``fGain``
     - ``LREAL;``
     - Steady-state gain (K). Ratio of output to input once the plant has fully settled.
   * - ``tTau``
     - ``LTIME;``
     - Time constant (τ). Time for the step response to reach 63.2% of its final value.


.. _fb_firstorderplant.reset:

Reset
~~~~~

Sets the output to zero, returning the plant to its initial state.

.. _fb_firstorderplant.run:

Run
~~~

Advances the plant by one time step.

.. note::
   Must be called once per cycle on a single PLC task. This is because on the 
   first call, the cycle time is measured and stored for use in all subsequent calls. 
 
   If the measured cycle time is zero the method returns early without updating 
   the output, guarding against a divide-by-zero.
