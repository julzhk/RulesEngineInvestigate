from dataclasses import dataclass

import rule_engine
from rule_engine.builtins import Builtins


class ControlLimitException(Exception):
    pass


def subtract_lists(a, b):
    return [a_i - b_i for a_i, b_i in zip(a, b)]


@dataclass
class SieveResult:
    name: str
    # example one of eg:  ["3/4\"", "1/2\"", "3/8\"", "No.8", "No.4"],
    pc_retained: float
    cum_passing_pct: float
    cum_retained_pct: float


@dataclass
class SieveData:
    # Annotated[Literal["ASTM", "CSA"] | None, Field(examples=["ASTM"],
    sieve_size: list[str]
    # examples=["3/4\"", "1/2\"", "3/8\"", "No.8", "No.4"],
    pc_retained: list[float]
    # examples=[0.0, 40.0, 50.0, 10.0, 0.0],
    cum_passing_pct: list[float]
    # examples=[100.0, 60.0, 50.0, 90.0, 100.0],
    cum_retained_pct: list[float]
    # examples=[100.0, 60.0, 50.0, 90.0, 100.0],
    sieve_standard: str = "astm"

    def get_sieve_data(self, item: str):
        index = self.sieve_size.index(item)
        datum = SieveResult(
            name=item,
            pc_retained=self.pc_retained[index],
            cum_passing_pct=self.cum_passing_pct[index],
            cum_retained_pct=self.cum_retained_pct[index],
        )
        return datum

    def __sub__(self, other: "SieveData"):
        return SieveData(
            sieve_size=self.sieve_size,
            pc_retained=subtract_lists(self.pc_retained, other.pc_retained),
            cum_passing_pct=subtract_lists(
                self.cum_retained_pct, other.cum_passing_pct
            ),
            cum_retained_pct=subtract_lists(
                self.cum_retained_pct, other.cum_retained_pct
            ),
        )


class CustomBuiltinsContext(rule_engine.Context):
    def __init__(self, *args, **kwargs):
        super(CustomBuiltinsContext, self).__init__(*args, **kwargs)
        self.builtins = Builtins.from_defaults(
            {
                "startswith": lambda x, y: y.startswith(x),
                "contains": lambda x, y: x in y,
            },
        )


def apply_rule(rule, data, data_types=None):
    rule = convert_from_if_then_format(rule)

    using_dicts = type(data) == dict
    resolver = None if using_dicts else rule_engine.resolve_attribute
    type_resolver = data_types
    context = CustomBuiltinsContext(resolver=resolver, type_resolver=type_resolver)
    r = rule_engine.Rule(rule, context=context).matches(data)
    return r


def convert_from_if_then_format(rule):
    # convert if...require syntax to ternary operator format
    if rule.startswith("if "):
        rule = rule.replace("if ", "")
        rule = rule.replace(" require ", " ? ")
        rule += " : true"
    return rule


def sieve_data_conforms(data: SieveData, rules: list[str]) -> bool:
    for sieve_size in data.sieve_size:
        sieve_data = data.get_sieve_data(sieve_size)
        for rule in rules:
            row_result = apply_rule(rule, sieve_data)
            if row_result == False:
                raise ControlLimitException(f"Rule {rule} failed for {sieve_data}  ")
    return True


def range_sieve_check(name, lt, gt) -> str:
    return f'if name == "{name}" require (pc_retained >={lt}  and pc_retained <= {gt})'
