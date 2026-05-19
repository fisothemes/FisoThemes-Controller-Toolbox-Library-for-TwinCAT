.. _fb_deadband:

FB_Deadband (Function Block)
============================

Suppresses small input signals within a configurable band.

When the input falls within [:attr:`Minimum`, :attr:`Maximum`], the output
is either zeroed or held at its last value depending on :attr:`Mode`. Outside
the band the input passes through unchanged.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fMinimum`, :attr:`fMaximum`, and :attr:`eMode`
   at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_Deadband EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_fMinimum : LREAL; // Lower bound of the deadband. Clamped to <= Maximum.
   	_fMaximum : LREAL; // Upper bound of the deadband. Clamped to >= Minimum.
   	_eMode    : E_DeadbandMode; // Output behaviour when input is within the band.
   END_VAR

Properties
----------

.. _fb_deadband.maximum:

Maximum
~~~~~~~

Type: ``LREAL``

Gets or sets the upper bound of the deadband.

Internally clamped to be greater than or equal to :attr:`Minimum`.
Set this before :attr:`Minimum` to ensure the guard applies correctly.

.. _fb_deadband.minimum:

Minimum
~~~~~~~

Type: ``LREAL``

Gets or sets the lower bound of the deadband.

Internally clamped to be less than or equal to :attr:`Maximum`.
Set :attr:`Maximum` before this property to ensure the guard applies correctly.

.. _fb_deadband.mode:

Mode
~~~~

Type: ``E_DeadbandMode``

Gets or sets the output behaviour when the input is within the band.

:attr:`~E_DeadbandMode.Zero` sets the output to zero. 
:attr:`~E_DeadbandMode.Hold` retains the last output value. 

Changes take effect on th next :meth:`Run` call.

Methods
-------

.. _fb_deadband.fb_init:

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
   * - ``fMaximum``
     - ``LREAL;``
     - Upper bound of the deadband.
   * - ``fMinimum``
     - ``LREAL;``
     - Lower bound of the deadband.
   * - ``eMode``
     - ``E_DeadbandMode;``
     - Output behaviour when the input is within the band.


.. _fb_deadband.reset:

Reset
~~~~~

Resets the output to a value consistent with the current mode. 

In :attr:`~E_DeadbandMode.Zero` mode the output is set to zero.
In :attr:`~E_DeadbandMode.Hold` mode the output is set to the current input.

.. _fb_deadband.run:

Run
~~~

Applies the deadband to the current input.
