.. _fb_integrator:

FB_Integrator (Function Block)
==============================

Integrates the input error signal over time.

The output accumulates the input scaled by the integral gain :math:`K_i = 1 / T_n`,
and is clamped to [:attr:`Minimum`, :attr:`Maximum`] on every cycle. Two anti-windup
strategies are available via :attr:`AntiWindupMethod`.

Setting :attr:`Tn` to ``LTIME#0`` disables integration, holding the output at
its current integrator state.

.. note::
   Set :attr:`Maximum` before :attr:`Minimum` to ensure the clamp is applied
   correctly. Setting :attr:`Minimum` first may cause it to be clamped against
   an uninitialised :attr:`Maximum`.

   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`tTn`, :attr:`fMaximum`, :attr:`fMinimum`,
   :attr:`eAntiWindupMethod`, and :attr:`tTrackingTimeConstant` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_Integrator EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_tTn                   : LTIME; // Integral action time (Tn).
   	_fMaximum              : LREAL :=  FsCommon.GVL_TypeValueLimits.LREAL_MAX; // Upper output clamp.
   	_fMinimum              : LREAL :=  FsCommon.GVL_TypeValueLimits.LREAL_MIN; // Lower output clamp.
   	_eAntiWindupMethod     : E_AntiWindupMethod; // Anti-windup strategy.
   	_tTrackingTimeConstant : LTIME; // Tracking time constant (Tt) for back-calculation anti-windup.
   	_fIntegratorState      : LREAL; // Internal integrator accumulator.
   	_bAntiWindupActive     : BOOL;  // TRUE when the output is saturated and anti-windup is limiting integration.
   	_bSync                 : BOOL;  // Triggers a bumpless transfer on the next Run call.
   	_fSync                 : LREAL; // Target integrator state for bumpless transfer.
   END_VAR

Properties
----------

.. _fb_integrator.antiwindupactive:

AntiWindupActive
~~~~~~~~~~~~~~~~

Type: ``BOOL``

Gets whether the output is currently saturated and anti-windup is actively limiting integration.

.. _fb_integrator.antiwindupmethod:

AntiWindupMethod
~~~~~~~~~~~~~~~~

Type: ``E_AntiWindupMethod``

Gets or sets the anti-windup strategy.

:attr:`~E_AntiWindupMethod.Clamping` halts integration when the output is
saturated. :attr:`~E_AntiWindupMethod.BackCalculation` feeds the saturation
error back into the integrator gradually, which is better suited to slow
systems with significant lag such as thermal processes.

.. _fb_integrator.maximum:

Maximum
~~~~~~~

Type: ``LREAL``

Gets or sets the upper output clamp.

The output is clamped to this value on every cycle. Internally clamped to be
greater than or equal to :attr:`Minimum`. Set this before :attr:`Minimum` to
ensure the guard applies correctly.

.. _fb_integrator.minimum:

Minimum
~~~~~~~

Type: ``LREAL``

Gets or sets the lower output clamp.

The output is clamped to this value on every cycle. Internally clamped to be
less than or equal to :attr:`Maximum`. Set :attr:`Maximum` before this property
to ensure the guard applies correctly.

.. _fb_integrator.tn:

Tn
~~

Type: ``LTIME``

Gets or sets the integral action time (Tn).

This controls how aggressively the integrator responds to sustained error.
A shorter value increases integral action. Setting it to ``LTIME#0`` disables
integration entirely, holding the output at the current integrator state.

.. _fb_integrator.trackingtimeconstant:

TrackingTimeConstant
~~~~~~~~~~~~~~~~~~~~

Type: ``LTIME``

Gets or sets the tracking time constant (Tt) for back-calculation anti-windup.

This controls how quickly the integrator unwinds after saturation. A typical
starting value is ``SQRT(Tn * Td)``. Setting it to ``LTIME#0`` disables the
back-calculation correction. Ignored when :attr:`AntiWindupMethod` is
:attr:`~E_AntiWindupMethod.Clamping`.

Methods
-------

.. _fb_integrator.fb_init:

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
   * - ``tTn``
     - ``LTIME;``
     - Integral action time. LTIME#0 disables integration.
   * - ``fMaximum``
     - ``LREAL;``
     - Upper output clamp.
   * - ``fMinimum``
     - ``LREAL;``
     - Lower output clamp.
   * - ``eAntiWindupMethod``
     - ``E_AntiWindupMethod;``
     - Anti-windup strategy.
   * - ``tTrackingTimeConstant``
     - ``LTIME;``
     - Tracking time constant for back-calculation anti-windup.


.. _fb_integrator.reset:

Reset
~~~~~

Clears the integrator state, output, and anti-windup flag.

.. _fb_integrator.run:

Run
~~~

Advances the integrator by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If :attr:`Tn` is
   ``LTIME#0`` the output is held at the current integrator state without
   further integration.

.. _fb_integrator.sync:

Sync
~~~~

Forces the integrator state to a given value on the next :meth:`Run` call.

The value is clamped to [:attr:`Minimum`, :attr:`Maximum`] before being applied.
Use this for bumpless transfer when switching from manual to automatic mode,
to prevent a sudden jump in output.

**Parameters**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Name
     - Type
     - Description
   * - ``fValue``
     - ``LREAL``
     -

