.. _fb_pid:

FB_PID (Function Block)
=======================

Ideal-form PID controller with clamped output, comparator-based anti-windup,
and bumpless manual-to-auto transfer.

The control output is computed as:

.. math::

   u(t) = K_p \left( e(t) + \frac{1}{T_n} \int e(t)\, dt + T_v \frac{d(-y)}{dt} \right)

where :math:`e(t) = SP - PV` is the error, :math:`-y` is the negated process
variable (derivative on measurement, avoiding derivative kick on setpoint steps).

In :attr:`~E_PIDMode.Manual` mode the output tracks :attr:`Setpoint` directly
through the output clamp. The integrator is continuously primed so that
switching to :attr:`~E_PIDMode.Auto` produces no jump in output.

.. note::
   Set :attr:`Maximum` before :attr:`Minimum` to ensure the clamp guard applies
   correctly. The same applies to :attr:`IntegratorBounds`.

   Use ``FB_init`` to set :attr:`fKp`, :attr:`tTn`, :attr:`tTv` and :attr:`tTd`,
   :attr:`fMaximum`, and :attr:`fMinimum` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_PID EXTENDS FB_SoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable, I_Bounded
   VAR
   	_fSetpoint  : LREAL; // Setpoint (SP).
   	_fFeedback  : LREAL; // Process variable (PV).
   	_fError     : LREAL; // Current error (SP - PV).
   	_bEnable	: BOOL := TRUE;
   	_eMode      : E_ControllerMode := E_ControllerMode.Auto; // Operating mode. Auto or Manual.
   	_fbClamp    : FB_Clamp(
   					fMaximum := FsCommon.GVL_TypeValueLimits.LREAL_MAX, 
   					fMinimum := FsCommon.GVL_TypeValueLimits.LREAL_MIN); // Bounds of the controller's Output.
   	_fbP        : FB_ProportionalGain(fKp := 2.0); // P Component.
   	_fbI        : FB_ClampingIntegrator(tTn := LTIME#0S, eMode := E_AntiWindupMode.Hold); // I Component.
   	_fbD        : FB_Differentiator(tTv := LTIME#0S, tTd := LTIME#200MS); // D Components.
   END_VAR

Properties
----------

.. _fb_pid.antiwindupactive:

AntiWindupActive
~~~~~~~~~~~~~~~~

Type: ``BOOL``

Gets whether the integrator is currently saturated and integration is halted or disabled.

.. _fb_pid.antiwindupmode:

AntiWindupMode
~~~~~~~~~~~~~~

Type: ``E_AntiWindupMode``

Gets or sets the anti-windup mode for the integrator.

See :class:`E_AntiWindupMode` for available modes.

.. _fb_pid.enable:

Enable
~~~~~~

Type: ``BOOL``

Gets or sets whether the controller is active.

When ``FALSE`` all internal components are reset and the output is held at zero.
The controller resumes from a clean state when re-enabled. Defaults to ``TRUE``.

.. _fb_pid.error:

Error
~~~~~

Type: ``LREAL``

Gets the current error (Setpoint - Feedback, SP - PV).

.. _fb_pid.feedback:

Feedback
~~~~~~~~

Type: ``LREAL``

Gets or sets the process variable (PV). 

Used to compute the error and the derivative on measurement.

.. _fb_pid.integratorbounds:

IntegratorBounds
~~~~~~~~~~~~~~~~

Type: ``I_Bounded``

Gets the integrator bounds interface.

Use this to set independent upper and lower limits on the integrator output,
separate from the output clamp. This is useful when you want tighter integrator 
limits than the output clamp.

.. _fb_pid.kp:

Kp
~~

Type: ``LREAL``

Gets or sets the proportional gain (Kp).

Scales the response to the current error. A higher value reacts more strongly
to error but risks overshoot and oscillation. A value of 0 disables the P term.

.. _fb_pid.maximum:

Maximum
~~~~~~~

Type: ``LREAL``

Gets or sets the upper output clamp.

Internally clamped to be greater than or equal to :attr:`Minimum`.
Set this before :attr:`Minimum` to ensure the guard applies correctly.

.. _fb_pid.minimum:

Minimum
~~~~~~~

Type: ``LREAL``

Gets or sets the lower output clamp.

Internally clamped to be less than or equal to :attr:`Maximum`.
Set :attr:`Maximum` before this property to ensure the guard applies correctly.

.. _fb_pid.mode:

Mode
~~~~

Type: ``E_ControllerMode``

Gets or sets the operating mode.

In :attr:`~E_PIDMode.Auto` mode the output is computed from :attr:`Setpoint` and
:attr:`Feedback`. In :attr:`~E_ControllerMode.Manual` mode the output tracks
:attr:`Setpoint` directly through the output clamp. The integrator is continuously
primed in manual mode so switching to auto produces no jump in output.

.. _fb_pid.setpoint:

Setpoint
~~~~~~~~

Type: ``LREAL``

Gets or sets the setpoint. 

In :attr:`~E_ControllerMode.Manual` mode this is used as 
the manual output value, routed directly through the output clamp.

.. _fb_pid.td:

Td
~~

Type: ``LTIME``

Gets or sets the derivative damping time (Td).

Filters the derivative signal to reduce sensitivity to measurement noise.
A longer value gives more filtering but weakens derivative action. ``LTIME#0``
removes the filter entirely, not recommended when the measurement is noisy.

.. _fb_pid.tn:

Tn
~~

Type: ``LTIME``

Gets or sets the integral action time (Tn).

Controls how quickly accumulated error is corrected. A shorter value eliminates
steady-state error, faster but risks overshoot. A longer value is more stable but
slower to correct. ``LTIME#0`` disables the I term entirely.

.. _fb_pid.tv:

Tv
~~

Type: ``LTIME``

Gets or sets the derivative action time (Tv).

Controls how strongly the controller reacts to changes in the process variable (Feedback).
A longer value dampens sudden changes and reduces overshoot, but too much can
cause instability. ``LTIME#0`` disables the D term entirely.

Methods
-------

.. _fb_pid.fb_init:

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
   * - ``fKp``
     - ``LREAL;``
     - Proportional gain.
   * - ``tTn``
     - ``LTIME;``
     - Integral action time. LTIME#0 disables the I term.
   * - ``tTv``
     - ``LTIME;``
     - Rate time. LTIME#0 disables the D term.
   * - ``tTd``
     - ``LTIME;``
     - Derivative damping time.
   * - ``fMaximum``
     - ``LREAL;``
     - Upper output clamp.
   * - ``fMinimum``
     - ``LREAL;``
     - Lower output clamp.


.. _fb_pid.reset:

Reset
~~~~~

Resets all internal components and sets the output to zero.

.. _fb_pid.run:

Run
~~~

Advances the PID controller by one time step.

.. note::
   Must be called once per cycle on a single PLC task.

.. _fb_pid.synctn:

SyncTn
~~~~~~

Presets the integrator state to match a given output value on the next :meth:`Run` call.

Use this when switching from manual to automatic mode with a known starting output,
or when initialising the controller to a steady-state value to avoid an initial transient.

**Parameters**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Name
     - Type
     - Description
   * - ``fValue``
     - ``LREAL;``
     - Target integrator state.

