.. _fb_trackingintegrator:

FB_TrackingIntegrator (Function Block)
======================================

Integrates the input error signal with back-calculation anti-windup.

Extends :class:`FB_Integrator` by accepting an external comparator input,
typically the :attr:`~FB_Clamp.Residual` of an :class:`FB_Clamp` block, to
unwind the integrator gradually when the output is saturated. The residual is
scaled by ``1 / Tt`` and subtracted from the integrator input each cycle.

A typical wiring pattern:

.. code-block:: pascal

   fbI.Input           := fbP.Output; // Standard form. Use fError for parallel form.
   fbI.ComparatorInput := fbClamp.Residual;
   fbI.Run();
   fbClamp.Input := fbP.Output + fbI.Output + fbD.Output;
   fbClamp.Run();

.. note::
   Set :attr:`Maximum` before :attr:`Minimum` to ensure the clamp guard applies
   correctly.

   Use ``FB_init`` to set :attr:`tTn` and :attr:`tTt` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_TrackingIntegrator EXTENDS FB_Integrator
   VAR
   	_fComparatorInput  : LREAL; // External residual signal for back-calculation anti-windup.
   	_tTt 			   : LTIME; // Tracking time constant (Tt). Controls how quickly the integrator unwinds.
   END_VAR

Properties
----------

.. _fb_trackingintegrator.comparatorinput:

ComparatorInput
~~~~~~~~~~~~~~~

Type: ``LREAL``

Gets or sets the comparator input.

This is typically the :attr:`~FB_Clamp.Residual` of an :class:`FB_Clamp` block
placed after the PID summation, passed directly without negation. The block
subtracts the scaled residual from the integrator input internally to unwind
the integrator when the output is saturated.

A positive value indicates the unsaturated sum exceeded the clamp maximum.
A negative value indicates it fell below the clamp minimum.

.. _fb_trackingintegrator.tt:

Tt
~~

Type: ``LTIME``

Gets or sets the tracking time constant (Tt).

Controls how quickly the integrator unwinds after saturation. A typical
starting value is ``SQRT(Tn * Td)``. Setting it to ``LTIME#0`` disables
the back-calculation correction entirely.

Methods
-------

.. _fb_trackingintegrator.fb_init:

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
   * - ``tTt``
     - ``LTIME;``
     - Tracking time constant (Tt). A typical starting value is SQRT(Tn * Td).


.. _fb_trackingintegrator.run:

Run
~~~

Advances the tracking integrator by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If :attr:`Tn` is
   ``LTIME#0`` the output is set to zero. If :attr:`Tt` is ``LTIME#0``
   the back-calculation correction is disabled.
