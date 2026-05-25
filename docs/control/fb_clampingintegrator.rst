.. _fb_clampingintegrator:

FB_ClampingIntegrator (Function Block)
======================================

Integrates the input error signal with comparator-based anti-windup.

Extends :class:`FB_Integrator` by suppressing integration when the
:attr:`ComparatorInput` indicates saturation and the input would push
further into saturation. The suppression behaviour is controlled by :attr:`Mode`.

:attr:`ComparatorInput` is typically the :attr:`~FB_Clamp.Residual` of an
:class:`FB_Clamp` block placed after the PID summation.

.. note::
   Set :attr:`Maximum` before :attr:`Minimum` to ensure the clamp guard applies
   correctly.

   Use ``FB_init`` to set :attr:`tTn` and :attr:`eMode` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_ClampingIntegrator EXTENDS FB_Integrator
   VAR
   	_fComparatorInput  : LREAL;
   	_bAntiWindupActive : BOOL; // TRUE when the output is saturated and integration is halted.
   	_eMode			   : E_AntiWindupMode; // The integrator behaviour during saturation.
   END_VAR

Properties
----------

.. _fb_clampingintegrator.antiwindupactive:

AntiWindupActive
~~~~~~~~~~~~~~~~

Type: ``BOOL``

Gets whether the output is currently saturated and integration is halted.

.. _fb_clampingintegrator.comparatorinput:

ComparatorInput
~~~~~~~~~~~~~~~

Type: ``LREAL``

Gets or sets the comparator input.

This is typically the :attr:`~FB_Clamp.Residual` of an :class:`FB_Clamp` block
placed after the PID summation. A positive value indicates the unsaturated sum
exceeded the clamp maximum; a negative value indicates it fell below the clamp
minimum. When this value and :attr:`Input` have the same sign, integration is
suppressed according to :attr:`Mode`.

.. _fb_clampingintegrator.mode:

Mode
~~~~

Type: ``E_AntiWindupMode``

Gets or sets the anti-windup mode.

Controls the integrator behaviour when saturation is detected via
:attr:`ComparatorInput`. See :class:`E_AntiWindupMode` for available modes.

Methods
-------

.. _fb_clampingintegrator.fb_init:

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
   * - ``eMode``
     - ``E_AntiWindupMode;``
     - The integrator behaviour during saturation.


.. _fb_clampingintegrator.reset:

Reset
~~~~~

Clears the integrator state, output, and anti-windup flag.

.. _fb_clampingintegrator.run:

Run
~~~

Advances the clamping integrator by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If :attr:`Tn` is
   ``LTIME#0`` the output is set to zero and anti-windup is cleared.
