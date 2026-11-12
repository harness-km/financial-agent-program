"""Week 3 — the schema is the prompt surface.

Spec: docs/weeks/week-03/spec.md.

The other three files in this folder check what your tools return. This one checks
what the model is told about them before it calls anything, which is the part you
cannot see going wrong: a schema whose parameter names drift from the function's
signature produces a tool call your code rejects, and the model has no way to know
why. An assistant writing the schema separately from the function gets this wrong
often enough to be worth a test.

Nothing here judges whether a description is any good. That is what the live
misuse demo is for.
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from types import ModuleType

import pytest

from fin_agent.config import TICKERS
from fin_agent.tools import financials, news, prices

TOOLS: list[tuple[ModuleType, Callable[..., object]]] = [
    (financials, financials.get_income_statement),
    (prices, prices.get_prices),
    (news, news.get_news),
]

IDS = [function.__name__ for _, function in TOOLS]

MIN_DESCRIPTION = 20


@pytest.mark.parametrize(("module", "function"), TOOLS, ids=IDS)
def test_module_exports_a_schema(module: ModuleType, function: Callable[..., object]) -> None:
    """One `SCHEMA` per tool module, beside the function it describes.

    Week 4 collects these into the list it hands the model. Keeping each one next
    to its own function is why that collection is a loop rather than a file of
    hand-maintained duplicates.
    """
    assert isinstance(getattr(module, "SCHEMA", None), dict)


@pytest.mark.parametrize(("module", "function"), TOOLS, ids=IDS)
def test_schema_is_a_function_tool(module: ModuleType, function: Callable[..., object]) -> None:
    assert module.SCHEMA["type"] == "function"
    assert isinstance(module.SCHEMA["function"], dict)


@pytest.mark.parametrize(("module", "function"), TOOLS, ids=IDS)
def test_schema_name_matches_the_function(
    module: ModuleType, function: Callable[..., object]
) -> None:
    """A mismatch here is a tool the model asks for and your registry does not have."""
    assert module.SCHEMA["function"]["name"] == function.__name__


@pytest.mark.parametrize(("module", "function"), TOOLS, ids=IDS)
def test_schema_has_a_real_description(module: ModuleType, function: Callable[..., object]) -> None:
    """The one thing the model reads before deciding whether this tool fits."""
    description = module.SCHEMA["function"].get("description", "")
    assert len(description.strip()) >= MIN_DESCRIPTION


@pytest.mark.parametrize(("module", "function"), TOOLS, ids=IDS)
def test_function_has_a_docstring(module: ModuleType, function: Callable[..., object]) -> None:
    """For the next person reading the code, which is you in week 7."""
    assert (function.__doc__ or "").strip()


@pytest.mark.parametrize(("module", "function"), TOOLS, ids=IDS)
def test_parameters_match_the_signature(
    module: ModuleType, function: Callable[..., object]
) -> None:
    """Every argument the function takes, declared, and nothing it does not."""
    declared = set(module.SCHEMA["function"]["parameters"]["properties"])
    actual = set(inspect.signature(function).parameters)
    assert declared == actual


@pytest.mark.parametrize(("module", "function"), TOOLS, ids=IDS)
def test_required_matches_arguments_without_defaults(
    module: ModuleType, function: Callable[..., object]
) -> None:
    """`ticker` is required; `years`, `days` and `limit` have defaults and are not."""
    required = set(module.SCHEMA["function"]["parameters"].get("required", []))
    expected = {
        name
        for name, parameter in inspect.signature(function).parameters.items()
        if parameter.default is inspect.Parameter.empty
    }
    assert required == expected


@pytest.mark.parametrize(("module", "function"), TOOLS, ids=IDS)
def test_every_parameter_is_described(module: ModuleType, function: Callable[..., object]) -> None:
    """An undescribed parameter is one the model fills in from the name alone."""
    properties = module.SCHEMA["function"]["parameters"]["properties"]
    undescribed = [name for name, spec in properties.items() if not spec.get("description")]
    assert undescribed == []


@pytest.mark.parametrize(("module", "function"), TOOLS, ids=IDS)
def test_ticker_is_constrained_to_the_programme_tickers(
    module: ModuleType, function: Callable[..., object]
) -> None:
    """The allowlist told to the model, not only enforced after it guesses.

    Your tool raises `ValueError` for anything outside `config.TICKERS`, and it
    keeps doing that. But a refusal the model could have avoided is a wasted call
    and a confusing trace, so the same list goes in the schema. Two expressions of
    one rule, from one source.
    """
    ticker = module.SCHEMA["function"]["parameters"]["properties"]["ticker"]
    assert ticker["enum"] == list(TICKERS)


@pytest.mark.parametrize(("module", "function"), TOOLS, ids=IDS)
def test_parameters_object_is_well_formed(
    module: ModuleType, function: Callable[..., object]
) -> None:
    parameters = module.SCHEMA["function"]["parameters"]
    assert parameters["type"] == "object"
    assert isinstance(parameters["properties"], dict)
