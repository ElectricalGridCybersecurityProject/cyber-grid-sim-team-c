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


def run_quasi_dynamic(case=14, load_scales=(1.0,), gen_scales=None):
    """T-1.2: solve the power flow again at each load or generation step."""
    key = str(case)
    if key not in IEEE_CASES:
        known = ", ".join(IEEE_CASES)
        raise ValueError(f"Unknown IEEE case {case!r}. Available: {known}")

    scales = [float(scale) for scale in load_scales]
    if not scales:
        raise ValueError("load_scales must contain at least one step")

    generation = None
    if gen_scales is not None:
        generation = [float(scale) for scale in gen_scales]
        if len(generation) != len(scales):
            raise ValueError("gen_scales must have one value per load step")

    net = IEEE_CASES[key]()
    base_p = net.load.p_mw.copy()
    base_q = net.load.q_mvar.copy()
    base_gen = net.gen.p_mw.copy()

    records = []
    for step, scale in enumerate(scales):
        net.load.p_mw = base_p * scale
        net.load.q_mvar = base_q * scale
        gen_scale = None
        if generation is not None:
            gen_scale = generation[step]
            net.gen.p_mw = base_gen * gen_scale
        pp.runpp(net)
        records.append(
            {
                "step": step,
                "load_scale": scale,
                "gen_scale": gen_scale,
                "load_p_mw": float(net.load.p_mw.sum()),
                "converged": bool(net.converged),
                "vm_pu": net.res_bus.vm_pu.to_numpy(copy=True),
            }
        )
    return records


if __name__ == "__main__":
    for name in IEEE_CASES:
        net = load_ieee(name)
        print(
            name,
            "converged:", net.converged,
            "buses:", len(net.bus),
        )
