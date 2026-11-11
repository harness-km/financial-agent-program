# Recorded model responses

Real chat-completion responses, saved so that the code which parses them can be tested without a
key, a network call or a bill.

They are what `conftest.py`'s `load_response` fixture reads:

```python
def test_something(load_response):
    response = load_response("tool_call")
```

| File | What it is | What it should make your code do |
| --- | --- | --- |
| `tool_call.json` | a well-formed request to call `get_latest_close` for AAPL | parse to `ToolCall("get_latest_close", {"ticker": "AAPL"})` |
| `prose_answer.json` | the model answered in text and asked for no tool | return `None` — this is not an error |
| `unknown_tool.json` | a request to call a tool that was never offered | raise `ValueError` |
| `bad_arguments.json` | `arguments` is a truncated JSON string | raise `ValueError` |
| `non_object_arguments.json` | `arguments` decodes to a list, not an object | raise `ValueError` |

The last three are the week 2 security criterion. None of them is a hypothetical: a model that has
read a web page, a filing or a document someone else wrote can emit any of them, and
`unknown_tool.json` is what that looks like when it goes badly.

The `usage` block in each file is real. If you have no model key in week 2, those token counts are
the ones to put in your ledger row — say in your pull request that they came from here rather than
from a run of your own.

Do not edit these files. Several weeks of tests assert against their exact contents. If you want a
response of your own to experiment with, save it beside your notebook instead.
