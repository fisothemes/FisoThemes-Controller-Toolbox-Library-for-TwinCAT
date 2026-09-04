.. _fb_ladrc:

FB_LADRC (Function Block)
=========================

Linear Active Disturbance Rejection Controller (LADRC) with integral action.

An alternative to PID control that actively estimates and cancels disturbances,
unmodelled dynamics, and plant nonlinearities in real time using an Extended
State Observer (ESO). The integral term eliminates steady-state offset.

Tuning procedure:

1. Estimate :attr:`B0` from a step test by applying a known control output and
   measuring the initial rate of change of the process variable.
2. Set :attr:`Wc` to roughly the desired closed-loop bandwidth. For a process
   that should settle in 10 seconds, start with ``Wc = 0.5`` rad/s.
3. Set :attr:`Wo` to 3–5 times :attr:`Wc` and increase if disturbance rejection
   is too slow.
4. By default :attr:`AutoTn` is ``FALSE``, when it is ``TRUE``, the integral action time is derived
   automatically as :math:`T_n = 1 / \omega_c^2`. Set :attr:`AutoTn` to ``FALSE``
   and tune :attr:`Tn` manually if the automatic value causes overshoot or instability.
   ``LTIME#0`` disables integral action entirely.

In :attr:`~E_ControllerMode.Manual` mode the output tracks :attr:`Setpoint`
directly through the output clamp. The observer and integrator continue running
in manual mode so switching to :attr:`~E_ControllerMode.Auto` produces no jump
in output.

.. note::
   Set :attr:`Maximum` before :attr:`Minimum` to ensure the clamp guard applies
   correctly. The same applies to :attr:`IntegratorBounds`.

   Uses Forward Euler discretisation. For stability ensure ``Wo \* T < 1`` where
   ``T`` is the task cycle time in seconds.

   Use ``FB_init`` to set :attr:`fWc`, :attr:`fWo`, :attr:`fB0`, :attr:`fMinimum`,
   and :attr:`fMaximum` at declaration time.

**Extends:** :ref:`FB_SoComponent <fb_socomponent>`

Properties
----------

.. _fb_ladrc.autotn:

AutoTn
~~~~~~

Type: ``BOOL``

Gets or sets whether the integral action time is derived automatically.

When ``TRUE`` (default), :attr:`Tn` is computed as :math:`1 / \omega_c^2`.
Set to ``FALSE`` to tune :attr:`Tn` manually if the automatic value causes
overshoot or instability.

.. _fb_ladrc.b0:

B0
~~

Type: ``LREAL``

Gets or sets the estimated plant gain (b0).

This is the ratio of how much the output changes per unit of control signal.
For example, if a 10% heater output raises the temperature at 2°C/s, then
``b0 = 0.2``. This does not need to be exact because the observer treats inaccuracies
as disturbance and cancels them. Must be non-zero.

Sets both the observer and control law gain simultaneously.

.. _fb_ladrc.enable:

Enable
~~~~~~

Type: ``BOOL``

Gets or sets whether the controller is active.

When ``FALSE`` all internal components are reset and the output is held at zero.
Defaults to ``TRUE``.

.. _fb_ladrc.feedback:

Feedback
~~~~~~~~

Type: ``LREAL``

Gets or sets the process variable (PV).

Used by the observer to estimate the process state and total disturbance.

.. _fb_ladrc.integratorbounds:

IntegratorBounds
~~~~~~~~~~~~~~~~

Type: :ref:`I_Bounded <i_bounded>`

Gets the integrator bounds interface.

Use this to set independent upper and lower limits on the integrator output,
separate from the output clamp. Useful when the actuator range differs from
the process range.

.. _fb_ladrc.maximum:

Maximum
~~~~~~~

Type: ``LREAL``

Gets or sets the upper output clamp.

Internally clamped to be greater than or equal to :attr:`Minimum`.
Set this before :attr:`Minimum` to ensure the guard applies correctly.

.. _fb_ladrc.minimum:

Minimum
~~~~~~~

Type: ``LREAL``

Gets or sets the lower output clamp.

Internally clamped to be less than or equal to :attr:`Maximum`.
Set :attr:`Maximum` before this property to ensure the guard applies correctly.

.. _fb_ladrc.mode:

Mode
~~~~

Type: :ref:`E_ControllerMode <e_controllermode>`

Gets or sets the operating mode.

In :attr:`~E_ControllerMode.Auto` mode the output is computed from :attr:`Setpoint`
and :attr:`Feedback`. In :attr:`~E_ControllerMode.Manual` mode the output tracks
:attr:`Setpoint` directly through the output clamp. The observer continues
running in manual mode so switching to auto produces no jump in output.

.. _fb_ladrc.setpoint:

Setpoint
~~~~~~~~

Type: ``LREAL``

Gets or sets the setpoint. 

In :attr:`~E_ControllerMode.Manual` mode this is used as 
the manual output value, routed directly through the output clamp.

.. _fb_ladrc.tn:

Tn
~~

Type: ``LTIME``

Gets or sets the integral action time (Tn).

Only used when :attr:`AutoTn` is ``FALSE``. Controls how aggressively the
integral term corrects steady-state offset. A shorter value eliminates offset
faster but risks overshoot. ``LTIME#0`` disables the integral term entirely.

.. _fb_ladrc.wc:

Wc
~~

Type: ``LREAL``

Gets or sets the controller bandwidth in rad/s.

Controls the speed of the closed-loop response. A higher value gives a faster
response but risks overshoot and noise sensitivity. For a process that should
settle in roughly 10 seconds, start with ``Wc = 0.5`` rad/s and increase gradually.

.. _fb_ladrc.wo:

Wo
~~

Type: ``LREAL``

Gets or sets the observer bandwidth in rad/s.

Controls how quickly disturbances are estimated and rejected. Set to 3–5 times
:attr:`Wc`. For stability ensure ``Wo \* T < 1`` where ``T`` is the task cycle
time in seconds. For a 10ms task, keep ``Wo`` below 100 rad/s.

Methods
-------

.. _fb_ladrc.fb_init:

FB_init
~~~~~~~

**Inputs**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Name
     - Type
     - Description
   * - ``bInitRetains``
     - ``BOOL``
     - if TRUE, the retain variables are initialized (warm start / cold start)
   * - ``bInCopyCode``
     - ``BOOL``
     - if TRUE, the instance afterwards gets moved into the copy code (online change)
   * - ``fB0``
     - ``LREAL``
     - Estimated plant gain.
   * - ``fWc``
     - ``LREAL``
     - Controller bandwidth in rad/s.
   * - ``fWo``
     - ``LREAL``
     - Observer bandwidth in rad/s. Typically 3–5 times Wc.
   * - ``fMaximum``
     - ``LREAL``
     - Upper output clamp.
   * - ``fMinimum``
     - ``LREAL``
     - Lower output clamp.


.. _fb_ladrc.run:

Run
~~~

Advances the ADRC by one time step.

.. note::
   Must be called once per cycle on a single PLC task.
