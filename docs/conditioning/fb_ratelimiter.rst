.. _fb_ratelimiter:

FB_RateLimiter (Function Block)
===============================

Limits the rate of change of the input signal.

The output tracks the input but cannot change faster than :attr:`RisingLimit`
units per second when increasing, or :attr:`FallingLimit` units per second when
decreasing. A limit of zero removes the restriction in that direction, allowing
the output to change freely.

Calling :meth:`Reset` snaps the output to the current input immediately.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fRisingLimit` and :attr:`fFallingLimit` at
   declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_RateLimiter EXTENDS FB_SisoComponent
   IMPLEMENTS FsCommon.I_Runnable, I_Resettable
   VAR
   	_fRisingLimit  : LREAL; // Maximum rate of increase in units per second. Zero means no limit.
   	_fFallingLimit : LREAL; // Maximum rate of decrease in units per second. Zero means no limit.
   END_VAR

Properties
----------

.. _fb_ratelimiter.fallinglimit:

FallingLimit
~~~~~~~~~~~~

Type: ``LREAL``

Gets or sets the maximum rate of decrease in units per second.

The output will not fall faster than this value regardless of how quickly
the input changes. A value of zero removes the falling limit entirely.
Values below zero are clamped to zero.

.. _fb_ratelimiter.risinglimit:

RisingLimit
~~~~~~~~~~~

Type: ``LREAL``

Gets or sets the maximum rate of increase in units per second.

The output will not rise faster than this value regardless of how quickly
the input changes. A value of zero removes the rising limit entirely.
Values below zero are clamped to zero.

Methods
-------

.. _fb_ratelimiter.fb_init:

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
   * - ``fRisingLimit``
     - ``LREAL;``
     - Maximum rate of increase in units per second. Zero means no limit.
   * - ``fFallingLimit``
     - ``LREAL;``
     - Maximum rate of decrease in units per second. Zero means no limit.


.. _fb_ratelimiter.reset:

Reset
~~~~~

Snaps the output to the current input, bypassing the rate limit.

.. _fb_ratelimiter.run:

Run
~~~

Advances the rate limiter by one time step.

.. note::
   Must be called once per cycle on a single PLC task. If the measured cycle
   time is zero the method returns early without updating the output.
