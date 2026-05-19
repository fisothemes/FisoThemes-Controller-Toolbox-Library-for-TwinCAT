.. _i_resettable:

I_Resettable (Interface)
========================

Interface for components that can be returned to a known initial state.

Implementors must define :meth:`Reset` to clear any internal state, such as
accumulators, filter history, or elapsed time, and restore the output to its
initial condition.

.. code-block:: none

   INTERFACE I_Resettable EXTENDS __SYSTEM.IQueryInterface
