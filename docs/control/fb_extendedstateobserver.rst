.. _fb_extendedstateobserver:

FB_ExtendedStateObserver (Function Block)
=========================================

Estimates the process output and total disturbance for use in an Active
Disturbance Rejection Controller (ADRC).

The observer tracks two states:

- ``Z1`` estimate of the process output.
- ``Z2`` estimate of the total disturbance, including unmodelled dynamics,
  nonlinearities, and external disturbances.

The observer gain is derived from :attr:`Wo` and :attr:`b0`. A higher :attr:`Wo`
tracks disturbances faster but amplifies sensor noise.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fWo` and :attr:`fB0` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_ExtendedStateObserver EXTENDS FB_SoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_fWo      : LREAL; // Observer bandwidth in rad/s.
   	_fB0      : LREAL; // Estimated plant gain.
   	_fInputU  : LREAL; // Control signal from the previous cycle.
   	_fInputY  : LREAL; // Measured process output (feedback).
   	_fZ1      : LREAL; // Estimated process output.
   	_fZ2      : LREAL; // Estimated total disturbance.
   END_VAR

Properties
----------

.. _fb_extendedstateobserver.b0:

B0
~~

Type: ``LREAL``

Gets or sets the estimated plant gain (b0).

This is the ratio of how much the output changes per unit of control signal.
For example, if a 10% heater output raises the temperature at 2°C/s, then
``b0 = 0.2``. This does not need to be exact because the observer treats inaccuracies
as part of the disturbance and cancels them.

.. _fb_extendedstateobserver.inputu:

InputU
~~~~~~

Type: ``LREAL``

Gets or sets the control signal from the previous cycle.

Set this to the controller output before calling :meth:`Run`.

.. _fb_extendedstateobserver.inputy:

InputY
~~~~~~

Type: ``LREAL``

Gets or sets the measured process output.

Set this to the feedback value before calling :meth:`Run`.

.. _fb_extendedstateobserver.wo:

Wo
~~

Type: ``LREAL``

Gets or sets the observer bandwidth in rad/s.

Controls how quickly the observer tracks the process output and disturbances.
Typically set to 3–10 times :attr:`~FB_ADRC.Wc`. A value of ``10`` means the
observer reacts roughly 10 times faster than the controller.

Too high amplifies sensor noise and risks numerical instability, for a 10ms
task cycle, keep ``Wo`` below 100 rad/s. Too low and disturbances are not
rejected fast enough.

.. _fb_extendedstateobserver.z1:

Z1
~~

Type: ``LREAL``

Gets the estimated process output.

.. _fb_extendedstateobserver.z2:

Z2
~~

Type: ``LREAL``

Gets the estimated total disturbance.

A large value indicates significant unmodelled dynamics or external disturbance acting on the process.

Methods
-------

.. _fb_extendedstateobserver.fb_init:

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
   * - ``fWo``
     - ``LREAL;``
     - Observer bandwidth in rad/s.
   * - ``fB0``
     - ``LREAL;``
     - Estimated plant gain.


.. _fb_extendedstateobserver.reset:

Reset
~~~~~

Clears the observer state. Z1 and Z2 are set to zero.

.. _fb_extendedstateobserver.run:

Run
~~~

Advances the observer by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If the measured cycle
   time is zero the method returns early without updating the state.

   Uses Forward Euler discretisation. For stability, ensure :attr:`Wo` satisfies
   ``Wo * T < 1`` where ``T`` is the task cycle time in seconds. For a 10ms task,
   ``Wo`` should not exceed 100 rad/s.
