.. _fb_proportionalgain:

FB_ProportionalGain (Function Block)
====================================

Applies a proportional gain to the input error signal.

The output is computed as:

.. math::

   y = K_p \cdot e

where :math:`K_p` is :attr:`Kp` and :math:`e` is the error signal set via :attr:`Input`.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fKp` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_ProportionalGain EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_fKp : LREAL; // Proportional gain.
   END_VAR

Properties
----------

.. _fb_proportionalgain.kp:

Kp
~~

Type: ``LREAL``

Gets or sets the proportional gain.

A higher value produces a stronger response to error but may cause overshoot.
A lower value produces a more gradual response. A value of 0 disables the
proportional term entirely.

Methods
-------

.. _fb_proportionalgain.fb_init:

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
   * - ``fKp``
     - ``LREAL;``
     - Proportional gain.


.. _fb_proportionalgain.reset:

Reset
~~~~~

Sets the output to zero. Takes effect until the next :meth:`Run` call.

.. _fb_proportionalgain.run:

Run
~~~

Computes the proportional output for the current cycle.

.. note::
   Must be called once per cycle on a single PLC task.
