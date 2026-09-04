.. _fb_rampprofile:

FB_RampProfile (Function Block)
===============================

Generates a ramp signal that rises or falls toward a target value within a
configurable duration, then holds at the target.

The rate of change is derived automatically from :attr:`Target`, :attr:`StartValue`,
and :attr:`Duration`. Once the output is within one time step of the target it
snaps to the target and :attr:`IsComplete` becomes ``TRUE``. If :attr:`Target`
or :attr:`Duration` change mid-run the rate is recalculated immediately.

A duration of ``LTIME#0`` snaps the output to :attr:`Target` immediately.
If :attr:`Target` equals :attr:`StartValue`, :attr:`IsComplete` is ``TRUE``
from the first call.

Calling :meth:`Reset` returns the output to :attr:`StartValue` and clears
:attr:`IsComplete`.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fStartValue`, :attr:`fTarget`, and :attr:`tDuration`
   at declaration time.

**Extends:** :ref:`FB_SoComponent <fb_socomponent>`

Properties
----------

.. _fb_rampprofile.duration:

Duration
~~~~~~~~

Type: ``LTIME``

Gets or sets the duration. 

This is the time taken to ramp from :attr:`StartValue` to :attr:`Target`.
``LTIME#0`` snaps the output to the target immediately. 
Changes take effect immediately.

.. _fb_rampprofile.iscomplete:

IsComplete
~~~~~~~~~~

Type: ``BOOL``

Gets whether the output has reached :attr:`Target`. 

Becomes ``TRUE`` when the output is within one time step of the target,
and ``FALSE`` again if :attr:`Target` changes and the output no longer matches.

.. _fb_rampprofile.startvalue:

StartValue
~~~~~~~~~~

Type: ``LREAL``

Gets or sets the start value.

This is the output value the ramp returns to after a :meth:`Reset`.

.. _fb_rampprofile.target:

Target
~~~~~~

Type: ``LREAL``

Gets or sets the target value. 

The output ramps toward this value within :attr:`Duration`. 
Changes take effect immediately, recalculating the rate.

Methods
-------

.. _fb_rampprofile.fb_init:

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
   * - ``fStartValue``
     - ``LREAL``
     - Initial output value.
   * - ``fTarget``
     - ``LREAL``
     - Target value to ramp toward.
   * - ``tDuration``
     - ``LTIME``
     - Time to reach the target from StartValue. LTIME#0 snaps immediately.


.. _fb_rampprofile.reset:

Reset
~~~~~

Returns the output to the start value set in ``FB_init`` and clears :attr:`IsComplete`.

.. _fb_rampprofile.run:

Run
~~~

Advances the ramp profile by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If the measured cycle
   time is zero the method returns early without updating the output.
