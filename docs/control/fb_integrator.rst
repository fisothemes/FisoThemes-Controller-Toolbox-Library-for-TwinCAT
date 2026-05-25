.. _fb_integrator:

FB_Integrator (Function Block)
==============================

Integrates the input error signal over time.

The output accumulates the input scaled by the integral gain :math:`K_i = 1 / T_n`,
and is clamped to [:attr:`Minimum`, :attr:`Maximum`] on every cycle.
Setting :attr:`Tn` to ``LTIME#0`` disables integration, setting the output to zero.

Use :meth:`Sync` to preset the integrator state for bumpless transfer when
switching from manual to automatic mode.

.. note::
   Set :attr:`Maximum` before :attr:`Minimum` to ensure the clamp guard applies
   correctly.

   Use ``FB_init`` to set :attr:`tTn` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FB_Integrator EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable, I_Bounded
   VAR
   	_tTn   		: LTIME; // Integral action time (Tn).
   	_bSync 		: BOOL;  // Triggers a bumpless transfer on the next Run call.
   	_fSync 		: LREAL; // Target integrator state for bumpless transfer.
   	_fMaximum   : LREAL := FsCommon.GVL_TypeValueLimits.LREAL_MAX; // Upper output clamp. Clamped to >= Minimum.
   	_fMinimum   : LREAL := FsCommon.GVL_TypeValueLimits.LREAL_MIN; // Lower output clamp. Clamped to <= Maximum.
   END_VAR

Properties
----------

.. _fb_integrator.maximum:

Maximum
~~~~~~~

Type: ``LREAL``

Gets or sets the upper output clamp.

Internally clamped to be greater than or equal to :attr:`Minimum`.
Set this before :attr:`Minimum` to ensure the guard applies correctly.

.. _fb_integrator.minimum:

Minimum
~~~~~~~

Type: ``LREAL``

Gets or sets the lower output clamp.

Internally clamped to be less than or equal to :attr:`Maximum`.
Set :attr:`Maximum` before this property to ensure the guard applies correctly.

.. _fb_integrator.tn:

Tn
~~

Type: ``LTIME``

Gets or sets the integral action time (Tn).

This controls how aggressively the integrator responds to sustained error.
A shorter value increases integral action. Setting it to ``LTIME#0`` disables
integration entirely, setting the output to zero.

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


.. _fb_integrator.reset:

Reset
~~~~~

Clears the integrator state and output.

.. _fb_integrator.run:

Run
~~~

Advances the integrator by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If :attr:`Tn` is
   ``LTIME#0`` the output is set to zero.

.. _fb_integrator.sync:

Sync
~~~~

Forces the integrator state to a given value on the next :meth:`Run` call.

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

