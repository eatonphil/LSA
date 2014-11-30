import circ

NAMESPACE = "stdl"

GATE_CIRCS = NAMESPACE+"/STDLGates.circ"
PLEXER_CIRCS = NAMESPACE+"/STDLPlexers.circ"
MEMORY_CIRCS = NAMESPACE+"/STDLMemory.circ"

COMP_NOT_FOUND_ERROR = "Error, component lookup not yet supported: %s width %s inputs %s."

GATES = {
    "AND Gate": "AND",
    "OR Gate": "OR",
    "NAND Gate": "NAND",
    "NOR Gate": "NOR",
    "XOR Gate": "XOR",
    "XNOR Gate": "XNOR",
    "NOT Gate": "NOT"
}

PLEXERS = {
    "Decoder": {
        2: {1: "Decoder2"},
        3: {1: "Decoder3"},
        4: {1: "Decoder4"}
    },
    "Multiplexer": {
        1: {
            1: "Multiplexer1x1",
            2: "Multiplexer1x2",
            4: "Multiplexer1x4",
            8: "Multiplexer1x8",
            16: "Multiplexer1x16"
        },
        2: {
            1: "Multiplexer2x1",
            2: "Multiplexer2x2",
            4: "Multiplexer2x4",
            8: "Multiplexer2x8",
            16: "Multiplexer2x16"
        },
        4: {
            1: "Multiplexer4x1",
            2: "Multiplexer4x2",
            4: "Multiplexer4x4",
            8: "Multiplexer4x8",
            16: "Multiplexer4x16"
        },
        8: {
            1: "Multiplexer8x1",
            2: "Multiplexer8x2",
            4: "Multiplexer8x4",
            8: "Multiplexer8x8",
            16: "Multiplexer8x16"
        },
        16: {
            1: "Multiplexer16x1",
            2: "Multiplexer16x2",
            4: "Multiplexer16x4",
            8: "Multiplexer16x8",
            16: "Multiplexer16x16"
        }
    }
}

MEMORY = {
    "S-R Flip-Flop": {
        1: {1: "SRLatch"}
    },
    "J-K Flip-Flop": {
        1: {1: "JKLatch"}
    },
    "D Flip-Flop": {
        1: {1: "DLatch"}
    },
    "Register": {
        1: {
            1: "Register1",
            2: "Register2",
            4: "Register4",
            8: "Register8",
            16: "Register16",
            32: "Register32"
        }
    }
}

STDL_RMAP = {}

for comp, mapped_comp in GATES.iteritems():
    STDL_RMAP[mapped_comp] = comp

for section in [PLEXERS, MEMORY]:
    for comp, widths in section.iteritems():
        for width, inputs in widths.iteritems():
            for i in inputs:
                STDL_RMAP[i] = comp

def component(comp, width, inputs, fail=True):
    try:
        if comp in STDL_RMAP:
            unmap = STDL_RMAP[comp]
            if unmap in GATES:
                return comp, GATE_CIRCS
            elif unmap in PLEXERS:
                return comp, PLEXER_CIRCS
            elif unmap in MEMORY:
                return comp, MEMORY_CIRCS
        elif comp in GATES:
            return GATES[comp], GATE_CIRCS
        elif comp in PLEXERS:
            return PLEXERS[comp][width][inputs], PLEXER_CIRCS
        elif comp in MEMORY:
            return MEMORY[comp][width][inputs], MEMORY_CIRCS
    except:       
        pass

    error = COMP_NOT_FOUND_ERROR % (comp, width, inputs)

    if fail:
        import sys
        print 
        sys.exit(0)
    return False, error
