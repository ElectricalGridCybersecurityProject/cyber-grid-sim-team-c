import pandapower as pp
import pandapower.networks as pn


def load_ieee14():
    """T-1.1: load the IEEE 14-bus network and solve one power flow."""
    net = pn.case14()
    pp.runpp(net)
    return net


if __name__ == "__main__":
    net = load_ieee14()
    print("converged:", net.converged)
    print("buses:", len(net.bus))
    print("generators:", len(net.gen) + len(net.ext_grid))
    print("loads:", len(net.load))
    print("branches:", len(net.line) + len(net.trafo))
