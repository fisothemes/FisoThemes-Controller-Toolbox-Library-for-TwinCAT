.. _fb_gaussiannoise:

FB_GaussianNoise (Function Block)
=================================

Generates normally distributed (Gaussian) noise using the Box-Muller transform.

The output follows a normal distribution with the configured :attr:`Mean` and
:attr:`StdDev`. Values beyond ±3σ occur roughly 0.3% of the time. This models
real sensor noise more accurately than uniform white noise.

.. note::
   The block is ``FINAL`` and must be instantiated, not extended.
   Use ``FB_init`` to set :attr:`fMean` and :attr:`fStdDev` at declaration time.

.. code-block:: none

   FUNCTION_BLOCK FINAL FB_GaussianNoise EXTENDS FB_SoComponent
   IMPLEMENTS FsCommon.I_Runnable
   VAR
   	_fMean   : LREAL; // Mean (centre) of the distribution.
   	_fStdDev : LREAL; // Standard deviation. Controls the spread of the noise.
   	_fbRng   : FsCommon.FB_RandomNumberGenerator(0); // Internal random number generator.
   END_VAR

Properties
----------

.. _fb_gaussiannoise.mean:

Mean
~~~~

Type: ``LREAL``

Gets or sets the mean.

This is the centre of the distribution, the average value the noise oscillates
around. For pure noise centred on zero, set this to 0.

.. _fb_gaussiannoise.stddev:

StdDev
~~~~~~

Type: ``LREAL``

Gets or sets the standard deviation (σ).

Controls the spread of the noise. Roughly 68% of samples fall within ±1σ of
the mean, 95% within ±2σ, and 99.7% within ±3σ. A larger value produces
more spread-out noise.

Methods
-------

.. _fb_gaussiannoise.fb_init:

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
   * - ``fMean``
     - ``LREAL;``
     - Mean of the distribution.
   * - ``fStdDev``
     - ``LREAL;``
     - Standard deviation. A larger value produces more spread-out noise.


.. _fb_gaussiannoise.run:

Run
~~~

Generates the next Gaussian noise sample using the Box-Muller transform.

Two uniform random samples are drawn per cycle to produce one Gaussian sample.
If either sample is zero it is replaced with a small epsilon to avoid a
logarithm of zero.
