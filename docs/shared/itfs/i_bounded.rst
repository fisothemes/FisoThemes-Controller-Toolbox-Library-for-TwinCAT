.. _i_bounded:

I_Bounded (Interface)
=====================

Exposes configurable upper and lower bounds for blocks with clamped output.

Implemented by blocks such as :class:`FB_ClampingIntegrator` and :class:`FB_Clamp`
to allow external configuration of their output limits.

.. code-block:: none

   INTERFACE I_Bounded EXTENDS I_Component

Properties
----------

.. _i_bounded.maximum:

Maximum
~~~~~~~

Type: ``LREAL``

Gets or sets the upper bound.

This value could be clamped to be greater than or equal to :attr:`Minimum`.
Thus it is best practice to set this before :attr:`Minimum` to ensure the 
guard applies correctly.

.. _i_bounded.minimum:

Minimum
~~~~~~~

Type: ``LREAL``

Gets or sets the lower bound.

This value could be clamped to be less than or equal to :attr:`Maximum`.
Thus it is best practice to set :attr:`Maximum` before this property to 
ensure the guard applies correctly.
