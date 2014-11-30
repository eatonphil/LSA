Logisim Static Analysis Tool - LSA
==================================

This is a tool to statically analyze logisim circuits. You can use this in conjunction with the new STDL (discussed below) to count transistors and get other information statically available.

STDL - Standard Library
-----------------------

This library re-implements the Logisim standard library from the ground up building from CMOS logic universal gates. Some of the larger circuits (i.e. Multiplexer16x16) can be VERY slow because of the poor way memory is handled in Logisim. Most importantly, this library is one way to get a transistor count for all elements used in Logisim circuits. Unlike the Logisim standard library that implements all gates in terms of Java API calls, each component in the STDL is built atop lower-level components. Unfortunately, this means that arbitrary bit-width or input-number gates are currently impossible in Logisim. They were only possible in the standard library because the author could "cheat" and make API calls.

Mostly, this library was a fun chance to learn more about circuits in a hands on manner. The library does NOT NEED TO BE USED to get the transistor count. The lsa program provides lookups for many components. Support for more components will continue to grow in time.

This tool and library is still in its infancy. Please report any bugs!
