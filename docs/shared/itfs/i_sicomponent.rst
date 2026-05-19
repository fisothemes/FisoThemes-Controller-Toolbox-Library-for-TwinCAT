.. _i_sicomponent:

I_SiComponent (Interface)
=========================

Interface for single-input controller toolbox components.

Implementors expose a write-only :attr:`Input` property. For components that
also produce an output signal, use ``I_SisoComponent`` instead.

.. code-block:: none

   INTERFACE I_SiComponent

Properties
----------

.. _i_sicomponent.input:

Input
~~~~~

Type: ``LREAL``
