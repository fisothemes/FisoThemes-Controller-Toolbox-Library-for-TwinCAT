.. _i_socomponent:

I_SoComponent (Interface)
=========================

Interface for single-output controller toolbox components.

Implementors expose a read-only :attr:`Output` property. For components that
also accept an input signal, use ``I_SisoComponent`` instead.

.. code-block:: none

   INTERFACE I_SoComponent EXTENDS I_Component

Properties
----------

.. _i_socomponent.output:

Output
~~~~~~

Type: ``LREAL``
