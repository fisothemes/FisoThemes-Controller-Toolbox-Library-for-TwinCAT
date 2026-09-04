.. _i_socomponent:

I_SoComponent (Interface)
=========================

Interface for single-output controller toolbox components.

Implementors expose a read-only :attr:`Output` property. For components that
also accept an input signal, use ``I_SisoComponent`` instead.

**Extends:** :ref:`I_Component <i_component>`

Properties
----------

.. _i_socomponent.output:

Output
~~~~~~

Type: ``LREAL``

Gets the output produced by the component.
