.. _fb_sisocomponent:

FB_SisoComponent (Function Block)
=================================

Abstract function block providing :attr:`Input` and :attr:`Output` properties
for single-input single-output controller toolbox components.

.. NOTE::
   Direct calls to this function block are not permitted (``no_explicit_call``).

.. code-block:: none

   FUNCTION_BLOCK ABSTRACT FB_SisoComponent
   IMPLEMENTS I_SisoComponent, I_SiComponent, I_SoComponent
   VAR
   	_fInput 	: LREAL;
   	_fOutput 	: LREAL;
   END_VAR

Properties
----------

.. _fb_sisocomponent.input:

Input
~~~~~

Type: ``LREAL``

Gets or sets the input to the component.

.. _fb_sisocomponent.output:

Output
~~~~~~

Type: ``LREAL``

Gets the output produced by the component.
