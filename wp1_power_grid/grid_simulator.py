import pandapower as pp
import pandapower.networks as pn


# IEEE cases shipped with pandapower. "30" is the usual IEEE 30-bus case.
# "ieee30" is the other IEEE 30-bus file from MATPOWER.
IEEE_CASES = {
    "14": pn.case14,
    "24": pn.case24_ieee_rts,
    "30": pn.case30,
    "ieee30": pn.case_ieee30,
    "57": pn.case57,
    "118": pn.case118,
    "300": pn.case300,
}


def load_ieee(case=14):
    """Load one IEEE network and solve one power flow."""
    key = str(case)
    if key not in IEEE_CASES:
        known = ", ".join(IEEE_CASES)
        raise ValueError(f"Unknown IEEE case {case!r}. Available: {known}")
    net = IEEE_CASES[key]()
    pp.runpp(net)
    return net


def load_ieee14():
    """T-1.1: the IEEE 14-bus baseline."""
    return load_ieee(14)


if __name__ == "__main__":
    for name in IEEE_CASES:
        net = load_ieee(name)
        print(
            name,
            "converged:", net.converged,
            "buses:", len(net.bus),
        )
