Logisim Static Analysis Tool - LSA
==================================

This is a tool to statically analyze logisim circuits. You can use this in conjunction with the new STDL (discussed below) to count transistors and get other information statically available.

STDL - Standard Library
-----------------------

This library re-implements the Logisim standard library from the ground up building from CMOS logic universal gates. As a result, some of the larger circuits (i.e. Multiplexer16x16) can be VERY slow because of the poor way memory is handled in Logisim. This library is one way to get a transistor count for all elements used in Logisim circuits. Unfortunately, arbitrary bit-width or input-number gates are currently impossible in Logisim. They were only possible in the standard library because the author could "cheat" by making API calls to functions in Java.

Mostly, this library was a fun chance to learn more about circuits in a hands on manner. The library does NOT NEED TO BE USED to get the transistor count. The lsa program provides lookups for many components. Support for more components will continue to grow in time.

Setup & Usage
-----

#### Setup

Add the folder to the path. This is necessary to make sure the STDL circuits are available to the lsa application.

#### lsa circuit-file [circuit-name]

Where circuit-name defaults to "main". This can be changed to narrowly target a specific circuit/sub-circuit within a file.

This creates a few lsa files, currently: transistors.lsa and unused.lsa.

WARNING: This will fail if a component is used that is not yet supported (reimplemented in the STDL) by lsa.

#### Example

From the lsa directory:

    ./lsa tests/vendor/emcdowell/RightShift.circ
    cat transistors.lsa
    cat unused.lsa

### Generated Files

#### transistors.lsa

This file contains a list of all components used and their transistor counts. Components are separated by sub-circuits and sub-total transistor counts are listed at the end of each sub-section.

#### unused.lsa

This file displays any unused circuits in the circuit.

WARNING: The lsa program is easily tricked. An unconnected circuit or component that is placed in or referenced (recursively) by circuit-name (second argument to ./lsa) will be counted as a connected circuit or component.

This tool and library is still in its infancy. Please report any bugs!
