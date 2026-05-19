.. _i_sisocomponent:

I_SisoComponent (Interface)
===========================

Interface for single-input single-output controller toolbox components.

Implementors expose a writable :attr:`Input` and a read-only :attr:`Output`,
both as ``LREAL``.

.. code-block:: none

   INTERFACE I_SisoComponent EXTENDS I_Component

Properties
----------

.. _i_sisocomponent.input:

Input
~~~~~

Type: ``LREAL``

.. _i_sisocomponent.output:

Output
~~~~~~

Type: ``LREAL``
