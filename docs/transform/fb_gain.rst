.. _fb_gain:

FB_Gain (Function Block)
========================

Scales the input signal by a fixed gain.

A value greater than 1 amplifies the signal. A value between 0 and 1 attenuates
it. A negative value inverts and scales. A value of 0 holds the output at zero.

**Extends:** :ref:`FB_SisoComponent <fb_sisocomponent>`

Properties
----------

.. _fb_gain.gain:

Gain
~~~~

Type: ``LREAL``

Gets or sets the scaling factor.

A value greater than 1 amplifies the signal. A value between 0 and 1
attenuates it. A value of -1 inverts the signal. A value of 0 holds
the output at zero.

Methods
-------

.. _fb_gain.fb_init:

FB_init
~~~~~~~

**Inputs**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Name
     - Type
     - Description
   * - ``bInitRetains``
     - ``BOOL``
     - if TRUE, the retain variables are initialized (warm start / cold start)
   * - ``bInCopyCode``
     - ``BOOL``
     - if TRUE, the instance afterwards gets moved into the copy code (online change)
   * - ``fGain``
     - ``LREAL``
     - Factor the input is scaled by.


.. _fb_gain.run:

Run
~~~

Scales the current input by :attr:`Gain`.
