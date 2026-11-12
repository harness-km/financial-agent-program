# VS Code, for people who have never used it

VS Code is a text editor. That is genuinely all it is — it opens files and lets you change them,
like Notepad or TextEdit. Everything else it does is an optional extra that happens to be very
good.

You will spend sixteen weeks in it, so twenty minutes now learning four things is a good trade.
Those four things are: open a folder, find a file, use the terminal, and pick the right Python.
The last one causes more confusion on this course than the other three put together, so it gets
the most space.

## Install it

Download from [code.visualstudio.com](https://code.visualstudio.com/) and install it the normal
way. There is a free version and there is no other version; if a site offers to sell it to you,
you are on the wrong site.

## Open the course folder, not a file

This is the first habit worth forming.

**File → Open Folder**, then choose the `financial-agent-program` folder you cloned. Not a file
inside it — the folder itself.

**Why it matters.** VS Code behaves completely differently depending on whether you opened a file
or a folder. With a folder open it knows about your project: it finds your Python environment, it
runs tests, its terminal starts in the right place, and the file list down the left actually has
something in it. Open a single file and almost nothing on this course works, and the reason will
not be obvious.

If you ever find that tests pass in a terminal but fail in VS Code, or that nothing shows in the
sidebar, check this first. It is the answer about a third of the time.

The first time you open the folder, VS Code asks whether you trust the authors. Yes — it is your
own clone of a public repository you just looked at.

## The bits of the window

| Where | What it is |
| --- | --- |
| Left strip of icons | The activity bar. Files, search, source control, extensions |
| The panel beside it | Whatever you clicked. Mostly you want the top icon, Explorer — your files |
| The big area | Your open files, in tabs |
| The bottom | The terminal, when you open it |

You can close, move or hide any of it. Nothing is load-bearing.

## Install the recommended extensions

When you first open the folder, a small box appears in the bottom right offering the recommended
extensions. Say yes.

If you miss it, click the Extensions icon in the left strip, type `@recommended` in the search
box, and install what it lists.

**Why.** The repo ships a list of extensions it expects — Python support, Jupyter notebooks, and
a few smaller things. Installing them means your editor behaves the same as everyone else's,
which matters a great deal when someone is helping you with a problem over a screen share.

## The terminal

**Ctrl and the backtick key** opens a terminal at the bottom. Backtick is the one above Tab,
left of the 1.

A terminal is a place to type commands. That is the whole concept. Everything on this course that
is not typing code is typing a short command into this box: `pytest`, `git pull`,
`python scripts/doctor.py`.

Two useful things about VS Code's version specifically:

It starts in your project folder, so commands act on the right files without you navigating
anywhere. And it notices your Python environment, so you do not have to activate it by hand every
time.

Trash a terminal with the bin icon if it gets into a state. Opening a fresh one fixes a
surprising number of problems and costs nothing.

## Picking the right Python

Here is the one that catches people, including people who have been doing this for years.

Your computer can have several Pythons on it: one that came with the operating system, maybe one
you installed, and the one this course sets up in a folder called `.venv` inside your project.
They are separate, and they do not share installed packages.

The course's Python is the only one that has the course's packages. If VS Code is pointed at a
different one, your code will say it cannot find things that are plainly installed, and you will
doubt your sanity for a while.

**Point VS Code at the right one.** Press `Ctrl+Shift+P`, type `Python: Select Interpreter`,
press Enter, and choose the entry with `.venv` in its path. It is usually marked "Recommended".

`Ctrl+Shift+P` opens the command palette, by the way — a search box for everything VS Code can
do. It is the single most useful key combination in the program. If you ever cannot find a menu
item, press it and type what you want.

**How to tell it worked.** Look at the bottom-right of the window while a Python file is open.
It shows the interpreter. You want the one saying `.venv`.

**The symptom when it is wrong**, so you recognise it later: `pytest` works in the terminal but
the editor underlines your imports in red, or a notebook cell fails on an import that the
terminal is perfectly happy with. Same cause every time. Select the interpreter again.

## Running the tests

Open a terminal and type:

```bash
pytest tests/week_01
```

That is the whole of it. There is also a beaker icon in the left strip that runs tests with a
mouse, and some people prefer it. Either is fine; the command is what the course documents,
because it is the same on everyone's machine.

## Notebooks

Weeks 2 onwards use notebook files — `.ipynb` — which are documents with code cells you can run
one at a time. Open one from the Explorer and it just works, provided the Jupyter extension is
installed and your interpreter is set.

Run a cell with `Shift+Enter`. The first run of a session takes a few seconds while Python wakes
up. After that it is instant.

One thing worth knowing: cells remember what you ran, not what is on screen. If you edit a cell
and do not re-run it, the old version is still what Python thinks. When a notebook starts
behaving impossibly, run everything from the top — there is a **Restart** and a **Run All** in
the toolbar — and the impossibility usually goes away.

## Markdown preview

The specs and guides are `.md` files. They are readable as plain text, but `Ctrl+Shift+V` shows
them formatted, which is nicer for the longer ones.

## A few keys worth knowing

| Keys | Does |
| --- | --- |
| `Ctrl+Shift+P` | Command palette — search everything VS Code can do |
| `Ctrl+P` | Jump to a file by typing part of its name |
| Ctrl and backtick | Terminal |
| `Ctrl+S` | Save |
| `Ctrl+F` | Find in this file |
| `Ctrl+Shift+F` | Find across every file in the project |
| `Ctrl+/` | Comment out the selected lines |

On a Mac, Cmd instead of Ctrl throughout.

## If something looks broken

**The sidebar is empty.** You opened a file rather than a folder. File → Open Folder.

**Imports are underlined in red but the code runs.** Interpreter. `Ctrl+Shift+P`, Select
Interpreter, pick `.venv`.

**A terminal command is not found.** Check you are in the project folder — the prompt shows
where you are. `cd` into it if not.

**Everything is wrong and you do not know why.** Close VS Code, open it again, open the folder.
This is not a joke; it is a real first step and it works more often than it should.

**Still wrong.** Post the full output of `python scripts/doctor.py` to the Help category in
Discussions. Full output, not a summary — the useful line is almost always one of the ones people
trim.
