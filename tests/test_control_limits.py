import pytest

from control_limits import apply_rule, ControlLimitException, sieve_data_conforms, SieveData

data = SieveData (
    sieve_size=     ["3/4", "1/2", "3/8", "No.8", "No.4"],
    cum_passing_pct=  [100.0, 60.0, 50.0, 90.0, 100.0],
    pc_retained=      [0.0, 40.0, 50.0, 10.0, 0.0],
    cum_retained_pct= [100.0, 60.0, 50.0, 90.0, 100.0],
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
    rule = '(false not in [ retained_val > 11 for retained_val in pc_retained])'
    results = apply_rule(rule, data)
    assert results == False

def test_conforms_more_complex():
    rules = [
        range_sieve_check('3/4',0,60),
        # 'if name == "3/4" require (pc_retained >= 0 and pc_retained < 10)',
        # 'if name == "3/8" require (pc_retained > 45 and pc_retained < 60)',
        # 'if name == "No.8" require (pc_retained > 5 and pc_retained < 20)',
        # 'if name == "No.4" require (pc_retained >= 0 and pc_retained < 10)',
    ]
    results = sieve_data_conforms(data, rules)
    assert results == True


def range_sieve_check(name, lt,gt) -> str:
    return f'if name == "{name}" require (pc_retained >={lt}  and pc_retained <= {gt})'


   # "eq": lambda column: column.__eq__,
        # "gt": lambda column: column.__gt__,
        # "lt": lambda column: column.__lt__,
        # "gte": lambda column: column.__ge__,
        # "lte": lambda column: column.__le__,
        # "ne": lambda column: column.__ne__,
        # "is": lambda column: column.is_,
        # "is_not": lambda column: column.is_not,
        # "like": lambda column: column.like,
        # "notlike": lambda column: column.notlike,
        # "ilike": lambda column: column.ilike,
        # "notilike": lambda column: column.notilike,
        # "startswith": lambda column: column.startswith,
        # "endswith": lambda column: column.endswith,
        # "contains": lambda column: column.contains,
        # "match": lambda column: column.match,
        # "between": lambda column: column.between,
        # "in": lambda column: column.in_,
        # "not_in": lambda column: column.not_in,
        # "or": lambda column: column.or_,
        # "not": lambda column: column.not_,
    # }