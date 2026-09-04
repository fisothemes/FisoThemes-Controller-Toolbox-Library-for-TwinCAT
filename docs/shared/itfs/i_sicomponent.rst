.. _i_sicomponent:

I_SiComponent (Interface)
=========================

Interface for single-input controller toolbox components.

Implementors expose a write-only :attr:`Input` property. For components that
also produce an output signal, use ``I_SisoComponent`` instead.

Properties
----------

.. _i_sicomponent.input:

Input
~~~~~

Type: ``LREAL``

Gets or sets the input to the component.
