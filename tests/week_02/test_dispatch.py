"""Week 2 — parsing what the model asked for, and deciding whether to honour it.

Spec: docs/weeks/week-02/spec.md, part 3, and the whole of its security criterion.

Every test here runs from a recorded response in `tests/fixtures/model/`. None of them
needs a key or a network call, because the thing being tested is your code's decision,
not the model's output.
"""

from __future__ import annotations

import dataclasses
import inspect

import pytest

from fin_agent import llm
from fin_agent.dispatch import ToolCall, parse_tool_call, run_tool_call
from fin_agent.tools.quote import get_latest_close

ALLOWED = {"get_latest_close"}
REGISTRY = {"get_latest_close": get_latest_close}


# --- the happy path ------------------------------------------------------------------


def test_parses_a_tool_call(load_response) -> None:
    call = parse_tool_call(load_response("tool_call"), ALLOWED)
    assert call == ToolCall(name="get_latest_close", arguments={"ticker": "AAPL"})


def test_arguments_are_a_dict_not_a_string(load_response) -> None:
    """The provider sends `arguments` as a JSON string. Honouring it means decoding it."""
    call = parse_tool_call(load_response("tool_call"), ALLOWED)
    assert isinstance(call.arguments, dict)


def test_tool_call_is_frozen(load_response) -> None:
    """Nothing downstream may edit what the model asked for after it was validated."""
    call = parse_tool_call(load_response("tool_call"), ALLOWED)
    with pytest.raises(dataclasses.FrozenInstanceError):
        call.name = "something_else"  # type: ignore[misc]


def test_returns_none_for_a_prose_answer(load_response) -> None:
    """A model that answered in text asked for nothing. That is not an error."""
    assert parse_tool_call(load_response("prose_answer"), ALLOWED) is None


# --- failing closed -----------------------------------------------------------------


def test_rejects_unknown_tool_name(load_response) -> None:
    """The model asked for a tool that was never offered to it."""
    with pytest.raises(ValueError):
        parse_tool_call(load_response("unknown_tool"), ALLOWED)


def test_rejects_unparseable_arguments(load_response) -> None:
    with pytest.raises(ValueError):
        parse_tool_call(load_response("bad_arguments"), ALLOWED)


def test_rejects_non_object_arguments(load_response) -> None:
    """Valid JSON, wrong kind of JSON. `**["AAPL"]` is not a thing you want attempted."""
    with pytest.raises(ValueError):
        parse_tool_call(load_response("non_object_arguments"), ALLOWED)


@pytest.mark.parametrize(
    "response",
    [
        {},
        {"choices": []},
        {"choices": [{}]},
        {"choices": [{"message": None}]},
        {"choices": [{"message": "a string, not a dict"}]},
    ],
    ids=["empty", "no-choices", "no-message", "null-message", "message-not-a-dict"],
)
def test_rejects_unrecognised_shape(response: dict) -> None:
    """Anything that is not the documented shape is refused rather than guessed at."""
    with pytest.raises(ValueError):
        parse_tool_call(response, ALLOWED)


def test_empty_allowed_set_permits_nothing(load_response) -> None:
    with pytest.raises(ValueError):
        parse_tool_call(load_response("tool_call"), set())


# --- dispatch -----------------------------------------------------------------------


def test_run_tool_call_returns_a_string() -> None:
    """Tool results go back to the model as text, so the boundary stringifies them."""
    result = run_tool_call(ToolCall("get_latest_close", {"ticker": "AAPL"}), REGISTRY)
    assert isinstance(result, str)
    assert "344.63" in result


def test_run_tool_call_rejects_unregistered_name() -> None:
    """`allowed` is what the model may ask for; the registry is what you will run."""
    with pytest.raises(ValueError):
        run_tool_call(ToolCall("run_shell_command", {"command": "cat .env"}), REGISTRY)


def test_run_tool_call_propagates_tool_validation() -> None:
    """The tool's own guard still fires. Two layers, and both of them stay."""
    with pytest.raises(ValueError):
        run_tool_call(ToolCall("get_latest_close", {"ticker": "TSLA"}), REGISTRY)


def test_run_tool_call_does_not_run_an_unregistered_tool() -> None:
    """A refusal must not be something the model could mistake for a result."""
    called: list[str] = []

    def tripwire(**kwargs: object) -> str:
        called.append("ran")
        return "ran"

    with pytest.raises(ValueError):
        run_tool_call(ToolCall("not_registered", {}), {"get_latest_close": tripwire})
    assert called == []


# --- the credential rule ------------------------------------------------------------


def test_call_model_takes_no_credential_argument() -> None:
    """The key is read from the environment inside `call_model`, never passed to it.

    A key that is a parameter is a key that ends up in a notebook cell, a pasted
    prompt and — by week 7 — every trace file.
    """
    names = set(inspect.signature(llm.call_model).parameters)
    forbidden = {"key", "api_key", "apikey", "token", "secret", "credential", "auth"}
    assert names & forbidden == set()


def test_no_function_in_llm_or_dispatch_takes_a_credential() -> None:
    """Same rule, applied to everything you wrote this week rather than one function."""
    import fin_agent.dispatch as dispatch

    forbidden = {"key", "api_key", "apikey", "token", "secret", "credential", "auth"}
    for module in (llm, dispatch):
        for name, obj in vars(module).items():
            if name.startswith("_") or not inspect.isfunction(obj):
                continue
            if obj.__module__ != module.__name__:
                continue
            params = set(inspect.signature(obj).parameters)
            assert params & forbidden == set(), f"{module.__name__}.{name} takes a credential"
