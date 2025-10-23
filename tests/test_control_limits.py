import pytest

from control_limits import (
    apply_rule,
    ControlLimitException,
    range_sieve_check,
    sieve_data_conforms,
    SieveData,
)
from rule_engine import DataType as rules_type

data = SieveData(
    sieve_size=["3/4", "1/2", "3/8", "No.8", "No.4"],
    cum_passing_pct=[100.0, 60.0, 50.0, 90.0, 100.0],
    pc_retained=[0.0, 40.0, 50.0, 10.0, 0.0],
    cum_retained_pct=[100.0, 60.0, 50.0, 90.0, 100.0],
)


def test_conforms_passes():
    rules = [
        'if name == "1/2" require (pc_retained > 30 and pc_retained < 60)',
        'if name == "3/8" require (pc_retained > 45 and pc_retained < 60)',
    ]
    results = sieve_data_conforms(data, rules)
    assert results == True


def test_conforms_fails():
    rules = [
        'if name == "1/2" require (pc_retained > 30 and pc_retained < 60)',
        'if name == "3/8" require (pc_retained > 55 and pc_retained < 60)',
    ]
    with pytest.raises(ControlLimitException) as err:
        sieve_data_conforms(data, rules)


def test_check_all_retained_percentages():
    rule = "(false not in [ retained_val > 11 for retained_val in pc_retained])"
    results = apply_rule(rule, data)
    assert results == False


def test_conforms_more_complex():
    rules = [
        range_sieve_check("3/4", 0, 60),
        'if name == "3/4" require (pc_retained >= 0 and pc_retained < 10)',
        'if name == "3/8" require (pc_retained > 45 and pc_retained < 60)',
        'if name == "No.8" require (pc_retained > 5 and pc_retained < 20)',
        'if name == "No.4" require (pc_retained >= 0 and pc_retained < 10)',
    ]
    results = sieve_data_conforms(data, rules)
    assert results == True


@pytest.mark.parametrize(
    "value, target, expected",
    [
        (10, range(0, 100), True),
        (0, range(0, 100), True),
        (10, range(0, 100), True),
        (-10, range(0, 100), False),
        (110, range(0, 100), False),
        ("a", "abc", True),
        ("abc", "abc", True),
        ("d", "abc", False),
        ("", "abc", True),
    ],
)
def test_given_an_integer_is_it_in_the_range(value, target, expected):
    data = {"value": value, "target": target}
    rule = "value in target"
    results = apply_rule(rule, data)
    assert results == expected


def test_in_with_type_checking():
    data = {
        "value": 3,
        "target": range(0, 100),
    }
    data_types = {
        "value": rules_type.FLOAT,
        "target": rules_type.ARRAY(rules_type.FLOAT),
    }
    rule = "value in target"
    r = apply_rule(rule, data, data_types)
    assert r == True


def test_in_with_type_checking_fails_deeper_type():
    data = {
        "value": 3,
        "target": range(0, 100),
    }
    data_types = {
        "value": rules_type.FLOAT,
        "target": rules_type.ARRAY(rules_type.STRING),
    }
    rule = "value in target"
    with pytest.raises(Exception):
        r = apply_rule(rule, data, data_types)


def test_in_raises_exception():
    data = {
        "value": "value",
        "target": range(0, 100),
    }
    data_types = {
        "value": rules_type.FLOAT,
        "target": rules_type.ARRAY(rules_type.FLOAT),
    }
    rule = "value in target"
    with pytest.raises(Exception):
        apply_rule(rule, data, data_types)


@pytest.mark.parametrize(
    "needle, haystack, expected",
    [
        ("v", "abc", False),
        ("a", "abc", True),
        ("d", "abc", False),
        ("", "abc", True),
    ],
)
def test_custom_function(needle, haystack, expected):
    data = {
        "needle": needle,
        "haystack": haystack,
    }
    rule = "startswith(haystack, needle)"
    r = apply_rule(
        rule,
        data,
    )
    assert r == expected


