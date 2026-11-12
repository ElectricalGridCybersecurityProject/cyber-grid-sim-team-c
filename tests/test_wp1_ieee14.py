import pytest

from wp1_power_grid.grid_simulator import IEEE_CASES, load_ieee, load_ieee14, run_quasi_dynamic


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


def test_quasi_dynamic_load_steps_on_ieee14():
    """T-1.2: three load steps, and the unchanged step matches one power flow."""
    scales = (0.8, 1.0, 1.2)
    records = run_quasi_dynamic(14, scales)

    assert len(records) == 3
    assert all(record["converged"] for record in records)

    base = load_ieee14()
    base_load = float(base.load.p_mw.sum())
    for record, scale in zip(records, scales):
        assert record["load_p_mw"] == pytest.approx(base_load * scale)

    load_buses = set(base.load.bus)
    gen_buses = set(base.gen.bus) | set(base.ext_grid.bus)
    pq_bus = min(load_buses - gen_buses)
    assert records[0]["vm_pu"][pq_bus] != pytest.approx(records[2]["vm_pu"][pq_bus])
    assert records[1]["vm_pu"] == pytest.approx(base.res_bus.vm_pu.to_numpy())
