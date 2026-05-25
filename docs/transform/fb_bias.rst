.. _fb_bias:

FB_Bias (Function Block)
========================

Adds a fixed offset to the input signal.

A positive value shifts the output up; a negative value shifts it down.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_Bias EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable
   VAR
   	_fBias : LREAL; // Fixed offset added to the input.
   END_VAR

Properties
----------

.. _fb_bias.bias:

Bias
~~~~

Type: ``LREAL``

Gets or sets the fixed offset added to the input. Negative values subtract.

Methods
-------

.. _fb_bias.fb_init:

Initialisation
~~~~~~~~~~~~~~

**Parameters**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Name
     - Type
     - Description
   * - ``bInitRetains``
     - ``BOOL;``
     - if TRUE, the retain variables are initialized (warm start / cold start)
   * - ``bInCopyCode``
     - ``BOOL;``
     - if TRUE, the instance afterwards gets moved into the copy code (online change)
   * - ``fBias``
     - ``LREAL;``
     - Fixed offset added to the input.


.. _fb_bias.run:

Run
~~~

Adds :attr:`Bias` to the current input.
