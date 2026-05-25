.. _fb_linearstateerrorfeedback:

FB_LinearStateErrorFeedback (Function Block)
============================================

Computes the control output for a Linear Active Disturbance Rejection Controller (LADRC).

The control law is:

.. math::

   u_0 = \omega_c \cdot (SP - z_1) + u_i

   u = \frac{u_0 - z_2}{b_0}

where :math:`u_0` is the error feedback, :math:`u_i` is the integral correction
from an external integrator, :math:`z_2` cancels the estimated disturbance from
:class:`FB_ExtendedStateObserver`, and dividing by :attr:`B0` scales the output
to the plant's input range.

If :attr:`B0` is zero the output is held at zero.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fWc` and :attr:`fB0` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_LinearStateErrorFeedback EXTENDS FB_SoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_fWc       : LREAL; // Controller bandwidth in rad/s.
   	_fB0       : LREAL; // Estimated plant gain.
   	_fSetpoint : LREAL; // Desired process output (SP).
   	_fZ1       : LREAL; // Estimated process output from the observer.
   	_fZ2       : LREAL; // Estimated total disturbance from the observer.
   	_fIntegral : LREAL; // Integral correction from the external integrator.
   END_VAR

Properties
----------

.. _fb_linearstateerrorfeedback.b0:

B0
~~

Type: ``LREAL``

Gets or sets the estimated plant gain (b0).

Must be non-zero. A value of zero disables the control output entirely.
See :attr:`~FB_ADRC.B0` for guidance on how to estimate this value.

.. _fb_linearstateerrorfeedback.integral:

Integral
~~~~~~~~

Type: ``LREAL``

Gets or sets the integral correction.

Set this to the integrator output before calling :meth:`Run`.

.. _fb_linearstateerrorfeedback.setpoint:

Setpoint
~~~~~~~~

Type: ``LREAL``

Gets or sets the setpoint. This is the desired process output.

.. _fb_linearstateerrorfeedback.wc:

Wc
~~

Type: ``LREAL``

Gets or sets the controller bandwidth in rad/s.

Controls how fast the closed loop responds to setpoint changes. A higher value
gives a faster response but risks overshoot and sensitivity to noise. Start with
a low value and increase until the response is satisfactory.

For a process that should settle in roughly 10 seconds, a starting value of
``Wc = 0.5`` rad/s is reasonable.

.. _fb_linearstateerrorfeedback.z1:

Z1
~~

Type: ``LREAL``

Gets or sets the estimated process output from :class:`FB_ExtendedStateObserver`. 

Set this to ``Z1`` before calling :meth:`Run`.

.. _fb_linearstateerrorfeedback.z2:

Z2
~~

Type: ``LREAL``

Gets or sets the estimated total disturbance from :class:`FB_ExtendedStateObserver`. 

Set this to ``Z2`` before calling :meth:`Run`.

Methods
-------

.. _fb_linearstateerrorfeedback.fb_init:

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
   * - ``fWc``
     - ``LREAL;``
     - Controller bandwidth in rad/s.
   * - ``fB0``
     - ``LREAL;``
     - Estimated plant gain.


.. _fb_linearstateerrorfeedback.reset:

Reset
~~~~~

Sets the output to zero.

.. _fb_linearstateerrorfeedback.run:

Run
~~~

Computes the control output for the current cycle.

.. note::
   Must be called once per cycle on a single PLC task.
   If :attr:`b0` is zero the output is held at zero.
