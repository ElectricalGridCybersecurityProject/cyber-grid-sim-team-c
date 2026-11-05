from wp1_power_grid.grid_simulator import load_ieee14


def test_ieee14_baseline_import():
    """T-1.1: the grid module loads the IEEE 14-bus case and the power flow converges."""
    net = load_ieee14()
    assert len(net.bus) == 14
    assert len(net.load) == 11
    assert len(net.gen) + len(net.ext_grid) == 5
    assert len(net.line) + len(net.trafo) == 20
    assert net.converged is True
    assert abs(float(net.res_bus.vm_pu.iloc[0]) - 1.06) < 1e-6
