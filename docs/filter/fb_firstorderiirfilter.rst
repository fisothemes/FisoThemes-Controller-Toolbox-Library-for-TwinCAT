.. _fb_firstorderiirfilter:

FB_FirstOrderIIRFilter (Function Block)
=======================================

Applies an exponential moving average (EMA) to the input signal.

On the first call the output is set to the current input. On subsequent calls:

.. math::

   y[k] = \alpha \cdot u[k] + (1 - \alpha) \cdot y[k-1]

where :math:`\alpha` is :attr:`Alpha`. A value of 0 passes the input through
unchanged. A value of 1 holds the output at the first input value.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fAlpha` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_FirstOrderIIRFilter EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_fAlpha : LREAL; // Smoothing factor. Clamped to 0..1.
   END_VAR

Properties
----------

.. _fb_firstorderiirfilter.alpha:

Alpha
~~~~~

Type: ``LREAL``

Gets or sets the smoothing factor.

Controls the balance between the current input and the previous output.
A value closer to 0 produces a smoother, slower-responding output. A value
closer to 1 tracks the input more closely with less smoothing.
Values outside 0..1 are clamped.

Methods
-------

.. _fb_firstorderiirfilter.fb_init:

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
   * - ``fAlpha``
     - ``LREAL;``
     - Smoothing factor. Clamped to 0..1.


.. _fb_firstorderiirfilter.reset:

Reset
~~~~~

Sets the output to zero. 
On the next :meth:`Run` call the output will reinitialise to the current input.

.. _fb_firstorderiirfilter.run:

Run
~~~

Advances the filter by one time step.

On the first call the output is initialised to the current input to avoid
a transient caused by a zero initial state. Subsequent calls apply the
exponential moving average.
