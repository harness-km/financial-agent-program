"""Where our code decides whether to honour what the model asked for.

The model never calls a tool. It emits JSON asking for one, and this file
decides. Everything in weeks 4 to 16 is a bigger version of that decision.

Two arguments carry the decision, and they look redundant this week:

- `allowed` is what the model is permitted to ask for.
- `registry` is what this process is willing to execute.

They are not the same question, and in week 4 they become the two halves of the
pre-tool hook. Keeping them apart now is why that is a small change later.

Everything here fails closed. A response shape we do not recognise raises
rather than returning a default, because the only alternative to refusing is
handing the model something it will treat as an answer.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Collection, Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class ToolCall:
    """One validated request to run one tool.

    Frozen on purpose: once this exists, the request has been checked, and
    nothing downstream may quietly edit what was approved.
    """

    name: str
    arguments: dict


def parse_tool_call(response: dict, allowed: Collection[str]) -> ToolCall | None:
    """Pull one validated tool call out of a raw model response.

    Returns `None` when the model answered in prose and asked for nothing, which
    is allowed. Raises `ValueError` for everything else it does not recognise.

    Only `tool_calls[0]` is considered. Parallel tool calls are week 4's problem.
    """
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError(f"No choices in the model response: {response!r}")

    first_choice = choices[0]
    message = first_choice.get("message") if isinstance(first_choice, dict) else None
    if not isinstance(message, dict):
        raise ValueError(f"No message in the first choice: {first_choice!r}")

    tool_calls = message.get("tool_calls")
    if not tool_calls:
        return None

    function = tool_calls[0].get("function") if isinstance(tool_calls[0], dict) else None
    if not isinstance(function, dict):
        raise ValueError(f"Malformed tool call: {tool_calls[0]!r}")

    name = function.get("name")
    if name not in allowed:
        raise ValueError(f"The model asked for {name!r}, which is not in allowed: {set(allowed)}")

    try:
        arguments = json.loads(function.get("arguments") or "")
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError(f"Arguments for {name!r} are not valid JSON: {error}") from error

    if not isinstance(arguments, dict):
        raise ValueError(
            f"Arguments for {name!r} decoded to {type(arguments).__name__}, not an object"
        )

    return ToolCall(name=name, arguments=arguments)


def run_tool_call(call: ToolCall, registry: Mapping[str, Callable[..., object]]) -> str:
    """Invoke the named tool and return its result as a string.

    An argument the tool does not accept raises `TypeError` from Python itself,
    and we let it: the tool does not run, which is the behaviour we want. Week 4
    is where every refusal gets one name and one place to live.
    """
    if call.name not in registry:
        raise ValueError(f"{call.name!r} is not a registered tool: {sorted(registry)}")
    return str(registry[call.name](**call.arguments))
