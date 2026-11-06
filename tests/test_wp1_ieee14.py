import pytest

from wp1_power_grid.grid_simulator import IEEE_CASES, load_ieee, load_ieee14


def test_ieee14_baseline_import():
    """T-1.1: the grid module loads the IEEE 14-bus case and the power flow converges."""
    net = load_ieee14()
    assert len(net.bus) == 14
    assert len(net.load) == 11
    assert len(net.gen) + len(net.ext_grid) == 5
    assert len(net.line) + len(net.trafo) == 20
    assert net.converged is True
    assert abs(float(net.res_bus.vm_pu.iloc[0]) - 1.06) < 1e-6


@pytest.mark.parametrize("case", list(IEEE_CASES))
def test_ieee_case_loads(case):
    net = load_ieee(case)
    expected_buses = 30 if case == "ieee30" else int(case)
    assert len(net.bus) == expected_buses
    assert net.converged is True


def test_unknown_ieee_case_is_rejected():
    with pytest.raises(ValueError):
        load_ieee(999)
