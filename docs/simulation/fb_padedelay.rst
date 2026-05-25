.. _fb_padedelay:

FB_PadeDelay (Function Block)
=============================

Approximates a transport delay (dead time) using a second-order Padé approximation.

The continuous-time transfer function is:

.. math::

   G(s) = \frac{1 - \frac{L}{2}s + \frac{L^2}{12}s^2}{1 + \frac{L}{2}s + \frac{L^2}{12}s^2}

where :math:`L` is :attr:`DelayTime` in seconds. The approximation is discretised
using the Tustin (bilinear) method with frequency pre-warping.

The output initially moves in the opposite direction to the input before settling
at the correct delayed value. This is a known characteristic of Padé approximations
and not a bug.

A delay of ``LTIME#0`` passes the input through unchanged.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`tDelayTime` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_PadeDelay EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_tDelayTime : LTIME; // Approximate transport delay (L).
   	_fY1        : LREAL; // y[k-1]
   	_fY2        : LREAL; // y[k-2]
   	_fU1        : LREAL; // u[k-1]
   	_fU2        : LREAL; // u[k-2]
   END_VAR

Properties
----------

.. _fb_padedelay.delaytime:

DelayTime
~~~~~~~~~

Type: ``LTIME``

Gets or sets the approximate transport delay.

This is the time between a change in the input and when that change appears
at the output. Longer values produce a more sluggish, harder-to-control process.
A value of ``LTIME#0`` passes the input through unchanged.

Note that the Padé approximation causes the output to initially move in the
opposite direction to the input. This effect is more pronounced for longer
delays relative to the cycle time.

Methods
-------

.. _fb_padedelay.fb_init:

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
   * - ``tDelayTime``
     - ``LTIME;``
     - Approximate transport delay.


.. _fb_padedelay.reset:

Reset
~~~~~

Clears all internal state, returning the delay approximation to its initial conditions.

.. _fb_padedelay.run:

Run
~~~

Advances the Padé delay by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If the measured cycle
   time is zero or :attr:`DelayTime` is ``LTIME#0`` the input passes through
   unchanged.
