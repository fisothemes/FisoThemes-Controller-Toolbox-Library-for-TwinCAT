.. _fb_linearscaler:

FB_LinearScaler (Function Block)
================================

Maps the input signal from one range to another using linear interpolation.

The input range [:attr:`InputMin`, :attr:`InputMax`] is mapped to the output
range [:attr:`OutputMin`, :attr:`OutputMax`]. Values outside the input range
are extrapolated linearly.

If :attr:`InputMin` equals :attr:`InputMax` the output is set to :attr:`OutputMin`.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fInputMax`, :attr:`fInputMin`, :attr:`fOutputMin`,
   :attr:`fOutputMax` and :attr:`fOutputMin` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_LinearScaler EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable
   VAR
   	_fInputMax  : LREAL; // Upper bound of the input range.
   	_fInputMin  : LREAL; // Lower bound of the input range.
   	_fOutputMax : LREAL; // Upper bound of the output range.
   	_fOutputMin : LREAL; // Lower bound of the output range.
   END_VAR

Properties
----------

.. _fb_linearscaler.inputmax:

InputMax
~~~~~~~~

Type: ``LREAL``

Gets or sets the upper bound of the input range.

.. _fb_linearscaler.inputmin:

InputMin
~~~~~~~~

Type: ``LREAL``

Gets or sets the lower bound of the input range.

.. _fb_linearscaler.outputmax:

OutputMax
~~~~~~~~~

Type: ``LREAL``

Gets or sets the upper bound of the output range.

.. _fb_linearscaler.outputmin:

OutputMin
~~~~~~~~~

Type: ``LREAL``

Gets or sets the lower bound of the output range.

Methods
-------

.. _fb_linearscaler.fb_init:

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
   * - ``fInputMax``
     - ``LREAL;``
     - Upper bound of the input range.
   * - ``fInputMin``
     - ``LREAL;``
     - Lower bound of the input range.
   * - ``fOutputMax``
     - ``LREAL;``
     - Upper bound of the output range.
   * - ``fOutputMin``
     - ``LREAL;``
     - Lower bound of the output range.


.. _fb_linearscaler.run:

Run
~~~

Applies the linear scaling to the current input.
