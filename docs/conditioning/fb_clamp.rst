.. _fb_clamp:

FB_Clamp (Function Block)
=========================

Clamps the input signal to the range [:attr:`Minimum`, :attr:`Maximum`].

Any input below :attr:`Minimum` is set to :attr:`Minimum`. Any input above
:attr:`Maximum` is set to :attr:`Maximum`. Inputs within the range pass
through unchanged.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fMaximum` and :attr:`fMinimum` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_Clamp EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Bounded
   VAR
   	_fMaximum  : LREAL; // Upper clamp bound. Clamped to >= Minimum.
   	_fMinimum  : LREAL; // Lower clamp bound. Clamped to <= Maximum.
   	_fResidual : LREAL; // Difference between the unclamped input and the clamped output.
   END_VAR

Properties
----------

.. _fb_clamp.maximum:

Maximum
~~~~~~~

Type: ``LREAL``

Gets or sets the upper clamp bound.

Internally clamped to be greater than or equal to :attr:`Minimum`.
Set this before :attr:`Minimum` to ensure the guard applies correctly.

.. _fb_clamp.minimum:

Minimum
~~~~~~~

Type: ``LREAL``

Gets or sets the lower clamp bound.

Internally clamped to be less than or equal to :attr:`Maximum`.
Set :attr:`Maximum` before this property to ensure the guard applies correctly.

.. _fb_clamp.residual:

Residual
~~~~~~~~

Type: ``LREAL``

Gets the difference between the unclamped input and the clamped output. Zero when the input is within [:attr:`Minimum`, :attr:`Maximum`].

Methods
-------

.. _fb_clamp.fb_init:

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
     - Upper clamp bound.
   * - ``fMinimum``
     - ``LREAL;``
     - Lower clamp bound.


.. _fb_clamp.run:

Run
~~~

Clamps the current input to [:attr:`Minimum`, :attr:`Maximum`].
