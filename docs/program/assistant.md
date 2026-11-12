# Your AI assistant

You are going to specify code and have an assistant write it. That is the intended way to work on
this course, not a shortcut around it, and nobody is going to ask you to type a `for` loop from
memory.

This guide covers choosing one and setting it up. How to *direct* it well is
[`ai-assistant-rules.md`](ai-assistant-rules.md), which is seven rules and the most re-read
document in the repository. Read this one first, that one from week 2.

## Which one

Claude, Gemini or ChatGPT. All three can do everything this course asks.

| | |
| --- | --- |
| **Claude** | [claude.ai](https://claude.ai) |
| **Gemini** | [gemini.google.com](https://gemini.google.com) |
| **ChatGPT** | [chatgpt.com](https://chatgpt.com) |

Use whichever you already have, or whichever your employer permits. If you have no preference,
pick one and stay with it for the sixteen weeks — the useful skill here is learning how *your*
assistant goes wrong, and that resets when you switch.

**Free or paid?** Free tiers work. You will hit usage limits in the busier weeks, usually at the
least convenient moment, and a paid tier removes that. Start free. Upgrade if the limits start
costing you evenings.

**This is separate from your agent's API key.** From week 4 your own code starts calling a model
directly, and that needs a key, which is billed by usage and costs a few dollars a week. The
assistant you are chatting with and the model your code calls are two different accounts with two
different bills. `setup.md` covers the key when you need it, which is not yet.

## Set it up in a separate window

Keep VS Code in one window and your assistant in another — a browser tab is fine — and copy code
across by hand.

Not side by side in the same editor. Not a plugin. Two windows, and you moving text between them.

**This is deliberate, and it is the most important sentence in this guide.** Tools that write
into your files directly are excellent and you should use them in your work. Here they would ruin
the course, for a specific reason: they let you accumulate hundreds of lines you have never
actually read. You get working code and no idea why it works, and then week 6 breaks for a reason
planted in week 3, and you cannot find it because you have never read the file.

Code you paste yourself is code you glance at. That glance is most of what keeps you oriented
over sixteen weeks. It is a small tax, paid weekly, and it is the difference between finishing
and stalling around week 10.

## What to expect from it

Three things about assistants that are worth knowing before you are surprised by them.

**It is confident when it is wrong.** It will not sound uncertain when it invents a function that
does not exist. Tone tells you nothing about accuracy, which is a hard habit to unlearn because
tone tells you a great deal about accuracy in people.

**It will agree with you when you are wrong.** Say "this is broken because of X" and it will
usually help you fix X, even if X was fine. Try asking "what else could cause this?" before
committing to a theory.

**It cannot know what you meant.** It only has your words. This is why the course gives you a
written spec every week and asks you to prompt from it — the spec is the part that does the work,
and a vague request produces a confident, fluent, wrong answer rather than a question.

The tests are the arbiter. Not the assistant's assurance that the code is correct, and not yours.
Run them.

## A first conversation

Nothing to do until week 2, but if you want to try the shape now, this is roughly how a week
goes:

> I'm writing one Python function. It reads a JSON file at `cache/AAPL/income.json`, takes the
> list under the `data` key, sorts it by `fiscal_year` newest first, and returns the first three.
> No other functions, no classes, no error handling beyond raising `ValueError` on a bad ticker.
> Describe how you'd do it in four sentences, then stop.

Three things make that work, and you will do all three every week: it says exactly what is wanted,
it says what is *not* wanted, and it asks for the approach before the code. That last one costs
one exchange and saves you reading a hundred lines in order to reject them.

Compare it with "write me a tool that gets financial data for a stock", which produces a class
hierarchy, a caching layer, three retry strategies and an abstract base class nobody asked for.
We do exactly that comparison live in week 2. It is funnier than it sounds.

## Keeping your prompts

Every week you post the prompts you used, including the ones that went wrong, and the Definition
of Done calls this the item that carries the most weight.

So keep them as you go. A scratch file in your project folder is enough — your assistant's own
history works too, but it is harder to quote from. Reconstructing a week's prompts on a Sunday
evening from memory produces a tidy fiction, and the tidy version is worth nothing to anybody.

The failed prompts are the useful ones. Everyone's working code looks much the same by Friday.
How you got there is the part worth reading, and the part worth writing down.
