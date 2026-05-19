.. _fb_differentiator:

FB_Differentiator (Function Block)
==================================

Differentiates the input signal with an optional first-order damping filter.

The transfer function is:

.. math::

   D(s) = \frac{T_v \cdot s}{T_d \cdot s + 1}

where :math:`T_v` is :attr:`Tv` and :math:`T_d` is :attr:`Td`. The filter is
discretised using the Tustin (bilinear) method.

Setting :attr:`Tv` to ``LTIME#0`` disables the derivative term entirely.
Setting :attr:`Td` to ``LTIME#0`` removes the damping filter, giving a pure
derivative. This is not recommended in practice due to noise sensitivity.

.. note::
   If derivative kick on setpoint steps is undesirable, pass the negated
   process variable as :attr:`Input` rather than the full error. The integrator
   should still receive the full error signal.

   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`tTv` and :attr:`tTd` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_Differentiator EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_tTv          : LTIME; // Rate time (Tv). Determines derivative action strength.
   	_tTd          : LTIME; // Damping time (Td). Filters the derivative signal to reduce noise sensitivity.
   	_fPrevInput   : LREAL; // Input from the previous cycle.
   	_fFilterState : LREAL; // Internal state of the damping filter.
   END_VAR

Properties
----------

.. _fb_differentiator.td:

Td
~~

Type: ``LTIME``

Gets or sets the damping time (Td).

This filters the derivative signal to reduce sensitivity to noise. A longer
value gives more filtering but reduces derivative effectiveness. Setting it
to ``LTIME#0`` removes the filter entirely, giving a pure derivative (not
recommended in practice due to noise sensitivity).

.. _fb_differentiator.tv:

Tv
~~

Type: ``LTIME``

Gets or sets the rate time (Tv).

This controls how strongly the block reacts to changes in the input. A longer
value increases derivative action. Setting it to ``LTIME#0`` disables the
derivative term entirely, holding the output at zero.

Methods
-------

.. _fb_differentiator.fb_init:

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
   * - ``tTv``
     - ``LTIME;``
     - Rate time. T#0S disables the derivative term entirely.
   * - ``tTd``
     - ``LTIME;``
     - Damping time. LTIME#0 means no filtering (pure derivative).


.. _fb_differentiator.reset:

Reset
~~~~~

Clears the filter state and output. 
Sets the previous input to the current input to avoid a spike on the next :meth:`Run` call.

.. _fb_differentiator.run:

Run
~~~

Advances the differentiator by one time step.

On the first call the cycle time is measured, the filter state is initialised,
and the method returns early without producing an output. This prevents a spike
caused by an uninitialised previous input.

.. note::
   Must be called once per cycle on a single PLC task. If :attr:`Tv` is
   ``LTIME#0`` the output is held at zero.
