.. _fb_socomponent:

FB_SoComponent (Function Block)
===============================

Abstract function block providing an :attr:`Output` property for single-output
controller toolbox components.

Concrete implementations must call this block cyclically and write their
result to ``_fOutput``.

.. note::
   Direct calls to this function block are not permitted (``no_explicit_call``).
   Extend it and call the derived block instead.

.. code-block:: none

   FUNCTION_BLOCK ABSTRACT FB_SoComponent
   IMPLEMENTS I_SoComponent
   VAR
   	_fOutput : LREAL;
   END_VAR

Properties
----------

.. _fb_socomponent.output:

Output
~~~~~~

Type: ``LREAL``

Gets the output produced by the component.
