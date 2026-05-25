.. _fb_whitenoise:

FB_WhiteNoise (Function Block)
==============================

Generates uniformly distributed white noise.

The output is a random value in the range [-:attr:`Amplitude`, +:attr:`Amplitude`]
on every cycle. Useful for testing controller robustness against measurement noise
and disturbances.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`Amplitude` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_WhiteNoise EXTENDS FB_SoComponent
   IMPLEMENTS FsCommon.I_Runnable
   VAR
   	_fAmplitude : LREAL; // Maximum absolute output value.
   	_fbRng      : FsCommon.FB_RandomNumberGenerator(0); // Internal random number generator.
   END_VAR

Properties
----------

.. _fb_whitenoise.amplitude:

Amplitude
~~~~~~~~~

Type: ``LREAL``

Gets or sets the amplitude.

The output is uniformly distributed in [-:attr:`Amplitude`, +:attr:`Amplitude`].
A value of 0 holds the output at zero.

Methods
-------

.. _fb_whitenoise.fb_init:

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
   * - ``fAmplitude``
     - ``LREAL;``
     - Maximum absolute output value.


.. _fb_whitenoise.run:

Run
~~~

Generates the next white noise sample.
