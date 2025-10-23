import pytest

from control_limits import ControlLimitException, sieve_data_conforms, SieveData


yesterday_data = SieveData(
    sieve_size=["3/4", "1/2", "3/8", "No.8", "No.4"],
    cum_passing_pct=[100.0, 60.0, 50.0, 90.0, 100.0],
    pc_retained=[0.0, 20.0, 30.0, 0.0, 0.0],
    cum_retained_pct=[100.0, 60.0, 50.0, 90.0, 100.0],
)
data = SieveData(
    sieve_size=["3/4", "1/2", "3/8", "No.8", "No.4"],
    cum_passing_pct=[100.0, 60.0, 50.0, 90.0, 100.0],
    pc_retained=[0.0, 40.0, 50.0, 10.0, 0.0],
    cum_retained_pct=[100.0, 60.0, 50.0, 90.0, 100.0],
)


def test_sieve_diff():
    diff = data - yesterday_data
    rules = [
        'if name == "1/2" require (pc_retained < 21)',
    ]
    results = sieve_data_conforms(diff, rules)
    assert results == True
