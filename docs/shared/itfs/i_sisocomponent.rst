.. _i_sisocomponent:

I_SisoComponent (Interface)
===========================

Interface for single-input single-output controller toolbox components.

Implementors expose a writable :attr:`Input` and a read-only :attr:`Output`,
both as ``LREAL``.

**Extends:** :ref:`I_Component <i_component>`

Properties
----------

.. _i_sisocomponent.input:

Input
~~~~~

Type: ``LREAL``

Gets or sets the input to the component.

.. _i_sisocomponent.output:

Output
~~~~~~

Type: ``LREAL``

Gets the output produced by the component.
