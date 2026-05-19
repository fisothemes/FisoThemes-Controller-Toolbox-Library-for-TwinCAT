.. _fb_sicomponent:

FB_SiComponent (Function Block)
===============================

Abstract function block providing an :attr:`Input` property for single-input
controller toolbox components.

Concrete implementations read from ``_fInput`` to consume the signal written
by the caller.

.. note::
   Direct calls to this function block are not permitted (``no_explicit_call``).
   Extend it and call the derived block instead.

.. code-block:: none

   FUNCTION_BLOCK ABSTRACT FB_SiComponent
   IMPLEMENTS I_SiComponent
   VAR
       _fInput : LREAL;
   END_VAR

Properties
----------

.. _fb_sicomponent.input:

Input
~~~~~

Type: ``LREAL``

Gets or sets the input to the component.
