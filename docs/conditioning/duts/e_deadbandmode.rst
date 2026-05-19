.. _e_deadbandmode:

E_DeadbandMode (Enum)
=====================

Specifies the behaviour of ``FB_Deadband`` when the input is within the band.

Members
-------

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - Name
     - Value
     - Description
   * - ``Hold``
     - 0
     - Output holds its last value while the input is within the band.
   * - ``Zero``
     - 1
     - Output is set to zero while the input is within the band.
