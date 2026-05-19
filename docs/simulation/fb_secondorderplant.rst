.. _fb_secondorderplant:

FB_SecondOrderPlant (Function Block)
====================================

Simulates a second-order linear plant using the Tustin (bilinear) discretisation
with frequency pre-warping to preserve the natural frequency :attr:`Wn` exactly.

The continuous-time transfer function is:

.. math::

   G(s) = \frac{K \omega_n^2}{s^2 + 2 \zeta \omega_n s + \omega_n^2}

where :math:`K` is :attr:`Gain`, :math:`\omega_n` is :attr:`Wn`, and
:math:`\zeta` is :attr:`Zeta`.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fGain`, :attr:`fWn`, and :attr:`fZeta` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_SecondOrderPlant EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_fGain 	: LREAL; // Steady-state gain (K). Ratio of output to input once the plant has fully settled.
   	_fWn 	: LREAL; // Natural frequency, rad/s), sets how fast the plant responds.
   	_fZeta	: LREAL; // Damping ratio. Less than 1 gives overshoot, 1 is critically damped, greater than 1 is overdamped.
   	_fY1    : LREAL; // y[k-1]
       _fY2    : LREAL; // y[k-2]
       _fU1    : LREAL; // u[k-1]
       _fU2    : LREAL; // u[k-2]
   END_VAR

Properties
----------

.. _fb_secondorderplant.gain:

Gain
~~~~

Type: ``LREAL``

Gets or sets the steady-state gain.

This is the factor by which a constant input is scaled to produce the output once
the plant has fully settled. For example, a gain of 2 with a constant input of 5
will eventually produce an output of 10.

.. _fb_secondorderplant.wn:

Wn
~~

Type: ``LREAL``

Gets or sets the natural frequency in rad/s.

This controls the speed of the plant's response. 
A higher value means a faster response. To convert from Hz, multiply by 2π.

.. _fb_secondorderplant.zeta:

Zeta
~~~~

Type: ``LREAL``

Gets or sets the damping ratio.

This controls the shape of the response.
  - A value below 1 produces an oscillating response that overshoots before settling. 
  - A value of exactly 1 (critically damped) settles as fast as possible without any overshoot.
  - A value above 1 settles more slowly with no overshoot.

Methods
-------

.. _fb_secondorderplant.fb_init:

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
   * - ``fWn``
     - ``LREAL;``
     - Natural frequency in rad/s. Controls how fast the plant responds.
   * - ``fZeta``
     - ``LREAL;``
     - Damping ratio. Less than 1 gives overshoot, 1 is critically damped, greater than 1 is overdamped.


.. _fb_secondorderplant.reset:

Reset
~~~~~

Sets the output and all internal state to zero, returning the plant to its initial conditions.

.. _fb_secondorderplant.run:

Run
~~~

Advances the plant by one time step.

.. note::
   Must be called once per cycle on a single PLC task. This is because on the 
   first call, the cycle time is measured and stored for use in all subsequent calls. 
 
   If the cycle time is zero or :attr:`Wn` is zero, the method returns early 
   without updating the output.
