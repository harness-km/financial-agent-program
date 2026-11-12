"""One raw model call. Nothing else.

This file posts a request and hands back the decoded JSON exactly as it arrived.
It does not parse it, judge it, retry it or reshape it — `dispatch.py` decides
what to honour, and keeping the two apart is the whole point of the week. A
module that both fetched and interpreted would hide the moment where our code
takes responsibility for the model's output.

No retries, no backoff, no timeout, no streaming: one `requests.post`. Each of
those is a real concern and each is a later week's, added once there is a reason
rather than because an assistant offered it.

The API key is read from the environment inside `call_model`. It is deliberately
not a parameter: a key that can be passed in is a key that ends up in a notebook
cell, in a prompt pasted into Discussions, and by week 7 in every trace file.
"""

from __future__ import annotations

import os

import requests

from fin_agent import config

API_URL = "https://api.openai.com/v1/chat/completions"


def call_model(messages: list[dict], tools: list[dict]) -> dict:
    """POST one chat completion request and return the decoded JSON unchanged."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Put it in your .env file (see .env.example) "
            "and restart the kernel, or run scripts/doctor.py to check your setup."
        )

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": config.MODEL, "messages": messages, "tools": tools},
    )
    response.raise_for_status()
    return response.json()
